# ARB-012-C04 — Sponsor Nomination Decision

| Field | Value |
|---|---|
| Decision ID | ARB-012-C04-DEC-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Decision authority | Massimo Mainini — Project Owner / Architecture Sponsor |
| Status | Two-person segregation model recorded; closure prerequisites remain open |
| Effective date | 2026-07-31 |
| Review date | Required after substitute and audit-independence completion |
| Runtime effect | None |

## 1. Decision purpose

This record captures the nominative governance decision required to establish organizational segregation for ARB-012-C04. Completion of this record does not itself grant application, infrastructure, device or command privileges. Technical access remains subject to separate implementation, access review, validation and ARB approval.

## 2. Mandatory nomination principles

The Sponsor decision must satisfy all of the following:

- requester and approver are distinct for C3 and C4;
- C4 execution and second approval use distinct identities;
- Maintainer is distinct from the safety-relevant return-to-service approver;
- Safety Authority is independent from Operations and the DSOC command path;
- Security Authority does not approve its own access or the access of an identity it directly represents;
- Auditor has read-only evidence access and no command execution;
- critical roles have approved substitutes;
- delegations are time-bound, scoped and revocable;
- the same natural person represented through multiple accounts does not satisfy four-eyes independence.

## 3. Nominative decision table

The Sponsor authorizes the following minimum two-person segregation model. Massimo Mainini holds operational, service and technical execution responsibilities. Leonardo Di Egidio holds independent approval, safety, security and control responsibilities. No person may act as substitute for an incompatible role held by the other person. Where an independent substitute is not available, the role remains without substitute and the affected action remains prohibited.

| Role | Primary identity | Substitute | Valid from | Valid until | Scope | Sponsor decision |
|---|---|---|---|---|---|---|
| Operations Lead | Massimo Mainini | Not appointed | 2026-07-31 | Until revoked | Operations governance | Approved for non-operational governance |
| Service Owner | Massimo Mainini | Not appointed | 2026-07-31 | Until revoked | Service accountability | Approved for non-operational governance |
| Technical Owner | Massimo Mainini | Not appointed | 2026-07-31 | Until revoked | Technical ownership | Approved for non-operational governance |
| Operator | Massimo Mainini | Not appointed | 2026-07-31 | Until revoked | C0–C2 request/execution as separately authorized | Approved for non-operational validation only |
| Senior Operator / C3 Approver | Leonardo Di Egidio | Not appointed | 2026-07-31 | Until revoked | Independent C3 approval | Approved for non-operational validation only |
| C4 Second Approver | Leonardo Di Egidio | Not appointed | 2026-07-31 | Until revoked | Independent C4 second approval | Recorded; C4 execution remains prohibited because a further independent approval/execution chain is not established |
| Incident Coordinator | Massimo Mainini | Not appointed | 2026-07-31 | Until revoked | Incident coordination | Approved for non-operational governance |
| Maintainer | Massimo Mainini | Not appointed | 2026-07-31 | Until revoked | Controlled maintenance | Approved for non-operational validation only |
| Return-to-Service Approver | Leonardo Di Egidio | Not appointed | 2026-07-31 | Until revoked | Independent recovery approval | Approved for non-operational validation only |
| Safety Authority | Leonardo Di Egidio | Not appointed | 2026-07-31 | Until revoked | Independent permit/deny/stop and safety verification | Approved for non-operational validation only |
| Security Authority | Leonardo Di Egidio | Not appointed | 2026-07-31 | Until revoked | Access and privileged-access governance | Approved subject to prohibition on self-approval |
| Documentation Governor | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Documentation governance | Approved |
| Auditor | Leonardo Di Egidio | Not appointed | 2026-07-31 | Until revoked | Read-only audit of evidence not authored or approved by the Auditor | Provisional; independent final audit remains required |

## 4. Conflict declarations

| Conflict ID | Identity | Roles or relationship | Risk | Mitigation | Sponsor disposition |
|---|---|---|---|---|---|
| C04-CONFLICT-001 | Massimo Mainini | Operations Lead, Service Owner, Technical Owner, Operator, Incident Coordinator, Maintainer and Documentation Governor | Concentration of operational and technical responsibilities | Massimo cannot approve his own C3/C4 requests, privileged access, safety decisions or return-to-service actions | Accepted for non-operational bootstrap scope |
| C04-CONFLICT-002 | Leonardo Di Egidio | C3/C4 approver, Return-to-Service Approver, Safety Authority, Security Authority and provisional Auditor | Concentration of approval and assurance responsibilities; risk of reviewing decisions in which he participated | Auditor scope excludes evidence authored or approved by Leonardo; such evidence requires a future independent Auditor. Security self-approval and audit self-review are prohibited | Open Major conflict; additional independent Auditor required |
| C04-CONFLICT-003 | Massimo Mainini / Leonardo Di Egidio | Two-person pool has no independent substitutes | Loss of availability and inability to preserve segregation during absence or delegation | No cross-substitution for incompatible roles; affected action remains denied until a compatible substitute is appointed | Open blocker for resilient operational closure |
| C04-CONFLICT-004 | Leonardo Di Egidio | Sole C3 approver and C4 second approver | Two-person model cannot establish a broader C4 approval chain beyond requester/executor and one independent approver | C4 runtime and break-glass remain prohibited; additional independent approver required before C4 validation or enablement | Open blocker for C4 |

## 5. Training and access-review prerequisites

Before an appointment becomes operationally effective, repository evidence must confirm:

- role-specific training completed;
- least-privilege scope reviewed;
- authentication identity verified;
- privileged access approved by an independent authority;
- revocation path tested or documented;
- substitute activation procedure documented;
- audit access established for an independent Auditor.

No training, identity verification, access review, privileged-access approval, revocation test or substitute activation evidence has yet been recorded for these appointments.

## 6. Sponsor attestation

```text
Decision: Approved as a minimum two-person segregation model for governance and non-operational validation
Decision date: 2026-07-31
Approved by: Massimo Mainini — Project Owner / Architecture Sponsor
Scope: Organizational appointments only; no runtime authorization
Rationale: Operational and technical roles are assigned to Massimo Mainini, while approval, safety, security and control roles are assigned to Leonardo Di Egidio. This removes direct self-approval for C3 requests and separates maintenance from return-to-service approval. The model does not yet provide independent substitutes, a fully independent Auditor or the additional approval capacity required for C4. Those actions remain blocked until further identities and validation evidence are available.
```

## 7. Current decision

**TWO-PERSON SEGREGATION RECORDED — ARB-012-C04 REMAINS BLOCKED PENDING COMPLETION AND INDEPENDENT VALIDATION.**

The allocation now supports preparation of non-operational C3 four-eyes and Maintainer/return-to-service validation scenarios using distinct natural persons. It does not support operational authorization or C4 runtime.

Remaining blockers:

- independent substitutes for critical roles are not appointed;
- a fully independent Auditor is not appointed;
- training, identity verification and access reviews are not recorded;
- four-eyes scenarios have not been executed;
- C4 requires additional independent approval capacity;
- no independent ARB `Passed` decision exists.

Until these conditions are closed:

- ARB-012-C04 remains `Blocked`;
- issue #11 remains open;
- C3/C4 runtime remains prohibited;
- C4 validation requiring an additional independent actor remains prohibited;
- break-glass runtime remains prohibited;
- self-approval remains prohibited;
- operational return-to-service remains prohibited;
- local physical interlocks remain independent and authoritative.
