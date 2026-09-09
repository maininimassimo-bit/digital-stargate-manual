# RQ-BKL-039-F4-A — Release Quality Review — 2026-09-09

| Field | Value |
|---|---|
| Review ID | `RQ-BKL-039-F4-A` |
| Capability | BKL-039 — Equipment Performance Registry |
| Increment | F4-A — Machine-Readable Read-Only Consumer |
| PR | #130 |
| Reviewed HEAD | `1a82088b88d1dcb419ae689740f311f6147a265f` |
| Base | `ce2482aa6b2da62296ebdc221f73f39c1acd3aa2` |
| ARB | `ARB-BKL-039-F4-A` — APPROVED 98/100 |
| Decision | **READY FOR MERGE** |
| Waiver | None |

## 1. Release impact report

BKL-039 F4-A is a bounded repository/static read-only consumer increment. It projects accepted F3 equipment-performance evidence into a deterministic machine-readable consumer model without creating new measurement, assessment or operational semantics.

The implementation adds a strict read-model schema, deterministic generator, generated read-model fixture, fail-closed validator, negative regression suite, dedicated F4 Governance workflow and Developer Foundation integration. It does not add collectors, writable APIs, runtime services, schedulers, EAGLE dependencies, device commands, remediation, thresholds, ranking, health scoring, anomaly diagnosis, prediction or maintenance recommendations.

## 2. Quality-gate matrix

| Gate | Status | Evidence |
|---|---|---|
| Architecture review | Passed | Independent ARB re-review `APPROVED — 98/100`; review `5156625629` |
| Dedicated F4 governance | Passed | BKL-039 F4 Governance #4 — SUCCESS on exact reviewed HEAD |
| Build / repository validation | Passed | Developer Foundation #1163 — SUCCESS on exact reviewed HEAD |
| Documentation | Passed | Validate documentation #782 — SUCCESS |
| Word/manual generation | Passed | Genera manuale Word #1207 — SUCCESS |
| Upstream dependency | Passed | Accepted F3 merge `ce2482aa6b2da62296ebdc221f73f39c1acd3aa2` remains the base |
| Consumer population | Passed | Same bounded `QUATTRO200_TOUPTEK294_BIN1` / `2026-07-14_2026-07-15` / `LDN 1320` / `LPRO` / `LIGHT` population |
| Measurement fidelity | Passed | Exactly 19 accepted F3 measurements are projected in deterministic source order |
| Statistic fidelity | Passed | Accepted F3 mean/min/max/sample-stddev values are copied without reinterpretation |
| Unit/calibration | Passed | `NINA_FILENAME_FWHM_SOURCE_UNIT`, `SOURCE_NATIVE_UNCALIBRATED`, `NOT_PROVEN` preserved |
| Method/version semantics | Passed | Accepted versioned F3 method identifiers preserved |
| Fail-closed structure | Passed | Strict field sets and schema; arbitrary/forbidden assessment fields rejected |
| Negative regression | Passed | Authority, action authority, value/statistic, unit/calibration, lineage, population and prohibited-semantics mutations rejected |
| Citation / Provenance | Passed | Source/Citation/Provenance retained and required |
| Security | Passed / bounded | No credentials, listeners, writable endpoints or command surfaces added |
| Safety | Passed | `authority=projection`, `action_authority=NONE`; no current-time Safety inference; local physical interlocks remain authoritative |
| Observability | Not Applicable | No runtime component |
| Migration | Not Applicable | No runtime or persistent-data migration |
| Rollback | Passed | Repository revert sufficient |
| Operations | Not Applicable | No PC/EAGLE action required |

## 3. Definition of Done assessment

F4-A satisfies the bounded release Definition of Done:

- accepted F3 evidence remains the only semantic source;
- machine-readable schema, generator, generated read model, validator and negative tests are repository-integrated;
- source values, four descriptive statistics, units, calibration state, method identifiers, quality, Citation and Provenance are preserved;
- prohibited health/ranking/threshold/recommendation/remediation semantics fail closed structurally;
- dedicated F4 Governance and Developer Foundation independently execute the F4 checks and are green on the exact reviewed HEAD;
- independent ARB is APPROVED;
- runtime, command authority and Safety Authority remain unchanged.

## 4. Risk and waiver register

### R01 — Source FWHM physical unit remains unproven

Disposition: **Accepted bounded semantic distinction / non-blocking**.

The consumer preserves `NINA_FILENAME_FWHM_SOURCE_UNIT`, `SOURCE_NATIVE_UNCALIBRATED` and `angular_calibration_state=NOT_PROVEN`. No conversion to arcseconds, pixels or a physical seeing/focus metric is authorized.

### R02 — Consumer is intentionally bounded to one accepted population

Disposition: **Intentional bounded scope / non-blocking**.

F4-A proves deterministic consumption of the accepted F3 population only. Expansion requires preserving source, unit, method, identity, population and lineage comparability.

### R03 — Interpretation creep in future consumers

Disposition: **Future-governance entry gate**.

Health labels, RAG states, thresholds, target ranges, rankings, percentiles, scores, anomaly/failure diagnosis, prediction, maintenance recommendation, remediation and control surfaces remain outside this increment.

### R04 — F4-B portal projection is not part of this release increment

Disposition: **Explicitly deferred / non-blocking**.

F4-A establishes the governed machine-readable consumer artifact. Any portal/static exposure is a separate F4-B step unless it can be shown to reuse this artifact without creating a new runtime/service or authority boundary and is separately governed.

### Waivers

None.

## 5. Safety and authority statement

F4-A remains historical/static, read-only and projection-only with `authority=projection` and `action_authority=NONE`.

It introduces no device command, process restart, focus/cooling/mount action, power/USB/network remediation, scheduler action or present-time Safety inference. Local physical interlocks remain independent and authoritative.

## 6. Rollback and recovery

Rollback is repository revert of the F4-A schema, generator, read-model fixture, validator, regression tests, workflow integration, contract and review artifacts. Accepted F2/F3 evidence remains unchanged. No EAGLE action, migration rollback or runtime data recovery is required.

## 7. Release recommendation

**READY FOR MERGE — no waivers.**

Merge is authorized only if:

1. final exact-head CI is green after this Release Quality artifact is committed;
2. PR #130 remains open, non-draft, mergeable and unchanged in scope;
3. merge uses expected-head protection;
4. applicable post-merge workflows succeed on the real merge SHA;
5. F4-A is marked repository-integrated/ACCEPTED only after post-merge exact-SHA verification.
