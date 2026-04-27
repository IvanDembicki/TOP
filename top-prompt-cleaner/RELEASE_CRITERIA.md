# Release Criteria — TOP Prompt Cleaner

© 2026 Ivans Dembickis · MIT License

---

## 1.0.0 Stable — criteria (all closed)

### Schema contract
- [x] All schemas have `$id` matching their filename
- [x] All `$ref` paths in schemas resolve to files that exist
- [x] `output_contract.schemas` in `spec.json` lists all 15 schemas
- [x] `final_output.schema.json` enforces `oneOf` for `cleaned_prompt` / `target_style_output`
- [x] `final_output.schema.json` forbids field cross-contamination between terminal states

### Example coverage
- [x] At least one example for every terminal state: `ready`, `blocked`, `escalated`
- [x] At least one example for every mode: `quick_clean`, `strict_clean`, `target_llm_style`
- [x] At least one example for `blocked` due to sensitive data
- [x] At least one example for `blocked` due to clarification request (with U option)
- [x] Full `final_output` JSON block for each terminal state (ready/cleaned_prompt, ready/target_style_output, blocked, escalated)
- [x] All examples pass `npm run validate` — zero failures, zero unknown skips
- [x] Every StructureExtractor block has `goal_source` and `output_format_source`

### Prompt/node consistency
- [x] `final-decision-controller.md` uses `all_pass` (not `status`) from `validation_result`
- [x] `input-controller.md` documents SensitiveDataDetector running before ComplexityDetector
- [x] No active reference to `FrontendStyleMode` or `FrontendStyleAdapter` in non-deprecated files
- [x] All active modes have `status: stable` in `top/spec.json`

### Validator
- [x] `npm ci && npm run validate` passes on a clean install
- [x] Unknown JSON blocks are treated as failures (not silent skips)
- [x] Markdown links in repo docs verified to exist on disk
- [x] `$ref` resolution works across schemas (Ajv2020 + `$id`)

### Documentation
- [x] `README.md` — no broken links, examples coverage table, validator section
- [x] `docs/usage.md` — step-by-step user guide
- [x] `docs/troubleshooting.md` — common failure modes and remedies
- [x] `docs/contracts.md` — schema reference for all 15 contracts
- [x] `docs/security.md` — sensitive data policy
- [x] `top/examples/README.md` — index table of all 10 examples
- [x] `VALIDATION_REPORT.md` — reflects current validator run

### Release hygiene
- [x] All four version sources synchronized: `package.json`, `release-metadata.json`, `top/spec.json`, `SKILL.md`
- [x] `release_channel: stable`, `status: stable` in all relevant files
- [x] `node_modules/` excluded from release archive (`.gitignore`)
- [x] `package.json` + `package-lock.json` allow `npm ci` on clean install
- [x] `.github/workflows/validate.yml` CI workflow present
- [x] `RELEASE_NOTES.md` has 1.0.0 entry

---

## Post-1.0 (future milestones)

Not required for 1.0. Do not block 1.0 on these.

- `BatchCleanMode` implementation (target: 1.1.0)
- Prompt library integration
- TopSkillFactory automation
- `npm script: validate:release` stricter thresholds
