# BKL-031 F3-A3 Google Cloud infrastructure

This directory contains repository-only Terraform scaffolding for the future ephemeris/lunar validation spike.

Current state: BOOTSTRAP NOT EXECUTED, PLATFORM NOT PLANNED, PLATFORM NOT APPLIED, JOB NOT EXECUTED.

## Directories

- bootstrap: enables required APIs, creates the GitHub Workload Identity Federation trust, deployer/runtime service accounts, and private state/data/evidence buckets.
- method-profile: stores the canonical owner-approved decision profile used by the future container preflight.
- platform: creates Artifact Registry, an isolated VPC/subnet without Cloud NAT, and the digest-pinned Cloud Run Job.

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
- GCP_TF_STATE_BUCKET
- GCP_F3_DATA_BUCKET
- GCP_F3_EVIDENCE_BUCKET

## Platform gate

The platform module deliberately requires:

- an immutable container image digest;
- exact owner-approved SPK SHA-256 and private content-addressed URI;
- exact IERS snapshot SHA-256;
- immutable method profile `BKL-031-F3-A3-METHOD-PROFILE-001` at SHA-256 `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`;
- an exact owner-decision reference.

F3-OD05 is approved at artifact-identity level by `BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16`. The checked-in example carries the approved non-secret SPK digest and future private URI while retaining placeholders for still-unmaterialized runtime identities and artifacts. The SPK binary is never repository content.

The future container must embed the exact profile at `/app/dsg/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json` and invoke `.github/scripts/verify-bkl-031-f3-a3-method-profile.mjs` as a fail-closed preflight before scientific code. CI verifies the exact digest and proves that content or digest drift is rejected. No container has been built or executed.

This package has no authenticated plan/apply workflow. CI performs method-profile preflight, static policy and Terraform validation only. Bootstrap, authenticated plan/apply, upload and execution remain blocked by ARB-213-MI02, exact artifact/container evidence and exact-head re-review.

## Local validation

Run:

1. set `DSG_METHOD_PROFILE_PATH=infrastructure/bkl-031-f3-a3-gcp/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json` and `DSG_METHOD_PROFILE_SHA256=e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`, then run `node .github/scripts/verify-bkl-031-f3-a3-method-profile.mjs`
2. node .github/scripts/verify-bkl-031-f3-a3-gcp-bootstrap.mjs
3. terraform -chdir=bootstrap fmt -check
4. terraform -chdir=bootstrap init -backend=false
5. terraform -chdir=bootstrap validate
6. terraform -chdir=platform fmt -check
7. terraform -chdir=platform init -backend=false
8. terraform -chdir=platform validate

No command above authenticates to GCP or mutates cloud resources.
