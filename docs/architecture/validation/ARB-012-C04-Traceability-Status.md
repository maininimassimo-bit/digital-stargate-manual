# ARB-012-C04 — Traceability Status

| Field | Value |
|---|---|
| Condition | `ARB-012-C04` |
| Scope | Role Assignment and Four-Eyes Enforcement |
| Target model | **Two-Person Limited Operations Model** |
| Status | `Approved with Conditions — C04-W08-C01 final CI pending` |
| Updated | 2026-08-25 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |

## Work-item traceability

| Work item | Verified status |
|---|---|
| C04-W01 | Complete — Sponsor two-person target decision recorded |
| C04-W02 | Complete — role/conflict register reconciled |
| C04-W03 | Complete — attributable two-person governance evidence recorded |
| C04-W04 | Complete — approved/reconciled FE-01…FE-12 plan |
| C04-W05/W06 | Complete — ENV-011 baseline plus VM-R01…VM-R12 residual controls PASS |
| C04-W07 | **Complete — FE-01…FE-12 = 12/12 PASS** |
| C04-W08 | **Complete — ARB Approved with Conditions** |

## Validated DSOC baselines

- implementation repository: `maininimassimo-bit/DigitalStarGate.Control`;
- original immutable ENV-011 application commit: `37bbd581f37b62243f012cb7a72057207ab10ca6`;
- W07 four-eyes harness validated commit: `7881408279921f83556ebc48f27c29477f27d9cd`;
- validation host: `dsg-arb012-c04-val` on Microsoft Hyper-V;
- guest OS: Ubuntu 26.04 LTS;
- simulator-only configuration: `DSOC-ENV011-SIM-CONFIG-001`;
- fixture SHA-256: `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94`;
- ENV-011 technical-evidence completion merge: `8883c596849907cd63a76c33347ff01386bdd34c`;
- W07 run correlation: `9141ad57-6c11-48ab-a272-192c9a3d7890`.

ENV-011 technical execution remains complete and must not be rerun solely because governance has been reconciled.

## Two-person governance disposition

The Sponsor-approved target supports Massimo requester/executor with Leonardo C3 approver, Massimo Maintainer with Leonardo Return-to-Service Approver, Massimo Operations with Leonardo Safety Authority, and Leonardo Security Authority for Massimo access decisions.

The target denies or excludes self-approval, Leonardo self-access approval, positive C4, break-glass, incompatible cross-substitution and independent internal audit closure. A third person, independent substitute or independent internal Auditor is not a C04 closure prerequisite.

## Completed gates

**W03 COMPLETE.** Applicable IDV/TRN/AR/ACC/REV governance evidence is reconciled against the approved two-person target.

**W06/ENV COMPLETE.** ENV-011 and VM-R01…VM-R12 have attributable PASS evidence covering distinct identities, least privilege, isolation, reset/repeatability, correlation, denial controls, revocation and simulator-only fallback prevention.

**W07 COMPLETE — 12/12 PASS.** `E-ARB012-C04-W07-001` records FE-01…FE-12 at DSOC commit `7881408279921f83556ebc48f27c29477f27d9cd`, including `FE04_STALE_APPROVAL_VALID=false`, `LOCAL_INTERLOCK_TOUCHED=false`, `FE12_TAMPER_DETECTED=true`, `PHYSICAL_COMMAND_SENT=false` and `PRODUCTION_ACCESS_USED=false`.

**W08 COMPLETE — APPROVED WITH CONDITIONS.** `ARB-012-C04-W08-Final-ARB-ReReview.md` records the independent architecture/evidence re-review. No technical validation blocker remains.

## Remaining closure condition

`C04-W08-C01` requires an attributable successful repository CI/quality-gate run on the final reconciled governance baseline.

Until C04-W08-C01 is verified:

- ARB-012-C04 remains `Approved with Conditions`, not `Closed`;
- BKL-011 remains `In Progress`;
- no additional VM validation is required solely for closure;
- runtime enablement remains separate and unauthorized.

## Current disposition

**ARB-012-C04: APPROVED WITH CONDITIONS — FINAL CI ONLY.**

Completion or closure does not authorize production access, physical-device control, positive C4, break-glass or runtime enablement.