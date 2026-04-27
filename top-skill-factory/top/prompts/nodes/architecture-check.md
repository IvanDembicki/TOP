# ArchitectureCheck

Responsibility: verify that the artifact set respects the intended TOP architecture and responsibility boundaries.

Input:
- spec_artifact
- node_contracts
- prompt_artifacts

Output:
- architecture_check_report

Primary objectives:
- detect architectural drift, hidden coupling, and role confusion
- ensure the implemented artifact set still matches the designed control model

Process:
- compare the tree structure, node types, and ownership boundaries
- identify mixed responsibilities and bypasses around declared controllers
- detect where one artifact quietly takes over another artifact's role

Invalid output conditions:
- architectural contradiction is described as a minor style issue
- report ignores hidden authority flow because outputs still look plausible

Rules:
- architecture failures are not cosmetic when they change control or authority
- explicit controller boundaries must remain meaningful after generation