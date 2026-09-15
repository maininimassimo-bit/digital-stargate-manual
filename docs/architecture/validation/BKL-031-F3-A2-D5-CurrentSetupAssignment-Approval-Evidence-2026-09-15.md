# BKL-031 F3-A2-D5 — CurrentSetupAssignment Approval Evidence

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A2-D5-VAL-001 |
| Status | **IMPLEMENTED / REVIEW CANDIDATE** |
| Date | 15/09/2026 |
| PR | #209 |
| Implementation head | `14e5bbd846c0459939df27343b38ad9b04894d48` |
| Dedicated workflow | `35020381258` — SUCCESS |
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
