# BKL-031 F4-B — Forecast Machine-Readable Contracts, Fixture and Validator

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-B-CONTRACTS-001` |
| Status | **ACCEPTED — POST-MERGE VERIFIED / ZERO PROVIDER TRAFFIC** |
| Date | 2026-09-17 |
| Decision authority | Accepted ADR-011 |
| Fixture | `BKL031-F4B-FIXTURE-001` |
| Contract digest | `a96a8268c571c2fc7fbe715cce8183ecc3ee02d45cbea91aaaa1a46506533d48` |
| Environment / authority | `TEST / NONE` |
| Runtime and Safety effect | None |

## Implemented contract

F4-B materializes the accepted F4-A decision as three closed JSON Schemas: forecast source profile, request and normalized evidence. A deterministic validator enforces exact provider, upstream authority, model and run lineage; the 00/12 UTC cadence; the 72-hour horizon; the 18-hour run-age ceiling; one generalized location; GMT/ISO-8601/land-cell/NaN-elevation request policy; the exact eleven-variable vocabulary and units; ordered hourly instants; returned-grid applicability; Citation, Provenance, terms and attribution; and TEST/NONE authority boundaries.

The bounded fixture contains four synthetic hourly instants for a clearly labelled generalized Italian-domain point. Its raw-response digest is a synthetic marker digest, not a fabricated provider response. The source profile sets `DENY_F4B`, zero requests and an empty host allow-list. Validation therefore performs no DNS lookup or network call.

## Validation result

The suite passes two positive/determinism checks and **24/24 negative cases** mapped one-to-one to F4-A N01–N24. It rejects missing or implicit lineage, best-match/seamless substitution, invalid run cadence or age, horizon and timezone drift, multiple locations/models/runs, unknown variables, outbound elevation, acquisition enablement, provider errors, response lineage/spatial/unit/temporal/value defects, missing Citation/Provenance/digests, observation substitution, run mixing, public-coordinate projection, ranking/readiness/command claims, terms drift and unauthorized production use.

## Authority boundary

F4-B authorizes only repository schemas, a synthetic fixture and deterministic validation. Provider calls remain zero. Protected-site coordinates, production subscriptions, runtime S10, public forecast projection, ranking, readiness, scheduling, commands and Safety Authority remain unavailable.

F4-C is the next independent gate. It must first define and pass an exact network/privacy authorization for one bounded synthetic/generalized acquisition; F4-B acceptance does not grant that authorization.
