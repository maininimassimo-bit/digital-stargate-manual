# CAP-SAF-001 - Technical Manual

## Purpose

This manual defines conceptual responsibilities, interfaces, dependencies, inputs, outputs, operational considerations and safety principles for Observatory Safety.

## Responsibilities

| Area | Responsibility |
|---|---|
| Safety authority | Provide the authoritative conceptual safety decision for Core Observatory operations. |
| Policy evaluation | Evaluate safety inputs against governed safety policy and rules. |
| Fail-safe posture | Ensure unknown, disabled, unsafe or emergency conditions do not authorize unattended observation. |
| Decision output | Provide allow, suspend, abort, safe mode, recovery and audit outputs. |
| Traceability | Record inputs, rule, assessment, state, operator decision and action evidence. |
| Recovery support | Determine whether recovery is allowed after unsafe or emergency state. |

## Safety Principles

- Safety decisions take precedence over observation continuity.
- `Unknown` is not `Safe`.
- `Disabled` is not `Safe`.
- Safety consumes weather and equipment evidence but does not own weather sensing or equipment registry authority.
- Safety provides policy decision support; OSM owns session lifecycle execution.
- Hardware and PLC behavior are outside this package.
- Operator decisions must be auditable.

## Conceptual Interfaces

| Interface | Provider | Consumer | Input | Output |
|---|---|---|---|---|
| Weather Safety Context | Weather Monitoring | Observatory Safety | Weather state, alerts, freshness | Safety input. |
| Equipment Safety Context | Equipment Registry | Observatory Safety | Equipment/roof/power-related context | Safety input. |
| Session Context | OSM | Observatory Safety | Active session and lifecycle state | Safety assessment context. |
| Schedule Context | Scheduling | Observatory Safety | Planned observation and window | Allow/block decision. |
| Safety Decision | Observatory Safety | OSM, Scheduling, Operations | Safety assessment and state | Allow, suspend, abort, safe mode, recovery allowed. |
| Audit Evidence | Observatory Safety | Knowledge / Governance | Safety decision data | Audit Record. |

## Inputs

- Weather Monitoring state and alerts.
- Observation Session state.
- Equipment Registry readiness and lifecycle context.
- Observation Scheduling context.
- Target constraints when relevant.
- Manual operator decision or emergency call.
- Maintenance activity context.
- Power status.
- Roof status.
- Communication status.

## Outputs

- Allow Observation.
- Suspend Observation.
- Abort Observation.
- Close Roof Request.
- Safe Mode.
- Recovery Allowed.
- Operator Notification.
- Audit Event.

## Operational Considerations

- Safety state should be evaluated before schedule approval, before session start and during active operation.
- Emergency state should trigger emergency runbook handling and audit evidence.
- Recovery should require fresh evidence and explicit validation.
- Maintenance and Disabled states should block normal observing unless future governance permits a specific exception.
- Future implementation must resolve open decisions before the affected behavior is built.

## Configuration Governance

| Topic | Status |
|---|---|
| Safety rule priority | OPEN until approved. |
| Policy versioning | OPEN until approved. |
| Decision freshness | OPEN until approved. |
| Operator override | OPEN until approved. |
| Audit retention | OPEN until approved. |
