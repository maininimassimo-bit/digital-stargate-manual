# BKL-040 F3 — Multi-Source Synchronization & Skew Classification

| Field | Value |
|---|---|
| Package | BKL-040 — Night Timeline / Observatory Replay |
| Increment | F3 — Multi-Source Synchronization, Conflict & Skew Classification |
| Status | Proposed |
| Version | 0.2 |
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

The governed session manifest declares `timezone_id = Europe/Rome` and explicit local session boundaries with `+02:00` offset. Its `files[].modified_local` values remain file metadata only and are prohibited as replay event time.

### 2.1 Verified source eligibility inventory

| Source family | Historical evidence | Native event-time evidence | F3 state | Governed normalization method |
|---|---|---|---|---|
| N.I.N.A. | `raw/nina/20260815-204018-3.2.0.9001.6188-202608.log` | `DATE` column, e.g. `2026-08-15T20:40:29.7413` | **eligible** | `BKL040-F3-NINA-LOCAL-TO-UTC-1` |
| PHD2 GuideLog | `raw/phd2/PHD2_GuideLog_2026-08-15_203750.txt` | absolute anchor `Guiding Begins at 2026-08-15 22:11:13` plus frame `Time` seconds | **eligible** | `BKL040-F3-PHD2-GUIDE-ANCHOR-1` |
| CloudWatcher | `raw/weather/CloudWatcher_2026-08-15_2026-08-16.csv` | per-row `Date` + `Time`, e.g. `2026-08-15` + `19:00:09` | **eligible** | `BKL040-F3-CLOUDWATCHER-LOCAL-TO-UTC-1` |
| SQM | governed historical capability exists, but no session-scoped F3 locator is bound in this increment | deferred | candidate | none in F3 v0.2 |
| EAGLE health | governed historical capability exists, but no session-scoped F3 locator is bound in this increment | deferred | candidate | none in F3 v0.2 |
| Power / Network / local Safety | no exact durable session-scoped source contract proven for this increment | none | excluded | none |

### 2.2 N.I.N.A. timestamp contract

- Eligible records are normal log rows after the `DATE|LEVEL|SOURCE|MEMBER|LINE|MESSAGE` header.
- `DATE` is a local wall-clock timestamp without an embedded offset.
- For this bounded session, timezone interpretation comes only from the session manifest `timezone_id = Europe/Rome`.
- UTC normalization must use the timezone rules for the actual record date; no fixed offset may be hard-coded as a general parser rule.
- A row whose `DATE` cannot be parsed under this contract becomes `UNPLACED`; file name or file modification time must not be substituted.

The inspected N.I.N.A. log also independently records `Mount UTC Time` and `System UTC Time` with a reported difference of `0.004 seconds`. This is evidence that may later support a clock assessment method, but F3 v0.2 does **not** turn it into a general skew threshold or timestamp correction.

### 2.3 PHD2 GuideLog timestamp contract

- Each guiding section begins with an explicit absolute local anchor, for example `Guiding Begins at 2026-08-15 22:11:13`.
- The subsequent CSV-like frame rows expose `Time` as elapsed seconds from that guiding-section anchor.
- A frame event time is therefore derived only as `anchor_local + Time seconds`, interpreted in the manifest timezone `Europe/Rome`, then normalized to UTC.
- `Log enabled at ...` is metadata for the log lifecycle and must not replace a missing guiding-section anchor.
- Historical calibration timestamps such as `Timestamp = 17/02/2026 22:49:09` are calibration metadata and are not frame event time.
- If a frame occurs without a valid enclosing absolute guiding anchor, it is `UNPLACED`.

### 2.4 CloudWatcher timestamp contract

- Each CSV data row carries explicit `Date` and `Time` fields.
- The combined local timestamp is interpreted using the session manifest `timezone_id = Europe/Rome`, then normalized to UTC.
- The first inspected row is `2026-08-15 19:00:09`, demonstrating record-level temporal evidence independent of file metadata.
- The CSV may contain UTF-8 BOM and quoted fields; parser normalization may remove BOM/quoting syntax but must not alter evidence values.
- A row with malformed/missing `Date` or `Time` becomes `UNPLACED`; `modified_local` must not be used as fallback.

### 2.5 Eligibility consequence

The first executable F3 synchronization fixture may therefore onboard **N.I.N.A., PHD2 GuideLog and CloudWatcher** only. SQM/EAGLE remain candidate until exact session-scoped locators are bound; Power/Network/Safety remain excluded in this increment.

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

`COINCIDENT` remains unavailable until a versioned coincidence window is separately governed. In the initial executable F3 path, cross-source placed events can be classified `SEQUENTIAL` with exact `delta_ms` and `classification_state = NOT_ASSESSED`.

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

The first executable F3 increment remains bounded to session `2026-08-15_2026-08-16` and the three eligible source families above.

Implementation sequence:

1. implement deterministic parsers for N.I.N.A., PHD2 GuideLog and CloudWatcher using the three versioned timestamp methods;
2. select a small, auditable event subset from each source rather than bulk-importing all records;
3. extend the replay projection without changing F2 `PLACED | UNPLACED`, ordering or lineage semantics;
4. add a separate bounded correlation/conflict artifact;
5. validate exact `delta_ms`, total ordering, Citation/Provenance and conflict visibility;
6. keep cross-source skew state at `NOT_ASSESSED` until an explicit method window is approved.

No parser may infer event time from filename, file creation/modification, ingestion, Git commit, session boundary or persistence time.

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

- N.I.N.A., PHD2 GuideLog and CloudWatcher timestamp contracts are explicit and versioned;
- timezone interpretation is bound to the governed session timezone and not guessed from the execution host;
- malformed timestamps become `UNPLACED` rather than receiving fallback times;
- no source timestamp can be inferred from file/ingestion/commit metadata;
- correlation records preserve both participating event references and full lineage;
- timestamp deltas are descriptive and do not rewrite event time;
- no skew/coincidence threshold exists without a versioned governed method;
- conflict preservation is fail-closed and non-flattening;
- Safety and command boundaries remain unchanged;
- implementation scope remains bounded to repository-proven source contracts.

Before merge of any executable F3 package: Developer Foundation, documentation, Word, independent ARB and Release Quality must all pass on the exact head.