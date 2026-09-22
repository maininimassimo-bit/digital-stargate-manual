# BKL-036-F5 — Live Read-Only Health Score

| Field | Value |
|---|---|
| Package | BKL-036-F5 |
| Status | CLOSED / ACCEPTED / POST-MERGE VERIFIED |
| Owner / accountable | Massimo Mainini |
| Dependency | AP-008 bounded live read-only integration |
| Authority | Projection only; `action_authority=NONE` |
| Safety | Local physical interlocks remain the only Safety Authority |

## Purpose

Define the next governed increment after the accepted repository-only BKL-036 capability.
F5 will determine whether a descriptive numeric score can be calculated from the AP-008 live
read-only projections without turning telemetry into readiness, safety or command authority.

## Mandatory domains

The score may be available only when all seven domains are independently mapped, fresh,
schema-valid and comparable:

1. weather;
2. dome;
3. mount;
4. camera;
5. power;
6. network;
7. EAGLE Health.

Missing, stale, malformed or conflicting evidence yields `UNAVAILABLE`; no partial score is
allowed. The existing archived-evidence F3 projection remains unchanged.

## Proposed live evidence envelope

Each domain must carry source component, observed timestamp, freshness deadline, quality,
authority, correlation identifier and a compatibility classification. The aggregate projection
must expose the domain matrix and reasons, not only a scalar. A score is descriptive and must be
labeled non-authoritative, read-only and separate from BKL-032 readiness/go-no-go.

## Explicit exclusions

F5 does not introduce broker, scheduler, device command, remediation, automatic target
selection, Safety Authority, `runtime_event_published=true`, or a replacement for BKL-032.
The AP-008 producer scheduler remains a transport publisher only.

## Acceptance gates

- source-to-domain mapping reviewed and versioned;
- live envelope schema and compatibility rules validated;
- freshness, missingness, conflict and failure tests pass;
- portal rendering preserves `UNKNOWN`/`STALE`/`UNAVAILABLE` semantics;
- independent ARB and Release Quality review complete;
- owner-authorized production OAT records all seven domain read-backs;
- rollback returns to descriptive `UNAVAILABLE` without changing safety or command boundaries.

Until these gates pass, the portal must continue showing the current F3 archived-evidence
projection and its explicit `UNAVAILABLE` result.

## Current gate result

The source mapping and live envelope contract are now versioned in
`BKL-036-F5-SOURCE-MAPPING-2026-09-22.md`, with a fail-closed `UNAVAILABLE` fixture and
validator. The first live OAT also recorded all seven read-backs: six Observatory domains
were comparable, while EAGLE Health was current but semantically `UNKNOWN` because
`POLICY_NOT_ACTIVATED`. The aggregate therefore remains `UNAVAILABLE`; ARB/RQ and policy
review remain open.

The owner-confirmed EAGLE comparability policy is versioned in
`BKL-036-F5-EAGLE-HEALTH-POLICY-2026-09-22.md` and is now active in production. The final
read-only OAT returned `HEALTHY`, `CURRENT`, `score=100`, `reason=ALL_REQUIRED_SIGNALS_HEALTHY`
with all five mandatory EAGLE signals current. The rendered GitHub Pages consumer was directly
verified with the same live values. Post-merge acceptance is recorded in
`docs/project/BKL-036-F5-CLOSURE-2026-09-23.md`.
