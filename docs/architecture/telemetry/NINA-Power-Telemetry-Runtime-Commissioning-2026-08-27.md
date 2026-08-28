# N.I.N.A. TS Shelter J6 Power Telemetry — Runtime Commissioning Evidence

| Campo | Valore |
|---|---|
| Scope | BKL-027 / BKL-028 — Observatory Status Power source and integration |
| Runtime host | `EAGLE30154` |
| Source | Tecnosky TS Shelter Board J6 voltage supervision |
| Driver | `ASCOM.TS_Shelter.SafetyMonitor` |
| Integration boundary | Digital StarGate N.I.N.A. Observatory Telemetry Exporter |
| Data test fisico | 2026-08-27 |
| Stato | **POWER ACCEPTANCE PASS — source, mapping, runtime integration and portal visibility verified** |

## 1. Physical source architecture

The observatory uses a dedicated 230 V AC to 12 V DC sensing power supply connected to the Tecnosky TS Shelter Board J6 voltage-supervision input.

The sensing supply is intentionally outside battery backup. The TS Shelter Board remains powered from the backed-up power path. Therefore:

```text
Mains present
  -> sensing PSU produces 12 V
  -> J6 voltage present
  -> no mains-loss fault

Mains blackout
  -> sensing PSU loses 230 V
  -> J6 voltage disappears
  -> TS Shelter Board remains alive on backup power
  -> mains-loss condition becomes observable
```

This source observes mains presence; it is not a measurement of battery state or UPS autonomy.

## 2. ASCOM discovery

Runtime discovery on `EAGLE30154` verified the registered SafetyMonitor ProgID:

```text
ASCOM.TS_Shelter.SafetyMonitor
```

The driver exposes the standard SafetyMonitor state plus a read-only diagnostic query through:

```text
CommandString("safeties", false)
```

Static inspection established that the diagnostic result is backed by the driver's `moni_safety_status` integer state. `IsSafe` remains an aggregate SafetyMonitor verdict and is not used as a synonym for Power state.

## 3. Read-only baseline test

With normal mains supply and J6 sensing present:

```text
Connected   = True
IsSafe      = True
SafetiesRaw = 0
```

The query did not operate relays, switch outputs, dome controls, router configuration or any other actuator.

## 4. Controlled J6 source-loss test

A controlled commissioning test removed only the dedicated 12 V sensing supply connected to J6. The TS Shelter Board, EAGLE, LAN, router and backed-up observatory equipment remained powered.

The configured TS Shelter Power delay was allowed to expire before observation.

Observed transition:

```text
Baseline
Time        : 2026-08-27 17:20:52 local
Connected   : True
IsSafe      : True
SafetiesRaw : 0

J6 sensing absent
Time        : 2026-08-27 17:23:24 local
Connected   : True
IsSafe      : False
SafetiesRaw : 1

J6 sensing restored
Time        : 2026-08-27 17:25:15 local
Connected   : True
IsSafe      : True
SafetiesRaw : 0
```

The measured bit transition is therefore:

```text
0 -> 1 -> 0
```

and the commissioned mains-loss mask is:

```text
PowerMask decimal = 1
PowerMask hex     = 0x00000001
```

No bit value was assumed before the physical test; the mask is based on observed runtime evidence.

## 5. Semantic mapping

The Digital StarGate Power adapter uses only bit `0x00000001` for mains-state telemetry:

```text
(safetiesRaw & 0x00000001) == 0
  -> MAINS_PRESENT

(safetiesRaw & 0x00000001) != 0
  -> MAINS_LOST

source unavailable / parse failure / COM failure
  -> UNKNOWN
```

Other SafetyMonitor reasons remain independent. An aggregate `UNSAFE` caused by rain or other configured conditions must not by itself imply `MAINS_LOST`.

## 6. N.I.N.A. plugin boundary

Power telemetry is integrated inside the existing Digital StarGate N.I.N.A. Observatory Telemetry Exporter, together with the previously commissioned passive Network adapter.

The architectural boundary is:

```text
TS Shelter Board J6
  -> ASCOM.TS_Shelter.SafetyMonitor
  -> read-only safeties diagnostic
  -> PowerTelemetryAdapter
  -> N.I.N.A. Digital StarGate plugin projection
  -> canonical Observatory Status producer
  -> Cloud Run relay
  -> Observatory Status portal
```

This preserves the design decision that Network and Power collection belong to the N.I.N.A. plugin rather than to independent sidecar producers.

## 7. Fail-safe behavior

Power telemetry follows the same fail-safe rule as the other N.I.N.A.-owned telemetry:

- no fresh observation means no retained assertion of current healthy state;
- adapter/source failure maps to `UNKNOWN`;
- the portal does not treat stale observations as current;
- Power telemetry remains observational and does not become a Safety Authority.

The existing physical Safety chain remains authoritative.

## 8. Observatory Status verification

The Observatory Status page was verified after the Power integration and is correctly populated with the newly added Power/Alimentazione state together with the other realtime telemetry.

The dedicated Power KPI is therefore considered runtime-visible and operational.

This verifies the complete path:

```text
J6 physical sensing
  -> TS Shelter ASCOM state
  -> Digital StarGate N.I.N.A. plugin
  -> local projection
  -> canonical projection
  -> hosted transport
  -> Observatory Status UI
```

## 9. Safety and side-effect disposition

The commissioning introduced no command path toward observatory equipment:

- no power relay switching;
- no dome command;
- no mount command;
- no camera command;
- no WAN/router configuration change;
- no battery/UPS control;
- no replacement of the existing N.I.N.A. SafetyMonitor Hub;
- no elevation of portal telemetry to Safety Authority.

The only physical test action was removal and restoration of the dedicated J6 mains-sensing 12 V source.

## 10. Acceptance decision

**PASS.** The Power workstream satisfies the acceptance requirements:

1. physical source identified and documented;
2. read-only software source identified and verified;
3. J6 mains-loss mask measured at runtime (`0x00000001`);
4. healthy -> lost -> restored transition verified (`0 -> 1 -> 0`);
5. Power semantics separated from aggregate SafetyMonitor `IsSafe`;
6. adapter integrated inside the Digital StarGate N.I.N.A. telemetry plugin;
7. fail-safe `UNKNOWN` behavior retained for missing/unreadable source;
8. canonical/hosted Observatory Status path populated;
9. Power KPI visible and correct on the Observatory Status page;
10. no operational command path introduced.

**BKL-027 source discovery and BKL-028 Power/Network integration are accepted as complete.**

Future UPS battery/autonomy telemetry, if required, is a separate capability and must not be inferred from the J6 mains-presence signal.
