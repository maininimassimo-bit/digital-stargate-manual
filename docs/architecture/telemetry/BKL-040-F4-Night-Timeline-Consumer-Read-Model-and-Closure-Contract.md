# BKL-040 F4 — Night Timeline Consumer Read-Model & Closure Contract

| Field | Value |
|---|---|
| Package | BKL-040 — Night Timeline / Observatory Replay |
| Increment | F4 — Consumer / Read-Model Projection and Closure |
| Status | Proposed |
| Version | 1.0 |
| Date | 2026-09-08 |
| Baseline | `7dc867c50ee588d46f4e23e2880d10373f3fbbc5` |
| Upstream | BKL-040 F1 + F2 + F3 |
| Authority | Projection only |
| Runtime impact | None |
| Safety impact | None |

## 1. Purpose

F4 defines the bounded consumer/read-model that a future portal or API may render for historical Night Timeline / Observatory Replay. It closes the package only if the consumer preserves F1 temporal semantics, F2 structural/lineage invariants and F3 multi-source synchronization without creating new truth, authority, conflict resolution, clock-skew policy or command capability.

F4 is repository-only and read-only. It does not implement browser controls, playback against devices, a runtime service, database, event bus or historical backfill.

## 2. Consumer contract

The consumer projection is `docs/data/night-timeline-read-model.json` and is derived from the accepted F3 artifact `docs/data/night-timeline-replay-f3.json`.

The consumer exposes:

- package/session identity;
- governed timezone;
- a bounded ordered timeline of display events;
- source family and source authority labels;
- raw source timestamp alongside canonical UTC;
- Citation and Provenance references per event;
- bounded correlation summaries with exact `delta_ms` and preserved `NOT_ASSESSED` skew state;
- a distinct `unplaced_events` collection for future `UNPLACED` evidence;
- explicit read-only UI semantics.

## 3. Preservation rules

A F4 consumer must preserve the following fields exactly from F3 for every rendered event:

- `replay_event_id`;
- `event_time_utc`;
- `source_timestamp_raw`;
- `source_type`;
- `source_order`;
- `source_authority`;
- `event_kind`;
- `quality_state`;
- Citation refs;
- Provenance refs.

A consumer may add presentation-only labels, but it must not rename or reinterpret source evidence.

## 4. Correlation and skew semantics

F4 may display F3 correlations, but it must preserve:

- `relationship_type = SEQUENTIAL`;
- exact `delta_ms`;
- `classification_method_id = BKL040-F3-EXACT-DELTA-1`;
- `classification_state = NOT_ASSESSED`;
- participating event refs and lineage refs.

The consumer must not translate `NOT_ASSESSED` into healthy, synchronized, acceptable, warning, unsafe or any other operational judgment.

No coincidence/skew threshold is introduced in F4.

## 5. Conflict and UNPLACED preservation

The accepted F3 bounded fixture contains no conflict records and no `UNPLACED` events. F4 nevertheless reserves explicit collections rather than flattening these states.

Rules:

- `unplaced_events` is separate from the synchronized UTC sequence;
- conflict references, when present in a later governed upstream contract, must remain explicit;
- consumer code must not discard conflicting source records in favor of the first/last rendered event;
- absence of conflicts in the current fixture does not mean conflict-free semantics are authorized globally.

## 6. UI/API semantics

The read-model declares:

- `interaction_mode = READ_ONLY`;
- `playback_mode = VISUAL_ONLY`;
- `command_actions = []`;
- `safety_authority = UNCHANGED_LOCAL_AUTHORITY`.

A future portal may implement scrub, play/pause visualization, filtering, source highlighting and evidence drill-down. Those controls operate only on historical projection state.

It must never expose actions that:

- replay a historical device command;
- open/close the roof;
- move/park the mount;
- change camera/power/network state;
- acknowledge/bypass Safety;
- convert historical evidence into current command authorization;
- alter the local Safety Authority or physical interlocks.

## 7. Failure behavior

The validator fails closed if the read-model:

- promotes authority;
- changes baseline/session/timezone identity;
- drops or reorders timeline events;
- changes event timestamps, source identity or lineage;
- rewrites correlation deltas or skew state;
- introduces command actions;
- changes read-only/visual-only semantics;
- removes explicit containers for future UNPLACED/conflict preservation.

## 8. Architecture impact

### Components

- **F3 synchronization projection** — upstream authoritative projection for F4 consumption;
- **F4 consumer read-model** — stable read-only adapter for future UI/API surfaces;
- **F4 validator/tests** — CI guard against semantic/authority drift.

### Data flow

`raw historical evidence -> F3 deterministic synchronization -> F4 read-model -> future visual consumer`

There is no reverse path from F4 to F3, source logs, runtime telemetry or observatory devices.

## 9. Migration and rollback

F4 is additive. No existing F1/F2/F3 artifact is modified.

Rollback is repository revert of the F4 read-model, validator/tests, schema/contract and CI integration. No runtime or hardware rollback is required.

## 10. Acceptance and package closure criteria

BKL-040 can close only when:

1. F4 read-model validates exactly against accepted F3 evidence;
2. fail-closed tests prove authority, timestamp, ordering, lineage, skew and command boundaries;
3. Developer Foundation, documentation and Word workflows pass on the exact head;
4. independent ARB approves the F4 consumer contract;
5. Release Quality returns Ready for Merge;
6. merge uses expected-head protection;
7. post-merge workflows are green on the actual merge SHA;
8. roadmap/closure artifacts are updated only after those validations are verified.

Runtime OAT and EAGLE actions are Not Applicable for this repository-only consumer projection.