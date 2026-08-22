# ARB-012-C04 — VM-R05 Authorization Plumbing Assessment

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R05-ASSESS |
| Work item | C04-W06 |
| Control | VM-R05 / ENV-005 |
| Date | 2026-08-22 |
| Status | **Blocked by application authorization plumbing** |
| Runtime effect | None |

## 1. Purpose

Determine whether ENV-005 (two-person least-privilege role mapping) should be implemented at Linux account/group level or in the DigitalStarGate.Control application baseline.

## 2. Repository truth

The current `DigitalStarGate.Control` repository is explicitly in **bootstrap / validation-only** state for ARB-012-C04 W06. Its README states that simulator-only execution is permitted, production/physical-device access is prohibited, positive C4/break-glass are prohibited, and that the bootstrap does not claim operational readiness.

The current repository tree under `src/` contains only `DigitalStarGate.Control.Domain`; the test tree contains only `DigitalStarGate.Control.Domain.Tests`. No implemented Application/API/Infrastructure authorization layer, identity provider, role store, requester/approver workflow, return-to-service authorization service or account-to-role mapping implementation is present in the inspected baseline.

## 3. Architectural disposition

ENV-005 is an **application authorization concern**, not a Linux group-membership concern.

The Linux accounts:

- `dsgmassimo` — distinct non-production validation session, no sudo;
- `dsgleonardo` — distinct non-production validation session, no sudo;

provide identity/session separation for ENV-004 only. They must not be overloaded into application governance roles through ad-hoc OS groups.

The target application mapping remains:

| Identity | Supported application scope | Explicit denial |
|---|---|---|
| Massimo / `dsgmassimo` | Requester, Operator, Maintainer in isolated validation scope | no C3 approval, no self-approval, no own return-to-service approval, no C4, no production access |
| Leonardo / `dsgleonardo` | C3 Approver, Safety Authority, Security Authority, Return-to-Service Approver in isolated validation scope | no requester+approver same action, no self-access approval, no positive C4, no production access |

## 4. VM-R05 result

**VM-R05 cannot yet be executed as an application-level PASS test.**

Reason: the current DSOC baseline does not expose the required authorization plumbing to bind the two validated Linux identities to governed application roles and then prove deterministic deny/allow behavior.

This is not a VM misconfiguration and must not be remediated by granting Linux sudo/group privileges.

## 5. Required implementation before VM-R05 execution

The minimum non-production authorization slice must provide:

1. two validation identities mapped to stable application principals;
2. explicit role assignments for the approved two-person model;
3. deny-by-default authorization;
4. C3 requester/approver separation;
5. self-approval denial;
6. Maintainer / Return-to-Service separation;
7. Security Authority cannot approve own access;
8. positive C4 and break-glass unavailable;
9. attributable audit events with correlation ID;
10. simulator-only execution boundary retained.

Only after that slice exists can ENV-005 be validated and VM-R09/VM-R10/VM-R11 become executable.

## 6. Current disposition

**VM-R05 / ENV-005: BLOCKED — application authorization plumbing not yet implemented in the inspected DSOC baseline.**

VM-R03 and VM-R04 remain valid PASS evidence for distinct non-production accounts. No additional Linux group or sudo changes are required or permitted for VM-R05.