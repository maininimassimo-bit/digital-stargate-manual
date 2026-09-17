# BKL-031 F8 — Current Astronomy and Setup Suitability

| Field | Value |
|---|---|
| Parent | BKL-031 — Observation Planner intelligente |
| Increment | F8 — current astronomy + explicit setup suitability |
| Status | REVIEW CANDIDATE |
| Date | 2026-09-17 |
| Authority | `NONE` / read-only advisory |
| Predecessor | F7 ACCEPTED — POST-MERGE VERIFIED |

## Purpose

F8 closes the scientific-evidence gap left after F7 by combining the real, protected-site F7 weather forecast with night-specific astronomical geometry and explicit OTA/camera/filter suitability. Exact site coordinates are resolved only inside the protected/server-side calculation boundary and are never written to the public projection.

## Governed inputs

- F7 sanitized real site forecast: `docs/data/observation-planner-forecast-f7-site-projection.json`.
- Approved current setup assignment and configuration baseline under `governance/setup-authority/`.
- Governed target identities and J2000 coordinates from the Target Knowledge / scientific metadata chain.
- Target physical profiles are bounded to LDN 1320 and M 27; historical acquisition is not treated as optical suitability by itself.
- Auditable suitability evidence: `docs/data/observation-planner-f8-suitability-evidence.json`, pinned to the approved setup baseline digest, setup-assignment digest, target-coordinate source blob and F7 workflow/artifact digest.

## Computation

The bounded F8 evidence covers the night 2026-09-17/18. It computes hourly target altitude/azimuth, solar altitude, Moon altitude/phase/separation and binds each hour to the real F7 forecast. Suitability is explicit and explainable from framing, filter/signal-family compatibility and image-scale/object-class compatibility. The final advisory score combines astronomy (60%), weather (30%) and setup suitability (10%). These weights are method parameters, not safety thresholds.

Setup suitability is independently auditable through three machine-readable component scores with weights framing `0.2`, filter/signal `0.4` and image-scale/object-class `0.4`. Each bounded setup-target case carries its inputs, component values, aggregate score and reason codes. The executable verifier recomputes the aggregate and rejects mutations.

The display window filter `solarAltitudeDeg <= -18 and targetAltitudeDeg > 0` selects candidate dark-sky rows for presentation only. It is not a readiness, safety, scheduling or device-control rule.

## Executable source binding

`.github/scripts/verify-observation-planner-f8.mjs` now verifies rather than merely trusting the projection:

- every F8 weather row is matched by instant to F7 and compared for cloud cover, relative humidity, precipitation, wind and gust values;
- F7 workflow run and artifact digest are pinned by the suitability evidence;
- effective focal length, f-ratio and image scale are checked against the approved setup baseline;
- horizontal/vertical FOV are recomputed from sensor dimensions and governed focal length;
- LDN 1320 and M 27 J2000 coordinates are checked against the pinned scientific-metadata source;
- suitability components are recomputed into the aggregate setup score;
- each displayed best-window advisory score, mean altitude and mean cloud cover is recomputed from the hourly F8 rows and method weights.

The test suite contains explicit mutation cases for F7 weather, setup optics, suitability components, aggregate suitability and advisory windows.

## Public projection and privacy

`docs/data/observation-planner-f8-current-astronomy-suitability.json` exposes only the generalized site label, governed setup identifiers, bounded target profiles, hourly scientific/weather facts, setup-specific suitability and best windows. Protected latitude/longitude, elevation and provider grid coordinates are prohibited.

## Failure behaviour

The validator fails closed when F7 lineage is wrong, a source-bound weather value changes, governed setup facts/FOV diverge, target coordinates lose their evidence binding, a suitability component or aggregate changes, protected coordinates appear, the authority boundary changes, governed setup/target identities are missing, or required ranking/windows disappear. The browser consumer never falls back to F5/F6 values as if they were current F8 results.

## Authority boundaries

F8 does not grant readiness, go/no-go, automatic target selection, scheduling, command, action or Safety Authority. BKL-032 owns Session Readiness / Go-No-Go and local physical interlocks remain Safety Authority. S10 production runtime remains `UNAVAILABLE`.

## Acceptance boundary

F8 proves the scientific integration path for one governed night. It does **not** by itself prove recurring production forecast/astronomy refresh. BKL-031 therefore remains open until a final read-only functional/runtime closure gate demonstrates repeatable current-night refresh and portal integration without changing authority boundaries.
