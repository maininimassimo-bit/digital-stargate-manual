# BKL-031 F3-A2-D5 — CurrentSetupAssignment Approval and Promotion

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A2-D5-SA-001 |
| Status | **ACCEPTED / POST-MERGE VERIFIED** |
| Version | 1.1 |
| Date | 15/09/2026 |
| Governing ADR | ADR-009 |
| Predecessor | F3-A2-D4 accepted/post-merge verified |
| Exact publication head | `6947e79a53282db2a7f6d879643e51840ed9e553` |
| Merge | `bc4307c2042a45985622044e11631421de5b2c3d` |
| Runtime impact | None |

## Purpose

Record the Repository Owner's explicit approval of the exact protected assignment payload and promote a separate lifecycle envelope from `DRAFT` to `APPROVED` without changing the payload or its canonical digest.

## Current and target state

| Concern | Before D5 | D5 target |
|---|---|---|
| Historical assignment envelope | protected `DRAFT` | retained unchanged |
| Approval evidence | absent | separate protected immutable receipt |
| Current lifecycle envelope | absent | protected `APPROVED` envelope |
| Payload and digest | validated D4 payload | byte-semantic payload and digest unchanged |
| Repository resolver | `UNAVAILABLE_CURRENT` for DRAFT-only input | `AVAILABLE` for authorized caller with all approved sources |
| Runtime S09 | `UNAVAILABLE_CURRENT` | unchanged; no adapter exists |

## Architecture rules

1. The approval receipt is a closed, versioned protected record outside `docs/`.
2. The receipt binds assignment identity, revision, validity, exact digest, approving authority and repository evidence.
3. Repository Owner is the human Approval Authority; the Architecture Office remains a non-approving custodian.
4. Only lifecycle metadata changes in the new envelope. The historical DRAFT, assignment payload and canonical digest remain unchanged.
5. Promotion fails closed on payload mutation, authority mismatch, validity mismatch, receipt mismatch or missing source authority.
6. Resolver eligibility is limited to authorized repository consumers and still requires the approved Site Authority and approved setup baseline.
7. Public output remains deny-by-default and cannot expose protected identifiers, locators, digests or exact site facts.
8. Approval does not create a runtime adapter and does not authorize EAGLE, device, readiness, go/no-go or Safety Authority behavior.

## Components

| Component | Responsibility |
|---|---|
| approval receipt schema | closed receipt contract |
| protected receipt | immutable human-decision evidence |
| APPROVED envelope | lifecycle projection over the unchanged payload |
| assignment validator | receipt, promotion, authority and resolver gates |
| executable suite | positive, negative, privacy, mutation and property evidence |
| governance workflow | redacted repository-authoritative execution |

## Failure and rollback

Any integrity or binding failure rejects promotion and resolution. Rollback is a reviewed Git revert of the APPROVED envelope and receipt while retaining the historical DRAFT. Because no runtime adapter is introduced, there is no operational rollback.

## Security, privacy and safety

The exact digest and protected authority details are intentionally omitted from public documentation and workflow logs. Coordinates, elevation and exact address remain unpublished. Local physical interlocks and Safety Authority are unaffected.

## Acceptance criteria

- explicit digest-bound human authorization is represented by a protected receipt;
- receipt schema and validator key sets are closed and aligned;
- approved and draft assignment payloads canonicalize identically;
- protected digest is unchanged;
- authorized repository resolution is `AVAILABLE` only with all approved sources;
- DRAFT remains ineligible;
- 65/65 executable cases pass;
- public protected-literal scan passes;
- exact-head CI, AI-assisted process-separated reviews and post-merge verification complete.

## Acceptance reconciliation

PR #209 completed 5/5 exact-head workflows and 7/7 post-merge workflows. Documentation governance recorded `ACCEPTED WITH OBSERVATION`; the AI-assisted, process-separated ARB recorded `APPROVED WITH CONDITIONS — 99/100`; Release Quality recorded `CONDITIONALLY READY FOR MERGE`. These reviews are not equivalent to independent human approval. No Blocker or Major remains open.

The accepted state is repository authority `APPROVED/AVAILABLE` for authorized validated input. Runtime S09 remains `UNAVAILABLE_CURRENT`; no adapter, EAGLE operation, readiness/go-no-go, device command or Safety Authority change is introduced.
