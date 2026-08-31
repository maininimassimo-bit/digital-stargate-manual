# BKL-030 — EAGLE Health Projection Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-030-G2 |
| Stato | **Planning contract — implementation blocked until BKL-029 closure** |
| Data | 2026-08-31 |
| Target projection | `%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json` |
| Producer target | `DSG.EagleHostHealthCollector` |
| Safety authority | **Outside scope — local physical interlocks remain authoritative** |

## 1. Purpose

Define the machine-readable contract for host-level EAGLE health telemetry using only sources already demonstrated or explicitly classified during D1/D2 discovery on `EAGLE30154`.

This contract is intentionally separate from:

- N.I.N.A. equipment telemetry;
- the canonical Observatory Status projection;
- the future Observatory Health Score (BKL-036);
- Safety Authority;
- AI/anomaly analytics.

No producer implementation or acceptance is declared by this document.

## 2. Design rules

1. Preserve raw observed evidence separately from derived classification.
2. Every signal carries its own `quality`, `observed_at_utc`, `fresh_until_utc`, `source` and optional `reason`.
3. `CURRENT`, `STALE` and `UNKNOWN` describe evidence freshness/availability only.
4. `HEALTHY`, `DEGRADED`, `CRITICAL`, `UNKNOWN` are summary classifications and must always include explicit reasons.
5. No classification threshold is implicit in this schema.
6. A source access failure degrades only the affected signal unless a future policy marks that signal mandatory.
7. Missing values are `null`; no synthetic substitute is allowed.
8. The projection must never contain credentials, tokens, secrets or full sensitive configuration payloads.
9. The collector is observational/read-only. No state in this projection may authorize equipment or safety actions.
10. Heavy trend/forecast/AI analysis remains downstream.

## 3. Top-level contract

```json
{
  "schema_version": "1.0",
  "component": "DSG.EagleHostHealthCollector",
  "computer": "EAGLE30154",
  "observed_at_utc": "2026-08-31T00:00:00Z",
  "fresh_until_utc": "2026-08-31T00:02:00Z",
  "quality": "CURRENT",
  "correlation_id": "00000000-0000-0000-0000-000000000000",
  "summary": {
    "state": "UNKNOWN",
    "reasons": []
  },
  "signals": {},
  "diagnostics": {}
}
```

### Top-level field semantics

| Field | Required | Semantics |
|---|---|---|
| `schema_version` | yes | Versioned projection contract |
| `component` | yes | Fixed producer identity `DSG.EagleHostHealthCollector` |
| `computer` | yes | Observed Windows host |
| `observed_at_utc` | yes | Collector sample timestamp |
| `fresh_until_utc` | yes | Projection freshness boundary |
| `quality` | yes | `CURRENT / STALE / UNKNOWN` for the projection as a whole |
| `correlation_id` | yes | Sample/run correlation identifier |
| `summary.state` | yes | `HEALTHY / DEGRADED / CRITICAL / UNKNOWN` only when governed classification exists |
| `summary.reasons` | yes | Machine-readable reason list supporting the summary state |
| `signals` | yes | Per-domain observed evidence |
| `diagnostics` | yes | Collector/source diagnostics, never Safety authority |

Until threshold/severity policy is approved, a prototype collector may emit `summary.state = UNKNOWN` while still publishing `CURRENT` raw signals.

## 4. Common signal envelope

Every signal must implement the following envelope:

```json
{
  "state": "OBSERVED",
  "quality": "CURRENT",
  "observed_at_utc": "...",
  "fresh_until_utc": "...",
  "source": "...",
  "reason": null,
  "data": {}
}
```

Allowed evidence states for baseline use:

- `OBSERVED` — source read succeeded and raw data is available;
- `UNAVAILABLE` — source exists but cannot currently provide data;
- `NOT_SUPPORTED` — source capability is not exposed on this host;
- `UNKNOWN` — result cannot be determined safely.

`state` is not a severity classification.

## 5. Signal contracts

### 5.1 `storage`

Source basis: `Win32_LogicalDisk`, `Get-PhysicalDisk`, optional reliability counters.

```json
{
  "logical_disks": [
    {
      "device_id": "C:",
      "volume_name": "EAGLE3",
      "filesystem": "NTFS",
      "size_bytes": 223397015552,
      "free_bytes": 4335616000,
      "free_ratio": 0.0194
    }
  ],
  "physical_disks": [
    {
      "friendly_name": "KINGSTON SA400S37960G",
      "media_type": "SSD",
      "bus_type": "SATA",
      "health_status": "Healthy",
      "operational_status": ["OK"],
      "size_bytes": 960197124096
    }
  ],
  "reliability": {
    "available": false,
    "temperature_c": null,
    "temperature_max_c": null,
    "wear_pct": null,
    "read_errors_total": null,
    "write_errors_total": null,
    "power_on_hours": null,
    "reason": "UNAVAILABLE_NON_ELEVATED"
  }
}
```

Rules:

- `free_ratio` is descriptive, not a severity threshold.
- Aggregate `HealthStatus` from Windows may be preserved as raw evidence but does not replace detailed SMART evidence.
- Detailed reliability values remain `null` when unavailable.

