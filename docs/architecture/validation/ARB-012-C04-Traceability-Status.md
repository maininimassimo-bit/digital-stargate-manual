# ARB-012-C04 — Traceability Status

| Field | Value |
|---|---|
| Condition | `ARB-012-C04` |
| Scope | Role Assignment and Four-Eyes Enforcement |
| Target model | **Two-Person Limited Operations Model** |
| Status | `Pending final ARB re-review — W03/W06/W07 complete` |
| Updated | 2026-08-24 |
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
| C04-W08 | **Ready — final ARB architecture/evidence re-review pending** |

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

The Sponsor-approved target supports:

- Massimo requester/executor + Leonardo C3 approver;
- Massimo Maintainer + Leonardo Return-to-Service Approver;
- Massimo Operations + Leonardo Safety Authority;
- Leonardo Security Authority for Massimo access decisions.

The target denies or excludes:

- self-approval;
- Leonardo self-access approval;
- positive C4;
- break-glass;
- incompatible cross-substitution;
- independent internal audit closure.

A third person, independent substitute or independent internal Auditor is not a C04 closure prerequisite.

## Superseded third-person evidence

`E-ARB012-C04-07` is retained as historical evidence but is **Superseded — N/A by governance design**. No person was nominated through it and no historical control is retroactively marked Passed.

## W03 gate

**COMPLETE.** Applicable IDV/TRN/AR/ACC/REV governance evidence has been reconciled against the approved two-person target, including explicit denial/exclusion of positive C4 and break-glass.

## W06/ENV gate

**COMPLETE.** ENV-011 technical evidence remains valid and VM-R01…VM-R12 residual validation controls have attributable PASS evidence, including distinct non-production identities, least privilege, isolated data/audit stores, reset/repeatability, correlated evidence, self-approval denial, revocation, C4/break-glass denial and simulator-only fallback prevention.

## W07 gate

**COMPLETE — 12/12 PASS.** `E-ARB012-C04-W07-001` records FE-01…FE-12 execution at DSOC commit `7881408279921f83556ebc48f27c29477f27d9cd`.

Key safety/negative results:

- `FE04_STALE_APPROVAL_VALID=false`;
- `FE07_SAFETY_DECISION=DENY`;
- `LOCAL_INTERLOCK_TOUCHED=false`;
- `FE12_TAMPER_DETECTED=true`;
- `PHYSICAL_COMMAND_SENT=false`;
- `PRODUCTION_ACCESS_USED=false`.

FE-10 and FE-11 passed by deterministic denial of positive C4 and break-glass. FE-09 is technical/repository traceability completeness and is not an independent organizational audit claim.

## Remaining gate — C04-W08

Only the final ARB architecture/evidence re-review remains before a closure recommendation can be issued.

The re-review must confirm:

1. W01–W07 evidence is mutually consistent and attributable;
2. the two-person limited-operations target is represented consistently across governance, architecture and validation evidence;
3. explicit limitations remain visible: no positive C4, no break-glass, no self-approval, no independent internal-audit claim;
4. W07 evidence remains isolated, simulator-only and non-production;
5. repository quality/CI is acceptable for the final evidence baseline;
6. closure of C04 does not imply runtime enablement.

## Current disposition

**ARB-012-C04 is READY FOR C04-W08 FINAL ARB RE-REVIEW.**

Runtime enablement remains a separate decision and is not implied by C04 closure.