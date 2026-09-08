# BKL-040 F4 — Night Timeline Consumer Read-Model & Closure Contract

| Field | Value |
|---|---|
| Package | BKL-040 — Night Timeline / Observatory Replay |
| Increment | F4 — Consumer / Read-Model Projection and Closure |
| Status | Proposed |
| Version | 1.1 |
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

The consumer exposes package/session identity, governed timezone, a bounded ordered timeline, source authority, raw and canonical timestamps, Citation/Provenance lineage, correlation summaries, explicit `unplaced_events` and `conflicts` collections, and read-only UI semantics.

For this accepted F3 baseline both `unplaced_events` and `conflicts` MUST be empty. They are reserved containers, not extension points for consumer-authored evidence.

## 3. Preservation rules

A F4 consumer must preserve exactly from F3 for every rendered event: `replay_event_id`, `event_time_utc`, `source_timestamp_raw`, `source_type`, `source_order`, `source_authority`, `event_kind`, `summary`, `quality_state`, Citation refs and Provenance refs.

A consumer may add presentation-only labels only in a future governed extension; it must not rename, reinterpret or manufacture source evidence.

## 4. Correlation and skew semantics

F4 may display F3 correlations, but it must preserve `relationship_type = SEQUENTIAL`, exact `delta_ms`, `classification_method_id = BKL040-F3-EXACT-DELTA-1`, `classification_state = NOT_ASSESSED`, participating event refs and lineage refs.

The consumer must not translate `NOT_ASSESSED` into healthy, synchronized, acceptable, warning, unsafe or any other operational judgment. No coincidence/skew threshold is introduced in F4.

## 5. Conflict and UNPLACED preservation

The accepted F3 bounded fixture contains no conflict records and no `UNPLACED` events. F4 therefore requires both consumer collections to be present and empty.

Rules:

- `unplaced_events` is a separate reserved collection and MUST be empty for this baseline;
- `conflicts` is a separate reserved collection and MUST be empty for this baseline;
- consumer code MUST fail closed if either collection contains evidence not materialized by the accepted upstream projection;
- a future non-empty collection is valid only after an accepted upstream F3+ contract materializes the records and F4 preserves their stable identity, Citation/Provenance and conflict lineage;
- consumer code must never discard or fabricate conflicting source records;
- absence of conflicts in the current fixture does not authorize a global conflict-free assumption.

## 6. UI/API semantics

The read-model declares `interaction_mode = READ_ONLY`, `playback_mode = VISUAL_ONLY`, `command_actions = []`, and `safety_authority = UNCHANGED_LOCAL_AUTHORITY`.

A future portal may implement scrub, play/pause visualization, filtering, source highlighting and evidence drill-down. Those controls operate only on historical projection state.

It must never replay a historical device command; open/close the roof; move/park the mount; change camera/power/network state; acknowledge/bypass Safety; convert historical evidence into current command authorization; or alter local Safety Authority/physical interlocks.

## 7. Failure behavior

The normative F4 structural contract for this bounded increment is the CI-executed validator `.github/scripts/verify-night-timeline-read-model.mjs` plus its fail-closed regression suite. A dedicated JSON Schema is not introduced in this increment; any future contract expansion should either add a closed schema or explicitly retain the validator as normative.

The validator fails closed if the read-model promotes authority; changes baseline/session/timezone identity; drops/reorders timeline events; changes event timestamps, source identity or lineage; rewrites correlation deltas/skew state; introduces command actions; changes read-only/visual-only semantics; removes reserved containers; or injects unsupported UNPLACED/conflict evidence.

## 8. Architecture impact

Components are the accepted F3 synchronization projection, the F4 stable read-only adapter for future UI/API surfaces, and F4 validator/tests as CI guard against semantic/authority drift.

Data flow: `raw historical evidence -> F3 deterministic synchronization -> F4 read-model -> future visual consumer`.

There is no reverse path from F4 to F3, source logs, runtime telemetry or observatory devices.

## 9. Migration and rollback

F4 is additive. No existing F1/F2/F3 artifact is modified. Rollback is repository revert of the F4 read-model, validator/tests, contract and CI integration. No runtime or hardware rollback is required.

## 10. Acceptance and package closure criteria

BKL-040 can close only when:

1. F4 read-model validates exactly against accepted F3 evidence;
2. fail-closed tests prove authority, timestamp, ordering, lineage, skew, unsupported evidence injection and command boundaries;
3. Developer Foundation, documentation and Word workflows pass on the exact head;
4. independent ARB approves the F4 consumer contract;
5. Release Quality returns Ready for Merge;
6. merge uses expected-head protection;
7. post-merge workflows are green on the actual merge SHA;
8. roadmap/closure artifacts are updated only after those validations are verified.

Runtime OAT and EAGLE actions are Not Applicable for this repository-only consumer projection.