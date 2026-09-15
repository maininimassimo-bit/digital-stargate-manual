# BKL-031 F3 — Governed Site/Setup and Ephemeris/Lunar Validation Plan

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-VAL-001 |
| Status | **ACCEPTED AS VALIDATION PLAN — NOT EXECUTED** |
| Version | 1.1 |
| Date | 2026-09-14 |
| Contract under validation | `docs/architecture/scientific-assets/BKL-031-F3-Governed-Site-Setup-and-Ephemeris-Lunar-Solution-Architecture.md` |
| Baseline | `main` @ `2ffc77917bcd3fc25a3c5657e8f12e62c9284303` |
| Architecture acceptance | PR #191 merge `3a79bb93c9a0925280eba5214d517107804cb13c` |
| Open conditions | `ARB-191-MI01`, `ARB-191-MI02` |
| Runtime impact | None |
| Safety impact | None |

## 1. Objective

Define the evidence required to accept a future F3 architecture and implementation while preserving the accepted F2 fail-closed contract. This document does not provide test results and does not authorize schemas, fixtures, validators, adapters, dependencies, external calls or runtime execution.

## 2. Gate model

| Gate | Scope | Design-package expectation | Future implementation expectation |
|---|---|---|---|
| V1 Traceability | F1/F2/handoff/AP-006/DSDM-002 links | complete | unchanged |
| V2 Authority | site/setup source ownership and validity | contract defined | approved records resolve |
| V3 Time/coordinates | UTC/IANA/frame/epoch/datum/refraction | semantics defined | conformance demonstrated |
| V4 Method/data | adapter, provider/kernel and versions | neutral contract | ADR-selected and pinned |
| V5 Scientific validity | error budget and independent reference | method defined, values open | tolerance passes |
| V6 Failure behavior | missing/conflict/stale/coverage/network/cache | cases defined | all cases pass |
| V7 Privacy/security | coordinate/locator/credential sanitization | boundary defined | leak tests pass |
| V8 Compatibility | F2 states and prohibited fields | preserved | F2 regression passes |
| V9 Operability | placement, audit, cache and rollback | design defined | OAT/rollback evidence |
| V10 Documentation/CI | MkDocs, links, projections and workflows | exact-head success | exact-head and post-merge success |

## 3. Test-data policy

- Real site coordinates and protected locators are never committed to public/browser fixtures.
- Synthetic fixtures must carry `environment=TEST`, `authority=NONE` and unmistakable non-production identifiers.
- Synthetic data demonstrates validator behavior only and never closes S08/S09/S10 production authority.
- Real source acceptance uses protected evidence plus a sanitized pass/fail report, digests and approval references.
- Historical session/configuration data may support regression tests but cannot act as current setup authority.
- Golden astronomical vectors must record generator/reference, version, time scale, frame, site class, target identity, date range and digest.
- No value is accepted merely because two libraries agree; the approved error budget and independent reference remain mandatory.

## 4. Positive contract cases

| ID | Case | Expected result |
|---|---|---|
| P01 | exactly one approved interval-valid site record | S08 available internally; public projection sanitized |
| P02 | exactly one approved active setup assignment | S09 available with exact assignment/baseline lineage |
| P03 | valid site plus missing setup | geometry may be available; setup remains `UNAVAILABLE_CURRENT` |
| P04 | selected local method with pinned data in coverage | normalized S10 evidence with complete lineage |
| P05 | selected remote method with valid typed response | normalized evidence with request/response digest |
| P06 | identical normalized request repeated | identical normalized output within accepted deterministic tolerance |
| P07 | UTC instant displayed across DST using IANA zone | same UTC calculation; unambiguous local display metadata |
| P08 | target/Moon facts at same instant | separation and lunar facts share input digest and method |
| P09 | immutable kernel/cache hit | digest and coverage match; result reproducible |
| P10 | public projection publication | no protected coordinates, credentials, hosts or raw paths |

## 5. Mandatory negative cases

### 5.1 Site authority

| ID | Mutation/failure | Expected result |
|---|---|---|
| N21 | missing `siteRecordId` or `observatoryId` | S08 invalid; geometry not calculated |
| N22 | latitude outside [-90, 90] or non-finite | validation failure |
| N23 | longitude outside [-180, 180] or non-finite | validation failure |
| N24 | fixed offset/display label used instead of valid IANA zone | validation failure |
| N25 | zero current site records | S08 `UNAVAILABLE` |
| N26 | overlapping approved site intervals | S08 `CONFLICTED` |
| N27 | approval reference or authority missing | record not current |
| N28 | site digest does not resolve | record rejected |
| N29 | exact coordinates appear in public/browser artifact | publication fails closed |

### 5.2 Setup authority

