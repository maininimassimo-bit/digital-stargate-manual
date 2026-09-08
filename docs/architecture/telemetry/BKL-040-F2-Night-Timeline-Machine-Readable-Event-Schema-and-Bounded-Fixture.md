# BKL-040 F2 — Night Timeline Machine-Readable Event Schema & Bounded Fixture

| Field | Value |
|---|---|
| Package | BKL-040 — Night Timeline / Observatory Replay |
| Increment | F2 — Machine-Readable Event Schema + Bounded Fixture |
| Status | Proposed |
| Version | 1.0 |
| Date | 2026-09-08 |
| Baseline | `4a4d6b89b374e87ca7f945e7399b7e69f0c9ba87` |
| Upstream | BKL-040 F1 — Source Discovery & Temporal Contract |
| Authority | Projection only |
| Runtime impact | None |
| Safety impact | None |

## 1. Purpose and scope

F2 materializes the accepted F1 temporal contract as a bounded, machine-readable repository projection. It intentionally starts with one governed session and only event timestamps explicitly present in the session manifest. It does not parse or infer N.I.N.A., PHD2, CloudWatcher, SQM or EAGLE events yet.

## 2. Artifacts

- `schemas/night-timeline-replay.schema.json` — JSON Schema 2020-12 structural contract;
- `docs/data/night-timeline-replay.json` — bounded governed fixture;
- `.github/scripts/verify-night-timeline-replay.mjs` — normative semantic/source validator;
- `.github/scripts/test-night-timeline-replay.mjs` — fail-closed regression suite;
- `.github/workflows/developer-foundation.yml` — CI integration.

## 3. Current state

F1 established:

- `event_time_utc` as the canonical replay axis;
- explicit `PLACED | UNPLACED` semantics;
- `event_time_utc = null` for `UNPLACED` evidence;
- neutral deterministic source ordering via `BKL040-F1-SOURCE-ORDER-1`;
- prohibition on substituting file-modified, ingestion, commit, session-boundary, persistence or projection-production times for missing source event time;
- strict separation between historical replay and command/Safety Authority.

## 4. Target state

F2 provides an executable projection contract with these root invariants:

- `schema_version = 1.0`;
- `component = DSG.NightTimelineReplay`;
- `authority = projection`;
- exact accepted F1 baseline commit;
- `source_order_method_id = BKL040-F1-SOURCE-ORDER-1`;
- maximum two sessions and twenty events;
- explicit Citation and Provenance collections.

The initial fixture contains only session `2026-08-15_2026-08-16` and two events:

1. governed session start from `manifest.json#/start_local`;
2. governed session end from `manifest.json#/end_local`.

The UTC timestamps are exact normalizations of the source offsets and are validated against the manifest.

## 5. Architecture rules

### 5.1 Temporal placement

A `PLACED` event must have a valid UTC timestamp and a source timestamp whose instant is exactly equivalent. An `UNPLACED` event must have `event_time_utc = null`.

The validator rejects any attempt to manufacture a UTC time for missing/unparseable source timestamps.

### 5.2 No fallback timestamp inference

For `SESSION_PROJECTION`, the only accepted F2 event kinds are `SESSION_START` and `SESSION_END`, bound respectively to `start_local` and `end_local` of the governed manifest.

Manifest file `modified_local` values are provenance/file metadata and are not eligible event timestamps.

### 5.3 Neutral source ordering

The accepted initial mapping is:

- `NINA = 10`;
- `PHD2 = 20`;
- `CLOUDWATCHER = 30`;
- `SQM = 40`;
- `EAGLE_HEALTH = 50`;
- `SESSION_PROJECTION = 90`.

This mapping is a deterministic tie-break only. It carries no truth, lifecycle, Safety or source-authority precedence.

### 5.4 Authority and lineage

Replay remains `projection`. Each event must resolve its Citation and Provenance references. Provenance output must bind exactly to the event ID and input must match the governed source field.

### 5.5 Safety

F2 is historical/read-only and introduces no command path, device action, current Safety inference, automatic remediation, EAGLE runtime change or hardware behavior.

## 6. Validation model

The executable validator checks:

- closed root structure and bounded cardinality;
- exact baseline and source-order method;
- unique session/event/Citation/Provenance identities;
- source family/order consistency;
- `PLACED`/`UNPLACED` semantics;
- exact UTC normalization for session-boundary events;
- exact source-reference binding to the governed manifest fields;
- complete Citation/Provenance resolution and event binding;
- deterministic event ordering.

The fail-closed test suite includes authority promotion, invented timestamps, wrong source order, missing Citation/Provenance, invalid `UNPLACED` timestamps and bounds overflow.

## 7. Benefits and trade-offs

Benefits:

- makes F1 temporal semantics executable;
- provides a small, auditable reference fixture;
- proves exact source-to-event lineage before introducing multi-source parsing;
- prevents early semantic drift into inferred or file-time-based events.

Trade-off:

- the initial timeline is intentionally sparse. It does not yet represent the rich observing-night chronology expected from later N.I.N.A./PHD2/weather/SQM/EAGLE sources.

This is deliberate: source-specific parsers and timestamp contracts belong to F3 synchronization/reconciliation work, not F2 source invention.

## 8. Migration strategy

F2 is additive. Existing session manifests and source logs remain unchanged. Future event families may be added only when an exact source contract, timestamp locator and Citation/Provenance method are governed.

Rollback is a repository revert of the schema, fixture, validator/tests, workflow integration and this document.

## 9. Testing and validation impact

Required before merge:

1. Developer Foundation executes both new replay validator/test steps successfully;
2. documentation workflow succeeds;
3. Word generation succeeds;
4. independent ARB confirms temporal, authority and Safety preservation;
5. Release Quality returns Ready for Merge;
6. merge uses expected-head protection;
7. post-merge workflows are green on the actual merge SHA.

No runtime OAT is required for F2 because no runtime collector, parser, scheduler or device integration changes.

## 10. Traceability

| Requirement | Source | F2 realization |
|---|---|---|
| Canonical UTC axis | BKL-040 F1 §3 | schema + validator |
| `PLACED/UNPLACED` | BKL-040 F1 §3 | event contract + tests |
| Neutral source ordering | BKL-040 F1 §3.1 | source-order mapping + validator |
| No invented timestamps | BKL-040 F1 §3/§7 | manifest binding + negative tests |
| Citation/Provenance | BKL-040 F1 §4/§5 | explicit collections + validator |
| Historical read-only replay | BKL-040 F1 §6 | no runtime or command integration |

## 11. Open issues / future evolution

Deferred to later increments:

- exact parsers and timestamp binding for N.I.N.A.;
- exact parsers and timestamp binding for PHD2;
- CloudWatcher/SQM/EAGLE history event extraction;
- durable historical Power/Network/Safety sources;
- clock-skew classification;
- multi-source correlation and conflict visibility;
- consumer/read-model timeline/replay UI.

No deferred source may be fabricated into the F2 fixture.