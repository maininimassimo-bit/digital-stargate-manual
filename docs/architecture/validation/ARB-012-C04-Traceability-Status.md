# ARB-012-C04 — Traceability Status

| Field | Value |
|---|---|
| Condition | `ARB-012-C04` |
| Scope | Role Assignment and Four-Eyes Enforcement |
| Target model | **Two-Person Limited Operations Model** |
| Status | `Blocked — organizational target approved; applicable W03/W06/W07 evidence pending` |
| Updated | 2026-08-22 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |

## Work-item traceability

| Work item | Verified status |
|---|---|
| C04-W01 | Complete — Sponsor two-person target decision recorded |
| C04-W02 | Complete for target definition — role/conflict register reconciled |
| C04-W03 | In Progress — two-person execution package ready; IDV/TRN/AR/REV evidence pending |
| C04-W04 | Approved/reconciled plan; FE-01…FE-12 not executed |
| C04-W05/W06 | ENV-011 technical evidence complete; remaining applicable PRV/ENV/account controls pending |
| C04-W07 | Blocked by W03/W06 completion; reconciled FE plan ready |
| C04-W08 | Final ARB re-review not started |

## Immutable DSOC baseline

- implementation repository: `maininimassimo-bit/DigitalStarGate.Control`;
- immutable application commit: `37bbd581f37b62243f012cb7a72057207ab10ca6`;
- validation host: `dsg-arb012-c04-val` on Microsoft Hyper-V;
- guest OS: Ubuntu 26.04 LTS;
- simulator-only configuration: `DSOC-ENV011-SIM-CONFIG-001`;
- fixture SHA-256: `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94`;
- technical-evidence completion merge: `8883c596849907cd63a76c33347ff01386bdd34c`;
- DSOC Bootstrap CI #8: success.

ENV-011 technical execution remains complete and must not be rerun solely because governance has been reconciled.

## Two-person governance disposition

The Sponsor-approved target explicitly supports:

- Massimo requester/executor + Leonardo C3 approver;
- Massimo Maintainer + Leonardo Return-to-Service Approver;
- Massimo Operations + Leonardo Safety Authority;
- Leonardo Security Authority for Massimo access decisions.

The target explicitly denies or excludes:

- self-approval;
- Leonardo self-access approval;
- positive C4;
- break-glass;
- incompatible cross-substitution;
- independent internal audit closure.

A third person, independent substitute or independent internal Auditor is no longer a C04 closure prerequisite.

## Superseded third-person evidence

`E-ARB012-C04-07` is retained as historical evidence but is now **Superseded — N/A by governance design**. No person was nominated through it and no historical control is retroactively marked Passed.

## Remaining W03 gate

Execute attributable evidence for:

- IDV-001–IDV-005;
- TRN-001–TRN-008 or approved bounded exceptions;
- AR-001–AR-006;
- AR-007 = N/A by governance design;
- AR-008 positive C4 = DENIED;
- AR-009 break-glass = DENIED;
- ACC-001/ACC-002 distinct non-production sessions;
- REV-001–REV-004.

## Remaining W06/ENV gate

Complete the still-applicable provisioning/environment controls: distinct accounts, non-production database/audit evidence as required by the validation implementation, reset/repeatability and applicable ENV acceptance. Reconcile `E-ENV011-06` so it evaluates technical evidence against the revised two-person target rather than requiring a third-person nomination.

## Remaining W07 gate

Execute FE-01…FE-12 according to the reconciled plan. FE-10 and FE-11 pass only by demonstrating deterministic denial of positive C4 and break-glass. FE-09 demonstrates technical/repository traceability completeness and is not an independent organizational audit claim.

## Exit criteria

ARB-012-C04 may move from `Blocked` after:

1. applicable W03 evidence passes;
2. applicable W06/ENV/account controls pass;
3. FE-01…FE-12 produce the expected two-person results;
4. self-approval, C4 and break-glass denial tests pass;
5. repository CI passes;
6. final ARB architecture/evidence re-review accepts the revised target and its explicit limitations.

Runtime enablement remains a separate decision and is not implied by C04 closure.