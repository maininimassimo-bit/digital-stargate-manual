# ARB-012-C04 — Validation Environment Provisioning and Account Setup Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-04 |
| Work item | C04-W06 — Validation Environment Provisioning and Account Setup |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Version | 1.2 |
| Date | 2026-08-22 |
| Status | In Progress — ENV-011 technical evidence complete; remaining provisioning, accounts and ENV controls pending |
| Runtime effect | None |

## 1. Purpose

This record governs the controlled provisioning of the isolated environment defined by `ARB-012-C04-Validation-Environment-Baseline.md` and the creation of distinct non-production accounts required for later four-eyes validation.

This revision reconciles the original provisioning plan with evidence produced after version 1.1. It does **not** repeat or invalidate the already completed ENV-011 technical campaign. Where later evidence exists, the register below reflects that evidence; controls without attributable evidence remain pending.

## 2. Verified technical baseline

The following environment facts are already versioned and do not require re-execution solely for documentation reconciliation:

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
- technical-evidence completion merge commit `8883c596849907cd63a76c33347ff01386bdd34c` and DSOC Bootstrap CI #8 `success`.

ENV-011 therefore has **complete positive technical evidence**. Formal acceptance remains pending only because `E-ENV011-06` requires an attributable independent-review disposition.

## 3. Provisioning register — reconciled state

| Item ID | Item | Verified / required value | Evidence reference | Status |
|---|---|---|---|---|
| PRV-001 | Validation host or runner | `dsg-arb012-c04-val` | E-ENV011-01 | Recorded |
| PRV-002 | Operating system | Ubuntu 26.04 LTS; kernel `7.0.0-28-generic` | E-ENV011-01 / ENV-011 execution result | Recorded |
| PRV-003 | Isolation mechanism | Microsoft Hyper-V VM; offline validation performed with adapter disconnected | E-ENV011-01 / E-ENV011-04A | Recorded for ENV-011 scope |
| PRV-004 | Network deny controls | Offline run proves no route/connectivity during ENV-011; permanent full ENV-001 isolation control still requires acceptance evidence | E-ENV011-04A | Partial — remaining ENV control pending |
| PRV-005 | Validation application | `DigitalStarGate.Control` commit `37bbd581f37b62243f012cb7a72057207ab10ca6` | immutable baseline / DSOC CI #2 | Recorded |
| PRV-006 | Non-production configuration | `DSOC-ENV011-SIM-CONFIG-001`, deterministic and checksummed | E-ENV011-03A | Recorded |
| PRV-007 | Test database | Non-production engine/version/instance | No attributable evidence found | Pending |
| PRV-008 | Audit evidence store | Store identifier, append-only control and retention | No attributable evidence found | Pending |
| PRV-009 | Simulation adapters | Versioned simulator manifest; physical access disabled | E-ENV011-03A / E-ENV011-05 | Recorded for ENV-011 scope |
| PRV-010 | Canonical fixtures | Versioned manifest and verified unsafe-weather checksum | E-ENV011-03 / E-ENV011-03A | Recorded |
| PRV-011 | Reset method | Snapshot/seed/rebuild repeatability | No attributable evidence found | Pending |
| PRV-012 | Time source | Chrony active and synchronized | E-ENV011-01B | Recorded |

A `Recorded` state above means the specific technical fact is supported by existing evidence. It does not imply W06 completion or formal environment acceptance.

## 4. Account setup register

Only distinct, named, non-production accounts are permitted. No repository evidence was found that supports changing the following states:

| Account ID | Natural person | Validation role scope | Prohibited permissions | Reviewer | Status |
|---|---|---|---|---|---|
| ACC-001 | Massimo Mainini | Requester, Operator and Maintainer in isolated validation only | Self-approval, C3 approval, Return-to-Service approval of own maintenance, C4 approval, production access | Leonardo Di Egidio subject to conflict check | Pending creation/evidence |
| ACC-002 | Leonardo Di Egidio | C3 Approver, Safety Authority, Security Authority and Return-to-Service Approver in isolated validation only | Request and approval for same operation, approval of own privileged access, positive C4 completion, production access, independent audit closure | Independent verification required | Pending creation/evidence |

