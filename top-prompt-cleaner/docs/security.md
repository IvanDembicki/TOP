# Security Policy — TOP Prompt Cleaner

© 2026 Ivans Dembickis · MIT License

---

## Sensitive data handling

TOP Prompt Cleaner runs `SensitiveDataDetector` as the **first transformation gate** — before ComplexityDetector, StructureExtractor, or any cleaning node. No prompt content is transformed until this check completes.

### What is detected

| Category | Examples | Default severity |
|---|---|---|
| `api_key` | `sk-proj-...`, `Bearer ...`, `AIza...` | **blocking** |
| `password` | `password: hunter2`, `pwd=...` | **blocking** |
| `private_key` | PEM blocks (`-----BEGIN PRIVATE KEY-----`) | **blocking** |
| `credential` | AWS access key ID, service account JSON | **blocking** |
| `pii_email` | `user@example.com` in prompt body | warning |
| `pii_phone` | `+1-555-000-0000` | warning |
| `pii_name` | Name + identifier combo | warning |
| `pii_id` | SSN, passport number patterns | warning |
| `internal_url` | `*.internal`, `*.corp`, non-public hostnames | warning |
| `internal_code` | Internal ticket IDs, internal system names | warning |

### Severity rules

- **Blocking**: pipeline halts immediately. No cleaned output is produced. The user receives a `blocked` status with a diagnosis and removal instructions.
- **Warning**: pipeline proceeds in `quick_clean` mode with a warning in `diff.warnings`. Pipeline halts in `strict_clean` mode.

### What is NOT logged or stored

TOP Prompt Cleaner is an LLM skill — it does not write to disk, call external APIs, or persist conversation history. Sensitive data is never echoed back verbatim: excerpts in `sensitive_findings` are truncated to 40 characters maximum to identify the location without reproducing the secret.

### Recommendations for users

1. **Never include real secrets in prompts.** Use placeholders: `{{API_KEY}}`, `{{DATABASE_PASSWORD}}`.
2. **If you receive a blocking finding**, remove the secret before resubmitting. The skill will not process the prompt until it is clear.
3. **PII in examples**: if your prompt contains PII for testing purposes, replace it with synthetic data before cleaning.

---

## Reporting vulnerabilities

This is a prompt skill, not a deployed service. If you find a prompt injection or data leakage issue in the skill logic, open an issue in the project repository or email [ivan.dembicki@gmail.com](mailto:ivan.dembicki@gmail.com).
