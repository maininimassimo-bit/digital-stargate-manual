# BKL-031 F3-C — Bounded Integration Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Capability | BKL-031 F3-C |
| Adapter | `BKL031-F3C-BOUNDED-ADAPTER@1.0` |
| Projection | `BKL031_F3C_BOUNDED_SANITIZED_PROJECTION` |
| Projection digest | `94278cfd22417943c7642038ae2527d6065bcfca74add47c93e4a5599f3ddc40` |
| Reviewed head | `5d6b7127475c9378e19b1bfc5e65f6ad11f597f1` |
| Pull request | [#261](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/261) |
| Merge commit | `fba1287efea0d1f36b147bc42a4fec5498990756` |
| Executable tests | 35/35 passing locally and in governed CI |
| Portal route | [Observation Planner](https://maininimassimo-bit.github.io/digital-stargate-manual/observation-planner/) — verified after deployment |
| Runtime effect | None; S10 remains `UNAVAILABLE` |

## Accepted decision

The F3-C repository increment passed exact-head ARB and Release Quality review on `5d6b7127475c9378e19b1bfc5e65f6ad11f597f1`. Pull request #261 completed all 16 required checks successfully and was merged with expected-head control as `fba1287efea0d1f36b147bc42a4fec5498990756`. It converts only the accepted F3-B `TEST` / `NONE` fixture into a deterministic sanitized projection, verifies the projection again in the browser and renders a dedicated read-only Observation Planner page.

## Acceptance matrix

| Gate | Accepted disposition |
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

## Post-merge verification

All 12 applicable push workflows completed successfully against the exact merge commit: F3-C Governance `35194573308`, F3-B Governance `35194573310`, F3-A3 GCP IaC Validation `35194573353`, Developer Foundation `35194573367`, Pages `35194573317`, documentation validation `35194573392`, Word generation `35194573406`, Governed Projection Sync `35194573295`, Scientific Platform Governance `35194573351`, BKL-041 F4 Governance `35194573383`, BKL-046 F4 governance `35194573354` and BKL-046 F5 governance `35194573361`.

The public route loaded from GitHub Pages after deployment with the expected navigation entry, JavaScript module, CSS, governed JSON projection, 9 sanitized facts and digest `94278cfd22417943c7642038ae2527d6065bcfca74add47c93e4a5599f3ddc40`.

Acceptance authorizes the repository adapter and TEST-only public projection. It does not activate production S10, authorize protected-site calculation, permit another cloud execution or external-reference call, or promote F4 forecast, F5 ranking/consumer, BKL-032 readiness, commands or Safety Authority. F4 forecast source discovery and integration contract is the next independent gate.
