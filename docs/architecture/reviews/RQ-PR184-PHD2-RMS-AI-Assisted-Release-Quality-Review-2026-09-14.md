# Release Quality — PR #184 Profile-Aware PHD2 RMS Hotfix

| Campo | Valore |
|---|---|
| Review ID | RQ-PR184-PHD2-RMS-AI-001 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Data | 2026-09-14 |
| Pull request | [#184](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/184) |
| Technical head reviewed | `8e789779bccb7038ab8d2d37b170dd55055cf113` |
| Base | `main` @ `82a0524e03f5d22ee9ca8dd573d9d8b4b4fe79fb` |
| ARB result | Approved with Conditions — 95/100 |
| Recommendation | **CONDITIONALLY READY FOR MERGE** |

## 1. Authorization disclosure

This Release Quality review was produced in AI-assisted mode after explicit repository-owner authorization scoped to PR #184 and technical head `8e789779bccb7038ab8d2d37b170dd55055cf113`.

It is **not equivalent to an independent human approval**. Review-mode exception `W-PR184-PHD2-REVIEW-001` permits publication of the two disclosed reviews only. It does not authorize merge, branch-protection bypass, EAGLE activity or historical data migration.

## 2. Release impact report

The increment changes the semantics and observability of canonical PHD2 analytics:

- RMS is calculated from raw RA/DEC tracking displacement and converted with the active segment pixel scale;
- saturated-but-found samples are included and counted separately;
- rejected, settling-excluded and unscaled rows, failed settling and equipment profiles are exposed;
- Markdown and PDF reports disclose the corrected method and diagnostic counters;
- regression coverage includes synthetic SW4P/C8 cases and the affected real session.

The intended output for session `2026-09-13_2026-09-14` changes from unavailable RMS to RA 1.210 arcsec, DEC 0.731 arcsec and total 1.414 arcsec. The resulting canonical severity is expected to require attention because rejected frames are now counted deterministically; it must be confirmed by post-merge reprocessing.

No application release version, EAGLE module, uploader, observatory runtime, command path, external provider or deployment topology changes.

## 3. Quality-gate matrix

| Gate | Stato | Evidenza / rationale |
|---|---|---|
| Scope and capability boundary | Passed | four-file analytics/report/test hotfix; no runtime-control expansion |
| Architecture consistency | Passed with Conditions | AI-assisted ARB 95/100; no Blocker or Major |
| PHD2 semantic contract | Passed | header-based mapping, raw displacement, segment scale, error-code handling |
| Backward compatibility | Passed with Conditions | additive metric keys; corrected existing RMS meaning; historical comparability deferred |
| Build and repository tests | Passed | Developer Foundation `34834661474` |
| Python dual-profile regression | Passed | SW4P and C8 fixtures on exact head |
| Real-session regression | Passed | exact GuideLog counts and RMS asserted on exact head |
| Formatting | Passed | Developer Foundation formatting step |
| Analytics Center consistency | Passed | run `34834661498` |
| History validation | Passed | run `34834661457` |
| MkDocs strict build | Passed | Developer Foundation MkDocs step |
| Markdown/PDF report generation | Not Executed | generators were inspected but full report production was not part of the triggered pre-merge path |
| Security/privacy | Passed | no credentials, endpoints or new data transfer |
| Safety | Passed | read-only analytics; physical Safety Authority unchanged |
| Observability | Passed | method and sample-quality counters added |
| Current-session migration | Not Executed | requires post-merge workflow dispatch |
| Historical/catalog-detail migration | Not Applicable to this hotfix | explicitly deferred to a separate governed increment |
| Rollback | Passed with Conditions | revert code plus rerun/revert of any generated post-merge projections |
| Human-independent review | Not Executed | owner-authorized AI-assisted review is explicitly non-equivalent |
| Review-publication exact-head CI | Blocked until publication | review documents change the PR head |
| Branch protection | Blocked pending merge-time verification | no merge waiver is granted here |
| Merge authorization | Blocked | separate owner authorization on final exact head required |
| Post-merge verification | Not Executed | possible only after merge |

## 4. Risk and waiver register

| ID | Tipo | Stato | Trattamento |
|---|---|---|---|
| RQ184-R01 | AI review lacks human independence | Accepted for review publication only | explicit owner authorization and permanent disclosure |
| RQ184-R02 | current canonical metrics/report still contain unavailable RMS | Open until post-merge reprocessing | dispatch governed workflow and verify committed artifacts |
| RQ184-R03 | historical RMS values use mixed semantics | Retained | prohibit direct trend comparison until governed migration |
| RQ184-R04 | catalog PHD2 detail parser remains on old semantics | Retained / deferred | separate parity migration with F4/F5 digest regeneration |
| RQ184-R05 | all valid current-session guide samples are saturated | Operational observation | review PHD2 guide-star/profile exposure; do not discard valid RMS evidence |
| RQ184-R06 | report generators not executed pre-merge | Open until reprocessing | verify Markdown and PDF workflow outputs post-merge |
| RQ184-R07 | rejected-frame counting can change severity | Open until reprocessing | verify severity and reason text in canonical metrics/report |
| RQ184-R08 | branch protection state not established by this review | Merge-control risk | reverify at merge time; separate exact-head one-time waiver if absent |
| W-PR184-PHD2-REVIEW-001 | review-mode exception | Consumed on publication | not extensible to merge, runtime or migration |
| Merge waiver | branch-protection exception | Not authorized | requires separate explicit repository-owner decision |

## 5. Exact-head evidence

| Workflow | Run | Esito |
|---|---:|---|
| Developer Foundation | [34834661474](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/34834661474) | SUCCESS |
| Validate Digital StarGate History | [34834661457](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/34834661457) | SUCCESS |
| Validate Analytics Center Consistency | [34834661498](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/34834661498) | SUCCESS |

The reviewed head was open and mergeable and had no prior submitted review. Exact real-session evidence is enforced by `dsg-analytics/tests/test_scientific_session_evidence.py`.

Not executed:

- independent human approval;
- Markdown/PDF production and visual inspection;
- PC Principale or EAGLE OAT;
- post-merge reprocessing and projection publication;
- historical/catalog-detail migration;
- post-merge workflows.

## 6. Validation commands represented by CI

- `dotnet restore DigitalStarGate.sln`;
- `dotnet build DigitalStarGate.sln --configuration Release --no-restore`;
- `dotnet test DigitalStarGate.sln --configuration Release --no-build`;
- `dotnet format DigitalStarGate.sln --verify-no-changes --no-restore`;
- `python dsg-analytics/tests/test_scientific_session_evidence.py`;
- Analytics Center and history consistency validators;
- `mkdocs build --strict`.

## 7. Conditions before merge

1. Publish the ARB and Release Quality reviews plus their navigation links without changing the reviewed four-file technical implementation.
2. Require all applicable workflows to succeed on the resulting publication head.
3. Obtain separate explicit owner merge authorization bound to that exact final head.
4. Reverify branch protection at merge time and obtain a separate one-time waiver if it is absent.
5. Preserve the deferred historical/catalog-detail migration as an explicit limitation; do not imply that it was completed by this hotfix.

## 8. Post-merge verification requirements

1. Dispatch `Analyze Observatory Session Automatically` for `2026-09-13_2026-09-14`.
2. Verify committed canonical metrics contain the expected profile, counters and RMS values.
3. Verify severity and its reasons after deterministic rejected-frame counting.
4. Verify Markdown and PDF report generation, history refresh, catalog top-level RMS and downstream projection workflows.
5. Record actual merge SHA and generated analytics commit SHA.
6. Review the PHD2 `C8_QHY695A` guide-star/exposure configuration separately because all accepted samples are saturated.
7. Plan the historical RMS and catalog-detail parser migration as a separate governed change.

## 9. Readiness recommendation

**CONDITIONALLY READY FOR MERGE**, subject to successful review-publication workflows and separate exact-head repository-owner authorization.

This AI-assisted recommendation is not an independent human approval and does not itself authorize merge.
