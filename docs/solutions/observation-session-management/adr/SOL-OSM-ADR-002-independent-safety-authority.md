# SOL-OSM-ADR-002 — Independent Safety Authority

- **Status:** Proposed
- **Date:** 2026-07-28
- **Decision owner:** Digital StarGate Architecture
- **Related capability:** CAP-SAF-001, CAP-OSM-001

## Context

Session orchestration requires safety information but must not become the sole authority responsible for roof closure, interlocks or emergency behavior.

## Decision

Maintain the safety controller as an independent authoritative component. SOL-OSM-001 consumes safety state and requests governed actions but cannot override an authoritative `UNSAFE` condition.

## Consequences

- Failure of the orchestrator does not eliminate the safety path.
- Integration must support authoritative state verification.
- Conflicting commands are resolved in favor of safety.
- Testing must include loss of the orchestration node while safety remains active.
