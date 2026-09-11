# ARB — BKL-046 F1 Independent Architecture Review

| Campo | Valore |
|---|---|
| Package | BKL-046 F1 — Source Discovery and Advisory Semantic Contract |
| Review date | 11/09/2026 |
| Repository baseline | PR #165 exact head `1ee04f401f98b96fe2bc5555df9d0b8f34c17212` |
| Review role | Independent Architecture Review Board |
| Decision | **APPROVED** |
| Score | **99/100** |
| Blocker / Major / Minor | **0 / 0 / 0** |

## 1. Review scope and evidence

The review evaluated the proposal against repository truth and the accepted BKL-015, BKL-044, BKL-045, ADR-008, AP-013/AP-014 and BKL-041 boundaries. It also verified the canonical roadmap/projections, continuity documents, MkDocs navigation and the seven successful workflows associated with the exact reviewed head.

This approval applies to the F1 architecture/documentation increment only. It does not approve an AI runtime, model/provider, retrieval technology, recommendation-quality claim, external data transfer, PixInsight apply path or production capability.

## 2. Dimension scoring

| Dimension | Score | Evidence and assessment |
|---|---:|---|
| Existing architecture and ADR consistency | 100 | Reuses BKL-044 semantics and ADR-008/BKL-045 provenance rather than creating parallel authority. |
| Domain and dependency integrity | 100 | Downstream-only references preserve AP-013 asset authority and AP-014/AP14-W06 reconciliation. |
| Semantic and authority contract | 99 | Recommendation, rationale, user decision and execution evidence are explicitly separated; machine-readable closure is correctly deferred to F2. |
| Safety | 100 | No device command, observatory dependency, interlock bypass, automatic acceptance, unattended remediation or Safety Authority. |
| Security and privacy | 98 | Local-first and no-transfer boundary is explicit; provider-specific threat modelling is correctly an open future decision. |
| Operability and observability | 96 | Required audit fields and failure isolation are defined; runtime SLI/SLO and placement are correctly not invented in F1. |
| Migration and rollback | 100 | Documentation-only additive adoption with repository-revert rollback; later increments have explicit entry/exit ordering. |
| Traceability and documentation | 100 | Program assessment, roadmap authority/projections, continuity, backlog, knowledge map, project index and MkDocs navigation align. |
| Validation evidence | 100 | All seven exact-head workflows succeeded, including Developer Foundation, documentation/MkDocs, Scientific Platform and BKL-045 governance. |
| Release impact and limitation integrity | 99 | Release remains unassigned; BKL-045 `UNAVAILABLE` and BKL-041 non-production limitations are preserved without overclaim. |

Overall score: **99/100**.

## 3. Architecture findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observations

- `ARB-BKL046-F1-O01` — F2 must close the machine-readable recommendation envelope and Human Decision Receipt with negative tests; this is planned scope, not an F1 defect.
- `ARB-BKL046-F1-O02` — confidence calibration, evaluation dataset, provider/runtime placement and recommendation-quality SLI/SLO remain undecided and must not be inferred from the F1 maturity scores.
- `ARB-BKL046-F1-O03` — any future external inference or `ASSISTED APPLY` path requires a new architecture/security review and cannot inherit this approval.

## 4. Independent checks

| Check | Result |
|---|---|
| Dependency readiness | PASS — BKL-015/BKL-044/BKL-045 accepted |
| Provenance limitation preservation | PASS — `UNAVAILABLE/PARTIAL` remain first-class and fail-closed |
| BKL-041 authority isolation | PASS — experimental context only, never ground truth or production signal |
| Duplicate contract/ingestion authority | PASS — none introduced |
| Human decision versus execution | PASS — separate receipt/evidence boundaries |
| Security/privacy expansion | NONE — no provider, upload or third-party transfer authorized |
| Runtime/operational change | NONE |
| Rollback | PASS — repository revert |
| Canonical/projection consistency | PASS — governed sync produced both projections |
| Exact-head CI | PASS — 7/7 workflows successful |

## 5. Decision

**APPROVED.** BKL-046 F1 is architecturally coherent and may proceed to Release Quality review on the exact reviewed head plus this review-evidence commit.

No waiver is granted and no open observation is a closure blocker. F1 must remain `Proposed` until Release Quality, protected merge and post-merge verification are complete.

## 6. Re-review triggers

ARB re-review is mandatory if the PR introduces any model/provider selection, image or metadata transfer outside the local boundary, executable PixInsight action, autonomous acceptance/remediation, new persistence/ingestion authority, weakened missingness behavior, or a change to observatory Safety Authority.
