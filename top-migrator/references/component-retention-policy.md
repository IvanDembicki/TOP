# Component Retention Policy

TOP migration should not convert every technical component into a TOP node.

## Components That May Stay Components

A local component may remain unchanged and be used inside view/content when it is:

- small;
- stable;
- locally understandable;
- presentation-focused;
- not a source of business state;
- not a source of lifecycle ownership;
- not responsible for async workflows;
- not directly coupled to global store, router, API, singleton service, or cross-branch mutation;
- not a form/modal/list/item/card/row/panel with independent behavior;
- not expected to grow into a larger subsystem.

Examples:

- button;
- icon;
- badge;
- simple input wrapper;
- static layout primitive;
- simple typography component.

## External Library Components

External components are normally not rewritten into TOP.

If simple, use them as platform/view primitives inside content.

If complex, wrap them as a black-box component or adapter boundary with a narrow contract. Do not claim the external component internals are TOP-valid.

Record:

- package/library name;
- component name;
- owner/maintainer if known;
- whether adapter is required;
- risk and update policy.

## TOP Candidate Components

Mark a component as a TOP migration candidate when it has:

- application state or state alternatives;
- independent lifecycle;
- subscriptions or async flows;
- API/store/router/singleton access;
- own validation/save workflow;
- modal/form/list/item/card/row/panel behavior;
- permission/status/mode branches;
- business decisions;
- wide props/callback surface;
- repeated semantic structure worth extracting as a reusable node or library node.

Size alone is not decisive. A large static view can remain a component. A small workflow-bearing component may need TOP migration.

## Final Inventory Requirement

Final migration reports must include:

```text
Preserved components:
- name/path
- internal or external
- why preserved
- where used
- risk of future TOP migration

TOP candidate components:
- name/path
- reason
- likely TOP role
- priority
- suggested migration trigger

Black-box components:
- source/library
- boundary contract
- adapter requirement
- unverified assumptions

Temporary residual components:
- reason retained
- expiry condition
- target repair direction
```
