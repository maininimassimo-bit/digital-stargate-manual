# ADR-013: Session Readiness / Go-No-Go Boundary

**Status:** Accepted with Conditions
**Date:** 2026-09-18  
**Release:** Release 2.x

## Context

BKL-031 now provides a bounded advisory Observation Planner. The next governed capability is BKL-032 Session Readiness / Go-No-Go Decision Support. Without an explicit boundary, planner ranking, readiness, scheduling and safety could be conflated.

## Decision Drivers

- preserve local physical interlocks as Safety Authority;
- keep planner and readiness semantics independently testable;
- fail closed on missing, stale or conflicting evidence;
- avoid runtime, device and provider expansion in the first slice;
- maintain provenance, privacy and auditability.

## Considered Options

1. Extend BKL-031 with readiness semantics — rejected because it couples advisory planning and decision authority.
2. Let readiness issue device commands — rejected because command and Safety Authority remain outside scope.
3. Create a separate BKL-032 read-only decision-support boundary — selected.

## Decision

BKL-032 is a separate application capability. It consumes a declared session context and governed evidence, validates the evidence, and emits a versioned readiness record. Its result is decision support only. `GO` never authorizes a device action, schedule, dome movement or bypass of local interlocks.

The owner approved on 2026-09-18 that `GO` requires forecast, current astronomy, setup compatibility and read-only live telemetry for weather, dome, mount, camera, power, network and EAGLE health to be present, fresh, consistent and passing. `NO_GO` means valid current evidence contains at least one blocking failure. `INDETERMINATE` means any mandatory domain is missing or stale, or required evidence is conflicting or unavailable, and therefore fails closed. Forecast/readiness freshness is six hours; rain greater than zero blocks; wind/gust beyond documented local limits blocks. No runtime or public readiness claim is authorized until source mappings and local limit references are accepted.

## Consequences

### Positive

- clear separation of responsibilities;
- explainable and auditable evidence chain;
- deterministic negative-path testing;
- no dependency on S10 or live apparatus.

### Negative

- duplicated context/provenance contracts must be reconciled carefully;
- readiness cannot be inferred from planner ranking;
- initial capability is limited until governed evidence sources are available.

### Risks

- users may read `GO` as safety authorization;
- thresholds may be introduced without owner approval;
- stale forecasts may create false confidence.

## Migration

Reconcile closure references, approve the BKL-032 package, define contracts and fixtures, implement the fail-closed evaluator, then add a read-only consumer. Any runtime/device integration requires a new package and safety review.

## Validation

Required: schema validation, positive and negative fixtures, stale/conflict tests, privacy checks, architecture-layer checks, documentation/link validation, exact-head CI, ARB, Release Quality and post-merge verification.

## Traceability

- BKL-031 closure PR #301, merge `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`
- BKL-032 architecture package `BKL-032-ARCH-001`
- DSG-AEM-001 v1.2
- ADR-009, ADR-010, ADR-011 and ADR-012
