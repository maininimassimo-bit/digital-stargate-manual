# AP-008 Governance Gate Closure Package — 2026-09-22

| Campo | Valore |
|---|---|
| Package | AP-008 |
| Pilot | INT-SESSION-METADATA-PILOT-001 |
| Accountable owner | Massimo Mainini |
| Scope of this package | governare il passaggio da shadow pilot a eventuale integrazione read-only |
| Runtime mode | shadow only |
| Current decision | NOT_READY — exception requested, not effective |
| Production traffic | unchanged; 100% on `dsg-observatory-status-relay-00005-rof` |

## 1. Purpose and boundary

This package consolidates the completed technical evidence and identifies the governance
actions that still require named human owners, independent security review and ARB decision.
It does not authorize live activation, `runtime_event_published=true`, a broker, scheduler,
command path or Safety Authority integration.

## 2. Gate status

| Gate | Status | Evidence or blocking action |
|---|---|---|
| G0 accountable owner | PASS | Massimo Mainini recorded as AP-008 accountable owner |
| G1 bounded transport | PASS — shadow scope only | HTTPS Cloud Run relay, bearer-authenticated ingest, read-only GET, persistent bucket `/data`, 0% canary traffic |
| G2 distinct role assignment | PASS — interim waiver | Massimo Mainini assigned to all four interim operational roles under `W-AP008-INTERIM-OWNERS-2026-09-22`; segregation remains a condition for live approval |
| G3 security/trust review | AI-ASSISTED WITH CONDITIONS | Owner-authorized review published under waiver; independent human review remains required |
| G4 live adapter compatibility | NOT APPLICABLE to shadow / BLOCKED for live | No live adapter or live contract activation is authorized |
| G5 consumer reconciliation | PASS — technical read-model scope | Observatory, EAGLE Health and shadow read-backs reconciled; independent portal/consumer replay remains a separate condition |
| G6 disable/rollback drill | PASS — shadow scope | No producer was active, timestamps remained unchanged for 20 seconds, then both producers restored fresh snapshots |
| G7 independent ARB re-review | PENDING | Submit this package after G2-G6 closure; no new decision is recorded here |
| G8 live readiness | BLOCKED | Remains `NOT_READY` until G2-G7 are independently evidenced |

## 3. Executed and verified

- Cloud Run revisions `00014-bux` and `00015-hak` were deployed with 0% production traffic.
- Production remained on `00005-rof` as rollback baseline.
- Persistent `/data` bucket continuity was verified across revisions.
- Observatory Status, EAGLE Health and SessionCompleted shadow read-backs returned HTTP `200`
  after the controlled revision sequence.
- SessionCompleted retained message ID
  `shadow-2026-09-21_2026-09-22-714a67f66799824e`.
- Duplicate SessionCompleted delivery returned HTTP `200` with `NO_OP` and did not append a
  second event.
- Stale snapshots return `404 snapshot_unavailable` and are not served as current data.
- `/v1/command` returned `404`.
- Bearer secret injection and the `EAGLE30154` authorized-source boundary were preserved.

Primary execution evidence:

- `docs/architecture/validation/AP008-SessionCompleted-Live-Shadow-OAT-Plan-2026-09-22.md`
- `docs/architecture/validation/evidence/AP008-SessionCompleted-Live-Shadow-OAT-Execution-2026-09-22.md`

## 4. Not executed

- No independent human security/trust review has been recorded for the relay and future live
  adapter boundary.
- No distinct adapter, consumer, security and operations owners have been assigned; an
  interim same-person assignment is recorded below and does not satisfy independence.
- No independent portal-side replay, divergence, partial-publication or recovery report has
  been attached; this remains a live-governance condition.
- No new ARB decision has been recorded after the technical canary completion.

## 5. Blocked

AP-008 cannot be declared `live-ready` because the remaining gates require authority that is
not inferable from technical execution logs:

1. distinct role owners, with separation between accountable owner and independent reviewers;
2. independent security/trust-boundary disposition;
3. independent consumer reconciliation evidence;
4. new ARB decision explicitly covering the bounded read-only scope.

## 6. Required owner actions

| Action | Required decision | Current state |
|---|---|---|
| Assign adapter owner | named person/account | Massimo Mainini — INTERIM |
| Assign consumer/portal owner | named person/account | Massimo Mainini — INTERIM |
| Assign security reviewer | independent reviewer | Massimo Mainini — INTERIM; independence not satisfied |
| Assign operations owner | named rollback/disable operator | Massimo Mainini — INTERIM |
| Approve bounded transport scope | read-only shadow or future read-only live scope | SHADOW SCOPE VERIFIED; LIVE SCOPE PENDING ARB |
| Record ARB disposition | approve, approve with conditions, or reject | PENDING |

## 7. Interim authorization and waiver

On 2026-09-22 the AP-008 accountable owner authorized the interim assignment of Massimo
Mainini to all four operational roles:

- read-only session adapter owner;
- consumer/portal reconciliation owner;
- security/trust review coordinator;
- disable/rollback operations owner.

This is recorded as waiver `W-AP008-INTERIM-OWNERS-2026-09-22`. It is limited to governance
coordination and shadow-pilot continuation. It does not create independent security approval,
satisfy four-eyes or segregation-of-duties requirements, create an ARB decision, or authorize
production promotion/live activation. The waiver must be replaced by distinct named owners and
an independent reviewer before any live-readiness decision.

## 8. Non-negotiable decision constraints

- `runtime_event_published` remains `false`.
- `safety_authority` and `command_authority` remain `NONE`.
- No broker, scheduler, command route or device-control integration may be introduced by
  closing this package.
- Production traffic must remain on the rollback revision until the ARB decision is recorded.

## 9. Decision

Technical OAT completion is recorded. Governance closure is not yet achieved. The authoritative
status remains:

`AP-008 = NOT_READY_FOR_LIVE_INTEGRATION`

An owner authorization to elevate readiness was recorded as an exception request, but it is not
effective because the independent security/trust review and ARB decision remain mandatory. See
`AP008-Readiness-Exception-Request-2026-09-22.md`.
