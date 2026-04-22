# Human Confirmation Protocol

This protocol defines when the agent stops to interact with a human
and what control options are provided.

---

## When the agent stops

- unresolvable ambiguity — the agent cannot make a justified assumption;
- exhaustion of verification loop attempts without a successful result;
- a conflict between the spec and code that requires a human decision;
- large or irreversible changes are expected;
- the task goes beyond the originally agreed scope.

---

## What the agent communicates when stopping

The agent must provide:
- what is known and what has been done;
- what is unknown or ambiguous;
- what the agent assumes by default if the human says "continue";
- what risk each option carries.

Stopping without this information does not allow the human to make a decision.

---

## Options for the human

| Option | Description |
|--------|-------------|
| Pause until instructions | the agent waits, the human formulates additional instructions |
| Request information | the human clarifies context, the agent continues with new data |
| Confirm assumption | the agent names a specific assumption, the human confirms or corrects it |
| Approve plan | the agent shows a plan of action, the human approves before execution |
| Narrow or expand scope | the human adjusts the task at the moment of stopping |
| Roll back last action | the human requests that the last action be undone before a decision is made |
| Continue once | the agent performs the next step and stops again |
| Continue without confirmations | the agent works autonomously until the task is complete |

The spectrum ranges from maximum control (pause) to full automation (no confirmations).

---

## Proposing a commit before large changes

If large or potentially destructive changes are expected,
the agent must propose making a commit of the current state
before beginning execution.

This allows changes to be easily rolled back if the result is unsatisfactory.

The agent does not make the commit itself — it only proposes it to the human.

## New files and Git

If new files were created during the work,
the agent proposes adding them to Git.

The agent does not add files to Git itself — it only informs the human
about which files were created and proposes adding them.

---

## When an agent audit is not sufficient

The final audit agent is an independent check, but still AI.

A human audit is necessary when:
- the result has architectural consequences that are difficult to reverse;
- the task touches on ownership boundaries between teams;
- the agent signals uncertainty or residual risks;
- the system is in production and the cost of error is high.

In all other cases, the final agent audit is sufficient.

---

## Canonical rule

The agent does not continue in the presence of unresolvable ambiguity without explicit human authorization.
The agent does not perform large or irreversible changes without a prior stop.
