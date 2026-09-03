# BKL-030 — EAGLE Health Projection Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-030-G2 |
| Stato | **ARCHITECTURE READY — contract and provenance governed; implementation pending G3** |
| Data | 2026-09-03 |
| Target projection | `%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json` |
| Producer target | `DSG.EagleHostHealthCollector` |
| Safety authority | **Outside scope — local physical interlocks remain authoritative** |

## 1. Purpose

Define the machine-readable contract for host-level EAGLE health telemetry using the governed G1 source inventory, D3 overhead evidence and D4 failure model. G2 defines data/provenance/freshness semantics; it does not claim a running collector.

## 2. Design rules

1. Raw observed evidence is separate from derived classification.
2. Every signal carries `state`, `quality`, `observed_at_utc`, `fresh_until_utc`, `source`, `cadence_class`, optional `reason`, and `data`.
3. `CURRENT`, `STALE`, `UNKNOWN` describe evidence freshness/availability, not severity.
4. `HEALTHY`, `DEGRADED`, `CRITICAL`, `UNKNOWN` require a separately governed classification policy and explicit reasons.
5. No health threshold is implicit in this schema.
6. Missing values are `null`; no synthetic substitute is allowed.
7. Source failure is isolated to the affected signal where possible.
8. The collector remains non-elevated/read-only and cannot remediate host/equipment state.
9. No projection field authorizes equipment or Safety actions.
10. Full monolithic D1 discovery is not a fast polling design.

## 3. Top-level contract

```json
{
  "schema_version": "1.0",
  "component": "DSG.EagleHostHealthCollector",
  "computer": "EAGLE30154",
  "observed_at_utc": "...",
  "fresh_until_utc": "...",
  "quality": "CURRENT",
  "correlation_id": "...",
  "summary": {
    "state": "UNKNOWN",
    "reasons": [
      {"code":"POLICY_NOT_ACTIVATED","signal":null,"severity":null,"evidence":null}
    ]
  },
  "signals": {},
  "diagnostics": {
    "cycle_overrun": false,
    "failed_probe_count": 0
  }
}
```

Top-level `observed_at_utc` is the publication cycle observation time. `fresh_until_utc` must be derived by implementation from a governed cadence/freshness policy; G2 deliberately does not invent numeric durations. A current collector may publish raw CURRENT signals while `summary.state` remains `UNKNOWN` until severity policy is activated.

## 4. Common signal envelope and provenance

```json
{
  "state": "OBSERVED",
  "quality": "CURRENT",
  "observed_at_utc": "...",
  "fresh_until_utc": "...",
  "source": "Win32_LogicalDisk",
  "cadence_class": "MEDIUM",
  "reason": null,
  "data": {}
}
```

Allowed `state`: `OBSERVED`, `UNAVAILABLE`, `NOT_SUPPORTED`, `UNKNOWN`.

Allowed `quality`: `CURRENT`, `STALE`, `UNKNOWN`.

Allowed `cadence_class`: `FAST`, `MEDIUM`, `SLOW_ON_CHANGE`.

`source` names the actual source/adapter used for the signal. Composite signals must preserve enough provenance to distinguish their constituent sources.

## 5. Governed signal map

| Signal | Source/provenance | Cadence class | Contract status |
|---|---|---|---|
| `cpu` | `Win32_Processor` | FAST | verified raw topology/load |
| `memory` | `Win32_OperatingSystem` / CIM | FAST | verified raw capacity/free |
| `processes` | Windows process table | FAST | verified contextual presence |
| `plugin_heartbeat` | N.I.N.A. telemetry projection | FAST | correlation only |
| `storage.capacity` | `Win32_LogicalDisk` | MEDIUM | verified size/free/ratio |
| `uptime` | OS boot time + collector arithmetic | MEDIUM | verified |
| `time_sync` | `w32tm` + Windows Time service | MEDIUM | verified source; service may be inactive |
| `log_sources` | filesystem metadata | MEDIUM | verified |
| `usb_com` | PnP + supplemental `Win32_SerialPort` | MEDIUM | governed composite |
| `storage.physical` | `Get-PhysicalDisk` | SLOW_ON_CHANGE | verified aggregate physical health |
| `storage.reliability` | `Get-StorageReliabilityCounter` | SLOW_ON_CHANGE | optional/unavailable non-elevated |
| `event_log` | System/Application Event Log | SLOW_ON_CHANGE | verified; provider policy pending |
| `scheduled_tasks` | Task Scheduler read API | SLOW_ON_CHANGE | verified raw state/result |
| `pending_reboot` | bounded registry evidence | SLOW_ON_CHANGE | verified raw evidence |
| `windows_update` | service state | SLOW_ON_CHANGE | verified read-only |
| `configuration_drift` | future baseline manifest | SLOW_ON_CHANGE | UNKNOWN until baseline approved |

No numeric cadence is accepted by G2. G3 must make cadence configurable and non-overlapping, then G5 OAT must demonstrate non-interference during imaging.

## 6. Storage contract — capacity and physical health are separate

