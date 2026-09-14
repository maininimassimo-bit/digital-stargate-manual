# BKL-039 F5 — Dynamic Multi-Session Equipment Performance Registry Contract

| Field | Value |
|---|---|
| Identifier | `BKL-039-F5` |
| Capability | BKL-039 — Equipment Performance Registry |
| Status | Proposed |
| Version | 0.2 |
| Date | 2026-09-09 |
| Base | F4-B accepted merge `e4ccecb3bc52af4a5baaa27cbc8df7178fd239ea` |
| Runtime impact | Repository/GitHub automation only; no observatory command path |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Objective

F5 evolves the accepted bounded single-population BKL-039 registry into a deterministic multi-session registry that is regenerated automatically whenever a newly imported COMPLETE scientific session updates the governed analytics history.

The normal production outcome is that a new eligible scientific session becomes visible in Equipment Performance without a manual per-session registry edit or portal page edit.

F5 remains historical, read-only and descriptive. It does not introduce equipment health, RAG state, thresholds, ranking, scoring, anomaly diagnosis, prediction, maintenance recommendation, remediation or control authority.

## 2. Verified upstream production flow

The accepted AP-014 automatic session path already promotes COMPLETE session evidence to `main`, runs `analyze-session-automatic.yml`, rebuilds normalized/history and target projections, commits governed analytics/catalog projections, and dispatches Pages.

F5 attaches Equipment Performance generation to that existing GitHub-side analytics projection phase. It does not add work to the EAGLE scheduled task and does not require a new EAGLE/PC command for normal operation.

## 3. Eligibility and fail-closed onboarding

A session is eligible for the registry only when all semantics required for the performance population are repository-resolvable. At minimum the generator must resolve:

- a scientific session identity;
- metadata risolti tramite record esplicito `metadata_state=REGISTERED` oppure tramite storia canonica con stato `CANONICAL_EVIDENCE`;
- a non-empty governed `configuration_id`;
- target identity/name;
- filter and frame population identity;
- source exposure rows produced by the governed analytics history;
- source-backed FWHM tokens for the declared measurement population;
- a matching target-summary population and count;
- Citation and Provenance locators.

Explicit metadata registry rows take precedence over canonical-history fallback for the same session. Canonical-history fallback is eligible only when target identity, `configuration_id` and exact `source_metrics_path` are all resolved; its Citation must reference `data/analytics/history/sessions.csv` and its Provenance the normalized session metrics. `PARTIAL` and `UNREGISTERED` sessions are never promoted to performance populations. Missing configuration identity, unresolved lineage, missing/invalid FWHM source values, missing summary rows or population/count disagreement must not be filled with defaults.

Fail-closed is population-scoped: an ineligible population is omitted with an explicit machine-readable exclusion reason in generation diagnostics; it must not corrupt or suppress already-valid historical populations. A structurally inconsistent population that claims complete coverage must fail validation.

## 4. Multi-session registry model

The F3 projection must no longer contain a hard-coded session/configuration/target/filter tuple. It must discover all eligible populations from governed repository inputs and emit deterministic records grouped by:

`configuration_id + session_id + target_name + filter_name + frame_type + metric_name + unit semantics`.

For each eligible population F5 preserves the accepted F3 semantics:

- `PERFORMANCE_MEASUREMENT` for source-backed FWHM values;
- `DESCRIPTIVE_PERFORMANCE_STATISTIC` for MEAN, MINIMUM, MAXIMUM and SAMPLE_STDDEV when sample size permits the declared statistic;
- `unit=NINA_FILENAME_FWHM_SOURCE_UNIT`;
- `unit_semantics=SOURCE_NATIVE_UNCALIBRATED`;
- `angular_calibration_state=NOT_PROVEN`;
- versioned method identifiers;
- `authority=projection`;
- `action_authority=NONE`;
- source record references, Citation and Provenance;
- explicit population coverage.

No cross-session or cross-configuration comparison is implied by co-location in the registry.

## 5. Dynamic read model and portal

F4 becomes a collection read model rather than a single `view`. It must expose a deterministic list of eligible population views. Each view carries its own configuration/session/target/filter/frame/metric identity, measurement count, measurements, descriptive statistics, unit/calibration semantics, lineage and limitations.

The Equipment Performance portal must consume this collection dynamically and provide a read-only population/session selector. The browser must not calculate authoritative measurements or statistics; it renders the generated repository projection.

A newly generated population therefore requires no Markdown edit. Once the automatic analytics commit containing the regenerated registry/read model reaches `main` and Pages is deployed, the population becomes available to the portal.

## 6. Automation integration

`analyze-session-automatic.yml` must regenerate and validate BKL-039 projections after target/history projections are rebuilt and before the governed analytics commit is created.

The governed commit path set must include the BKL-039 generated data artifacts. The regenerate/retry function must execute the same BKL-039 generation and validation sequence after each reset to `origin/main`, preserving the workflow's existing concurrency and retry behavior.

Required logical sequence:

```text
COMPLETE scientific session promoted to main
  -> analyze-session-automatic
  -> normalized session analytics/history
  -> target-exposures + target-summary + canonical sessions history + explicit scientific metadata
  -> discover eligible performance populations
  -> generate F3 multi-session registry
  -> validate F3
  -> generate F4 collection read model
  -> validate F4
  -> commit governed projections to main
  -> deploy Pages
  -> Equipment Performance exposes new eligible population
```

