#!/usr/bin/env node
import { readFileSync, readdirSync, existsSync } from "fs";
import { resolve, join, dirname, relative } from "path";
import { fileURLToPath } from "url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const SCHEMAS_DIR = join(ROOT, "top", "schemas");
const EXAMPLES_DIR = join(ROOT, "top", "examples");
const VERBOSE = process.argv.includes("--verbose");

// Load and register all schemas by $id so $ref resolution works
const ajv = new Ajv2020({ strict: false, allErrors: true });
addFormats(ajv);

function loadJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

const schemaFiles = readdirSync(SCHEMAS_DIR).filter(f => f.endsWith(".json"));
const schemaByFile = {};
const schemaById = {};

for (const filename of schemaFiles) {
  const schema = loadJson(join(SCHEMAS_DIR, filename));
  schemaByFile[filename] = schema;
  // Register by $id (for $ref resolution) if present; also register by filename
  const id = schema.$id || filename;
  schemaById[id] = schema;
  ajv.addSchema(schema, id);
}

// Compile validators keyed by the short logical name used in detectSchema
const KEY_MAP = {
  "clarification_request.schema.json": "clarification_request",
  "clarification_state.schema.json": "clarification_state",
  "complexity_report.schema.json": "complexity_report",
  "conflict_report.schema.json": "conflict_report",
  "diff.schema.json": "diff",
  "extraction_result.schema.json": "extraction_result",
  "final_decision_signal.schema.json": "final_decision_signal",
  "final_output.schema.json": "final_output",
  "mode_routing_result.schema.json": "mode_routing_result",
  "normalized_input.schema.json": "normalized_input",
  "release-metadata.schema.json": "release_metadata",
  "sensitive_data_report.schema.json": "sensitive_data_report",
  "structured_prompt.json": "structured_prompt",
  "target_style_output.schema.json": "target_style_output",
  "user_response.schema.json": "user_response",
  "validation_result.schema.json": "validation_result",
};

const validators = {};
for (const [filename, key] of Object.entries(KEY_MAP)) {
  const schema = schemaByFile[filename];
  if (!schema) continue;
  try {
    validators[key] = ajv.compile(schema);
  } catch (error) {
    console.warn(`Could not compile schema '${key}': ${error.message}`);
  }
}

// Heuristic: identify which schema a JSON block conforms to.
// Order matters — more specific checks before general ones.
function detectSchema(json) {
  if (!json || typeof json !== "object") return null;

  // Node-level outputs (narrow objects)
  if ("original_prompt" in json && "normalized" in json) return "normalized_input";
  if ("sensitive_findings" in json && "sensitive_blocking" in json) return "sensitive_data_report";
  if ("complexity_level" in json && "recommendation" in json) return "complexity_report";
  if ("conflicts" in json && "has_blocking_conflicts" in json) return "conflict_report";
  if ("clarification_needed" in json && "proceed_with_inference" in json) return "clarification_state";
  if ("question" in json && "missing_field" in json) return "clarification_request";
  if ("selected_mode" in json && "routing_reason" in json) return "mode_routing_result";
  if ("noise_candidates" in json) return "extraction_result";
  // extraction_result allows empty goal/output_format; structured_prompt does not
  if ("goal" in json && "goal_source" in json) {
    const isMissing = json.goal_source === "missing" || json.output_format_source === "missing"
      || json.goal === "" || json.output_format === "";
    return isMissing ? "extraction_result" : "structured_prompt";
  }
  if ("results" in json && "all_pass" in json) return "validation_result";
  if ("output_type" in json && "target_style" in json) return "target_style_output";
  if ("removed_noise" in json && "rewritten_phrases" in json) return "diff";
  if ("selected_option" in json && !("question" in json)) return "user_response";

  // final_decision_signal: has status but lacks the rich output fields
  if ("status" in json) {
    const richFields = ["cleaned_prompt", "structured_prompt", "diff",
      "escalation_notice", "clarification_request", "target_style_output"];
    const hasRichField = richFields.some(f => f in json);
    if (!hasRichField) return "final_decision_signal";
    return "final_output";
  }

  return null;
}

function extractJsonBlocks(markdown) {
  const blocks = [];
  const regex = /```json\s*([\s\S]*?)```/g;
  let match;
  while ((match = regex.exec(markdown)) !== null) {
    const raw = match[1].trim();
    try {
      blocks.push({ raw, parsed: JSON.parse(raw) });
    } catch {
      // ignore malformed JSON blocks
    }
  }
  return blocks;
}

function formatErrors(errors = []) {
  return errors.map(e => `${e.instancePath || "/"} ${e.message}`).join("; ");
}

// ── Repo-level checks ────────────────────────────────────────────────────────
let repoPassed = 0;
let repoFailed = 0;
const repoFailures = [];

function repoPass() { repoPassed++; }
function repoFail(msg) { repoFailed++; repoFailures.push(msg); }

const releaseMetadataPath = join(ROOT, "release-metadata.json");
const packageJsonPath = join(ROOT, "package.json");
const specPath = join(ROOT, "top", "spec.json");
const startupRulePath = join(ROOT, "top", "shared-rules", "startup-update-check.md");

