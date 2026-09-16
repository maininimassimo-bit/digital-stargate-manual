# BKL-031 F3-A3 — Ephemeris/Lunar Method Validation Spike Plan

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A3-VAL-001 |
| Status | **APPROVED DECISION PROFILE — AUTHENTICATED PLATFORM PLAN VERIFIED / SCIENTIFIC CAMPAIGN NOT EXECUTED** |
| Version | 1.1 |
| Date | 2026-09-15 |
| Architecture | BKL-031-F3-A3-SOLUTION-001 |
| Proposed ADR | ADR-010 |
| Baseline | `main@527b298094b07e5a00317e60cab3abefed7a5759` |
| Runtime / PC Principale / EAGLE | None |

## 1. Objective

Define the smallest reproducible evidence campaign that can inform F3-OD04–F3-OD10 without using production runtime, real protected site fixtures or implicit provider selection.

## 2. Entry gates

All must be satisfied before execution:

- ADR-010 contains explicit owner dispositions applicable to the spike;
- exact package/data versions and artifact digests are approved;
- license, notices, provenance and redistribution review is recorded;
- synthetic/generalized site and target inputs are approved;
- execution host is explicitly authorized and is not EAGLE;
- numeric per-metric error budget is approved;
- bounded grid and resource limits are approved;
- external access is disabled unless separately authorized;
- rollback and evidence destination are approved.

F3-OD04–F3-OD10 are recorded. F3-OD05 approves the exact `de442s.bsp` identity, but every scientific case remains `NOT EXECUTED`. The IERS snapshot must be pinned by SHA-256, no more than 30 days old at campaign preparation, with execution-time auto-download disabled and fail-closed coverage checks.

## 2.1 Immutable method-profile preflight

The canonical repository profile is `BKL-031-F3-A3-METHOD-PROFILE-001` with SHA-256 `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`. It records the approved method roles and every F3-OD06 scientific threshold, F3-OD07 time-data policy and F3-OD10 request/capacity limit. The same artifact also carries SPK identity, privacy, hosting and failure semantics.

Before any future scientific process starts, the container entrypoint verifies the embedded method profile, exact IERS wheel and installed package versions. A missing artifact, content mutation, unreviewed digest or value drift exits non-zero before calculation. Static CI executes positive and negative drift cases. `BKL-031-F3-A3-CONTAINER-MANIFEST-002` at SHA-256 `02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879` fixes the base/platform, pinned build tool and dependency identities, including IERS SHA-256 `43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc`. CI run `35122782246` acquired the exact inputs ephemerally, produced the same unpublished image config ID in two isolated no-cache builds and passed the preflight with network disabled. Scientific execution remains `NOT EXECUTED`.

## 3. Candidate manifests

| Track | Observed candidate baseline | Required execution pin |
|---|---|---|
| A | Astropy 8.0.1 + jplephem 2.24 | package artifact hashes, Python/runtime identity, exact JPL SPK and IERS data |
| B | Skyfield 1.55 | package artifact hash, Python/runtime identity, exact JPL SPK and timescale data |
| C | Horizons API v1.3 | response contract snapshot, request policy, service version evidence and privacy authorization |

Observed versions are decision inputs, not approved pins. Refresh them immediately before owner approval.

## 4. Test-data policy

- no exact Manciano coordinates, elevation, address, protected locator or protected record digest in public artifacts;
- use at least two unmistakably synthetic/generalized sites with `environment=TEST` and `authority=NONE`;
- use public celestial target coordinates with citations and immutable fixture digests;
- use UTC instants only; local-time displays are derived and never calculation inputs;
- real protected coordinates may be used only in a separately authorized protected campaign;
- Horizons receives geocentric or synthetic/generalized site data unless explicit exact-site approval exists;
- no golden vector is authoritative without generator/reference identity and digest.

## 5. Grid dimensions

The owner-approved maxima below are normative. The grid generator must enforce both per-axis and aggregate bounds before allocation.

