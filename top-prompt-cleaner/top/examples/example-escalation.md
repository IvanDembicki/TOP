# Example: FactoryEscalationController — escalated case

## Input prompt (raw)

```
Create a system where one AI generates product ideas, a second AI reviews them for market fit,
a third one writes the pitch, and then based on the pitch score it decides whether to send to
investors or loop back for revision.
```

## ComplexityDetector result

```json
{
  "complexity_level": "high",
  "signals": [
    "multiple AI agents with distinct roles",
    "conditional routing based on runtime score evaluation",
    "stateful loop-back behavior",
    "multi-step workflow with inter-agent communication"
  ],
  "recommendation": "escalate"
}
```

## Escalation notice

This prompt describes a multi-agent workflow with conditional routing and stateful loops.
It is not a single prompt to be cleaned — it is a system design task.

**Signals that triggered escalation:**
- Three distinct AI agents with separate responsibilities
- Routing logic between agents based on a score evaluation
- Conditional loop requiring shared state across steps

**What TOP Skill Factory can help with:**
- Define the agent tree and node contracts for each role
- Design structured signal passing between agents
- Set up validation and decision logic for the routing step

**Recommended next step:** Use TOP Skill Factory in CreateNewSkillMode.

## Final state: escalated

**Full final output (machine-verifiable contract):**

```json
{
  "status": "escalated",
  "escalation_notice": {
    "reason": "Prompt describes a multi-agent workflow with conditional routing and stateful loops. This is not a single prompt to be cleaned — it is a system design task.",
    "signals": [
      "multiple AI agents with distinct roles",
      "conditional routing based on runtime score evaluation",
      "stateful loop-back behavior",
      "multi-step workflow with inter-agent communication"
    ],
    "recommended_next_step": "Use TOP Skill Factory in CreateNewSkillMode to define the agent tree and node contracts."
  }
}
```
