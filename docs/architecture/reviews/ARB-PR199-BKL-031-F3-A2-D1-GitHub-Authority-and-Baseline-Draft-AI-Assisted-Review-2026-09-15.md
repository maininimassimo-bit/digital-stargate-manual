# ARB PR #199 — BKL-031 F3-A2-D1 GitHub Authority and Baseline Draft AI-Assisted Review

| Campo | Valore |
|---|---|
| Review ID | ARB-PR199-BKL031-F3A2-D1 |
| Data | 15/09/2026 |
| Role | Architecture Review Board — process-separated AI-assisted reviewer |
| Independence limitation | Not equivalent to an independent human approval |
| PR | #199 |
| Base | `main@687f966fa544f7c4b31eaa29433cfa8ab48e52fe` |
| Exact technical head | `b595680a0dcc042bc2046e0fdc166ed0d075f97b` |
| Decision | **APPROVED WITH CONDITIONS — 99/100** |
| Scope | ADR-009, protected authority registry, first DRAFT payload, governance continuity |
| Runtime / EAGLE | None |

## 1. Independent review statement

The ARB reviewed repository truth, the PR diff and governing AP-006/F3-A2 contracts after authoring/remediation stopped. The review did not modify the proposal. Owner selections for composite granularity, fixed validity and explicit exceptions are treated as decision evidence, not as approval of the payload digest.

## 2. Verified evidence

- PR #199 is mergeable and `7` commits ahead / `0` behind `main`.
- The diff contains 19 files: architecture/governance documents, generated projections, one knowledge-graph projection update and a protected DRAFT outside `docs/`.
- All seven PR workflows on the exact technical head completed `SUCCESS`:
  - Developer Foundation #1441;
  - Validate documentation #1078;
  - Genera manuale Word #1504;
  - Scientific Platform Governance #141;
  - BKL-041 F4 Governance #143;
  - BKL-046 F4 Governance #117;
  - BKL-046 F5 Governance #102.
- Build, 64 .NET tests, formatting, MkDocs, knowledge-graph coverage/material relations and governed projection checks passed inside Developer Foundation.
- The payload digest was recomputed independently from recursively key-sorted compact UTF-8 JSON and matches `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`.
- Repository visibility is private; `mkdocs.yml` uses `docs_dir: docs`, so `governance/setup-authority/` is not a Pages input.
- No new credential, provider, runtime path, device command or physical activity is present.

## 3. Score

| Dimensione | Score | Evidence |
|---|---:|---|
| Architecture/ADR consistency | 99 | ADR-009 specializes AP-006 and F3-A2 without changing their fail-closed boundary |
| Authority and lifecycle integrity | 99 | human Approval Authority and custodian are distinct; DRAFT is ineligible |
| Data semantics and provenance | 98 | projection lineage retained; missing values explicit; no observed-state promotion |
| Security and privacy | 100 | private repository, protected classification, outside Pages, no secrets/coordinates/serials |
| Safety boundary | 100 | no command, readiness, go/no-go or Safety Authority |
| Operability, migration and rollback | 98 | Git-history rollback; activation/retirement future path explicit |
| Traceability and documentation | 99 | ADR, contract, assessment, backlog, roadmap, knowledge graph, nav and continuity aligned |
| Verification evidence | 98 | 7/7 exact-head workflows and independent digest recomputation; schema/OAT correctly not executed |

Weighted outcome: **99/100**.

## 4. Findings

No Blocker or Major finding.

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| ARB-199-MI01 | Minor | The candidate has no human approval receipt and cannot be an approved baseline. | Assigned to the immediate exact-digest owner gate; non-blocking for DRAFT integration, blocking for lifecycle promotion or resolver use. |
| ARB-199-MI02 | Minor | No approved schema/validator/canonicalizer implementation exists. | Assigned to F3-B materialization gate; non-blocking for this documentation/DRAFT package. |
| ARB-199-MI03 | Minor | No concrete F3-A1 site record or separately approved `CurrentSetupAssignment` exists. | Assigned before S09 activation; S09 must remain `UNAVAILABLE_CURRENT`. |
| ARB-199-OB01 | Observation | Projection-sourced facts become desired authority only through later exact human approval. | ADR-009 and the DRAFT envelope preserve this distinction. |

## 5. Conditions

1. PR #199 may merge only as an authority decision plus protected DRAFT.
2. The Repository Owner must explicitly approve or correct the exact payload digest and validity before any `APPROVED` transition.
3. Baseline approval must not create or imply assignment approval.
4. S09 remains `UNAVAILABLE_CURRENT` until F3-A1 site authority and an independently approved assignment exist.
5. Schema, validator, adapter, persistence, public read model and OAT remain separate future gates.
6. The publication head, including this review, must complete all applicable workflows before merge.

## 6. Decision

**APPROVED WITH CONDITIONS — 99/100.**

The proposal is consistent, traceable, reversible and fail-closed for DRAFT integration. ARB-199-MI01 through MI03 are explicitly assigned future gates and do not block this PR; they block approval/materialization/activation as stated.
