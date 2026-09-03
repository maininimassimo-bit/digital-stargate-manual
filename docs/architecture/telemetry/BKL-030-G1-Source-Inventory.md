# BKL-030 — G1 Governed Source Inventory

| Campo | Valore |
|---|---|
| Identificativo | BKL-030-G1 |
| Stato | **COMPLETE — source inventory governed from D1/D2 evidence** |
| Target | EAGLE30154 |
| Boundary | Read-only host observability |
| Safety Authority | External/local and independent |

## 1. Purpose

Consolidate the source-of-truth inventory for the future `DSG.EagleHostHealthCollector` using only evidence demonstrated on EAGLE30154 during D1/D2 and the cost/failure constraints established by D3/D4.

## 2. Governed source matrix

| Signal | Primary source | Secondary/composite source | Disposition | Cadence class | Notes |
|---|---|---|---|---|---|
| OS identity / boot time | `Win32_OperatingSystem` | none | VERIFIED | slow/on-change | Host identity and boot evidence |
| CPU topology/load | `Win32_Processor` | future bounded counter if needed | VERIFIED | fast | Raw load only; no temperature source verified |
| RAM capacity/free | `Win32_OperatingSystem` / CIM | future bounded counter if needed | VERIFIED | fast | Raw bytes/ratio only |
| Logical disk capacity | `Win32_LogicalDisk` | none | VERIFIED | medium | Must publish total, free and free ratio/percent separately from physical health |
| Physical disk identity/aggregate health | `Get-PhysicalDisk` | none | VERIFIED | slow/on-change | KINGSTON SSD observed Healthy/OK |
| Detailed SMART/reliability | `Get-StorageReliabilityCounter` | none | UNAVAILABLE_NON_ELEVATED | slow/on-change | Remains UNKNOWN/UNAVAILABLE; no automatic elevation |
| Uptime | boot time + collector clock arithmetic | none | VERIFIED | medium | Unexpected reboot needs historical/event evidence |
| Time synchronization | `w32tm` + service state | none | VERIFIED_SOURCE / SERVICE_INACTIVE | medium | Source available but Windows Time inactive; offset/source may remain null |
| Scheduled Tasks DSG | Task Scheduler read API | none | VERIFIED | slow/on-change | Raw result code preserved; classification requires governed per-task mapping |
| Relevant processes | Windows process table | none | VERIFIED_SOURCE | fast | Presence is contextual evidence, not automatic failure |
| Reliability Event Log | Application/System Event Log | provider/event allowlist | VERIFIED | slow/on-change | Bounded normalized events only; no full unbounded messages |
| USB/COM | Windows PnP inventory | `Win32_SerialPort` as supplemental only | VERIFIED_COMPOSITE | medium | PnP observed COM1/9/14/47; `Win32_SerialPort` cannot be sole presence source |
| Pending reboot evidence | bounded registry keys | none | VERIFIED_RAW_EVIDENCE | slow/on-change | Raw CBS/WU/PendingFileRename evidence; final reboot_required may remain null until policy |
| Windows Update service | service state | none | VERIFIED | slow/on-change | Never start/scan/install solely for telemetry |
| Log source metadata | filesystem metadata | none | VERIFIED | medium | Path exists/length/last-write only; no arbitrary content copying |
| Configuration drift | governed baseline manifest | none yet | OPEN_SOURCE_GAP | slow/on-change | Signal remains UNKNOWN until baseline manifest is approved |
| N.I.N.A. plugin heartbeat | existing N.I.N.A. telemetry projection | file metadata/projection envelope | VERIFIED_TARGET_SOURCE | fast | Correlation only; host health remains outside plugin |

## 3. Storage contract requirement

Storage is explicitly two different evidence families and must never be collapsed into one number:

1. **Capacity** — logical volume `size_bytes`, `free_bytes`, `free_ratio`/`free_pct`.
2. **Physical health** — disk identity, Windows aggregate `HealthStatus`, `OperationalStatus` and optional detailed reliability fields.

The 03/09/2026 discovery observed C: with about 0.67% free and D: with about 48.37% free. These values are raw evidence/risk input only. G1 does not define DEGRADED or CRITICAL thresholds.

## 4. Source precedence

- COM presence: PnP inventory is authoritative for observed host presence; `Win32_SerialPort` is supplemental only.
- Disk capacity: `Win32_LogicalDisk` is authoritative for logical free/total bytes.
- Physical disk aggregate health: `Get-PhysicalDisk` is preserved as raw Windows evidence; it does not substitute detailed SMART.
- Detailed SMART: if access remains denied, publish unavailable/unknown rather than synthesize values or elevate automatically.
- Time sync: service/query evidence is authoritative; clock continuity is not proof of synchronization.
- Process presence and task results are contextual/raw evidence until G2/G3 policy maps them.

## 5. G1 acceptance

G1 is complete because every baseline BKL-030 signal is now either:

- mapped to a verified read-only source;
- mapped to a governed composite source;
- explicitly optional/unavailable; or
- recorded as an open source gap (`configuration_drift`, hardware temperature/detailed SMART as applicable).

No source requires an actuator command or changes the Safety Authority boundary.

**Disposition: G1 COMPLETE. Proceed with G2 contract and field provenance.**
