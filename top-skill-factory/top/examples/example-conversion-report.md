# Example: Conversion report

```json
{
  "source_artifacts": [
    "legacy-skill.md",
    "examples/legacy-usage.md"
  ],
  "detected_issues": [
    {
      "category": "mixed_responsibility",
      "description": "One large prompt mixed routing, validation, and output behavior.",
      "status": "resolved"
    },
    {
      "category": "hidden_assumption",
      "description": "The legacy skill assumed a fixed output format without declaring it as a contract.",
      "status": "resolved"
    },
    {
      "category": "blind_spot",
      "description": "Failure behavior for missing user data was not specified.",
      "status": "partially_resolved"
    }
  ],
  "preserved_behavior": [
    "The converted skill still produces a concise user-facing result.",
    "The converted skill still escalates to the user when the request is underspecified."
  ],
  "structural_changes": [
    "Routing behavior was separated from validation behavior.",
    "Output rules were turned into explicit validation artifacts.",
    "Blind-spot handling was made explicit."
  ],
  "unresolved_gaps": [
    "Detailed failure copy still needs user confirmation."
  ],
  "final_status": "partial",
  "final_rationale": "The conversion removed major structural drift, but one product-facing ambiguity still requires confirmation."
}
```