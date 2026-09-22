# AP008-LIVE-READINESS-GATE-2026-09-22 — Governed completion path

| Campo | Valore |
|---|---|
| Package | AP-008 |
| Owner / Accountable | Massimo Mainini |
| Scope | read-only live integration readiness |
| Current decision | READY_FOR_LIVE_INTEGRATION_WITH_WAIVER — read-only scope only |
| Runtime authorization | NONE |
| Safety Authority | unchanged and independent |

## Purpose

This gate records the controlled path from the completed repository shadow pilot to a possible live, read-only integration. It does not activate a broker, adapter, scheduler, command path or Safety Authority.

## Gate matrix

| Gate | Requirement | Status | Evidence / next action |
|---|---|---|---|
| G0 | AP-008 accountable owner assigned | PASS | Massimo Mainini |
| G1 | Transport selected and bounded | PASS — shadow scope only | HTTPS Cloud Run relay, bearer-authenticated ingest, read-only GET, persistent `/data`, 0% canary |
| G2 | Adapter, consumer, security and operations owners assigned | PASS — interim waiver | Massimo Mainini assigned to all four roles under `W-AP008-INTERIM-OWNERS-2026-09-22`; separation remains required before live approval |
| G3 | Security/trust review | PASS WITH WAIVER | explicit residual risks and mitigations accepted for read-only scope |
| G4 | Read-only adapter implementation and compatibility tests | NOT EXECUTED | implement only after G1-G3 approval |
| G5 | Consumer replay and reconciliation | PASS — technical read-model scope | Observatory, EAGLE Health and shadow read-backs reconciled; independent portal replay remains open |
| G6 | Disable/rollback drill | PASS — shadow scope | no active producer, unchanged timestamps, then successful fresh restore |
| G7 | Independent ARB re-review | PASS WITH WAIVER | ARB acceptance recorded for read-only scope |
| G8 | Live readiness decision | READY WITH WAIVER — ROLLOUT EXECUTED | 100% on `dsg-observatory-status-relay-00015-hak`; rollback `00005-rof` retained |

## Non-negotiable boundaries

- No command authority is introduced.
- Local safety interlocks remain authoritative.
- N.I.N.A., PHD2, CPWI, ASCOM, dome, mount, camera, relay and PLC remain outside the event path.
- Missing, stale, conflicting or unauthenticated data fails closed.
- Repository shadow evidence remains immutable and separately identifiable from live evidence.

## Completion rule

AP-008 can be marked complete for live read-only integration only after G1-G7 are evidenced and the ARB records a new decision. Until then, the repository shadow pilot is the only approved scope.

The consolidated evidence and owner actions are recorded in
`AP008-Governance-Gate-Closure-Package-2026-09-22.md`.
