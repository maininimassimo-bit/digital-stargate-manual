# SOL-OSM-ADR-001 — Local-First Session Orchestration

- **Status:** Proposed
- **Date:** 2026-07-28
- **Decision owner:** Digital StarGate Architecture
- **Related capability:** CAP-OSM-001

## Context

Observation sessions must remain safe and operationally governable when Internet connectivity is unavailable or unstable. The observatory already relies on a local control environment and independent safety mechanisms.

## Decision

Place the primary session orchestration, state persistence and evidence capture on the local observatory control node. Remote services may support planning, analytics, backup and supervision, but they are not required for the minimum safe runtime path.

## Consequences

### Positive

- WAN failure does not remove session governance.
- Safety decisions remain close to the controlled equipment.
- Evidence can be captured before synchronization.
- Latency and dependency on remote services are reduced.

### Negative

- Local backup and recovery require disciplined implementation.
- Remote visibility may be delayed during connectivity loss.
- Local resource constraints must be monitored.

## Rejected alternatives

- Cloud-only orchestration: rejected because WAN loss would become an operational dependency.
- Direct remote device control without a local orchestrator: rejected because it weakens lifecycle governance and evidence consistency.
