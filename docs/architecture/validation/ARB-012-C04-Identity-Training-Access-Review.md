# ARB-012-C04 — Identity, Training and Access Review Register

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-02 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Updated | 2026-08-23 |
| Target model | Two-Person Limited Operations Model |
| Status | **In Progress — IDV partial PASS; TRN-001..007 PASS; TRN-008 partial PASS; access/revocation reconciliation pending** |
| Runtime effect | None |

## 1. Purpose

This register governs identity assurance, role-specific training, least-privilege review and revocation evidence for the approved two-person model. It does not grant runtime privileges.

## 2. Current nominated identities

| Project identity | Natural person | Role group | Current evidence status |
|---|---|---|---|
| DSG-PERSON-001 | Massimo Mainini | Sponsor, architecture, operations, service, technical ownership, Operator, Incident Coordinator, Maintainer, Documentation Governor | Governance mapping + VM-R03 technical account evidence; Leonardo human attestation pending |
| DSG-PERSON-002 | Leonardo Di Egidio | C3 Approver, Return-to-Service Approver, Safety Authority, Security Authority | Governance mapping + VM-R04 technical account evidence + Massimo reciprocal human attestation PASS |

## 3. Identity assurance register

Execution artifact: `ARB-012-C04-IDV-Execution-Record.md`.

| Check ID | Identity | Verification requirement | Evidence reference | Verified by | Result |
|---|---|---|---|---|---|
| IDV-001 | Massimo / DSG-PERSON-001 | Natural-person identity mapped to unique project identity | E-ARB012-C04-IDV-001 / IDV-001 | Leonardo | **Pending Leonardo attestation** |
| IDV-002 | Leonardo / DSG-PERSON-002 | Natural-person identity mapped to unique project identity | E-ARB012-C04-IDV-001 / IDV-002 | Massimo | **PASS — 2026-08-22** |
| IDV-003 | Massimo | Non-production authentication account ownership; non-shared | VM-R03 / ACC-001 + IDV record | Leonardo | **Technical PASS / Leonardo ownership attestation pending** |
| IDV-004 | Leonardo | Non-production authentication account ownership; non-shared | VM-R04 / ACC-002 + IDV record | Massimo | **PASS — 2026-08-22** |
| IDV-005 | Both | Distinct usernames, credentials, factors and sessions | VM-R03 + VM-R04 + reciprocal IDV record | Reciprocal | **Partial PASS — Massimo half complete; Leonardo half pending** |

No third-party observer is required for IDV under the approved target. Technical account/session evidence is not treated as a substitute for the remaining human attestation.

## 4. Role-specific training matrix

Execution artifact: `ARB-012-C04-Training-Execution-Record.md`.

| Training ID | Identity | Required subject | Result |
|---|---|---|---|
| TRN-001 | Massimo | C0–C4 classification, request boundaries and self-approval prohibition | **PASS — Leonardo assessment, 2026-08-23** |
| TRN-002 | Massimo | Maintenance safety, rollback, safe-state preservation and return-to-service handoff | **PASS — Leonardo assessment, 2026-08-23** |
| TRN-003 | Massimo | Incident recording, audit trail and evidence preservation | **PASS — Leonardo assessment, 2026-08-23** |
| TRN-004 | Leonardo | Independent C3 approval criteria and conflict rejection | **PASS — Massimo assessment, 2026-08-23** |
| TRN-005 | Leonardo | Safety permit, deny, stop and safe-state verification | **PASS — Massimo assessment, 2026-08-23** |
| TRN-006 | Leonardo | Privileged-access approval, least privilege and revocation | **PASS — Massimo assessment, 2026-08-23** |
| TRN-007 | Leonardo | Return-to-service approval independent from Maintainer | **PASS — Massimo assessment, 2026-08-23** |
| TRN-008 | Both | Four-eyes workflow, approver revocation and audit completeness | **Partial PASS — Massimo assessment of Leonardo PASS; Leonardo assessment of Massimo pending** |

## 5. Least-privilege access review

| Review ID | Subject | Maximum target scope | Reviewer | Decision |
|---|---|---|---|---|
| AR-001 | Massimo C0–C2 validation | isolated simulator context only | Leonardo | Pending |
| AR-002 | Massimo C3 request | submit/request only under validated workflow | Leonardo | Pending |
| AR-003 | Massimo maintenance | isolated maintenance; no own return-to-service | Leonardo | Pending |
| AR-004 | Leonardo C3 approval | approve Massimo request; cannot request same action | Massimo as Sponsor/governance reviewer | Pending |
| AR-005 | Leonardo Safety Authority | bounded validation decisions; no local-interlock bypass | Massimo as Sponsor/governance reviewer | Pending |
| AR-006 | Leonardo Security Authority | approve Massimo scope; own-access approval prohibited | Massimo as Sponsor/governance reviewer | Pending |
| AR-007 | Independent internal audit access | Not part of target model | N/A | **N/A by governance design** |
| AR-008 | Positive C4 | Unsupported | Policy enforcement | **DENIED by governance design; VM-R11 PASS** |
| AR-009 | Break-glass | Unsupported | Policy enforcement | **DENIED by governance design; VM-R11 PASS** |

