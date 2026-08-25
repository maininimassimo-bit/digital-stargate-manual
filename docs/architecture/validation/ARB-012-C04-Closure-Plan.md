# ARB-012-C04 — Closure Plan

| Field | Value |
|---|---|
| Plan ID | ARB-012-C04-PLAN-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Updated | 2026-08-25 |
| Authority | Digital StarGate Chief Architect |
| Target model | **Two-Person Limited Operations Model** |
| Current status | **Approved with Conditions — final repository CI pending** |
| Runtime impact | No runtime enablement authorized |

## 1. Purpose

Define and record the controlled closure of ARB-012-C04 against the Sponsor-approved two-person target. The earlier closure assumption requiring a third permanent actor, independent substitutes, positive C4 and independent internal audit is superseded.

The target preserves fail-safe governance by denying unsupported capabilities rather than weakening segregation requirements.

## 2. Target state

C04 closure requires repository evidence demonstrating:

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

Items 1–10 and 12 are complete. Item 11 remains the sole closure condition after final governance reconciliation.

## 3. N/A by governance design

The following are not closure prerequisites:

- third permanent actor;
- independent substitutes for critical roles;
- positive C4 execution or validation;
- independent internal Auditor appointment;
- independent internal audit closure;
- third-party observer solely to validate the two-person model.

No `N/A` item is reported as `Passed`.

## 4. Dependency-ordered work

### C04-W01 — Sponsor target decision

**Status: Complete.** Sponsor decision records the Two-Person Limited Operations Model.

### C04-W02 — Role/conflict register

**Status: Complete.** Supported C3 separation, denied C4/break-glass, no incompatible cross-substitution and degraded availability are reconciled.

### C04-W03 — Identity, training and access evidence

**Status: Complete.** Applicable identity verification, training, least-privilege access review and revocation/suspension governance evidence has been completed against the two-person target. Independent internal audit remains N/A by governance design and no self-benefiting review is accepted.

### C04-W04 — Four-eyes validation plan

**Status: Complete.** FE-01..FE-12 were reconciled to the two-person target before execution.

### C04-W05/W06 — Environment and evidence

**Status: Complete.** ENV-011 and VM-R01..VM-R12 residual controls have attributable PASS evidence covering isolated non-production operation, identities, audit/evidence, reset/repeatability, denial controls, revocation and simulator-only fallback prevention.

### C04-W07 — Scenario execution

**Status: Complete — FE-01..FE-12 = 12/12 PASS.** Evidence is recorded in `ARB-012-C04-W07-Four-Eyes-Evidence.md`, run correlation `9141ad57-6c11-48ab-a272-192c9a3d7890`, DSOC commit `7881408279921f83556ebc48f27c29477f27d9cd`.

### C04-W08 — Final ARB re-review

**Status: Complete — APPROVED WITH CONDITIONS.** `ARB-012-C04-W08-Final-ARB-ReReview.md` records the independent review. There are no remaining technical validation blockers. The sole remaining closure condition is an attributable successful repository CI/quality-gate run on the final reconciled governance baseline.

## 5. Quality gates

| Gate | Current disposition |
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
| Repository CI | **Pending final reconciled baseline run** |
| Final ARB architecture/evidence re-review | **Approved with Conditions** |
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

**ARB-012-C04 is APPROVED WITH CONDITIONS.**

W01–W08 are complete from architecture/governance and technical-validation perspectives. The only remaining closure condition is `C04-W08-C01`: successful repository CI/quality-gate evidence on the final reconciled governance baseline.

Until that evidence is verified, C04 must not be marked `Closed` and BKL-011 remains `In Progress`.

Even after closure, runtime enablement, production access, physical-device control, positive C4 and break-glass are not authorized by C04.