# BKL-031 F3-A1-M4 — Site Authority Approval Promotion

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-M4-APPROVAL-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED** |
| Data | 15/09/2026 |
| Baseline | `main@e73b1aa631c41dff97b9e5ededb6d6be02a667d4` |
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

After PR #204 integration, the protected repository resolver may return the approved site to an authorized caller within governed validity. Unauthorized requests remain denied and audited without protected content.

No runtime adapter or `CurrentSetupAssignment` exists. Therefore the Observation Planner's runtime S08 remains `UNAVAILABLE` and S09 remains `UNAVAILABLE_CURRENT` despite the approved repository authority.

## 4. Exclusions

No public exact-site projection, setup assignment, provider, ephemeris calculation, forecast, ranking, readiness decision, device command, EAGLE workload or Safety Authority is introduced.

## 5. Acceptance and rollback

PR #204 was reviewed at exact head `f394ef5c3b5ad089e18fa3c4c431e2fcbd556e38`: CI passed 8/8, ARB decided **APPROVED WITH CONDITIONS — 98/100**, and Release Quality decided **CONDITIONALLY READY**, with no waiver, Blocker or Major. Expected-head merge produced `e73b1aa631c41dff97b9e5ededb6d6be02a667d4`; all 10 post-merge workflows succeeded.

Carried conditions: generalize schema/validator path binding before a second site revision or receipt (`ARB-204-MI01`), and define key/access/deployment boundaries before any runtime adapter (`ARB-204-MI02`). The next gate is a separate owner decision for `CurrentSetupAssignment`.

Rollback removes the approved envelope and receipt through reviewed Git revert while preserving the DRAFT/history. No runtime, credential, device or observatory rollback is required.
