# ARB-012-C04 — Four-Eyes Validation Plan

| Field | Value |
|---|---|
| Plan ID | ARB-012-C04-W04-PLAN-001 |
| Work item | C04-W04 — Four-Eyes Validation Plan |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Date | 2026-07-31 |
| Approved by | Massimo Mainini — Project Owner / Architecture Sponsor |
| Environment | Isolated non-operational validation environment |
| Status | Approved plan; execution not started |
| Runtime effect | None |

## 1. Purpose

This plan defines the controlled validation scenarios required to demonstrate role separation, denial of self-approval, revocation effectiveness, return-to-service separation and audit completeness for ARB-012-C04.

Approval of this plan authorizes preparation of the validation campaign only. It does not authorize runtime commands, physical-device control, break-glass use, local-interlock bypass or operational deployment.

## 2. Scope

The campaign covers:

- C3 request and independent approval;
- rejection of self-approval;
- Maintainer and Return-to-Service Approver separation;
- Safety Authority separation from Operations;
- Security Authority separation from the access beneficiary;
- role suspension and approval revocation;
- audit-trail completeness;
- preservation of denied C4 and break-glass paths.

The campaign does not claim positive C4 validation, independent audit closure, substitute resilience or runtime readiness.

## 3. Dependencies and entry criteria

Execution may start only when all applicable entry criteria are evidenced:

| Entry criterion | Required evidence | Current status |
|---|---|---|
| Sponsor-approved role assignment | `ARB-012-C04-Sponsor-Nomination-Decision.md` | Available |
| Updated role and conflict register | `ARB-012-C04-Role-Assignment-Register.md` | Available |
| Identity checks IDV-001–IDV-005 | `ARB-012-C04-Identity-Training-Access-Review.md` | Pending |
| Role-relevant training | TRN evidence register | Pending |
| Least-privilege decisions | AR-001–AR-007 | Pending |
| Distinct authentication accounts | Identity assurance evidence | Pending |
| Isolated test environment | Environment baseline and connection inventory | Pending |
| Test data and simulated device adapter | Versioned fixtures/configuration | Pending |
| Evidence repository location | Stable evidence index | Pending |
| Independent validation observer for conflicted checks | Nomination record | Pending |

No positive scenario may be marked `Passed` while an applicable entry criterion remains pending.

## 4. Validation environment

The target environment shall be technically isolated from operational observatory devices.

Mandatory controls:

1. no route to physical roof motors, relays, mount, cameras or safety controllers;
2. simulated device endpoints or disabled-output adapters;
3. separate test database and audit store;
4. distinct authenticated sessions for Massimo Mainini and Leonardo Di Egidio;
5. deterministic test fixtures and correlation identifiers;
6. deny-by-default authorization policy;
7. timestamps synchronized to a documented time source;
8. logs preserved without credentials, secrets or identity-document data;
9. explicit environment banner indicating `NON-OPERATIONAL`;
10. rollback by environment reset without physical effect.

If any physical-device route is detected, the campaign must stop and the environment must be treated as unsafe for C04 validation.

## 5. Participants

| Participant | Validation role | Prohibited combination during the same scenario |
|---|---|---|
| Massimo Mainini | Requester, Operator, Maintainer, evidence recorder where not self-assessing | Approver of own request; Return-to-Service Approver for own maintenance; reviewer of own privileged access |
| Leonardo Di Egidio | C3 Approver, Safety Authority, Security Authority, Return-to-Service Approver | Requester and approver for the same action; approver of own access; independent Auditor for controls he operated |
| Independent observer | Witness and evidence sufficiency reviewer for conflicted checks | Requester, approver or executor in the witnessed scenario |

The independent observer remains pending. Scenarios requiring that observer may be prepared but not accepted as final evidence until the role is filled.

## 6. Evidence model

Every execution record shall contain:

- test ID and scenario version;
- date, start time and end time;
- environment identifier and software revision;
- requester identity and effective roles;
- approver identity and effective roles;
- command classification and simulated target;
- policy decision and policy revision;
- correlation ID, request ID and audit event IDs;
- expected result and actual result;
- screenshots or exported logs where useful;
- deviations, defects and remediation references;
- result: `Passed`, `Failed`, `Blocked` or `Not Executed`;
- executor and reviewer sign-off.

Failures must be preserved. Re-execution must create a new evidence record rather than overwrite the failed result.

## 7. Validation scenarios

### FE-01 — Independent C3 request and approval

| Attribute | Value |
|---|---|
| Requester | Massimo Mainini — Operator |
| Approver | Leonardo Di Egidio — C3 Approver |
| Target | Simulated non-operational device/action |
| Expected result | Request remains pending until Leonardo approves; execution occurs only after valid approval |
| Mandatory evidence | Request record, separate sessions, approval record, policy result, simulated execution event, audit chain |
| Current result | Not Executed |

