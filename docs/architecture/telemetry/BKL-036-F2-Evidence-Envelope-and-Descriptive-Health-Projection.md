# BKL-036-F2 — Evidence Envelope and Descriptive Health Projection

| Field | Value |
|---|---|
| Identifier | BKL-036-F2 |
| Status | Accepted / Post-Merge Verified — repository-only |
| Version | 0.1 |
| Date | 2026-09-19 |
| Parent | BKL-036 — Observatory Health Score |
| Upstream | BKL-036-F1 Accepted / Post-Merge Verified |
| Authority | Projection only |
| Runtime impact | None |
| Safety Authority | No |

## 1. Purpose

Define a versioned evidence envelope and a bounded descriptive projection that preserve F1 evidence semantics without creating an operational health score.

## 2. Contract

The canonical contract is contracts/telemetry/bkl-036-f2-evidence-envelope-v1.schema.json.

Required envelope properties are:

- schema and contract version;
- synthetic/offline fixture declaration;
- projection and action authority;
- descriptive status with reasons and score_available=false;
- exactly seven governed domains;
- source authority, semantic field, unit, timestamp, freshness state, evidence status, compatibility, runtime disposition and privacy classification.

## 3. Descriptive semantics

The projection is explanatory only. DEGRADED, UNKNOWN, UNAVAILABLE and CONFLICTING are evidence descriptions, not safety or readiness decisions.

An incomplete, stale, unavailable, partial or conflicting evidence entry cannot be classified as COMPARABLE. The fixture therefore resolves to DEGRADED and explicitly states that a cross-domain aggregate is not authorized.

## 4. Offline fixture and validation

The bounded fixture is docs/data/bkl-036-f2-descriptive-health-fixture.json. It contains no live observations or credentials.

Validation is performed by:

- .github/scripts/verify-bkl-036-f2-evidence-envelope.mjs;
- .github/scripts/test-bkl-036-f2-evidence-envelope.mjs.

The negative suite verifies score promotion, missing mandatory domains, invalid comparability, runtime acceptance and operational-key injection are rejected.

## 5. Explicit exclusions

F2 does not implement:

- a numeric or banded health score;
- weights, thresholds, ranking or readiness;
- live telemetry transport or consumers;
- EAGLE/CloudWatcher runtime access;
- scheduling, remediation or device commands;
- a change to local physical interlocks or Safety Authority.

## 6. Future evolution

A future score-policy gate must cite ADR-015 and ADR-016, resolve all UNKNOWN, PARTIAL and CONFLICTING evidence, define comparability and authority, and receive independent ARB and Release Quality review.
