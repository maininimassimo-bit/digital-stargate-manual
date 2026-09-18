# BKL-036 — Source Discovery Record

| Field | Value |
|---|---|
| Identifier | `BKL-036-SOURCE-DISCOVERY-001` |
| Status | Closed / Accepted / Post-Merge Verified |
| Capability | Observatory Health Score |
| Date | 2026-09-18 |
| Architecture package | `BKL-036-ARCH-001` |
| Validation plan | `BKL-036-VAL-001` |
| Runtime impact | None |

## Boundary

BKL-036 starts with source discovery and a semantic contract. It does not implement or publish a numeric score. It does not define thresholds, weights, RAG bands, Safety Score, anomaly diagnosis, predictive maintenance, recommendation, remediation, scheduling or device commands.

## Candidate source domains

| Domain | Candidate repository authority | Current classification |
|---|---|---|
| EAGLE host health | BKL-030 EAGLE health foundation | Repository evidence exists; live cross-domain acceptance open |
| Network | BKL-027/BKL-028 and telemetry architecture | Source mapping required; runtime acceptance open |
| Power | BKL-027/BKL-028 and telemetry architecture | Source mapping required; runtime acceptance open |
| Dome/mount/camera/services | Observatory telemetry and adapter records | Must distinguish availability from Safety Authority |
| Producer/telemetry freshness | Telemetry producer health contracts | Candidate evidence; freshness semantics to validate |
| Scientific pipeline | Session and processing lineage | Use only with resolvable session/provenance evidence |

## Required semantic distinctions

`HEALTH_EVIDENCE` is source-backed. `HEALTH_DIMENSION` groups evidence. `DESCRIPTIVE_HEALTH_STATUS` is advisory and read-only. `OBSERVATORY_HEALTH_SCORE`, `RECOMMENDATION` and `SAFETY_STATE` are outside this gate.

Missing, stale, partial, unavailable and conflicting evidence must remain explicit and must not be converted into healthy/default values.

## Open issues

- confirm mandatory source domains with the owner;
- document freshness and retention per source;
- resolve cross-domain comparability;
- decide whether a future aggregate score is useful after source validation;
- keep live source/transport acceptance as a separate gate.

## Next governed step

Source discovery and semantic-contract review are accepted. The next separate increment is **BKL-036-F1 — Governed Source Mapping and Evidence Compatibility**, which remains repository/documentation-only. Any aggregate score or runtime consumer requires a further governed increment. No implementation or external traffic is authorized by this closure.
