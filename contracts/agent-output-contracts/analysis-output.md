# Analysis Output Contract

## Required structure

All sections are required. The absence of any section makes the output invalid.

goal:
context:
model:
findings:
recommendations:

## Required fields

goal:
- analysis_scope

context:
- input_material
- materialization_mode
- dominant_mode (if mixed)

model:
- reconstructed_tree
- controller_content_findings
- tree_classification
- state_ownership_map
- source_of_truth_map

findings:
- confirmed_violations
- possible_violations
- convention_issues
- open_questions

recommendations:
- refactor_order
- required_actions

## Findings classification

**confirmed_violation** — a violation is explicitly confirmed by the input material.

**possible_violation** — there are signs of a violation, but the data is insufficient
for a definitive conclusion.

**convention_issue** — not an architectural violation, but a deviation from accepted
project conventions or skill conventions.

**open_question** — ambiguity or lack of data;
a firm conclusion cannot be made, clarification is required.

## Rules

- All required sections must be present.
- `confirmed_violations`, `possible_violations`, `convention_issues`
  and `open_questions` must be separated.
- Do not escalate an open_question to a violation without sufficient grounds.
- Do not treat the absence of explicit confirmation as automatic refutation of a problem.
- `refactor_order` must reflect actual dependencies between changes,
  not an arbitrary sequence.
- Free text outside the required structure is prohibited.
- All required fields must contain semantically valid content.
  Empty values and formal stubs are considered invalid.
