# BKL-031 F3-A1-M4 — Site Authority Approval Promotion

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-M4-APPROVAL-001 |
| Stato | **OWNER APPROVED / REPOSITORY INTEGRATION CANDIDATE** |
| Data | 15/09/2026 |
| Baseline | `main@d5750ce160c5f80d20a72bc35dee321200647d03` |
| Protected values | Omitted by policy |
| Runtime / EAGLE | None |

## 1. Decision

The Repository Owner explicitly approved the exact canonical Site Authority payload digest and acknowledged its unbounded half-open validity. The same decision authorizes creation of the protected approval receipt and promotion of the lifecycle to `APPROVED`, while prohibiting publication of exact coordinates, elevation and address.

This public record does not reproduce the protected digest, site identifiers, source locator or exact site facts.

## 2. Repository transition

The package:

- retains the original DRAFT candidate unchanged;
- adds a separate APPROVED envelope with an identical canonical payload;
- adds an immutable, exact-digest and validity-bound owner receipt;
- extends schema/validator parity to the receipt's nested evidence;
- adds eight executable promotion checks, bringing the suite to 59 cases;
- preserves all publication, safety and scope boundaries.

## 3. Capability effect

After integration, the protected repository resolver may return the approved site to an authorized caller within governed validity. Unauthorized requests remain denied and audited without protected content.

No runtime adapter or `CurrentSetupAssignment` exists. Therefore the Observation Planner's runtime S08 remains `UNAVAILABLE` and S09 remains `UNAVAILABLE_CURRENT` despite the approved repository authority.

## 4. Exclusions

No public exact-site projection, setup assignment, provider, ephemeris calculation, forecast, ranking, readiness decision, device command, EAGLE workload or Safety Authority is introduced.

## 5. Acceptance and rollback

Integration requires exact-head CI, ARB, Release Quality, expected-head merge and post-merge verification. The following reconciliation increment must record the actual PR and merge evidence before promoting the next owner decision gate.

Rollback removes the approved envelope and receipt through reviewed Git revert while preserving the DRAFT/history. No runtime, credential, device or observatory rollback is required.
