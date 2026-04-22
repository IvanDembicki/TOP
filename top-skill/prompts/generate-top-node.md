# generate-top-node

agent: Generation Agent

input_contract:
- approved_top_model
- semantic_interpretation_output
- target_adaptation_output

output_contract:
- generated_artifact

rules:
- no architecture change
- generate from Layer B semantic intent and Layer C target adaptation, not from source-platform primitives
- do not invent behavior absent from the semantic layer
