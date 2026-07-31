# ARB-012-C04 — Sponsor Nomination Decision

| Field | Value |
|---|---|
| Decision ID | ARB-012-C04-DEC-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Decision authority | Massimo Mainini — Project Owner / Architecture Sponsor |
| Status | Bootstrap nominations recorded; C04 closure not achieved |
| Effective date | 2026-07-31 |
| Review date | Required after independent-role redesign |
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

The Sponsor has recorded Massimo Mainini as primary identity and Leonardo Di Egidio as substitute for every listed role. These appointments are accepted only as a bootstrap governance baseline. They do not satisfy the independence requirements for C04 because incompatible primary roles remain concentrated in one person and all substitutes remain concentrated in one second person.

| Role | Primary identity | Substitute | Valid from | Valid until | Scope | Sponsor decision |
|---|---|---|---|---|---|---|
| Operations Lead | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Operations governance | Approved for bootstrap only |
| Service Owner | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Service accountability | Approved for bootstrap only |
| Technical Owner | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Technical ownership | Approved for bootstrap only |
| Operator | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | C0–C2 request/execution as separately authorized | Approved for bootstrap only |
| Senior Operator / C3 Approver | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Independent C3 approval | Recorded; independence not satisfied |
| C4 Second Approver | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Independent C4 second approval | Recorded; independence not satisfied |
| Incident Coordinator | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Incident coordination | Approved for bootstrap only |
| Maintainer | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Controlled maintenance | Approved for bootstrap only |
| Return-to-Service Approver | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Independent recovery approval | Recorded; independence not satisfied |
| Safety Authority | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Independent permit/deny/stop and safety verification | Recorded; independence not satisfied |
| Security Authority | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Access and privileged-access governance | Recorded; independence not satisfied |
| Documentation Governor | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Documentation governance | Approved for bootstrap only |
| Auditor | Massimo Mainini | Leonardo Di Egidio | 2026-07-31 | Until revoked | Read-only independent audit | Recorded; independence not satisfied |

## 4. Conflict declarations

For every proposed identity, the Sponsor must declare:

- other Digital StarGate roles held;
- administrative or privileged accounts controlled;
- family, employment, contractual or supervisory relationships that may impair independence;
- ability to act as substitute without inheriting incompatible privileges;
- mitigation or rejection decision.

| Conflict ID | Identity | Roles or relationship | Risk | Mitigation | Sponsor disposition |
|---|---|---|---|---|---|
| C04-CONFLICT-001 | Massimo Mainini | Primary holder of all operational, approval, safety, security, maintenance and audit roles | Critical concentration of duties; self-approval and self-audit risk | Runtime disabled; C3/C4, break-glass, privileged self-approval and return-to-service approval remain prohibited; redesign role allocation before closure | Accepted for bootstrap only; open blocker |
| C04-CONFLICT-002 | Leonardo Di Egidio | Substitute for all operational, approval, safety, security, maintenance and audit roles | Critical concentration when acting as substitute; incompatible authorities may transfer together | Substitute activation must be scoped per role; incompatible roles must not be activated concurrently; additional independent identities required before closure | Accepted for bootstrap only; open blocker |
| C04-CONFLICT-003 | Massimo Mainini / Leonardo Di Egidio | Two-person pool covers all requester, approver, safety, security and audit functions | Insufficient independence for resilient four-eyes, substitute coverage and independent audit | Nominate additional distinct identities and define mutually exclusive role combinations | Returned for organizational redesign |

## 5. Training and access-review prerequisites

Before an appointment becomes operationally effective, repository evidence must confirm:

- role-specific training completed;
- least-privilege scope reviewed;
- authentication identity verified;
- privileged access approved by an independent authority;
- revocation path tested or documented;
- substitute activation procedure documented;
- audit access established for the independent Auditor.

No training, identity verification, access review, privileged-access approval, revocation test or substitute activation evidence has yet been recorded for these appointments.

## 6. Sponsor attestation

```text
Decision: Approved as bootstrap organizational appointments only
Decision date: 2026-07-31
Approved by: Massimo Mainini — Project Owner / Architecture Sponsor
Scope: Organizational appointments only; no runtime authorization
Rationale: Massimo Mainini is recorded as primary identity and Leonardo Di Egidio as substitute for all listed roles to establish a documented bootstrap baseline. The Sponsor acknowledges that this allocation does not satisfy C04 segregation, four-eyes, independent Safety Authority, independent Security Authority or independent audit requirements. Additional distinct identities and access-review evidence are required before C04 closure.
```

## 7. Current decision

**BOOTSTRAP NOMINATIONS RECORDED — ARB-012-C04 REMAINS BLOCKED.**

The current two-person allocation does not provide sufficient separation between requester, approver, executor, Maintainer, return-to-service approver, Safety Authority, Security Authority and Auditor. It therefore cannot support positive four-eyes validation or operational authorization.

Until the role allocation is redesigned and independently validated:

- ARB-012-C04 remains `Blocked`;
- issue #11 remains open;
- C3/C4 runtime remains prohibited;
- break-glass runtime remains prohibited;
- self-approval remains prohibited;
- operational return-to-service approval remains prohibited;
- independent audit is not established;
- local physical interlocks remain independent and authoritative.
