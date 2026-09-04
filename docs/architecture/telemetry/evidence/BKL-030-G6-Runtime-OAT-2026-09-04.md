# BKL-030 G6 — EAGLE Health History Runtime OAT — 2026-09-04

| Campo | Valore |
|---|---|
| Identificativo | `BKL-030-G6-OAT-2026-09-04` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Slice | G6-D — EAGLE runtime pilot |
| Host | `EAGLE30154` |
| Feature branch | `feature/bkl-030-g6-health-history-persistence` |
| Pilot worktree branch | `local/bkl-030-g6-pilot` |
| Pilot HEAD | `1c95f08b48fa2f3202fcac129625d4a50b2fecc5` |
| Operational runtime branch | `main` |
| Operational runtime HEAD during pilot | `ad9348314ced2660c91b448527e56e2e8a515861` |
| Safety Authority | **No** |
| Automatic remediation | **False** |
| Destructive retention | **Disabled** |

## 1. Purpose

Record verified runtime evidence for BKL-030 G6 historical persistence on the real EAGLE host while keeping the production session-import runtime on `main` and isolating the pilot in a separate Git worktree.

## 2. Runtime isolation

The production runtime remained:

```text
C:\DigitalStarGate\digital-stargate-manual-ap14-runtime
branch: main
HEAD: ad9348314ced2660c91b448527e56e2e8a515861
working tree: clean
```

The pilot used:

```text
C:\DigitalStarGate\digital-stargate-bkl030-g6-pilot
branch: local/bkl-030-g6-pilot
HEAD: 1c95f08b48fa2f3202fcac129625d4a50b2fecc5
working tree: clean at setup
```

This prevented the G6 pilot from changing the branch used by the automatic scientific-session import runtime.

## 3. G5 projection refresh

The real collector was executed read-only using:

```text
scripts\telemetry\Export-EagleHostHealth.ps1
CadenceClass: all
```

Verified projection:

```text
Computer             : EAGLE30154
SchemaVersion        : 1.0
Component            : DSG.EagleHostHealthCollector
ObservedAtUtc        : 2026-09-04T16:37:19.443Z
FreshUntilUtc        : 2026-09-04T16:39:19.443Z
Quality              : CURRENT
CadenceClass         : MIXED
CollectorMode        : READ_ONLY
AutomaticRemediation : False
NonOverlap           : MUTEX_SKIP
```

The canonical current projection remained:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json
```

## 4. First real history write

History root:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\history\eagle-health
```

Created monthly segment:

```text
2026\09\eagle-health-2026-09.ndjson
```

First runtime cycle evidence:

```text
records_seen               = 14
records_appended           = 14
records_duplicate_skipped  = 0
records_rejected           = 0
write_failures             = 0
historical_records_deleted = 0
retention_deletion_enabled = false
result                     = PASS
```

Measured segment after first write:

```text
Historical records = 14
Segment bytes       = 13945
```

Checkpoint confirmed:

```text
schema_version = 1.0
component = DSG.EagleHealthHistoryWriter
host = EAGLE30154
input_projection_observed_at_utc = 2026-09-04T16:37:19.443Z
records_seen = 14
records_appended = 14
records_duplicate_skipped = 0
historical_records_deleted = 0
retention_deletion_enabled = false
```

## 5. Runtime idempotency replay

The same projection was written again without refreshing the collector.

Second runtime cycle evidence:

```text
records_seen               = 14
records_appended           = 0
records_duplicate_skipped  = 14
records_rejected           = 0
write_failures             = 0
historical_records_deleted = 0
retention_deletion_enabled = false
result                     = PASS
```

The persisted segment remained unchanged:

```text
Historical records = 14
Segment bytes       = 13945
```

This demonstrates runtime duplicate safety for identical signal identities.

## 6. CI evidence

PR #87 executed the G6 CI package on the final G6-C correction commit.

Verified workflow conclusions:

```text
Genera manuale Word                 success
Validate documentation (no deploy)  success
Developer Foundation                success
```

Within Developer Foundation, G6-A serializer, G6-B writer and G6-C failure-injection coverage completed successfully after correcting the non-overlap test to simulate a distinct PowerShell execution context.

G6-C covers:

- missing input fail-closed;
- unsupported schema rejection;
- partial signal set without synthetic records;
- corrupt existing segment rejection;
- write failure preservation of unrelated valid history;
- non-overlap skip with a distinct execution context;
- permanent no-delete invariants.

## 7. Safety and deletion disposition

The pilot introduced no Safety Authority behavior and no automatic remediation.

Verified deletion invariants in both CI and real runtime:

```text
retention_deletion_enabled = false
historical_records_deleted = 0
```

No AP-013C transport cleanup authority is reused by G6.

## 8. Storage observation

The first persisted real projection produced:

```text
14 signal records
13945 bytes total
~996 bytes per persisted signal record at this sample
```

This is an initial single-projection measurement only. It is sufficient to validate bounded persistence mechanics, but not to approve any future retention/deletion policy. Long-term storage growth remains a future operational measurement concern.

## 9. Acceptance matrix

| Criterion | Runtime/CI evidence | Result |
|---|---|---|
| Versioned historical schema | history schema `1.0` | PASS |
| Traceable to current projection | projection schema/component/timestamps preserved | PASS |
| Append-only / duplicate-safe | second replay appended `0`, skipped `14` | PASS |
| Malformed/unavailable fail closed | G6-C CI | PASS |
| Existing history protected from corruption | G6-C CI | PASS |
| Realtime projection remains separate | dedicated history root; current projection retained | PASS |
| Runtime storage overhead measured | 14 records / 13,945 bytes | PASS for pilot baseline |
| Non-overlap | CI distinct execution context; writer mutex | PASS |
| No remediation | `automatic_remediation=False` | PASS |
| No retention deletion | deleted `0`; retention disabled | PASS |
| CI/documentation gates | all PR workflows green | PASS |
| Independent architecture review | required before closure | PENDING |

## 10. Pilot disposition

**G6-D runtime pilot: PASS.**

G6 is ready for G6-E independent review and governance closure. No permanent Scheduled Task/service for the history writer is approved by this OAT. Any permanent cadence/orchestration remains a separately governed operational decision.