Acceptance criteria:

- requester and approver are different natural persons and accounts;
- approval timestamp follows request timestamp;
- Massimo cannot alter the recorded approver identity;
- simulated execution references the approved request and policy revision.

### FE-02 — Self-approval rejection

| Attribute | Value |
|---|---|
| Actor | Massimo Mainini — requester |
| Action | Attempt to approve own C3 request |
| Expected result | Denied before execution; denial is audited |
| Mandatory evidence | Denial event, policy rule, unchanged request state, no execution event |
| Current result | Not Executed |

Acceptance criteria:

- denial is deterministic;
- no privilege escalation or alternate path succeeds;
- request remains pending or is cancelled according to policy.

### FE-03 — Approver conflict rejection

| Attribute | Value |
|---|---|
| Actor | Leonardo Di Egidio |
| Action | Attempt to request and approve the same classified action |
| Expected result | Approval or request path denied according to incompatible-role policy |
| Mandatory evidence | Conflict decision, denied transition, audit event |
| Current result | Not Executed |

### FE-04 — Approver revocation before execution

| Attribute | Value |
|---|---|
| Initial approver | Leonardo Di Egidio |
| Revocation authority | Massimo Mainini as Sponsor, witnessed by independent observer |
| Action | Suspend Leonardo's approval eligibility after approval but before simulated execution |
| Expected result | Approval becomes invalid; execution is denied |
| Mandatory evidence | Suspension record, invalidation event, denied execution, audit correlation |
| Current result | Not Executed |

This scenario cannot be accepted as final without an independent observer because the Sponsor participates in the revocation decision.

### FE-05 — Operator revocation before execution

| Attribute | Value |
|---|---|
| Operator | Massimo Mainini |
| Revocation authority | Leonardo Di Egidio — Security Authority |
| Action | Suspend requester eligibility before execution |
| Expected result | Pending request cannot execute and must be cancelled or revalidated |
| Mandatory evidence | Access decision, suspended role, denied execution, audit record |
| Current result | Not Executed |

### FE-06 — Maintainer and Return-to-Service separation

| Attribute | Value |
|---|---|
| Maintainer | Massimo Mainini |
| Return-to-Service Approver | Leonardo Di Egidio |
| Target | Simulated service or device adapter |
| Expected result | Massimo may complete test maintenance but cannot restore service; Leonardo independently verifies and approves or denies return to service |
| Mandatory evidence | Maintenance record, safe-state check, approval decision, service-state transition, audit trail |
| Current result | Not Executed |

Acceptance criteria:

- service remains unavailable after maintenance completion until Leonardo's decision;
- Massimo cannot approve his own return to service;
- denial leaves the simulated service in a safe state.

### FE-07 — Safety permit, deny and stop

| Attribute | Value |
|---|---|
| Operations actor | Massimo Mainini |
| Safety Authority | Leonardo Di Egidio |
| Target | Simulated command path only |
| Expected result | Safety decision can permit, deny or stop the simulated action; local physical interlocks remain outside the test and authoritative |
| Mandatory evidence | Safety input fixture, decision, resulting state, audit event |
| Current result | Not Executed |

A documentation decision by Leonardo does not authorize physical control.

### FE-08 — Security Authority cannot approve own access

| Attribute | Value |
|---|---|
| Actor | Leonardo Di Egidio — Security Authority |
| Action | Attempt to approve an access entitlement for himself |
| Expected result | Denied or held pending independent approval |
| Mandatory evidence | Access request, conflict detection, denial/hold decision, audit record |
| Current result | Not Executed |

### FE-09 — Audit-trail completeness

| Attribute | Value |
|---|---|
| Input | Evidence from FE-01 through FE-08 |
| Reviewer | Independent observer or ARB reviewer |
| Expected result | Every state transition is attributable, ordered and correlated |
| Mandatory evidence | Exported audit chain and completeness checklist |
| Current result | Not Executed |

Required fields:

- requester;
- approver;
- effective roles;
- request and decision timestamps;
- policy and software revisions;
- target and command classification;
- result and reason;
- correlation identifiers;
- revocation or conflict events where applicable.

### FE-10 — C4 positive path remains denied

| Attribute | Value |
|---|---|
| Participants | Massimo Mainini and Leonardo Di Egidio |
| Action | Attempt to initiate a positive C4 chain with only the current two-person allocation |
| Expected result | Denied because sufficient independent actors are unavailable |
| Mandatory evidence | Policy denial, role-conflict explanation, no execution event |
| Current result | Not Executed |

Passing this scenario means proving that C4 remains denied. It does not constitute positive C4 validation.

