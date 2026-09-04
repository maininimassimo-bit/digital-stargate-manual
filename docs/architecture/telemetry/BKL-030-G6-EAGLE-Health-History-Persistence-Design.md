# BKL-030 G6 — EAGLE Health History & Persistence Design

| Campo | Valore |
|---|---|
| Identificativo | `BKL-030-G6` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Stato | **Proposed for implementation** |
| Data | 2026-09-04 |
| Target host | `EAGLE30154` |
| Upstream contract | `BKL-030-EAGLE-Health-Projection-Contract.md` |
| Runtime baseline | G1–G5 accepted |
| Safety Authority | **No** |

## 1. Objective

G6 adds durable historical persistence downstream of the accepted read-only `DSG.EagleHostHealthCollector` projection. It must preserve host-health evidence over time without changing collector authority, cadence semantics, severity policy or observatory safety behavior.

The canonical flow is:

```text
DSG.EagleHostHealthCollector
        |
        | atomic current projection
        v
%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json
        |
        | read-only history ingestion
        v
DSG.EagleHealthHistoryWriter
        |
        +--> append-only historical records
        +--> bounded index / checkpoint metadata
        +--> evidence for analytics and future reliability views
```

The history writer is downstream. A failure to persist history must never block or mutate the current realtime projection.

## 2. Governing invariants

G6 SHALL preserve these rules:

- the collector remains non-elevated and read-only;
- no remediation, restart, process control, Windows Update action, USB reset or configuration write is introduced;
- local physical interlocks and Safety Authority remain independent;
- persisted history must preserve the original signal evidence state, freshness quality, timestamps, source provenance, cadence class, reason and raw value;
- historical persistence must not manufacture `HEALTHY`, `DEGRADED` or `CRITICAL` when the current contract remains `UNKNOWN/POLICY_NOT_ACTIVATED`;
- no historical aggregation may replace raw evidence;
- malformed or partial input is fail-closed and must not overwrite previously persisted valid history;
- persistence must not increase process priority over N.I.N.A./PHD2 or create overlapping write cycles.

## 3. Source contract

The only authoritative G6 input is a successfully parsed current projection conforming to the accepted `eagle-health.json` contract.

Minimum record provenance:

```text
schema_version
observed_at_utc
host
collector/component identity
projection correlation/run identity when present
signal id
cadence_class
source/provenance
quality
reason
value/raw payload
```

G6 SHALL NOT scrape independent operating-system sources in parallel with the collector. Source discovery and measurement stay in G1–G5.

## 4. Persistence model

### 4.1 Canonical record granularity

Persistence is **signal-sample based** rather than whole-file snapshot based. Each accepted current projection is normalized into independent historical signal records.

Logical key:

```text
host + signal_id + observed_at_utc + source identity
```

This makes history queryable without requiring the portal or analytics layer to reinterpret old projection files.

### 4.2 Append-only semantics

Historical records are append-only. Existing accepted records are not rewritten because a later sample changes state.

Duplicate ingestion of the same logical sample must be idempotent: it may be recognized and skipped, but it must not create conflicting duplicate facts.

### 4.3 Storage format

Initial implementation SHOULD use a local, line-oriented machine-readable history format under a dedicated Digital StarGate application-data history root. The exact physical format and file rotation implementation may be selected during implementation, provided it satisfies:

- append-only behavior;
- atomic publication/rotation;
- bounded recovery after interruption;
- schema/version field on every persisted record or segment;
- simple PowerShell 5.1-compatible read/write path;
- deterministic export to future analytics/warehouse stages;
- no dependency on network availability for local capture.

G6 does not approve a database engine, external cloud store or network share as a runtime dependency.

## 5. History root and separation

The implementation SHALL use an application-data history location separate from the current projection.

Logical layout:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\history\eagle-health\
    YYYY\
      MM\
        <history-segment>
        <history-segment>
    checkpoints\
    evidence\
```

The exact segment filename convention is an implementation detail, but it must be deterministic and UTC-based.

The current projection remains:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json
```

G6 must never rotate, move or delete that realtime projection.

## 6. Freshness and historical semantics

Historical quality records the quality observed at ingestion time. Later passage of time does not retroactively rewrite an old `CURRENT` historical sample to `STALE`.

Consumers may calculate age relative to query time, but the persisted record must preserve both:

- source/observation timestamp;
- quality as emitted by the collector at that observation.

This keeps historical truth distinct from current-state freshness.

## 7. Retention

No destructive retention policy is approved in this G6 baseline.

