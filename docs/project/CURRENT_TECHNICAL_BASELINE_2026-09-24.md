# Digital StarGate — Current Technical Baseline 24/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-24` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch baseline | `main` |
| Base head before this increment | `50624ba6ac94b83a41647ae7f5f716ea00ec5ce7` |
| Current `main` head before owner-acceptance reconciliation | `bdb15037f4a2505992c284a1dff4930af90801f8` (PR #362) |
| Current package | BKL-042 AI Observatory Assistant — F7 accepted within bounded read-only scope |
| Owner / accountable | Massimo Mainini |
| Authority | bounded advisory, repository-governed projections, read-only |

AP-008 and BKL-036-F5 remain closed within the accepted bounded read-only scope.
BKL-034, BKL-034-F2 and BKL-042 are not being reopened for image/runtime writes;
image storage and ingestion authority remain separately gated. The deployed BKL-042
relay now runs method v3 on `dsg-bkl042-ai-relay-00008-qat` with 100% traffic. Both
the service-level and revision-level maximum are 1 instance. Revision
`dsg-bkl042-ai-relay-00007-wrm` is retained as rollback. The portal gateway and its
configuration were not changed.

## BKL-042 state

Owner-witnessed authenticated OAT on method v2 answered the M 27 session query with
five citations, whose factual values were checked against the published historical
catalog. Following the directed source-coverage extension, Massimo supplied the
owner-witnessed OAT v3 results and formally accepted BKL-042/F7 within the bounded
read-only scope and the stated limitations. Acceptance evidence:
`docs/project/BKL-042-F7-BOUNDED-ACCEPTANCE-2026-09-24.md`.

The in-progress F7 method v3 adds BKL-037 historical session-comparison context and
BKL-041 experimental data-quality context. It preserves published source digests and
generation timestamps, limits results per source, and excludes synthetic quality
scores/decompositions. It does not consume fixture-only Digital Twin/archive/image
data, the expired current-night planner projection, unavailable readiness, incomplete
PixInsight provenance, or the current EAGLE snapshot (`UNAVAILABLE` / `UNKNOWN` / no
current snapshot). Evidence: `docs/architecture/validation/BKL-042-F7-F1-SOURCE-COVERAGE-EVIDENCE-2026-09-24.md`.

Local verification: 12 retrieval tests pass; live static-projection replay resolves
the expanded source set. AI-assisted ARB and Release Quality reviews are recorded
against implementation commit `8b89c048`; they are not independent human approvals.
Final-head checks passed on `7d7bc9d2`, PR #360 merged as
`6e6cf43fdf7d29d67d4800541049a4acdf7f42ee`, and all applicable post-merge workflows
passed, including Pages publication. Run IDs and outcomes are recorded in the F7
evidence document. On owner instruction, method v3 was deployed from the existing
relay source to the existing service; the final image digest is recorded in the
deployment evidence. Deployment preflight confirmed Ready, 100% traffic to v3,
service/revision maximum 1 and unauthenticated HTTP 403. Authenticated OAT on v3
was owner-witnessed and accepted with limitations: BKL-037 provides aggregate
historical SQM statistics but no per-session measurements; BKL-041 remains
`EXPERIMENTAL_NOT_ACCEPTED`, synthetic and uncalibrated. No definitive scientific
quality assessment is claimed. Future expansion to excluded evidence classes is
separately gated.

## Non-negotiable boundaries

`command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE`,
`acceptance_authority=HUMAN_ONLY`. No command path, broker, decision scheduler,
automatic remediation, image mutation, processing execution, provider tool execution,
or Safety Authority change is included or authorized.
