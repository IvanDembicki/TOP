# SensitiveDataDetector

Responsibility: detect private or dangerous source material before it contaminates reusable skill artifacts.

Input:
- legacy_skill_content
- imported_artifacts
- normalized_input

Output:
- sensitivity_report

Primary objectives:
- identify secrets, credentials, internal URLs, personal data, client data, and confidential business rules
- determine whether redaction is required before downstream conversion

Process:
- scan imported artifacts for direct secret patterns and obvious confidential structures
- distinguish between safe structural evidence and unsafe literal payload
- emit explicit redaction requirements when risky material is present

Rules:
- do not preserve literal secret values
- do not silently pass risky source material downstream
- conversion may continue only with redacted or isolated source evidence when sensitive content is detected
