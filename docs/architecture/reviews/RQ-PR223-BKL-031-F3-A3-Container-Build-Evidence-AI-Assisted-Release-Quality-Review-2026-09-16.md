# RQ PR 223 — BKL-031 F3-A3 Reproducible Container-Build Evidence AI-Assisted Release Quality Review

| Field | Value |
|---|---|
| Review | RQ-PR223-BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001 |
| Date | 2026-09-16 |
| Pull request | #223 |
| Exact reviewed head | `4d471f7aec8ad4530fc07133416590b543bd1503` |
| Release impact | Reproducible build evidence and governed portal status only; no published image or shipped runtime |
| Recommendation | **READY FOR EXPECTED-HEAD MERGE / NOT READY FOR IMAGE PUBLICATION, PLATFORM OR SPIKE** |
| Independence note | AI-assisted process-separated quality review; not equivalent to independent human approval |

## Release impact report

The increment replaces an online-install future-build contract with exact ephemeral acquisition, an isolated offline container build and materialized preflight evidence. It records an unpublished reproducible image config ID and advances the governed roadmap and Scientific Platform projection to the next separately reviewed publication/platform-plan gate. It changes no deployed portal application logic, cloud platform resource, scientific result, observatory device, EAGLE/N.I.N.A. behavior, readiness decision or Safety Authority.

## Exact-head quality gates

| Gate | Result | Evidence |
|---|---|---|
| static source/build evidence policy | Passed | GCP IaC run `35123762956`; immutable evidence digest and negative drift controls |
| reproducible offline build and preflight | Passed | GCP IaC run `35123762956`; identical candidates `sha256:411df908…bd5d0`, network-disabled preflight, IERS coverage pass |
| Terraform bootstrap fmt/init/validate | Passed | GCP IaC run `35123762956` |
| Terraform platform fmt/init/validate | Passed | GCP IaC run `35123762956` |
| Developer Foundation | Passed | run `35123762877` |
| documentation/MkDocs artifact | Passed | run `35123763053` |
| manual generation | Passed | run `35123762944` |
| Scientific Platform governance | Passed | run `35123762898` |
| governed projection sync | Passed | run `35123759218` |
| exact-head total | **9/9 passed** | head `4d471f7aec8ad4530fc07133416590b543bd1503` |

Local validation also passed the immutable container/build-evidence verifier, immutable method-profile verifier, GCP isolation policy, roadmap generation/consistency, Scientific Platform projection, workflow YAML parse, MkDocs strict build, diff checks and forbidden-artifact scan.

## Risk and waiver register

| ID | Risk | Disposition |
|---|---|---|
| RQ-223-R01 | local image config ID is mistaken for a registry digest | explicit identity kind and unavailable registry digest; publication requires a separate reviewed gate; no waiver |
| RQ-223-R02 | downloaded bytes or source endpoints drift | exact official URLs, redirect/name refusal, SHA-256 verification and ten-artifact closed set; no waiver |
| RQ-223-R03 | two builds differ because of timestamps or exporter behavior | pinned BuildKit platform digest, compatibility version `30`, normalized timestamps, no cache and equality assertion; no waiver |
| RQ-223-R04 | IERS data is exact but does not cover the campaign date | preflight opens installed IERS-A and proves `61299.0` lies within `41684.0..61659.0`; no waiver |
| RQ-223-R05 | build evidence is mistaken for scientific execution or runtime readiness | runner absence/exit `78`, ADR-010 Proposed, S10 unavailable and downstream controls `NOT_EXECUTED`; no waiver |
| RQ-223-R06 | evidence publication expands into image push or cloud mutation | no upload/push/plan/apply steps or credentials; separate gate required; no waiver |

## Readiness recommendation

Ready for expected-head merge as a reproducible offline build-evidence increment. After review-document publication, require successful checks on the final head, merge with expected-head protection and verify post-merge workflows plus live governed portal projections. Preserve the stop before image publication, authenticated platform plan/apply, artifact upload and scientific execution.
