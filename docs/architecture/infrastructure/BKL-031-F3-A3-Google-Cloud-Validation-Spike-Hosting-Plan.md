# BKL-031 F3-A3 — Google Cloud Validation-Spike Hosting Plan

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A3-INFRA-001 |
| Status | **PROPOSED — EXACT FOUR-RESOURCE PLATFORM APPLIED / ZERO DRIFT / JOB NOT EXECUTED** |
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
| GitHub Actions | static validation and manual exact-head authenticated plan | OIDC only; no service-account key |
| Workload Identity Pool | trusts only this repository and `refs/heads/main` | one deployer service account |
| bootstrap Terraform | APIs, deployer/runtime identities and three private buckets | one-time administrator action |
| registry Terraform | one Artifact Registry Docker repository in dedicated state | exact saved-plan apply only after separate review |
| platform Terraform | private VPC/subnet and Cloud Run Job | exact saved plan applied; zero-drift state evidence recorded |
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

1. the authorized GCP project, private buckets, WIF trust and service identities were created through the reviewed bootstrap;
2. bootstrap state was migrated to protected GCS and its permanent backend was post-promotion verified;
3. the approved F3-OD05 identity, immutable method profile and exact container/IERS source manifest were prepared;
4. the exact dependency/IERS bytes were acquired ephemerally and reproducible offline container-build/preflight evidence was recorded in a bounded gate;
5. the separately reviewed authenticated exact-head workflow produced a five-create saved plan through WIF without apply;
6. extract and apply only the Artifact Registry foundation through a separate exact-head review;
7. publish the exact OCI candidate and record the registry-resolved digest;
8. refresh and review the authenticated platform plan using the published digest;
9. apply the remaining platform resources through a separate authorization;
10. execute the spike only after ADR/ARB/Release Quality authorization.

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

The bootstrap applied 27 additions with 0 changes and 0 destroys. Protected remote state, permanent-backend promotion, locking, recovery candidate and zero drift are post-verified; ARB-213-MI02 is satisfied. `BKL-031-F3-A3-CONTAINER-MANIFEST-002` at SHA-256 `02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879` records the exact base/platform, pinned BuildKit, hash-locked wheels and IERS identity `43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc` with offline fail-closed policy.

CI run `35122782246` acquired all ten artifacts ephemerally with exact hashes, built twice without cache or RUN network, and produced the same linux/amd64 image config ID `sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0`. Network-disabled preflight, exact package/profile checks and IERS campaign-date coverage passed. `BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001` at SHA-256 `00546062e78887af003adb010bb60dcfbdfb1480429e22314e4476673c7633a3` records the result. The image config ID is not a registry digest.

Authenticated workflow run `35131365596` on exact commit `380bd8c3d04f570acb21a9a7f532930111adcdc8` used the reviewed WIF deployer identity and produced two identical unpublished OCI manifests at `sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce`. The saved plan is exactly five additions, zero changes and zero destroys. It was not retained outside the job; its text SHA-256 is `6fd9c1c3f9d1c754d310f88fa2e8f3dfb2422a5a9195ec40f6f57087bbb8c83e`. The platform backend contains one validated empty state and no lock. Evidence is recorded in `BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-001` at SHA-256 `06cf923ae2bad1e869782bffd6a7e5389f9a68419d6199d0d7df5319f50b12e6`.

The dedicated `dsg-f3-a3` Artifact Registry repository exists and its foundation was post-verified empty before publication. Exact OCI publication, the refreshed authenticated four-resource plan and the exact saved-plan platform apply are separately evidenced. Artifact upload and job execution remain `NOT_EXECUTED`.

The repository prepared the registry foundation as an explicit-dispatch, main-only WIF workflow. Artifact Registry ownership remains isolated in a dedicated Terraform root and state; the platform state is empty. Static policy requires exactly one registry resource and prohibits `-target`, bootstrap/platform apply, image publication and cloud mutations outside the saved registry plan.

Foundation run `35134193946` applied its exact one-resource plan and passed the immediate zero-drift check. The final evidence assertion stopped on the automatically added `goog-terraform-provisioned=true` label; the configured labels and repository identity matched. Incident `BKL-031-F3-A3-RF-I01` therefore preserves the successful apply while requiring a corrected, separately reviewed read-only verification of the existing state, exact labels, zero drift and empty image inventory. Rerunning the one-shot apply is prohibited because the repository and state now exist. Image publication remains `NOT_EXECUTED`.

Read-only recovery run `35135376900` succeeded on exact commit `9c0bc79f3d7fc12c27f36d8b41c51058f5b3decd`. The registry state has one resource, serial `2`, lineage `4badab1d-5898-9bfa-948a-946e0c34492b`, raw SHA-256 `1429875a7626c9faf51f76060ae79f352b1f1e7a96e6bd5f59c152cbeb71ac7f`, zero drift and zero images. Evidence is recorded in `BKL-031-F3-A3-REGISTRY-FOUNDATION-EVIDENCE-001` at SHA-256 `3ef42c012c5c8d79a9751beb7c8e7c49ceab603a202c4a0cda359ef85ba08c30`.

Run `35138527237` on exact commit `3abc8aa049262336fd5a814593cdfc521e4fc594` published only the reproduced OCI manifest `sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce`. It verified two independent OCI rebuilds, a no-push registry-exporter preflight, the empty precondition, raw registry manifest bytes, config digest and exclusive one-image inventory. `BKL-031-F3-A3-OCI-PUBLICATION-EVIDENCE-001` records the result at SHA-256 `be2d999b9383df1e55c1627cdf48fa2dcde4040f88c3198d224bc48bef60833d`.

Separate run `35138798214` resolved that published digest and verified the four remaining absent resources. Its saved plan contains exactly four additions, zero changes and zero destroys; its binary, JSON and text SHA-256 values are recorded in `BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-002` at SHA-256 `8d1864d0a766d11ff51c8461adc12714a845ef41ee624dbd1e17826cf2d5fbbb`. Only the empty platform state persists. The next gate is a separately reviewed exact saved-plan apply; artifact upload and scientific execution remain blocked.

PR #233 integrated the explicit-dispatch, main-only platform-apply workflow after exact-head CI, process-separated ARB and Release Quality review. Run `35141947085` revalidated the published image inventory, empty backend state, absence of every target resource and absence of the approved kernel object, then applied only the saved plan with the four established create addresses. The exact network/subnet/job/IAM configuration now persists in state serial `3`; zero Cloud Run executions, continued kernel absence and zero Terraform drift were verified. `BKL-031-F3-A3-PLATFORM-APPLY-EVIDENCE-001` records the result at SHA-256 `ca5952b67904f514e2e05b7abfd8aeb4df71cfdba89958441ca233bd01e710b8`. The next separately reviewed gate is exact approved-kernel acquisition and private content-addressed upload. The job remains unexecuted.
