# ARB-012-C04 — Identity, Training and Access Review Register

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-02 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Date | 2026-07-31 |
| Scope | Organizational and non-operational preparation only |
| Status | Evidence framework established; verification pending |
| Runtime effect | None |

## 1. Purpose

This register defines the evidence required before the current two-person role allocation can be used for any positive non-operational four-eyes validation. It records identity assurance, role-specific training, least-privilege review, approval separation, revocation and substitute activation.

This document does not assert that any identity, training course, account, privilege or control has already been verified. Every item remains `Pending` until supported by repository evidence and an identifiable reviewer.

## 2. Current nominated identities

| Identity | Current role group | Operational authority | Current evidence status |
|---|---|---|---|
| Massimo Mainini | Sponsor, architecture, operations, service, technical ownership, Operator, Incident Coordinator, Maintainer, Documentation Governor | None granted by this register | Pending verification |
| Leonardo Di Egidio | C3 Approver, C4 Second Approver, Return-to-Service Approver, Safety Authority, Security Authority, provisional Auditor | None granted by this register | Pending verification |

## 3. Identity assurance register

Identity verification must use an authoritative source suitable for the project context. Sensitive identity-document data must not be committed to the repository; the repository should retain only the verification result, reviewer, date and evidence reference.

| Check ID | Identity | Verification requirement | Evidence reference | Verified by | Date | Result |
|---|---|---|---|---|---|---|
| IDV-001 | Massimo Mainini | Natural-person identity confirmed and mapped to a unique project identity | Pending | Pending | Pending | Pending |
| IDV-002 | Leonardo Di Egidio | Natural-person identity confirmed and mapped to a unique project identity | Pending | Pending | Pending | Pending |
| IDV-003 | Massimo Mainini | Authentication account ownership verified; shared accounts prohibited | Pending | Pending | Pending | Pending |
| IDV-004 | Leonardo Di Egidio | Authentication account ownership verified; shared accounts prohibited | Pending | Pending | Pending | Pending |
| IDV-005 | Both | Distinct credentials and distinct authentication factors confirmed | Pending | Pending | Pending | Pending |

## 4. Role-specific training matrix

Training may be completed through a documented briefing, walkthrough, tabletop exercise or formal course, provided the subject, trainer, date and outcome are recorded.

| Training ID | Identity | Required subject | Completion evidence | Assessed by | Date | Result |
|---|---|---|---|---|---|---|
| TRN-001 | Massimo Mainini | C0–C4 classification, request boundaries and self-approval prohibition | Pending | Pending | Pending | Pending |
| TRN-002 | Massimo Mainini | Maintenance safety, rollback, safe-state preservation and return-to-service handoff | Pending | Pending | Pending | Pending |
| TRN-003 | Massimo Mainini | Incident recording, audit trail and evidence preservation | Pending | Pending | Pending | Pending |
| TRN-004 | Leonardo Di Egidio | Independent C3 approval criteria and conflict rejection | Pending | Pending | Pending | Pending |
| TRN-005 | Leonardo Di Egidio | Safety permit, deny, stop and safe-state verification | Pending | Pending | Pending | Pending |
| TRN-006 | Leonardo Di Egidio | Privileged-access approval, least privilege and revocation | Pending | Pending | Pending | Pending |
| TRN-007 | Leonardo Di Egidio | Return-to-service approval independent from Maintainer | Pending | Pending | Pending | Pending |
| TRN-008 | Both | Four-eyes workflow, approver revocation and audit completeness | Pending | Pending | Pending | Pending |

## 5. Least-privilege access review

The baseline is deny-by-default. Role nomination does not imply account creation or privilege assignment.

| Review ID | Identity | Requested capability | Maximum permitted scope before C04 closure | Independent reviewer | Evidence | Decision |
|---|---|---|---|---|---|---|
| AR-001 | Massimo Mainini | C0–C2 request/execution in test context | Simulated or isolated non-operational environment only | Leonardo Di Egidio as Security Authority, subject to conflict check | Pending | Pending |
| AR-002 | Massimo Mainini | Submit C3 request | Request creation only; no approval; no runtime execution | Leonardo Di Egidio | Pending | Pending |
| AR-003 | Massimo Mainini | Maintenance activity | Documentation and isolated test activity only; no operational return-to-service | Leonardo Di Egidio | Pending | Pending |
| AR-004 | Leonardo Di Egidio | C3 approval | Approval in non-operational validation only; no execution as requester | Massimo Mainini as Sponsor, with self-benefit exclusion | Pending | Pending |
| AR-005 | Leonardo Di Egidio | Safety Authority decisions | Documented validation decisions only; no physical-device or runtime authority | Massimo Mainini as Sponsor; independent ARB verification required | Pending | Pending |
| AR-006 | Leonardo Di Egidio | Security approval | Approve access for Massimo only; may not approve own access | Massimo Mainini as Sponsor; independent ARB verification required | Pending | Pending |
| AR-007 | Leonardo Di Egidio | Audit evidence access | Read-only repository evidence; no command execution | Pending independent reviewer | Pending | Blocked pending independent reviewer |
| AR-008 | Both | C4 workflow | No positive C4 execution or validation chain | Not applicable | Current two-person limitation | Denied |
| AR-009 | Both | Break-glass | No authority | Not applicable | Governance prohibition | Denied |

