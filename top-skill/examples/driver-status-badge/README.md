# Driver Status Badge Example

This generated fixture demonstrates a tiny TOP-style controller/content split
for surfacing orchestration driver results.

- `DriverStatusBadgeController` owns semantic status values.
- `DriverStatusBadgeControllerAccess` is the narrow content access contract.
- `DriverStatusBadgeContent` asks its owner for typed output data and does not
  decide workflow readiness.
- The final readiness meaning still comes from the run verifier status and
  `deliveryStatus`.

This example is intentionally small so it can be used as a code-generation
dogfood target for top-skill 2.0 orchestration.
