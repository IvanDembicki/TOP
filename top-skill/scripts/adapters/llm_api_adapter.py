#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def sha256_file(path):
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def resolve_ref(root, ref, label):
    if not ref:
        raise ValueError(f"{label} is required")
    candidate = Path(ref)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes adapter root: {ref}") from exc
    return resolved


def find_skill_root(root):
    for candidate in [root, *root.parents]:
        if (candidate / "skill.json").exists() and (candidate / "scripts").exists():
            return candidate.resolve()
    return root


def resolve_input_ref(root, ref):
    try:
        path = resolve_ref(root, ref, "input reference")
        if path.exists():
            return path, "run-root"
    except ValueError:
        pass

    skill_root = find_skill_root(root)
    candidate = Path(ref)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (skill_root / candidate).resolve()
    try:
        resolved.relative_to(skill_root)
    except ValueError as exc:
        raise ValueError(f"input reference escapes skill root: {ref}") from exc
    return resolved, "skill-root"


def read_ref_text(root, ref, byte_limit):
    path, resolved_from = resolve_input_ref(root, ref)
    if not path.exists() or not path.is_file():
        return {
            "ref": ref,
            "resolvedFrom": resolved_from,
            "status": "missing",
            "sha256": None,
            "content": None,
        }
    data = path.read_bytes()
    truncated = len(data) > byte_limit
    text = data[:byte_limit].decode("utf-8", errors="replace")
    return {
        "ref": ref,
        "resolvedFrom": resolved_from,
        "status": "truncated" if truncated else "read",
        "sha256": hashlib.sha256(data).hexdigest(),
        "content": text,
    }


def compact_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False)


def extract_json_object(text):
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("model response did not contain a JSON object")
    return json.loads(stripped[start : end + 1])


def handoff_template(context_package, task_capsule, handoff_ref):
    pass_id = context_package.get("passId")
    role = task_capsule.get("role")
    return {
        "schemaVersion": "1.0",
        "workflowId": context_package.get("workflowId"),
        "passId": pass_id,
        "taskId": task_capsule.get("taskId"),
        "role": role,
        "agentName": f"{role}-llm-api-pass",
        "taskCapsuleRef": context_package.get("taskCapsuleRef"),
        "inputReferences": task_capsule.get("inputReferences", []),
        "outputReferences": [handoff_ref],
        "filesRead": [context_package.get("taskCapsuleRef"), os.environ.get("TOP_CONTEXT_PACKAGE", "")],
        "filesChanged": [handoff_ref],
        "commandsRun": ["scripts/adapters/llm_api_adapter.py"],
        "status": "done",
        "executionEvidence": protocol_evidence([
            "Pass handoff may claim only protocol-followed-by-agent evidence; runner-enforced evidence is assigned by the runner."
        ]),
        "limitations": [],
        "didNotDo": task_capsule.get("forbiddenActions", []),
        "handoffTo": "orchestrator",
        "mayEditFiles": bool(task_capsule.get("mayEditFiles")),
        "mayValidate": bool(task_capsule.get("mayValidate")),
        "mayRepair": bool(task_capsule.get("mayRepair")),
        "mayReport": bool(task_capsule.get("mayReport")),
        "mayCertifyDelivery": bool(task_capsule.get("mayCertifyDelivery")),
    }


def build_prompt(context_package, task_capsule, referenced_inputs, handoff_ref):
    system = (
        "You are executing one Tree-Oriented Programming orchestration pass. "
        "Use only the supplied task capsule, context package, and referenced inputs. "
        "Do not rely on hidden chat memory. Return exactly one JSON object. "
        "When artifact writes are not requested, that object must match the TOP "
        "handoff artifact contract. When artifact writes are requested, that "
        "object must contain `handoff` and `artifactWrites`. Do not wrap it in Markdown."
    )
    artifact_write_requests = task_capsule.get("artifactWriteRequests", [])
    user = {
        "instruction": "Write the pass handoff artifact.",
        "expectedHandoffRef": handoff_ref,
        "contextPackage": context_package,
        "taskCapsule": task_capsule,
        "referencedInputs": referenced_inputs,
        "requiredOutputShape": handoff_template(context_package, task_capsule, handoff_ref),
        "allowedArtifactWrites": artifact_write_requests,
        "allowedStatusValues": ["done", "blocked", "failed", "partial", "not-certified"],
        "hardRules": [
            "One pass writes exactly one handoff and stops.",
            "`status` describes this pass handoff, not final delivery certification.",
            "Use status `done` when the assigned pass completed its handoff without a blocking failure.",
            "The pass must not certify delivery unless its capsule grants mayCertifyDelivery.",
            "The pass must not claim runner-enforced isolation; the runner decides that from invocation evidence.",
            "Executive and repair passes must not validate their own output.",
            "Artifact writes are allowed only when artifactWriteRequests lists the exact ref.",
            "When artifactWriteRequests is non-empty, return an object with keys `handoff` and `artifactWrites`.",
            "Each artifactWrites item must have `ref` and string `content` containing the complete file text.",
            "Return JSON only and do not add fields outside the required handoff contract inside the handoff object.",
        ],
    }
    return system, compact_json(user)


