# analyze-top-project

agent: Intake Agent

input_contract:
- raw_input

output_contract:
- task_type
- normalized_task
- ambiguity_flag

rules:
- do not interpret beyond normalization
