# ADR-010 — Ephemeris/Lunar Method and Validation Profile

| Field | Value |
|---|---|
| Status | **PROPOSED — REGISTRY FOUNDATION POST-VERIFIED / IMAGE NOT PUBLISHED / SCIENTIFIC CAMPAIGN NOT EXECUTED** |
| Date | 2026-09-15 |
| Release | Release 2.x planning increment |
| Capability | BKL-031 F3-A3 |
| Baseline | `main@527b298094b07e5a00317e60cab3abefed7a5759` |
| Decision authority | Repository Owner after evidence and ARB review |
| Runtime impact | None until separately authorized |

## Context

F3-A1 and F3-A2 have completed repository authority, but S08/S09 remain unavailable to runtime and S10 remains `UNAVAILABLE`. The owner approved the prudent method, accuracy, time-data, host and capacity baseline and completed F3-OD05 with the exact `de442s.bsp` identity, coverage, provenance, notices and SHA-256. The exact dependency/IERS inputs, reproducible offline container build and authenticated exact-head platform plan are verified; image publication, platform materialization and scientific validation remain absent.

This ADR records complete owner dispositions for F3-OD04–F3-OD10 and authorizes repository evidence and validation-only infrastructure source. It remains Proposed and does not authorize image publication, platform apply, further scientific-artifact acquisition, artifact upload, spike execution or runtime integration.

## Decision drivers

- reproducibility and exact artifact identity;
- sufficient scientific accuracy for planner evidence;
- local/offline determinism;
- explicit frame, time and refraction semantics;
- protected site privacy;
- independent validation;
- bounded resource use and cost;
- fail-closed behavior and no silent fallback;
- no EAGLE, N.I.N.A. or Safety Authority coupling.

## Recorded owner dispositions

| ID | Recorded disposition | State |
|---|---|---|
| F3-OD04 | Astropy 8.0.1 is the local primary candidate; jplephem 2.24 supports the governed SPK; Skyfield 1.55 is an explicit local implementation cross-check; Horizons API v1.3 is validation-only and never a runtime fallback | APPROVED |
| F3-OD05 | One exact local JPL SPK with declared target/time coverage, authoritative provenance, license/notice review and SHA-256 | **APPROVED — `de442s.bsp` / SHA-256 `54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c`** |
| F3-OD06 | geometric airless altitude ≤60 arcsec at altitude ≥5°; azimuth ≤60 arcsec for 5°–85°; above 85° use spherical separation ≤60 arcsec; target–Moon separation ≤60 arcsec; transit/culmination ≤5 s; lunar illumination absolute difference ≤0.001; rise/set geometric ≤60 s when included; each vector and metric passes independently; no averaging | APPROVED |
| F3-OD07 | pinned IERS-A snapshot with SHA-256; at most 30 days old when campaign is prepared; `auto_download=false` during execution; fail closed outside coverage; refresh through a governed campaign revision | APPROVED POLICY |
| F3-OD08 | no protected exact-site value in repository, logs or external requests; spike uses synthetic/generalized sites only; Horizons receives geocentric or synthetic/generalized inputs; local artifacts remain private; notices and retention are recorded | APPROVED |
| F3-OD09 | Google Cloud Run Job in `europe-west8`; immutable image digest; 2 vCPU, 2 GiB; task count 1, parallelism 1; 120 s task timeout; zero retries; dedicated service accounts; private buckets; no EAGLE/N.I.N.A./cupola access | APPROVED |
| F3-OD10 | max 50 targets; max 2,016 instants per target; max 10,000 target×instant pairs; max 7-day span; minimum grid step 1 minute; request ≤256 KiB; max concurrency 2; service-profile p95 ≤5 s after warm-up and hard timeout 15 s; spike batch bounded by the 120 s task timeout | APPROVED |

## Method profile

