# BKL-031 F3-A3 Google Cloud infrastructure

This directory contains the governed Terraform and container gates for the future ephemeris/lunar validation spike.

Current state: BOOTSTRAP APPLIED, REMOTE STATE AND BACKEND PROMOTION POST-VERIFIED, REPRODUCIBLE OFFLINE CONTAINER BUILD AND NETWORK-DISABLED PREFLIGHT VERIFIED, AUTHENTICATED FIVE-RESOURCE PLAN VERIFIED, SEPARATE REGISTRY-FOUNDATION GATE PREPARED BUT NOT EXECUTED, IMAGE NOT PUBLISHED, REMAINING PLATFORM NOT APPLIED, JOB NOT EXECUTED.

## Directories

- bootstrap: enables required APIs, creates the GitHub Workload Identity Federation trust, deployer/runtime service accounts, and private state/data/evidence buckets.
- container: records the exact linux/amd64 base image, hash-locked Python wheels, pinned IERS-A snapshot identity, offline Astropy policy and fail-closed entrypoint for a future build.
- method-profile: stores the canonical owner-approved decision profile used by the future container preflight.
- registry: owns only the `dsg-f3-a3` Docker repository in a dedicated Terraform state.
- platform: owns the isolated VPC/subnet without Cloud NAT and the digest-pinned Cloud Run Job after image publication.

## Safety and privacy

This infrastructure is separate from the existing N.I.N.A./EAGLE plugin and telemetry relay. Do not reuse their service accounts, secrets, buckets, routes or project-level application credentials.

Do not place exact site coordinates, elevation, address, protected locators or protected record digests in Terraform variables, state, labels, logs or job environment variables.

The platform job uses all-traffic direct VPC egress and no Cloud NAT. Private Google Access permits Google API access while public internet egress remains blocked. A later Horizons campaign requires a separate reviewed network profile.

## One-time bootstrap

Prerequisites:

- an owner-selected GCP project with billing;
- globally unique bucket names;
- a short-lived authorized administrator session;
- Terraform 1.16.2.

The committed provider lock carries the reviewed `linux_amd64` and `windows_amd64` checksums. Operator initialization must keep the lock file unchanged.

The authoritative bootstrap and state-transition procedure is [STATE_MIGRATION_AND_RECOVERY.md](STATE_MIGRATION_AND_RECOVERY.md). Do not execute bootstrap commands from this summary. The reviewed procedure requires an exact saved plan, one operator for the complete change window, an initial local bootstrap, immediate migration to the protected GCS backend, state-lineage verification, recovery evidence and backend promotion before any second operator or automation. This is the only phase that requires a short-lived GCP administrator identity.

Do not create or download a service-account key.

After apply, record these outputs as GitHub repository variables:

- GCP_PROJECT_ID
- GCP_REGION
- GCP_WIF_PROVIDER
- GCP_DEPLOY_SERVICE_ACCOUNT
- GCP_RUNTIME_SERVICE_ACCOUNT
- GCP_STATE_BUCKET
- GCP_DATA_BUCKET
- GCP_EVIDENCE_BUCKET

## Platform gate

The platform module deliberately requires:

- an immutable container image digest;
- exact owner-approved SPK SHA-256 and private content-addressed URI;
- exact IERS snapshot SHA-256;
- immutable method profile `BKL-031-F3-A3-METHOD-PROFILE-001` at SHA-256 `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`;
- an exact owner-decision reference.

F3-OD05 is approved at artifact-identity level by `BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16`. The checked-in example carries the approved non-secret SPK digest and future private URI while retaining placeholders for still-unmaterialized runtime identities and artifacts. The SPK binary is never repository content.

`BKL-031-F3-A3-CONTAINER-MANIFEST-002` fixes the linux/amd64 Python base and BuildKit by platform digest, every Python wheel by version and SHA-256, and `astropy-iers-data 0.2026.9.14.0.56.43` by SHA-256 `43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc`. Its raw SHA-256 is `02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879`. The container embeds the exact method profile and requires a fail-closed preflight before any supplied command. CI rejects manifest, dependency, base-image, build-tool, IERS, policy or source-file drift.

CI run `35122782246` acquired the ten exact dependency/IERS artifacts into an ignored ephemeral area and verified every hash. Two isolated no-cache builds with pinned BuildKit, normalized timestamps and no RUN network produced identical image config ID `sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0`. Network-disabled preflight verified the profile, installed package versions, IERS artifact and campaign-date coverage. The result is recorded in `BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001` at SHA-256 `00546062e78887af003adb010bb60dcfbdfb1480429e22314e4476673c7633a3`. This image config ID is not a registry digest. No wheel is committed.

The one-time bootstrap was applied from the reviewed saved plan for `main@af8b18f2f4e96642f453a30ead1e60e24ac8bd46`: 27 resources added, 0 changed and 0 destroyed. PR #219 promoted the permanent backend as merge `6c6a9454f1f1f13f72b4ae5098c0f2475b537d60`; remote lineage/content, recovery candidate, locking and a zero-drift exit code `0` were then verified. ARB-213-MI02 is satisfied.

Workflow run `35131365596` on exact main commit `380bd8c3d04f570acb21a9a7f532930111adcdc8` authenticated through the main-only WIF, rebuilt two identical unpublished OCI candidates and verified manifest digest `sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce`. Its saved Terraform plan contains exactly five additions, zero changes and zero destroys. The Artifact Registry repository, VPC, subnet and Cloud Run Job were confirmed absent before planning. The GCS backend contains only the empty state with zero resources and no residual lock. `BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-001` records the result. Because the target repository is one of the five unapplied resources, image publication remains blocked until a separately reviewed registry-foundation apply. Platform apply, artifact upload and scientific execution remain blocked.

The registry foundation is now isolated from the platform root without `-target`. The manual main-only workflow `BKL-031 F3-A3 Artifact Registry Foundation` fails closed unless the requested commit is the exact checked-out `main` head, the repository and registry state are absent, and the saved plan contains exactly one create action for `google_artifact_registry_repository.spike`. It applies only that saved plan and verifies one-resource state and zero drift. The source package does not execute the workflow. Exact-head CI, process-separated review, expected-head merge and post-merge verification are required before dispatch. Image publication is a later separate gate. The refreshed platform-plan workflow expects the future published digest and exactly four remaining create actions; it still cannot apply them.

## Local validation

Run:

1. set `DSG_METHOD_PROFILE_PATH=infrastructure/bkl-031-f3-a3-gcp/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json` and `DSG_METHOD_PROFILE_SHA256=e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`, then run `node .github/scripts/verify-bkl-031-f3-a3-method-profile.mjs`
2. node .github/scripts/verify-bkl-031-f3-a3-container-evidence.mjs
3. node .github/scripts/verify-bkl-031-f3-a3-gcp-bootstrap.mjs
4. node .github/scripts/verify-bkl-031-f3-a3-platform-plan-gate.mjs
5. node .github/scripts/verify-bkl-031-f3-a3-registry-foundation-gate.mjs
6. terraform -chdir=bootstrap fmt -check
7. terraform -chdir=bootstrap init -backend=false
8. terraform -chdir=bootstrap validate
9. terraform -chdir=registry fmt -check
10. terraform -chdir=registry init -backend=false
11. terraform -chdir=registry validate
12. terraform -chdir=platform fmt -check
13. terraform -chdir=platform init -backend=false
14. terraform -chdir=platform validate

No command above authenticates to GCP or mutates cloud resources.
