# BKL-031 F3-A3 Google Cloud infrastructure

This directory contains repository-only Terraform scaffolding for the future ephemeris/lunar validation spike.

Current state: BOOTSTRAP NOT EXECUTED, PLATFORM NOT PLANNED, PLATFORM NOT APPLIED, JOB NOT EXECUTED.

## Directories

- bootstrap: enables required APIs, creates the GitHub Workload Identity Federation trust, deployer/runtime service accounts, and private state/data/evidence buckets.
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
- exact SPK SHA-256;
- exact IERS snapshot SHA-256;
- an exact owner-decision reference.

F3-OD05 is still open, so no real platform tfvars file may be approved yet. The checked-in example uses obvious non-secret placeholders only.

This package has no authenticated plan/apply workflow. CI performs format, static policy and Terraform validation only. Authenticated plan/apply is a later reviewed increment after bootstrap and F3-OD05 closure.

## Local validation

Run:

1. node .github/scripts/verify-bkl-031-f3-a3-gcp-bootstrap.mjs
2. terraform -chdir=bootstrap fmt -check
3. terraform -chdir=bootstrap init -backend=false
4. terraform -chdir=bootstrap validate
5. terraform -chdir=platform fmt -check
6. terraform -chdir=platform init -backend=false
7. terraform -chdir=platform validate

No command above authenticates to GCP or mutates cloud resources.
