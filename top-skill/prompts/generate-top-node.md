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
- enforce Controller Role Purity
- node constructor receives only the parent reference as semantic input
- do not generate the Node/Controller as a framework-rendered component, widget, composable, render/build function, platform UI lifecycle object, or equivalent target-renderable entity
- renderable target artifacts belong to Content/View or thin adapters, not to the controller
- Content/View constructor receives exactly one narrow typed access interface implemented by the owning controller
- zero-contract content-to-controller access is an empty owner access interface implemented by the controller; do not generate `ControllerAccessZero` dummy objects
- controller stores and uses content through `IContentAccess`, not through the concrete Content/View class
- do not type Content/View against the concrete controller, and do not import/downcast back to it
- do not generate semantic injection through constructor parameters, public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, child components, platform child views, child-output getter bundles, or prebuilt fragments
- if the target materializes Content through one public runtime input object/value, generate that input as exactly the narrow owner access contract and nothing else
- do not replace `IControllerAccess` with an externally assembled access bundle, even when the bundle contains correctly named methods
- generate `IControllerAccess` methods as controller-boundary methods owned by the controller; they may delegate internally, but do not expose raw imported functions, external method references, service methods, store actions, or callbacks directly to Content as access methods
- Content pulls from owner; owner pulls from children when child output is required; children expose opaque handles
- name child-output access methods by semantic branch/output, for example `getAccountIdentityView()`; do not require `Handle`/`ViewHandle`, do not use `slot`, and avoid generic `children`/`render`/`builder` names