```json
{
  "capacity": {
    "logical_disks": [
      {
        "device_id": "C:",
        "volume_name": null,
        "filesystem": "NTFS",
        "size_bytes": 223397015552,
        "free_bytes": 1500758016,
        "free_ratio": 0.0067,
        "free_pct": 0.67
      }
    ]
  },
  "physical": {
    "disks": [
      {
        "friendly_name": "KINGSTON SA400S37960G",
        "media_type": "SSD",
        "bus_type": "SATA",
        "health_status": "Healthy",
        "operational_status": ["OK"],
        "size_bytes": 960197124096
      }
    ]
  },
  "reliability": {
    "available": false,
    "temperature_c": null,
    "wear_pct": null,
    "read_errors_total": null,
    "write_errors_total": null,
    "power_on_hours": null,
    "reason": "UNAVAILABLE_NON_ELEVATED"
  }
}
```

`free_bytes`, `free_ratio` and `free_pct` are mandatory descriptive capacity fields for each observed logical disk. Capacity pressure is not inferred from physical `HealthStatus`. Conversely `Healthy/OK` physical evidence must not hide low logical free space. No storage severity threshold is defined by G2.

## 7. Remaining domain data contracts

### CPU
`model`, `physical_cores`, `logical_processors`, `max_clock_mhz`, `load_pct`; optional window metrics remain null until implemented. `temperature_c` remains null until a verified source exists.

### Memory
`total_physical_bytes`, `available_physical_bytes`, `available_ratio`; commit/pressure fields remain optional/null until governed.

### Uptime
`last_boot_at_utc`, `uptime_seconds`, `unexpected_reboot_observed`. Unexpected reboot cannot be inferred from uptime alone.

### Time sync
`service_state`, `time_source`, `stratum`, `last_successful_sync_utc`, `offset_ms`, `command_available`. No fabricated offset when service/query cannot provide it.

### Event Log
Bounded normalized events: `log_name`, UTC time, `event_id`, `level`, `provider`, optional application/fingerprint. Full unbounded event messages are excluded. Raw Windows Error counts are not host severity.

### Processes
Per candidate: name, running, pid, start UTC, working set, total CPU, optional verified executable path. `running=false` is contextual evidence only.

### Scheduled Tasks
Task name/path/state, last/next run UTC and raw `last_task_result`; `result_classification` remains null until task-specific mapping is governed.

### Log sources
Source id/path, exists, length, last-write UTC. Metadata only unless another contract explicitly governs content parsing.

### USB/COM
PnP devices plus supplemental serial-port rows and reconciliation/provenance. Zero `Win32_SerialPort` rows cannot override observed PnP COM presence.

### Pending reboot
Raw CBS/WU/PendingFileRename indicators plus nullable `reboot_required`. No automatic reboot action.

### Windows Update
Service state/start type and only passive available metadata. Collector must not trigger scan/install/service start.

### Configuration drift
`baseline_id`, `baseline_version`, observed/drift items and `status`. Remains UNKNOWN until baseline manifest exists; no auto-remediation.

### Plugin heartbeat
Projection path/existence and the projection's observed/freshness/quality fields; plugin version only from verified metadata.

## 8. Freshness and failure semantics

Per D4:

```text
valid sample before fresh_until_utc -> CURRENT
valid sample after fresh_until_utc  -> STALE
no valid/readable sample            -> UNKNOWN
```

A single probe failure yields `UNAVAILABLE/UNKNOWN` for that signal with a bounded reason while other probes continue. The last valid canonical projection is retained on serialization/write failure and ages naturally toward STALE. G3 must use atomic publication and prevent overlapping cycles.

Required reason-code vocabulary for implementation baseline includes at least: `SOURCE_UNAVAILABLE`, `UNAVAILABLE_NON_ELEVATED`, `MALFORMED_SOURCE`, `TIMEOUT`, `SOURCE_QUERY_FAILED`, `POLICY_NOT_ACTIVATED`, `BASELINE_NOT_DEFINED`. G3/G4 may extend this only with documented stable codes.

## 9. Summary classification

Until a governed severity/threshold policy exists:

```json
{"state":"UNKNOWN","reasons":[{"code":"POLICY_NOT_ACTIVATED","signal":null,"severity":null,"evidence":null}]}
```

Raw telemetry may still be CURRENT. `UNKNOWN` is not `CRITICAL`; `STALE` is not `HEALTHY`; physical disk `Healthy` is source evidence, not overall host health.

## 10. Security and safety

Do not serialize credentials/tokens/API keys, wholesale environment/registry exports, arbitrary file contents, network secrets or unbounded Event Log messages. Collector failure or host-health state cannot command N.I.N.A., PHD2, ASCOM, dome, mount, power, router, Windows Update, reboot or Safety Authority.

`eagle-health.json` is a source projection, not the canonical Observatory Status source of truth. Any later `systems.eagle` adapter must preserve the independent `safety` boundary.

## 11. G2 acceptance

G2 architecture acceptance criteria are satisfied by this contract because:

1. every baseline field/domain maps to G1 verified/composite/optional/open-gap provenance;
2. storage capacity and physical disk health are explicitly independent;
3. cadence classes are defined without unsupported numeric intervals;
4. freshness and failure semantics align with D4;
5. no actuator command or privilege elevation is required;
6. summary severity remains disabled until separately governed;
7. implementation obligations for isolation, non-overlap and atomic publication are explicit.

**Disposition: G2 ARCHITECTURE READY. Proceed to G3 collector implementation; runtime acceptance remains pending G4/G5.**
