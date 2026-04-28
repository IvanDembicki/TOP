# ResearchForInsight

Responsibility: produce an open-ended landscape report to deepen understanding of a domain before or alongside skill design decisions.

Input:
- normalized_input
- discovery_result
- existing_solution_check_result (optional, for context)
- user_research_focus (optional: specific questions or areas the user wants investigated)

Output:
- research_report

Report must include:
- landscape_summary
- known_approaches (list)
- identified_gaps (what the landscape does not cover)
- relevant_patterns (reusable patterns or conventions found)
- open_questions (unresolved questions that may affect design)
- sources_reviewed
- time_box_status (within | exceeded)

Primary objectives:
- build understanding, not find a drop-in replacement
- surface patterns, conventions, and gaps that are not obvious from the goal description alone
- produce actionable input for subsequent design decisions

Process:
- accept user_research_focus if provided; otherwise derive focus areas from normalized_input and discovery_result
- investigate internal inventory, external sources, and domain knowledge
- record every reviewed source explicitly
- stop at the time-box limit and deliver findings as-is with a note if incomplete

Boundaries:
- do not make build/reuse/adapt decisions here — that is ExistingSolutionCheck's responsibility
- do not begin tree design in this node
- do not treat the report as a blocker; it is additive context, not a gate

Time-box rule:
- default limit: 60 minutes
- record `time_box_status: exceeded` and deliver partial findings if the limit is reached
- do not silently extend

## User-facing question

Before running, ask the user in their language. Canonical meaning:

> Would you like me to first explore existing solutions in the market — reviewing the approaches and practices in use, their strengths and weaknesses — so that I can work on your skill with you more precisely and with greater depth?

Adapt the phrasing to the user's language while preserving the meaning exactly: offer to study existing market solutions and practices to enable more informed and specific collaboration on the user's skill.

Rules:
- this node runs only when the user explicitly confirms after being asked
- the decision to run is the user's alone; it does not depend on prior pipeline results
- the question must always be asked before running — never run silently or by default
- findings are advisory; they do not override decisions already made in prior steps
- all sources must be listed; "I searched broadly" is not a valid source record
