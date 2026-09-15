# Digital StarGate Setup Authority Registry

This directory is the GitHub-governed, version-controlled authority location selected by ADR-009 for configuration-baseline and setup-assignment records.

## Publication and classification boundary

- This directory is outside `docs/` and is not a GitHub Pages input.
- Records are protected configuration artifacts unless a separate contract explicitly classifies a projection as public.
- Credentials, secrets, protected coordinates, serial numbers and internal runtime locators are prohibited.
- Observed or projection data may seed a `DRAFT`, but never becomes desired/current authority by inference.

## Lifecycle

`DRAFT -> APPROVED -> RETIRED`

Only an `APPROVED` record with a separately committed approval receipt from the human Approval Authority is eligible as a baseline reference during its validity interval. Baseline approval and setup-assignment approval require distinct evidence. The custodian may prepare and remediate records but cannot approve them.

An approved baseline alone never resolves the current setup. S09 remains `UNAVAILABLE_CURRENT` until the required F3-A1 site record and a separately approved, interval-valid `CurrentSetupAssignment` exist.

## Layout

- `configuration-baselines/`: immutable baseline payloads and lifecycle envelopes;
- `setup-assignments/`: future site-to-baseline assignments; currently empty;
- `approval-evidence/`: immutable human approval receipts.

`DSG-SETUP-BASELINE-001.approved.json` binds the approved lifecycle envelope to payload digest `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8` and receipt `DSG-SETUP-BASELINE-001.approval.json`. Its validity starts at `2026-09-16T00:00:00Z`. It remains protected and excluded from Pages.

The immutable payload retains proposal-time labels and gaps because those fields are covered by the approved digest. Current lifecycle truth is carried only by the outer envelope and matching approval receipt; changing the payload would require a new baseline version, digest and approval.
