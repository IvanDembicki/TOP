# generate-top-tree

agent: TOP Modeling Agent

input_contract:
- domain_structure

output_contract:
- nodes
- protocols
- lifecycle

rules:
- must follow canon strictly
- model ownership so every runtime object is born at its architectural tree position
- parent nodes/controllers own and construct direct children
- do not model runtime props, slots, builders, render callbacks, or prebuilt child fragments as TOP ownership
- use TOP spec props only as declarative metadata, not runtime props
