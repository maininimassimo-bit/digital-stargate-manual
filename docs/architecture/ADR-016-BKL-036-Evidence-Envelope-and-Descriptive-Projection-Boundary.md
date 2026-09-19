# ADR-016 — BKL-036 evidence envelope and descriptive projection boundary

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-09-19 |
| Release | Release 2.x |
| Capability | BKL-036 |
| Scope | Repository-only evidence envelope and descriptive projection |

## Context

BKL-036-F1 established source mapping and evidence compatibility, but it did not define a versioned exchange shape for preserving evidence status, compatibility, freshness and authority without implying a live runtime or aggregate score.

## Decision drivers

- preserve the distinction between repository evidence, live telemetry and runtime acceptance;
- make missing, stale, unavailable, partial and conflicting evidence fail-closed;
- provide an explainable descriptive projection without numeric scoring or operational policy;
- support deterministic offline validation and bounded regression fixtures.

## Considered options

1. Reuse BKL-032 readiness contracts — rejected because readiness/go-no-go belongs to BKL-032.
2. Introduce an aggregate health score — rejected because comparability, weights and thresholds remain ungoverned.
3. Define a versioned evidence envelope and descriptive projection — selected.

## Decision

BKL-036-F2 defines the contract DSG.BKL036.F2.EvidenceEnvelope version 1.0.

The envelope contains exactly the seven BKL-032 operational domains as evidence dimensions: weather, dome, mount, camera, power, network and eagle health. Each entry preserves source authority, semantic field, unit, observation timestamp, freshness state, F1 evidence status, F1 compatibility, runtime disposition and privacy classification.

The bounded projection may expose only a descriptive status (AVAILABLE, DEGRADED, UNKNOWN, UNAVAILABLE or CONFLICTING) with reasons. It must declare score_available=false, authority=projection and action_authority=NONE.

The contract deliberately has no score, threshold, weight, ranking, readiness, recommendation, remediation, scheduling, command or Safety Authority field.

## Migration and validation

The first fixture is synthetic and offline. The validator and negative regression suite run in Developer Foundation CI. No live source, transport, consumer, EAGLE or CloudWatcher runtime is used.

## Consequences

Positive: evidence semantics become machine-readable, auditable and fail-closed before any future policy decision.

Negative: the fixture does not establish current observatory state or cross-domain score comparability.

## Traceability

- ADR-014 — BKL-036 Observatory Health Score Boundary
- ADR-015 — BKL-036 source mapping and evidence compatibility boundary
- docs/architecture/telemetry/BKL-036-F2-Evidence-Envelope-and-Descriptive-Health-Projection.md
- contracts/telemetry/bkl-036-f2-evidence-envelope-v1.schema.json
