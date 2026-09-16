# ARB PR 221 — BKL-031 F3-A3 Static Container/IERS AI-Assisted Review

| Field | Value |
|---|---|
| Review | ARB-PR221-BKL-031-F3-A3-CONTAINER-IERS-001 |
| Date | 2026-09-16 |
| Pull request | #221 |
| Exact reviewed head | `bfad9412c7de891e59bb232c146ea6fc19f6c1fe` |
| Scope | Static container/IERS identity, fail-closed source contract and governed projections |
| Decision | **APPROVED WITH CONDITIONS — 98/100** |
| Independence note | AI-assisted process-separated review; not equivalent to independent human approval |

## Repository truth verified

- The raw manifest digest is `7923206d85c5670ef56f9310a813c165c7d516d226c994561516c843b338412e`.
- The linux/amd64 base image is fixed by platform digest; every declared Python wheel has an exact version, official file URL, SHA-256 and license expression.
- IERS-A is fixed as `astropy-iers-data 0.2026.9.14.0.56.43` with SHA-256 `43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc`, two days old at campaign preparation and below the approved 30-day limit.
- Runtime auto-download is disabled and degraded IERS accuracy fails closed.
- The entrypoint runs the profile/IERS/package preflight before any future supplied command; the current default command exits `78` because no scientific runner exists.
- Terraform accepts only the reviewed IERS digest.
- No wheel, SPK, FITS or IERS data bytes are committed; acquisition, installation, build, push, platform plan/apply, external traffic, protected-site use and scientific execution remain `NOT_EXECUTED`.
- ADR-010 remains Proposed and S10 remains `UNAVAILABLE`.
- Exact-head CI completed 7/7 successful checks, including static policy and both Terraform roots.

## Architecture scorecard

| Dimension | Score | Evidence |
|---|---:|---|
| governing ADR/capability consistency | 100 | manifest implements the approved F3-OD04/F3-OD07 identities without changing ADR status |
| reproducibility and immutability | 99 | platform base, ten wheels, method profile and source files are content-addressed |
| safety boundary | 100 | no runtime, device, readiness, interlock or Safety Authority path |
| security and privacy | 100 | non-root future image, no credential, no public principal, network retrieval denied during execution |
| fail-closed behavior | 99 | semantic verifier, negative mutations, exact Terraform value and entrypoint preflight |
| scientific-data governance | 96 | static IERS identity/freshness is exact; byte-level coverage inspection belongs to the next gate |
| traceability | 98 | ADR, validation plan, hosting plan, backlog, handover and generated projections align |
| operability | 94 | source contract is reviewable; materialized build and SBOM remain intentionally absent |
| **Overall** | **98** | **Approved for static repository integration** |

## Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observations and carried conditions

- The manifest proves reviewed identity and future inclusion intent. It does not prove downloaded bytes, internal IERS coverage, successful dependency installation or a built image.
- The next gate must acquire only the declared artifacts, verify their bytes and coverage, build reproducibly and record the image digest without pushing it.
- Image push, authenticated platform plan/apply, artifact upload, scientific execution, Horizons traffic, protected-site use and runtime activation require later separately reviewed gates.
- No waiver is created by this approval.

## Decision

Approved with Conditions for static repository integration. The reviewed head closes the exact container/IERS source-evidence gate only. It grants no artifact-acquisition, build, cloud, scientific or runtime authority.
