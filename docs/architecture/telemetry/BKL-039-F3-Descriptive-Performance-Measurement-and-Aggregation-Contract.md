# BKL-039 F3 — Descriptive Performance Measurement and Aggregation Contract

| Field | Value |
|---|---|
| Identifier | `BKL-039-F3` |
| Capability | BKL-039 — Equipment Performance Registry |
| Status | In Progress |
| Date | 2026-09-09 |
| Base | F2-A merge `96e0e7197d1b729b5ae0b2e0cec402b81baac17f` |
| Runtime impact | None — repository/analytics only |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Entry condition

BKL-039 F2-A is repository-integrated and post-merge green on merge SHA `96e0e7197d1b729b5ae0b2e0cec402b81baac17f`.

Verified post-merge workflows:

- BKL-039 F2 Governance #16 — SUCCESS;
- Genera manuale Word #1180 — SUCCESS;
- Deploy MkDocs artifact to GitHub Pages #723 — SUCCESS;
- Validate documentation #755 — SUCCESS;
- Developer Foundation #1136 — SUCCESS.

Therefore F2-A is accepted as the machine-readable identity/session-usage foundation for F3.

## 2. Objective

F3 introduces deterministic, source-backed **descriptive performance measurements and statistics** for equipment/configuration history.

F3 is not a health-scoring, ranking, anomaly, prediction or maintenance-policy increment. It may only compute quantities whose source values, unit, population and method are explicitly repository-resolvable.

## 3. Source discovery — accepted quantitative candidates

Repository search confirms an existing governed warehouse quality model and implementation capable of materializing historical image-quality statistics including:

- `image_count`;
- `average_fwhm`;
- `minimum_fwhm`;
- `maximum_fwhm`;
- `fwhm_stddev`;
- `average_camera_temperature_c`;
- `integration_hours`;
- first/last timestamps.

The current warehouse implementation computes FWHM statistics deterministically from source-backed FWHM values, including arithmetic mean, min/max and sample standard deviation. Existing tests verify deterministic known-answer behavior.

The repository also contains historical session/image evidence with FWHM embedded in source N.I.N.A. filenames and a session importer that extracts FWHM from those filenames.

These facts make **FWHM-based descriptive image-quality measurements** the preferred first bounded F3 metric family.

## 4. Initial bounded F3 scope

The first F3 executable slice should be limited to metrics that can be bound to the accepted F2-A configuration/session identities and to repository-resolvable source image records.

### 4.1 Authorized semantic types

F3 may add:

- `PERFORMANCE_MEASUREMENT`;
- `DESCRIPTIVE_PERFORMANCE_STATISTIC`.

F3 must preserve existing F2-A:

- `EQUIPMENT_IDENTITY`;
- `EQUIPMENT_USAGE_OBSERVATION`.

F3 must not add:

- `PERFORMANCE_ASSESSMENT`;
- `RECOMMENDATION`.

### 4.2 Preferred first metric family — FWHM

The bounded implementation should initially expose only FWHM-derived descriptive records when all source conditions are met.

Permitted examples:

- per-session/configuration mean FWHM;
- minimum FWHM;
- maximum FWHM;
- sample standard deviation;
- source image count used by the aggregation.

No numeric value may be interpreted as GOOD/BAD, healthy/degraded, acceptable/unacceptable, nominal/outlier or failure evidence.

## 5. Unit contract

FWHM values must retain the unit used by the accepted source model. F3 must not silently convert or assume arcseconds when the source evidence only provides a numeric FWHM value without an explicit angular calibration contract.

The machine-readable record must therefore carry an explicit `unit` field. If the source unit cannot be proven from accepted repository evidence, use an explicit governed source-unit label rather than inventing a physical unit.

Cross-unit aggregation must fail closed unless a separate normalization rule is governed.

## 6. Method contract

Every derived descriptive statistic must carry a versioned `method_id`.

Initial candidate method semantics may reuse the already implemented warehouse logic only after its exact source population and unit contract are bound to the F2-A session/configuration fixture.

For example, a future method identifier may represent:

- arithmetic mean over source-backed FWHM values;
- minimum/maximum over the same declared population;
- sample standard deviation using the already tested implementation.

The method identifier must be versioned and deterministic. F3 must not rely on an unversioned display label as provenance.

