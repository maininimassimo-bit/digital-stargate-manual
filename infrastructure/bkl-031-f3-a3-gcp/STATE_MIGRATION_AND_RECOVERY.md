# BKL-031 F3-A3 Terraform state migration and recovery

| Field | Value |
|---|---|
| Finding | ARB-213-MI02 |
| Scope | Bootstrap state lifecycle only |
| Status | PROCEDURE DEFINED — NOT EXECUTED |
| Backend | Google Cloud Storage |
| Bootstrap prefix | `bkl-031/f3-a3/bootstrap` |
| Platform prefix | `bkl-031/f3-a3/platform` |

## Purpose

This runbook governs the one-time transition of the bootstrap root from local Terraform state to the protected Google Cloud Storage state bucket created by that same bootstrap.

The state bucket uses uniform bucket-level access, enforced public-access prevention, Object Versioning and `force_destroy = false`.

This document does not authorize Google Cloud mutation. F3-OD05 is separately approved at the identity/provenance level; this procedure does not close ARB-213-MI01 or ARB-213-MI02 execution evidence and does not authorize platform plan/apply, container publication, artifact upload or Cloud Run execution.

## Mandatory stop conditions

Do not execute the bootstrap unless all of the following are true:

1. F3-OD05 is closed with exact SPK identity, coverage, provenance/notices and SHA-256.
2. ARB-213-MI01 is closed with an immutable full method profile.
3. An authenticated bootstrap plan from the exact reviewed commit is approved.
4. ARB and Release Quality re-review explicitly authorize bootstrap mutation.
5. One named operator owns the complete local-bootstrap and migration window.
6. No second operator or automation can run Terraform during the window.
7. The Git working tree is clean and the exact commit is recorded.
8. Terraform is version 1.16.2 and the committed dependency lock file is unchanged.
9. All operator inputs remain outside Git and contain no protected site data.
10. No service-account key is created or downloaded.

Failure of any condition is fail-closed.

## Fixed state identity

The bootstrap backend uses:

- bucket: the approved `state_bucket_name`;
- prefix: `bkl-031/f3-a3/bootstrap`;
- workspace: `default`;
- state object: `bkl-031/f3-a3/bootstrap/default.tfstate`.

The platform backend must use the same bucket with the distinct prefix `bkl-031/f3-a3/platform`.

## Phase 1 — reviewed local bootstrap

The following commands are execution instructions for a future authorized change window. They are not evidence of execution.

Set the paths and create a private evidence directory outside the repository:

```bash
export DSG_IAC_ROOT="$PWD/infrastructure/bkl-031-f3-a3-gcp"
export DSG_BOOTSTRAP_DIR="$DSG_IAC_ROOT/bootstrap"
export DSG_STATE_PREFIX="bkl-031/f3-a3/bootstrap"
export DSG_STATE_OBJECT="$DSG_STATE_PREFIX/default.tfstate"
umask 077
export DSG_STATE_EVIDENCE_DIR="$(mktemp -d)"
```

Create `bootstrap/terraform.tfvars` from the checked-in example. The file is ignored by Git. Set the approved project, region and globally unique bucket names. Do not add coordinates, elevation, protected locators, credentials or protected digests.

Record the exact source and toolchain:

```bash
git status --short
git rev-parse HEAD
terraform version
sha256sum "$DSG_BOOTSTRAP_DIR/.terraform.lock.hcl"
```

Initialize the bootstrap with the default local backend:

```bash
terraform -chdir="$DSG_BOOTSTRAP_DIR" init -reconfigure -input=false
```

Create and retain an exact reviewed plan outside the repository:

```bash
terraform -chdir="$DSG_BOOTSTRAP_DIR" plan -input=false -var-file=terraform.tfvars -out="$DSG_STATE_EVIDENCE_DIR/bootstrap.tfplan"
terraform -chdir="$DSG_BOOTSTRAP_DIR" show -json "$DSG_STATE_EVIDENCE_DIR/bootstrap.tfplan" > "$DSG_STATE_EVIDENCE_DIR/bootstrap-plan.json"
sha256sum "$DSG_STATE_EVIDENCE_DIR/bootstrap.tfplan" "$DSG_STATE_EVIDENCE_DIR/bootstrap-plan.json"
```

Only after exact-plan approval, apply that saved plan:

```bash
terraform -chdir="$DSG_BOOTSTRAP_DIR" apply -input=false "$DSG_STATE_EVIDENCE_DIR/bootstrap.tfplan"
```

No other Terraform operation is permitted until Phase 2 completes.

## Phase 2 — immediate migration to GCS

Set the exact bucket name from the approved bootstrap input:

```bash
export DSG_TF_STATE_BUCKET="replace-with-approved-state-bucket"
```

Verify the bucket protection before migration:

```bash
gcloud storage buckets describe "gs://$DSG_TF_STATE_BUCKET"
```

The operator must verify and record:

- approved region;
- uniform bucket-level access enabled;
- public-access prevention enforced;
- Object Versioning enabled;
- no public IAM principal;
- `force_destroy = false` remains in the reviewed Terraform source.

Pull and hash the local state before migration:

```bash
terraform -chdir="$DSG_BOOTSTRAP_DIR" state pull > "$DSG_STATE_EVIDENCE_DIR/bootstrap-pre-migration.tfstate"
jq -e '.lineage and (.serial | type == "number")' "$DSG_STATE_EVIDENCE_DIR/bootstrap-pre-migration.tfstate"
sha256sum "$DSG_STATE_EVIDENCE_DIR/bootstrap-pre-migration.tfstate"
```

Activate the reviewed backend template only for the controlled migration:

```bash
cp "$DSG_BOOTSTRAP_DIR/backend.tf.example" "$DSG_BOOTSTRAP_DIR/backend_migration.tf"
printf 'bucket = "%s"\nprefix = "%s"\n' "$DSG_TF_STATE_BUCKET" "$DSG_STATE_PREFIX" > "$DSG_BOOTSTRAP_DIR/backend.gcs.hcl"
```

Migrate interactively. Do not use `-force-copy`:

```bash
terraform -chdir="$DSG_BOOTSTRAP_DIR" init -migrate-state -input=true -backend-config=backend.gcs.hcl
```

Pull and verify the remote state:

```bash
terraform -chdir="$DSG_BOOTSTRAP_DIR" state pull > "$DSG_STATE_EVIDENCE_DIR/bootstrap-post-migration.tfstate"
jq -e '.lineage and (.serial | type == "number")' "$DSG_STATE_EVIDENCE_DIR/bootstrap-post-migration.tfstate"
test "$(jq -r '.lineage' "$DSG_STATE_EVIDENCE_DIR/bootstrap-pre-migration.tfstate")" = "$(jq -r '.lineage' "$DSG_STATE_EVIDENCE_DIR/bootstrap-post-migration.tfstate")"
test "$(jq -r '.serial' "$DSG_STATE_EVIDENCE_DIR/bootstrap-pre-migration.tfstate")" = "$(jq -r '.serial' "$DSG_STATE_EVIDENCE_DIR/bootstrap-post-migration.tfstate")"
sha256sum "$DSG_STATE_EVIDENCE_DIR/bootstrap-post-migration.tfstate"
```

Verify that the live object and its generations are visible:

```bash
gcloud storage ls --all-versions "gs://$DSG_TF_STATE_BUCKET/$DSG_STATE_PREFIX/"
```

Run a no-drift bootstrap plan. Exit code `0` is required; exit code `2` or any error blocks progression:

```bash
terraform -chdir="$DSG_BOOTSTRAP_DIR" plan -input=false -lock-timeout=60s -detailed-exitcode -var-file=terraform.tfvars
```

## Backend promotion gate

Before a second operator or any automation:

1. keep `backend_migration.tf` and `backend.gcs.hcl` local and protected;
2. create an immediate repository change that promotes the reviewed `backend "gcs" {}` block into `bootstrap/versions.tf`;
3. validate it using CI with `terraform init -backend=false`;
4. merge it through the normal exact-head review process;
5. reinitialize locally with the same approved backend configuration;
6. verify the remote lineage, serial and no-drift plan again;
7. only then remove the ignored `backend_migration.tf`.

Until this gate completes, no platform plan/apply and no second Terraform operator are permitted.

## Locking procedure

The GCS backend provides state locking.

- Never use `-lock=false`.
- Use a nonzero `-lock-timeout`.
- Do not run local Terraform concurrently with GitHub automation.
- Treat a lock as active unless the owning operation is conclusively absent.
- `terraform force-unlock LOCK_ID` is permitted only during an authorized incident, after confirming that no live Terraform process or workflow owns the lock.
- Record the lock ID, operator, UTC time, incident reference and verification evidence.
- Never use force-unlock merely to bypass contention.

## Recovery checklist

Recovery is an incident operation and must not be rehearsed against the live object by overwriting it.

1. stop all Terraform operations and automation;
2. confirm the exact bucket, prefix and object;
3. pull and securely hash the current live state;
4. list every generation:

```bash
gcloud storage ls --all-versions "gs://$DSG_TF_STATE_BUCKET/$DSG_STATE_PREFIX/"
```

5. select a generation using recorded lineage, serial and approved change evidence, never timestamp alone;
6. download the candidate generation to the private evidence directory without changing the live object:

```bash
gcloud storage cp "gs://$DSG_TF_STATE_BUCKET/$DSG_STATE_OBJECT#GENERATION_NUMBER" "$DSG_STATE_EVIDENCE_DIR/recovery-candidate.tfstate"
```

7. validate its JSON structure, lineage, serial and checksum;
8. obtain incident recovery approval;
9. restore the selected generation by copying it to the same live object:

```bash
gcloud storage cp "gs://$DSG_TF_STATE_BUCKET/$DSG_STATE_OBJECT#GENERATION_NUMBER" "gs://$DSG_TF_STATE_BUCKET/$DSG_STATE_OBJECT"
```

10. pull the restored state, verify lineage and serial, and run an approved no-drift plan;
11. preserve all evidence and record the new live generation.

Because Object Versioning is enabled, restoring a prior generation creates a new live generation and preserves the displaced live object as noncurrent.

## Migration failure rollback

If migration fails or any comparison differs:

1. stop immediately;
2. do not run plan, apply, `state push`, `-force-copy`, `-reconfigure` or force-unlock;
3. preserve the pre-migration state, post-migration output, `.terraform` directory and command transcript;
4. prevent every second operator and automation;
5. inspect the live and noncurrent GCS generations without modifying them;
6. perform recovery only through an approved incident procedure.

The pre-migration state is evidence and must never be committed, attached to a public issue or copied to an unapproved location.

## Required evidence

The MI02 execution record must contain:

- exact Git commit and approved plan SHA-256;
- operator and UTC change window;
- Terraform and Google provider versions;
- state-bucket protection output;
- pre/post state checksums, lineage and serial;
- GCS live object and generation identifiers;
- no-drift plan exit code;
- backend-promotion PR and merge SHA;
- locking checklist result;
- read-only recovery-candidate download result;
- deviations, failures and rollback actions.

Until all evidence is reviewed, ARB-213-MI02 remains open.