Therefore initial G6 behavior is:

```text
RetentionDeletionEnabled = False
HistoricalRecordsDeleted = 0
```

Storage growth must be measured during pilot/OAT. A later governed retention policy may define compaction or deletion only after measured capacity evidence and explicit approval.

This is separate from AP-013C transport cleanup and must not reuse AP-013C deletion authority.

## 8. Failure model

### Input unavailable

If `eagle-health.json` does not exist, cannot be read, or is invalid, the history writer records operational evidence/logging where possible but appends no synthetic health sample.

### Partial/malformed projection

Reject the malformed ingestion unit. Preserve previously persisted valid history.

### Duplicate sample

Treat as idempotent skip; do not create a second conflicting fact.

### Write failure

Do not truncate or corrupt the active history segment. Use temp/validate/atomic-replace semantics where a replace is required; append paths must have explicit recovery handling.

### Disk pressure

G6 may report persistence failure or capacity evidence but must not invent thresholds or auto-delete history. Automatic cleanup is prohibited in this baseline.

### Restart/crash

After host or process restart, ingestion resumes from persisted checkpoint/history evidence. No historical fact may be inferred solely because a checkpoint advanced.

## 9. Non-overlap and workload protection

The history writer must be bounded and non-overlapping. If a prior history cycle is still active, a new cycle must skip/coalesce rather than accumulate parallel processes.

It must remain lower priority than the imaging workload and must not require N.I.N.A., PHD2 or ASCOM to pause.

## 10. Observability

Each history cycle must expose machine-readable evidence including at least:

```text
run_id
started_at_utc
completed_at_utc
host
input_projection_observed_at_utc
records_seen
records_appended
records_duplicate_skipped
records_rejected
write_failures
historical_records_deleted = 0
result
last_error
```

No overall host health severity is inferred from writer success/failure.

## 11. Security and privacy

Persist only evidence already approved in the BKL-030 projection contract. Do not add usernames, secrets, tokens, command lines containing credentials or arbitrary file contents to history unless separately governed.

History files inherit local host access controls. G6 introduces no remote write API.

## 12. Delivery slices

### G6-A — History contract and serializer

- define versioned historical record schema;
- normalize current projection to signal records;
- implement deterministic identity/idempotency;
- unit tests for schema and malformed input.

### G6-B — Local append-only persistence

- create bounded local history writer;
- atomic/validated write behavior;
- checkpoint/recovery semantics;
- no deletion/retention automation.

### G6-C — CI and failure injection

Validate at minimum:

- nominal append;
- duplicate replay;
- missing input;
- malformed input;
- partial signal set;
- write denied/failure;
- interrupted write/recovery;
- non-overlap;
- schema upgrade rejection/compatibility behavior.

### G6-D — EAGLE runtime pilot

On `EAGLE30154` verify:

- history creation from real G5 projection;
- repeated samples remain idempotent where identical identity is replayed;
- storage growth is measured;
- collector realtime projection remains unaffected;
- no process overlap;
- N.I.N.A./PHD2 non-interference during an imaging-capable window when practical;
- `HistoricalRecordsDeleted=0`.

### G6-E — Acceptance and handoff

Preserve evidence, update backlog/roadmap only from verified runtime outcome, then request independent ARB/release-quality review before declaring G6 complete.

## 13. Acceptance criteria

G6 is ready for acceptance only when all are true:

1. historical schema is versioned and traceable to BKL-030 current projection;
2. persistence is append-only and duplicate-safe;
3. malformed/unavailable input fails closed;
4. interruption cannot corrupt previously accepted history;
5. history persistence failure cannot block or mutate realtime telemetry;
6. runtime storage overhead is measured on EAGLE30154;
7. non-overlap is demonstrated;
8. no automated remediation or deletion exists;
9. `HistoricalRecordsDeleted=0` is demonstrated in CI and runtime evidence;
10. CI and documentation gates are green;
11. independent review is completed before final closure.

## 14. Out of scope

G6 does not include:

- portal charts or UX (G7);
- overall health scoring or severity thresholds;
- anomaly/trend detection (future BKL-038/BKL-036);
- MTBF/MTTR/SLO calculations (BKL-043);
- configuration-drift baseline approval;
- automatic retention deletion;
- Safety Authority integration;
- remote remediation.

## 15. Disposition

**G6 architecture is ready to enter implementation through slices G6-A to G6-E.**

The next implementation step is G6-A: versioned historical record schema and serializer derived only from the accepted `eagle-health.json` projection contract.
