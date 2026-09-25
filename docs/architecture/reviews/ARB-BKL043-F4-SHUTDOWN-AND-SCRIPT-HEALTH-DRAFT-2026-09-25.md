# Architecture Review Board — BKL-043 F4 shutdown and production-script drafts

| Field | Value |
|---|---|
| Review ID | `ARB-BKL043-F4-DRAFT-AI-001` |
| Review mode | AI-assisted, owner-authorized under DSG-AEM-001; not independent human approval |
| Date | 2026-09-25 |
| Pull request | [#383](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/383) |
| Technical head reviewed | `58d29c05e3ea44d9a840991306db50b4331f70de` |
| Base | `e69a299036719a85bef6ff2225e157288f06a086` |
| Decision | **APPROVED — preparation-only, with limitations** |

## 1. Scope and independence

This assessment covers the documentation-only BKL-043 F4 preparation package
on the exact head above. The reviewed changes define a proposed local shutdown
evidence contract, offline historical reconciliation plan, owner-selected
all-Digital-StarGate production-script scope, repository-only candidate map,
and their governance dispositions. No implementation, runtime action, source
access, deployment, secret, device, or authority change is part of the package.

Massimo Mainini reported that Leonardo Di Egidio approved the quality of the
updated drafts and repository map at the prior technical head
`854b15f6f50df3c0e2713d1ea3275889aebd5bbc`. This is recorded as owner-reported
human review evidence; it is not a GitHub review record. This AI-assisted ARB is
a separate assessment and is not represented as Leonardo's independent review.

The package was not modified during this assessment.

## 2. Verified repository state

- PR #383 is open and in draft at the reviewed head; its base is current
  `main@e69a299036719a85bef6f1f87b6e4c0b5ec9`.
- The branch contains current `main` by a normal merge and is zero commits
  behind; it has not rewritten history.
- The six applicable technical-head workflows completed successfully: F4-A,
  F4-C, F4-D, F6, documentation validation (no deploy), and Word generation.
- The draft records policy B for local shutdown evidence while keeping planned
  intent, cause, and uncorroborated intervals `UNKNOWN`.
- Windows System events, N.I.N.A. records, and sessions remain candidate inputs
  for a separately authorized offline reconciliation; no real logs were read.
- The all-Digital-StarGate production-script population boundary is owner
  selected. The repository map explicitly does not claim a complete current
  production inventory and distinguishes historical reports, workflow
  configuration, and CI/build activity.
- `command_authority=NONE`, `execution_authority=NONE`, and
  `safety_authority=NONE` remain unchanged.

## 3. Architecture assessment

The package preserves evidence provenance and uncertainty rather than deriving
intent or incident cause from an orderly shutdown marker. It separates host-on
intervals from observatory availability and scientific activity, and does not
claim MTBF/MTTR without a validated event population, semantics, coverage, and
exposure denominator.

The script-health extension correctly treats production inventory and run
evidence as distinct: repository presence is not deployment proof, a workflow
trigger is not proof of a run, a process result does not prove downstream
success, and an absent local result while EAGLE is off is not automatically a
failure. Event-driven and release workflows require their own expected-trigger
semantics; periodic missing-run rules cannot be inferred from them.

No architecture conflict is found with the two-plane BKL-043 design or its
read-only boundary. The all-DSG population scope is explicitly owner selected;
classifying individual workflows and establishing current source authority
remain future design gates rather than implicit approvals in this package.

## 4. Findings

### Blocker

None for the documentation-only preparation scope.

### Major

None for the documentation-only preparation scope.

### Minor / limitations

- `ARB-043-F4-D01` — The current production-script population is not verified.
  Resolve the authoritative inventory source and execution-boundary owners
  before claiming completeness or specifying operational checks.
- `ARB-043-F4-D02` — Event-driven and release workflow inclusion and expected-run
  semantics remain unselected. Keep them out of missed-period classifications
  until their trigger populations are governed.
- `ARB-043-F4-D03` — Exact runtime authorization, security/privacy review,
  witness selection, cost limits, installation, rollback and OAT remain open.
  This decision approves preparation documents only and cannot be used to start
  a runtime pilot or access real data.

These limitations are assigned to the later exact-inventory and exact-runtime
gates; they do not block integration of the bounded preparation documents.

## 5. Technical-head validation evidence

All six applicable workflows passed on reviewed head
`58d29c05e3ea44d9a840991306db50b4331f70de`:

| Workflow | Run | Result |
|---|---:|---|
| BKL-031 F4-A Governance | `36184373614` | SUCCESS |
| BKL-031 F4-C Gate Governance | `36184373619` | SUCCESS |
| BKL-031 F4-D Forecast Projection Governance | `36184373576` | SUCCESS |
| BKL-031 F6 Real-Evidence Setup-Aware E2E Governance | `36184373518` | SUCCESS |
| Validate documentation (no deploy) | `36184373536` | SUCCESS |
| Genera manuale Word | `36184373533` | SUCCESS |

## 6. Boundary and rollback

- No code, runtime, infrastructure, data schema, credential, command path,
  scheduler, remediation, safety interlock or Safety Authority is changed.
- No real EAGLE access, log access/import, workflow dispatch, spend or deployment
  is authorized or claimed.
- Rollback is a repository revert of the documentation commit set; no data
  migration or runtime rollback is involved.

## 7. Decision

**APPROVED — preparation-only, with limitations.** The package may proceed to
the separate Release Quality review. The open findings remain mandatory gates
before any exact runtime authorization or production-inventory completeness
claim.