### 5.2 `memory`

Source basis: `Win32_OperatingSystem` / bounded performance counters.

```json
{
  "total_physical_bytes": 12543135744,
  "available_physical_bytes": 0,
  "available_ratio": null,
  "commit_used_bytes": null,
  "commit_limit_bytes": null,
  "memory_pressure": null
}
```

`memory_pressure` remains `null` until a governed calculation/policy is defined.

### 5.3 `cpu`

Source basis: `Win32_Processor` and future lightweight counters.

```json
{
  "model": "Intel(R) Celeron(R) J4005 CPU @ 2.00GHz",
  "physical_cores": 2,
  "logical_processors": 2,
  "max_clock_mhz": 2001,
  "load_pct": 21.0,
  "window_avg_pct": null,
  "window_peak_pct": null,
  "temperature_c": null
}
```

No temperature field may be populated until a verified host source is identified.

### 5.4 `uptime`

```json
{
  "last_boot_at_utc": "...",
  "uptime_seconds": 0,
  "unexpected_reboot_observed": null
}
```

`unexpected_reboot_observed` requires historical comparison or event evidence and must not be inferred from uptime alone.

### 5.5 `time_sync`

Discovery evidence showed `w32tm` available while Windows Time service was stopped.

```json
{
  "service_state": "STOPPED",
  "time_source": null,
  "stratum": null,
  "last_successful_sync_utc": null,
  "offset_ms": null,
  "command_available": true
}
```

Rules:

- Never infer clock accuracy from wall-clock continuity.
- When service/query cannot provide a valid offset, `offset_ms = null`.

### 5.6 `event_log`

Source basis: Windows `System` and `Application` logs.

```json
{
  "window_start_utc": "...",
  "window_end_utc": "...",
  "critical_count": 0,
  "error_count": 0,
  "events": [
    {
      "log_name": "Application",
      "time_created_utc": "...",
      "event_id": 1000,
      "level": "Error",
      "provider": "Application Error",
      "application": "EagleManager.exe",
      "fingerprint": null
    }
  ]
}
```

The projection should not copy entire verbose Windows event messages by default. Preserve normalized fields and optionally a bounded/sanitized summary or fingerprint. Provider/event policy must distinguish observatory-relevant failures from unrelated Windows noise such as TPM/system-restore events.

### 5.7 `processes`

```json
{
  "items": [
    {
      "name": "NINA",
      "running": true,
      "pid": 7800,
      "started_at_utc": "...",
      "working_set_bytes": 403259392,
      "cpu_total_seconds": 1689.09,
      "executable_path": "C:\\Program Files\\N.I.N.A. - Nighttime Imaging 'N' Astronomy\\NINA.exe"
    }
  ]
}
```

Baseline candidates include N.I.N.A., PHD2, AAG CloudWatcher, ASCOM CloudWatcher Server, TS Shelter and verified Digital StarGate processes. `running = false` is evidence only; it does not automatically mean failure because process expectation depends on operational context.

### 5.8 `scheduled_tasks`

```json
{
  "items": [
    {
      "task_name": "Digital StarGate - Daily Session Upload",
      "task_path": "\\",
      "state": "Ready",
      "last_run_at_utc": "...",
      "last_task_result": 1,
      "next_run_at_utc": "...",
      "result_classification": null
    }
  ]
}
```

`result_classification` remains `null` until Task Scheduler result-code semantics are explicitly governed per task.

### 5.9 `log_sources`

```json
{
  "items": [
    {
      "source_id": "cloudwatcher-csv",
      "path": "C:\\Users\\PrimaLuceLab\\Documents\\CloudWatcher\\CloudWatcher.csv",
      "exists": true,
      "length_bytes": 241741030,
      "last_write_at_utc": "..."
    }
  ]
}
```

Known source candidates include CloudWatcher, ASCOM, N.I.N.A., PHD2 and Digital StarGate runtime logs. Absence/freshness policy is source-specific and must be explicit.

### 5.10 `usb_com`

```json
{
  "usb_devices": [
    {
      "name": "USB Serial Converter",
      "status": "OK",
      "manufacturer": "FTDI",
      "device_id": "USB\\VID_0403&PID_6001\\..."
    }
  ],
  "serial_ports": [],
  "source_reconciliation": "REQUIRED"
}
```

D1/D2 observed COM-related PnP devices while `Win32_SerialPort` returned no rows. Until reconciled, serial-port completeness must not be asserted.

### 5.11 `pending_reboot`

```json
{
  "cbs_reboot_pending": false,
  "windows_update_reboot_required": false,
  "pending_file_rename_present": true,
  "pending_file_rename_count": null,
  "reboot_required": null
}
```

`reboot_required` remains `null` until deterministic policy exists; `PendingFileRenameOperations` alone is raw evidence, not an automatic mandatory reboot decision.

### 5.12 `windows_update`

```json
{
  "service_name": "wuauserv",
  "service_state": "Stopped",
  "start_type": "Manual",
  "pending_update_count": null,
  "last_scan_at_utc": null
}
```

The collector must never start the service or trigger update scans/installations solely to populate telemetry.

