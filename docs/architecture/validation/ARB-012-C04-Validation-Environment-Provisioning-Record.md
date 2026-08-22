# ARB-012-C04 — Validation Environment Provisioning and Account Setup Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-04 |
| Work item | C04-W06 — Validation Environment Provisioning and Account Setup |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Version | 1.3 |
| Date | 2026-08-22 |
| Target model | Two-Person Limited Operations Model |
| Status | In Progress — ENV-011 accepted as technical baseline; reduced VM residual controls pending |
| Runtime effect | None |

## 1. Purpose

This record governs the isolated validation environment and the distinct non-production accounts required for ARB-012-C04. Version 1.3 reconciles W06 with the Sponsor-approved Two-Person Limited Operations Model and removes the superseded dependency on a third-person observer/reviewer.

The completed ENV-011 technical campaign remains valid and must not be rerun solely because governance changed. Only controls that still lack attributable evidence remain pending.

## 2. Verified technical baseline — do not repeat

The following facts are already versioned and accepted as the technical VM baseline:

- validation host `dsg-arb012-c04-val` on Microsoft Hyper-V;
- Ubuntu 26.04 LTS guest, kernel `7.0.0-28-generic`;
- .NET SDK `8.0.129`;
- immutable application commit `37bbd581f37b62243f012cb7a72057207ab10ca6`;
- simulator-only effective configuration `DSOC-ENV011-SIM-CONFIG-001`;
- canonical fixture SHA-256 `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94`;
- four domain tests PASS online and PASS again with the VM network adapter disconnected;
- offline transcript showing no operational global IPv4 address and no default route;
- simulator manifest prohibiting physical-device and production integrations;
- Chrony active with synchronized system clock;
- no persisted Git credential helper or plaintext credential file found;
- technical-evidence completion merge commit `8883c596849907cd63a76c33347ff01386bdd34c`;
- DSOC Bootstrap CI #8 `success`.

These facts satisfy the ENV-011 technical objective: the tested commit/configuration and simulator-only execution context are immutable and attributable.

## 3. Provisioning register — reconciled state

| Item ID | Item | Evidence / target | Status |
|---|---|---|---|
| PRV-001 | Validation host or runner | `dsg-arb012-c04-val` / E-ENV011-01 | **Done** |
| PRV-002 | Operating system | Ubuntu 26.04 LTS; kernel `7.0.0-28-generic` | **Done** |
| PRV-003 | Isolation mechanism | Hyper-V VM; offline validation with adapter disconnected | **Done for tested baseline** |
| PRV-004 | Network deny controls | Offline run proves no route/connectivity during ENV-011; persistent/repeatable isolation assertion still required | **Partial** |
| PRV-005 | Validation application | immutable commit `37bbd581...` | **Done** |
| PRV-006 | Non-production configuration | `DSOC-ENV011-SIM-CONFIG-001`, deterministic and checksummed | **Done** |
| PRV-007 | Test database | non-production engine/version/instance | **Pending** |
| PRV-008 | Audit evidence store | non-production store, retention/traceability characteristics | **Pending** |
| PRV-009 | Simulation adapters | simulator manifest; physical access disabled | **Done for tested baseline** |
| PRV-010 | Canonical fixtures | versioned manifest and verified checksum | **Done** |
| PRV-011 | Reset method | snapshot/seed/rebuild repeatability | **Pending** |
| PRV-012 | Time source | Chrony active and synchronized | **Done** |

## 4. Account setup register

The approved target uses two distinct named non-production accounts only.

| Account ID | Natural person | Validation role scope | Prohibited permissions | Reviewer | Status |
|---|---|---|---|---|---|
| ACC-001 | Massimo Mainini | Requester, Operator and Maintainer in isolated validation only | self-approval, C3 approval, own return-to-service approval, C4, production access | Leonardo Di Egidio | Pending creation/evidence |
| ACC-002 | Leonardo Di Egidio | C3 Approver, Safety Authority, Security Authority, Return-to-Service Approver in isolated validation only | requester+approver same action, own access approval, positive C4, production access | Massimo Mainini | Pending creation/evidence |

Required controls: unique usernames, distinct credentials and sessions, deny-by-default grants, explicit role mapping, revocation capability, attributable audit events and no secrets committed as evidence.

No third account or independent observer account is required by the target model.

## 5. ENV acceptance matrix — reduced target

