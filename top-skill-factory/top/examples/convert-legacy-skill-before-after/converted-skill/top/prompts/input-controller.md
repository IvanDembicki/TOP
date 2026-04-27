# InputController

Purpose: normalize the user request before routing.

Responsibilities:
- extract goal, audience, timeline, and success criteria when present
- identify whether the request is compact, strategic, or underspecified
- classify missing information as either safe visible assumption material or blocking scope gaps

Rules:
- missing scope, timeline, owner, or success criteria are blocking when they materially change the plan
- a rushed tone lowers verbosity, not safety thresholds
- strategic indicators must be made explicit before detailed routing
