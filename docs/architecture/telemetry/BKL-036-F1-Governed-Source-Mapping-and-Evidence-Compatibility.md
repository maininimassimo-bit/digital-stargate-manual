# BKL-036-F1 — Governed source mapping and evidence compatibility

| Field | Value |
|---|---|
| Identifier | `BKL-036-F1-SRC-001` |
| Status | Review candidate — repository/documentation-only |
| Date | 2026-09-18 |
| Runtime traffic | None authorized or used |
| Safety Authority | Local physical interlocks only |

## 1. Purpose

Define the source, field and evidence-compatibility boundary for BKL-036 using repository evidence already accepted elsewhere. This document is a mapping and gap register, not a runtime contract and not a score implementation.

## 2. Controlled classifications

### Evidence status

| Status | Meaning |
|---|---|
| `PRESENT` | Repository evidence identifies the source and required semantic locator. It is not runtime acceptance. |
| `MISSING` | No governed source or field was found. |
| `STALE` | Evidence exists but its declared validity has elapsed for the intended observation. |
| `UNAVAILABLE` | The source/interface is known but no usable observation is accepted for this consumer. |
| `PARTIAL` | Some fields or semantics exist, but the complete dimension contract is not established. |
| `CONFLICTING` | Governed sources disagree and no resolution authority is defined. |

### Evidence compatibility

| Compatibility | Meaning |
|---|---|
| `COMPARABLE` | Same semantic type, unit/scale, temporal basis, quality and authority boundary; descriptive grouping only. |
| `CONTEXT_ONLY` | Useful explanatory evidence, but not valid for cross-source aggregation in F1. |
| `INCOMPATIBLE` | Semantic, unit, temporal or authority mismatch prevents combination. |
| `UNKNOWN` | Repository evidence is insufficient to decide. |

`COMPARABLE` never authorizes a numeric score, weight, threshold or recommendation.

## 3. Source mapping

| BKL-036 dimension | Source authority / repository evidence | Field(s) and unit | Time/freshness contract | Evidence status | Compatibility | Runtime/consumer disposition |
|---|---|---|---|---|---|---|
| Weather context | BKL-032 source mapping and Observatory Status pilot; CloudWatcher/N.I.N.A. projection | `rain_rate_mm_h`, `wind_speed_kmh`, `wind_gust_kmh`, `cloud_cover_pct`, `humidity_pct`, `ambient_temperature_c`, `dew_point_c`; normalized units as named | `observed_at_utc`, `fresh_until_utc`, `quality`, `source`; pilot weather freshness is 60 s only for that pilot | `PARTIAL` | `CONTEXT_ONLY` | BKL-032 owns readiness/weather policy; CloudWatcher-only export leaves numeric fields incomplete; no BKL-036 live consumer |
| Dome availability | Observatory Status/N.I.N.A. telemetry contracts and bounded dome exporter records | `services.dome`; `OPEN`, `CLOSED`, `MOVING`, `FAULT`, `UNKNOWN`; unitless state | Projection envelope `observed_at_utc`/`fresh_until_utc`; actual OPEN/CLOSED/SAFE interface remains unverified | `PARTIAL` | `UNKNOWN` | Availability evidence is not Safety Authority; runtime mapping open |
| Mount availability | Observatory Status/N.I.N.A. projection and ASCOM/CPWI source records | `services.mount`; park/home/tracking state; unitless state | Projection timestamps and freshness when emitted; concurrent driver polling is not accepted | `PRESENT` | `CONTEXT_ONLY` | Host/driver availability evidence only; no readiness or command path |
| Camera availability | Observatory Status/N.I.N.A. projection and camera diagnostic contract | `services.camera`; temperature/cooler/exposing diagnostics where present; temperature in °C when supplied | Projection timestamps and freshness when emitted; camera status interface remains unverified | `PRESENT` | `CONTEXT_ONLY` | Availability evidence only; field completeness is unresolved |
| Power | N.I.N.A. projection and TS Shelter J6 metadata | `mainsPresent`, `powerFault`, `powerFaultMask`, `safetyIsSafe`; booleans/masks as defined by source | Source observation/freshness envelope where emitted; interface semantics require runtime verification | `PARTIAL` | `INCOMPATIBLE` | Power evidence cannot be interpreted as Safety Authority or a command permission |
| Network | BKL-027/BKL-028 N.I.N.A. exporter and `Export-PassiveNetworkTelemetry.ps1` | route/gateway reachability, Internet TCP, DNS, active-link metadata; booleans, addresses and durations as source-defined | Passive telemetry preserves observation/freshness metadata; router/VPN management telemetry is not included | `PRESENT` | `COMPARABLE` | Comparable only with the same network-availability semantic type; no router credentials or control |
| EAGLE host health | BKL-030 G1/G2 governed source inventory and projection contract | CPU/load, memory, logical/physical storage, uptime, time sync, processes, tasks, event evidence; source-native units | Per-signal `observed_at_utc`, `fresh_until_utc`, `quality`, `source`, cadence class; no unapproved numeric cadence generalized | `PRESENT` | `CONTEXT_ONLY` | Host-health evidence is not equipment health or Safety Authority; live BKL-036 consumer open |
| Telemetry freshness/producer health | Observatory Status producer-health and projection contracts | `state`, `quality`, `observed_at_utc`, `fresh_until_utc`, `correlation_id`, failure count; unitless/status fields | Source-defined freshness; CloudWatcher pilot uses 60 s, EAGLE contract leaves numeric cadence to later implementation | `PRESENT` | `COMPARABLE` | Comparable only within freshness/availability evidence with the same envelope semantics |
| Scientific session/pipeline | Governed session manifests, BKL-044 provenance contract and BKL-045 workflow-provenance boundary | `report_status`, session identity, file checksum/size and generated time; bytes, timestamps and lifecycle values | Session-scoped historical timestamps; no live freshness contract for observatory health | `PRESENT` | `CONTEXT_ONLY` | Historical/session evidence explains pipeline lineage; it cannot be promoted to live health |
| Cross-domain aggregate | No accepted source authority | No canonical field, unit, temporal basis or policy | No accepted aggregate freshness contract | `MISSING` | `UNKNOWN` | Future score policy is a separate gate |

## 4. Evidence-plane separation

| Plane | What it contains | What it proves |
|---|---|---|
| Repository evidence | Contracts, source inventories, pilots, manifests and historical records | That a source, field or semantic contract is documented and traceable |
| Live telemetry | A current observation with source timestamps and freshness | Only the observation represented by that accepted source contract |
| Runtime/consumer acceptance | An accepted transport and consumer path for a defined environment | That the governed consumer path has been validated |

No row in this mapping promotes repository evidence to live telemetry or runtime acceptance.

## 5. Gaps and fail-closed rules

- Missing, stale, unavailable, partial or conflicting evidence remains explicit.
- No null, unknown or stale value is replaced by zero, healthy, current or a default.
- A source with unresolved unit, timestamp, freshness or authority semantics is `UNKNOWN` or `PARTIAL`, never `COMPARABLE`.
- A historical session record cannot satisfy a live observatory-health freshness requirement.
- `safetyIsSafe`, CloudWatcher `Safe Status`, host health and descriptive health status do not change local interlock authority.
- Protected coordinates, credentials, tokens, raw sensitive payloads and live traffic are excluded.

## 6. Future gate entry conditions

Any next implementation or score-policy increment must define the versioned consumer contract, source ownership, retention, freshness per source, compatibility rules, bounded fixtures, privacy checks, rollback and authority wording, then pass exact-head CI, ARB, Release Quality, expected-head merge and post-merge verification.