If the imported session is COMPLETE but its scientific metadata is not yet REGISTERED/resolvable, the session may remain visible in the scientific catalog while Equipment Performance excludes it until governed metadata becomes eligible. Automation must never synthesize configuration identity to force inclusion.

## 7. Current migration baseline

Repository scientific metadata currently contains multiple REGISTERED sessions, including LDN 1320 and M 27 populations, while the accepted F3/F4 implementation is hard-coded to `2026-07-14_2026-07-15 / LDN 1320`.

F5 migration must discover and onboard every currently eligible historical population from the same governed sources, including REGISTERED M 27 sessions when their exposure/summary/FWHM evidence satisfies this contract. The `2026-08-10_2026-08-11` M 27 session is explicitly PARTIAL and remains excluded unless a future governed reconciliation changes its metadata state.

No exact M 27 measurement count or statistic is asserted by this architecture contract; those values must be generated from repository evidence and validated by executable tests.

## 8. Determinism, idempotency and ordering

Generation must be deterministic and idempotent. Stable ordering is required at least by session, configuration, target, filter, frame type, source timestamp/sequence and statistic type. Re-running against unchanged repository inputs must produce byte-equivalent semantic content apart from fields explicitly governed as generated timestamps; generated timestamps should be avoided unless required.

Record identifiers must be deterministic from governed population identity and source sequence and must not depend on random UUID generation.

## 9. Validation requirements

Executable governance must prove at least:

1. more than one eligible session/population can coexist;
2. accepted LDN 1320 evidence remains preserved;
3. currently eligible M 27 evidence is included when source requirements are met;
4. PARTIAL metadata is excluded;
5. an unresolved configuration is excluded/fails closed rather than synthesized;
6. exposure/summary count mismatch is rejected;
7. invalid or missing FWHM source values are not silently converted;
8. per-population statistics match the exact declared source population;
9. unit and calibration semantics cannot be escalated;
10. Citation/Provenance/source-record lineage remains complete;
11. F4 contains exactly the eligible F3 populations and does not recalculate values;
12. portal code cannot introduce health/ranking/threshold/recommendation/control semantics;
13. the automatic session workflow executes F3/F4 generation and validation and stages their generated artifacts for the governed commit;
14. unchanged inputs regenerate without semantic drift.

Negative tests must cover authority escalation, synthetic identity, PARTIAL inclusion, cross-population leakage, duplicate records and stale read-model output.

## 10. Delivery slices

### F5-A — Multi-session source discovery and generator

Remove the single-session constants from F3 generation, discover eligible repository populations and generate deterministic per-population measurements/statistics. Migrate currently eligible historical sessions, including M 27 where evidence qualifies.

### F5-B — Collection read model and dynamic portal

Evolve F4 schema/generator/validator and Equipment Performance UI from one view to a collection with dynamic session/population selection while preserving read-only semantics.

### F5-C — Automatic import integration

Integrate F3/F4 regeneration and validation into `analyze-session-automatic.yml`, include generated BKL-039 artifacts in the governed analytics commit, and prove idempotent automatic onboarding with repository-level tests/fixtures. No EAGLE change is required unless later evidence shows the existing AP-014 producer contract itself must change.

### F5-D — Governance and closure

Run exact-head CI, independent ARB and Release Quality. Only after accepted F5-A/B/C may BKL-039 enter final closure governance.

## 11. Security, operations and Safety

F5 adds no secrets, credentials, listeners, writable portal API, device protocol or observatory command path. It runs in the existing repository/GitHub analytics publication boundary.

The portal, registry, analytics and automation remain non-authoritative for physical Safety. Local physical interlocks and the local Safety Authority remain independent and authoritative. F5 cannot bypass interlocks, alter Safety state or issue remediation commands.

## 12. Acceptance

F5 is accepted only when repository evidence proves both historical multi-session coverage and automatic future-session onboarding through the existing AP-014 publication chain, with exact-head CI, independent ARB, Release Quality and post-merge verification.


## 13. Corrective reconciliation — 2026-09-14

A production population audit found that target exposure and summary history reached session `2026-09-13_2026-09-14`, while the explicit scientific metadata registry ended at `2026-08-15_2026-08-16`. The prior discovery loop iterated only explicit metadata rows, so later canonical sessions were neither evaluated nor emitted as exclusions.

Version 0.2 therefore:

- retains explicit metadata rows as the higher-precedence governed attestation;
- adds `data/analytics/history/sessions.csv` as the canonical-history fallback for sessions with resolved target, configuration and normalized source locator;
- requires every canonical history session to be represented by at least one eligible population or an explicit fail-closed exclusion;
- keeps population eligibility strict: every declared exposure still requires a valid source-backed FWHM token and matching summary count;
- adds this coverage invariant to the automatic session workflow and unit tests;
- exposes the count of explicit exclusions in the read-only portal.

This amendment does not calibrate FWHM to angular units, classify equipment health, introduce thresholds/ranking/recommendations, infer Safety or add any PC Principale/EAGLE workload.
