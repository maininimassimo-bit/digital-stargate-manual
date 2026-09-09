# BKL-039 F1 — Equipment Performance Registry Source Discovery and Semantic Contract

| Field | Value |
|---|---|
| Identifier | `BKL-039-F1` |
| Capability | BKL-039 — Equipment Performance Registry |
| Status | In Progress |
| Version | 0.1 |
| Date | 2026-09-09 |
| Base | BKL-038 closure merge `a23d758a72046b7c5c414ed84e7bbc71d9b0d1e7` |
| Runtime impact | None — repository/architecture only |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Objective

BKL-039 establishes a governed historical Equipment Performance Registry for observatory equipment and instrument configurations. F1 defines source authority, identity, semantic types, evidence lineage, quality/freshness handling and the boundaries that later executable increments must preserve.

The planning authority describes BKL-039 as historical performance for OTA/camera/filter/focuser/mount with statistics and correlation to SQM and environmental conditions. F1 does not invent performance ratings, thresholds, health bands or remediation policy.

## 2. Governing repository sources discovered

### 2.1 Instrument identity and configuration authority

`docs/architecture/scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model.md` defines stable logical identities for Telescope, Camera, Mount, Focuser, FilterWheel, Filter and versioned `InstrumentConfiguration`. Observation sessions reference an `instrumentConfigurationId`; scientifically significant configuration changes create a new configuration version instead of rewriting historical sessions.

This model is the preferred semantic foundation for BKL-039 equipment/configuration identity. BKL-039 must not create competing equipment identifiers when an accepted repository identity exists.

### 2.2 Session and scientific-history evidence

Accepted scientific/session repository evidence may contribute observations such as session usage, acquisition metadata and quality measurements only when the specific record is repository-resolvable and its provenance is preserved.

BKL-039 must distinguish:

- equipment identity/configuration metadata;
- observed session facts;
- derived descriptive statistics;
- performance assessment/rating;
- recommendation/remediation.

Only the first three are in scope for the bounded foundation unless later governance explicitly authorizes assessment policy.

### 2.3 BKL-015 / BKL-044 lineage foundation

Stable Citation/Provenance and repository evidence semantics from the accepted Knowledge Graph / AI Evidence Contract remain mandatory for registry records and derived statistics.

### 2.4 BKL-038 analytical foundation

BKL-038 provides accepted deterministic historical analytical semantics and strict separation among observation, trend, anomaly candidate, correlation candidate and recommendation. BKL-039 may reuse these lineage/quality principles but must not reinterpret BKL-038 descriptive trends as equipment-performance scores.

### 2.5 Environmental context

SQM, weather and other environmental values may be correlated only when repository-resolvable session-aligned evidence exists with timestamp/quality/provenance. Environmental context is explanatory evidence, not an equipment property and not Safety Authority.

### 2.6 Historical/non-authoritative prototype code

Repository search found historical `.bak` analytics files containing fields such as `equipment_id`, `session_count` and `usage_hours`. Backup/prototype files are not authoritative BKL-039 contracts and must not be treated as implementation evidence. They may be inspected only as historical design input after reconciliation with current accepted models.

## 3. Semantic types

F1 defines the following semantic categories.

### 3.1 `EQUIPMENT_IDENTITY`

Stable reference to a governed equipment entity or versioned instrument configuration. It describes what equipment/configuration is being referenced; it is not a performance result.

### 3.2 `EQUIPMENT_USAGE_OBSERVATION`

A source-backed historical fact linking equipment/configuration to a session or observation window. Examples may include session participation, exposure duration or number of source records only when directly evidenced.

### 3.3 `PERFORMANCE_MEASUREMENT`

A quantitative historical measurement with explicit unit, source/evidence, analysis window and method. Examples are allowed only when directly measured or deterministically derived from accepted evidence.

A measurement is not automatically a rating, health state, anomaly or recommendation.

### 3.4 `DESCRIPTIVE_PERFORMANCE_STATISTIC`

A deterministic aggregation of homogeneous accepted measurements over a declared equipment/configuration and time/session set. It must declare aggregation method, population, sample count, unit, quality/coverage and evidence lineage.

### 3.5 `PERFORMANCE_ASSESSMENT`

A qualitative or scored interpretation such as GOOD/BAD, HEALTHY/DEGRADED, percentile band, threshold breach or ranking. **Not authorized in F1** unless a later architecture decision defines governed policy, baseline population and validation evidence.

### 3.6 `RECOMMENDATION`

Maintenance, configuration or operational advice derived from performance evidence. **Not authorized in the bounded foundation** and must never imply command/remediation authority.

## 4. Equipment/configuration identity rules

1. Reuse accepted repository equipment identifiers where available.
2. Prefer `InstrumentConfiguration` as the session-level configuration key because historical sessions must remain bound to the exact configuration version used at acquisition time.
3. Do not collapse physically different devices that share the same manufacturer/model.
4. Do not merge configuration versions retroactively.
5. A display label is never sufficient as a stable identity key.
6. Missing equipment identity is explicit `UNKNOWN`/unresolved; do not infer a device from a metric value alone.

## 5. Source authority and provenance contract

Every BKL-039 observation/measurement/statistic must preserve or resolve:

- stable source record reference(s);
- equipment/configuration reference;
- session and/or analysis window where applicable;
- observed or derived timestamp semantics;
- source system/component;
- method identifier and version for derived records;
- unit and measurement semantics;
- quality/coverage state;
- non-empty Citation references;
- non-empty Provenance references;
- `authority=projection` for registry-derived records;
- `action_authority=NONE`.

Unresolvable source identity, missing required lineage or incompatible units must fail closed in later executable increments.

## 6. Quality and unknown semantics

BKL-039 must not rewrite stale/partial/unknown evidence as current or complete.

At minimum later schemas must distinguish:

- source quality known and acceptable for the historical observation;
- stale/partial historical evidence;
- unknown/unavailable evidence;
- insufficient sample/coverage for aggregation.

`0`, empty string and fabricated default values must not represent unknown data.

## 7. Measurement comparability rules

Measurements may be aggregated or compared only when their semantic contract is compatible. At minimum the registry must consider:

- same equipment/configuration identity or explicitly governed comparison class;
- same measurement semantic type;
- compatible units;
- compatible acquisition/derivation method and version, or an explicit normalization rule;
- known time/session population;
- declared environmental/context dimensions when they materially affect interpretation.

F1 does not define normalization coefficients, weights, thresholds or cross-equipment ranking.

## 8. Environmental correlation boundary

SQM, temperature, humidity, seeing/FWHM, guiding or other contextual factors may be linked as evidence dimensions where repository-resolvable.

Correlation is descriptive. It does not establish equipment causation. A degraded measurement observed under poor environmental conditions cannot be assigned automatically to equipment failure.

## 9. Safety and operational boundary

BKL-039 is historical/read-only.

It must not:

- issue device commands;
- change camera cooling, focus, mount, filter wheel, USB, power or network state;
- restart services;
- schedule maintenance automatically;
- define or override local Safety state;
- bypass physical interlocks;
- convert historical performance into present-time Safety Authority.

Local physical interlocks remain independent and authoritative.

## 10. Candidate source families for later bounded onboarding

The following are candidate families, not claims of implementation:

| Source family | Potential use | F1 disposition |
|---|---|---|
| DSDM equipment/configuration model | Stable equipment/configuration identity | Accepted semantic foundation |
| Observation/session records | Equipment usage and session population | Eligible when repository-resolvable |
| Acquisition/frame metadata | Quantitative source observations | Eligible when lineage/units are explicit |
| Session quality measurements | Historical descriptive measurements | Eligible when semantic method is governed |
| SQM/weather evidence | Environmental context | Eligible as context, not equipment authority |
| BKL-038 derived records | Historical descriptive analytical context | Eligible only without promoting trends to ratings |
| BKL-030 EAGLE history | Computer-health context | Deferred unless bounded repository-resolvable evidence exists |
| `.bak` analytics prototypes | Historical design input | Non-authoritative; excluded from executable evidence |

## 11. Initial bounded implementation strategy

BKL-039 should advance incrementally:

1. **F1 — Source Discovery & Semantic Contract**: current document; establish identity, authority, semantic types and boundaries.
2. **F2 — Machine-Readable Registry Contract & Bounded Fixture**: schema plus a small repository-resolvable equipment/configuration/session fixture; no ratings or thresholds.
3. **F3 — Deterministic Descriptive Aggregation Engine**: source-backed measurements and descriptive statistics with explicit units/sample counts/coverage and fail-closed rules.
4. **F4 — Read-Only Consumer / Registry Projection**: equipment/configuration history with drill-down to source/Citation/Provenance and explicit limitations.
5. **Closure**: only after independent ARB, Release Quality, exact-head CI, merge and post-merge validation.

Any assessment/ranking/predictive-maintenance extension requires separate governance and may not be smuggled into F2/F3/F4.

## 12. Acceptance criteria for F1

F1 is reviewable when:

- repository equipment/configuration identity authority is identified;
- source families are classified as accepted, eligible, deferred or non-authoritative;
- semantic distinctions among identity, usage observation, measurement, statistic, assessment and recommendation are explicit;
- Citation/Provenance and quality/unknown requirements are defined;
- measurement comparability and environmental-correlation boundaries are explicit;
- no rating/threshold/severity/remediation policy is introduced;
- BKL-030/EAGLE history is not fabricated;
- runtime and Safety Authority remain unchanged;
- exact-head documentation/build/governance gates pass;
- independent ARB approval is obtained before F2 begins.

## 13. Open items

1. Identify the smallest accepted repository fixture that binds one or more `InstrumentConfiguration` identities to repository-resolvable session evidence without fabricating missing hardware identity.
2. Determine which existing quality/measurement records are sufficiently governed for F2 inclusion.
3. Determine whether a dedicated equipment identity read model is required or whether existing DSDM identifiers can be referenced directly.
4. Reconcile any useful historical analytics prototype concepts only after source authority and semantic compatibility are proven.

## 14. Decision summary

BKL-039 starts as an **evidence-first Equipment Performance Registry**, not as a scoring engine. The first accepted baseline must preserve stable equipment/configuration identity, historical source lineage, measurement semantics, units, quality and explicit unknowns. Performance interpretation, ranking, health policy, prediction and remediation remain outside the bounded foundation until separately governed.