| ID | Mutation/failure | Expected result |
|---|---|---|
| N30 | no active assignment at evaluation instant | S09 `UNAVAILABLE_CURRENT` |
| N31 | unknown `configurationId` or missing baseline | assignment rejected |
| N32 | assignment outside effective interval | not current |
| N33 | overlapping active assignments | S09 `CONFLICTED` |
| N34 | explicit conflicted assignment state | no setup-specific claim |
| N35 | latest historical session is promoted to current | validation failure |
| N36 | derived configuration summary overrides authority | validation failure |
| N37 | observed configuration differs from desired baseline | preserve drift/conflict; no silent reconciliation |
| N38 | assignment digest or approval reference missing | assignment rejected |

### 5.3 Time, coordinates and method

| ID | Mutation/failure | Expected result |
|---|---|---|
| N39 | target frame or epoch absent | celestial/lunar evidence non-available |
| N40 | invalid/ambiguous local civil time without resolved UTC | request rejected |
| N41 | method, adapter or data version absent | S10 `UNAVAILABLE` |
| N42 | input time outside kernel/service coverage | S10 `UNAVAILABLE`; no extrapolation |
| N43 | required EOP/leap-second data missing or unqualified | affected evidence non-available |
| N44 | input/calculation time scale mismatch | validation failure |
| N45 | output frame/refraction mode missing | result rejected |
| N46 | cache input, method or data digest mismatch | cache entry rejected |
| N47 | cached result outside declared validity | `STALE` or `UNAVAILABLE` |
| N48 | remote timeout, DNS/TLS error, throttling or 5xx | `UNAVAILABLE`; no silent fallback |
| N49 | malformed/truncated provider response | result rejected |
| N50 | NaN/infinite/out-of-range normalized fact | affected evidence rejected |
| N51 | target and Moon facts use different instants/site/method | separation result rejected |
| N52 | phase convention differs from contract | result rejected |
| N53 | precision profile or error-budget reference absent | facts cannot be `AVAILABLE` |
| N54 | requested grid exceeds approved bounds | request rejected before calculation |

### 5.4 Capability and Safety boundaries

| ID | Mutation/failure | Expected result |
|---|---|---|
| N55 | forecast/provider-run fields introduced | fail; belongs to F4 |
| N56 | weight, score, threshold or target order introduced | fail; belongs to F5 |
| N57 | readiness, go/no-go or `safe` conclusion introduced | fail; belongs to BKL-032/Safety |
| N58 | scheduler or device-command field introduced | fail |
| N59 | software projection claims Safety Authority | fail |
| N60 | calculation/external call placed on EAGLE | architecture validation failure |
| N61 | browser calls provider with exact site coordinates | security validation failure |
| N62 | credential, local host, UNC path, serial or raw locator published | security validation failure |
| N63 | last-known-good promoted after source failure | fail; retain non-current state |
| N64 | unavailable/conflicted fact contains a value | fail per F2 |
| N65 | Citation/Provenance or source locator is dropped | fail |
| N66 | F2 prohibited vocabulary becomes accepted | F2 regression failure |

## 6. Scientific validation campaign

The future selected method must be compared with an independent reference over a versioned grid that includes:

- representative accepted BKL-035 targets across declination;
- instants near rise/set, meridian transit and the requested-night boundaries;
- dates around daylight-saving transitions for display validation;
- lunar phases and target–Moon separations across the supported range;
- supported-date boundaries and one out-of-coverage case;
- airless/topocentric transformations and any separately approved refracted semantic.

The campaign records for every vector:

- target identity and governed coordinate citation;
- protected site-record digest, not public coordinates;
- UTC instant and internal time scales;
- frame, epoch, datum and refraction mode;
- primary and independent method/data versions;
- normalized result and absolute/directional differences;
- accepted numeric tolerance from the approved ADR/error budget;
- pass/fail and evidence digest.

No numeric tolerance is invented by this plan. Until the ADR defines and the campaign passes the error budget, S10 remains `UNAVAILABLE` for production evidence.

## 7. Determinism and cache tests

- repeat the same request in the same process and a clean process;
- repeat after cache warm-up;
- verify output digest across supported host environments;
- corrupt each source/method/data digest independently;
- replace a cached payload while preserving its key;
- test concurrent requests for the same content-addressed entry;
- test atomic publication interruption and retry;
- prove that a failed refresh does not relabel the previous response as current.

## 8. Privacy, security and supply-chain tests

- scan public artifacts for coordinate pairs, protected locators, hosts, paths, serials and credentials;
- verify that logs/events contain only approved IDs, digests and reason codes;
- inspect external request minimization and TLS requirements;
- record package/license notices and data/kernel provenance;
- verify pinned dependency and artifact checksums;
- execute malformed/untrusted provider-response tests;
- verify bounds against resource exhaustion and oversized requests;
- document vulnerability review and rollback of a selected dependency.

## 9. Migration and rollback evidence

