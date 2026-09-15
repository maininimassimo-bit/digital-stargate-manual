# BKL-031 F3-A2-D1 — Authority and Baseline Draft Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D1-ACCEPTANCE-001 |
| Stato | **ACCEPTED / PR #201 POST-MERGE VERIFIED** |
| Data | 15/09/2026 |
| Integrated PR | #199 |
| Publication head | `7c124d6f2cb1b6356c7008ac2f70824b5579a262` |
| Merge | `4e8802c80359efce28d8d75521a1b9cc4cb44b05` |
| Review | ARB 99/100; Release Quality Conditionally Ready |
| Runtime / EAGLE | None |

## 1. Accepted increment

PR #199 integrated the owner-authorized GitHub setup-authority model, ADR-009, the protected registry outside `docs/`, the mandatory stop-notification rule and the first exact DRAFT payload.

The Repository Owner confirmed:

- one composite baseline for the parallel Quattro 200P and C8 profiles on CGX-L;
- validity from `2026-09-16T00:00:00Z`;
- explicit null/`DA_VALIDARE` exceptions for C8 guiding, serials and runtime versions.

These choices defined the candidate. The Repository Owner subsequently approved the exact digest and validity through the owner-controlled interaction channel. The separate receipt is now part of this lifecycle-promotion package.

## 2. Exact candidate state

| Elemento | Stato |
|---|---|
| Baseline ID | `DSG-SETUP-BASELINE-001` |
| Payload digest | `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8` |
| Lifecycle | `APPROVED` |
| Baseline-reference eligible | true only inside the approved validity interval |
| Approval receipt | `DSG-SETUP-BASELINE-001-APPROVAL-001` / exact-digest bound |
| CurrentSetupAssignment | absent |
| S09 | `UNAVAILABLE_CURRENT` |
| Publication | protected; excluded from Pages |

The digest was independently recomputed and matched. JSON parse and source-lineage checks are verified. Approved-schema validation, physical inventory and runtime OAT are correctly `NOT_EXECUTED`.

## 3. Reviews and CI

ARB AI-assisted: **APPROVED WITH CONDITIONS — 99/100**. Release Quality AI-assisted: **CONDITIONALLY READY FOR MERGE**. These reviews are process-separated and not equivalent to independent human approval.

Exact publication head completed 7/7 PR workflows. Merge `4e8802c80359efce28d8d75521a1b9cc4cb44b05` completed 9/9 post-merge workflows:

| Workflow | Run | Esito |
|---|---:|---|
| Developer Foundation | #1447 | SUCCESS |
| Validate documentation | #1084 | SUCCESS |
| Genera manuale Word | #1510 | SUCCESS |
| Scientific Platform Governance | #147 | SUCCESS |
| BKL-041 F4 Governance | #149 | SUCCESS |
| BKL-046 F4 governance | #123 | SUCCESS |
| BKL-046 F5 governance | #108 | SUCCESS |
| Governed Projection Sync | #60 | SUCCESS |
| Deploy MkDocs artifact to GitHub Pages | #808 | SUCCESS |

## 4. Finding disposition

- `ARB-197-MI01-A`: closed by ADR-009 for authority system, roles, evidence location and separation.
- `ARB-197-MI01-B` / `ARB-199-MI01`: closed by exact-digest human approval and matching receipt.
- `ARB-199-MI02`: assigned to schema/validator materialization.
- `ARB-199-MI03`: assigned before S09 activation to F3-A1 site record and separately approved assignment.

No Blocker or Major remains for the owner-approved lifecycle-promotion review candidate.

## 5. Next mandatory gate

After exact-head review, CI, merge and post-merge verification of this approval package, F3-A1 concrete site materialization and a separately approved `CurrentSetupAssignment` remain mandatory before S09 can become available. Baseline approval does not create or imply either record.

## 6. Rollback

Retire or revert the approved envelope and receipt through reviewed Git history. No migration, runtime deployment, credential or observatory operation exists.


## 7. PR #201 lifecycle completion

PR #201 integrated the separate approval receipt and the `APPROVED` lifecycle envelope without mutating the canonical payload. The reviewed head was `e12aad1c3ea5f817e78759020a2b4621d094bcc4`; the merge is `9932bace989565a10fd8e0d6f4a9c3b2cc057c46`; post-merge verification completed 6/6 workflows. The detailed outcome is recorded in [BKL-031 F3-A2-D2 Baseline Approval Acceptance](BKL-031-F3-A2-D2-BASELINE-APPROVAL-ACCEPTANCE-2026-09-15.md).
