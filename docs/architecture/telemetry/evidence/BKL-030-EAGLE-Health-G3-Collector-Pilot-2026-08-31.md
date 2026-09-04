# BKL-030 — EAGLE Health G3 Collector Pilot — 2026-08-31

## Status

**PASS — nominal and controlled failure/recovery non-commissioned collector pilots completed on EAGLE30154.**

This is runtime implementation evidence for the G3 pilot only. It does not commission the collector, activate health policy, change BKL-030 from Planned, or constitute BKL-030 acceptance.

## Nominal execution

- Host: `EAGLE30154`
- Branch: `feature/bkl-030-eagle-health-discovery`
- Script: `scripts/telemetry/Start-EagleHealthCollectorPilot.ps1`
- Duration: 300 s
- Fast cadence: 30 s
- Medium cadence: 120 s
- Slow cadence: 600 s
- Projection: `%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health-pilot.json`
- Cycles completed: 10
- Signals projected per cycle: 13
- Stop disposition: normal
- N.I.N.A. was running during the pilot.

The console continuously reported `summary=UNKNOWN` and the final projection retained `POLICY_NOT_ACTIVATED`.

## Projection boundary verified

Observed final projection:

- `schema_version = 1.0`
- `component = DSG.EagleHostHealthCollector`
- `computer = EAGLE30154`
- projection quality `CURRENT`
- `summary.state = UNKNOWN`
- summary reason `POLICY_NOT_ACTIVATED`
- diagnostics mode `NON_COMMISSIONED_PILOT`
- diagnostics `policy_enabled = false`
- diagnostics safety authority `OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS`

No health severity policy was activated.

## Fast signals

Verified CURRENT/OBSERVED signals:

- CPU: Intel Celeron J4005, 2 physical / 2 logical processors, instantaneous load captured; temperature remains null.
- Memory: 12,543,135,744 bytes physical total; 8,408,637,440 bytes available in final sample; no memory-pressure policy activated.
- Uptime: boot time `2026-08-20T14:28:42.5000000Z`; unexpected reboot remains unclassified/null.
- Processes: AAG_CloudWatcher, ASCOM.CloudWatcher.Server, ASCOM.TS_Shelter, EagleManager and NINA observed running.
- NINA plugin projection: exists and was CURRENT in the final sample.

Process presence is evidence only; absence/presence is not yet a governed health severity.

## Medium signals

### Storage

Final nominal sample:

- C: `4,229,361,664` bytes free / `223,397,015,552` bytes, free ratio `0.018932` (~1.8932%).
- D: `356,942,249,984` bytes free / `735,304,478,720` bytes, free ratio `0.485435` (~48.5435%).
- detailed reliability/SMART remains `UNAVAILABLE_NON_ELEVATED`.

No storage severity threshold was activated.

### Scheduled Tasks

- `Digital StarGate - Daily Session Upload`: Ready, raw `LastTaskResult = 1`, result classification null.
- `Digital StarGate - OneDrive Export`: Ready, raw `LastTaskResult = 0`, result classification null.

The collector correctly preserves raw task evidence without inventing exit-code semantics.

### Log-source freshness

Observed existing sources:

- CloudWatcher CSV;
- `C:\DigitalStarGate\TelemetryRuntime\producer.log`;
- NINA observatory-status projection.

All were present and had recent last-write timestamps during the nominal pilot.

## Slow signals

### Reliability events

The 7-day bounded Event Log projection captured repeated reliability-significant EagleManager fingerprints:

- Application Error event 1000;
- .NET Runtime event 1026.

No full verbose Event Log messages are projected.

### USB / COM

PnP and `SERIALCOMM` again reconcile the same active ports:

- COM1 — Prolific;
- COM9 — FTDI;
- COM14 — FTDI;
- COM47 — FTDI.

Source reconciliation remains `PNP_AND_SERIALCOMM`.

### Pending reboot

Observed:

- CBS reboot pending: false;
- Windows Update reboot required: false;
- PendingFileRenameOperations present: true, count 6;
- `reboot_required = null`;
- policy `RAW_EVIDENCE_ONLY`.

This confirms the pilot does not infer a reboot requirement from PendingFileRenameOperations alone.

### Time synchronization

Observed:

- W32Time service: Stopped;
- start mode: Manual;
- last successful synchronization evidence: `2026-08-31T02:29:26.9206792Z`;
- current offset remains null;
- `w32tm.exe` available.

Service state alone is not classified as a time fault.

### Configuration drift

No baseline is approved. Projection remains `status = UNKNOWN` with null baseline identifiers and empty drift evidence.

## Controlled failure/recovery pilot

A second non-commissioned pilot exercised the collector's error-isolation path without stopping, reconfiguring or mutating any real source.

Configuration:

- duration: 180 s;
- fast cadence: 15 s;
- medium cadence: 60 s;
- slow cadence: 120 s;
- injected group: `FAST`;
- injection start cycle: 3;
- injection cycle count: 2;
- cycles completed: 12;
- stop disposition: normal.

Observed behavior:

1. cycles 1-2: all 13 signals available;
2. cycles 3-4: only the FAST group was projected `UNAVAILABLE/UNKNOWN`:
   - `cpu`;
   - `memory`;
   - `uptime`;
   - `processes`;
   - `plugin_heartbeat`;
3. medium and slow signals remained present and were not marked unavailable;
4. cycle 5 automatically recovered the FAST group without operator action;
5. cycles 5-12 completed with all 13 signals available;
6. `summary` remained `UNKNOWN` for every cycle;
7. final projection returned all 13 signals to `OBSERVED/CURRENT`;
8. diagnostics preserved the test parameters and retained `policy_enabled = false` and `safety_authority = OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS`.

This validates group-level failure isolation and automatic recovery for the injected FAST-source failure path.

The test does not yet prove every possible real-source failure mode, nor a commissioned stale-file scenario after collector termination. Those remain later OAT concerns.

## Failure and safety disposition

Nominal runtime, injected failure isolation and automatic recovery are now verified for the pilot implementation.

No dome, roof, mount, camera, power, relay, network, Windows service, Scheduled Task, registry or update state was changed. The injected fault existed only inside the pilot collector's test path. Local physical Safety Authority remained independent.

## Gate disposition

- D1 source discovery: PASS
- D2 privilege/source assessment: PASS
- G2 projection contract: DEFINED
- D3 overhead pilot: PASS
- G3 collector implementation — nominal non-commissioned runtime pilot: **PASS**
- G3 controlled failure/recovery pilot: **PASS**
- G3 commissioned producer: **BLOCKED until BKL-029 closure**
- G4 CI: NOT EXECUTED for this collector increment
- G5 commissioned runtime OAT: NOT EXECUTED
- G6 history: NOT EXECUTED
- G7 portal: NOT EXECUTED
- G8 Safety acceptance review: NOT EXECUTED

**BKL-030 remains Planned.**
