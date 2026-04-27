# ArtifactConsistencyValidator

Responsibility: compare the generated artifact set and detect contradiction, drift, or missing correspondence between files.

Input:
- spec_artifact
- prompt_artifacts
- validation_artifacts
- schema_artifacts
- example_artifacts

Output:
- artifact_consistency_report

Primary objectives:
- verify that the artifact set describes one coherent skill
- detect where one file promises behavior another file does not support

Process:
- compare declared nodes in the spec against materialized prompt files
- compare mode outputs against validation and schema expectations
- compare examples against declared behavior and contracts
- record contradictions, omissions, and weak correspondence

Invalid output conditions:
- report says artifacts are consistent while required files disagree materially
- contradictions are described but not classified

Rules:
- treat missing correspondence as a real defect, not a cosmetic issue
- prefer concrete file-to-file evidence over impressionistic judgment