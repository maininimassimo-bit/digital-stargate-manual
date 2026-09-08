# BKL-038 F2 — Machine-Readable Analytical Schema and Bounded Fixture

| Field | Value |
|---|---|
| Identifier | `BKL-038-F2` |
| Status | In Progress — F2-A |
| Version | 0.2 |
| Date | 2026-09-08 |
| Parent | BKL-038 — Anomaly & Trend Center |
| Accepted upstream | BKL-038 F1 merge `0a91e280d86cbcb7272d88c1c68f282d00272823` |
| Authority | Projection only |
| Runtime impact | None |
| Safety Authority | No |

## 1. Purpose

Materialize the first machine-readable analytical-record contract and a bounded deterministic fixture without depending on the live EAGLE filesystem.

F2-A intentionally uses only the accepted BKL-040 F3 repository artifact because it is directly repository-resolvable. It does not fabricate BKL-030 EAGLE signal history. A BKL-030 fixture may be onboarded only when a bounded accepted record sample/evidence projection is available in the repository with upstream identity, timestamp, quality, source and provenance preserved.

## 2. Deliverables

- `schemas/anomaly-trend-analytical-record.schema.json` — strict analytical-record schema;
- `docs/data/anomaly-trend-f2-fixture.json` — bounded deterministic fixture;
- `.github/scripts/verify-anomaly-trend-f2.mjs` — fail-closed schema/source/semantic validator;
- `.github/scripts/test-anomaly-trend-f2.mjs` — bounded negative regression suite;
- Developer Foundation integration for both positive and negative validation;
- this architecture contract.

## 3. Bounded fixture

The fixture contains exactly three derived records over accepted `docs/data/night-timeline-replay-f3.json` evidence:

1. one source-backed `OBSERVATION` for the first CloudWatcher replay event;
2. one `TREND_MEASUREMENT` representing the exact elapsed milliseconds between the CloudWatcher and N.I.N.A. events, explicitly `descriptive_only=true`;
3. one `CORRELATION_CANDIDATE` for the accepted N.I.N.A. -> PHD2 sequential relationship, explicitly `NOT_ASSESSED` and `CAUSATION_NOT_INFERRED`.

No anomaly candidate is fabricated because the accepted bounded replay evidence does not itself provide a governed anomaly rule suitable for F2-A.

## 4. Machine-readable semantics

Every record carries:

- a unique bounded-fixture `derived_record_id`;
- semantic type;
- method id/version;
- upstream source record references;
- Citation references;
- Provenance references;
- explicit analysis window;
- optional measurement;
- candidate/rule state where applicable;
- observation-time quality classification;
- explanation codes;
- `authority=projection`;
- `action_authority=NONE`.

F2-A validates uniqueness but does not yet define a normative deterministic ID-generation algorithm. The F1 deterministic identity tuple (`semantic type + method id/version + ordered source references + declared analysis window`) remains the required basis for F3 generation. F3 must define/version the canonical serialization and generation algorithm before producing analytical records dynamically. F2-A therefore does not claim that its human-authored fixture IDs prove deterministic generation.

The schema deliberately excludes recommendation execution and any command/remediation field.

## 5. Fail-closed validator and regression suite

The positive validator rejects:

- schema violations or unexpected properties;
- duplicate derived identities;
- unresolved upstream replay-event references;
- unresolved Citation/Provenance references;
- descriptive trends promoted to anomaly state;
- `OBSERVED_RULE_MATCH` without `rule_id`;
- correlation candidates not left `NOT_ASSESSED` in this bounded slice;
- correlation candidates without `CAUSATION_NOT_INFERRED`;
- authority other than `projection`;
- action authority other than `NONE`;
- an exact temporal delta that does not reproduce accepted BKL-040 source timestamps.

The negative suite mutates the accepted fixture and requires fail-closed rejection for trend self-promotion, rule-match without rule identity, correlation promotion/causation-guard removal, unresolved source/Citation/Provenance, and authority/action-authority changes. Developer Foundation executes both the positive validator and negative suite on every applicable change.

## 6. F2-A explicit exclusions

F2-A does not implement arbitrary thresholds, z-scores, severity bands, predictive limits, anomaly scoring, causal/root-cause inference, recommendations, ML/AI inference, EAGLE runtime reads, new collectors/services/schedulers/APIs, Power/Network/Safety historical materialization, present-time Safety inference, device commands or automatic remediation.

## 7. ARB finding disposition

The first independent ARB review of exact head `3da393f0a3f76593b6cf1bed248dcd96127e4ef2` returned **REWORK REQUIRED**.

- `ARB-BKL-038-F2-A-M01`: resolved by adding the positive F2 validator and negative F2 suite to Developer Foundation.
- `ARB-BKL-038-F2-A-M02`: resolved by adding `.github/scripts/test-anomaly-trend-f2.mjs` with bounded fail-closed mutations.
- `ARB-BKL-038-F2-A-m01`: resolved by narrowing F2-A identity claims; deterministic ID generation is explicitly deferred to F3 with the F1 identity tuple preserved as normative input.
- `ARB-BKL-038-F2-A-O01`: remains open; no BKL-030 EAGLE history is fabricated and CI remains repository-resolvable.

A new exact-head CI pass and independent ARB re-review are mandatory after these changes.

## 8. ARB F1 observation disposition

`ARB-BKL-038-F1-O01` required F2 to avoid CI dependency on the live EAGLE filesystem. F2-A satisfies the repository-resolvable aspect using accepted BKL-040 evidence. The EAGLE-fixture portion remains open until a governed bounded BKL-030 history fixture/evidence projection is repository-resolvable.

## 9. TD-012

F2 consumes `replay_event_id` exactly as present in accepted BKL-040 F3. It does not retrofit the BKL-040 envelope or manufacture `source_event_id` values.

## 10. Safety boundary

All F2 records are historical analytical projections. They cannot authorize or execute roof, mount, camera, power, network, process or Safety actions. Local physical interlocks remain independent and authoritative.

## 11. Acceptance criteria for F2-A

F2-A is review-ready when schema/fixture/validator/tests are integrated; fixture resolves only accepted evidence; exact delta reproduces source timestamps; Citation/Provenance resolve; trend remains non-anomalous; correlation remains non-causal and `NOT_ASSESSED`; authority boundaries fail closed; Developer Foundation executes positive and negative F2 checks; exact-head CI is green; and independent ARB approves before further detector implementation.

## 12. Next slice after F2-A

F2-B may add a bounded BKL-030 EAGLE history fixture only from accepted repository-resolvable evidence, then demonstrate a data-quality anomaly candidate (or another explicitly governed rule match) without inventing thresholds. F3 must define the deterministic derived-ID generation algorithm before dynamic analytical record production.