### 5.13 `configuration_drift`

```json
{
  "baseline_id": null,
  "baseline_version": null,
  "observed_items": [],
  "drift_items": [],
  "status": "UNKNOWN"
}
```

This signal remains `UNKNOWN` until a governed baseline manifest is approved. No auto-remediation is allowed.

### 5.14 `plugin_heartbeat`

This signal correlates host health with the already-existing N.I.N.A. telemetry projection without moving host collection into the plugin.

```json
{
  "projection_path": "%LOCALAPPDATA%\\DigitalStarGate\\telemetry\\nina-observatory-status.json",
  "exists": true,
  "observed_at_utc": "...",
  "fresh_until_utc": "...",
  "quality": "CURRENT",
  "plugin_version": null
}
```

Plugin version may be populated only from a verified DLL/file metadata source or projection field.

## 6. Projection freshness model

The producer must assign freshness explicitly. Initial implementation should use per-signal cadences rather than one universal cadence.

Recommended classes for pilot design only:

- fast: CPU/memory/process/plugin heartbeat;
- medium: storage/log-source/task state;
- slow: Event Log summaries, pending reboot/update, drift, SMART.

Actual intervals are not fixed by this contract and must be measured in D3 overhead pilot.

Top-level `quality` rules:

- `CURRENT`: collector sample itself is fresh;
- `STALE`: collector output exists but exceeded freshness;
- `UNKNOWN`: collector cannot produce a valid projection.

Top-level quality must not collapse every child source failure into `UNKNOWN` if the collector itself is functioning.

## 7. Summary classification contract

The summary object is deliberately evidence-driven:

```json
{
  "state": "UNKNOWN",
  "reasons": [
    {
      "code": "POLICY_NOT_ACTIVATED",
      "signal": null,
      "severity": null,
      "evidence": null
    }
  ]
}
```

Future reason object:

| Field | Purpose |
|---|---|
| `code` | Stable machine-readable reason |
| `signal` | Signal responsible for classification |
| `severity` | Governed classification severity |
| `evidence` | Bounded observed value(s) supporting the reason |

Until policy thresholds are approved, the collector must not label the host `HEALTHY`, `DEGRADED` or `CRITICAL` solely from developer assumptions.

## 8. Canonical Observatory Status integration

`eagle-health.json` is a **source projection**, not the portal source of truth. A future canonical adapter may map it into Observatory Status as a dedicated `systems.eagle` (or equivalent repository-approved name) while preserving the current structure and keeping `safety` separate.

Target shape, subject to integration review:

```json
{
  "systems": {
    "eagle": {
      "state": "UNKNOWN",
      "observed_at_utc": "...",
      "fresh_until_utc": "...",
      "quality": "CURRENT",
      "source": "DSG.EagleHostHealthCollector",
      "reasons": []
    }
  },
  "safety": {
    "observed_state": "...",
    "authority": "NINA_SAFETY_MONITOR_OBSERVATION"
  }
}
```

Health and Safety must remain independent.

## 9. Failure behavior

| Failure | Required behavior |
|---|---|
| Collector cannot read one source | affected signal `UNAVAILABLE/UNKNOWN`; other signals continue |
| SMART/reliability denied | reliability values `null`, reason retained |
| Windows Time stopped | source state preserved; no fabricated NTP offset |
| Event Log query fails | event_log signal `UNKNOWN`; collector continues |
| Scheduled Task query fails | scheduled_tasks signal `UNKNOWN`; no task mutation |
| Plugin projection missing | plugin_heartbeat `UNKNOWN`; host collector continues |
| Collector stops | `eagle-health.json` becomes `STALE` downstream |
| Malformed source value | affected field/signal `UNKNOWN`; diagnostic reason; no crash loop |

## 10. Security and privacy

Do not serialize:

- passwords, tokens, API keys;
- full registry exports;
- environment variables wholesale;
- complete event-log messages when they may expose user/application data;
- network secrets;
- file contents unrelated to bounded diagnostics.

Paths and executable names may be recorded where needed for provenance and diagnostics.

## 11. Validation gates for G2

G2 is architecture-ready when:

1. every contract field maps to a verified source, explicitly optional source, or documented open source gap;
2. no field requires an actuator command;
3. failure semantics are explicit;
4. Safety boundary is explicit;
5. no undeclared threshold exists;
6. source-specific privilege requirements are documented;
7. canonical integration does not overwrite N.I.N.A. equipment telemetry.

Runtime implementation remains blocked until BKL-029 closure.

## 12. Traceability

Related artifacts:

- `docs/architecture/telemetry/BKL-030-EAGLE-Health-Reliability-Architecture-Assessment.md`
- `docs/architecture/telemetry/evidence/BKL-030-EAGLE-Health-Source-Discovery-2026-08-31.md`
- `scripts/telemetry/Inspect-EagleHealthSources.ps1`
- `scripts/telemetry/Export-NinaObservatoryStatus.ps1`
- `docs/project/BACKLOG.md`
- `docs/project/FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md`

## 13. Current disposition

**G2 contract defined for planning/review. BKL-030 remains `Planned` and producer implementation remains blocked by BKL-029.**
