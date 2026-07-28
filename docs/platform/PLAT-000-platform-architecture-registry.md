# PLAT-000 — Platform Architecture Registry

## 1. Purpose

This registry provides the authoritative index of Digital StarGate platform architectures and their relationship with enterprise domains, capabilities and solution architectures.

## 2. Scope

The registry covers software platforms that host, coordinate or expose reusable services for observatory operations, automation, safety, data management and remote control.

## 3. Registered platforms

| Platform ID | Platform name | Status | Primary solution | Primary capabilities |
|---|---|---|---|---|
| PLAT-OBS-001 | Observation Automation Platform | Draft | SOL-OSM-001 Observation Session Management | Session planning, orchestration, equipment control, safety supervision, telemetry |

## 4. Architecture principles

1. **Safety overrides automation.** Any unsafe condition can interrupt or inhibit an observation session.
2. **Local-first execution.** Core runtime operations must continue when external connectivity is degraded.
3. **Loose coupling.** Device-specific integrations are isolated behind adapters.
4. **Observable by design.** Every significant command, state transition and recovery action is recorded.
5. **Configuration as data.** Equipment profiles, policies and thresholds are versioned and auditable.
6. **Deterministic recovery.** Failures must transition the platform to a known and safe state.

## 5. Traceability

| Architecture layer | Reference |
|---|---|
| Enterprise Architecture | `EA-000` Enterprise Architecture Baseline |
| Domain Architecture | `DOM-001` Core Observatory Domain |
| Capability Architecture | `CAP-000` Capability Registry |
| Solution Architecture | `SOL-OSM-001` Observation Session Management |
| Platform Architecture | `PLAT-OBS-001` Observation Automation Platform |

## 6. Governance

New platform records must include:

- platform identifier and owner;
- supported solutions and capabilities;
- service and component catalogue;
- integration and deployment model;
- operational and security requirements;
- lifecycle status and review date.

## 7. Lifecycle states

- **Proposed** — initial concept awaiting review;
- **Draft** — architecture under active definition;
- **Approved** — accepted as implementation baseline;
- **Operational** — deployed and in active use;
- **Deprecated** — retained for transition only;
- **Retired** — no longer in use.
