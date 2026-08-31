# BKL-030 — EAGLE Health G5 Precommissioning OAT Evidence

| Field | Value |
|---|---|
| Backlog item | BKL-030 |
| Gate | G5 precommissioning OAT |
| Date | 2026-08-31 |
| Host | `EAGLE30154` |
| Branch | `feature/bkl-030-eagle-health-discovery` |
| Result | **PASS — PRECOMMISSIONING ONLY** |
| Commissioning | **NOT EXECUTED** |
| Acceptance | **NOT DECLARED** |
| Dependency | **BKL-029 remains blocking** |
| Safety authority | `OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS` |

## 1. Purpose

Record the runtime evidence supplied from `EAGLE30154` for the BKL-030 read-only precommissioning OAT. This evidence validates only the pilot projection and the precommissioning guardrails. It does not commission the collector, install a Windows service or Scheduled Task, activate health severity policy, or authorize any equipment or Safety action.

## 2. Command executed

```powershell
cd C:\DigitalStarGate\digital-stargate-manual-ap14-runtime
git pull --ff-only

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\telemetry\Test-EagleHealthCollectorOat.ps1
```

The branch was fast-forwarded to commit `03138b657fec319ef9fdde4423adb527cbfdf449` before execution.

## 3. Observed runtime output

```text
Digital StarGate BKL-030 EAGLE Health OAT - PRECOMMISSIONING
Computer: EAGLE30154
Projection: C:\Users\PrimaLuceLab\AppData\Local\DigitalStarGate\telemetry\eagle-health-pilot.json
Pilot boundary: C:\Users\PrimaLuceLab\AppData\Local\DigitalStarGate\telemetry\eagle-health-pilot.json
Signals: 13; required=13; missing=0
Summary: UNKNOWN; policy_enabled=False
Safety authority: OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS
BKL-030 OAT RESULT: PASS - PRECOMMISSIONING ONLY; NOT COMMISSIONING OR ACCEPTANCE
```

## 4. Evidence classification

| Check | Result | Evidence |
|---|---|---|
| Script executes on Windows PowerShell 5.1 runtime | PASS | OAT completed without parser/binding error after compatibility fixes |
| Pilot projection selected | PASS | `eagle-health-pilot.json` |
| Required signal set complete | PASS | `13 required / 13 present / 0 missing` |
| Summary policy remains disabled | PASS | `Summary: UNKNOWN; policy_enabled=False` |
| Safety boundary preserved | PASS | `OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS` |
| Commissioned projection activated | NOT EXECUTED | OAT remained on pilot path |
| Scheduled Task/service installation | NOT EXECUTED | Outside this OAT scope |
| Health severity classification | NOT EXECUTED | Policy remains disabled |
| Equipment/Safety action | NOT EXECUTED | Collector remains observational/read-only |
| Acceptance | NOT EXECUTED | Explicitly excluded by OAT result |

## 5. Compatibility defects encountered and corrected

Two Windows PowerShell 5.1 compatibility defects were exposed by the EAGLE runtime before the successful run:

1. interpolated strings using `$name:` were parsed as invalid variable references; fixed by delimiting as `${name}`;
2. `$PSScriptRoot` was not safely available inside the parameter default expression for `ConfigPath`; fixed by resolving the default path in the script body after parameter binding.

The successful OAT was executed only after both fixes were pulled to the EAGLE clone.

## 6. Gate interpretation

**G5 precommissioning OAT: PASS.**

This result means the current pilot projection and precommissioning guardrails are runtime-valid on `EAGLE30154` for the tested execution. It does **not** mean BKL-030 is commissioned or accepted.

BKL-030 remains `Planned` while dependency BKL-029 is open. Commissioned output `eagle-health.json`, permanent runtime installation, policy activation and acceptance remain blocked until the governed dependency and later gates are satisfied.

## 7. Safety statement

No device, mount, dome, relay, power controller, router, SafetyMonitor or other actuator command was part of this OAT. Local physical interlocks remain authoritative and independent of EAGLE Health telemetry availability.
