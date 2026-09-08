# BKL-038 F2 — Machine-Readable Analytical Schema and Bounded Fixture

| Field | Value |
|---|---|
| Identifier | `BKL-038-F2` |
| Status | In Progress — F2-A |
| Version | 0.1 |
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
- this architecture contract.

## 3. Bounded fixture

The fixture contains exactly three derived records over accepted `docs/data/night-timeline-replay-f3.json` evidence:

1. one source-backed `OBSERVATION` for the first CloudWatcher replay event;
2. one `TREND_MEASUREMENT` representing the exact elapsed milliseconds between the CloudWatcher and N.I.N.A. events, explicitly `descriptive_only=true`;
3. one `CORRELATION_CANDIDATE` for the accepted N.I.N.A. -> PHD2 sequential relationship, explicitly `NOT_ASSESSED` and `CAUSATION_NOT_INFERRED`.

No anomaly candidate is fabricated because the accepted bounded replay evidence does not itself provide a governed anomaly rule suitable for F2-A.

## 4. Machine-readable semantics

Every record carries:

- deterministic derived identity;
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

The schema deliberately excludes recommendation execution and any command/remediation field.

## 5. Fail-closed validator

The validator must reject:

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

## 6. F2-A explicit exclusions

F2-A does not implement:

- arbitrary thresholds, z-scores, severity bands or predictive limits;
- anomaly scoring;
- causal/root-cause inference;
- recommendations;
- machine learning or AI inference;
- EAGLE runtime reads;
- new collectors, services, schedulers or APIs;
- Power/Network/Safety historical materialization;
- present-time Safety inference;
- device commands or automatic remediation.

## 7. ARB F1 observation disposition

`ARB-BKL-038-F1-O01` required F2 to avoid CI dependency on the live EAGLE filesystem.

F2-A satisfies the repository-resolvable aspect by starting with accepted BKL-040 evidence. It does **not** close the EAGLE-fixture part of the observation: no signal-level BKL-030 sample is invented. The observation remains carried forward until a governed bounded BKL-030 history fixture/evidence projection is repository-resolvable.

## 8. TD-012

F2 consumes `replay_event_id` exactly as present in the accepted BKL-040 F3 artifact. It does not retrofit the F1/F2 BKL-040 envelope or manufacture `source_event_id` values.

## 9. Safety boundary

All F2 records are historical analytical projections. They cannot authorize or execute roof, mount, camera, power, network, process or Safety actions. Local physical interlocks remain independent and authoritative.

## 10. Acceptance criteria for F2-A

F2-A is review-ready when:

1. schema, fixture and validator are repository-integrated on the feature branch;
2. the fixture resolves only accepted repository evidence;
3. exact temporal delta reproduces upstream timestamps;
4. Citation/Provenance references resolve;
5. descriptive trend remains non-anomalous;
6. correlation remains non-causal and `NOT_ASSESSED`;
7. authority/action boundaries are fail-closed;
8. applicable exact-head CI is green;
9. independent ARB approves the slice before further detector implementation.

## 11. Next slice after F2-A

F2-B should add a bounded BKL-030 EAGLE history fixture only from accepted repository-resolvable evidence, then demonstrate a data-quality anomaly candidate (or another explicitly governed rule match) without inventing thresholds.