| Dimension | Required coverage | Bound |
|---|---|---|
| target declination | representative north/equatorial/south targets | max 50 targets |
| hour angle | rise/set vicinity, transit and off-meridian | max 2,016 instants per target |
| lunar geometry | multiple phases and separations | aggregate target×instant pairs ≤10,000 |
| date | normal dates, time-data boundary, kernel boundaries | span ≤7 days; grid step ≥1 minute |
| site | synthetic latitude/longitude/elevation classes | synthetic/generalized only |
| refraction | airless baseline; refracted only as separate profile | airless only in this campaign |
| failure mutation | dependency/data/time/cache/provider errors | bounded case list |

The grid generator must reject expansion beyond the accepted manifest.

## 6. Metrics and units

| Metric | Calculation | Owner threshold |
|---|---|---|
| altitude difference | absolute angular difference in arcseconds | ≤60 arcsec at altitude ≥5° |
| azimuth difference | circular angular difference in arcseconds | ≤60 arcsec for altitude 5°–85°; above 85° use spherical separation ≤60 arcsec |
| transit difference | absolute time difference in seconds | ≤5 seconds |
| target–Moon separation difference | absolute angular difference in arcseconds | ≤60 arcsec |
| lunar illumination difference | absolute fraction difference | ≤0.001 |
| repeatability | same normalized input/profile across repeated executions | identical normalized output |
| performance | duration and peak resource observations | Cloud Run task ≤120 s, 2 vCPU/2 GiB, zero retries; service profile p95 ≤5 s and hard timeout 15 s |

Each metric passes independently. No average or weighted score is permitted.

## 7. Validation stages

### Stage V0 — Static decision evidence

Verify documents, identifiers, links, official-source snapshot, candidate manifests and owner dispositions. No dependency installation.

Execution record `A3-S01`: completed as static repository evidence on 2026-09-16. Official metadata, exact candidate artifact URLs/hashes/licenses, the immutable base-platform digest, the offline IERS configuration and fail-closed source contract were verified. No package or IERS artifact bytes were acquired, no dependency was installed and no image was built or run.

### Stage V1 — Isolated acquisition

On the authorized host only, acquire exact package/data artifacts, record hashes/attestations/licenses and prevent implicit network retrieval during calculation.

### Stage V2 — Synthetic execution

Execute the bounded grid for each authorized candidate. Store normalized inputs/results, raw protected evidence where authorized, metrics and digests.

### Stage V3 — Independent comparison

Compare implementation cross-checks separately from the approved independent reference. Record per-vector results and disagreement classification.

### Stage V4 — Failure, privacy and resource campaign

Execute negative cases, public-artifact scanning, parser/service failures, bounds and rollback.

### Stage V5 — Decision review

Produce a sanitized evidence matrix. ADR-010 is Accepted, Rejected or left Proposed. No adapter enters runtime.

## 8. Positive cases

| ID | Case | Expected evidence |
|---|---|---|
| A3-P01 | exact manifest resolves | all artifact identities and coverage recorded |
| A3-P02 | one normalized instant, airless topocentric | typed result with complete lineage |
| A3-P03 | bounded vector batch | every vector within accepted bounds |
| A3-P04 | repeated clean execution | repeatability within `E_repeat` |
| A3-P05 | target and Moon same instant/profile | shared request/profile digest |
| A3-P06 | meridian-transit comparison | per-method time and `E_transit` result |
| A3-P07 | lunar phase/illumination comparison | explicit convention and `E_illum` result |
| A3-P08 | target–Moon separation | consistent frame/time and `E_sep` result |
| A3-P09 | exact cache hit | identical artifact/request/profile identity |
| A3-P10 | sanitized publication | no protected value or correlatable digest |

## 9. Negative and boundary cases

