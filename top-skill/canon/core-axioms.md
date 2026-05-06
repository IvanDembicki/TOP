# Core Axioms

## Human readability

The code must be written to be maximally understandable to a human reader.
Clarity and unambiguity take priority over brevity or conciseness.

All structural and naming decisions must support fast, reliable understanding of the code at scale, without requiring implicit knowledge or guesswork.

## Typing

- Object typing must be as strict, explicit, and complete as the technology reasonably permits.
- If an explicit type contract can be defined, it must be defined.
- Weak, implicit, partial, or shape-based typing is non-canonical unless stricter typing is not realistically achievable in the given technology.

## Naming

- Code must remain readable at scale (volumetrically readable).
- Names must be fully descriptive and unambiguous.
- An abbreviation is allowed only if it is immediately clear without explanation
  to any developer in the given domain.
- Any abbreviation that requires explanation or domain-external context is a violation.

## Behavioral state split (hidden switchable)

A node is a hidden switchable if it independently manages switching between fundamentally different representations or behaviors by accessing external architectural state.

Detection criterion — both conditions must hold simultaneously:

1. The node reads external architectural state (mode, lifecycle phase, openedChild, etc.)
2. And as a result changes at least one of:
   - the visual representation of its constituent elements
   - the available behavior (drag, add, delete, etc. — either present or absent)

The number of explicit child nodes is irrelevant. A hidden switchable may be a monolithic node whose internal elements and handlers change.

Not a violation:
- A controller changes only already-resolved model data exposed through a narrow
  access contract while node behavior is identical in both states. Locally
  implemented content still may not derive or select label text, color, style,
  visibility, structure, handlers, or representation by itself.

Canonical refactoring: the node becomes an explicit switchable holder with child state nodes. Each state node fully owns its own representation and behavior. A state node does not read the external mode — it is itself the representation of that mode.

## Locally implemented content static materialization

Locally implemented content is static implementation material, not a decision
layer. Locally implemented content must not derive output values.

It must not contain conditional selection logic of any kind and must not derive
output values. It must not decide, derive, branch, select, toggle, format,
concatenate, hardcode, or compute which structure, class/style/token, text,
icon, visibility, handler, child output, platform primitive, representation,
output value, or capability should be used.

Locally implemented content may only materialize a structurally static content
shape and apply already-resolved primitive values received through its owning
controller access contract.

Even simple formatting or concatenation belongs to the owning controller. The
controller resolves the final primitive/output value; locally implemented
content only asks for that value and applies it.

Controller must not push presentation state or imperative mutation commands into
locally implemented content. Presentation changes flow as controller state
updates plus node/runtime dirty or lifecycle/render refresh, followed by content
pulling already-resolved primitive values through controller access.

This preserves deterministic materialization, cacheability, pre-rendering,
portability, and verifiability. If content contains selection logic, it becomes
a hidden decision engine and breaks the TOP boundary between controller/tree
decision ownership and content materialization.

## Context attachment, not data injection

TOP objects are context-bound, not parameter-bound.

Construction attaches an object to its ownership context. It does not fill that
object with the data, flags, callbacks, configuration, presentation values,
runtime state, services, stores, child views, or handlers it will use.

A TOP object constructor may receive only the narrow contextual reference needed
to place it inside the tree or boundary:
- a node receives its parent/context reference;
- locally implemented content receives its owning controller access contract;
- a connector or black-box boundary receives its explicit boundary interface.

After attachment, the object requests required information through that
contract. The owner remains responsible for exposing the contract, but it does
not push changing state or presentation decisions into the object through
constructor arguments or post-construction setters.

This preserves tree locality, predictable regeneration, cacheability,
pre-rendering, and a single narrow validation path for data flow.

## Presentation content and data content

The no-push presentation rule applies to locally implemented presentation,
rendering, and materialization content.

Presentation content reports intent. Controllers make decisions. Data
controllers mutate data. Presentation content later pulls resolved values.

Correct presentation flow:
1. user input in locally implemented content is reported as a semantic
   event/request to the owning controller;
2. the controller validates, interprets, and either updates its own state, calls
   an architecturally allowed data-node controller API, or raises the semantic
   event upward;
3. affected controllers or data controllers update;
4. the node/runtime marks dirty or requests refresh;
5. presentation content pulls already-resolved primitive values again.

Data content is different. A data node controller may expose domain methods such
as `setAge(value)`, `updateName(value)`, or `replaceRecord(record)` when the
relationship is architecturally allowed. Inside that same data node, the data
controller may mutate its own private data content through `IContentAccess` or
an equivalent internal storage boundary. Validation and business rules remain in
the data controller, not in raw data content.

External objects must not mutate data content directly. Presentation content
must not directly access or mutate data content.

## Migration decomposition axiom

Migration is architectural extraction, not wrapping.

A legacy screen, route, file, tab, section, or component names the analysis
scope. It does not prove that the result is one TOP node.

Migration must discover hidden objects, state holders, state alternatives,
runtime entities, async processes, forms, modals, lists, list items, data
owners, connectors, bridge boundaries, black-box components, and repeated
structures. The result must be an explicit tree of responsibilities.

A node with a giant controller access surface, many display-style methods, many
bridge hooks, many pending actions/mutations, or multiple independent
modal/form/list/workflow responsibilities is not "complete" by having a large
contract. It is a decomposition-risk signal until proven otherwise.

`PanelDisplayStyle` is not a substitute for node decomposition. It may represent
an already-resolved display value for a stable structural section, but it must
not conceal state alternatives, lifecycle-bearing branches, independent
workflows, forms, modals, permission-gated capabilities, or data ownership
boundaries.

## Behavioral coherence

A node must not simultaneously own capabilities with mutually exclusive preconditions.

If capability A requires condition X, and capability B requires condition NOT-X — they belong to different state nodes.

Detection criterion:

Conflicting event handlers in a single node — handlers for opposite sides of a single transition:
- `mouseenter` / `mouseleave` — hover state
- `mouseover` / `mouseout` — hover state
- `pointerdown` / `pointerup` — press state
- analogous pairs with mutually exclusive preconditions

The presence of such pairs in a single node means the node contains hidden internal state that must be explicitly extracted into state nodes.

Not a violation:
- A single node registers both handlers to manage one continuous behavior (e.g. drag: `pointerdown` begins, `pointerup` ends a single action).

Canonical refactoring: extract NormalState and HoverState (or equivalents) as child state nodes. Each state node owns only those handlers that are active in its state.

## Typing fallback hierarchy

Typing priority:

1. strict nominal typing
2. explicit structural typing
3. documented weak typing

Rules:
- Moving to a weaker level is permitted only if the technology syntactically does not support a stricter level
- Convenience, verbosity, implementation speed, and local familiarity are not grounds for weakening
- `Realistic` means only technical impossibility of stricter typing, not its inconvenience
- If weak typing is used, it must be explicitly documented as a fallback, not as a norm
