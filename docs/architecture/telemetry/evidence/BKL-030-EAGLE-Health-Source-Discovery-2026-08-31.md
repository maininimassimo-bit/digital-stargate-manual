# BKL-030 — EAGLE Health Source Discovery Evidence — 2026-08-31

## Status

**D1/D2 discovery evidence captured. BKL-030 remains Planned.**

This record documents read-only source availability on `EAGLE30154`. It is not BKL-030 acceptance and does not activate the capability.

## Execution context

- Computer: `EAGLE30154`
- User: `EAGLE30154\PrimaLuceLab`
- Elevated: `False`
- Script: `scripts/telemetry/Inspect-EagleHealthSources.ps1`
- Mode: `READ_ONLY_DISCOVERY`
- Evidence bundle: `C:\DigitalStarGate\TelemetryEvidence\eagle-health-source-discovery-20260831-060716`

## D1/D2 source classification

| Signal/source | Discovery result | Classification | Notes |
|---|---|---|---|
| Operating system | Windows 10 Enterprise LTSC 10.0.17763 x64 | VERIFIED | Readable non-elevated |
| Boot time / uptime source | `LastBootUpTime` available | VERIFIED | Readable non-elevated |
| CPU identity/load | Intel Celeron J4005, 2 cores/2 logical, load observed | VERIFIED | Readable non-elevated |
| Memory totals/free | Total/free physical memory available | VERIFIED | Readable non-elevated |
| Logical disks | C: and D: size/free available | VERIFIED | Readable non-elevated |
| Physical disk inventory | KINGSTON SA400S37960G, SSD/SATA, HealthStatus Healthy | VERIFIED | Readable non-elevated |
| Storage reliability counters / SMART detail | CIM access error | UNAVAILABLE_NON_ELEVATED | Requires targeted privilege/source assessment; do not infer SMART counters |
| Windows Time status/config | `w32tm` reports service not started | VERIFIED_SOURCE / SERVICE_INACTIVE | Source command available; synchronization state currently unavailable because service is stopped |
| DSG Scheduled Tasks | Daily Session Upload and OneDrive Export visible | VERIFIED | Readable non-elevated |
| Relevant processes | AAG CloudWatcher, ASCOM CloudWatcher, TS Shelter, N.I.N.A. visible | VERIFIED | Readable non-elevated |
| System/Application Event Log | Critical/Error entries readable | VERIFIED | Readable non-elevated |
| USB PnP inventory | USB/FTDI/Prolific devices visible | VERIFIED | Readable non-elevated |
| Serial ports via Win32_SerialPort | Probe succeeds but returned no rows | NEEDS_RECONCILIATION | PnP inventory shows Prolific COM1; Win32_SerialPort source must be cross-checked |
| Pending reboot registry | CBS/WU reboot keys absent; PendingFileRenameOperations present | VERIFIED_RAW_EVIDENCE | Do not yet classify host reboot state until policy is defined |
| Windows Update service | `wuauserv` visible, Stopped/Manual | VERIFIED | Read-only source available |
| DSG/runtime paths | Key DSG, telemetry, plugin and CloudWatcher paths visible | VERIFIED | Readable non-elevated |
| Known log files | CloudWatcher, ASCOM and TelemetryRuntime evidence visible | VERIFIED | Readable non-elevated |

## Capacity evidence

Logical disk evidence:

```text
C: size      = 223397015552 bytes
C: free      =   4335616000 bytes
D: size      = 735304478720 bytes
D: free      = 356942249984 bytes
```

Calculated free ratios (descriptive only; no severity threshold is declared):

```text
C: ~1.94% free
D: ~48.54% free
```

The very low observed free capacity on C: is an operational risk candidate for BKL-030 policy design. It must not be labeled `DEGRADED` or `CRITICAL` until explicit storage thresholds are governed.

## Scheduled Task evidence

Observed:

```text
Digital StarGate - Daily Session Upload
  State          : Ready
  LastRunTime    : 31/08/2026 07:20:20
  LastTaskResult : 1
  NextRunTime    : 01/09/2026 07:20:20

Digital StarGate - OneDrive Export
  State          : Ready
  LastRunTime    : 31/08/2026 08:07:07
  LastTaskResult : 267009
  NextRunTime    : 31/08/2026 08:17:17
```

These values are retained as raw evidence. BKL-030 must define an explicit mapping for Task Scheduler result codes before deriving a health state.

## Event Log findings relevant to reliability

The discovery proves that Application/System errors can be collected without elevation. Relevant observed examples include repeated `EagleManager.exe` failures on 26–27 August 2026 with:

- `Application Error` event ID 1000;
- `.NET Runtime` event ID 1026;
- `System.Threading.SemaphoreFullException`;
- `System.InvalidOperationException: Nullable object must have a value`;
- stack traces in `EagleManager.Services.Boards.SerialBoard<T>.OnTimeoutTimerElapsed`.

This validates Event Log as a useful reliability source. It does **not** establish root cause for the observatory as a whole.

Repeated TPM-WMI event ID 1803 and System Restore event ID 8193 were also observed. BKL-030 must avoid treating every Windows Error event as observatory-critical; provider/event allowlists or severity policy are required.

## Pending reboot evidence

Observed raw registry state:

- Component Based Servicing `RebootPending`: absent;
- Windows Update `RebootRequired`: absent;
- `PendingFileRenameOperations`: present with entries including Edge Update paths.

This is sufficient to prove source readability, not sufficient to declare a mandatory reboot. A deterministic policy must distinguish benign pending file rename operations from reboot-requiring conditions.

## Time synchronization evidence

Both:

```text
w32tm /query /status
w32tm /query /configuration
```

returned:

```text
Servizio non avviato. (0x80070426)
```

Therefore Windows Time command/source visibility is VERIFIED, while active NTP/clock synchronization evidence is currently unavailable from this service state. BKL-030 should represent this explicitly rather than inventing an offset.

## SMART/reliability evidence

`Get-PhysicalDisk` is available and reports the Kingston SSD as `Healthy / OK`. Detailed `Get-StorageReliabilityCounter` data failed under the non-elevated user with a CIM resource access error.

Disposition:

- physical disk inventory/aggregate health: VERIFIED;
- detailed reliability counters: UNAVAILABLE_NON_ELEVATED pending targeted assessment;
- no admin privilege should be introduced solely for SMART unless justified by architecture review.

## D1/D2 conclusion

The non-elevated operational account can already provide the majority of BKL-030 evidence sources. The architecture can therefore retain its preferred low-privilege collector model.

Open source gaps:

1. detailed SMART/reliability counters;
2. serial-port source reconciliation (`Win32_SerialPort` empty vs PnP COM1 evidence);
3. hardware/CPU temperature source;
4. explicit NTP/clock offset source while Windows Time is stopped;
5. governed mapping of Scheduled Task result codes;
6. governed pending-reboot classification;
7. provider/event policy for reliability-significant Windows Event Log entries;
8. storage capacity thresholds and trend policy.

## Safety boundary

No device command, restart, registry mutation, Scheduled Task mutation, Windows Update action, network change, power change or Safety Authority action occurred during discovery.

**BKL-030 remains `Planned`; this is discovery evidence only.**
