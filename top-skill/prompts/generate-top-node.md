# generate-top-node

agent: Generation Agent

input_contract:
- approved_top_model
- semantic_interpretation_output
- target_adaptation_output

output_contract:
- generated_artifact

rules:
- no architecture change
- generate from Layer B semantic intent and Layer C target adaptation, not from source-platform primitives
- do not invent behavior absent from the semantic layer
- enforce Pull-Based Construction / Locality of Object Birth
- node constructor receives only the parent reference as semantic input
- Content/View constructor receives exactly one narrow typed access interface implemented by the owning controller
- zero-contract content-to-controller access is an empty owner access interface implemented by the controller; do not generate `ControllerAccessZero` dummy objects
- controller stores and uses content through `IContentAccess`, not through the concrete Content/View class
- do not type Content/View against the concrete controller, and do not import/downcast back to it
- do not generate semantic injection through constructor parameters, runtime props, slots, builders, render parameters, callbacks, stores, services, child components, platform child views, or prebuilt fragments
- View pulls from owner; owner pulls from children; children expose opaque handles
- name child-output access methods by semantic branch/output, for example `getAccountIdentityView()`; do not require `Handle`/`ViewHandle`, do not use `slot`, and avoid generic `children`/`render`/`builder` names