The selected roles are fixed for the future spike. The repository carries the canonical immutable profile `BKL-031-F3-A3-METHOD-PROFILE-001` at SHA-256 `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`. It includes every approved F3-OD06, F3-OD07 and F3-OD10 value together with the method, SPK, privacy, hosting and fail-closed boundaries. Terraform passes only its exact ID, path and digest; duplicated request-bound environment variables are prohibited.

The container embeds those exact bytes at `/app/dsg/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json` and invokes the repository preflight before scientific code. The preflight rejects modified bytes, an unreviewed digest or a changed approved value. Immutable source manifest `BKL-031-F3-A3-CONTAINER-MANIFEST-002` at SHA-256 `02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879` supersedes the static manifest without rewriting it and fixes the linux/amd64 Python base, BuildKit identity, all dependency wheels and IERS-A identity `43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc`, with runtime auto-download disabled. CI run `35122782246` acquired the ten artifacts ephemerally, verified their hashes, produced identical image config ID `sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0` in two isolated no-cache builds, and passed the preflight with network disabled. Evidence is fixed in `BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001` at SHA-256 `00546062e78887af003adb010bb60dcfbdfb1480429e22314e4476673c7633a3`. The image ID is not a registry digest and the image was not pushed or run scientifically.

Exact dependency artifacts, a future published registry digest, IERS snapshot identity and the F3-OD05 SPK identity must be recorded in the campaign manifest before execution.

Astropy and Skyfield using the same SPK are an implementation cross-check, not data-model independence. Horizons may be used only as a separately authorized validation reference and only with non-protected location inputs.

## Scientific semantics

- altitude and azimuth are geometric/airless;
- pressure is zero for the accepted baseline;
- UTC is the normalized input time scale and all conversion data is pinned;
- azimuth is not evaluated as a scalar near zenith; spherical separation is used above 85° altitude;
- refraction is outside this baseline and requires a separate profile;
- any unexplained over-budget vector blocks acceptance.

## Hosting decision

The validation host profile is a dedicated Cloud Run Job, not a VM and not EAGLE. The Google Cloud project may already host the N.I.N.A. plugin, but this profile shares no runtime identity, secret, bucket, route, queue or authorization with it.

Repository infrastructure:

- bootstrap module: APIs, service accounts, Workload Identity Federation and private buckets;
- platform module: Artifact Registry, private VPC/subnet and the Cloud Run Job;
- GitHub workflow: formatting, static policy, Terraform validation and bounded reproducible offline container-build evidence;
- no service-account key;
- no `allUsers` or `allAuthenticatedUsers`;
- no public network egress for the local profile because all traffic uses a VPC without Cloud NAT.

## Decision

`COMPLETE_OWNER_DECISION_RECORDED`.

F3-OD04–F3-OD10 are approved as recorded above. ADR-010 remains Proposed and S10 remains `UNAVAILABLE` because implementation and the authorized scientific campaign are not complete.

Authorized now:

- repository-only Terraform and CI scaffolding;
- static validation and documentation review;
- the recorded WIF-based exact-head plan-only gate and its empty backend state.

Not authorized now:

- platform-resource apply or any GCP mutation beyond the governed empty backend state;
- further acquisition or any upload of packages, SPK or IERS artifacts;
- additional container build or image push outside the reviewed exact-head gates;
- Cloud Run execution;
- Horizons call;
- protected-site use;
- runtime adapter, F3-B/F3-C, EAGLE or N.I.N.A. change.

## Consequences

### Positive

- most owner choices are exact and reviewable;
- the future host is isolated from observatory control paths;
- no static GCP credential is required after one-time bootstrap;
- compute cost is pay-per-execution rather than an idle VM;
- the exact SPK identity is content-addressed and fail-closed.

### Negative

- the one-time GCP administrator bootstrap, permanent-backend promotion and post-promotion verification are complete;
- ARB-213-MI01 and ARB-213-MI02 are satisfied; exact artifact acquisition, reproducible build, network-disabled preflight and authenticated exact-head plan evidence are recorded, while registry foundation, immutable image publication and a refreshed published-digest plan still block platform apply and spike execution;
- Cloud Run cold start and regional service availability must be measured;
- private VPC egress prevents Horizons from the local job profile.

