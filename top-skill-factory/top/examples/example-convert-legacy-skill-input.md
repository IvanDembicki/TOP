# Example input: convert legacy skill

Task:
Convert an existing working prompt-based code review skill into TOP standard.

Legacy skill:
- Accepts pull request diff.
- Reviews architecture, bugs, style, and tests.
- Produces a markdown review.

Conversion goals:
- Extract node responsibilities.
- Define signal contracts.
- Add validation.
- Preserve behavior where possible.

Important rule:
Legacy skill is evidence, not authority.