# Digital StarGate — Current Technical Baseline 24/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-24` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch baseline | `main` |
| Base head before this increment | `50624ba6ac94b83a41647ae7f5f716ea00ec5ce7` |
| Current `main` head before BKL-042 closure / BKL-043 start | `ec17c69cbf350b4952e781525b782128ed293a22` (PR #363) |
| Current package | BKL-043 Observatory Reliability Engineering — F1 repository-only source discovery |
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

## BKL-043 initial source-discovery state

BKL-042 is ACCEPTED / POST-MERGE VERIFIED within its bounded read-only scope by
`docs/project/BKL-042-CLOSURE-2026-09-24.md`. BKL-043 is the dependency-ready
successor. Its initial repository-only inventory is recorded in
`docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md` and finds
no eligible operational population for service availability, correlated incident
rates, MTBF, MTTR or failure budget. Historical session completion fields are
descriptive only; EAGLE is `UNAVAILABLE` / `UNKNOWN`; the archived telemetry is a
synthetic fixture. Per AP-007, numeric SLI/SLO thresholds remain undefined pending
measured baseline and applicable owner/architecture deliberation.

The follow-up population/contract analysis is recorded in
`docs/architecture/validation/BKL-043-F1-POPULATION-AND-CONTRACT-GAP-DISCOVERY-2026-09-24.md`.
It also accounts for the bounded real BKL-030 G6 OAT (one 14-signal manual write
and idempotent replay), which proves pilot persistence mechanics but not continuous
availability. The repository still lacks an authoritative planned-session
denominator, a complete incident lifecycle population, and continuous telemetry
coverage. No new schema, event source, writer cadence, alert, or metric threshold
has been approved.
