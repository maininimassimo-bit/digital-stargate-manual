# BKL-031 F3-B — Ephemeris/Lunar Machine-Readable Contracts and Validator

| Field | Value |
|---|---|
| Identifier | `BKL-031-F3-B-CONTRACT-001` |
| Status | **IMPLEMENTED — ACCEPTANCE REVIEW PENDING** |
| Date | 2026-09-17 |
| Predecessor | F3-A3 accepted method profile and scientific campaign |
| Runtime effect | None |
| Safety effect | None |

## Scope

F3-B materializes the source-neutral contract boundary described by the accepted F3 solution architecture. It provides separate JSON Schemas for `EphemerisLunarRequest`, `EphemerisLunarEvidence` and the accepted method profile, plus one bounded synthetic fixture and a deterministic fail-closed validator.

The increment is repository-only. It does not implement the F3-C adapter, resolve a protected site at runtime, execute a scientific calculation, call an external reference, activate S10, publish forecast evidence, rank targets, declare readiness, issue commands or assume Safety Authority.

## Governed artifacts

| Artifact | Purpose | Raw SHA-256 |
|---|---|---|
| `schemas/observation-planner-ephemeris-lunar-method-profile-f3b.schema.json` | source-neutral method/data/time/output/error-budget contract | `6720d501917ba5fec17b4536d923cfffefd2f4d1ddbe2b9fd443feaa10248419` |
| `schemas/observation-planner-ephemeris-lunar-request-f3b.schema.json` | bounded request, target, synthetic site snapshot and optional setup binding | `08cac6ae2877d85c1f9d33a52418086f032c7e88737807bbc332b7eaf3ee9f18` |
| `schemas/observation-planner-ephemeris-lunar-evidence-f3b.schema.json` | normalized facts, availability, method/data lineage, citations and provenance | `5d15a79ee19b68c02d98d9e53a0dcfdecf1fb6ebc44a7d44b5822b5d2f5134a2` |
| `docs/data/observation-planner-ephemeris-lunar-f3b-fixture.json` | bounded `TEST` / `authority=NONE` fixture | `e2d49122741275b086bbf2e25a5701f0403b4c36999e28847d79146ef26eaca9` |

The fixture carries the canonical contract digest `b06932edb860cc4062b45d75b62e7874c3a327a4b4dbfd0b8cb70bdf115cd1f1`. Its four evaluation instants and nine normalized facts use the pre-existing public synthetic site `SYNTHETIC-MID-LATITUDE-001` profile values. They are test data and establish no production authority.

## Contract invariants

The validator enforces:

- exact property sets and canonical SHA-256 identity for profile, request, evidence and fixture;
- exact binding to the accepted ADR-010 method-profile source bytes, `de442s.bsp` digest and IERS identity;
- explicit UTC input, calculation time scales, ICRS/J2000 target coordinates, WGS84 site semantics, topocentric AltAz output and airless refraction;
- at most eight strictly ordered instants, nine fact types and a 24-hour request span;
- half-open evidence validity and exact request/profile/method/data lineage;
- closed fact vocabulary with units and numeric ranges;
- `AVAILABLE` facts only with precision/error-budget references; non-available states carry reasons and no values;
- target/Moon separation only with co-temporal target and Moon facts;
- repository-relative resolvable citations and synthetic-validation provenance;
- a non-correlatable public site evidence reference and a public projection without protected coordinates, record identities or internal digests;
- zero F3-C/runtime/protected-site/external-reference activity and no forecast, ranking, readiness, command or software Safety authority.

Unknown properties, stale or mismatched digests, coverage violations, malformed facts and prohibited semantics fail closed. The validator does not repair input or select a fallback method.

## Executable evidence

The F3-B suite contains 34 tests. It covers deterministic identity, bounds, coordinates, timezone, coverage, availability/value exclusivity, method/data/time/frame semantics, half-open validity, fact ranges, co-temporal lunar evidence, citations/provenance, public-boundary leakage and authority separation.

The existing F3-A1 and F3-A2 authority validators remain responsible for their complete record lifecycle and overlap behavior. F3-B consumes only their normalized contract shape and does not duplicate or alter either authority store.

## Rollback

Rollback removes the three F3-B schemas, fixture, validator/test/workflow and their documentation references. The accepted F2 schema, fixture and validator remain unchanged. S08, S09 and S10 runtime states remain unavailable, so rollback requires no runtime or data migration.

## Successor gate

F3-C may be prepared only after exact-head review, merge and post-merge verification of this increment. F3-C must implement a bounded adapter and sanitized projection as a separate gate. Protected-site calculation, another cloud execution and runtime activation remain outside this package.
