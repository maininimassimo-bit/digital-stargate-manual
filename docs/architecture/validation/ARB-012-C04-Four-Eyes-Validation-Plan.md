# ARB-012-C04 — Four-Eyes Validation Plan

| Field | Value |
|---|---|
| Plan ID | ARB-012-C04-W04-PLAN-001 |
| Work item | C04-W04 — Four-Eyes Validation Plan |
| Package | AP-012 |
| Updated | 2026-08-22 |
| Target model | Two-Person Limited Operations Model |
| Environment | Isolated non-operational validation environment |
| Status | Approved/reconciled plan; execution not started |
| Runtime effect | None |

## 1. Scope

The campaign validates what the two-person model actually supports and proves denial of what it does not support:

- C3 request and distinct approval;
- self-approval/conflict rejection;
- revocation effectiveness;
- Maintainer / Return-to-Service separation;
- Safety Authority separation from Operations;
- Security Authority self-access denial;
- audit-trail completeness as repository/technical traceability, not independent internal audit;
- positive C4 denial;
- break-glass denial;
- evidence traceability.

## 2. Entry criteria

| Criterion | Required state before positive C3 execution |
|---|---|
| Sponsor two-person target | Available |
| Role/conflict register | Available |
| IDV-001–IDV-005 | Passed |
| Applicable TRN evidence | Passed / approved exception |
| AR-001–AR-006 | Attributable decisions |
| AR-007 | N/A by governance design |
| AR-008 positive C4 | Denied |
| AR-009 break-glass | Denied |
| Distinct ACC-001/ACC-002 sessions | Verified |
| Applicable isolated ENV controls | Passed |

No third observer is an entry criterion.

## 3. Participants

| Participant | Validation role | Prohibited combination |
|---|---|---|
| Massimo Mainini | Requester, Operator, Maintainer, Sponsor for bounded revocation governance | approve own C3 request; approve own return-to-service; self-grant privileged access |
| Leonardo Di Egidio | C3 Approver, Safety Authority, Security Authority, Return-to-Service Approver | requester+approver same action; approve own access; claim independent audit over own controls |

## 4. Required scenarios

| Test | Scenario | Expected result | Required for closure |
|---|---|---|---|
| FE-01 | Massimo C3 request -> Leonardo approval | positive flow only after distinct approval | Yes |
| FE-02 | Massimo attempts self-approval | Denied, audited, no execution | Yes |
| FE-03 | Leonardo attempts requester+approver conflict | Denied | Yes |
| FE-04 | Leonardo approval eligibility suspended by Sponsor before execution | stale approval invalidated; execution denied | Yes |
| FE-05 | Massimo eligibility revoked by Leonardo Security Authority | execution denied | Yes |
| FE-06 | Massimo maintenance -> Leonardo return-to-service | service remains unavailable until distinct approval | Yes |
| FE-07 | Massimo operation -> Leonardo Safety permit/deny/stop | bounded simulated decision; local interlocks untouched | Yes |
| FE-08 | Leonardo attempts to approve own access | Denied | Yes |
| FE-09 | audit/traceability completeness | requester, approver, roles, policy, timestamps and correlation IDs complete | Yes |
| FE-10 | positive C4 with only Massimo+Leonardo | **Denied by governance design** | Yes — denial evidence |
| FE-11 | break-glass request/approval | **Denied by governance design** | Yes — denial evidence |
| FE-12 | evidence tamper-resistance | modification remains prevented or repository-traceable | Yes |

No scenario requires or claims a third independent actor.

## 5. Evidence model

Every execution record shall contain test ID/version, timestamps, environment/software revision, requester/approver identities, effective roles, classification, simulated target, policy revision/result, correlation IDs, expected/actual result, logs/screenshots where safe, deviations and attributable executor/reviewer sign-off.

Failures must be preserved. Secrets and sensitive identity data must not be committed.

## 6. Execution order

1. validate applicable environment controls;
2. verify distinct accounts/sessions;
3. execute FE-02/FE-03 denial tests;
4. execute FE-01 positive C3;
5. execute FE-04/FE-05 revocation;
6. execute FE-06 return-to-service;
7. execute FE-07/FE-08 authority conflict tests;
8. execute FE-10/FE-11 prohibited paths;
9. execute FE-12 evidence integrity;
10. perform FE-09 technical/repository audit completeness review.

A failed denial test blocks later positive scenarios.

## 7. Stop conditions

Stop if physical observatory routes are reachable, shared credentials are detected, self-approval succeeds, revoked authorization remains executable, an action executes without the required C3 chain, local interlocks are bypassed, or evidence loses traceability.

## 8. Exit criteria

The campaign is complete when all FE-01…FE-12 have attributable evidence and expected results, including explicit denial for FE-10/FE-11. FE-09 demonstrates traceability completeness but is **not represented as independent organizational audit**.

Positive C4, break-glass, third-person approval, independent internal audit closure and runtime enablement remain outside the supported target.

## 9. Current disposition

**C04-W04: APPROVED/RECONCILED PLAN — NOT EXECUTED.**

The plan is ready after W03 and applicable W06/ENV prerequisites complete. ARB-012-C04 remains `Blocked` pending evidence.