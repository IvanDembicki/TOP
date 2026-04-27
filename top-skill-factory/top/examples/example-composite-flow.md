# Example composite flow

Goal:
Safely convert an existing working skill without touching the original version.

Flow:
1. ForkExperimentMode
2. ConvertLegacySkillMode
3. CompareSkillMode
4. DocumentationMode
5. UserAcceptanceController
6. FinalDecisionController

Invariant:
The source skill is never overwritten.