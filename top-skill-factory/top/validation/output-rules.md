# Output validation rules

Checks:
- Required artifacts exist.
- Folder structure matches spec.
- Prompts cover required controllers, modes, and declared executable child nodes.
- Validation files exist.
- Schemas exist.
- Final decision artifacts declare the artifact contract they rely on.
- README explains purpose and usage.
- Required artifacts are not empty placeholders.
- Mode files contain purpose, input, output, and rules.
- Ready output has no unresolved blocking blind spots.
- Ready demo bundles that use a minimal contract state that contract explicitly.
- Example set includes at least one input-side example and at least one output-side example when the skill generates artifact bundles.
- Legacy conversion outputs include a conversion report when `ConvertLegacySkillMode` is used or demonstrated.

Blocking violations:
- Missing spec.json.
- Missing core prompts.
- Missing validation rules.
- OutputAssembler invented missing artifacts.
- Empty required artifact.
- Placeholder artifact presented as ready output.
- Ready result claims full completeness while relying only on the minimal demo contract.
- Blocking blind spots unresolved in a ready or draft-as-ready result.
- Claimed output-generation skill has no output-side example artifacts.
- Legacy conversion result is presented as ready without a conversion report.
