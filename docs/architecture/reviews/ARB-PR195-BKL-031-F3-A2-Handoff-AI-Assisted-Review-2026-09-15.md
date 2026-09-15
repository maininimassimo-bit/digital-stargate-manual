# Architecture Review Board — PR #195 BKL-031 F3-A2 Setup Authority Handoff

| Field | Value |
|---|---|
| Review ID | ARB-PR195-BKL031-F3A2-HANDOFF-AI-001 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-15 |
| Pull request | [#195](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/195) |
| Technical head reviewed | `047ca2d1f208d8291d88823f4b99c401232ecd6b` |
| Base | `1fd771632239cdca38d7527c55b974d805ffd1b9` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **98 / 100** |

## 1. Independence and authorization disclosure

This assessment was produced by an AI acting in the Architecture Review Board role after explicit owner authorization for PR #195 and exact head `047ca2d1f208d8291d88823f4b99c401232ecd6b`. It is not equivalent to an independent human approval.

The same AI context assisted preparation of the handoff package. Independence is process separation only, not human or organizational independence. The package was not changed during assessment. Publication of this report does not authorize merge, detailed F3-A2 design, materialization, schema, fixtures, a real assignment, provider selection, runtime, EAGLE activity or Safety Authority.

## 2. Verified repository truth

- PR #195 is open, draft, mergeable and not merged;
- the reviewed branch is two commits ahead and zero behind `main@1fd771632239cdca38d7527c55b974d805ffd1b9`;
- scope is 14 files, +299/-109;
- the second commit is the governed projection synchronization;
- technical-head workflows are 7/7 SUCCESS;
- generated roadmap and scientific-platform status projections are present on the exact head;
- no GitHub review submissions or review threads existed before this assessment;
- repository ruleset collection is empty;
- basic `main` metadata reports `protected=false` and `protection.enabled=false`; the detailed protection endpoint is inaccessible to the integration (HTTP 403);
- no executable, dependency, credential, real setup assignment, deployment or runtime change exists.

## 3. Architecture assessment

The package correctly selects F3-A2 as the next dependency-ready, documentation-only handoff after F3-A1 acceptance reconciliation. It delegates detailed `CurrentSetupAssignment` design to the Solution Architect and preserves the source-neutral F3 architecture: stable assignment identity, AP-006-compatible configuration/baseline references, explicit lifecycle and approval evidence, UTC half-open validity, deterministic fail-closed resolution, protected/public separation, validation, migration and rollback.

The proposal correctly rejects latest-history inference, derived configuration summary authority and host/EAGLE fallback. S09 remains `UNAVAILABLE_CURRENT`; F3-A3/B/C, forecast, ranking, readiness and device control remain unpromoted and unauthorized. Local physical interlocks remain the only Safety Authority.

One clarification is required before detailed contract design. AP-006 is the architecture authority for configuration and approved-baseline concepts, but that authority does not itself prove that a concrete approved desired baseline instance or active setup assignment exists. The future contract must make that distinction executable and traceable.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 99 | F3-A2 is sequenced after accepted F3-A1 without closing BKL-031 |
| Dependency ordering | 98 | F3-A3/B/C remain blocked and no successor is promoted |
| Authority semantics | 95 | AP-006 architecture authority is identified; concrete approved baseline-instance authority needs clarification |
| Domain and layer preservation | 99 | source-neutral ports/adapters and planner/read-model boundaries remain intact |
| Specialist handoff completeness | 98 | expected contract, lifecycle, failure, validation and rollback outputs are bounded |
| Security and privacy | 98 | public/protected boundary is carried; executable enforcement remains a later gate |
| Safety | 100 | no readiness, command, remediation or Safety Authority is introduced |
| Operability and failure semantics | 98 | fail-closed cases are explicit; no runtime is claimed |
| Migration and rollback | 99 | materialization and retirement/rollback are future, controlled increments |
| Traceability and exact-head evidence | 99 | accepted predecessors, carried findings, immutable head and 7/7 CI are recorded |

Conservative rounded ARB score: **98 / 100**.

## 5. Findings

### Blocker

None.

### Major

None.

### Minor

#### ARB-195-MI01 — AP-006 architecture authority versus concrete approved baseline

Before the detailed F3-A2 contract is approved, it must:

1. distinguish AP-006 architectural governance authority from a concrete, approved desired-baseline instance;
2. identify the canonical owner/custodian and source for `configurationId` and `baselineId`;
3. require verifiable approval, revision and validity evidence for the referenced baseline;
4. define fail-closed outcomes for missing, unapproved, ambiguous, superseded or mismatched baselines;
5. preserve S09 as `UNAVAILABLE_CURRENT` until a separately authorized active assignment is materialized and resolved.

This finding does not block integration of the documentation-only handoff.

### Observations

- `ARB-195-O01` — Detailed lifecycle vocabulary and resolver contract are intentionally deferred to the Solution Architect.
- `ARB-195-O02` — The review-publication head requires fresh exact-head CI before merge consideration.
- `ARB-195-O03` — Independent human review was not executed.
- `ARB-195-O04` — Ruleset absence remains a merge-governance issue, not an architecture acceptance waiver.

## 6. Carried-condition disposition

| Condition | Disposition on reviewed head |
|---|---|
| `ARB-195-MI01` | **OPEN / NEW** — mandatory before approval of the detailed F3-A2 contract |
| `ARB-193-MI01` | **OPEN / CARRIED** — elevation semantics mandatory before F3-B |
| `ARB-193-MI02` | **OPEN / CARRIED** — canonical site resolver identity/scope mandatory before F3-B |
| `ARB-191-MI01` | **OPEN / CARRIED** — public/internal enforcement and leak tests mandatory before F3-B/F3-C |
| `ARB-191-MI02` | **NORMATIVE DESIGN SATISFIED / EXECUTABLE GATE OPEN** — interval boundary, adjacency, overlap and unbounded tests mandatory before materialization |

No unexecuted validation and no concrete baseline or assignment are approved as existing.

## 7. Validation evidence

| Workflow | Run ID | Result |
|---|---:|---|
| Developer Foundation | 34954495134 | SUCCESS |
| Validate documentation | 34954495126 | SUCCESS |
| Genera manuale Word | 34954495238 | SUCCESS |
| Scientific Platform Governance | 34954495149 | SUCCESS |
| BKL-041 F4 Governance | 34954495113 | SUCCESS |
| BKL-046 F4 governance | 34954495022 | SUCCESS |
| BKL-046 F5 governance | 34954495179 | SUCCESS |

Not executed or claimed: detailed F3-A2 contract validation, schema/fixture validation, privacy leak tests, runtime/OAT, real baseline or assignment approval, scientific accuracy, PC/EAGLE activity, independent human review, merge or post-merge publication of PR #195.

## 8. Decision and conditions

**APPROVED WITH CONDITIONS — 98/100.**

The documentation-only Program Assessment/Handoff may proceed to merge consideration after:

1. publication of this report and the paired Release Quality report;
2. successful exact-head CI on the review-publication head;
3. confirmation that the branch remains zero behind current `main`;
4. separate owner authorization for merge and explicit treatment of the absent ruleset.

`ARB-195-MI01` is mandatory before approval of the future detailed F3-A2 contract, not before integration of this handoff. No implementation or operational readiness is asserted.
