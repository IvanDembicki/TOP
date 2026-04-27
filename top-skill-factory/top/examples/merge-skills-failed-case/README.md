# MergeSkillsMode Failed Case

This example demonstrates a truthful `failed` outcome.

It is not a `blocked` case because the workflow is not merely waiting for user clarification.
It is not a `draft` case because there is no safe partial package worth presenting as reviewable output.

The failure happens because two source skills impose incompatible output authority and escalation policies, and the bounded repair budget is exhausted without finding a coherent merged contract.
