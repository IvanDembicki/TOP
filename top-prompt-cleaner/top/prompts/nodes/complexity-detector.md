# ComplexityDetector

Responsibility: determine whether the input describes a single-prompt task or a multi-step workflow that exceeds single-prompt scope.

Input:
- raw_prompt

Output:
- complexity_report containing: complexity_level (low / medium / high), signals, recommendation

Signals that indicate high complexity:
- multiple AI agents or coordinated AI roles
- stateful multi-step flows where outputs feed subsequent steps
- conditional routing between different behaviors based on runtime evaluation
- references to other prompts, external systems, or inter-component communication
- the prompt is designing an AI system or workflow, not describing a task for one model

Medium vs high boundary:
- medium = sequential instructions for ONE model; no separate agents; no persistent shared state; no external handoff; conditional logic stays within a single model context
- high = any hard signal: multiple AI agents, stateful loops across steps, external system routing, designing an AI system (not using one)

Process:
- inspect raw_prompt for each signal type
- assign complexity_level based on signal count and severity:
    low: zero signals
    medium: sequential or conditional logic within a single model — no agents, no state, no external handoff
    high: any hard signal (multi-agent, stateful routing, system design)
- record which specific signals triggered the assessment

Boundaries:
- a long or detailed prompt is not automatically high complexity
- do not conflate detailed requirements with multi-step architecture
- medium complexity proceeds with a note in diff; high complexity always escalates

Invalid output conditions:
- high complexity assigned without naming a triggering signal
- low complexity assigned to a prompt that contains multi-agent or routing language

Rules:
- high complexity routes to FactoryEscalationController; no other mode is selected
- medium complexity proceeds to QuickCleanMode with a complexity_warning in the output
- complexity_report is the sole authority for escalation routing
