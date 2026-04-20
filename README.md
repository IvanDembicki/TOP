# TOP Skill — Tree-Oriented Programming

**Version:** 1.0.0 | **License:** CC BY-NC 4.0 | **Invocation:** `/top`

A skill for AI-driven design, generation, and validation of systems built with the **Tree-Oriented Programming (TOP)** paradigm.

---

## What is TOP?

TOP is a programming paradigm in which any system is modeled as a strictly typed tree of nodes.

The tree is the structural model of the entire system. It defines composition, state organization, and how the system evolves over time.

TOP extends OOP: if OOP defines how individual objects work, TOP defines strict rules for their composition and interaction within the system as a whole.

The practical goal is **complexity control**. Without explicit structural constraints, cross-dependencies tend to grow as O(n²). TOP constrains them through a typed tree and keeps growth closer to O(n).

---

## What this skill provides

This is a complete AI-native development system:

- **Architectural model** — typed tree, node contracts, controller/content split, state machines
- **Generation protocol** — pipeline `spec → prompt → code → verification`
- **Validation system** — canon rules, violation catalog, audit agents
- **Multi-target generation** — one spec tree generates implementations for Web, Android, React Native, and other platforms

The sufficient operational unit in TOP is the pair **`spec + prompt`**. Code is a derived artifact. The spec and prompts remain the source of truth.

---

## Benefits

1. **Complexity grows linearly** — typed tree constrains cross-dependencies; growth stays near O(n) instead of O(n²)
2. **Multi-platform from one spec** — one tree generates Web, Android, React Native, and other targets without rewriting architecture
3. **Verifiable architecture** — canon rules and audit agents validate structural correctness at any point
4. **Control under AI generation** — the system stays controllable and transparent even when AI generates most of the code
5. **Full regenerability** — spec and prompts are the source of truth; code can be regenerated at any time on any platform
6. **Local context per node** — each node is self-contained; AI works effectively without knowing the entire system
7. **Parallel development by design** — independent branches can be developed simultaneously without conflicts

---

## Getting started

Give your AI the link to this repository:

```
Load the TOP skill from https://github.com/IvanDembicki/TOP
```

The AI will load all the knowledge it needs about the paradigm and can start applying TOP in your work. Type `/top` to begin.

---

## Pipeline

```
Spec tree (JSON)
    ↓
Node Implementation Prompts (language-agnostic)
    ↓
Generated code (any platform)
    ↓
Verification (canon rules + audit agents)
```

The architecture stays recoverable and regenerable at any point. AI generates and verifies within the model — it does not replace architectural decisions.

---

## Agent pipeline

The skill includes a full agent pipeline:

**Intake → Domain Structuring → TOP Modeling → Canon Precheck → Semantic Interpretation → Target Adaptation → Generation → Spec Sync → Validation → Repair → Final Audit**

Task modes: `analysis-only` · `modeling-refactor` · `generation-pipeline` · `spec-change`

---

## License

CC BY-NC 4.0 — free for non-commercial use with attribution.