## 6. Required separation checks

| Separation ID | Requirement | Current allocation | Status |
|---|---|---|---|
| SEP-001 | C3 requester distinct from approver | Massimo requests; Leonardo approves | Structurally satisfied; evidence pending |
| SEP-002 | Maintainer distinct from Return-to-Service Approver | Massimo maintains; Leonardo approves return to service | Structurally satisfied; evidence pending |
| SEP-003 | Safety Authority distinct from Operations | Leonardo / Massimo | Structurally satisfied; evidence pending |
| SEP-004 | Security Authority distinct from operational beneficiary | Leonardo / Massimo | Structurally satisfied; evidence pending |
| SEP-005 | Auditor independent from approval and control functions | Leonardo holds both control and provisional audit roles | Not satisfied |
| SEP-006 | Positive C4 chain has sufficient independent actors | Only two natural persons available | Not satisfied |
| SEP-007 | Critical roles have independent substitutes | No independent substitutes nominated | Not satisfied |

## 7. Revocation and suspension procedure

Any role or access may be suspended immediately when identity assurance, training, conflict status or control effectiveness is uncertain.

Minimum procedure:

1. record the identity, role, reason and timestamp;
2. suspend the affected logical access or mark it unavailable;
3. invalidate pending approvals from that identity;
4. prevent execution of any request relying on the revoked approval;
5. preserve audit evidence;
6. require a new independent review before reinstatement.

| Revocation test | Owner | Evidence | Result |
|---|---|---|---|
| Revoke Massimo's Operator eligibility before execution | Leonardo Di Egidio | Pending | Not executed |
| Revoke Leonardo's C3 approval eligibility before execution | Massimo Mainini / independent validation observer | Pending | Not executed |
| Invalidate a pending approval after role suspension | Validation campaign | Pending | Not executed |
| Confirm denied access after revocation | Validation campaign | Pending | Not executed |

## 8. Substitute activation

No independent substitutes are currently nominated. Therefore:

- absence of Massimo suspends operational and maintenance-side validation activities;
- absence of Leonardo suspends approval, safety, security and return-to-service validation activities;
- one person may not activate the other person's incompatible roles as a substitute;
- C3 validation requires both identities;
- C4 remains denied regardless of availability.

Substitute coverage status: **Blocked**.

## 9. Evidence acceptance rules

Evidence is acceptable only when it includes:

- stable evidence identifier;
- date and scope;
- identity or role assessed;
- assessor identity;
- explicit result: `Passed`, `Failed`, `Pending` or `Not Applicable`;
- links or references to supporting repository artifacts;
- preserved failure and remediation history;
- no secrets, passwords, private keys or identity-document images.

A person must not approve their own privileged access, training assessment or identity verification when that approval creates a material conflict.

## 10. Work-item exit criteria

C04-W03 may be marked complete only when:

- IDV-001 through IDV-005 are `Passed`;
- all role-relevant training items are `Passed` or have an approved, time-bound exception;
- AR-001 through AR-007 have explicit decisions and supporting evidence;
- revocation procedures have been exercised in the non-operational validation environment;
- prohibited capabilities remain denied;
- all conflicts are recorded;
- an independent reviewer confirms that the evidence is sufficient for C04-W04.

## 11. Current disposition

**C04-W03: IN PROGRESS — evidence framework created, verification not yet performed.**

The two-person allocation is structurally suitable for limited non-operational C3 and return-to-service validation after the listed identity, training and access reviews are completed. It is not sufficient for positive C4 validation, independent audit or substitute resilience.

ARB-012-C04 remains `Blocked`. Runtime, break-glass, physical-device control, self-approval and local-interlock bypass remain prohibited.
