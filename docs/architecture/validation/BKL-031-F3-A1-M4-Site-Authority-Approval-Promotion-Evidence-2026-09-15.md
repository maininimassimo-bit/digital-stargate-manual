# BKL-031 F3-A1-M4 — Site Authority Approval Promotion Evidence

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-M4-VAL-001 |
| Stato | **59/59 PASS / EXACT-HEAD AND POST-MERGE VERIFIED** |
| Data | 15/09/2026 |
| Baseline | `main@e73b1aa631c41dff97b9e5ededb6d6be02a667d4` |
| Protected values | Omitted by policy |
| Runtime / OAT | Not Applicable |

## 1. Scope

Validate the separately owner-approved transition from the immutable protected DRAFT candidate to an APPROVED envelope. The package adds a protected approval receipt, preserves the candidate for audit and verifies that the approved envelope contains an identical canonical payload and digest.

The approval is exact-digest and validity-bound. Its protected statement, internal identifiers and digest are deliberately absent from this public evidence.

## 2. Promotion invariants

- DRAFT candidate remains present, ineligible and without approval evidence;
- APPROVED envelope changes lifecycle metadata only;
- canonical payload and internal digest are identical across candidate and approved envelope;
- receipt subject binds identity, revision, digest and half-open unbounded validity;
- human approving authority is the Repository Owner; the Architecture Office remains non-approving custodian;
- receipt timestamp and approved-envelope timestamp match;
- receipt, candidate and approved paths bind exactly;
- publication restrictions remain unchanged;
- authorized repository resolution is available within validity; unauthorized access fails closed and is audited;
- runtime S08/S09 remain unavailable because no adapter or assignment is introduced.

## 3. Executable evidence

| Range | Count | Local result | Exact-head gate |
|---|---:|---|---|
| A1-P01–P10 | 10 | PASS | PASS |
| A1-N01–N41 | 41 | PASS | PASS |
| M4-P01–P02 | 2 | PASS | PASS |
| M4-N01–N06 | 6 | PASS | PASS |
| Total | 59 | **PASS** | **PASS** |

Commands:

- `node governance/site-authority/tools/site-authority-validator.mjs`
- `node --test governance/site-authority/tools/test-site-authority.mjs`

The validator output is generic and never prints protected values or the internal digest.

## 4. Negative promotion cases

The M4 suite rejects:

- non-approved receipt decisions;
- receipt digest mismatch;
- validity mismatch;
- approving-authority mismatch;
- approval-evidence path mismatch;
- any payload mutation during lifecycle promotion.

## 5. Security and safety

The protected registry remains outside Pages and repository membership remains the access boundary. No public coordinate, elevation, exact address, internal identifier, source locator or internal digest is added. No runtime, credential, device command, readiness, EAGLE workload or Safety Authority change occurs. Local interlocks remain independent.

## 6. Review and integration evidence

- PR: #204;
- reviewed exact head: `f394ef5c3b5ad089e18fa3c4c431e2fcbd556e38`;
- exact-head workflows: 8/8 SUCCESS;
- ARB: `APPROVED WITH CONDITIONS — 98/100`;
- Release Quality: `CONDITIONALLY READY`; no waiver, Blocker or Major;
- expected-head merge: `e73b1aa631c41dff97b9e5ededb6d6be02a667d4`;
- post-merge workflows: 10/10 SUCCESS, including the dedicated Site Authority gate, projection sync, documentation and Pages.

`ARB-204-MI01` and `ARB-204-MI02` are carried into the next applicable revision/adapter packages; neither invalidates the accepted lifecycle promotion.

## 7. Rollback

Revert the approved envelope and receipt, leaving the immutable DRAFT candidate as historical evidence and returning repository resolution to `UNAVAILABLE`. No runtime or observatory rollback is required.
