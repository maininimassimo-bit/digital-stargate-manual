# BKL-040 F1 — Night Timeline / Observatory Replay Source Discovery & Temporal Contract

| Field | Value |
|---|---|
| Package | BKL-040 — Night Timeline / Observatory Replay |
| Increment | F1 — Source Discovery & Temporal Contract |
| Status | Proposed |
| Date | 2026-09-08 |
| Baseline | `07f2ab1ca0c2d43fdef6595472cef894d3587bb1` |
| Authority | Projection only |
| Runtime impact | None |
| Safety impact | None |

## 1. Purpose

Define the bounded source inventory and temporal semantics required to build a synchronized, read-only replay of an observing night. F1 does not implement a replay engine, UI, database, event bus or device command path.

The governed roadmap describes BKL-040 as a synchronized timeline across N.I.N.A., PHD2, CloudWatcher, SQM, Power, Network, Safety, EAGLE health and session events.

## 2. Repository-truth source inventory

### 2.1 Verified governed sources

1. **Session package** — `data/sessions/YYYY/MM/<session_id>/` is the accepted historical session envelope. Real repository sessions contain `manifest.json`, `normalized/` and `raw/`; the inspected M27 session contains raw `nina/`, `phd2/` and `weather/` trees.
2. **N.I.N.A. raw evidence** — session-scoped N.I.N.A. logs under `raw/nina/`; source authority remains raw session evidence.
3. **PHD2 raw evidence** — session-scoped PHD2 logs under `raw/phd2/`; source authority remains raw session evidence.
4. **Weather / CloudWatcher evidence** — session-scoped weather evidence under `raw/weather/`; CloudWatcher remains evidence/telemetry and not Safety Authority.
5. **SQM scientific history** — BKL-029 defines canonical SQM history and scientific-session aggregation. Existing repository baseline records `%LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-history.ndjson` as the local history source and `raw/sqm/sqm-history.ndjson` plus `raw/sqm/sqm-summary.json` as session evidence when materialized.
6. **EAGLE health history** — BKL-030 defines a dedicated historical persistence contract consumed by the Observatory Status portal projection. It remains health telemetry, not Safety Authority.
7. **Session catalog / normalized projections** — accepted scientific session and observation projections provide stable session identity and bounded normalized facts. They are projections, not replacements for raw evidence.

### 2.2 Candidate sources requiring later executable binding

The roadmap also names **Power, Network, Safety and session events**. Their current real-time projections are known, but F1 does not assume a durable historical source unless repository evidence explicitly binds one. These sources therefore remain `candidate` for F2 until an exact historical file/contract and timestamp semantics are verified.

## 3. Temporal model

BKL-040 uses a single canonical replay axis:

`event_time_utc`

Rules:

- UTC is the canonical comparison domain.
- Original source timestamp and timezone/offset, when present, must be retained as evidence.
- Ingestion/commit time must never replace source event time.
- Missing or unparsable source time fails closed for synchronized placement; the evidence may remain visible as `UNPLACED` but must not be assigned an invented timestamp.
- Multiple events with the same timestamp are ordered deterministically by `source_priority`, then stable `source_event_id`.
- Clock skew may be measured later but F1 does not authorize automatic timestamp rewriting.

## 4. Replay event envelope

A future machine-readable F2 projection must preserve, at minimum:

- `replay_event_id`;
- `session_id`;
- `event_time_utc`;
- `source_timestamp_raw`;
- `source_type`;
- `source_authority`;
- `event_kind`;
- `summary`;
- `source_ref`;
- Citation/Provenance refs;
- lifecycle/quality state;
- optional correlation identifiers already present in source evidence.

No replay event may increase the authority of its source.

## 5. Source precedence and conflicts

Replay is a correlation projection, not an authority arbitration layer.

If two sources describe similar facts with different values or timestamps:

1. both events remain visible;
2. source authority remains explicit;
3. the consumer must not silently merge them into one fact;
4. any derived correlation must carry Citation/Provenance and a governed method identifier;
5. Safety-related observations remain observational evidence only unless produced by the local Safety Authority itself.

## 6. Safety boundary

BKL-040 is strictly historical/read-only.

It must not:

- open/close the roof;
- move or park the mount;
- switch power;
- change router/network state;
- acknowledge/bypass Safety;
- replay commands against real devices;
- convert historical Safety observations into present-time Safety Authority.

A future UI may visually replay what happened; it may not execute what happened.

## 7. Bounded F1 scope

F1 accepts only source discovery and semantics. It does not authorize broad repository ingestion.

The first executable F2 fixture should use one or two already governed sessions and only source families with verified historical evidence. Candidate Power/Network/Safety/session-event histories must remain absent until exact durable sources are proven.

## 8. Migration strategy

1. F1 — source inventory and temporal contract.
2. F2 — bounded machine-readable event schema + fixture over verified historical sources.
3. F3 — deterministic multi-source synchronization, conflict/skew classification and Citation/Provenance validation.
4. F4 — consumer/read-model projection suitable for a timeline/replay UI, followed by package closure.

Each increment is additive and reversible by repository revert.

## 9. Acceptance criteria for F1

- repository source inventory distinguishes verified historical evidence from candidates;
- canonical UTC temporal semantics are explicit;
- raw/source time is preserved and no timestamp is invented;
- authority and conflict rules are explicit;
- historical replay is explicitly separated from command execution and present-time Safety Authority;
- downstream F2 scope is bounded to verified sources and governed sessions;
- exact-head CI, independent ARB and Release Quality are required before merge.

## 10. Open issues for F2

- exact durable historical source for Power;
- exact durable historical source for Network;
- exact durable historical source for local Safety observations;
- exact durable historical source/schema for generic session events;
- clock-skew measurement method across N.I.N.A., PHD2, CloudWatcher/SQM and EAGLE health;
- bounded session selection for the initial executable fixture.

Until these are resolved, F2 must not fabricate missing historical channels.