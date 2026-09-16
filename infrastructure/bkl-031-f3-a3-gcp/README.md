# BKL-031 F3-A3 Google Cloud infrastructure

This directory contains the governed Terraform and container gates for the future ephemeris/lunar validation spike.

Current state: BOOTSTRAP APPLIED, REMOTE STATE AND BACKEND PROMOTION POST-VERIFIED, PREFLIGHT IMAGE PUBLISHED, EXACT FOUR-RESOURCE PLATFORM APPLIED AND ZERO-DRIFT VERIFIED, EXACT APPROVED KERNEL PRIVATELY PUBLISHED AND FULL-READ-BACK VERIFIED, BOUNDED SCIENTIFIC RUNNER SOURCE GATE PREPARED, JOB NOT EXECUTED.

## Directories

- bootstrap: enables required APIs, creates the GitHub Workload Identity Federation trust, deployer/runtime service accounts, and private state/data/evidence buckets.
- container: records the exact linux/amd64 base image, hash-locked Python wheels, pinned IERS-A snapshot identity, offline Astropy policy, fail-closed entrypoint and separate runner-candidate Dockerfile.
- runner: stores the bounded scientific runner and reviewed synthetic/public campaign fixture; neither file grants publication, platform-update or execution authority.
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

F3-OD05 is approved at artifact-identity level by `BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16`. The checked-in example carries the approved non-secret SPK digest and private URI while retaining placeholders for still-unmaterialized runtime identities and artifacts. The SPK binary is never repository content.

`BKL-031-F3-A3-CONTAINER-MANIFEST-002` fixes the linux/amd64 Python base and BuildKit by platform digest, every Python wheel by version and SHA-256, and `astropy-iers-data 0.2026.9.14.0.56.43` by SHA-256 `43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc`. Its raw SHA-256 is `02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879`. The container embeds the exact method profile and requires a fail-closed preflight before any supplied command. CI rejects manifest, dependency, base-image, build-tool, IERS, policy or source-file drift.

CI run `35122782246` acquired the ten exact dependency/IERS artifacts into an ignored ephemeral area and verified every hash. Two isolated no-cache builds with pinned BuildKit, normalized timestamps and no RUN network produced identical image config ID `sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0`. Network-disabled preflight verified the profile, installed package versions, IERS artifact and campaign-date coverage. The result is recorded in `BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001` at SHA-256 `00546062e78887af003adb010bb60dcfbdfb1480429e22314e4476673c7633a3`. This image config ID is not a registry digest. No wheel is committed.

The one-time bootstrap was applied from the reviewed saved plan for `main@af8b18f2f4e96642f453a30ead1e60e24ac8bd46`: 27 resources added, 0 changed and 0 destroyed. PR #219 promoted the permanent backend as merge `6c6a9454f1f1f13f72b4ae5098c0f2475b537d60`; remote lineage/content, recovery candidate, locking and a zero-drift exit code `0` were then verified. ARB-213-MI02 is satisfied.

Workflow run `35131365596` on exact main commit `380bd8c3d04f570acb21a9a7f532930111adcdc8` authenticated through the main-only WIF, rebuilt two identical unpublished OCI candidates and verified manifest digest `sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce`. Its saved Terraform plan contains exactly five additions, zero changes and zero destroys. The Artifact Registry repository, VPC, subnet and Cloud Run Job were confirmed absent before planning. The GCS backend contains only the empty state with zero resources and no residual lock. `BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-001` records that historical pre-foundation result.

The registry foundation is now isolated from the platform root without `-target`. The manual main-only workflow `BKL-031 F3-A3 Artifact Registry Foundation` fails closed unless the requested commit is the exact checked-out `main` head, the repository and registry state are absent, and the saved plan contains exactly one create action for `google_artifact_registry_repository.spike`. It applies only that saved plan and verifies one-resource state and zero drift. The source package does not execute the workflow. Exact-head CI, process-separated review, expected-head merge and post-merge verification are required before dispatch. Image publication is a later separate gate. The refreshed platform-plan workflow expects the future published digest and exactly four remaining create actions; it still cannot apply them.

