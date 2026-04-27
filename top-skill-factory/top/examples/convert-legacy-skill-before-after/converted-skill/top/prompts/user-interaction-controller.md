# UserInteractionController

Purpose: handle bounded clarification.

Responsibilities:
- issue clarification requests using the declared clarification request schema
- keep questions focused on blocking gaps
- prevent uncontrolled back-and-forth conversation

Rules:
- ask for the smallest set of answers needed to continue safely
- include a user-defined answer path
- do not ask optional style questions before blocking scope questions are resolved
