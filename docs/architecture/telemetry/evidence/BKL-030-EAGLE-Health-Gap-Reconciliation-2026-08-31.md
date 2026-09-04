# BKL-030 — EAGLE Health Gap Reconciliation Evidence — 2026-08-31

## Status

**PASS — read-only source reconciliation completed on EAGLE30154.**

This evidence does not constitute BKL-030 acceptance and does not activate a producer.

## Execution context

- Host: `EAGLE30154`
- Mode: read-only discovery/reconciliation
- Script: `scripts/telemetry/Inspect-EagleHealthSourceGaps.ps1`
- Evidence bundle: `C:\DigitalStarGate\TelemetryEvidence\eagle-health-gap-reconciliation-20260831-075943`
- Result: 8/8 probes `AVAILABLE`

## Reconciled findings

### Hardware temperature

`MSAcpi_ThermalZoneTemperature` returned `Accesso negato` for the non-elevated user. No verified CPU/hardware temperature source is currently available to the low-privilege collector.

Disposition:

- `cpu.temperature_c = null`;
- signal quality for hardware temperature remains `UNKNOWN/UNAVAILABLE`;
- do not introduce elevation solely to populate this signal without a separate architecture review.

### Windows Time / clock synchronization

Observed configuration:

- `W32Time` service state: `Stopped`;
- start mode: `Manual`;
- type: `NTP`;
- configured source: `time.windows.com,0x9`;
- NTP client enabled;
- special poll interval: `32768` seconds.

Windows Event Log contains repeated `Microsoft-Windows-Time-Service` event IDs 35 and 37 showing successful synchronization with `time.windows.com,0x9`; event 35 reports local stratum 5. Event 158 reports unsupported `VMICTimeProvider` outside Hyper-V, which is expected and should not be treated as a reliability fault.

Disposition:

- service state and configured source are VERIFIED;
- successful historical synchronization evidence is VERIFIED through Event Log;
- current clock offset remains `null` because no verified current offset source was captured;
- `W32Time = Stopped` alone must not be labeled a clock fault because historical event evidence proves scheduled/on-demand synchronization behavior.

### Scheduled Tasks

Observed tasks:

#### Digital StarGate - Daily Session Upload

- state: Ready;
- `LastTaskResult = 1` / `0x00000001`;
- principal: `PrimaLuceLab`;
- PowerShell action invokes `Invoke-DSGSessionPreflight.ps1` and `Invoke-DSGAutomaticSession.ps1`.

#### Digital StarGate - OneDrive Export

- state: Ready;
- `LastTaskResult = 0` / `0x00000000`;
- principal: `PrimaLuceLab`;
- PowerShell action invokes `Start-DSGOneDriveExport.ps1`.

Disposition:

- `0x00000000` may be classified as success where the task contract expects normal process exit semantics;
- `0x00000001` must remain raw/non-success evidence for Daily Session Upload until its launcher/preflight exit-code contract is explicitly mapped;
- task `Ready` is scheduler state only and is not equivalent to successful last execution.

### Serial / COM reconciliation

`Win32_SerialPort` returned no rows, but two independent sources identify four active COM mappings:

- COM1 — Prolific PL2303GT;
- COM9 — FTDI;
- COM14 — FTDI;
- COM47 — FTDI.

Sources:

- `Win32_PnPEntity` Ports class / device names;
- `HKLM:\HARDWARE\DEVICEMAP\SERIALCOMM`.

Disposition:

- `Win32_SerialPort` is not authoritative on this host;
- BKL-030 should use PnP + `SERIALCOMM` as the baseline inventory sources;
- absence from `Win32_SerialPort` must not be classified as missing hardware.

### Pending reboot

Observed:

- CBS `RebootPending`: false;
- Windows Update `RebootRequired`: false;
- `PendingFileRenameOperations`: present;
- raw count: 6 entries, associated with Microsoft Edge Update paths.

Disposition:

- no deterministic reboot-required condition is currently proven;
- baseline rule: `reboot_required = true` only when a strong reboot indicator such as CBS or Windows Update `RebootRequired` is present;
- `PendingFileRenameOperations` alone remains advisory raw evidence and does not force `reboot_required = true`.

### Reliability Event Log fingerprints

Observed 30-day fingerprints:

- `.NET Runtime` event 1026: 13 occurrences, examples contain `EagleManager`;
- `Application Error` event 1000: 13 occurrences, examples contain `EagleManager`;
- `Service Control Manager` event 7023: 5 occurrences.

Disposition:

- EagleManager 1000/1026 is accepted as a reliability-significant application fingerprint;
- generic SCM 7023 remains unclassified until service identity is normalized;
- event severity must be provider/event/application aware; not every Windows Error is observatory-critical.

### Storage capacity

Observed:

```text
C: 4,262,043,648 bytes free / 223,397,015,552 bytes = 1.908% free
D: 356,942,249,984 bytes free / 735,304,478,720 bytes = 48.543% free
```

Disposition:

- values are VERIFIED raw evidence;
- no severity is assigned by this evidence record;
- C: low free capacity is a clear policy input and operational risk candidate;
- thresholds require explicit governance before `DEGRADED/CRITICAL` classification.

## Source classification after reconciliation

| Signal | Status |
|---|---|
| Storage capacity | VERIFIED |
| Physical disk inventory | VERIFIED from prior D1/D2 |
| Detailed SMART counters | UNAVAILABLE_NON_ELEVATED |
| CPU/RAM/uptime | VERIFIED from prior D1/D2 |
| Hardware temperature | UNAVAILABLE_NON_ELEVATED |
| Windows Time config | VERIFIED |
| Historical time sync events | VERIFIED |
| Current clock offset | OPEN / UNKNOWN |
| DSG Scheduled Tasks | VERIFIED |
| COM inventory | VERIFIED via PnP + registry |
| Pending reboot strong indicators | VERIFIED |
| Pending file rename | VERIFIED advisory evidence |
| Reliability Event Log fingerprints | VERIFIED |

## Safety boundary

No device command, task mutation, registry mutation, service start/stop, reboot, Windows Update action, power change, network change or Safety Authority action occurred.

**BKL-030 remains Planned.**
