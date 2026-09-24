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
| Owner-witnessed v3 OAT | **PENDING** |
| BKL-042 acceptance | **NOT ACCEPTED / PACKAGE OPEN** |

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

No authenticated request, model response, citation result or owner acceptance is
claimed here. Massimo must perform and witness OAT through the existing portal for
both new-source intents: BKL-037 descriptive SQM comparison and BKL-041 experimental
quality context. Verify response `method_version` is v3, BKL-037 is cited as
descriptive only, BKL-041 is labeled `EXPERIMENTAL_NOT_ACCEPTED`, and no synthetic
score/confidence/decomposition is exposed. Record correlation IDs and non-secret
response evidence only. Formal acceptance remains a separate human decision.
