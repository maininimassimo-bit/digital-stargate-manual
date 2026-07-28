# Service Decomposition

## 1. Purpose

This document defines the platform services required to implement `SOL-OSM-001` while preserving clear responsibility boundaries.

## 2. Service map

| Service | Responsibility | Criticality |
|---|---|---|
| Command Gateway | Receives authenticated operator and automation commands | High |
| Session Orchestrator | Coordinates the end-to-end observation workflow | Critical |
| Safety Policy Service | Evaluates whether operations are permitted | Critical |
| Equipment Coordination Service | Sequences device initialization and shutdown | Critical |
| Scheduler Service | Selects and activates observation plans | Medium |
| Configuration Service | Supplies equipment profiles, thresholds and policies | High |
| Event Store | Persists state transitions and operational evidence | High |
| Telemetry Collector | Collects metrics and device status | High |
| Notification Service | Delivers alerts and session outcomes | Medium |
| Health and Diagnostics Service | Exposes readiness, liveness and dependency health | High |

## 3. Responsibility boundaries

### Command Gateway

The gateway validates commands, assigns a correlation identifier and routes the request to the correct service. It does not contain session logic.

### Session Orchestrator

The orchestrator owns the session state machine and coordinates calls to safety, equipment and integration services. It does not directly communicate with vendor drivers.

### Safety Policy Service

The safety service evaluates weather, roof or dome status, power state, connectivity and configured thresholds. It can deny or revoke permission to operate.

### Equipment Coordination Service

This service manages ordered startup and shutdown across mount, camera, focuser, guiding, roof or dome and supporting power channels.

### Scheduler Service

The scheduler selects a plan according to time window, target visibility, equipment profile and operator constraints. It may request a session start but cannot bypass safety checks.

## 4. Service interaction rules

1. All commands carry a correlation identifier.
2. Services must be idempotent where retries are expected.
3. Safety decisions are authoritative and cannot be overridden by the scheduler.
4. Device commands must be issued through adapters.
5. State changes must be emitted before dependent actions continue.
6. Timeouts and retry limits must be explicit.

## 5. Initial implementation approach

The first implementation may run as a modular monolith on the local observatory host while preserving service boundaries in code. Services may later be separated without changing their contracts.
