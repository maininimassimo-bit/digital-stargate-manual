# ARB-012-C04 — Closure Plan

| Field | Value |
|---|---|
| Plan ID | ARB-012-C04-PLAN-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Updated | 2026-08-22 |
| Authority | Digital StarGate Chief Architect |
| Target model | **Two-Person Limited Operations Model** |
| Current status | Blocked pending applicable evidence |
| Runtime impact | No runtime enablement authorized |

## 1. Purpose

Define the controlled sequence required to close ARB-012-C04 against the Sponsor-approved two-person target. The earlier closure assumption requiring a third permanent actor, independent substitutes, positive C4 and independent internal audit is superseded.

The revised target preserves fail-safe governance by denying unsupported capabilities rather than weakening segregation requirements.

## 2. Target state

C04 may close when repository evidence demonstrates:

1. Massimo and Leonardo are distinct natural persons using distinct validation accounts/sessions;
2. Massimo requester/executor and Leonardo approver separation works for C3;
3. self-approval and incompatible-role paths are denied;
4. Maintainer/return-to-service separation works;
5. Safety Authority is separated from Operations for supported decisions;
6. Security self-access approval is denied;
7. revocation/suspension invalidates affected authorization before execution;
8. positive C4 is denied with the current two-person allocation;
9. break-glass is denied;
10. applicable environment controls and audit traceability pass;
11. repository quality gates pass;
12. final ARB re-review accepts the revised two-person target.

## 3. N/A by governance design

The following are no longer closure prerequisites:

- third permanent actor;
- independent substitutes for critical roles;
- positive C4 execution or validation;
- independent internal Auditor appointment;
- independent internal audit closure;
- third-party observer solely to validate the two-person model.

No `N/A` item may be reported as `Passed`.

## 4. Dependency-ordered work

### C04-W01 — Sponsor target decision

**Status: Complete.**

`ARB-012-C04-Sponsor-Nomination-Decision.md` records the Two-Person Limited Operations Model.

### C04-W02 — Role/conflict register

**Status: Complete for target definition.**

The role register defines supported C3 separation, denied C4/break-glass, no incompatible cross-substitution and degraded availability when either actor is absent.

### C04-W03 — Identity, training and access evidence

**Status: In Progress.**

Required evidence:

- IDV-001–IDV-005;
- TRN-001–TRN-008 or approved bounded exceptions;
- least-privilege decisions applicable to Massimo/Leonardo;
- distinct non-production accounts;
- revocation/suspension evidence.

A third observer is not required. Each person may review the other person's non-self controls where no conflict exists. Controls that would require independent internal audit are N/A; self-benefiting decisions remain denied.

### C04-W04 — Four-eyes validation plan

**Status: Approved plan requiring reconciliation to the two-person target before execution.**

Required outcomes include positive C3 and return-to-service separation plus denial tests for self-approval, conflicts, C4 and break-glass.

### C04-W05/W06 — Environment and evidence

ENV-011 technical evidence is complete. Remaining applicable PRV/ENV controls, distinct accounts, test database/audit evidence and reset/repeatability must be completed. `E-ENV011-06` must be re-dispositioned under the revised target; absence of a third reviewer is not itself a blocker.

### C04-W07 — Scenario execution

Execute the reconciled FE set in the isolated environment. Unsupported third-person/positive-C4 scenarios are replaced by explicit denial evidence.

### C04-W08 — Final ARB re-review

The final Architecture Review Board review evaluates architecture consistency, evidence sufficiency, fail-safe behavior and scope limitations. It must not claim independent organizational audit if none exists.

## 5. Quality gates

| Gate | Required disposition |
|---|---|
| Sponsor two-person target decision | Passed |
| Role/conflict target definition | Passed |
| Third person / substitute coverage | N/A by governance design |
| W03 identity/training/access | Passed for applicable scope |
| Distinct validation accounts | Passed |
| Applicable ENV controls | Passed |
| C3 four-eyes scenarios | Passed |
| Self-approval/conflict denial | Passed |
| Positive C4 | Denied by design and validated as denied |
| Break-glass | Denied by design and validated as denied |
| Independent internal audit closure | N/A by governance design |
| Repository CI | Passed |
| Final ARB architecture/evidence re-review | Passed |
| Runtime enablement | Separate decision; not implied by C04 |

## 6. Risks and controls

| Risk | Severity | Control |
|---|---|---|
| Self-approval | Critical | Deterministic denial and evidence |
| Loss of one actor | High availability impact | Suspend operations requiring both; no incompatible cross-substitution |
| Attempt to use C4 with two actors | Critical | Deny positive C4 |
| Break-glass bypass | Critical | Deny break-glass |
| Leonardo reviews own access/control | High | Self-review denied; no independent audit claim |
| C04 closure interpreted as runtime authorization | Critical | Runtime remains a separate gate |
| Physical interlock bypass | Critical | Prohibited; local interlocks remain authoritative |

## 7. Current disposition

**ARB-012-C04 remains BLOCKED pending evidence applicable to the approved two-person target.**

The organizational-design blocker requiring a third person is removed. Remaining work is IDV/TRN/access/revocation, applicable environment evidence, reconciled FE execution, CI and final ARB re-review.