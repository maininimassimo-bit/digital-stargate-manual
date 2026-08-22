# ARB-012-C04 — Identity, Training and Access Review Register

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-02 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Updated | 2026-08-22 |
| Target model | Two-Person Limited Operations Model |
| Status | In Progress — IDV reciprocal execution record prepared |
| Runtime effect | None |

## 1. Purpose

This register governs identity assurance, role-specific training, least-privilege review and revocation evidence for the approved two-person model. It does not grant runtime privileges.

## 2. Current nominated identities

| Project identity | Natural person | Role group | Current evidence status |
|---|---|---|---|
| DSG-PERSON-001 | Massimo Mainini | Sponsor, architecture, operations, service, technical ownership, Operator, Incident Coordinator, Maintainer, Documentation Governor | Governance mapping established; IDV attestation pending |
| DSG-PERSON-002 | Leonardo Di Egidio | C3 Approver, Return-to-Service Approver, Safety Authority, Security Authority | Governance mapping established; IDV attestation pending |

## 3. Identity assurance register

Execution artifact: `ARB-012-C04-IDV-Execution-Record.md`.

| Check ID | Identity | Verification requirement | Evidence reference | Verified by | Result |
|---|---|---|---|---|---|
| IDV-001 | Massimo / DSG-PERSON-001 | Natural-person identity mapped to unique project identity | E-ARB012-C04-IDV-001 / IDV-001 | Leonardo | Pending attestation |
| IDV-002 | Leonardo / DSG-PERSON-002 | Natural-person identity mapped to unique project identity | E-ARB012-C04-IDV-001 / IDV-002 | Massimo | Pending attestation |
| IDV-003 | Massimo | Non-production authentication account ownership; non-shared | E-ARB012-C04-IDV-001 / IDV-003 | Leonardo | Pending account evidence |
| IDV-004 | Leonardo | Non-production authentication account ownership; non-shared | E-ARB012-C04-IDV-001 / IDV-004 | Massimo | Pending account evidence |
| IDV-005 | Both | Distinct usernames, credentials, factors and sessions | E-ARB012-C04-IDV-001 / IDV-005 | Reciprocal | Pending account evidence |

No third-party observer is required for IDV under the approved target. No IDV item is marked Passed merely from role nomination.

## 4. Role-specific training matrix

| Training ID | Identity | Required subject | Result |
|---|---|---|---|
| TRN-001 | Massimo | C0–C4 classification, request boundaries and self-approval prohibition | Pending |
| TRN-002 | Massimo | Maintenance safety, rollback, safe-state preservation and return-to-service handoff | Pending |
| TRN-003 | Massimo | Incident recording, audit trail and evidence preservation | Pending |
| TRN-004 | Leonardo | Independent C3 approval criteria and conflict rejection | Pending |
| TRN-005 | Leonardo | Safety permit, deny, stop and safe-state verification | Pending |
| TRN-006 | Leonardo | Privileged-access approval, least privilege and revocation | Pending |
| TRN-007 | Leonardo | Return-to-service approval independent from Maintainer | Pending |
| TRN-008 | Both | Four-eyes workflow, approver revocation and audit completeness | Pending |

## 5. Least-privilege access review

| Review ID | Subject | Maximum target scope | Reviewer | Decision |
|---|---|---|---|---|
| AR-001 | Massimo C0–C2 validation | isolated simulator context only | Leonardo | Pending |
| AR-002 | Massimo C3 request | submit/request only under validated workflow | Leonardo | Pending |
| AR-003 | Massimo maintenance | isolated maintenance; no own return-to-service | Leonardo | Pending |
| AR-004 | Leonardo C3 approval | approve Massimo request; cannot request same action | Massimo as Sponsor/governance reviewer | Pending |
| AR-005 | Leonardo Safety Authority | bounded validation decisions; no local-interlock bypass | Massimo as Sponsor/governance reviewer | Pending |
| AR-006 | Leonardo Security Authority | approve Massimo scope; own-access approval prohibited | Massimo as Sponsor/governance reviewer | Pending |
| AR-007 | Independent internal audit access | Not part of target model | N/A | N/A by governance design |
| AR-008 | Positive C4 | Unsupported | Policy enforcement | DENIED by governance design |
| AR-009 | Break-glass | Unsupported | Policy enforcement | DENIED by governance design |

## 6. Required separation checks

| Separation ID | Requirement | Target allocation | Status |
|---|---|---|---|
| SEP-001 | C3 requester distinct from approver | Massimo / Leonardo | Structurally satisfied; execution evidence pending |
| SEP-002 | Maintainer distinct from Return-to-Service Approver | Massimo / Leonardo | Structurally satisfied; execution evidence pending |
| SEP-003 | Safety Authority distinct from Operations | Leonardo / Massimo | Structurally satisfied; execution evidence pending |
| SEP-004 | Security Authority distinct from operational beneficiary | Leonardo / Massimo | Structurally satisfied; execution evidence pending |
| SEP-005 | Independent internal Auditor | Outside target | N/A by governance design |
| SEP-006 | Positive C4 chain | Outside target | DENIED by governance design |
| SEP-007 | Independent substitutes | Outside target | N/A; absence suspends two-person-dependent capability |

## 7. Revocation and suspension

Required non-operational tests remain:

| Test | Actors | Result |
|---|---|---|
| REV-001 — revoke Massimo Operator eligibility | Leonardo revokes Massimo eligibility | Not executed |
| REV-002 — suspend Leonardo approval eligibility | Massimo Sponsor action against Leonardo validation eligibility | Not executed |
| REV-003 — invalidate pending approval after suspension | Validation workflow | Not executed |
| REV-004 — verify deterministic denied access after revocation | Validation workflow | Not executed |

No third observer is a target prerequisite. Technical audit evidence must demonstrate the state transition and denial.

## 8. Availability model

There are no incompatible-role substitutes in the target model. This is an accepted degraded-availability characteristic, not a closure blocker:

- absence of Massimo suspends requester/operator/maintenance-side capabilities;
- absence of Leonardo suspends C3 approval, safety, security and return-to-service capabilities;
- cross-substitution remains prohibited;
- positive C4 remains denied regardless of availability.

## 9. Evidence acceptance rules

Evidence must contain a stable ID, date, subject, verifier/actor, explicit result and repository reference. Secrets, passwords, private keys, MFA seeds, recovery codes and identity-document images/numbers must not be stored.

Reciprocal verification is valid only across distinct subjects: Massimo does not verify IDV-001/003 for himself; Leonardo does not verify IDV-002/004 for himself. IDV-005 requires reciprocal confirmation.

## 10. Work-item exit criteria

C04-W03 may complete when:

- IDV-001–IDV-005 are Passed;
- TRN-001–TRN-008 are Passed or have bounded approved exceptions;
- AR-001–AR-006 have attributable decisions;
- AR-007 is recorded N/A by governance design;
- AR-008 and AR-009 remain denied;
- ACC-001/ACC-002 prove distinct non-production sessions;
- REV-001–REV-004 pass in the isolated environment;
- conflicts and limitations remain explicit.

## 11. Current disposition

**C04-W03: IN PROGRESS — IDV EXECUTION RECORD READY; HUMAN/ACCOUNT ATTESTATION PENDING.**

The next executable action is reciprocal completion of IDV-001 through IDV-005 using `ARB-012-C04-IDV-Execution-Record.md`. Runtime, physical-device control, self-approval, positive C4, break-glass and local-interlock bypass remain prohibited.