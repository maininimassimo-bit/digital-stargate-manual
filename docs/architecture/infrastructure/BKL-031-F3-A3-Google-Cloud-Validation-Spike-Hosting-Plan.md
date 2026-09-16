# BKL-031 F3-A3 — Google Cloud Validation-Spike Hosting Plan

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A3-INFRA-001 |
| Status | **PROPOSED / REPOSITORY SCAFFOLDING ONLY — BOOTSTRAP NOT EXECUTED** |
| Version | 1.0 |
| Date | 2026-09-15 |
| Baseline | `main@527b298094b07e5a00317e60cab3abefed7a5759` |
| Region | `europe-west8` |
| Runtime | Google Cloud Run Job |
| Safety impact | None |

## Purpose

Provide an isolated, low-idle-cost execution boundary for the future F3-A3 validation spike while preserving repository governance, site privacy and the separation from EAGLE, N.I.N.A. and every observatory control path.

## Topology

| Component | Role | Boundary |
|---|---|---|
| GitHub Actions | static validation now; future authenticated plan after bootstrap | OIDC only; no service-account key |
| Workload Identity Pool | trusts only this repository and `refs/heads/main` | one deployer service account |
| bootstrap Terraform | APIs, deployer/runtime identities and three private buckets | one-time administrator action |
| platform Terraform | Artifact Registry, private VPC/subnet and Cloud Run Job | no apply in this package |
| data bucket | read-only kernel/IERS input for runtime identity | no public access |
| evidence bucket | create-only spike evidence from runtime identity | versioned, no public access |
| state bucket | Terraform state for later authenticated runs | versioned, deployer-only |
| Cloud Run Job | one bounded validation task | no EAGLE/N.I.N.A./cupola access |
| private VPC without NAT | route all job traffic; allow Private Google Access | blocks public internet egress |

## Resource profile

- region: `europe-west8`;
- CPU: 2 vCPU;
- memory: 2 GiB;
- task count: 1;
- parallelism: 1;
- task timeout: 120 seconds;
- retries: 0;
- immutable image reference ending in `@sha256:<64 hex>`;
- deletion protection enabled;
- no public IAM principals;
- execution allowed only to the dedicated deployer identity.

## Identity and trust

The bootstrap module creates separate deployer and runtime service accounts. GitHub can impersonate only the deployer service account and only when the OIDC token states both:

- repository `maininimassimo-bit/digital-stargate-manual`;
- ref `refs/heads/main`.

The runtime identity can read the scientific-data bucket and create evidence objects. It cannot administer infrastructure, invoke observatory systems or read the N.I.N.A. plugin’s resources.

## Network and privacy

The local validation profile routes all Cloud Run egress through a dedicated VPC/subnet with Private Google Access and no Cloud NAT. This makes the no-external-provider rule an infrastructure control, not only an application convention.

Horizons validation, if later authorized, requires a separate reviewed network profile. It cannot be silently enabled in this job.

No exact site coordinate, elevation, address, locator, protected digest or correlatable identifier appears in Terraform, variables, labels, logs or evidence paths.

## Cost posture

There is no continuously running VM. Cost is primarily:

- Cloud Run compute while a job executes;
- small Cloud Storage and Artifact Registry footprints;
- logging and any retained evidence;
- no Cloud NAT in the local profile.

Budgets and billing alerts remain project-level operator controls because this repository does not know the billing account. The job remains single-task and zero-retry to avoid accidental multiplication.

## Bootstrap and autonomy sequence

1. select an existing or new GCP project and confirm billing;
2. choose globally unique state/data/evidence bucket names;
3. run the bootstrap Terraform once with an authorized GCP administrator identity;
4. record WIF provider, deployer account and bucket outputs as GitHub repository variables;
5. use the approved F3-OD05 identity and prepare the remaining exact container, IERS and immutable method-profile digests;
6. introduce a separately reviewed authenticated plan/apply workflow;
7. apply platform resources through WIF;
8. execute the spike only after ADR/ARB/Release Quality authorization.

There is no native Google Cloud connector in the available ChatGPT plugin catalog. After the one-time bootstrap, repository changes and GitHub Actions WIF are the governed automation path and avoid reusable cloud keys.

## Failure and rollback

| Failure | Required response |
|---|---|
| OIDC repository/ref mismatch | deny impersonation |
| missing project/bucket variables | Terraform validation or plan fails |
| image is not digest-pinned | variable validation fails |
| SPK/IERS digest placeholder | plan/apply gate fails |
| public IAM principal | static policy workflow fails |
| public egress required | create a separate reviewed profile; do not add NAT here |
| job timeout or failure | no retry; evidence remains incomplete |
| rollback | destroy later-created platform resources through a reviewed change; retain governed audit evidence |

## Current evidence

Terraform source and static checks are prepared. GCP authentication, init against remote state, plan, apply, image push, artifact upload and job execution are all `NOT EXECUTED`.