## Migration

1. integrate the complete owner-decision evidence and repository-only infrastructure source;
2. owner completed F3-OD05 through `BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16`;
3. ARB and Release Quality review the completed decision profile;
4. a GCP administrator performed the one-time bootstrap using short-lived credentials and migrated its state to protected GCS;
5. GitHub variables are populated from bootstrap outputs;
6. exact artifacts were acquired ephemerally and a reproducible unpublished container was built and preflighted in a bounded increment;
7. the authenticated exact-head plan-only gate produced a verified five-create plan with an unpublished reproducible OCI digest;
8. a separately reviewed registry-foundation apply creates only the target repository, then the exact OCI candidate is published;
9. the authenticated plan is refreshed with the published registry digest and platform apply is separately reviewed;
10. the bounded spike is executed and evidence reviewed;
11. ADR-010 is Accepted, Rejected or remains Proposed;
12. F3-B remains blocked until acceptance conditions are satisfied.

## Validation

Normative plan: `docs/architecture/validation/BKL-031-F3-A3-Ephemeris-Lunar-Method-Validation-Spike-Plan.md`.

Current evidence:

- owner dispositions recorded on 2026-09-15;
- Google Cloud topology and Terraform scaffolding prepared;
- bootstrap Terraform apply executed with 27 additions, 0 changes and 0 destroys; platform Terraform apply `NOT EXECUTED`;
- exact container/IERS manifest and fail-closed source contract verified; ten artifacts acquired ephemerally; two reproducible offline builds and network-disabled preflight `PASS`; image push and artifact upload `NOT EXECUTED`;
- authenticated workflow run `35131365596` on `main@380bd8c3d04f570acb21a9a7f532930111adcdc8` produced two identical OCI manifest digests and an exact platform plan of 5 additions, 0 changes and 0 destroys; the backend state is present and empty; platform apply `NOT EXECUTED`;
- spike and scientific campaign `NOT EXECUTED`;
- dependency/IERS acquisition `EXACT_HASH_VERIFIED_EPHEMERAL`; SPK and other scientific-data acquisition `NOT EXECUTED`;
- privacy/runtime/OAT `NOT EXECUTED`.

## Traceability

- BKL-031-F3-A3-PROGRAM-001;
- BKL-031-F3-A3-SOLUTION-001;
- BKL-031-F3-A3-OD-2026-09-15;
- BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16;
- BKL-031-F3-A3-METHOD-PROFILE-001@sha256:e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca;
- BKL-031-F3-A3-CONTAINER-MANIFEST-002@sha256:02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879;
- BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001@sha256:00546062e78887af003adb010bb60dcfbdfb1480429e22314e4476673c7633a3;
- BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-001@sha256:06cf923ae2bad1e869782bffd6a7e5389f9a68419d6199d0d7df5319f50b12e6;
- ARB-213-MI01;
- BKL-031-F3-A3-INFRA-001;
- BKL-031-F3-A3-VAL-001;
- ADR-009;
- F3-OD04–F3-OD10;
- ARB-204-MI01 and ARB-204-MI02.

## Acceptance rule

ADR-010 may become Accepted only when F3-OD05 is exact, all package/container/data digests and coverage are recorded, the authorized campaign passes every approved metric and capacity bound, and ARB/Release Quality gates complete.

## Rollback

Revert the repository package for source changes. The authorized bootstrap and remote state require the governed Terraform state-recovery and rollback procedure; platform and runtime execution remain unauthorized.

## Governance stop

The authenticated exact-head five-resource plan, isolated Artifact Registry foundation, exact OCI publication and refreshed published-digest four-resource plan gates are complete. The registry contains one post-verified image at the approved digest, while the platform backend remains empty. Stop before the separately reviewed exact four-resource platform apply. Artifact upload, spike execution, protected-site use and runtime activation remain blocked. S10 remains `UNAVAILABLE`.
