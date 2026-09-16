# ARB PR 223 — BKL-031 F3-A3 Reproducible Container-Build Evidence AI-Assisted Review

| Field | Value |
|---|---|
| Review | ARB-PR223-BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001 |
| Date | 2026-09-16 |
| Pull request | #223 |
| Exact reviewed head | `4d471f7aec8ad4530fc07133416590b543bd1503` |
| Scope | Exact ephemeral acquisition, reproducible offline container build, network-disabled preflight and governed evidence/projections |
| Decision | **APPROVED WITH CONDITIONS — 99/100** |
| Independence note | AI-assisted process-separated review; not equivalent to independent human approval |

## Repository truth verified

- Immutable source manifest `BKL-031-F3-A3-CONTAINER-MANIFEST-002` has raw SHA-256 `02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879` and preserves predecessor manifest `001` as historical evidence.
- The acquisition script accepts only the ten exact `files.pythonhosted.org` URLs, rejects redirects/name mismatches, writes exclusively to the ignored container `.build/wheels` area and verifies every SHA-256 before build.
- The build context admits only reviewed container inputs and the immutable method profile. Package installation is offline, hash-locked and dependency-resolution-free.
- The linux/amd64 base and BuildKit platform are pinned by digest. BuildKit `0.30.0`, `SOURCE_DATE_EPOCH=0`, timestamp rewriting and compatibility version `30` make image assembly behavior explicit.
- CI run `35123762956` built twice without cache or RUN network and produced the same Docker image config ID in both candidates: `sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0`.
- The non-root container preflight passed with network disabled and verified exact method-profile bytes, IERS artifact SHA-256, installed package versions, offline policy and IERS-A coverage `MJD 41684.0..61659.0` for campaign preparation `MJD 61299.0`.
- The default scientific runner is absent by design and exits `78`; no scientific calculation was performed.
- `BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001` has raw SHA-256 `00546062e78887af003adb010bb60dcfbdfb1480429e22314e4476673c7633a3` and distinguishes the local image config ID from a future registry digest.
- Exact-head checks completed 9/9 successfully. The exact-head rebuild reproduced the same image ID recorded by the earlier successful implementation run.
- Image push, artifact upload, authenticated platform plan/apply, Horizons traffic, protected-site use, scientific execution and runtime activation remain `NOT_EXECUTED`. ADR-010 remains Proposed and S10 remains `UNAVAILABLE`.

## Architecture scorecard

| Dimension | Score | Evidence |
|---|---:|---|
| governing ADR/capability consistency | 100 | the gate advances evidence only and preserves ADR-010 Proposed plus S10 unavailable |
| reproducibility and immutability | 100 | exact URLs/hashes, digest-pinned build inputs/tool, two no-cache builds and identical image IDs |
| safety boundary | 100 | runner absent; no runtime, device, readiness, interlock or Safety Authority path |
| security and privacy | 100 | isolated context, non-root UID/GID, no credentials, no protected-site data and no network during preflight |
| fail-closed behavior | 100 | redirect/hash/source drift, method/profile/package/IERS drift and missing runner all fail closed |
| scientific-data governance | 99 | IERS identity, freshness and materialized coverage are verified; SPK acquisition remains outside scope |
| traceability | 99 | immutable evidence links source manifest, CI run/job, image ID, coverage and prohibited operations |
| operability | 96 | reproducible image exists only inside ephemeral CI; publication and registry digest remain separate |
| **Overall** | **99** | **Approved for build-evidence repository integration** |

## Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observations and carried conditions

- The recorded `sha256:411df908…` value is a Docker image config ID, not an Artifact Registry digest. It cannot be used as the Terraform image reference.
- The evidence JSON records the first successful implementation head/run. Exact-head run `35123762956` independently reproduced the same image ID after the evidence and governance update; this later CI record does not rewrite the immutable evidence file.
- External retrieval occurs only in the bounded acquisition and base/build-tool preparation steps. Dockerfile RUN steps and preflight run without network.
- The next gate must separately review immutable image publication and the authenticated exact-head platform plan. Platform apply and scientific execution remain later gates.
- No waiver or runtime authority is created by this approval.

## Decision

Approved with Conditions for repository integration of reproducible offline container-build evidence. The reviewed head closes acquisition/build/preflight evidence only. It grants no image-publication, artifact-upload, platform plan/apply, cloud-job, external-reference, protected-site, scientific or runtime authority.
