# BKL-031 F7 — Fresh Protected-Site Forecast Supply Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Capability | BKL-031 F7 |
| Solution | `BKL-031-F7-SOLUTION-001` |
| Environment / authority | `EVALUATION` / `NONE` |
| Consumer mode | `READ_ONLY` |
| Reviewed head | `000fc81558060b45e71b9f1a69122249b6a5fe8e` |
| Pull request | [#277](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/277) |
| Merge commit | `59a1d690406d733b6e61e64220f84cef9b6fb1a2` |
| Exact-head workflows | 9/9 successful |
| Post-merge workflows | 10/10 successful |
| Protected-site provider request | workflow run `35255829165`, attempt 1, SUCCESS |
| F7 provider request budget | `1/1_EXHAUSTED` |
| Runtime effect | One-shot evaluation supply only; S10 remains `UNAVAILABLE` |
| Safety effect | None; local physical interlocks remain authoritative |

## Accepted decision

F7 is accepted as the first governed Observation Planner forecast supply that uses the approved protected observatory coordinates for a real provider request while keeping those coordinates outside the public portal projection. The exact site coordinates are resolved only inside the server-side provider adapter under the explicit owner authorization and outbound privacy decision; they are neither logged into the public contract nor persisted in the public projection.

The accepted provider lineage is Open-Meteo Single Runs with upstream authority ItaliaMeteo/ARPAE and exact model selector `italia_meteo_arpae_icon_2i`, run initialization `2026-09-17T12:00Z`. The provider response contained 72 hourly positions; 71 complete positions were accepted, one initialization instant was excluded because precipitation was null/non-finite, zero values were imputed, and 66 accepted instants were future-valued at retrieval. Freshness at retrieval was within the ADR-011 18-hour ceiling.

The public projection `BKL031_F7_PROTECTED_SITE_SANITIZED_FORECAST_PROJECTION` contains the real normalized weather values and generalized public site label but no latitude, longitude, elevation, returned-grid coordinates, raw request URL or raw provider body. The browser consumer recomputes run age and fails closed instead of presenting stale evidence as a current forecast.

## Verification

The exact reviewed head `000fc81558060b45e71b9f1a69122249b6a5fe8e` completed all 9 applicable pull-request workflows successfully. Architecture Review Board returned **APPROVED WITH CONDITIONS** with 0 Blocker, 0 Major and 0 Minor findings. Release Quality returned **CONDITIONALLY READY FOR MERGE** with 0 blockers and 0 waivers.

PR #277 was merged under expected-head control as `59a1d690406d733b6e61e64220f84cef9b6fb1a2`. All 10 applicable post-merge push workflows completed successfully on that exact merge SHA, including F7 governance, Developer Foundation, documentation/manual pipelines and portal deployment paths.

## Retained limitations

- the accepted F7 provider acquisition is a one-shot evaluation request; recurring forecast refresh is not activated;
- the F7 protected-site request budget is permanently `1/1_EXHAUSTED` and does not authorize replay or additional provider traffic;
- recurring provider traffic requires a separately governed operating authorization covering cadence, provider/license mode, failure handling and freshness monitoring;
- ranking geometry from the earlier F5/F6 chain is not yet current-night astronomical evidence;
- setup compatibility from F6 is historical acquisition evidence, not explicit OTA/camera/filter suitability;
- no readiness/go-no-go, scheduler, automatic target selection, device command or Safety Authority is introduced;
- BKL-032 remains the separate owner of readiness/go-no-go decision support;
- S10 production runtime remains `UNAVAILABLE`.

## Transition

BKL-031 remains **In Progress**. F7 acceptance promotes **BKL-031 F8 current astronomy and explicit setup suitability integration** as the next dependency-ordered scientific gate.

F8 must calculate current target astronomical windows/altitude/transit/lunar geometry from governed site/time inputs, implement explicit OTA/camera/filter/target suitability rather than historical compatibility alone, and integrate those results with the current weather supply in an explainable read-only planner ranking. A later closure gate must additionally prove the governed recurring forecast operating model so the page remains fresh night after night rather than relying on one-shot evidence.
