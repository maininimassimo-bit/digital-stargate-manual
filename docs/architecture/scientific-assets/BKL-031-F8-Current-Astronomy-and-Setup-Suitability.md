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

## Computation

The bounded F8 evidence covers the night 2026-09-17/18. It computes hourly target altitude/azimuth, solar altitude, Moon altitude/phase/separation and binds each hour to the real F7 forecast. Suitability is explicit and explainable from framing, filter/signal-family compatibility and image-scale/object-class compatibility. The final advisory score combines astronomy (60%), weather (30%) and setup suitability (10%). These weights are method parameters, not safety thresholds.

The display window filter `solarAltitudeDeg <= -18 and targetAltitudeDeg > 0` selects candidate dark-sky rows for presentation only. It is not a readiness, safety, scheduling or device-control rule.

## Public projection and privacy

`docs/data/observation-planner-f8-current-astronomy-suitability.json` exposes only the generalized site label, governed setup identifiers, bounded target profiles, hourly scientific/weather facts, setup-specific suitability and best windows. Protected latitude/longitude, elevation and provider grid coordinates are prohibited.

## Failure behaviour

The validator fails closed when F7 lineage is wrong, protected coordinates appear, the authority boundary changes, governed setup/target identities are missing, or required ranking/windows disappear. The browser consumer never falls back to F5/F6 values as if they were current F8 results.

## Authority boundaries

F8 does not grant readiness, go/no-go, automatic target selection, scheduling, command, action or Safety Authority. BKL-032 owns Session Readiness / Go-No-Go and local physical interlocks remain Safety Authority. S10 production runtime remains `UNAVAILABLE`.

## Acceptance boundary

F8 proves the scientific integration path for one governed night. It does **not** by itself prove recurring production forecast/astronomy refresh. BKL-031 therefore remains open until a final read-only functional/runtime closure gate demonstrates repeatable current-night refresh and portal integration without changing authority boundaries.
