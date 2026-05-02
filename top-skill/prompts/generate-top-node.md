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
- do not generate semantic injection through constructor parameters, public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, child components, platform child views, child-output getter bundles, or prebuilt fragments
- do not replace `IControllerAccess` with an externally assembled access bundle, even when the bundle contains correctly named methods
- Content pulls from owner; owner pulls from children when child output is required; children expose opaque handles
- name child-output access methods by semantic branch/output, for example `getAccountIdentityView()`; do not require `Handle`/`ViewHandle`, do not use `slot`, and avoid generic `children`/`render`/`builder` names
