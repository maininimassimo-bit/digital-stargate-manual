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
- `setup-assignments/`: immutable site-to-baseline lifecycle envelopes; the historical `DRAFT` and separate `APPROVED` envelope are retained;
- `schemas/`: closed, versioned assignment, owner-decision and approval-receipt schemas;
- `tools/`: deterministic validator, privacy gate and executable contract tests;
- `decision-evidence/`: immutable owner decisions that authorize bounded future materialization but are not lifecycle approval;
- `approval-evidence/`: immutable human approval receipts.

The first configuration baseline is approved with its separate receipt. Its immutable payload retains proposal-time labels and gaps because those fields are covered by the approved digest. Current lifecycle truth is carried only by the outer envelope and matching approval receipt; changing the payload would require a new baseline version, digest and approval.

F3-A2-D3 records the assignment source, roles, separation and validity policy in protected decision evidence. F3-A2-D4 materializes the first protected `CurrentSetupAssignment` as a resolver-ineligible `DRAFT`. F3-A2-D5 records the Repository Owner's exact-digest approval in a separate protected receipt and adds an `APPROVED` envelope whose assignment payload and digest are unchanged. Repository resolution is eligible only for authorized callers with the separately approved Site Authority and setup baseline. Runtime S09 remains `UNAVAILABLE_CURRENT` until a separately governed adapter exists.