| ID | Mutation/failure | Expected result |
|---|---|---|
| A3-N01 | package version range or `latest` | manifest rejected |
| A3-N02 | package/artifact hash mismatch | acquisition rejected |
| A3-N03 | kernel ID/hash mismatch | no calculation |
| A3-N04 | instant outside kernel coverage | `OUT_OF_COVERAGE` |
| A3-N05 | IERS/EOP missing or stale | `TIME_DATA_UNAVAILABLE` |
| A3-N06 | time scale/frame/epoch absent | invalid request/profile |
| A3-N07 | refraction requested without profile | invalid request/profile |
| A3-N08 | near-horizon refracted instability | separate-profile failure; airless baseline unaffected |
| A3-N09 | local adapter exception | S10 unavailable; no alternate adapter |
| A3-N10 | Horizons 503/timeout | reference unavailable; no promotion |
| A3-N11 | Horizons HTTP 200 with error payload | semantic failure |
| A3-N12 | malformed/unexpected remote payload | parser failure |
| A3-N13 | exact site data in remote request without approval | privacy failure |
| A3-N14 | protected coordinates/digest in public artifact/log | publication failure |
| A3-N15 | candidate disagreement over metric budget | conflicted evidence |
| A3-N16 | implementation agreement without independent reference | insufficient evidence |
| A3-N17 | target/instant/span exceeds bound | `REQUEST_BOUND_EXCEEDED` |
| A3-N18 | cached response identity mismatch | cache rejected |
| A3-N19 | previous result served after refresh failure as current | failure |
| A3-N20 | unavailable/conflicted result contains value | contract failure |
| A3-N21 | reference used as runtime fallback | architecture failure |
| A3-N22 | execution on EAGLE | placement failure |
| A3-N23 | forecast/ranking/readiness/command field appears | scope regression |
| A3-N24 | Safety state inferred | critical boundary failure |

## 10. Evidence manifest

Every run records:

- campaign ID and exact repository commit;
- execution host authorization reference;
- sanitized fixture-set digest;
- package/runtime artifact identities and hashes;
- kernel/data/IERS identities, hashes, coverage and freshness;
- method profile, time scale, frame, epoch, datum and refraction mode;
- normalized request/result digests;
- per-vector, per-metric difference and pass/fail;
- failure state/reason code;
- duration and bounded resource observations;
- external-call count and approved destination if applicable;
- privacy scan result;
- raw/sanitized evidence locations with access classification.

## 11. Independence rules

- Astropy and Skyfield using the same JPL SPK constitute an implementation cross-check, not full data-model independence.
- Horizons may serve as an external reference only within its accepted privacy/availability profile.
- A second kernel/report or another owner-approved reference is required if the accepted error budget demands data-model independence.
- No majority vote, averaging or silent normalization resolves disagreement.
- Any unexplained over-budget vector blocks acceptance.

## 12. Supply-chain and licensing gates

- verify package metadata, license and exact artifact hashes;
- verify JPL SPK source, coverage, checksum, notices and permitted retention/redistribution;
- verify IERS/EOP source, version, freshness and redistribution;
- generate an SBOM or equivalent manifest for the isolated spike;
- record vulnerability review at the exact versions;
- disable unpinned transitive resolution;
- prove rollback/removal of acquired artifacts.

## 13. Privacy and security gates

- scan public diff, generated site, logs and artifacts for coordinate pairs, protected IDs/digests, local hosts/paths and credentials;
- prove remote payload minimization;
- prove TLS verification and bounded timeouts if remote access is authorized;
- no remote request retry with a different site or method;
- malformed provider content remains untrusted input;
- public evidence uses non-correlatable references.

## 14. Quality-gate matrix

