# BKL-030 — EAGLE Health G5 Commissioning and OAT Plan

| Field | Value |
|---|---|
| Status | **Prepared — commissioning disabled and blocked by BKL-029** |
| Date | 2026-08-31 |
| Host | `EAGLE30154` |
| Component | `DSG.EagleHostHealthCollector` |
| Pilot projection | `%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health-pilot.json` |
| Future commissioned projection | `%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json` |
| Safety authority | **Outside scope — local physical interlocks remain authoritative** |

## 1. Purpose

Prepare the G5 runtime/OAT package without commissioning BKL-030 before its dependency BKL-029 is closed.

This package is deliberately inert: it does not install a Scheduled Task, Windows service, startup entry, remediation path or device command.

## 2. Prepared artifacts

- `scripts/telemetry/eagle-health-commissioning.config.json` — disabled commissioning configuration and future runtime parameters.
- `scripts/telemetry/Test-EagleHealthCollectorOat.ps1` — read-only OAT validator. By default it accepts only the pilot projection and refuses the commissioned projection.
- existing `scripts/telemetry/Start-EagleHealthCollectorPilot.ps1` remains the only runnable producer in this increment.

## 3. Dependency guard

Commissioning configuration must remain:

- `enabled = false`;
- `state = BLOCKED_BY_BKL_029`;
- `dependency = BKL-029`;
- `install_mode = NONE`;
- Scheduled Task and Windows service names null.

No installation action is authorized while BKL-029 is open.

## 4. Precommissioning OAT

After a nominal pilot run on EAGLE30154, execute:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\telemetry\Test-EagleHealthCollectorOat.ps1
```

The OAT validates:

1. commissioning remains disabled and BKL-029-blocked;
2. policy remains disabled;
3. Safety Authority remains outside the collector;
4. component/schema/computer identity is present;
5. summary remains `UNKNOWN` with `POLICY_NOT_ACTIVATED`;
6. all 13 pilot signals exist;
7. signal state/quality values stay within the G2 envelope;
8. projection freshness boundary is internally valid;
9. no acceptance or commissioning is inferred from an OAT PASS.

The precommissioning OAT does not prove continuous service operation, startup persistence, restart behavior or downstream stale detection.

## 5. Future commissioning sequence — BLOCKED

Only after BKL-029 is explicitly closed and BKL-030 is authorized to advance:

1. re-fetch `main`, backlog and dependency evidence;
2. re-run G4 CI on the exact commissioning candidate;
3. approve the runtime installation mechanism and identity;
4. change from pilot projection to the commissioned `eagle-health.json` boundary;
5. install only the approved lightweight producer mechanism;
6. verify start/restart behavior and projection freshness;
7. stop the collector deliberately and prove downstream `STALE` handling;
8. prove one-source failure does not stop unrelated signals;
9. prove recovery after source restoration;
10. verify reboot/power-cycle behavior without weakening physical safety;
11. verify no collector path can actuate dome, mount, camera, power, relays, router or Safety Authority;
12. capture G5 evidence and rollback evidence before any acceptance decision.

## 6. Failure-mode and safety review

| Scenario | Required disposition |
|---|---|
| Loss of network connectivity | Host collection continues where sources are local; no Safety inference |
| Collector stopped/crashed | Projection becomes stale downstream; no equipment command |
| Source unavailable | Affected signal becomes `UNAVAILABLE/UNKNOWN`; unrelated signals continue |
| Host power loss | Collector unavailable; local physical safety remains independent |
| Windows service/task failure | Evidence only; no automatic repair until separately governed |
| Partial dome closure / emergency stop | Outside host-health authority; physical/local Safety Authority remains authoritative |
| Manual override | Collector remains observational and must not countermand operator/local interlock |
| Stale/absent telemetry | Must never be interpreted as safe |
| Reboot required evidence | Raw evidence only until deterministic policy is approved |
| Health policy unavailable | Summary remains `UNKNOWN`; no invented severity |

## 7. Rollback contract for future commissioning

Before commissioning, an approved rollback must be able to:

- stop/disable only the Digital StarGate host-health producer mechanism;
- remove or disable only its approved persistence entry;
- preserve existing N.I.N.A., PHD2, CloudWatcher, ASCOM and Safety components;
- leave the last projection as stale evidence or archive it according to the approved runtime runbook;
- require no dome/mount/power/network device action.

No rollback command is implemented by this planning increment.

## 8. Gate disposition

At creation of this plan:

- D1: PASS
- D2: PASS
- G2: DEFINED
- D3: PASS
- G3 nominal pilot: PASS
- G3 controlled failure/recovery: PASS
- G4 CI: PASS on the verified precommissioning candidate preceding this plan
- G5 precommissioning plan: **PREPARED**
- G5 commissioned runtime OAT: **NOT EXECUTED / BLOCKED BY BKL-029**
- BKL-030 acceptance: **NOT EXECUTED**

BKL-030 remains `Planned` until the dependency and governance gates permit advancement.
