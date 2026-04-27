# MarketplaceValidationMode

Purpose: validate third-party skills for TOP compliance and trustworthiness.

Maturity: planned / skeletal alpha.

Input:
- third_party_skill
- trust_policy

Output:
- compliance_report
- risk_report
- trust_score

Rules:
- Treat third-party claims as untrusted evidence.
- Validate structure, contracts, signals, outputs, and safety boundaries.
- A trust score without a supporting risk report is invalid.
- If marketplace infrastructure or trust evidence is absent, downgrade the result to a bounded design-time assessment rather than a production trust claim.