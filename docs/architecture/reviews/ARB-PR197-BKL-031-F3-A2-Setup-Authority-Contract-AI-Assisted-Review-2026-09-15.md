# Architecture Review Board — PR #197 BKL-031 F3-A2 Setup Authority Contract

| Field | Value |
|---|---|
| Review ID | ARB-PR197-BKL-031-F3-A2-AI-001 |
| Review mode | AI-assisted, owner-authorized; process-separated from authorship; not an independent human approval |
| Date | 2026-09-15 |
| Pull request | [#197](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/197) |
| Technical head reviewed | `6de6ac21acc6f310b022df20954fd0389bd275d1` |
| Base | `357a5edfbd39346b10a1a2d751018ff6d1dd208f` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **97 / 100** |

## 1. Independence disclosure

This assessment is an AI-assisted ARB review authorized by `DSG-AEM-001`. Review judgment was performed after authorship stopped and no package file was modified during the assessment. It is not equivalent to an independent human approval.

## 2. Verified repository truth

- PR #197 is open, draft, mergeable and not merged;
- technical head is three commits ahead and zero behind `main@357a5edfbd39346b10a1a2d751018ff6d1dd208f`;
- scope is 13 documentation/governance files, +610/-81;
- technical-head workflows are 7/7 SUCCESS;
- the package is explicitly source-neutral and does not assert a concrete approved setup baseline or current assignment;
- no schema, validator, fixture, adapter, provider, runtime, EAGLE activity, ranking, readiness, command path or Safety Authority change exists;
- generated roadmap and scientific-platform status projections are synchronized.

## 3. Architecture assessment

The contract establishes the missing semantic boundary between four distinct authorities: AP-006 architecture governance, a concrete approved configuration-baseline instance, the time-bounded `CurrentSetupAssignment`, and observed or historical evidence. AP-006 is correctly treated as architectural authority and never as proof that a deployable baseline exists.

Ownership and approval responsibilities are expressed as required logical references for the baseline and assignment lifecycles. Baseline approval and setup-assignment approval remain separate. The source-neutral ports preserve hexagonal boundaries and prevent file layout, modification time, N.I.N.A./EAGLE state or historical observations from becoming implicit authority.

Temporal semantics reuse the F3-A1 half-open UTC validity model. Resolution is deterministic and fail-closed for absence, overlap, ambiguity, digest mismatch, invalid approval or authority failure. The protected/public namespace split is deny-by-default. The added `publicReasonCode` boundary prevents internal baseline or assignment details from leaking into public projections without an explicit allowlisted mapping.

The package is safe to accept as a detailed documentation contract. It is not sufficient to start schema or adapter materialization because the repository still does not identify a concrete authority owner, approval source or approved baseline instance.

## 4. Scoring matrix

| Dimension | Score | Assessment |
|---|---:|---|
| Program alignment | 99 | follows the accepted F3-A2 dependency and scope |
| Domain integrity | 98 | separates governance, baseline, assignment and observed evidence |
| Layering and ports | 98 | source-neutral application/outbound boundaries |
| Temporal semantics | 99 | reuses approved half-open UTC rules |
| Determinism/fail-closed behavior | 99 | no latest-wins or environmental inference |
| Security and privacy | 98 | protected details and internal reasons excluded from public projection |
| Safety | 100 | no command, interlock or Safety Authority impact |
| Operability/auditability | 97 | append-only lifecycle, digests and approval evidence defined |
| Migration/rollback | 97 | no migration; future materialization and rollback bounded |
| Validation readiness | 95 | strong plan, but executable schema/runtime tests are intentionally not implemented |

Conservative rounded score: **97 / 100**.

## 5. Findings

### Blocker

None.

### Major

None.

### Minor

- `ARB-197-MI01` — Before any F3-B schema, fixture, validator, adapter or real assignment is materialized, the repository must identify the concrete Configuration Baseline Authority, Assignment Authority, approval evidence source and first approved baseline instance. Until then S09 remains `UNAVAILABLE_CURRENT`.

### Observations

- `ARB-197-O01` — `ARB-195-MI01` is closed at the normative contract level: the authority boundary and required roles are now explicit. Its unresolved real-world instantiation is carried as `ARB-197-MI01`.
- `ARB-197-O02` — AP-006 remains an architecture/governance source; it cannot be used as evidence of a current deployable setup.
- `ARB-197-O03` — Independent human review and executable schema/runtime validation were not performed.
- `ARB-197-O04` — Fresh CI is required after publication of this review and the paired Release Quality report.

## 6. Validation evidence

| Workflow | Run | Result |
|---|---:|---|
| Developer Foundation #1430 | 34960854627 | SUCCESS |
| Validate documentation #1067 | 34960854587 | SUCCESS |
| Genera manuale Word #1493 | 34960854836 | SUCCESS |
| Scientific Platform Governance #130 | 34960854619 | SUCCESS |
| BKL-041 F4 Governance #132 | 34960854620 | SUCCESS |
| BKL-046 F4 governance #106 | 34960854615 | SUCCESS |
| BKL-046 F5 governance #91 | 34960854592 | SUCCESS |

Not executed or claimed: F3-A2 schema/fixture/validator tests, real baseline or assignment approval, provider evaluation, device activity, OAT, scientific threshold approval, independent human review, merge or post-merge publication.

## 7. Decision and conditions

**APPROVED WITH CONDITIONS — 97/100.**

The documentation contract may proceed to merge after review-publication exact-head CI and the substitute merge controls of `DSG-AEM-001` / `W-DSG-AEM-RULESET-001`.

`ARB-197-MI01` is a mandatory predecessor to materialization and F3-B acceptance, not a blocker to merging this source-neutral contract.