if (!existsSync(releaseMetadataPath)) {
  repoFail("Missing release-metadata.json.");
} else {
  const metadata = loadJson(releaseMetadataPath);
  const validateReleaseMeta = validators.release_metadata;
  if (!validateReleaseMeta) {
    repoFail("release-metadata.schema.json could not be compiled — skipping metadata validation.");
  } else if (!validateReleaseMeta(metadata)) {
    repoFail(`release-metadata.json schema validation failed: ${formatErrors(validateReleaseMeta.errors)}`);
  } else {
    repoPass();
  }

  const pkg = loadJson(packageJsonPath);
  const spec = loadJson(specPath);

  if (metadata.current_version !== pkg.version) {
    repoFail(`Version mismatch: release-metadata.json (${metadata.current_version}) vs package.json (${pkg.version}).`);
  } else {
    repoPass();
  }

  if (metadata.current_version !== spec.skill_version) {
    repoFail(`Version mismatch: release-metadata.json (${metadata.current_version}) vs top/spec.json (${spec.skill_version}).`);
  } else {
    repoPass();
  }

  const startupInvariant = "A startup update check should run before active work begins when release metadata and a trusted comparison manifest are available.";
  if (!spec.invariants.includes(startupInvariant)) {
    repoFail("top/spec.json is missing the startup update check invariant.");
  } else {
    repoPass();
  }
}

if (!existsSync(startupRulePath)) {
  repoFail("Missing top/shared-rules/startup-update-check.md.");
} else {
  repoPass();
}

// Verify all schemas listed in spec.json output_contract exist on disk
const spec = loadJson(specPath);
for (const schemaPath of (spec.output_contract?.schemas ?? [])) {
  const fullPath = join(ROOT, "top", schemaPath);
  if (!existsSync(fullPath)) {
    repoFail(`Schema listed in spec.json not found on disk: ${schemaPath}`);
  } else {
    repoPass();
  }
}

// ── Markdown link checking ────────────────────────────────────────────────────
const MD_DIRS = [ROOT, join(ROOT, "docs"), join(ROOT, "top"), join(ROOT, "product")];
const LINK_PATTERN = /\[([^\]]+)\]\(([^)]+)\)/g;

function collectMdFiles(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { recursive: true })
    .filter(f => f.endsWith(".md") && !f.includes("node_modules"))
    .map(f => join(dir, f));
}

const allMdFiles = [...new Set(MD_DIRS.flatMap(collectMdFiles))];

for (const mdPath of allMdFiles) {
  const content = readFileSync(mdPath, "utf8");
  let match;
  LINK_PATTERN.lastIndex = 0;
  while ((match = LINK_PATTERN.exec(content)) !== null) {
    const href = match[2];
    if (href.startsWith("http") || href.startsWith("mailto:") || href.startsWith("#")) continue;
    const target = resolve(dirname(mdPath), href.split("#")[0]);
    if (!existsSync(target)) {
      repoFail(`Broken link in ${relative(ROOT, mdPath)}: [${match[1]}](${href})`);
    } else {
      repoPass();
    }
  }
}

// ── Example JSON block validation ─────────────────────────────────────────────
const exampleFiles = readdirSync(EXAMPLES_DIR)
  .filter(f => f.endsWith(".md"))
  .sort();

let totalBlocks = 0;
let passedBlocks = 0;
let failedBlocks = 0;
let unknownSkipped = 0;
let validatorSkipped = 0;
const failures = [];

for (const file of exampleFiles) {
  const content = readFileSync(join(EXAMPLES_DIR, file), "utf8");
  const blocks = extractJsonBlocks(content);

  if (VERBOSE) console.log(`\n${file} — ${blocks.length} JSON block(s)`);

  for (let i = 0; i < blocks.length; i++) {
    const { parsed } = blocks[i];
    const schemaKey = detectSchema(parsed);
    totalBlocks++;

    if (!schemaKey) {
      unknownSkipped++;
      if (VERBOSE) console.log(`  [${i + 1}] UNKNOWN SKIP — no schema detected`);
      failures.push({ file, blockIndex: i + 1, schemaKey: "(unknown)", errors: "No schema detected — add schema or fix detectSchema()" });
      failedBlocks++;
      continue;
    }

    const validate = validators[schemaKey];
    if (!validate) {
      validatorSkipped++;
      if (VERBOSE) console.log(`  [${i + 1}] skipped — validator for '${schemaKey}' not compiled`);
      continue;
    }

    if (validate(parsed)) {
      passedBlocks++;
      if (VERBOSE) console.log(`  [${i + 1}] pass — ${schemaKey}`);
    } else {
      failedBlocks++;
      const errMsg = formatErrors(validate.errors);
      failures.push({ file, blockIndex: i + 1, schemaKey, errors: errMsg });
      if (VERBOSE) console.log(`  [${i + 1}] fail — ${schemaKey}: ${errMsg}`);
    }
  }
}

// ── Report ────────────────────────────────────────────────────────────────────
console.log("\n=== TOP Prompt Cleaner — Validation Report ===\n");
console.log(`Repo checks   : ${repoPassed + repoFailed} (${repoPassed} pass, ${repoFailed} fail)`);
console.log(`Examples      : ${exampleFiles.length}`);
console.log(`JSON blocks   : ${totalBlocks} (${passedBlocks} pass, ${failedBlocks} fail, ${validatorSkipped} skipped)`);
if (unknownSkipped > 0) {
  console.log(`  WARNING: ${unknownSkipped} block(s) had no schema detected — treated as failures`);
}

if (repoFailures.length > 0) {
  console.log("\nRepo failures:");
  for (const msg of repoFailures) console.log(`  - ${msg}`);
}

if (failures.length > 0) {
  console.log("\nExample failures:");
  for (const f of failures) {
    console.log(`  ${f.file} [block ${f.blockIndex}] (${f.schemaKey})`);
    console.log(`    ${f.errors}`);
  }
}

const ok = repoFailures.length === 0 && failures.length === 0;
if (ok) {
  console.log("\nAll checks passed.\n");
}
process.exit(ok ? 0 : 1);
