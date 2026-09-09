# BKL-039 F4 — Equipment Performance Read-Only Consumer Contract

| Field | Value |
|---|---|
| Identifier | `BKL-039-F4` |
| Capability | BKL-039 — Equipment Performance Registry |
| Status | In Progress |
| Version | 0.1 |
| Date | 2026-09-09 |
| Base | F3 accepted merge `ce2482aa6b2da62296ebdc221f73f39c1acd3aa2` |
| Runtime impact | None — repository/static read model only |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Objective

F4 defines the final bounded consumer layer for BKL-039. It presents the accepted F2/F3 equipment-performance evidence through a deterministic, read-only registry projection suitable for portal/static consumption, while preserving source identity, method, units, quality, Citation and Provenance.

F4 is a consumer/read-model increment only. It does not create new measurements, reinterpret FWHM, calculate new performance scores, define thresholds, compare equipment, infer health, generate recommendations or issue commands.

## 2. Governing upstream inputs

F4 consumes only accepted repository-integrated BKL-039 inputs:

- F2 bounded registry fixture and configuration/session identity binding;
- F3 `PERFORMANCE_MEASUREMENT` records;
- F3 `DESCRIPTIVE_PERFORMANCE_STATISTIC` records;
- F3 source/Citation/Provenance lineage;
- F1 semantic and Safety boundaries.

The accepted F3 merge SHA is `ce2482aa6b2da62296ebdc221f73f39c1acd3aa2`.

## 3. Consumer responsibilities

The F4 consumer read model may:

1. group records by `configuration_id` and bounded session;
2. expose human-readable configuration/session/target/filter labels already present in accepted inputs;
3. expose individual source-backed measurements;
4. expose accepted descriptive statistics;
5. preserve unit and calibration semantics exactly;
6. expose source record references, Citation and Provenance for drill-down;
7. expose quality/coverage and method identifiers;
8. render explicit limitations and non-authoritative semantics.

The consumer must not silently transform, normalize or reinterpret upstream values.

## 4. Required read-model semantics

The machine-readable F4 projection must include, at minimum:

- `schema_version`;
- `component`;
- `authority=projection`;
- `action_authority=NONE`;
- source F3 artifact reference;
- `configuration_id`;
- session identity;
- target/filter/frame population identity;
- measurement metric name;
- unit, `unit_semantics` and `angular_calibration_state` copied exactly from F3;
- method identifiers;
- measurement count;
- accepted descriptive statistics;
- quality/coverage;
- source/Citation/Provenance drill-down references;
- limitations/explanation codes.

Missing mandatory upstream semantics must fail closed. Unknown values must remain explicit unknowns; fabricated defaults are prohibited.

## 5. Determinism and source preservation

The F4 read model is a deterministic projection of F3.

For the first bounded implementation:

- the consumer population must resolve to the same 19 F3 measurements for `QUATTRO200_TOUPTEK294_BIN1` / `2026-07-14_2026-07-15` / `LDN 1320` / `LPRO` / `LIGHT`;
- the four accepted F3 statistics must be copied without recalculation or precision change;
- measurement ordering must be deterministic by accepted source sequence;
- source lineage arrays must remain repository-resolvable;
- the consumer may add presentation-oriented grouping/labels only when derived directly from accepted fields.

If F3 changes or becomes inconsistent, F4 generation/validation must fail rather than serving a stale authoritative-looking view.

## 6. Unit and comparability boundary

F4 must preserve exactly:

- `unit=NINA_FILENAME_FWHM_SOURCE_UNIT`;
- `unit_semantics=SOURCE_NATIVE_UNCALIBRATED`;
- `angular_calibration_state=NOT_PROVEN`.

F4 must not display or label the values as arcseconds, pixels, seeing, focus quality or equipment health unless a future governed increment proves and authorizes that semantic transformation.

Cross-configuration comparison and ranking are out of scope.

## 7. Consumer/UI boundary

A portal/static consumer may provide:

- configuration summary;
- session/target/filter context;
- measurement table;
- descriptive-statistic table/cards;
- drill-down links or textual references to source/Citation/Provenance;
- visible limitations and quality/coverage semantics.

It must not provide:

- GOOD/BAD/HEALTHY/DEGRADED labels;
- red/amber/green performance state;
- thresholds or target ranges;
- ranking, percentile or score;
- anomaly/failure diagnosis;
- predictive maintenance;
- recommended remediation;
- controls that can alter EAGLE, camera, focuser, mount, filter wheel, USB, power or network state.

## 8. Fail-closed validation requirements

Executable F4 validation must reject at least:

- missing or unresolved F3 source artifact;
- population/count mismatch versus F3;
- changed measurement/statistic values;
- changed unit or calibration semantics;
- unknown or unversioned method identifiers;
- missing source/Citation/Provenance references;
- arbitrary unknown consumer fields where schema forbids them;
- authority escalation;
- action authority other than `NONE`;
- health/ranking/threshold/recommendation semantics;
- incomplete drill-down lineage for a view claiming complete coverage.

Negative regression tests must prove the bounded fail-closed behaviors.

## 9. Security, operations and Safety

F4 introduces no secrets, credentials, network listeners, writable APIs or runtime command paths.

It is a repository/static read model. No EAGLE/PC command is required.

Historical performance data must never be used as current observatory Safety state. Local physical interlocks remain independent and authoritative.

## 10. Migration and rollback

No runtime migration is required. Existing F2/F3 evidence remains unchanged.

Rollback is repository revert of the F4 schema/read model/generator/validator/tests/portal projection/workflow integration.

## 11. Bounded implementation slices

### F4-A — Machine-readable consumer read model

Deliver:

- F4 schema;
- deterministic generator;
- generated read-model fixture;
- fail-closed validator;
- negative regression suite;
- dedicated F4 governance workflow;
- Developer Foundation integration.

Acceptance: exact-head CI green and independent ARB approval.

### F4-B — Read-only portal projection

Only after F4-A acceptance, optionally expose the same read model in the Scientific Platform/portal using static/read-only rendering with visible limitations and lineage drill-down.

If existing portal architecture already consumes repository JSON directly, F4-A and F4-B may be combined only if no new runtime/service boundary is introduced and ARB reviews the combined package.

## 12. Definition of Done for F4

F4 is complete when:

- deterministic consumer projection is repository-integrated;
- source values and semantics are preserved exactly;
- Citation/Provenance drill-down is preserved;
- fail-closed and negative tests are executable;
- no performance assessment/ranking/threshold/recommendation semantics are introduced;
- no runtime/Safety authority is added;
- dedicated governance and Developer Foundation are green;
- independent ARB is approved;
- Release Quality is READY;
- final exact-head CI is green;
- merge and post-merge exact-SHA workflows succeed.

After F4 acceptance, BKL-039 may enter formal closure governance.
