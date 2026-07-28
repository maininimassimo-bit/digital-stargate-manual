# SOL-OSM-001 - Solution Overview

## Purpose

This document defines the solution context and design boundary for Observation Session Management. It separates the known observatory environment from the target Digital StarGate solution and records assumptions that require technical validation.

## Current Environment

The current environment contains established observatory products and infrastructure. Their exact versions, supported integration mechanisms and operational configuration require validation before implementation.

| Area | Known element | Classification | Validation status |
|---|---|---|---|
| Connectivity | Starlink Internet access | Existing infrastructure | Confirm active topology and failover behaviour |
| Gateway | Teltonika RUT955 | Existing product | Confirm routing, VPN and LTE failover configuration |
| Control computing | PrimaLuceLab EAGLE3 on Windows | Existing product | Confirm OS, services, storage and account model |
| Imaging orchestration | N.I.N.A. | Existing product | Confirm version, profile structure and supported automation interfaces |
| Guiding | PHD2 | Existing product | Confirm version, server/API availability and log locations |
| Mount control | CPWI and Celestron CGX-L | Existing products | Confirm connection chain and ASCOM exposure |
| Device integration | ASCOM Platform; Alpaca where applicable | Existing platform / candidate mechanism | Confirm driver inventory and actual Alpaca use |
| Imaging equipment | C8 XLT, Quattro 200P, QHY695A, ToupTek 294MC PRO and supporting devices | Existing equipment | Resolve authoritative profiles through `CAP-EQR-001` |
| Focusing and calibration | Pegasus FocusCube, ESATTO 2-inch, Wanderer Cover V4 | Existing equipment | Confirm active profiles and control interfaces |
| Enclosure | Motorised enclosure or roof with position/safety sensors | Existing physical system | Interface and fail-safe behaviour `TBD` |
| Environmental evidence | Weather sensing and Raspberry Pi AllSky | Existing supporting systems | Confirm authoritative source and data freshness rules |

This table is contextual. It does not replace the Equipment Registry or assert unsupported technical specifications.

## Target Solution

The target solution introduces a governed orchestration layer around existing products.

The target architecture shall:

- represent each observing session through a deterministic, auditable lifecycle;
- coordinate preparation, execution, pause, recovery, shutdown and closure;
- consume authoritative references from scheduling, equipment and target capabilities;
- consume weather assessment and safety authorisation without embedding their policy logic;
- integrate existing products through adapters;
- record state transitions, commands, acknowledgements, operator actions and evidence;
- retain safe local shutdown behaviour when remote connectivity is unavailable;
- support supervised implementation before any safety-constrained unattended operation.

## Design Principles

1. **Capability authority remains external.** The solution consumes capability decisions and does not redefine them.
2. **Safety overrides workflow.** A denied or withdrawn safety authorisation prevents ordinary progression and initiates the governed safe path.
3. **Local-first control.** Operational execution and safe shutdown shall not depend on continued Internet connectivity.
4. **Adapter isolation.** Product-specific mechanisms are isolated from the canonical session workflow.
5. **Deterministic state.** Commands and recovery decisions are associated with explicit states and auditable transitions.
6. **Evidence by design.** Session events and evidence are treated as required outputs, not optional diagnostics.
7. **Incremental automation.** Read-only observation and supervised commands precede automated orchestration.

## Assumptions

| ID | Assumption | Validation required |
|---|---|---|
| `SOL-OSM-ASM-001` | The EAGLE3 can host the proposed local orchestration runtime or connect to a dedicated local host. | Resource, operating-system and supportability assessment |
| `SOL-OSM-ASM-002` | N.I.N.A., PHD2 and CPWI expose sufficient control or telemetry mechanisms for supervised orchestration. | Version-specific interface validation |
| `SOL-OSM-ASM-003` | Weather and enclosure state can be consumed locally with bounded freshness. | Sensor, protocol and timeout validation |
| `SOL-OSM-ASM-004` | Safety authorisation can be represented as an explicit, queryable decision with evidence. | `CAP-SAF-001` implementation design |
| `SOL-OSM-ASM-005` | Session evidence can be persisted locally during Internet loss and synchronised later. | Storage and retention assessment |

## Constraints

- The solution shall not bypass existing product safety interlocks.
- The Safety capability is a policy and authorisation authority, not a PLC or device controller.
- Hardware controllers execute physical actions under governed commands and constraints.
- Master target and equipment data remain owned by `CAP-TGT-001` and `CAP-EQR-001`.
- Internet and VPN loss shall not prevent local safe shutdown.
- Real credentials, addresses, tokens and secrets shall not be stored in documentation.
- Unsupported integration claims shall remain `TBD`.
- The first implementation stages shall require operator supervision.

## Implementation Scope

The solution scope covers:

1. session definition and references;
2. eligibility, weather and safety validation;
3. equipment connectivity and preparation;
4. enclosure-opening authorisation;
5. mount, imaging, focusing, plate-solving and guiding coordination;
6. acquisition progress and meridian-flip coordination;
7. continuous health and safety monitoring;
8. pause, retry, resume, abort, shutdown and closure;
9. session outcome, logs, evidence and notifications.

## Out of Scope

- weather-threshold ownership;
- safety-policy ownership;
- target catalogue ownership;
- equipment master-data ownership;
- replacement of N.I.N.A., PHD2, CPWI or ASCOM;
- post-processing pipelines such as PixInsight processing;
- public portal implementation;
- autonomous emergency actions not already validated;
- production deployment in this documentation block.

## Dependencies

| Dependency | Required outcome |
|---|---|
| `CAP-OSM-001` | Governing session requirements and lifecycle intent |
| `CAP-SCH-001` | Eligible plan and scheduling context |
| `CAP-EQR-001` | Authoritative equipment profile references |
| `CAP-TGT-001` | Authoritative target references |
| `CAP-WEA-001` | Weather assessment and freshness evidence |
| `CAP-SAF-001` | Safety authorisation, denial and withdrawal |
| Enterprise Architecture | Application, integration, security, observability and technology constraints |
| `DOM-001` | Core Observatory capability collaboration boundary |

## Open Decisions

| ID | Decision | Status | Required evidence |
|---|---|---|---|
| `SOL-OSM-OD-001` | Runtime location: EAGLE3 or dedicated local host | Open | Capacity, resilience and supportability assessment |
| `SOL-OSM-OD-002` | Canonical persistence technology for session state and events | Open | Data-volume, reliability, backup and offline requirements |
| `SOL-OSM-OD-003` | N.I.N.A. integration mechanism | Open | Version-specific interface and command validation |
| `SOL-OSM-OD-004` | PHD2 telemetry and command mechanism | Open | Server/API and failure-mode validation |
| `SOL-OSM-OD-005` | Enclosure controller interface and acknowledgement model | Open | Controller, sensor and fail-safe assessment |
| `SOL-OSM-OD-006` | Notification channels and escalation ownership | Open | Operational communication requirements |
| `SOL-OSM-OD-007` | Local evidence retention and remote synchronisation strategy | Open | Storage, backup and recovery assessment |

## Technical Validation Exit Criteria

The package may progress beyond **Ready for Technical Validation** when:

- software versions and driver inventory are recorded;
- actual interfaces for N.I.N.A., PHD2, CPWI, weather and enclosure are verified;
- local runtime and persistence placement are selected;
- safety authorisation semantics are defined;
- offline and shutdown behaviour are tested conceptually against real controllers;
- unresolved decisions have owners and target dates.