Workflow run `35134193946` on exact main commit `ccf23e68f4bf8d321ccf707d0918e231c1ec2be1` authenticated through WIF, verified the one-create saved plan, applied the one registry resource and passed the immediate Terraform zero-drift plan. Its final evidence step then failed safely because Google added the provider-managed label `goog-terraform-provisioned=true` and the assertion expected only the four configured labels. No image operation exists in that workflow. The corrected assertion includes the exact provider label. A separate manual verification workflow performs only read-only repository/image inventory, one-resource state and zero-drift checks; it contains no apply, destroy or image publication.

Read-only run `35135376900` on exact main commit `9c0bc79f3d7fc12c27f36d8b41c51058f5b3decd` then verified the exact repository and labels, one-resource state, zero drift and zero images. `BKL-031-F3-A3-REGISTRY-FOUNDATION-EVIDENCE-001` records the apply, fail-closed incident and successful recovery at SHA-256 `3ef42c012c5c8d79a9751beb7c8e7c49ceab603a202c4a0cda359ef85ba08c30`. Exact OCI publication is the next separately reviewed gate. Platform apply, artifact upload and scientific execution remain blocked.

The exact OCI publication gate is an explicit-dispatch, main-only WIF workflow. Before it can publish, it revalidates the immutable source and registry-foundation evidence, rebuilds the OCI candidate twice without build network or cache, and requires manifest `sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce` and config `sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0`. A third no-push registry-exporter build must resolve to those same values. WIF then verifies the exact empty repository before the workflow performs its single push exporter. Registry-resolved manifest bytes, config, image count and commit-derived tag must match exactly. The workflow contains no Terraform, platform mutation, artifact upload or scientific execution. This source package prepares the gate; it does not publish the image.

PR #231 merged the reviewed gate as `3abc8aa049262336fd5a814593cdfc521e4fc594`. Run `35138527237` published and post-verified the exact manifest as the repository's sole image under tag `candidate-3abc8aa04926`; `BKL-031-F3-A3-OCI-PUBLICATION-EVIDENCE-001` records it at SHA-256 `be2d999b9383df1e55c1627cdf48fa2dcde4040f88c3198d224bc48bef60833d`. Separate plan-only run `35138798214` then resolved that registry digest and produced exactly four create actions with no change or destroy. `BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-002` records its ephemeral plan hashes and empty backend state at SHA-256 `8d1864d0a766d11ff51c8461adc12714a845ef41ee624dbd1e17826cf2d5fbbb`. The next gate is separately reviewed platform apply; artifact upload and scientific execution remain blocked.

The `BKL-031 F3-A3 Exact Platform Apply` workflow is manual, main-only and serialized with the authenticated plan gate. It fails closed unless the exact published image is the sole registry version, the platform state is the single validated empty object, the four target resources and the approved kernel object are absent, and a newly generated saved plan contains exactly the reviewed four create actions. Its only mutation command applies that saved plan once. Postconditions require the exact four-resource state, immutable job image and configuration, the deployer-only invoker binding, zero job executions, absent kernel, and an immediate zero-drift plan.

PR #233 merged that gate as `af81b807c8f6d8861ede3ecf3ae9b34e66df7790`. Run `35141947085` applied only the exact saved plan with four additions, zero changes and zero destroys. The protected platform state now contains the exact four addresses at serial `3`, lineage `2be9b82b-88d3-888f-4fcd-dded2f74f7f3` and raw SHA-256 `11b1888ceac0f39552e735d134a134bbbd7a6a75d623ac5c06897583842cf0e4`; the immediate plan reported zero drift. The Cloud Run Job has zero executions and the approved kernel object is still absent. `BKL-031-F3-A3-PLATFORM-APPLY-EVIDENCE-001` records the result at SHA-256 `ca5952b67904f514e2e05b7abfd8aeb4df71cfdba89958441ca233bd01e710b8`. The next separately reviewed gate is exact kernel acquisition and private content-addressed upload. Scientific execution, external reference traffic, protected-site use and runtime activation remain blocked.

The candidate `BKL-031 F3-A3 Exact Kernel Acquisition and Upload` workflow is manual and accepts only an exact `main` commit through the established WIF deployer. Before any external request it requires the protected data bucket, the exact reviewed four-resource platform state, the digest-pinned job with zero executions and an empty kernel prefix. A committed Node acquisition script performs one HTTPS request to the owner-approved NAIF URL, rejects redirects and verifies `32701440` bytes, `DAF/SPK`, SHA-256 `54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c` and MD5 `cc49327e06088124c0e39d8dde9f0b58`. The workflow contains one upload command, guarded by destination generation `0` and server-side Content-MD5, to the exact private content-addressed URI. It then reads the GCS object back, verifies the bytes and exclusive one-object inventory, confirms the job remains unexecuted and removes local ephemeral copies. This source package prepares the gate; it does not acquire or upload the kernel.

