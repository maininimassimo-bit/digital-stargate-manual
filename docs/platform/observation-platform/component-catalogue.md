# Component Catalogue

## 1. Purpose

The component catalogue identifies the concrete software modules and adapters expected in the first implementation baseline.

## 2. Core components

| Component ID | Component | Type | Main responsibility |
|---|---|---|---|
| CMP-OBS-001 | Platform Host | Runtime | Hosts platform services on the observatory control computer |
| CMP-OBS-002 | Command API | Application | Exposes commands and status to operators and automation clients |
| CMP-OBS-003 | Session Engine | Application | Executes the observation session state machine |
| CMP-OBS-004 | Safety Evaluator | Application | Evaluates operational safety and revokes permission when required |
| CMP-OBS-005 | Equipment Coordinator | Application | Controls ordered equipment startup and shutdown |
| CMP-OBS-006 | Configuration Repository | Data | Stores profiles, thresholds, plans and policies |
| CMP-OBS-007 | Operational Event Store | Data | Stores commands, events and state transitions |
| CMP-OBS-008 | Telemetry Agent | Agent | Collects host and equipment metrics |
| CMP-OBS-009 | Notification Dispatcher | Application | Sends alerts and completion notifications |

## 3. Integration adapters

| Adapter ID | Adapter | Target |
|---|---|---|
| ADP-OBS-001 | N.I.N.A. Adapter | Sequence execution and imaging status |
| ADP-OBS-002 | PHD2 Adapter | Guiding start, stop and health |
| ADP-OBS-003 | CPWI or Mount Adapter | Slew, park, tracking and mount state |
| ADP-OBS-004 | ASCOM Equipment Adapter | Camera, focuser, filter wheel and related devices |
| ADP-OBS-005 | Roof or Dome Adapter | Open, close, stop and position state |
| ADP-OBS-006 | Weather Adapter | Cloud, rain, wind, humidity and derived safety state |
| ADP-OBS-007 | Power Control Adapter | Relay and power-channel operations |
| ADP-OBS-008 | Network Status Adapter | WAN, VPN and local connectivity state |

## 4. Component states

Each runtime component must expose at least:

- `starting`;
- `ready`;
- `degraded`;
- `unavailable`;
- `stopping`;
- `stopped`.

## 5. Versioning

Components and adapters must publish:

- semantic version;
- supported contract version;
- configuration schema version;
- build identifier;
- runtime environment information.

## 6. Ownership

Each catalogue entry must eventually include a named owner, source repository, deployment unit and support status before the platform can move from Draft to Approved.