## 6. Required separation checks

| Separation ID | Requirement | Target allocation | Status |
|---|---|---|---|
| SEP-001 | C3 requester distinct from approver | Massimo / Leonardo | Structurally satisfied; VM-R09 proves self-approval denial; positive two-person C3 scenario still governed separately |
| SEP-002 | Maintainer distinct from Return-to-Service Approver | Massimo / Leonardo | Structurally satisfied; attributable scenario evidence still pending |
| SEP-003 | Safety Authority distinct from Operations | Leonardo / Massimo | Structurally satisfied; attributable scenario evidence still pending |
| SEP-004 | Security Authority distinct from operational beneficiary | Leonardo / Massimo | Structurally satisfied; attributable access-review decision still pending |
| SEP-005 | Independent internal Auditor | Outside target | N/A by governance design |
| SEP-006 | Positive C4 chain | Outside target | **DENIED by governance design; VM-R11 PASS** |
| SEP-007 | Independent substitutes | Outside target | N/A; absence suspends two-person-dependent capability |

## 7. Revocation and suspension

VM-R10 / ENV-007 proves the technical policy behavior `ALLOW -> suspended -> DENY`, reason `principal-suspended`, with `execution_attempted=false` and correlated audit/evidence. This establishes the suspension enforcement substrate but does not automatically satisfy all actor-specific governance scenarios below.

| Test | Actors | Result |
|---|---|---|
| REV-001 — revoke Massimo Operator eligibility | Leonardo revokes Massimo eligibility | Pending attributable actor-specific execution/reconciliation |
| REV-002 — suspend Leonardo approval eligibility | Massimo Sponsor action against Leonardo validation eligibility | Pending attributable actor-specific execution/reconciliation |
| REV-003 — invalidate pending approval after suspension | Validation workflow | Pending explicit stale/pending-approval invalidation evidence |
| REV-004 — verify deterministic denied access after revocation | Validation workflow | **Technical behavior demonstrated by VM-R10; governance mapping pending final reconciliation** |

No third observer is a target prerequisite. Technical audit evidence must demonstrate the state transition and denial.

## 8. Availability model

There are no incompatible-role substitutes in the target model. This is an accepted degraded-availability characteristic, not a closure blocker:

- absence of Massimo suspends requester/operator/maintenance-side capabilities;
- absence of Leonardo suspends C3 approval, safety, security and return-to-service capabilities;
- cross-substitution remains prohibited;
- positive C4 remains denied regardless of availability.

## 9. Evidence acceptance rules

Evidence must contain a stable ID, date, subject, verifier/actor, explicit result and repository reference. Secrets, passwords, private keys, MFA seeds, recovery codes and identity-document images/numbers must not be stored.

Reciprocal verification is valid only across distinct subjects: Massimo does not verify IDV-001/003 for himself; Leonardo does not verify IDV-002/004 for himself. IDV-005 and TRN-008 require reciprocal confirmation.

## 10. Work-item exit criteria

C04-W03 may complete when:

- IDV-001–IDV-005 are Passed;
- TRN-001–TRN-008 are Passed or have bounded approved exceptions;
- AR-001–AR-006 have attributable decisions;
- AR-007 is recorded N/A by governance design;
- AR-008 and AR-009 remain denied;
- ACC-001/ACC-002 prove distinct non-production sessions;
- REV-001–REV-004 pass or are explicitly reconciled to accepted evidence;
- conflicts and limitations remain explicit.

## 11. Current disposition

**C04-W03: IN PROGRESS.**

Completed: TRN-001 through TRN-007, Massimo half of TRN-008, IDV-002, IDV-004, Massimo half of IDV-005, distinct technical accounts/sessions, AR-008/AR-009 denial evidence and technical suspension enforcement substrate.

Remaining: Leonardo attestation for IDV-001/IDV-003/IDV-005, Leonardo half of reciprocal TRN-008, AR-001 through AR-006 decisions, and REV-001 through REV-004 reconciliation/execution as applicable.

Runtime, physical-device control, self-approval, positive C4, break-glass and local-interlock bypass remain prohibited.