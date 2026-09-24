# BKL-042 F7 — Method v3 Existing-Relay Deployment Evidence

| Field | Value |
|---|---|
| Evidence ID | `BKL042-F7-V3-DEPLOYMENT-2026-09-24` |
| Owner authorization | Massimo Mainini explicitly selected restoration of the documented one-instance cap during method v3 deployment |
| Project / region | `digital-stargate-telemetry` / `europe-west1` |
| Existing service | `dsg-bkl042-ai-relay` |
| New revision | `dsg-bkl042-ai-relay-00008-qat` |
| Previous / rollback revision | `dsg-bkl042-ai-relay-00007-wrm` |
| Method | `bkl042-static-projection-retrieval-v3` |
| Runtime image | `europe-west1-docker.pkg.dev/digital-stargate-telemetry/cloud-run-source-deploy/dsg-bkl042-ai-relay@sha256:625a5df4ae211b0b2d45dbb814066a67d0b11be823058f90e352de988cee77f7` |
| Cloud Build ID | `8a9eb24c-98da-4e2d-8d2a-26e4deff564d` |
| Cloud Run operation ID | `3b0f3e2e-96da-43d5-9c96-37295103cb6c` |
| Owner-witnessed v3 OAT | **PASS WITH ACCEPTED LIMITATIONS — 2026-09-24** |
| BKL-042-F7 acceptance | **ACCEPTED / BOUNDED READ-ONLY SCOPE** |

## Scope and source

The owner authorized deploying method v3 to the existing private AI relay and
restoring the documented maximum of one instance. The relay is separate from the
observability telemetry relay. No new Cloud Run service, portal-gateway deployment,
provider/model selection, credential, runtime data source or authority was added.

The build context was `infrastructure/bkl042-ai-relay` from a checkout whose source
files were byte-identical to the merged `main` implementation in PR #360. The source
defines retrieval method v3. Relevant source blob IDs at the verified main baseline
were: Dockerfile `d05499c6ab9e729bce04a433c6a194ce9bb8952b`, app
`b7baf818727087c6fb6828991c65f31105951f6e`, retrieval
`8c73d56727706a8980707c0509d556de7d490298`.

## Deployment sequence

1. Read-only preflight confirmed service `dsg-bkl042-ai-relay`, region
   `europe-west1`, previous revision `00007-wrm` at 100% traffic, and the existing
   Secret Manager reference name/version. Secret material was not read.
2. Local relay suite passed: 12/12 tests.
3. Built and deployed the source to the existing service without traffic, assigning
   tag `bkl042-f7-oat`; set service maximum (`--max=1`) and new revision maximum
   (`--max-instances=1`).
4. Before routing, Cloud Run reported the new revision Ready, the service-level
   maximum annotation as `1`, revision-level `autoscaling.knative.dev/maxScale=1`,
   unchanged CPU/memory limits (1 vCPU / 512 MiB), unchanged service identity and
   unchanged Secret Manager reference. The tagged endpoint rejected unauthenticated
   `/health` with HTTP 403.
5. Routed 100% of relay traffic to revision `00008-qat` so the existing authenticated
   portal gateway can exercise v3 for the owner-witnessed OAT.
6. Post-deployment read-only verification confirmed latest-ready revision `00008-qat`,
   100% traffic to that revision, service-level max `1`, revision-level max `1`,
   revision Ready, and canonical unauthenticated `/health` HTTP 403.

The portal gateway remains unchanged at its existing revision. No provider request
was intentionally generated as part of this deployment. An authenticated health
probe was not performed by the agent; only the owner-witnessed portal OAT can
establish authenticated v3 behavior and source citations.

## Rollback

If the owner OAT or live validation fails, route traffic back to
`dsg-bkl042-ai-relay-00007-wrm` using the Cloud Run traffic update for the existing
service. Preserve the service-level maximum of one instance. The old revision is
retained; do not delete it. Verify the restored traffic assignment and readiness.

## Boundaries and remaining gate

The runtime remains advisory and bounded read-only:

- `command_authority=NONE`;
- `execution_authority=NONE`;
- `safety_authority=NONE`;
- tools disabled and runtime event publication false;
- no storage/upload, processing, command, broker, scheduler, automatic remediation
  or Safety Authority change.

## Owner-witnessed OAT and acceptance

Massimo performed and supplied the authenticated portal OAT results on 2026-09-24.
Both responses identify `bkl042-static-projection-retrieval-v3` and include the
expected governed projection and source digest:

| Intent | OAT evidence | Outcome and accepted limitation |
|---|---|---|
| BKL-037 SQM comparison | `bkl042-pages-7597330b-5970-4696-b7a6-767defa6e8ff`; citation `session-comparison`; digest `b1d1e516eb872e686ce18178858f42eb85c690de2ce011d845a7f2436c0717d4` | Bounded descriptive retrieval passed. Available evidence is aggregate (15 sessions; min 18.66, max 20.96, median 20.57 mag/arcsec²), not per-session SQM. The answer explicitly reports that limitation and does not present a quality score. |
| BKL-041 M 27 quality context | `bkl042-pages-4971ae55-44cf-47e0-afc5-ecca6e774442`; citation `scientific-data-quality`; digest `7c4ffc905f2a57b18f221ffabf4e58820ad03549968db2e2aec78d2b88846838` | Bounded experimental-context retrieval passed. Both cited records are `EXPERIMENTAL_NOT_ACCEPTED`, synthetic and uncalibrated; no definitive quality grade is claimed. |

The owner explicitly confirmed formal acceptance of BKL-042/F7 within the bounded
read-only scope and accepted the limitations reported above. The acceptance record
is `docs/project/BKL-042-F7-BOUNDED-ACCEPTANCE-2026-09-24.md`. This does not accept
or promote excluded source classes or authorize any additional runtime authority.
