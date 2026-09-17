# BKL-031 F3-A3 — Scientific Campaign Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFICATION PENDING** |
| Date | 2026-09-17 |
| Capability | BKL-031 F3-A3 |
| Scientific execution | `dsg-f3-a3-spike-g4x8g` |
| Governed workflow | run `35189574972`, job `105098953021` |
| Runner source | `5ce8214311757c974134494dcc8f1e232dd4c390` |
| Evidence | `BKL-031-F3-A3-SCIENTIFIC-EXECUTION-EVIDENCE-001` |
| Decision record | ADR-010 Accepted for repository method authority |
| Runtime effect | None; S10 remains `UNAVAILABLE` |

## Decision

The exact remediated campaign passes the approved F3-A3 decision profile. Astropy 8.0.1 with jplephem 2.24 and the exact private `de442s.bsp` is accepted as the primary repository method. Skyfield 1.55 using the same governed SPK is accepted as an implementation cross-check. This result makes no claim of data-model independence and does not authorize an external reference, protected-site calculation or runtime adapter.

The campaign evaluated eight synthetic target/time vectors and 17 applicable metrics. All 17 passed. Deterministic repeatability passed, and the Mars transit difference was `0.08065768669985118` seconds against the approved five-second limit. Runner duration was 5,818 ms; the Cloud Run execution completed successfully in 16.34 seconds inside the 120-second task envelope.

The private evidence object was created once at generation `1789626252024638`. Its raw SHA-256 is `483794c9a8a373e8aff2f0dd2ab0f6342826c9bd210beeebcf92e744fad72494`; its normalized result SHA-256 is `d4f5163f0ef9c5701fb98a6b9ceef8411c24100e4674298183c770afbc2318e2`.

## Acceptance matrix

| Gate | Disposition | Evidence |
|---|---|---|
| exact artifacts and coverage | PASS | immutable method profile, runner image, IERS identity and kernel generation were checked before execution |
| positive scientific cases A3-P01–P08 | PASS | exact manifest, normalized synthetic request, bounded vectors, repeatability, shared target/Moon metrics, transit and illumination are present in the evidence |
| A3-P09 exact reuse | PASS BY CONTENT IDENTITY | no mutable cache or latest alias exists; the runner reads the exact content-addressed kernel and verifies its SHA-256 |
| A3-P10 sanitized publication | PASS | public record contains synthetic identifiers and digests only; protected-site use is `NOT_EXECUTED` |
| A3-N01–N08 | PASS STATIC / PREFLIGHT | manifest, digest, coverage, time/frame/refraction and IERS failures are rejected before or during bounded calculation |
| A3-N09 | PASS STATIC | a local failure exits non-zero; no alternate adapter path exists |
| A3-N10–N13 | NOT APPLICABLE BY APPROVED PROFILE | external-provider policy is `DENY`, no external client is present, and the fixture is synthetic |
| A3-N14 | PASS | repository/public-boundary checks and the exact evidence inspection found no protected value or protected digest |
| A3-N15–N16 | PASS | over-budget metrics produce conflicted evidence and non-zero exit; the accepted result is explicitly classified as a shared-SPK implementation cross-check |
| A3-N17 | PASS | request size, targets, instants, pairs, span and one-minute grid are bounded fail closed |
| A3-N18–N19 | NOT APPLICABLE BY DESIGN | the runner has no response cache and cannot serve stale prior output |
| A3-N20–N21 | PASS STATIC | unavailable/conflicted evidence is never promoted and no reference fallback exists |
| A3-N22 | PASS | execution host is the approved isolated Cloud Run Job in `europe-west8` |
| A3-N23–N24 | PASS STATIC | campaign contract contains no forecast, ranking, readiness, command or Safety field or behavior |
| resource and privacy boundary | PASS | one task, one parallelism, zero retries, synthetic site, zero external-reference calls |
| immutable postconditions | PASS | platform state serial 6 and raw digest, job generation 3, kernel generation and registry inventory remained unchanged |

The earlier dispatch `35188870937` is retained as `BKL-031-F3-A3-REMEDIATED-SCIENTIFIC-PREFLIGHT-INCIDENT-001`. It failed before execution because a local text pipeline had changed state bytes while calculating a digest. The corrected byte-preserving digest was reviewed before the successful dispatch. No execution or evidence object was created by the failed preflight.

## Governance outcome

ADR-010 is Accepted because the exact approved campaign passed every evaluated metric and bound, the failure/privacy controls are satisfied for the selected local-only profile, and the exact evidence enters ARB and Release Quality review in this change.

F3-A3 is complete at repository decision/evidence level. F3-B becomes the next dependency-ready increment for machine-readable contracts and validator work. F3-C, runtime activation, protected-site calculation, further Cloud Run execution and external-reference traffic remain separate gates. S10 remains `UNAVAILABLE` until an accepted F3-C adapter and projection exist.

## Post-merge condition

The acceptance becomes `POST-MERGE VERIFIED` only after exact-head CI, expected-head merge, successful repository workflows and successful Pages deployment. Failure preserves this record as a candidate and does not promote F3-B.
