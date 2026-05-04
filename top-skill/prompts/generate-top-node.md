# generate-top-node

agent: Generation Agent

input_contract:
- approved_top_model
- Behavior Preservation Plan when generating a migrated scope with legacy tests
- semantic_interpretation_output
- target_adaptation_output

output_contract:
- generated_artifact

rules:
- no architecture change
- generate from Layer B semantic intent and Layer C target adaptation, not from source-platform primitives
- for migrated scopes, generate from normalized requirements in the Behavior Preservation Plan as well as Layer B and Layer C
- do not invent behavior absent from the semantic layer
- do not lose, weaken, omit from prompts, or leave uncovered behavior proven by legacy tests
- generate or adapt TOP-compatible tests for each prompt requirement derived from legacy tests
- classify missing Behavior Preservation Plan as `WF-010` and test-covered behavior loss as `CORE-028`
- enforce Pull-Based Construction / Locality of Object Birth
- enforce Controller Role Purity
- node constructor receives only the parent reference as semantic input
- do not generate Node/Controller runtime inputs for semantic data, parent-derived facts, callbacks, services, stores, props/config/options, parameter bags, or runtime argument sets; use explicit pull access/update methods or modeled connector contracts instead
- do not generate the Node/Controller as a framework-rendered component, widget, composable, render/build function, platform UI lifecycle object, or equivalent target-renderable entity
- renderable target artifacts belong to Content or thin adapters, not to the controller
- Content constructor receives exactly one semantic value: the owning controller instance typed only as the narrow `IControllerAccess`/target-equivalent interface
- zero-contract content-to-controller access is an empty owner access interface implemented by the controller; do not generate `ControllerAccessZero` dummy objects
- controller stores and uses content through `IContentAccess`, not through the concrete Content class
- controller receives/stores/uses its own Content instance typed through
  `IContentAccess`; do not generate decomposed content command bags,
  facade/adapters, platform primitive handles, or inline closure objects
- do not generate `IContentAccess` as a data/view-model/state/callback bag for Content; Content pulls controller-owned data through `IControllerAccess`
- do not type Content against the concrete controller, and do not import/downcast back to it
- do not generate semantic injection through constructor parameters, public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, child components, platform child views, child-output getter bundles, or prebuilt fragments
- if the target materializes Content through one public runtime input object/value, generate that input as a target-required envelope containing exactly one controller-typed value, for example `access={controllerAsIControllerAccess}` or `controller={controllerAsIControllerAccess}`; do not generate separate JSX props for access methods
- do not replace `IControllerAccess` with an externally assembled access bundle, adapter/facade, method bag, or inline closure object, even when it contains correctly named methods
- generate `IControllerAccess` methods as controller-boundary methods owned by the controller; they may delegate internally, but do not expose raw imported functions, external method references, service methods, store actions, or callbacks directly to Content as access methods
- for shared derived facts, do not generate either duplicate derivation in multiple controllers or parent-to-child runtime input tunneling; generate an explicit typed access/update boundary, named controller method, or modeled connector contract, or report the model as blocked
- Content pulls from owner; owner pulls from children when child output is required; children expose opaque handles
- name child-output access methods by semantic branch/output, for example `getAccountIdentityView()`; do not require `Handle`/`ViewHandle`, do not use `slot`, and avoid generic `children`/`render`/`builder` names
