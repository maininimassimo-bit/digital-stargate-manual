# AP-008 ARB Re-Review — AI-Assisted, Owner-Authorized — 2026-09-22

| Campo | Valore |
|---|---|
| Review ID | `ARB-AP008-AI-RR-2026-09-22` |
| Review mode | AI-assisted, owner-authorized |
| Independent human ARB review | NO — explicitly not equivalent |
| Decision | APPROVED WITH ACCEPTED RISKS — READ-ONLY SCOPE |
| Live integration | READY WITH WAIVER |

## Evidence considered

- technical OAT completion and Cloud Run canary continuity;
- persistent `/data` bucket and cross-revision read-back;
- shadow idempotency and duplicate `NO_OP`;
- freshness fail-closed behavior;
- Observatory Status and EAGLE Health read-model reconciliation;
- disable/no-new-artifact/restore drill;
- interim owner waiver;
- AI-assisted security/trust review and its independence waiver;
- readiness exception request.

## Findings

| Finding | Severity | Decision |
|---|---|---|
| Shadow boundary, no command path and local authority preservation | — | PASS for shadow |
| Technical OAT and rollback evidence | — | PASS for shadow |
| Interim same-person ownership | Major | accepted under owner waiver for bounded read-only scope |
| Security/trust review is owner-witnessed under waiver | Major | accepted risk; replace with independent review when available |
| Portal-side independent replay/divergence evidence | Major | technical read-model reconciliation passed; portal evidence remains a follow-up control |
| Live adapter/broker/scheduler semantics | Blocker outside scope | not implemented or authorized |
| Production promotion | Controlled action | allowed only for bounded read-only scope after preflight |

## Conditions

1. Continue only within the bounded read-only scope.
2. Preserve `runtime_event_published=false`, `safety_authority=NONE` and
   `command_authority=NONE`.
3. Retain the accepted-risk register and one-hour rollback rule.
4. Replace owner-witnessed waivers with independent human review when available.

## Decision

The AP-008 bounded read-only integration is approved with accepted risks and owner-witnessed
waivers. This is a readiness decision only; it does not activate command, broker, scheduler or
Safety Authority semantics.
