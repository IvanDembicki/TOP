# Privacy and Security Validation Rules

Checks:
- legacy import scans for secrets, credentials, internal URLs, personal data, and client-confidential content
- sensitive material is redacted or isolated before reusable output artifacts are emitted
- examples do not expose raw secrets or private business details

Blocking violations:
- secret or credential copied into reusable artifact
- private client or personal data copied into reusable example without redaction
- conversion flow claims ready without performing a sensitive-data pass on imported legacy material
