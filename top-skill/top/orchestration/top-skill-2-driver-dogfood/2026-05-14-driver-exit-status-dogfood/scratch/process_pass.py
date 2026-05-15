import json
import os
from pathlib import Path


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


root = Path.cwd().resolve()
context_ref = os.environ["TOP_CONTEXT_PACKAGE"]
handoff_ref = os.environ["TOP_HANDOFF_ARTIFACT"]
context = load_json(root / context_ref)
capsule = load_json(root / context["taskCapsuleRef"])
role = capsule["role"]
pass_id = context["passId"]
is_judicial = role == "judicial"

handoff = {
    "schemaVersion": "1.0",
    "workflowId": context["workflowId"],
    "passId": pass_id,
    "taskId": capsule["taskId"],
    "role": role,
    "agentName": f"{role}-process-dogfood",
    "taskCapsuleRef": context["taskCapsuleRef"],
    "inputReferences": capsule.get("inputReferences", []),
    "outputReferences": [handoff_ref],
    "filesRead": [context_ref, context["taskCapsuleRef"]],
    "filesChanged": [handoff_ref],
    "commandsRun": ["scratch/process_pass.py"],
    "status": "done",
    "executionEvidence": {
        "executionIsolationLevel": "protocol-followed-by-agent",
        "verificationEvidenceLevel": "agent-claimed",
        "runnerName": None,
        "separateInvocationIds": [],
        "schemaValidationCommand": None,
        "hardCheckCommands": [],
        "limitations": [
            "Process dogfood pass records a handoff but does not prove LLM context isolation."
        ],
    },
    "limitations": [
        "This dogfood pass is process-backed and cannot certify delivery complete.",
        "The actual skill edit was made by the current Codex context before the driver run.",
    ],
    "didNotDo": capsule.get("forbiddenActions", []),
    "handoffTo": "certification" if is_judicial else "judicial",
    "mayEditFiles": bool(capsule.get("mayEditFiles")),
    "mayValidate": bool(capsule.get("mayValidate")),
    "mayRepair": bool(capsule.get("mayRepair")),
    "mayReport": bool(capsule.get("mayReport")),
    "mayCertifyDelivery": bool(capsule.get("mayCertifyDelivery")),
}

if is_judicial:
    handoff["filesRead"].extend(
        [
            "handoffs/executive.handoff.json",
            "workflow/run-package-layout.md",
            "top/validation/output-rules.md",
            "SKILL.md",
            "CHANGELOG.md",
        ]
    )

write_json(root / handoff_ref, handoff)
