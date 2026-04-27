# SensitiveDataDetector

## Purpose

Scan the input prompt for content that must not be passed to an external LLM without explicit user acknowledgment. This node runs before any transformation and produces a warning or blocking signal. It never removes data autonomously — it surfaces, warns, and halts when necessary.

## Input

Signal keys received:
- `original_prompt` — raw user text
- `mode` — routing target (affects severity threshold)

## Output

Signal keys emitted:
- `sensitive_findings` — array of `{ type, excerpt, severity, recommendation }` objects. Empty array when nothing found.
- `sensitive_blocking` — boolean. True when at least one finding has `severity: "blocking"`.

## Detection categories

### Blocking (halt processing, require user confirmation)

| Type key | Examples |
|---|---|
| `api_key` | Bearer tokens, API keys, `sk-…`, `AKIA…` AWS keys |
| `password` | Inline passwords, secrets in connection strings |
| `private_key` | PEM blocks (`-----BEGIN …-----`), private key material |
| `credential` | OAuth tokens, session cookies embedded in text |

### Warning (surface to user, do not halt)

| Type key | Examples |
|---|---|
| `pii_name` | Full names combined with addresses or ID numbers |
| `pii_email` | Email addresses (bare email alone is low-risk) |
| `pii_phone` | Phone numbers |
| `pii_id` | Passport, SSN, national ID numbers |
| `internal_url` | `*.internal`, `10.x.x.x`, `192.168.x.x`, `localhost` endpoints |
| `internal_code` | Code snippets containing connection strings or hardcoded IPs |

## Process

1. Scan `original_prompt` text against all category patterns.
2. For each match, build a finding object:
   ```json
   {
     "type": "api_key",
     "excerpt": "Authorization: Bearer eyJhbG…[truncated at 20 chars]",
     "severity": "blocking",
     "recommendation": "Remove or replace with a placeholder before sending to an LLM."
   }
   ```
3. Truncate the `excerpt` to 40 characters — enough to identify the location, not enough to reproduce the secret.
4. Set `sensitive_blocking: true` if any finding has `severity: "blocking"`.
5. Emit both signals even when `sensitive_findings` is empty (empty array + `sensitive_blocking: false`).

## Severity rules

- If `mode = "quick_clean"`: warning-level findings do NOT block; they are included in the diff `warnings` array.
- If `mode = "strict_clean"`: all findings at warning or blocking severity are surfaced; blocking severity halts.
- Blocking findings always halt regardless of mode.

## Boundaries

- Do NOT redact, modify, or remove any text from the original prompt. Detection only.
- Do NOT invent findings — only report what is present in the text.
- Do NOT store, log, or repeat the full value of any secret found. Always truncate excerpts.
- Do NOT treat generic technical terms (e.g., "key", "token" as plain words) as secrets without corroborating pattern evidence.

## Invalid output conditions

- Emitting `sensitive_blocking: true` with an empty `sensitive_findings` array.
- Including the full value of an API key or password in `excerpt`.
- Halting processing when `sensitive_findings` contains only warning-level entries in `quick_clean` mode.

## Example output (blocking case)

```json
{
  "sensitive_findings": [
    {
      "type": "api_key",
      "excerpt": "sk-proj-AbCdEfGhIjKlMnOpQr…",
      "severity": "blocking",
      "recommendation": "Remove the API key and replace with a placeholder like {{API_KEY}} before processing."
    }
  ],
  "sensitive_blocking": true
}
```

## Example output (clean)

```json
{
  "sensitive_findings": [],
  "sensitive_blocking": false
}
```
