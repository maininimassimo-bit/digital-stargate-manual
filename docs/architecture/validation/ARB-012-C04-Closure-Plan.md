# ARB-012-C04 — Closure Plan

| Field | Value |
|---|---|
| Plan ID | ARB-012-C04-PLAN-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Date | 30/07/2026 |
| Authority | Digital StarGate Chief Architect |
| Current status | Blocked |
| Runtime impact | No runtime enablement authorized |

## 1. Purpose

This plan defines the controlled sequence required to close ARB-012-C04. It does not nominate people, grant privileges, enable command paths or reclassify the condition. Only the Project Owner / Architecture Sponsor may approve nominative assignments, and only independently verified evidence may change C04 from `Blocked` to `Passed`.

## 2. Verified current state

The current bootstrap organization assigns incompatible responsibilities to one identity. The repository therefore records:

- no independent requester and approver for C3/C4;
- no independent return-to-service approver;
- no independent Safety Authority;
- no independent Security Authority;
- no independent Auditor;
- no approved substitutes for critical roles;
- no operational privileged access or break-glass authority;
- no runtime command authorization.

The mitigating controls remain prohibition and runtime disablement. Local physical interlocks remain independent and authoritative.

## 3. Required target state

C04 may close only when the repository contains approved evidence for all of the following:

1. distinct identities for incompatible roles;
2. approved substitutes for critical roles;
3. explicit validity periods and revocation authority;
4. completed training records where required;
5. completed access reviews;
6. approved conflict mitigations;
7. requester/approver separation for C3 and C4;
8. Maintainer/return-to-service approver separation;
9. independent Safety Authority and Security Authority;
10. Auditor with read-only evidence access and no command execution;
11. successful four-eyes validation scenarios;
12. complete audit evidence for every validation decision.

## 4. Dependency-ordered work items

### C04-W01 — Sponsor nomination decision

Owner: Project Owner / Architecture Sponsor.

Output: `ARB-012-C04-Sponsor-Nomination-Decision.md` completed with actual identities, substitutes, validity, scope and approval.

Exit criteria:

- no `TBD` remains for mandatory critical roles;
- incompatible roles are assigned to distinct identities;
- the Sponsor signs or otherwise records an explicit repository decision;
- no assignment grants runtime privileges by itself.

### C04-W02 — Role register and conflict update

Owner: Chief Architect with Sponsor-approved input.

Affected artifact:

- `ARB-012-C04-Role-Assignment-Register.md`.

Exit criteria:

- nominative register matches the Sponsor decision;
- delegation records are time-bound and revocable;
- conflict register is updated;
- access matrix C1–C4 is explicit;
- prohibited combinations remain technically and procedurally denied.

### C04-W03 — Access review and training evidence

Owner: Security Authority and Operations governance after valid independent appointment.

Required evidence:

- identity and role mapping;
- least-privilege review;
- privileged-access approval separation;
- training completion or approved exception;
- revocation and substitute activation procedure.

Exit criteria: all required reviews are approved by actors independent from the beneficiary.

### C04-W04 — Four-eyes validation plan

Owner: Release and Quality Governor.

Mandatory scenarios:

1. C3 request and approval by distinct identities;
2. self-approval rejection;
3. C4 request with required independent approvals;
4. approver revocation before execution;
5. return-to-service approval by an actor distinct from the Maintainer;
6. SEV-1 closure with independent safety verification;
7. safety-relevant suppression rule with distinct author and approver;
8. complete requester, approver, policy, timestamp and decision audit trail.

All scenarios must remain non-operational unless a separate ARB authorization explicitly permits a broader scope.

### C04-W05 — Execution evidence and quality gate

Owner: Release and Quality Governor.

Outputs:

- `ARB-012-C04-Execution-Evidence.md`;
- updated `ARB-012-Validation-Campaign.md`;
- successful repository quality gate.

Exit criteria:

- every scenario has an explicit result;
- failed attempts and corrections are preserved;
- CI restore, build, test, formatting and MkDocs checks pass;
- scope limitations are explicit.

### C04-W06 — Independent ARB re-review

Owner: Architecture Review Board.

Decision options:

- `Passed`;
- `Blocked`;
- `Rework Required`.

The Board must not infer organizational independence from simulated identities or documentation alone.

### C04-W07 — Issue closure and campaign disposition

Owner: Program governance.

Issue #11 may close only after an ARB decision of `Passed` is merged. Runtime readiness remains a separate decision and is not implied by C04 closure.

## 5. RACI for closure work

| Activity | Sponsor | Chief Architect | Operations | Security Authority | Safety Authority | Release Governor | ARB |
|---|---|---|---|---|---|---|---|
| Approve nominations | A/R | C | C | C | C | I | I |
| Update role register | A | R | C | C | C | I | I |
| Access review | I | C | C | A/R | I | I | I |
| Safety independence verification | I | C | C | I | A/R | I | I |
| Design validation campaign | I | C | C | C | C | A/R | I |
| Execute and record tests | I | C | R | C | C | A/R | I |
| Final C04 decision | I | I | I | I | I | C | A/R |

## 6. Quality gates

| Gate | Required status |
|---|---|
| Sponsor nomination decision | Passed |
| Distinct critical identities | Passed |
| Substitute coverage | Passed |
| Access review | Passed |
| Conflict mitigation | Passed |
| Four-eyes scenarios | Passed |
| Audit evidence | Passed |
| Repository CI | Passed |
| Independent ARB review | Passed |
| Runtime enablement | Not Applicable to C04 closure |

## 7. Risks and controls

| Risk | Severity | Control |
|---|---|---|
| Same person represented by multiple logical identities | Critical | Reject as organizational evidence |
| Self-approval or privilege self-grant | Critical | Deny and preserve C04 as Blocked |
| Safety Authority dependent on Operations | Critical | Independent appointment required |
| Premature issue closure | High | Require merged ARB `Passed` decision |
| C04 closure interpreted as runtime approval | Critical | Separate runtime proposal and ARB decision required |
| Physical interlock bypass | Critical | Prohibited; local interlocks remain independent |

## 8. Current disposition

**ARB-012-C04 remains BLOCKED.**

The closure process is prepared, but nominative Sponsor decisions and independent identities are not yet present in repository evidence. C3/C4 runtime, break-glass runtime, self-approval and local-interlock bypass remain prohibited.
