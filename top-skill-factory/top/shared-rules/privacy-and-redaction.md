# Privacy and Redaction Rules

- Imported legacy material must be scanned for secrets, credentials, internal URLs, personal data, and client-confidential content before conversion proceeds.
- Sensitive material must be redacted, tokenized, or isolated before it becomes reusable example, schema, or prompt content.
- Redaction must preserve enough structural evidence to reason about the skill, but must not preserve the secret value itself.
- A conversion flow is not ready if private material was propagated into reusable output artifacts without an explicit safe-handling policy.
