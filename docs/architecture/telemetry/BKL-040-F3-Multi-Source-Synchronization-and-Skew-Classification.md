# BKL-040 F3 — Multi-Source Synchronization & Skew Classification

| Field | Value |
|---|---|
| Package | BKL-040 — Night Timeline / Observatory Replay |
| Increment | F3 — Multi-Source Synchronization, Conflict & Skew Classification |
| Status | Proposed |
| Version | 0.1 |
| Date | 2026-09-08 |
| Baseline | `ba17df5584a82c4396bd7dccf6bf593c518d8429` |
| Upstream | BKL-040 F1 + F2 |
| Authority | Projection only |
| Runtime impact | None |
| Safety impact | None |

## 1. Purpose

F3 defines how independently timestamped historical evidence can be correlated into a deterministic observing-night timeline without changing source authority, inventing event time or silently collapsing disagreement.

F3 is a synchronization and classification layer only. It does not implement a replay UI, device command path, runtime collector, message bus or historical-data backfill.

## 2. Verified starting point

The accepted F2 baseline provides a bounded replay projection for session `2026-08-15_2026-08-16` with executable schema validation, Citation/Provenance binding, `PLACED | UNPLACED` temporal semantics and deterministic ordering.

Repository truth also confirms historically stored session evidence families for N.I.N.A., PHD2 and weather/CloudWatcher, plus previously governed SQM and EAGLE health history contracts. However F3 must not assume that every stored source family already has an accepted event parser or timestamp locator.

Therefore source participation is split into:

- **eligible** — an exact source field or record timestamp is governed and can be normalized without invention;
- **candidate** — historical bytes/records exist, but an exact event-time extraction contract is not yet governed;
- **excluded** — no durable historical source has been proven.

Candidate or excluded sources do not enter the synchronized sequence.

## 3. Synchronization model

F3 preserves the F1 canonical axis `event_time_utc` and the F2 total order:

1. `event_time_utc ASC`;
2. neutral `source_order ASC`;
3. stable `replay_event_id ASC`.

Synchronization never rewrites source timestamps. A derived synchronization record may classify relationships between events, but source events remain immutable projections of their own evidence.

## 4. Correlation envelope

A future F3 machine-readable artifact must represent each derived relationship explicitly, at minimum with:

- `correlation_id`;
- `session_id`;
- `left_event_ref`;
- `right_event_ref`;
- `relationship_type`;
- `delta_ms` when both events are `PLACED`;
- `classification_method_id`;
- `classification_state`;
- `citation_refs`;
- `provenance_refs`;
- `conflict_refs` where material disagreement exists.

Derived correlation records are always `projection` authority.

## 5. Relationship types

Initial bounded relationship vocabulary:

- `COINCIDENT` — two placed events represent independent evidence close enough in time to be considered co-temporal under a governed method;
- `SEQUENTIAL` — deterministic temporal ordering exists but no co-temporal claim is made;
- `UNPLACED_RELATED` — at least one event is `UNPLACED`; evidence may be associated by governed non-temporal identity only, never by invented time;
- `CONFLICTING` — two source records make materially incompatible claims that must remain simultaneously visible;
- `UNRELATED` — no governed correlation can be asserted.

No relationship type changes the source-authority class of either event.

## 6. Clock-skew classification

F3 may calculate observed timestamp deltas between already placed events, but it must not automatically correct or rewrite timestamps.

Initial classification states are deliberately descriptive rather than operational:

- `NOT_ASSESSED`;
- `WITHIN_METHOD_WINDOW`;
- `OUTSIDE_METHOD_WINDOW`;
- `UNAVAILABLE`.

A numeric threshold must not be invented. Any window used by F3 must be introduced as a versioned governed method with explicit rationale, source families and tests. Until such a method exists, only exact delta calculation and `NOT_ASSESSED` classification are allowed.

## 7. Conflict preservation

If independent historical sources disagree:

1. both source events remain present;
2. neither source is silently preferred by display order;
3. the disagreement is materialized as a separate conflict record;
4. the conflict carries Citation/Provenance for all participating evidence;
5. conflict state cannot be flattened into a single reconciled value without a later governed decision.

Historical Safety observations are evidence only. A conflict involving Safety-related history cannot be used to infer or modify present-time Safety Authority.

## 8. Source-family onboarding rule

A source family can become F3-eligible only when all of the following are true:

1. durable historical source is identified;
2. exact record/event locator is known;
3. source timestamp semantics are explicit;
4. UTC normalization is deterministic;
5. Citation locator is resolvable;
6. Provenance method is versioned;
7. malformed/missing timestamp behavior is fail-closed;
8. source-order mapping already exists or is explicitly extended by governance.

This rule applies independently to N.I.N.A., PHD2, CloudWatcher, SQM, EAGLE health and any future Power/Network/Safety/session-event channel.

## 9. Bounded F3 implementation path

The first executable F3 increment should remain bounded to one governed session and a small number of source families whose event-time contracts can be proven directly from repository evidence.

Recommended implementation sequence:

1. inventory exact event-time locators for N.I.N.A., PHD2 and weather evidence in the accepted session;
2. onboard only sources with deterministic parsers;
3. extend the replay fixture with those events while preserving F2 schema semantics;
4. add a separate correlation/conflict artifact;
5. validate deltas, total ordering, Citation/Provenance and conflict visibility;
6. keep skew classification at `NOT_ASSESSED` until an explicit method window is approved.

If no exact parser can be proven for a source, it remains `candidate`; F3 must not infer timestamps from file metadata.

## 10. Safety and security boundaries

F3 remains historical/read-only and must not:

- execute recorded commands;
- open/close the roof;
- move/park the mount;
- switch power or network state;
- acknowledge or bypass Safety;
- transform historical observations into current command authorization;
- modify EAGLE runtime behavior;
- introduce automatic remediation.

Local physical interlocks and the local Safety Authority remain independent and authoritative.

## 11. Migration and rollback

F3 is additive. Existing F2 replay events and source evidence remain unchanged. Derived correlations/conflicts are new projections only.

Rollback is repository revert of F3 artifacts and validators; no runtime or hardware rollback is required.

## 12. Acceptance criteria

F3 architecture is ready for executable implementation when:

- source eligibility criteria are explicit;
- no source timestamp can be inferred from file/ingestion/commit metadata;
- correlation records preserve both participating event references and full lineage;
- timestamp deltas are descriptive and do not rewrite event time;
- no skew threshold exists without a versioned governed method;
- conflict preservation is fail-closed and non-flattening;
- Safety and command boundaries remain unchanged;
- implementation scope is bounded to repository-proven source contracts.

Before merge of any executable F3 package: Developer Foundation, documentation, Word, independent ARB and Release Quality must all pass on the exact head.