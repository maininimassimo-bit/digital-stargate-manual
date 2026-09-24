# Digital StarGate — Current Technical Baseline 24/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-24` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch baseline | `main` |
| Base head before this increment | `50624ba6ac94b83a41647ae7f5f716ea00ec5ce7` |
| Current `main` head | `6e6cf43fdf7d29d67d4800541049a4acdf7f42ee` (PR #360) |
| Current package | BKL-042 AI Observatory Assistant — F7 source coverage in progress |
| Owner / accountable | Massimo Mainini |
| Authority | bounded advisory, repository-governed projections, read-only |

AP-008 and BKL-036-F5 remain closed within the accepted bounded read-only scope.
BKL-034, BKL-034-F2 and BKL-042 are not being reopened for image/runtime writes;
image storage and ingestion authority remain separately gated. The deployed BKL-042
v2 runtime remains the last published relay version. The v3 retrieval change is
merged and post-merge verified; deployment to the existing relay is the next
separate gate solely to enable the owner-witnessed v3 OAT. No new service or traffic
promotion is in scope.

## BKL-042 state

Owner-witnessed authenticated OAT on method v2 answered the M 27 session query with
five citations, whose factual values were checked against the published historical
catalog. The owner explicitly directed that BKL-042 not be closed until coverage of
other eligible F1 sources is extended.

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
evidence document. F7 and BKL-042 remain open pending deployment to the existing
relay solely for OAT, owner-witnessed authenticated OAT on method v3, and formal
human acceptance.

## Non-negotiable boundaries

`command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE`,
`acceptance_authority=HUMAN_ONLY`. No command path, broker, decision scheduler,
automatic remediation, image mutation, processing execution, provider tool execution,
or Safety Authority change is included or authorized.
