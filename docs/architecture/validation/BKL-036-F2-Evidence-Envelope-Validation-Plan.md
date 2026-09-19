# BKL-036-F2 — Evidence Envelope Validation Plan

| Field | Value |
|---|---|
| Identifier | BKL-036-F2-VAL-001 |
| Status | Accepted / Post-Merge Verified |
| Version | 0.1 |
| Date | 2026-09-19 |
| Runtime traffic | None authorized |
| Safety Authority | Local physical interlocks only |

## Scope

Validate the versioned BKL-036-F2 evidence envelope and its descriptive, read-only projection using only a synthetic offline fixture.

## Acceptance criteria

- schema and contract identifiers are fixed and versioned;
- all seven mandatory domains are represented exactly once;
- F1 evidence statuses and compatibility classifications are preserved;
- incomplete evidence cannot be marked COMPARABLE;
- projection authority is projection and action authority is NONE;
- descriptive status includes reasons and never exposes a score;
- privacy classification is mandatory;
- negative tests reject missingness, invalid comparability, runtime acceptance and operational-key injection;
- no live telemetry, EAGLE, CloudWatcher, transport or command path is used.

## Validation commands

    node .github/scripts/verify-bkl-036-f2-evidence-envelope.mjs
    node --test .github/scripts/test-bkl-036-f2-evidence-envelope.mjs

## Open issues

- freshness retention remains source-specific and is not generalized by this contract;
- cross-domain comparability remains unresolved for any aggregate score;
- the next score-policy gate requires a separate decision and authority review.