| Check ID | Acceptance criterion | Reconciled status |
|---|---|---|
| ENV-001 | Operational subnets and VPN routes are unreachable | **Partial** — offline evidence exists; repeatable environment-level isolation check still required |
| ENV-002 | No production credential or secret is present | **Partial** — Git/plaintext checks exist; final environment scan/attestation still required |
| ENV-003 | All device adapters resolve only to simulators | **Technical evidence complete** — preserve; no rerun unless configuration changes |
| ENV-004 | Two distinct authenticated accounts exist | **Pending** |
| ENV-005 | Role-to-permission mapping matches W03 two-person model | **Pending** |
| ENV-006 | Self-approval is denied by policy | **Partial** — domain/unit evidence exists; environment scenario pending |
| ENV-007 | Revocation is enforced before execution | **Pending** |
| ENV-008 | Test database and audit store are non-production | **Pending** |
| ENV-009 | Initial state can be reset deterministically | **Pending** |
| ENV-010 | Logs, correlation IDs and evidence export are available | **Pending operational verification** |
| ENV-011 | Tested commit and configuration are immutable and recorded | **PASS — technical baseline accepted under revised target** |
| ENV-012 | Positive C4, break-glass and physical control remain unavailable | **Partial** — technical/source evidence exists; environment denial scenarios pending |

## 6. ENV-011 disposition after governance redesign

The former requirement for `E-ENV011-06` to obtain a third-person independent-review disposition is **superseded by the Two-Person Limited Operations Model**.

`E-ENV011-06` is retained as historical traceability but is no longer a W06 closure blocker. ENV-011 is accepted as a technical baseline because the repository already contains attributable technical evidence for host, immutable commit, configuration, fixture, online/offline execution, time synchronization and simulator-only isolation.

This does not turn an AI review into a human approval and does not claim independent audit closure. Independent internal audit is N/A by governance design.

## 7. W03 dependency

C04-W03 remains required for the supported two-person scope:

- IDV-001–IDV-005;
- TRN-001–TRN-008 or bounded approved exceptions;
- AR-001–AR-006;
- AR-007 N/A by governance design;
- AR-008 positive C4 denied;
- AR-009 break-glass denied;
- ACC-001/ACC-002 evidence;
- REV-001–REV-004.

Positive C4, break-glass and independent internal audit are not target capabilities and therefore cannot become implied prerequisites again.

## 8. Stop conditions

Provisioning or validation must stop immediately if:

- a production route, VPN profile, credential or device endpoint is discovered;
- either account can self-approve;
- request and approval can be performed by the same identity for C3;
- revocation is ineffective before execution;
- positive C4 or break-glass becomes available;
- tested commit/configuration cannot be identified;
- simulator configuration can fall back to production endpoints;
- evidence cannot be attributed or its integrity cannot be demonstrated.

## 9. Reduced VM work package

The only VM activities still required are maintained in `ARB-012-C04-VM-Residual-Checklist.md`.

The reduced sequence is:

1. prove repeatable isolation / no operational routes (ENV-001/PRV-004);
2. perform final no-production-secret scan/attestation (ENV-002);
3. create/evidence ACC-001 and ACC-002 (ENV-004);
4. apply/evidence role mapping (ENV-005);
5. define/evidence non-production test DB and audit store (PRV-007/008, ENV-008);
6. prove reset/rebuild repeatability (PRV-011, ENV-009);
7. verify logging/correlation/evidence export (ENV-010);
8. execute self-approval, revocation, C4/break-glass/physical-control denial scenarios (ENV-006/007/012).

ENV-003 and ENV-011 are not part of the rerun list unless their baseline changes.

## 10. Work-item exit criteria

C04-W06 may be marked complete when:

1. the reduced VM checklist has attributable PASS evidence for all applicable remaining controls;
2. ACC-001 and ACC-002 exist as distinct non-production accounts;
3. role grants match the accepted two-person least-privilege matrix;
4. test DB and audit store are proven non-production;
5. reset/rebuild repeatability is proven;
6. required denial/revocation scenarios pass;
7. no production access or physical-device path exists.

A third person, substitute or independent internal Auditor is not a W06 exit criterion.

## 11. Current disposition

**C04-W06: IN PROGRESS — REDUCED RESIDUAL VM WORK ONLY.**

ENV-011 is accepted as the immutable technical baseline and must not be rerun solely for governance reconciliation. Remaining work is limited to the controls listed in the reduced VM checklist. C04-W07 remains blocked until W03 and these W06 residual controls are complete.