# Example: QuickClean — Blocked (Sensitive Data Detected)

**Mode:** `quick_clean`
**Final state:** `blocked`
**Blocking reason:** API key detected in prompt body before any transformation.

---

## Input

```
You are a helpful assistant. Use the OpenAI API to summarize the following article.
My API key is: sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890abcdef

Summarize this article in 3 bullet points. Focus on the main argument, key evidence, and conclusion.

Article: {{article_text}}
```

---

## Node trace

### InputController

```json
{
  "original_prompt": "...",
  "normalized": true
}
```

### SensitiveDataDetector

```json
{
  "sensitive_findings": [
    {
      "type": "api_key",
      "excerpt": "sk-proj-AbCdEfGhIjKlMn…",
      "severity": "blocking",
      "recommendation": "Remove the API key from the prompt and replace with a placeholder like {{OPENAI_API_KEY}}. API keys must never be sent to an LLM."
    }
  ],
  "sensitive_blocking": true
}
```

### Pipeline halted

`sensitive_blocking: true` — no further nodes run. ComplexityDetector, StructureExtractor, and all transformation nodes are skipped.

---

## Final output

**Status:** `blocked`

**Diagnosis:**

> A blocking sensitive data finding was detected before processing could begin.
>
> **Finding:** API key pattern detected.
> **Location:** `sk-proj-AbCdEfGhIjKlMn…` (truncated)
> **Risk:** Sending an API key to an LLM exposes it to logging, training pipelines, and potential leakage.
>
> **What to do:** Remove the API key from the prompt. Replace it with a placeholder: `{{OPENAI_API_KEY}}`. If you need the LLM to know that an API key will be used, describe it by name only, not value.
>
> After removing the key, resubmit the prompt for cleaning.

---

**Full final output (machine-verifiable contract):**

```json
{
  "status": "blocked",
  "diagnosis": "A blocking sensitive data finding was detected before processing could begin. API key pattern detected: 'sk-proj-AbCdEfGhIjKlMn…'. Remove the API key from the prompt and replace with a placeholder such as {{OPENAI_API_KEY}} before resubmitting."
}
```

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 10 | SensitiveDataDetector runs before any transformation | PASS — pipeline halted at SensitiveDataDetector |
| 4 | OutputBuilder cannot invent goal, constraints, or output format | PASS — no output produced |
| 9 | Escalation and cleaned output are mutually exclusive | PASS — status is `blocked` |