| Gate | Current state | Execution evidence required |
|---|---|---|
| architecture/ADR traceability | DEFINED | exact accepted ADR |
| package/data pins | EXACT DEPENDENCY/IERS ARTIFACTS HASH-VERIFIED EPHEMERALLY; REPRODUCIBLE BUILD/PREFLIGHT AND UNPUBLISHED OCI DIGEST PASS | published registry digest and campaign manifest remain |
| license/provenance | PACKAGE/IERS METADATA, EXACT ACQUIRED HASHES AND EXACT `de442s.bsp` IDENTITY RECORDED | SPK acquisition and execution-manifest review remain |
| scientific error budget | OWNER APPROVED | ADR-010 per-metric thresholds |
| synthetic grid | OWNER BOUNDED | 50 targets; 2,016 instants/target; 10,000 pairs; 7 days; 1-minute minimum step; 256 KiB request |
| candidate execution | NOT EXECUTED | normalized result evidence |
| independent reference | NOT SELECTED | accepted reference and vectors |
| failure/privacy tests | NOT EXECUTED | A3-N01–N24 results |
| performance/resource | PROFILE APPROVED / NOT EXECUTED | Cloud Run Job europe-west8, 2 vCPU, 2 GiB, one task, one parallelism, 120 s, zero retries |
| runtime/OAT | NOT AUTHORIZED | not part of spike |

## 15. Acceptance criteria

The spike may support ADR acceptance only when:

- every entry gate is satisfied;
- all artifact identities and coverage are exact;
- all positive cases pass;
- all negative/boundary cases produce expected fail-closed outcomes;
- every vector passes every owner-approved metric;
- independent-reference semantics are satisfied;
- no protected/public boundary violation occurs;
- resource bounds pass on the authorized host;
- evidence is reproducible from the manifest;
- ARB and Release Quality review the exact evidence commit.

## 16. Rollback

Delete or quarantine the isolated environment and acquired artifacts according to approved retention, retain audit evidence, reject/leave ADR-010 Proposed and keep S10 `UNAVAILABLE`. No operational rollback or EAGLE action is required.

## 17. Current execution status

Stage V0 record `A3-S01` is complete. Preparatory exact dependency/IERS acquisition, reproducible offline container builds and the network-disabled preflight passed and are recorded in `BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001`. The exact OCI image was subsequently published and the registry-resolved four-resource plan verified. Main-only WIF run `35141947085` then applied only the reviewed saved plan with four additions, zero changes and zero destroys; `BKL-031-F3-A3-PLATFORM-APPLY-EVIDENCE-001` records the exact state, immediate zero drift and zero job executions. Run `35146023621` subsequently acquired the exact approved `de442s.bsp` once, uploaded it once to the private content-addressed URI and verified GCS generation `1789590110146663` by full read-back; `BKL-031-F3-A3-KERNEL-PUBLICATION-EVIDENCE-001` records the result. This is preparatory infrastructure/data evidence, not execution of V1–V5. All stages V1–V5 and cases A3-P01–P10/A3-N01–N24 remain `NOT EXECUTED`; no scientific calculation occurred.

## 18. Governance stop

F3-OD05, bootstrap/MI02, reproducible offline container-build, isolated Artifact Registry foundation, exact OCI publication, refreshed plan, exact four-resource platform apply and exact private kernel publication gates are closed at evidence level. The target repository contains one post-verified image at the approved digest; the platform state contains only the exact VPC, subnet, Cloud Run Job and invoker binding with zero drift and zero executions; the private data prefix contains the one full-read-back-verified approved kernel object. Stop before separately reviewed exact scientific-spike execution. This plan does not authorize job execution, external reference calls, protected-site use, scientific execution, schema, adapter or runtime work.

## 19. Approved execution and request envelope

The future local campaign uses a dedicated Cloud Run Job in `europe-west8`, an immutable image digest, 2 vCPU, 2 GiB, task count 1, parallelism 1, 120-second timeout and zero retries. The runtime identity reads a private data bucket and creates objects in a separate private evidence bucket. The job has no EAGLE, N.I.N.A. or observatory-control dependency.

The serialized request is limited to 256 KiB and concurrency to two requests. Capacity rejection occurs before expansion or allocation. Public internet egress is denied in the local job profile. Horizons, if separately authorized, uses another reviewed profile and only geocentric or synthetic/generalized site inputs.