def openai_responses_call(endpoint, api_key, model, system_prompt, user_prompt, timeout_seconds):
    payload = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8")
    data = json.loads(body)
    return data, extract_response_text(data)


def extract_response_text(data):
    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    chunks = []
    for item in data.get("output", []) if isinstance(data.get("output"), list) else []:
        for content in item.get("content", []) if isinstance(item, dict) else []:
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str):
                chunks.append(text)
    if chunks:
        return "\n".join(chunks)
    raise ValueError("response did not contain output text")


def protocol_evidence(limitations):
    return {
        "executionIsolationLevel": "protocol-followed-by-agent",
        "verificationEvidenceLevel": "agent-claimed",
        "runnerName": None,
        "separateInvocationIds": [],
        "schemaValidationCommand": None,
        "hardCheckCommands": [],
        "limitations": limitations,
    }


def failure_handoff(workflow_id, pass_id, task_capsule, refs, message):
    role = task_capsule.get("role", "executive")
    return {
        "schemaVersion": "1.0",
        "workflowId": workflow_id,
        "passId": pass_id,
        "taskId": task_capsule.get("taskId", f"{pass_id}-task"),
        "role": role,
        "agentName": f"{role}-llm-api-adapter",
        "taskCapsuleRef": refs["taskCapsuleRef"],
        "inputReferences": task_capsule.get("inputReferences", []),
        "outputReferences": [refs["handoffArtifactRef"]],
        "filesRead": [refs["contextPackageRef"], refs["taskCapsuleRef"]],
        "filesChanged": [refs["handoffArtifactRef"]],
        "commandsRun": ["scripts/adapters/llm_api_adapter.py"],
        "status": "failed",
        "executionEvidence": protocol_evidence([message]),
        "limitations": [message],
        "didNotDo": task_capsule.get("forbiddenActions", ["certify delivery"]),
        "handoffTo": "orchestrator",
        "mayEditFiles": bool(task_capsule.get("mayEditFiles")),
        "mayValidate": bool(task_capsule.get("mayValidate")),
        "mayRepair": bool(task_capsule.get("mayRepair")),
        "mayReport": bool(task_capsule.get("mayReport")),
        "mayCertifyDelivery": bool(task_capsule.get("mayCertifyDelivery")),
    }


def normalize_model_handoff(handoff, workflow_id, run_id, pass_id, task_capsule, refs):
    if not isinstance(handoff, dict):
        raise ValueError("handoff must be a JSON object")
    if handoff.get("workflowId") != workflow_id:
        raise ValueError("handoff workflowId does not match context package")
    if handoff.get("passId") != pass_id:
        raise ValueError("handoff passId does not match context package")
    if handoff.get("taskId") != task_capsule.get("taskId"):
        raise ValueError("handoff taskId does not match task capsule")
    if handoff.get("role") != task_capsule.get("role"):
        raise ValueError("handoff role does not match task capsule")
    evidence = handoff.get("executionEvidence")
    if isinstance(evidence, dict) and evidence.get("executionIsolationLevel") == "runner-enforced":
        raise ValueError("pass handoff must not self-claim runner-enforced isolation")
    if handoff.get("taskCapsuleRef") not in {None, refs["taskCapsuleRef"]}:
        raise ValueError("handoff taskCapsuleRef does not match task capsule")

    handoff.setdefault("agentName", f"{task_capsule.get('role')}-llm-api-pass")
    handoff.setdefault("taskCapsuleRef", refs["taskCapsuleRef"])
    handoff.setdefault("inputReferences", task_capsule.get("inputReferences", []))
    handoff.setdefault("outputReferences", [])
    handoff.setdefault("filesRead", [refs["contextPackageRef"], refs["taskCapsuleRef"]])
    handoff.setdefault("filesChanged", [refs["handoffArtifactRef"]])
    handoff.setdefault("commandsRun", ["scripts/adapters/llm_api_adapter.py"])
    handoff.setdefault(
        "executionEvidence",
        protocol_evidence(["Adapter normalized missing pass execution evidence to protocol-followed-by-agent."]),
    )
    handoff.setdefault("limitations", [])
    handoff.setdefault("didNotDo", task_capsule.get("forbiddenActions", ["certify delivery"]))
    handoff.setdefault("handoffTo", "orchestrator")
    for key in ["mayEditFiles", "mayValidate", "mayRepair", "mayReport", "mayCertifyDelivery"]:
        handoff.setdefault(key, bool(task_capsule.get(key)))
    return handoff


