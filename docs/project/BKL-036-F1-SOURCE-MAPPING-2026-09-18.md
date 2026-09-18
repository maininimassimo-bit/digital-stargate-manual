# BKL-036-F1 — Source Mapping and Evidence Compatibility Record

| Field | Value |
|---|---|
| Identifier | `BKL-036-F1-CLOSURE-001` |
| Status | Review candidate — repository/documentation-only |
| Date | 2026-09-18 |
| Capability | Observatory Health Score |
| Scope | Governed source mapping and evidence compatibility |
| Runtime impact | None |

## 1. Disposition

BKL-036-F1 maps repository evidence already accepted by BKL-030, BKL-031, BKL-032 and the telemetry foundations. It does not claim a live source chain, runtime consumer, score, policy, threshold or Safety Authority. Source mapping is deliberately separate from the earlier BKL-036 source-discovery gate and from any future score-policy increment.

## 2. Mapping rules

Every row records source authority, semantic field, unit, observation timestamp, freshness representation, evidence status, compatibility and the runtime disposition. `PRESENT` describes repository evidence; it is not a runtime acceptance state. Compatibility is a semantic comparison result, not a score input.

The canonical mapping is maintained in [`BKL-036-F1 governed source mapping`](../architecture/telemetry/BKL-036-F1-Governed-Source-Mapping-and-Evidence-Compatibility.md). The boundary decision is [`ADR-015`](../architecture/ADR-015-BKL-036-Source-Mapping-and-Evidence-Compatibility-Boundary.md).

## 3. Accepted separations

- BKL-031 remains advisory/read-only planning.
- BKL-032 remains readiness/go-no-go decision support and owns its approved weather policy.
- Repository evidence, live telemetry and runtime/consumer acceptance are distinct planes.
- Local physical interlocks remain the only Safety Authority.
- Missing, stale, unavailable, partial and conflicting evidence remains fail-closed.
- Historical session/pipeline evidence is context-only and cannot satisfy a live freshness claim.

## 4. F1 outcome

The mapping identifies reusable evidence for network availability, telemetry freshness and source-backed host/asset observations, while retaining `CONTEXT_ONLY`, `PARTIAL`, `UNAVAILABLE`, `INCOMPATIBLE` and `UNKNOWN` where semantics or runtime acceptance are incomplete. No cross-domain aggregate is currently comparable; the future score remains unimplemented and ungoverned.

## 5. Evidence and validation

The package is validated by `BKL-036-F1-Source-Mapping-Validation-Plan.md`. Required checks cover source ownership, field/unit/timestamp/freshness completeness, status semantics, compatibility rules, privacy, authority boundaries, traceability, Knowledge Graph, roadmap, navigation and regression checks for BKL-031/BKL-032.

## 6. Residual conditions

- Live source/transport acceptance per domain remains open.
- Retention and authoritative freshness rules remain source-specific and must not be generalized.
- Cross-domain comparability is not established for an aggregate score.
- Any score, threshold, ranking, recommendation, remediation, scheduling or command path requires a new governed increment.