The first dispatch, run `35145051566`, stopped before acquisition because the least-privilege deployer correctly lacks the bucket-control-plane `storage.buckets.get` permission. No source request or upload occurred. The remediation preserves that IAM boundary and verifies the data bucket through the exact bootstrap state object already available to the deployer: raw live-generation SHA-256 `735b5fe6f368802ebf66ba14248ae85e9b7c7016e6a199e1561ea024d0a56386`, lineage `50e17f72-9d0a-0152-1130-060b583f103a`, serial `24`, and exact private/versioned/non-destructive attributes. Object listing still proves the approved bucket is reachable and the kernel prefix is empty before acquisition.

PR #236 merged that least-privilege remediation as `824afce15fe119b94e436fd19ec185d59e91e02c`. Run `35146023621` passed the exact bootstrap/platform/job/empty-prefix preconditions, made one non-redirected request to the approved NAIF source, verified the approved size, SPICE header, SHA-256 and MD5, and made one destination-generation-zero upload to the private content-addressed URI. GCS generation `1789590110146663` was then read back completely and reverified; the prefix contains exactly one object and Cloud Run execution count remains zero. `BKL-031-F3-A3-KERNEL-PUBLICATION-EVIDENCE-001` records the result at SHA-256 `53ca4364cd8c24495a5a7f4d1ca8bf6af3dfd1683ff6e8d73ffad7b884ef399b`. The next gate is separately reviewed exact scientific-spike execution. Horizons traffic, protected-site use and runtime activation remain blocked.

The published image is preflight-only and deliberately exits `78` when invoked without an override. `BKL-031-F3-A3-RUNNER-MANIFEST-001` therefore prepares a separate candidate image containing the exact synthetic/public fixture and a bounded fail-closed runner. It verifies the private kernel digest after read-only acquisition, evaluates Astropy 8.0.1 against Skyfield 1.55 using the same approved SPK, records each metric independently, repeats the calculation for deterministic-output evidence and writes one generation-zero evidence object. It permits only the metadata service and private Google Storage API; Horizons, protected-site data and runtime integration remain prohibited. CI builds the candidate twice offline and runs only its no-network contract self-test. No image publication, platform mutation or scientific calculation belongs to this source gate.

## Local validation

Run:

1. set `DSG_METHOD_PROFILE_PATH=infrastructure/bkl-031-f3-a3-gcp/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json` and `DSG_METHOD_PROFILE_SHA256=e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`, then run `node .github/scripts/verify-bkl-031-f3-a3-method-profile.mjs`
2. node .github/scripts/verify-bkl-031-f3-a3-container-evidence.mjs
3. node .github/scripts/verify-bkl-031-f3-a3-gcp-bootstrap.mjs
4. node .github/scripts/verify-bkl-031-f3-a3-platform-plan-gate.mjs
5. node .github/scripts/verify-bkl-031-f3-a3-registry-foundation-gate.mjs
6. node .github/scripts/verify-bkl-031-f3-a3-registry-foundation-verification.mjs
7. node .github/scripts/verify-bkl-031-f3-a3-exact-oci-publication.mjs
8. node .github/scripts/verify-bkl-031-f3-a3-platform-apply-gate.mjs
9. node .github/scripts/verify-bkl-031-f3-a3-kernel-acquisition-upload.mjs
10. node .github/scripts/verify-bkl-031-f3-a3-scientific-runner-gate.mjs
11. python infrastructure/bkl-031-f3-a3-gcp/runner/scientific_runner.py --contract-self-test
12. terraform -chdir=bootstrap fmt -check
13. terraform -chdir=bootstrap init -backend=false
14. terraform -chdir=bootstrap validate
15. terraform -chdir=registry fmt -check
16. terraform -chdir=registry init -backend=false
17. terraform -chdir=registry validate
18. terraform -chdir=platform fmt -check
19. terraform -chdir=platform init -backend=false
20. terraform -chdir=platform validate

No command above authenticates to GCP or mutates cloud resources.