Mandatory controls remain: unique usernames, distinct credentials and sessions, deny-by-default grants, explicit role mapping, revocation before later authorization checks, attributable audit events and no secrets committed as evidence.

## 5. ENV acceptance matrix — reconciled state

| Check ID | Acceptance criterion | Reconciled status |
|---|---|---|
| ENV-001 | Operational subnets and VPN routes are unreachable | Partial evidence from offline ENV-011; complete environment control still pending |
| ENV-002 | No production credential or secret is present | Partial technical evidence; complete environment acceptance pending |
| ENV-003 | All device adapters resolve only to simulators | Technical evidence available; formal ENV-set acceptance pending |
| ENV-004 | Two distinct authenticated accounts exist | Pending |
| ENV-005 | Role-to-permission mapping matches C04-W03 | Pending |
| ENV-006 | Self-approval is denied by policy | Domain/unit-test evidence exists; environment scenario evidence pending |
| ENV-007 | Revocation is enforced before execution | Pending |
| ENV-008 | Test database and audit store are non-production | Pending |
| ENV-009 | Initial state can be reset deterministically | Pending |
| ENV-010 | Logs, correlation IDs and evidence export are available | Pending |
| ENV-011 | Tested commit and configuration are immutable and recorded | **Technical evidence complete; formal independent disposition pending** |
| ENV-012 | C4, break-glass and physical control remain unavailable | Technical source/simulator evidence exists; formal environment scenario evidence pending |

## 6. Independent review gate

`E-ENV011-06` remains mandatory. The independent AI technical re-review already recorded in the repository is informative technical review only and is **not** substituted for the attributable reviewer disposition required by ARB-012-C04.

Until `E-ENV011-06` is `Passed` by an attributable independent reviewer:

- ENV-011 is not formally accepted;
- C04-W06 remains `IN PROGRESS`;
- C04-W07 remains blocked.

## 7. W03 dependency

C04-W03 remains a prerequisite for positive four-eyes scenarios. Identity assurance, role-specific training, least-privilege decisions and revocation evidence in `ARB-012-C04-Identity-Training-Access-Review.md` remain pending unless separately supported by attributable evidence.

The current two-person allocation may support limited non-operational C3 validation only after W03 and W06 prerequisites are satisfied. It does not support positive C4, independent audit closure or substitute resilience.

## 8. Stop conditions

Provisioning or validation must stop immediately if:

- a production route, VPN profile, credential or device endpoint is discovered;
- either account can self-approve;
- request and approval can be performed by the same identity;
- revocation is not effective before execution;
- positive C4 or break-glass becomes available;
- tested commit/configuration cannot be identified;
- simulator configuration can fall back to production endpoints;
- evidence cannot be attributed or its integrity cannot be demonstrated.

## 9. Work-item exit criteria

C04-W06 may be marked complete only when:

1. remaining PRV items have attributable evidence;
2. ACC-001 and ACC-002 exist as distinct non-production accounts;
3. role grants match the accepted least-privilege matrix;
4. ENV-001 through ENV-012 are executed and formally passed;
5. reset/rebuild repeatability is proven;
6. `E-ENV011-06` is `Passed` by an attributable independent reviewer;
7. no production access or physical-device path exists.

## 10. Current disposition

**C04-W06: IN PROGRESS.**

ENV-011 technical execution is complete and must **not** be rerun solely because version 1.1 of this document was stale. Remaining blockers are formal independent acceptance plus the still-unverified PRV/account/ENV controls listed above.

C04-W07 remains blocked. `ARB-012-C04` remains `Blocked`. Runtime activation, production credentials, observatory routes, physical-device control, positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.