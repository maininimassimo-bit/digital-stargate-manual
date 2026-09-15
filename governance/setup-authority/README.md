# Digital StarGate Setup Authority Registry

This directory is the GitHub-governed, version-controlled authority location selected by ADR-009 for configuration-baseline and setup-assignment records.

## Publication and classification boundary

- This directory is outside `docs/` and is not a GitHub Pages input.
- Records are protected configuration artifacts unless a separate contract explicitly classifies a projection as public.
- Credentials, secrets, protected coordinates, serial numbers and internal runtime locators are prohibited.
- Observed or projection data may seed a `DRAFT`, but never becomes desired/current authority by inference.

## Lifecycle

`DRAFT -> APPROVED -> RETIRED`

Only an `APPROVED` record with a separately committed approval receipt from the human Approval Authority is eligible for resolution. Baseline approval and setup-assignment approval require distinct evidence. The custodian may prepare and remediate records but cannot approve them.

## Layout

- `configuration-baselines/`: immutable baseline payloads and lifecycle envelopes;
- `setup-assignments/`: future site-to-baseline assignments; currently empty;
- `approval-evidence/`: future approval receipts; currently empty.

The initial record `DSG-SETUP-BASELINE-001.draft.json` remains fail-closed. Its payload digest is `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`; it is not an approved baseline and cannot make S09 available.
