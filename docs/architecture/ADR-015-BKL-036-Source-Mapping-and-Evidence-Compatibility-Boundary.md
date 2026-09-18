# ADR-015 — BKL-036 source mapping and evidence compatibility boundary

| Field | Value |
|---|---|
| Status | Accepted / Post-Merge Verified |
| Date | 2026-09-18 |
| Release | Release 2.x |
| Capability | BKL-036 |
| Scope | Governed source mapping and evidence compatibility; repository-only |

## Context

BKL-036 source discovery established the semantic boundary for a future Observatory Health Score but did not establish which repository evidence can be compared across dimensions. BKL-032 separately owns readiness decision support and its owner-approved weather policy. Existing telemetry artifacts mix repository contracts, historical evidence, local pilots and runtime-open interfaces. Treating their presence as runtime acceptance, or combining them as if they had the same semantics, would create an unsupported health claim.

## Decision

BKL-036-F1 introduces a governed mapping record with two independent classifications:

1. **Evidence status**: `PRESENT`, `MISSING`, `STALE`, `UNAVAILABLE`, `PARTIAL` or `CONFLICTING`.
2. **Compatibility**: `COMPARABLE`, `CONTEXT_ONLY`, `INCOMPATIBLE` or `UNKNOWN`.

The mapping must preserve, for every source field, source authority, semantic field, unit, observation timestamp, freshness representation, quality, privacy classification and repository locator. `PRESENT` means that repository evidence identifies the source or contract; it does not mean that a live BKL-036 consumer is accepted.

`COMPARABLE` is permitted only for evidence with the same semantic type, unit/scale, temporal basis, quality interpretation and authority boundary. It permits descriptive grouping only in this increment; it does not authorize an aggregate score, ranking, threshold or recommendation. `CONTEXT_ONLY` is retained for evidence useful to explain a dimension but not suitable for cross-source aggregation. `INCOMPATIBLE` is an explicit exclusion. `UNKNOWN` is used when compatibility cannot be decided from governed evidence.

The repository evidence plane, live telemetry plane and runtime/consumer acceptance plane remain separate. A candidate source is never promoted automatically because an adapter, pilot or historical record exists.

## Authority boundaries

- BKL-031 remains advisory/read-only planning.
- BKL-032 remains the owner of readiness/go-no-go decision support.
- Local physical interlocks remain the only Safety Authority.
- BKL-036-F1 defines no score, weights, thresholds, RAG bands, remediation, scheduling, transport, runtime or command path.

## Consequences

- Source gaps and incompatibilities become auditable before any future policy decision.
- Historical/session evidence cannot be silently reused as live observatory health.
- A later score policy must cite this mapping, resolve `UNKNOWN`/`PARTIAL`/`CONFLICTING` cases and receive a separate ARB and Release Quality review.
- Rollback is a documentation and projection revert; no data or runtime migration is introduced.

## Acceptance criteria

- Each BKL-036 dimension has an explicit source mapping or an explicit gap.
- Each mapping includes authority, field, unit, timestamp, freshness and evidence locator.
- Evidence status and compatibility are independent and fail-closed.
- Repository evidence, live telemetry and runtime acceptance are visibly separated.
- No score, threshold, command, remediation or Safety Authority change is introduced.

## Traceability

- ADR-014 — BKL-036 source-discovery boundary.
- ADR-013 — BKL-032 readiness boundary.
- `docs/project/BKL-036-F1-SOURCE-MAPPING-2026-09-18.md`.
- `docs/architecture/telemetry/BKL-036-F1-Governed-Source-Mapping-and-Evidence-Compatibility.md`.
- `docs/architecture/validation/BKL-036-F1-Source-Mapping-Validation-Plan.md`.
