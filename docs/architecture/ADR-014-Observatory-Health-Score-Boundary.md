# ADR-014: Observatory Health Score Boundary

**Status:** Proposed  
**Date:** 2026-09-18  
**Release:** Release 2.x  
**Capability:** BKL-036

## Context

The roadmap selects BKL-036 after BKL-032 to organize telemetry, EAGLE, network, power, services and scientific-pipeline evidence. Without an explicit boundary, a health score could be confused with readiness, safety, anomaly diagnosis or remediation.

## Decision drivers

- preserve local physical interlocks as the only Safety Authority;
- keep BKL-031 planner and BKL-032 readiness separate;
- make source quality, freshness and missingness visible;
- avoid introducing unapproved thresholds or runtime traffic;
- enable later deterministic validation and explainable reporting.

## Considered options

1. Extend BKL-032 with a health score — rejected because readiness and health semantics have different consumers and authority boundaries.
2. Introduce an immediate numeric score — rejected because source comparability, weights and thresholds are not yet governed.
3. Define BKL-036 as source discovery and a descriptive semantic contract — selected.

## Decision

BKL-036 begins as a repository-only, read-only source-discovery and semantic-contract package. It may define `HEALTH_EVIDENCE`, `HEALTH_DIMENSION` and `DESCRIPTIVE_HEALTH_STATUS`, but not an aggregate score, threshold policy, Safety Score, recommendation, remediation or device command.

Any future aggregate score requires a new governed decision increment with explicit source comparability, policy, validation evidence and authority wording.

## Consequences

### Positive

- prevents premature operational interpretation;
- preserves fail-closed and provenance semantics;
- allows source gaps to be measured before implementation;
- keeps BKL-031, BKL-032 and local interlocks independent.

### Negative

- no numeric health score is available in this increment;
- source discovery may expose unresolved runtime dependencies;
- later policy work remains necessary.

### Risks

- descriptive status could be misread as safety status;
- stale or partial data could be presented as healthy;
- host health could be confused with apparatus or scientific quality.

## Migration

No runtime, data, provider or device migration. Later increments must consume the versioned semantic contract and pass independent review. Rollback is a documentation revert.

## Validation

Validate source inventory, semantic categories, missingness, freshness, provenance, privacy and authority boundaries locally and in CI. Do not claim runtime acceptance from repository adapters or historical evidence.

## Traceability

- `docs/architecture/packages/BKL-036-Observatory-Health-Score.md`
- `docs/project/BKL-036-SOURCE-DISCOVERY-2026-09-18.md`
- BKL-030 closure and telemetry foundations
- BKL-031 closure and ADR-012
- BKL-032 closure and ADR-013
- DSG-AEM-001 v1.2
