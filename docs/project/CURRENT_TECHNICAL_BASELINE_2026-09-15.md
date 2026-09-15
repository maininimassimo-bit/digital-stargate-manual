# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — F3-A2-D5 ACCEPTED / POST-MERGE VERIFIED** |
| Repository baseline | `main@bc4307c2042a45985622044e11631421de5b2c3d` |
| Current package | `BKL-031-F3-A2-D5` accepted; Program Architect successor selection current |
| Runtime delta | None |
| Data delta | Protected approval receipt and unchanged APPROVED lifecycle envelope integrated |
| Infrastructure delta | None |

## 1. Integrated state

PR #209 is merged as `bc4307c2042a45985622044e11631421de5b2c3d` and establishes the current verified repository baseline with 7/7 post-merge workflows. The protected setup baseline, Site Authority and CurrentSetupAssignment are separately approved. The historical assignment DRAFT remains immutable; the protected receipt and separate APPROVED envelope preserve the payload and digest.

## 2. Approved authority state

The setup baseline and Site Authority are independently approved. Their exact digests, internal identifiers, locators and protected site facts are intentionally omitted from this public baseline. Lifecycle truth is the applicable immutable payload plus its separate approval receipt.

## 3. Dependency readiness

| Elemento | Stato |
|---|---|
| Setup authority source/roles | integrated |
| First setup baseline | APPROVED / post-merge verified |
| F3-A1 normative site contract | accepted with conditions |
| Exact protected site facts | approved authority outside Pages; omitted publicly |
| Site Authority owner/approver/source | complete; receipt and lifecycle post-merge verified |
| Elevation vertical semantics | materialized and validated |
| Canonical site resolver identity/scope | materialized and validated |
| Executable validity/privacy/promotion tests | 59/59 PASS; exact-head and post-merge verified |
| CurrentSetupAssignment | APPROVED in repository authority; resolver `AVAILABLE` for authorized validated input; historical DRAFT retained |
| Assignment owner decisions | complete; protected evidence integrated |
| Assignment lifecycle validation | exact publication head 5/5 SUCCESS; 65/65 tests; post-merge 7/7 SUCCESS |
| S08 / S09 | `UNAVAILABLE` / `UNAVAILABLE_CURRENT` |
| Runtime adapter | absent; separate package and authorization required |

## 4. Rollback

The F3-A1-M4 promotion can be reverted through reviewed Git history by removing the APPROVED envelope and receipt while retaining the historical DRAFT. Approved authority retirement remains governed by ADR-009. No runtime, migration, credential or observatory impact exists.

## F3-A2-D4 baseline delta

PR #207 integrated repository-only protected authority artifacts and a redacted validation workflow. S08 remains unavailable to runtime and S09 remains `UNAVAILABLE_CURRENT`. No runtime, EAGLE, provider, readiness, command or Safety Authority delta is present. Rollback is the reviewed revert of the D4 merge; no operational rollback is required.


## F3-A2-D5 accepted delta

PR #209 integrated protected receipt/promotion artifacts, one closed schema, validator/tests and sanitized documentation. The approved envelope preserves the D4 assignment payload and digest. Repository resolution is `AVAILABLE` for authorized validated callers with approved sources. Runtime S09 remains `UNAVAILABLE_CURRENT` because no adapter is introduced. No EAGLE, provider, readiness, command or Safety Authority delta is present.

## F3-A2-D5 post-merge evidence

Exact publication head `6947e79a53282db2a7f6d879643e51840ed9e553` passed 5/5 applicable workflows and the 65-case suite. Expected-head merge `bc4307c2042a45985622044e11631421de5b2c3d` passed all 7 post-merge workflows, including GitHub Pages. D5 is ACCEPTED / POST-MERGE VERIFIED. The next state transition is Program Architect selection; runtime adapter work remains a separate package gated by `ARB-204-MI02`.
