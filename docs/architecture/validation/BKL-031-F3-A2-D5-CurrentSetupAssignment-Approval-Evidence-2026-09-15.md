# BKL-031 F3-A2-D5 — CurrentSetupAssignment Approval Evidence

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A2-D5-VAL-001 |
| Status | **ACCEPTED / POST-MERGE VERIFIED** |
| Date | 15/09/2026 |
| PR | #209 |
| Implementation head | `14e5bbd846c0459939df27343b38ad9b04894d48` |
| Exact publication head | `6947e79a53282db2a7f6d879643e51840ed9e553` |
| Merge | `bc4307c2042a45985622044e11631421de5b2c3d` |
| Dedicated exact-head workflow | `35021526883` — SUCCESS, 65/65 |
| Post-merge workflows | 7/7 SUCCESS |
| Runtime / EAGLE | Not applicable / none |

## Verified evidence

- owner authorization matched the exact protected DRAFT digest;
- the protected receipt validates against a closed schema;
- the APPROVED envelope validates and points to the matching receipt;
- historical DRAFT and approved assignment payload canonicalize identically;
- the protected digest is unchanged through promotion;
- validity remains half-open from the approved setup-baseline effective start with no end;
- assignment owner and human Approval Authority match; the custodian is not an approver;
- the approved repository envelope resolves `AVAILABLE` only with the approved Site Authority and setup baseline;
- the DRAFT remains resolver-ineligible;
- workflow diagnostics contain only redacted lifecycle/result metadata.

## Executable result

| Group | Result |
|---|---|
| Existing A2/D4/property suite | 57/57 PASS |
| D5 approval/promotion cases | 8/8 PASS |
| Total | 65/65 PASS |
| Failures | 0 |

The D5 cases cover receipt validation, approved-envelope validation, payload/digest immutability, promotion binding, approved-source resolution, payload mutation, invalid approving authority and subject/validity mismatch.

## Boundaries

This evidence validates repository authority only. It does not implement a runtime adapter, activate portal S09, operate EAGLE, issue a device command, decide readiness/go-no-go or modify Safety Authority. Exact protected values remain outside public evidence.

## Exact-head and post-merge evidence

Exact publication head `6947e79a53282db2a7f6d879643e51840ed9e553` completed all five applicable PR workflows successfully:

- Setup Assignment Governance `35021526883`;
- Scientific Platform Governance `35021526950`;
- Word `35021526834`;
- documentation validation `35021526906`;
- Developer Foundation `35021526839`.

Documentation governance recorded `ACCEPTED WITH OBSERVATION`. The AI-assisted, process-separated ARB recorded `APPROVED WITH CONDITIONS — 99/100`; Release Quality recorded `CONDITIONALLY READY FOR MERGE`. They are not equivalent to independent human approval. No Blocker or Major remained open.

Expected-head merge produced `bc4307c2042a45985622044e11631421de5b2c3d`. Setup Assignment Governance `35022075396`, Scientific Platform Governance `35022075485`, Governed Projection Sync `35022075340`, documentation validation `35022075416`, Word `35022075448`, Developer Foundation `35022075437` and GitHub Pages `35022075365` all completed `SUCCESS`.

D5 is therefore ACCEPTED / POST-MERGE VERIFIED. Repository authority is `APPROVED/AVAILABLE` for authorized validated input; runtime S09 remains `UNAVAILABLE_CURRENT` and no runtime/EAGLE/Safety change exists.