### FE-11 — Break-glass remains denied

| Attribute | Value |
|---|---|
| Participants | Both nominated identities |
| Action | Attempt to request or approve break-glass authority in the C04 environment |
| Expected result | Denied; no privilege or command path is enabled |
| Mandatory evidence | Denial event and unchanged entitlement state |
| Current result | Not Executed |

### FE-12 — Evidence tamper-resistance check

| Attribute | Value |
|---|---|
| Actor | Validation operator |
| Action | Attempt to modify or replace a completed evidence record without creating a revision |
| Expected result | Change is prevented or remains traceable through repository history and immutable audit references |
| Mandatory evidence | Commit history, audit reference and reviewer confirmation |
| Current result | Not Executed |

## 8. Execution order

The required execution order is:

1. validate environment isolation and record the baseline;
2. verify distinct identities and sessions;
3. execute FE-02 and FE-03 denial tests before any positive flow;
4. execute FE-01 limited positive C3 flow;
5. execute FE-04 and FE-05 revocation scenarios;
6. execute FE-06 return-to-service separation;
7. execute FE-07 and FE-08 authority-conflict scenarios;
8. execute FE-10 and FE-11 prohibited-path tests;
9. execute FE-12 evidence integrity check;
10. perform FE-09 independent audit-trail review.

A failed denial test blocks all later positive scenarios until corrected and re-reviewed.

## 9. Stop conditions

The campaign must stop immediately if:

- the test environment can reach a physical observatory device;
- a shared account or shared credential is detected;
- self-approval succeeds;
- a revoked approval remains executable;
- a command executes without a valid approval chain;
- logs omit requester, approver, policy or timestamps;
- a local physical interlock is bypassed or disabled;
- evidence is overwritten or altered without traceability;
- an undeclared conflict affects a validation decision.

A stop condition creates a `Failed` or `Blocked` evidence record and requires corrective action before resumption.

## 10. Result matrix

| Test ID | Scenario | Initial state | Required for limited C3 evidence | Required for C04 closure |
|---|---|---|---|---|
| FE-01 | Independent C3 approval | Not Executed | Yes | Yes |
| FE-02 | Self-approval rejection | Not Executed | Yes | Yes |
| FE-03 | Approver conflict rejection | Not Executed | Yes | Yes |
| FE-04 | Approver revocation | Not Executed | Yes | Yes |
| FE-05 | Operator revocation | Not Executed | Yes | Yes |
| FE-06 | Return-to-service separation | Not Executed | No | Yes |
| FE-07 | Safety authority decision | Not Executed | No | Yes |
| FE-08 | Security self-access rejection | Not Executed | No | Yes |
| FE-09 | Audit completeness | Not Executed | Yes | Yes |
| FE-10 | C4 remains denied | Not Executed | No | Yes |
| FE-11 | Break-glass remains denied | Not Executed | No | Yes |
| FE-12 | Evidence integrity | Not Executed | Yes | Yes |

## 11. Exit criteria

C04-W04 planning is complete when:

- this plan is approved and version controlled;
- scenario identifiers and evidence requirements are stable;
- dependencies on W03 and the independent observer are explicit;
- all initial results remain `Not Executed`;
- no runtime or physical-device authority is implied.

The validation campaign may be declared executed only when:

- all entry criteria are satisfied;
- every required scenario has an evidence record;
- failures and remediation are preserved;
- an independent reviewer accepts evidence sufficiency;
- results are incorporated into `ARB-012-C04-Execution-Evidence.md` and the validation campaign register.

## 12. Traceability

| Requirement | Source | Validation scenarios |
|---|---|---|
| Requester and approver separation | Role Assignment Register | FE-01, FE-02, FE-03 |
| Revocation effectiveness | Identity, Training and Access Review Register | FE-04, FE-05 |
| Maintainer / return-to-service separation | Role Assignment Register | FE-06 |
| Safety independence | Role Assignment Register | FE-07 |
| Security self-approval prohibition | Identity, Training and Access Review Register | FE-08 |
| Complete auditability | ARB-012 final re-review condition C04 | FE-09, FE-12 |
| Insufficient C4 actors remain denied | Current two-person allocation | FE-10 |
| Break-glass prohibition | Current ARB disposition | FE-11 |

## 13. Current disposition

**C04-W04: APPROVED PLAN — NOT EXECUTED.**

The validation design is ready for implementation after C04-W03 evidence and environment-isolation prerequisites are completed. ARB-012-C04 remains `Blocked`.

C3 may not be considered validated until the required scenarios are executed with accepted evidence. Positive C4, independent audit closure, runtime enablement, break-glass, physical-device control and local-interlock bypass remain prohibited.