## 7. Population and sample semantics

Every statistic must declare:

- `configuration_id`;
- `session_id` or explicit analysis window;
- source population selector;
- `sample_count`;
- source record references;
- method/version;
- unit;
- quality/coverage;
- Citation references;
- Provenance references.

`sample_count=0` is not a valid statistic. Missing source images or unresolved source values must produce no statistic or an explicit unavailable/insufficient state, never a fabricated zero.

## 8. Quality and coverage rules

F3 must distinguish at least:

- `COMPLETE_FOR_DECLARED_POPULATION`;
- `PARTIAL_FOR_DECLARED_POPULATION`;
- `UNKNOWN_COVERAGE`;
- `INSUFFICIENT_SAMPLE`.

These are evidence/coverage states only. They are not equipment-health states.

A statistic computed from a partial population must preserve that partial quality and must not be promoted to complete.

## 9. Comparability boundary

F3 may aggregate within one declared equipment configuration and one compatible method/unit population.

F3 must not perform cross-configuration ranking in this increment.

Comparison across configurations requires separate proof that the measurement semantics, source extraction, units, population and environmental context are comparable. Different optics, cameras, binning, filters, focal scales or acquisition conditions must not be normalized implicitly.

## 10. Environmental context boundary

Temperature, SQM, guiding RMS, seeing or weather may be referenced as contextual evidence only if repository-resolvable and session-aligned.

F3 must not claim that environmental correlation establishes equipment causation.

The first executable slice should prefer a single metric family rather than combine multiple contexts prematurely.

## 11. FWHM interpretation boundary

FWHM is treated only as a historical descriptive image-quality measurement.

F3 must not infer:

- optical health;
- focus quality state;
- collimation state;
- seeing quality;
- mount performance;
- camera performance;
- threshold breach;
- anomaly;
- failure prediction;
- maintenance recommendation.

Any such interpretation requires separate governed methods and evidence.

## 12. Authority and Safety

All F3 derived records remain:

- `authority=projection`;
- `action_authority=NONE`;
- historical/read-only.

F3 introduces no device commands, service restart, focusing action, cooling adjustment, mount action, USB/power/network remediation, scheduler action or current-time Safety inference.

Local physical interlocks remain independent and authoritative.

## 13. Candidate executable artifact set

The next implementation step should produce:

1. F3 extension to the machine-readable Equipment Performance Registry schema;
2. bounded F3 fixture derived from repository-resolvable FWHM source records for one or more accepted F2-A sessions/configurations;
3. deterministic generator/aggregator with versioned method identifiers;
4. fail-closed validator;
5. negative regression suite covering missing unit, missing method, zero/incorrect sample count, unresolved source record, unexpected property and forbidden assessment/ranking fields;
6. dedicated F3 Governance workflow or extension of the F2 workflow with explicit F3 gates;
7. Developer Foundation integration;
8. independent ARB and Release Quality before merge.

## 14. Acceptance criteria

F3 is reviewable only when:

- every emitted measurement/statistic resolves to accepted F2-A configuration/session identity;
- every source value resolves to repository evidence;
- unit semantics are explicit and non-invented;
- aggregation method is deterministic and versioned;
- sample population/count is explicit and validated;
- partial/unknown coverage fails closed or remains explicit;
- Citation/Provenance are non-empty and repository-resolvable;
- no performance assessment, threshold, ranking, anomaly, prediction or recommendation is introduced;
- runtime and Safety Authority remain unchanged;
- exact-head governance/documentation/build gates are green;
- independent ARB approves the executable F3 slice.

## 15. Open items before implementation

1. Identify the smallest repository-resolvable FWHM source population that maps cleanly to one accepted F2-A session/configuration.
2. Confirm the exact unit semantics of the FWHM values produced by the existing warehouse/import path; do not assume arcseconds without evidence.
3. Decide whether the existing warehouse quality dataset should be referenced directly or projected into a new BKL-039 F3 generated artifact.
4. Define the versioned F3 method identifiers only after the exact source population and calculation semantics are locked.

## 16. Decision summary

BKL-039 F3 will begin with **descriptive, deterministic FWHM history**, not with equipment scoring. The architecture deliberately minimizes scope to source-backed quantities whose identity, unit, method, population and lineage can be proven from the repository.