def split_model_output(model_output):
    if isinstance(model_output, dict) and "handoff" in model_output:
        handoff = model_output.get("handoff")
        artifact_writes = model_output.get("artifactWrites", [])
        if not isinstance(artifact_writes, list):
            raise ValueError("artifactWrites must be an array")
        return handoff, artifact_writes
    return model_output, []


def apply_artifact_writes(root, task_capsule, artifact_writes):
    requests = task_capsule.get("artifactWriteRequests", []) or []
    allowed = {
        item.get("ref"): item
        for item in requests
        if isinstance(item, dict) and isinstance(item.get("ref"), str)
    }
    if artifact_writes and not task_capsule.get("mayEditFiles"):
        raise ValueError("artifact writes require mayEditFiles true")
    if artifact_writes and not allowed:
        raise ValueError("artifact writes were returned but no artifactWriteRequests are allowed")

    written = []
    seen = set()
    for item in artifact_writes:
        if not isinstance(item, dict):
            raise ValueError("artifact write must be an object")
        ref = item.get("ref")
        content = item.get("content")
        if ref not in allowed:
            raise ValueError(f"artifact write ref is not allowed: {ref!r}")
        if not isinstance(content, str):
            raise ValueError(f"artifact write content must be a string for {ref!r}")
        path = resolve_ref(root, ref, "artifact write ref")
        write_text(path, content)
        written.append({"ref": ref, "sha256": sha256_file(path)})
        seen.add(ref)

    missing = [
        ref
        for ref, request in allowed.items()
        if request.get("required") is True and ref not in seen
    ]
    if missing:
        raise ValueError(f"missing required artifact writes: {', '.join(missing)}")
    return written


def build_invocation_evidence(
    args,
    context_package,
    task_capsule,
    refs,
    started_at,
    ended_at,
    response_data,
    handoff_path,
    model_invocation,
    artifact_writes,
    limitations,
):
    response_id = response_data.get("id") if isinstance(response_data, dict) else None
    invocation_id = response_id or f"{context_package.get('runId')}-{context_package.get('passId')}-{sha256_text(started_at)[:12]}"
    return {
        "schemaVersion": "1.0",
        "workflowId": context_package.get("workflowId"),
        "runId": context_package.get("runId"),
        "passId": context_package.get("passId"),
        "role": context_package.get("role"),
        "adapterKind": "llm-api",
        "invocationId": invocation_id,
        "contextId": f"{invocation_id}-fresh-context",
        "runnerName": os.environ.get("TOP_RUNNER_NAME", "top-protocol-runner"),
        "processId": os.getpid(),
        "command": "scripts/adapters/llm_api_adapter.py",
        "startedAt": started_at,
        "endedAt": ended_at,
        "exitCode": 0 if model_invocation else 1,
        "taskCapsuleRef": refs["taskCapsuleRef"],
        "contextPackageRef": refs["contextPackageRef"],
        "handoffArtifactRef": refs["handoffArtifactRef"],
        "contextHash": context_package.get("contextHash"),
        "handoffHash": sha256_file(handoff_path),
        "freshContext": bool(model_invocation),
        "receivedOnlyContextPackage": bool(model_invocation),
        "modelInvocationEvidence": bool(model_invocation),
        "artifactWrites": artifact_writes,
        "limitations": limitations,
    }


