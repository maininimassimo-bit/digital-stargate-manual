# ARB-012-C04 — Identity, Training and Access Review Register

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-02 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Updated | 2026-08-24 |
| Target model | Two-Person Limited Operations Model |
| Status | **PASS — C04-W03 complete** |
| Runtime effect | None |

## 1. Purpose

This register governs identity assurance, role-specific training, least-privilege review and revocation evidence for the approved two-person model. It does not grant runtime privileges.

## 2. Current nominated identities

| Project identity | Natural person | Role group | Current evidence status |
|---|---|---|---|
| DSG-PERSON-001 | Massimo Mainini | Sponsor, architecture, operations, service, technical ownership, Operator, Incident Coordinator, Maintainer, Documentation Governor | **PASS — governance mapping + VM-R03 + Leonardo reciprocal attestation** |
| DSG-PERSON-002 | Leonardo Di Egidio | C3 Approver, Return-to-Service Approver, Safety Authority, Security Authority | **PASS — governance mapping + VM-R04 + Massimo reciprocal attestation** |

## 3. Identity assurance register

Execution artifact: `ARB-012-C04-IDV-Execution-Record.md`.

| Check ID | Identity | Verification requirement | Verified by | Result |
|---|---|---|---|---|
| IDV-001 | Massimo / DSG-PERSON-001 | Natural-person identity mapped to unique project identity | Leonardo | **PASS — 2026-08-23** |
| IDV-002 | Leonardo / DSG-PERSON-002 | Natural-person identity mapped to unique project identity | Massimo | **PASS — 2026-08-22** |
| IDV-003 | Massimo | Non-production authentication account ownership; non-shared | Leonardo | **PASS — 2026-08-23** |
| IDV-004 | Leonardo | Non-production authentication account ownership; non-shared | Massimo | **PASS — 2026-08-22** |
| IDV-005 | Both | Distinct usernames, credentials, factors and sessions | Reciprocal | **PASS — 2026-08-23** |

**Identity disposition: 5/5 PASS.**

## 4. Role-specific training matrix

Execution artifact: `ARB-012-C04-Training-Execution-Record.md`.

| Training ID | Identity | Required subject | Result |
|---|---|---|---|
| TRN-001 | Massimo | C0-C4 classification, request boundaries and self-approval prohibition | **PASS** |
| TRN-002 | Massimo | Maintenance safety, rollback, safe-state preservation and return-to-service handoff | **PASS** |
| TRN-003 | Massimo | Incident recording, audit trail and evidence preservation | **PASS** |
| TRN-004 | Leonardo | Independent C3 approval criteria and conflict rejection | **PASS** |
| TRN-005 | Leonardo | Safety permit, deny, stop and safe-state verification | **PASS** |
| TRN-006 | Leonardo | Privileged-access approval, least privilege and revocation | **PASS** |
| TRN-007 | Leonardo | Return-to-service approval independent from Maintainer | **PASS** |
| TRN-008 | Both | Four-eyes workflow, approver revocation and audit completeness | **PASS** |

**Training disposition: 8/8 PASS.**

## 5. Least-privilege access review

Execution artifact: `ARB-012-C04-Access-Review-Execution-Record.md`.

| Review ID | Subject | Reviewer | Decision |
|---|---|---|---|
| AR-001 | Massimo C0-C2 validation | Leonardo | **PASS — 2026-08-24** |
| AR-002 | Massimo C3 request | Leonardo | **PASS — 2026-08-24** |
| AR-003 | Massimo maintenance | Leonardo | **PASS — 2026-08-24** |
| AR-004 | Leonardo C3 approval | Massimo | **PASS — 2026-08-24** |
| AR-005 | Leonardo Safety Authority | Massimo | **PASS — 2026-08-24** |
| AR-006 | Leonardo Security Authority | Massimo | **PASS — 2026-08-24** |
| AR-007 | Independent internal audit access | N/A | **N/A by governance design** |
| AR-008 | Positive C4 | Policy enforcement | **DENIED — VM-R11 PASS** |
| AR-009 | Break-glass | Policy enforcement | **DENIED — VM-R11 PASS** |

**Least-privilege disposition: AR-001..AR-006 = 6/6 PASS; unsupported scopes remain denied.**

## 6. Required separation checks

| Separation ID | Requirement | Target allocation | Status |
|---|---|---|---|
| SEP-001 | C3 requester distinct from approver | Massimo / Leonardo | **Satisfied by governance allocation and validation evidence** |
| SEP-002 | Maintainer distinct from Return-to-Service Approver | Massimo / Leonardo | **Satisfied by governance allocation and reciprocal review** |
| SEP-003 | Safety Authority distinct from Operations | Leonardo / Massimo | **Satisfied by governance allocation and reciprocal review** |
| SEP-004 | Security Authority distinct from operational beneficiary | Leonardo / Massimo | **Satisfied by governance allocation and reciprocal review** |
| SEP-005 | Independent internal Auditor | Outside target | **N/A by governance design** |
| SEP-006 | Positive C4 chain | Outside target | **DENIED — VM-R11 PASS** |
| SEP-007 | Independent substitutes | Outside target | **N/A; absence suspends dependent capability** |

## 7. Revocation and suspension

Execution artifacts: `ARB-012-C04-Revocation-Reconciliation-Record.md` and `ARB-012-C04-REV001-004-Evidence.md`.

Dedicated validation at DigitalStarGate.Control commit `9c69fe1d1d5cea5c777293a1ddac2eeb31aa2fe3`, correlation ID `c3e9b339-f341-4723-b96b-8e0f507297f6`, completed all four controls.

| Test | Actors/scenario | Result |
|---|---|---|
| REV-001 | Leonardo revokes/suspends Massimo eligibility | **PASS — governance + technical evidence** |
| REV-002 | Massimo suspends Leonardo approval eligibility | **PASS — governance + technical evidence** |
| REV-003 | Pending approval invalidated after suspension | **PASS — stale approval invalidated** |
| REV-004 | Deterministic denied access after revocation | **PASS — deterministic denial demonstrated** |

Safety result: `PHYSICAL_COMMAND_SENT=false`; `PRODUCTION_ACCESS_USED=false`.

**Revocation disposition: 4/4 PASS.**

## 8. Availability model

There are no incompatible-role substitutes in the target model. This remains an accepted degraded-availability characteristic:

- absence of Massimo suspends requester/operator/maintenance-side capabilities;
- absence of Leonardo suspends C3 approval, safety, security and return-to-service capabilities;
- cross-substitution remains prohibited;
- positive C4 remains denied regardless of availability.

## 9. Evidence acceptance rules

Evidence contains stable IDs, dates, subjects, verifier/actor attribution, explicit results and repository references. Secrets, passwords, private keys, MFA seeds, recovery codes and identity-document images/numbers are not stored.

## 10. Work-item exit criteria

All C04-W03 exit criteria are satisfied:

- IDV-001..IDV-005: **5/5 PASS**;
- TRN-001..TRN-008: **8/8 PASS**;
- AR-001..AR-006: **6/6 PASS**;
- AR-007: **N/A by governance design**;
- AR-008/AR-009: **DENIED**;
- distinct non-production accounts/sessions: **demonstrated**;
- REV-001..REV-004: **4/4 PASS**;
- limitations and prohibited capabilities remain explicit.

## 11. Current disposition

**C04-W03: PASS / COMPLETE — 2026-08-24.**

Completion of C04-W03 is an evidence milestone only. It does not authorize runtime or production operation. Physical-device control, self-approval, positive C4, break-glass and local-interlock bypass remain prohibited unless separately governed and explicitly authorized.