# BKL-030 — EAGLE Health Source Discovery Evidence — 2026-09-03

## Status

**D1 Host Baseline Inventory: COMPLETE. D2 Privilege Assessment: COMPLETE. BKL-030 moves to In Progress.**

This record documents the second read-only source-discovery execution on `EAGLE30154` after the 03/09/2026 runtime baseline alignment. It is not BKL-030 acceptance, does not implement the collector and does not authorize remediation or device control.

## Execution context

- Computer: `EAGLE30154`
- User: `EAGLE30154\PrimaLuceLab`
- Elevated: `False`
- PowerShell: `5.1.17763.9121`
- Architecture: `AMD64`
- Observed at UTC: `2026-09-03T07:57:32.4969817Z`
- Script: `scripts/telemetry/Inspect-EagleHealthSources.ps1`
- Mode: `READ_ONLY_DISCOVERY`
- Evidence bundle: `C:\DigitalStarGate\TelemetryEvidence\eagle-health-source-discovery-20260903-075732`

All 17 top-level probes completed without a top-level `UNAVAILABLE`. Internal source semantics were inspected individually: top-level `AVAILABLE` means the probe executed, not that every nested signal produced usable data.

## D1 source classification

| Signal/source | Discovery result | Classification | Notes |
|---|---|---|---|
| Operating system | Windows 10 Enterprise LTSC 10.0.17763 x64 | VERIFIED | Readable non-elevated |
| Boot time / uptime | `LastBootUpTime = 2026-08-20 14:28:42` local | VERIFIED | Readable non-elevated |
| Computer system | Intel Client Systems NUC7CJYH | VERIFIED | Readable non-elevated |
| CPU | Intel Celeron J4005, 2 cores / 2 logical, load observed 22% | VERIFIED | Raw load descriptive only |
| Memory | total/free physical memory available | VERIFIED | Readable non-elevated |
| Logical disks | C: and D: capacity/free available | VERIFIED | No severity threshold yet |
| Physical disk inventory | KINGSTON SA400S37960G, SSD/SATA, `Healthy / OK` | VERIFIED | Aggregate health readable non-elevated |
| Storage reliability counters / SMART detail | nested CIM access error | UNAVAILABLE_NON_ELEVATED | Detailed counters remain unavailable |
| Windows Time status/config | source available; service not started `0x80070426` | VERIFIED_SOURCE / SERVICE_INACTIVE | No offset may be inferred |
| DSG Scheduled Tasks | Daily Session Upload and OneDrive Export visible | VERIFIED | Raw result codes need governed mapping |
| Relevant processes | AAG CloudWatcher and ASCOM TS Shelter observed | VERIFIED_SOURCE | Presence is time-dependent |
| System/Application Event Log | reliability-significant errors readable | VERIFIED | Provider/event policy still required |
| USB PnP inventory | USB/FTDI/Prolific devices visible | VERIFIED | Readable non-elevated |
| COM/serial inventory | PnP shows COM1, COM9, COM14, COM47; `Win32_SerialPort` zero rows | VERIFIED_WITH_SOURCE_RECONCILIATION | PnP is primary inventory source |
| Pending reboot registry | CBS/WU reboot keys absent; PendingFileRenameOperations present | VERIFIED_RAW_EVIDENCE | No reboot classification yet |
| Windows Update service | readable, observed Stopped/Manual | VERIFIED | No update action authorized |
| DSG/runtime paths and logs | key metadata readable | VERIFIED | Readable non-elevated |

## Capacity evidence

```text
C: size = 223397015552 bytes
C: free =   1500758016 bytes
D: size = 735304478720 bytes
D: free = 355645206528 bytes
```

Descriptive free ratios are approximately C: 0.67% and D: 48.37%. No `DEGRADED` or `CRITICAL` state is declared because storage thresholds are not governed. C: remains a high-priority policy/risk input because the previous 31/08 discovery already showed very low free space and absolute free bytes decreased further.

## COM reconciliation

Targeted PnP evidence observed healthy FTDI/Prolific serial devices on COM1, COM9, COM14 and COM47. This resolves the earlier source ambiguity: operational COM devices are inventory-visible through PnP without elevation, while `Win32_SerialPort` must not be the sole presence source.

## Reliability Event Log evidence

Application Event Log is readable without elevation and exposes repeated `EagleManager.exe` failures, including 03/09 00:09, 01/09 22:27, 31/08 20:04 and multiple 27/08 occurrences. Observed evidence includes `.NET Runtime` event 1026, `Application Error` event 1000, `System.Threading.SemaphoreFullException` and `System.InvalidOperationException: Nullable object must have a value`.

This validates Event Log as a reliability source; it does not establish root cause or justify treating every Windows error as observatory-critical. A governed provider/event allowlist and severity mapping remain required.

A separate interactive filter command used during reconciliation contained a PowerShell line-break error before `-or`; the resulting `CommandNotFoundException` did not modify Event Log or the discovery bundle and is not a host reliability event.

## D2 privilege assessment

The discovery ran as `EAGLE30154\PrimaLuceLab`, `elevated=False`, PowerShell `5.1.17763.9121`. All 17 top-level probes executed. Disposition: **PASS** for the low-privilege architecture boundary. Detailed SMART counters remain unavailable and must become an unavailable/unknown nested signal rather than causing privilege escalation by default.

## D1/D2 conclusion

D1 and D2 are complete with real runtime evidence. BKL-030 may move from `Ready` to `In Progress`.

Open items before G1/G2 closure:

1. decide whether detailed SMART counters are optional or justify a separate privileged adapter;
2. identify a non-invasive hardware/CPU temperature source, otherwise keep it `UNKNOWN`;
3. define clock synchronization evidence while Windows Time is inactive;
4. define Scheduled Task result-code semantics;
5. define deterministic pending-reboot policy;
6. define Event Log provider/event allowlist and severity mapping;
7. define storage capacity thresholds/trend policy, with C: as explicit risk candidate;
8. define configuration-drift source and provenance;
9. define sampling/retention cadence for D3/G6.

## Safety boundary

No device command, restart, service change, registry mutation, Scheduled Task mutation, Windows Update action, network change, power change or Safety Authority action occurred.

**Disposition: D1 COMPLETE, D2 COMPLETE, BKL-030 IN PROGRESS; G1–G8 remain subject to their own evidence and acceptance.**
