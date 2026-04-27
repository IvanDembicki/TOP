# Example: CreateNewSkillMode output bundle

This example shows the shape of a successful output bundle for a generated skill.

## Expected artifact bundle

- `spec.json`
- `README.md`
- `top/prompts/root.md`
- `top/prompts/mode-router.md`
- `top/prompts/...`
- `top/modes/...`
- `top/schemas/...`
- `top/validation/...`
- `top/shared-rules/...`
- `top/examples/...`

## Expected properties

- controllers declared in `spec.json` have corresponding prompts
- mode files define purpose, input, output, and rules
- schemas constrain structured signals and decisions
- validation rules can name evidence and failure conditions
- no required artifact is an empty placeholder
- final ready decision is backed by validation evidence

## Example dry run expectation

Input scenario:
- user asks for a new skill with two explicit modes and one validator

Expected result:
- `CreateNewSkillMode` produces a bounded tree
- contracts are explicit
- missing information produces clarification rather than invention
- ready state is not emitted if required artifacts are absent