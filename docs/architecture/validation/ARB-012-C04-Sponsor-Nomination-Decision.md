# ARB-012-C04 — Sponsor Nomination Decision

| Field | Value |
|---|---|
| Decision ID | ARB-012-C04-DEC-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Decision authority | Massimo Mainini — Project Owner / Architecture Sponsor |
| Status | Decision required |
| Effective date | TBD by Sponsor |
| Review date | TBD by Sponsor |
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

The Sponsor must replace every mandatory `TBD` with a verified identity before this decision can become `Approved`.

| Role | Primary identity | Substitute | Valid from | Valid until | Scope | Sponsor decision |
|---|---|---|---|---|---|---|
| Operations Lead | TBD | TBD | TBD | TBD | Operations governance | Pending |
| Service Owner | TBD | TBD | TBD | TBD | Service accountability | Pending |
| Technical Owner | TBD | TBD | TBD | TBD | Technical ownership | Pending |
| Operator | TBD | TBD | TBD | TBD | C0–C2 request/execution as separately authorized | Pending |
| Senior Operator / C3 Approver | TBD | TBD | TBD | TBD | Independent C3 approval | Pending |
| C4 Second Approver | TBD | TBD | TBD | TBD | Independent C4 second approval | Pending |
| Incident Coordinator | TBD | TBD | TBD | TBD | Incident coordination | Pending |
| Maintainer | TBD | TBD | TBD | TBD | Controlled maintenance | Pending |
| Return-to-Service Approver | TBD | TBD | TBD | TBD | Independent recovery approval | Pending |
| Safety Authority | TBD | TBD | TBD | TBD | Independent permit/deny/stop and safety verification | Pending |
| Security Authority | TBD | TBD | TBD | TBD | Access and privileged-access governance | Pending |
| Documentation Governor | TBD | TBD | TBD | TBD | Documentation governance | Pending |
| Auditor | TBD | TBD | TBD | TBD | Read-only independent audit | Pending |

## 4. Conflict declarations

For every proposed identity, the Sponsor must declare:

- other Digital StarGate roles held;
- administrative or privileged accounts controlled;
- family, employment, contractual or supervisory relationships that may impair independence;
- ability to act as substitute without inheriting incompatible privileges;
- mitigation or rejection decision.

| Conflict ID | Identity | Roles or relationship | Risk | Mitigation | Sponsor disposition |
|---|---|---|---|---|---|
| C04-CONFLICT-TBD-01 | TBD | TBD | TBD | TBD | Pending |

## 5. Training and access-review prerequisites

Before an appointment becomes operationally effective, repository evidence must confirm:

- role-specific training completed;
- least-privilege scope reviewed;
- authentication identity verified;
- privileged access approved by an independent authority;
- revocation path tested or documented;
- substitute activation procedure documented;
- audit access established for the independent Auditor.

## 6. Sponsor attestation

The Sponsor must record an explicit decision using the following disposition:

```text
Decision: Approved / Rejected / Returned for revision
Decision date: YYYY-MM-DD
Approved by: Massimo Mainini — Project Owner / Architecture Sponsor
Scope: Organizational appointments only; no runtime authorization
Rationale: <repository-recorded rationale>
```

## 7. Current decision

**PENDING — mandatory identities and substitutes have not been supplied.**

Until this record is completed and independently validated:

- ARB-012-C04 remains `Blocked`;
- issue #11 remains open;
- C3/C4 runtime remains prohibited;
- break-glass runtime remains prohibited;
- self-approval remains prohibited;
- local physical interlocks remain independent and authoritative.