def main():
    parser = argparse.ArgumentParser(description="Run one TOP pass through an LLM API adapter.")
    parser.add_argument("--provider", default="openai-responses", choices=["openai-responses"])
    parser.add_argument("--endpoint", default=os.environ.get("TOP_LLM_API_URL", "https://api.openai.com/v1/responses"))
    parser.add_argument("--model", default=os.environ.get("TOP_LLM_MODEL"))
    parser.add_argument("--api-key-env", default="TOP_LLM_API_KEY")
    parser.add_argument("--fallback-api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--input-byte-limit", type=int, default=120000)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--dry-run", action="store_true", help="Validate adapter inputs and write blocked artifacts without calling an API.")
    args = parser.parse_args()

    root = Path.cwd().resolve()
    context_ref = os.environ.get("TOP_CONTEXT_PACKAGE")
    handoff_ref = os.environ.get("TOP_HANDOFF_ARTIFACT")
    evidence_ref = os.environ.get("TOP_INVOCATION_EVIDENCE")
    if not context_ref or not handoff_ref or not evidence_ref:
        print("llm_api_adapter: FAILED", file=sys.stderr)
        print("- TOP_CONTEXT_PACKAGE, TOP_HANDOFF_ARTIFACT, and TOP_INVOCATION_EVIDENCE are required", file=sys.stderr)
        return 2

    started_at = utc_now()
    response_data = {}
    model_invocation = False
    limitations = []

    try:
        context_path = resolve_ref(root, context_ref, "TOP_CONTEXT_PACKAGE")
        handoff_path = resolve_ref(root, handoff_ref, "TOP_HANDOFF_ARTIFACT")
        evidence_path = resolve_ref(root, evidence_ref, "TOP_INVOCATION_EVIDENCE")
        context_package = load_json(context_path)
        task_capsule_ref = context_package.get("taskCapsuleRef")
        task_capsule_path = resolve_ref(root, task_capsule_ref, "taskCapsuleRef")
        task_capsule = load_json(task_capsule_path)
        workflow_id = context_package.get("workflowId")
        run_id = context_package.get("runId")
        pass_id = context_package.get("passId")
        refs = {
            "contextPackageRef": context_ref,
            "taskCapsuleRef": task_capsule_ref,
            "handoffArtifactRef": handoff_ref,
        }

        if args.dry_run:
            message = "dry-run did not call LLM API"
            limitations.append(message)
            handoff = failure_handoff(workflow_id, pass_id, task_capsule, refs, message)
            write_json(handoff_path, handoff)
        else:
            api_key = os.environ.get(args.api_key_env) or os.environ.get(args.fallback_api_key_env)
            if not api_key:
                raise RuntimeError(f"missing API key in {args.api_key_env} or {args.fallback_api_key_env}")
            if not args.model:
                raise RuntimeError("missing model; set --model or TOP_LLM_MODEL")

            referenced_inputs = [
                read_ref_text(root, ref, args.input_byte_limit)
                for ref in context_package.get("inputReferences", [])
            ]
            system_prompt, user_prompt = build_prompt(context_package, task_capsule, referenced_inputs, handoff_ref)
            response_data, response_text = openai_responses_call(
                args.endpoint,
                api_key,
                args.model,
                system_prompt,
                user_prompt,
                args.timeout_seconds,
            )
            model_invocation = True
            model_output = extract_json_object(response_text)
            model_handoff, artifact_writes = split_model_output(model_output)
            written_artifacts = apply_artifact_writes(root, task_capsule, artifact_writes)
            handoff = normalize_model_handoff(model_handoff, workflow_id, run_id, pass_id, task_capsule, refs)
            if written_artifacts:
                written_refs = [item["ref"] for item in written_artifacts]
                handoff["filesChanged"] = sorted(set(handoff.get("filesChanged", []) + [handoff_ref, *written_refs]))
                handoff["outputReferences"] = sorted(set(handoff.get("outputReferences", []) + [handoff_ref, *written_refs]))
            write_json(handoff_path, handoff)

        ended_at = utc_now()
        evidence = build_invocation_evidence(
            args,
            context_package,
            task_capsule,
            refs,
            started_at,
            ended_at,
            response_data,
            handoff_path,
            model_invocation,
            written_artifacts if model_invocation else [],
            limitations or ["LLM API invocation completed in a fresh request using only context package inputs."],
        )
        write_json(evidence_path, evidence)
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        ended_at = utc_now()
        try:
            context_package = load_json(resolve_ref(root, context_ref, "TOP_CONTEXT_PACKAGE"))
            task_capsule_ref = context_package.get("taskCapsuleRef")
            task_capsule = load_json(resolve_ref(root, task_capsule_ref, "taskCapsuleRef"))
            workflow_id = context_package.get("workflowId")
            pass_id = context_package.get("passId")
            handoff_path = resolve_ref(root, handoff_ref, "TOP_HANDOFF_ARTIFACT")
            evidence_path = resolve_ref(root, evidence_ref, "TOP_INVOCATION_EVIDENCE")
            message = f"llm-api adapter failed: {exc}"
            refs = {
                "contextPackageRef": context_ref,
                "taskCapsuleRef": task_capsule_ref,
                "handoffArtifactRef": handoff_ref,
            }
            write_json(handoff_path, failure_handoff(workflow_id, pass_id, task_capsule, refs, message))
            evidence = build_invocation_evidence(
                args,
                context_package,
                task_capsule,
                refs,
                started_at,
                ended_at,
                response_data,
                handoff_path,
                False,
                [],
                [message],
            )
            write_json(evidence_path, evidence)
        except Exception:
            pass
        print("llm_api_adapter: FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1

    if model_invocation:
        print("llm_api_adapter: OK")
    else:
        print("llm_api_adapter: DRY_RUN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
