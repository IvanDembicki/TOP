# Node Validation Rules

This file defines mandatory post-generation / post-refactor validation for node-level implementation.

Successful compilation, local operability, or passing partial framework checks do not imply architectural correctness.
A node implementation is not considered correct until the full cycle has been completed:
- identify the class of violation;
- classify it as `confirmed`, `possible`, or `ambiguity`;
- choose the canonical correction direction;
- re-validate the result after the fix.

Anything else is strictly prohibited.

---

## 1. Boundary validation

Required checks:
- if the node has a separate content, the controller does not bypass the content boundary through direct access to the concrete implementation;
- if the controller performs any operation on its own content implementation, it does so only through explicitly named `this.content.<command>(...)` methods on `IContentAccess`;
- controller code does not use the node's own render/view/native primitive, its platform API, or an equivalent exposed primitive handle, except inside the implementation of `getView()` itself and parent-owned placement/composition code that treats a child view as an opaque handle (detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().removeEventListener`, `this.getView().setAttribute`, `this.getView().querySelector`, `content.getView()`);
- if a child view is obtained through `getView()`, it is used only as an opaque materialization handle for mount/unmount/insert/reorder/replace/placement through the parent's content boundary;
- the parent/controller does not attach event listeners to a child view, mutate its styles/classes/attributes, query inside it, or use its platform API as a behavior or communication channel;
- content does not gain access to the public node surface;
- content does not reach the outside world through surrogate channels;
- internal implementation details are not used as a communication channel.

Canonical correction direction:
- move interaction into an explicit external interface of the content;
- remove direct controller bypass;
- replace direct platform primitive access with named content commands on `IContentAccess`;
- restrict `getView()` usage to parent-owned placement/composition only;
- close any surrogate channels.

---

## 2. Protocol artifact validation

Required checks:
- if the node has a separate content, there exists a separate explicit restricted-access artifact for content to access the controller;
- the artifact is narrow and whitelist-only;
- the artifact is explicitly typed where the language permits;
- the artifact is materialized as a separate named contract artifact, not as an anonymous object shape;
- the constructor/factory/method parameter receiving the artifact is explicitly typed where the language permits;
- the field/reference storing the artifact is explicitly typed where the language permits;
- if content access to the controller is permitted, the artifact is not an empty formal stub;
- if the artifact is empty, it explicitly signifies a complete prohibition of content access to the controller;
- the artifact does not contain parent/root/host/container/integration handles.

Canonical correction direction:
- materialize a separate protocol artifact;
- remove extraneous fields;
- fix an explicit contract type;
- remove anonymous/untyped protocol parameters.

---

## 3. Content behavior validation

Required checks:
- content has no architectural will;
- content does not decide to attach/integrate/mount/remove/show/hide/destroy as an architectural or lifecycle action;
- content may execute low-level platform commands on its own implementation material, including subscribe/unsubscribe and analogous platform operations, when those commands are part of content materialization or are requested through the content boundary;
- content does not make lifecycle and structural decisions;
- content does not interpret its own events as system commands.

Canonical correction direction:
- leave in content only allowed construction/update/platform-command/event-forwarding behavior;
- return lifecycle and structural decisions to the controller.

---

## 4. Controller behavior validation

Required checks:
- the controller remains the owner of node behavior;
- the controller manages lifecycle and orchestration;
- the controller does not use concrete implementation as a communication channel;
- the controller works with the implementation only through the content object and its external interface;
- the controller never performs visual/platform operations through inherited primitive fields or getters; it delegates such operations to named content commands;
- a public/base-class primitive getter is not used as justification for controller access to the concrete implementation.

Canonical correction direction:
- move behavior ownership to the controller;
- move concrete implementation access behind the content boundary.

---

## 5. Method semantics validation

Required checks:
- `buildChildren()` is used only for runtime child materialization;
- any analogous materialization/lifecycle methods have not been turned into an init bucket;
- method name does not mask a foreign semantic role.

Canonical correction direction:
- separate init/materialization/update/lifecycle responsibilities into their proper semantic methods;
- remove the method if its semantic role is absent.

---

## 6. Content lifecycle validation

Required checks:
- content is created on demand;
- content is destroyed when the node/branch becomes inactive, unless a retention pattern is explicitly declared;
- permanent content is absent by default.

Canonical correction direction:
- switch the lifecycle to create-on-demand / destroy-on-inactive;
- extract retention into a separate explicit pattern if it is genuinely needed.

---

## 7. Phase Separation Validation

Required checks:
- content materialization has a clear semantic boundary, whether implemented in a constructor, a dedicated method, or another target-native phase;
- child materialization has a clear semantic boundary, whether implemented in a constructor, a dedicated method, or another target-native phase;
- the constructor does not attach or mount this node's view into an external container;
- the constructor does not perform lifecycle activation/deactivation behavior that belongs to `onOpen()` / `onClose()` or equivalent;
- if the technology provides semantic lifecycle methods, each has one role and that role is not duplicated elsewhere.

Canonical correction direction:
- move content creation into the content materialization phase or method;
- move child materialization into the child materialization phase or method;
- move mount/attach logic to the parent's composition method.

---

## 8. Self-Mount Validation

Required checks:
- no child node calls `parent.content.mount()`, `parent.el.appendChild()`, or any equivalent on its own view from within itself;
- `onOpen()` does not attach the node's view into any external container;
- `onClose()` does not contain cross-boundary detach operations attributed to the parent's integration surface;
- no lifecycle hook performs self-insertion into a parent integration surface.

Canonical correction direction:
- move mount calls to the parent's `openChild()` or `buildChildren()`;
- child exposes `getView()`; mounting decision belongs to the parent.

---

## 9. Content Class Materialization Validation

Required checks:
- if the node has `contentType` in the spec, a separate content class exists in implementation;
- the content class is not a thin formal stub with actual platform logic remaining in the controller;
- the controller does not construct platform primitives inline as a substitute for the content layer;
- all platform-primitive construction is inside the content class, not in the controller.
- generated declarations follow architectural depth from outside to inside: controller/node first, internal access boundary artifact(s) next, content/view implementation last.

Canonical correction direction:
- create a separate content class;
- move platform construction into it;
- controller accesses content through `IContentAccess`.
- reorder declarations so the access boundary stands between the controller and the hidden content/view implementation.

---

## 10. Validation outcome

The result of a validation must always contain:
1. the identified class of problem;
2. confidence level (`confirmed` / `possible` / `ambiguity`);
3. canonical correction direction;
4. re-validation status after the fix.

If re-validation is absent, the work is not considered complete. Anything else is strictly prohibited.
