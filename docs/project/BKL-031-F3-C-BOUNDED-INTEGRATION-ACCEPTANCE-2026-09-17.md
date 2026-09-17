# BKL-031 F3-C — Bounded Integration Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTANCE CANDIDATE — POST-MERGE VERIFICATION PENDING** |
| Date | 2026-09-17 |
| Capability | BKL-031 F3-C |
| Adapter | `BKL031-F3C-BOUNDED-ADAPTER@1.0` |
| Projection | `BKL031_F3C_BOUNDED_SANITIZED_PROJECTION` |
| Projection digest | `94278cfd22417943c7642038ae2527d6065bcfca74add47c93e4a5599f3ddc40` |
| Executable tests | 35/35 passing locally |
| Portal route | `/observation-planner/` |
| Runtime effect | None; S10 remains `UNAVAILABLE` |

## Candidate decision

The F3-C repository increment is ready for exact-head review. It converts only the accepted F3-B `TEST` / `NONE` fixture into a deterministic sanitized projection, verifies the projection again in the browser and renders a dedicated read-only Observation Planner page.

## Acceptance matrix

| Gate | Candidate disposition |
|---|---|
| accepted F3-B input required | PASS — validator invoked before adaptation |
| deterministic adapter and projection identity | PASS |
| exact normalized fact preservation | PASS — no repair or recomputation |
| half-open validity and availability preservation | PASS |
| public/internal separation | PASS — deny-by-default property set and protected-value scan |
| Citation/Provenance | PASS — exact repository-resolvable references |
| browser digest and boundary verification | PASS |
| portal route and fail-closed consumer | PASS locally |
| forecast/ranking/readiness/command/Safety exclusion | PASS |
| protected-site/external-reference/cloud/runtime boundary | PASS — zero activity |
| F2/F3-B regression | PASS — unchanged upstream artifacts |

## Promotion condition

Acceptance requires exact-head ARB and Release Quality review, all required pull-request checks, expected-head merge and successful post-merge workflows including Pages. The published route must load the exact governed projection after deployment.

Acceptance will authorize the repository adapter and TEST-only public projection. It will not activate production S10, authorize protected-site calculation, permit another cloud execution or external-reference call, or promote F4 forecast, F5 ranking/consumer, BKL-032 readiness, commands or Safety Authority.
