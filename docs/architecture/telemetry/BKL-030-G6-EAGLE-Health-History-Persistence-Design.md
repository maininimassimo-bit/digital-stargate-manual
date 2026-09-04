# BKL-030 G6 — EAGLE Health History & Persistence Design

| Campo | Valore |
|---|---|
| Identificativo | `BKL-030-G6` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Stato | **Implemented and runtime-validated; independent review pending** |
| Data | 2026-09-04 |
| Target host | `EAGLE30154` |
| Upstream contract | `BKL-030-EAGLE-Health-Projection-Contract.md` |
| Runtime baseline | G1–G5 accepted; G6-A through G6-D verified |
| Runtime evidence | `evidence/BKL-030-G6-Runtime-OAT-2026-09-04.md` |
| Safety Authority | **No** |

## 1. Objective

G6 adds durable historical persistence downstream of the accepted read-only `DSG.EagleHostHealthCollector` projection. It preserves host-health evidence over time without changing collector authority, cadence semantics, severity policy or observatory safety behavior.

Canonical flow:

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
        +--> checkpoint metadata
        +--> cycle evidence
```

The history writer is downstream. A failure to persist history must never block or mutate the current realtime projection.

## 2. Governing invariants

G6 preserves these rules:

- collector remains non-elevated and read-only;
- no remediation, restart, process control, Windows Update action, USB reset or configuration write;
- local physical interlocks and Safety Authority remain independent;
- persisted history preserves signal evidence state, freshness quality, timestamps, source provenance, cadence class, reason and raw value;
- history does not manufacture `HEALTHY`, `DEGRADED` or `CRITICAL` while the current summary contract remains `UNKNOWN/POLICY_NOT_ACTIVATED`;
- historical aggregation does not replace raw evidence;
- malformed/unavailable input is fail-closed and cannot overwrite previously accepted valid history;
- writer is non-overlapping;
- no destructive retention is enabled.

## 3. Implemented source contract

The only authoritative G6 input is a successfully parsed projection conforming to `eagle-health.json` schema `1.0` and component `DSG.EagleHostHealthCollector` in `READ_ONLY` mode.

The serializer persists per-signal provenance including:

```text
history_schema_version
record_id
host
component
projection_schema_version
projection_correlation_id
projection_observed_at_utc
signal_id
signal_state
quality
observed_at_utc
fresh_until_utc
source
cadence_class
reason
data
retention_deletion_enabled
historical_records_deleted
```

G6 does not scrape operating-system sources independently.

## 4. Implemented persistence model

### 4.1 Signal-sample granularity

Persistence is signal-sample based. Logical identity is derived deterministically from:

```text
host + signal_id + observed_at_utc + source identity
```

`record_id` is a deterministic SHA-256 identity. Duplicate replay is skipped rather than appended.

### 4.2 Local storage

Implemented root:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\history\eagle-health\
    YYYY\
      MM\
        eagle-health-YYYY-MM.ndjson
    checkpoints\
      latest.json
    evidence\
      <cycle-evidence>.json
```

The writer validates NDJSON and uses temporary-file plus replace/move publication for a batch update. Existing malformed history is rejected rather than silently rewritten.

The current projection remains separate at:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json
```

## 5. Freshness semantics

Historical quality is persisted as emitted by the collector at observation time. Historical records are not retroactively rewritten from `CURRENT` to `STALE` merely because time passes.

## 6. Retention

No destructive retention policy is approved:

```text
RetentionDeletionEnabled = False
HistoricalRecordsDeleted = 0
```

The EAGLE pilot verified these values at runtime. AP-013C cleanup authority is not reused.

## 7. Failure and recovery model

Verified behavior includes:

- missing input: fail closed;
- unsupported schema: fail closed;
- partial valid signal set: persist only present signals, no synthesis;
- malformed existing history: reject and preserve it for diagnosis;
- write failure: do not alter unrelated valid history;
- duplicate sample: deterministic idempotent skip;
- concurrent execution: `SKIPPED_NON_OVERLAP` using a named mutex;
- checkpoint: operational resume metadata only, never a source from which health facts are inferred.

## 8. Workload protection

The writer is bounded and non-overlapping. G6 introduces no process-priority increase and no requirement for N.I.N.A., PHD2 or ASCOM to pause.

No permanent Scheduled Task or service was activated by the G6-D OAT. Permanent orchestration remains outside the accepted pilot evidence until separately governed.

## 9. Observability

Cycle evidence includes:

```text
run_id
started_at_utc
completed_at_utc
host
input_projection_observed_at_utc
segment_path
records_seen
records_appended
records_duplicate_skipped
records_rejected
write_failures
historical_records_deleted
retention_deletion_enabled
result
last_error
```

Writer success/failure does not infer overall host-health severity.

## 10. Runtime validation

Real EAGLE30154 pilot evidence is recorded in `evidence/BKL-030-G6-Runtime-OAT-2026-09-04.md`.

Verified first write:

```text
records_seen = 14
records_appended = 14
records_duplicate_skipped = 0
write_failures = 0
historical_records_deleted = 0
result = PASS
```

Measured first segment:

```text
14 records
13945 bytes
```

Verified identical replay:

```text
records_seen = 14
records_appended = 0
records_duplicate_skipped = 14
write_failures = 0
historical_records_deleted = 0
result = PASS
```

Segment remained 14 records / 13,945 bytes.

## 11. CI validation

PR #87 has verified green gates on the G6-C corrected baseline:

- Genera manuale Word — success;
- Validate documentation (no deploy) — success;
- Developer Foundation — success.

CI covers serializer, writer, malformed/missing input, schema rejection, partial signals, corrupted history, write failure, duplicate replay and distinct-execution-context non-overlap.

## 12. Security and safety

G6 persists only approved BKL-030 projection evidence and introduces no remote write API, Safety Authority function or remediation path.

The runtime pilot kept the production scientific-session import clone on `main` and used an isolated feature worktree.

## 13. Acceptance criteria status

| # | Criterion | Status |
|---|---|---|
| 1 | Versioned historical schema traceable to current projection | PASS |
| 2 | Append-only and duplicate-safe | PASS |
| 3 | Malformed/unavailable input fails closed | PASS |
| 4 | Interrupted/corrupt prior history cannot silently replace accepted history | PASS |
| 5 | History persistence cannot mutate realtime projection | PASS |
| 6 | Runtime storage overhead measured on EAGLE30154 | PASS — initial pilot baseline |
| 7 | Non-overlap demonstrated | PASS |
| 8 | No automated remediation/deletion | PASS |
| 9 | `HistoricalRecordsDeleted=0` in CI/runtime | PASS |
| 10 | CI/documentation gates green | PASS |
| 11 | Independent review before final closure | PENDING |

## 14. Out of scope / deferred

- portal charts/UX — G7;
- host-health severity thresholds;
- anomaly/trend detection — future BKL-038/BKL-036;
- MTBF/MTTR/SLO — BKL-043;
- configuration-drift baseline approval;
- automatic retention deletion;
- Safety Authority integration;
- remote remediation;
- permanent writer scheduling/service activation.

## 15. Disposition

**G6-A through G6-D are implemented and verified. G6-E is active.**

The package is ready for independent Architecture Review Board and release-quality review. BKL-030 G6 must not be declared complete until those independent reviews are recorded and any blocking findings are resolved.