| Slice | Required precondition | Acceptance evidence | Rollback proof |
|---|---|---|---|
| F3-A1 site authority | owner approves values/classification/storage | one valid protected record plus sanitized evidence | deactivate record; S08 unavailable |
| F3-A2 setup authority | AP-006 baseline and interval approved | one resolvable non-overlapping assignment | retire assignment; S09 unavailable-current |
| F3-A3 ADR/method | alternatives, licenses, privacy and error budget reviewed | accepted ADR and scientific campaign | reject adapter; S10 unavailable |
| F3-B contracts | separate implementation authorization | schema/fixture/validator and all contract tests | restore accepted F2 artifacts |
| F3-C integration | prior slices accepted | adapter, projection, CI and bounded OAT | disable publication; restore F2 missingness |

Rollback must preserve audit evidence and must not alter F4/F5/BKL-032 or local Safety behavior.

## 10. CI and validation evidence requirements

For the architecture-package PR:

- changed-file review proves documentation/governance-only scope;
- MkDocs strict build and link validation;
- Mermaid rendering/parse where applicable;
- canonical roadmap/generated projection consistency;
- Developer Foundation and all applicable governance workflows;
- exact-head run IDs recorded before review.

For future implementation:

- F2 normative fixture and 37-test regression remain green;
- all P01–P10 and N21–N66 cases execute;
- scientific campaign and deterministic digest tests pass;
- privacy/supply-chain checks pass;
- resource placement proves no execution on EAGLE;
- runtime/OAT is bounded, read-only and separately authorized;
- exact-head and post-merge workflows are successful.

## 11. Evidence classification

| Evidence | Current status |
|---|---|
| F1/F2 accepted contract and tests | VERIFIED predecessor evidence |
| repository source inventory | VERIFIED on baseline |
| official alternative documentation | REVIEWED for architecture comparison |
| F3 architecture document | ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED — NOT IMPLEMENTED |
| site/setup production authority | NOT MATERIALIZED |
| provider/library ADR | NOT EXECUTED |
| schema/fixture/validator | NOT IMPLEMENTED |
| scientific accuracy campaign | NOT EXECUTED |
| security/privacy runtime test | NOT EXECUTED |
| PC Principale/EAGLE OAT | NOT APPLICABLE to design; NOT AUTHORIZED for implementation |

## 12. Architecture acceptance evidence and current implementation rule

The architecture-package gate was satisfied through separately authorized ARB/Release Quality reviews, successful review-publication CI, PR #191 merge and 9/9 post-merge workflows.

F3 implementation cannot be recommended until:

1. open decisions F3-OD01–F3-OD10 applicable to the slice are closed;
2. provider/library and precision choices are accepted through an ADR;
3. source authority records are approved;
4. schemas/tests and scientific validation pass;
5. privacy, rollback and off-EAGLE placement are evidenced;
6. separate implementation, review and merge authorizations are granted.

## 13. Explicit non-evidence

This plan is not evidence that:

- the real site/setup records exist or are correct;
- any candidate provider/library is approved;
- ephemeris/lunar calculations are scientifically valid;
- a schema, fixture, validator, adapter or portal consumer exists;
- the capability is production-ready;
- the planner can rank, recommend, schedule or declare readiness/safety.

## 14. Current governance stop after plan acceptance

The architecture and this validation plan are accepted with conditions; their reviews and PR #191 merge are complete. Stop before remediation of implementation conditions, ADR/provider selection, authority records, schema/fixture/validator/adapter work, P01–P10/N21–N66 execution, scientific validation and every runtime activity unless separately authorized.


## 15. Acceptance and execution boundary

This document is accepted as the normative validation plan for future F3 slices. Its acceptance is not evidence that P01–P10, N21–N66, the scientific campaign, privacy tests or runtime/OAT have executed.

`ARB-191-MI01` adds a mandatory public-reference non-correlation test. `ARB-191-MI02` adds explicit half-open interval boundary and adjacency cases. These conditions must be materialized in the applicable future schema/test increment before implementation acceptance.


## 16. Current-state reconciliation — 2026-09-15

The original evidence classification captured the PR #191 baseline. Later F3-A1/F3-A2 increments materialized and approved repository authority with their own dedicated schemas, validators and evidence suites. Those results do not imply runtime availability and do not count as execution of this plan's P01–P10/N21–N66 campaign.

Current classification:

- F3-A1/F3-A2 repository authority: VERIFIED by later acceptance records;
- runtime S08/S09: `UNAVAILABLE` / `UNAVAILABLE_CURRENT`;
- F3-A3 provider/library ADR: proposed as ADR-010; decision pending;
- F3-A3 spike: governed by `docs/architecture/validation/BKL-031-F3-A3-Ephemeris-Lunar-Method-Validation-Spike-Plan.md`; NOT EXECUTED;
- S10: `UNAVAILABLE`;
- F3-B/F3-C and runtime/OAT: not authorized.

The original P01–P10/N21–N66 plan remains normative for later full F3 validation where applicable.
