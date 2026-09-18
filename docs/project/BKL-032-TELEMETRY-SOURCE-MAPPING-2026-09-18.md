# BKL-032 — Mandatory Telemetry Source Mapping

| Field | Value |
|---|---|
| Identifier | `BKL-032-SRC-001` |
| Date | 2026-09-18 |
| Status | **Source inventory complete at repository-contract level; runtime mapping open; owner thresholds defined** |
| Scope | Read-only evidence inputs for Session Readiness / Go-No-Go Decision Support |
| Authority | Local physical interlocks remain the Safety Authority |

## 1. Purpose and disposition

This record maps the owner-approved mandatory BKL-032 telemetry domains to repository-defined sources. It does not claim that a production readiness evaluator or a single live transport exists. `GO` remains unavailable until every mandatory domain has an accepted read-only source, a freshness/quality contract, and a validated consumer path.

The inventory is deliberately split into:

- `VERIFIED_REPOSITORY_SOURCE`: a repository contract or read-only adapter identifies the source and fields;
- `PARTIAL_SOURCE`: the artifact exists but does not provide all mandatory fields or semantics;
- `RUNTIME_OPEN`: repository evidence does not prove the live source/interface is currently integrated for BKL-032;
- `LIMIT_OPEN`: the required local operating limit is not numerically documented.

## 2. Mandatory domain matrix

| Mandatory domain | Candidate repository source | Evidence / fields | Current disposition | BKL-032 gap |
|---|---|---|---|---|
| Rain | N.I.N.A. Observatory Telemetry projection backed by CloudWatcher; `Export-NinaObservatoryStatus.ps1` maps `rainRate` | `weather.rain_rate_mm_h`; `docs/architecture/telemetry/observatory-status-realtime-telemetry-pilot.md` verifies the CloudWatcher CSV source | `PARTIAL_SOURCE` + `RUNTIME_OPEN` | CloudWatcher-only status export leaves `rain_rate_mm_h` null; live N.I.N.A. projection path is not a BKL-032 consumer |
| Wind | N.I.N.A. Observatory Telemetry projection | `windSpeed` → `wind_speed_m_s` / `wind_speed_kmh` | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | Runtime freshness and unit/field validation must be bound to the readiness input contract |
| Gusts | N.I.N.A. Observatory Telemetry projection | `windGust` → `wind_gust_m_s` / `wind_gust_kmh` | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | Runtime freshness and unit/field validation must be bound to the readiness input contract |
| Cloudiness | N.I.N.A. Observatory Telemetry projection | `cloudCoverPct` → `cloud_cover_pct` | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | CloudWatcher-only status export does not populate a normalized cloudiness field |
| Humidity / dew point | N.I.N.A. Observatory Telemetry projection backed by CloudWatcher | `humidityPct`, `dewPointC` → normalized weather fields | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | Readiness must reject null or stale fields; no synthetic derivation is allowed |
| Dome | N.I.N.A. Observatory Telemetry projection; bounded dome exporter path | `services.dome`; `nina-dome-exporter`; OPEN/CLOSED/MOVING/FAULT/UNKNOWN semantics | `PARTIAL_SOURCE` + `RUNTIME_OPEN` | Pilot records OPEN/CLOSED/SAFE runtime interface as not verified; no direct readiness integration |
| Mount | N.I.N.A. Observatory Telemetry projection | `services.mount`; diagnostics include park/home/tracking | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | Pilot records ASCOM/CPWI runtime contract as open; no concurrent driver polling is authorized |
| Camera | N.I.N.A. Observatory Telemetry projection | `services.camera`; diagnostics include temperature/cooler/exposing | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | Pilot records camera status interface as not verified |
| Power | N.I.N.A. Observatory Telemetry projection; TS Shelter J6 power adapter metadata | `mainsPresent`, `powerFault`, `powerFaultMask`, `safetyIsSafe` | `PARTIAL_SOURCE` + `RUNTIME_OPEN` | Source interface and semantics require runtime verification; observation must not become a power command path |
| Network | N.I.N.A. Observatory Telemetry projection; `Export-PassiveNetworkTelemetry.ps1` | route, gateway, Internet TCP, DNS, active-link metadata | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | Passive adapter does not prove Starlink/RUT955/VPN/LTE management telemetry; no credentials or scraping |
| EAGLE health | `DSG.EagleHostHealthCollector` and `DSG.EagleHealthPortalProjection` | host CPU, memory, storage, uptime, time sync, processes and bounded diagnostics; read-only | `VERIFIED_REPOSITORY_SOURCE` + `RUNTIME_OPEN` | Host health is not equipment safety; BKL-032 must consume a bounded read-only health signal without activating the portal health policy |

## 3. Freshness and quality binding

The owner-approved maximum forecast/readiness freshness is six hours. This is a BKL-032 acceptance limit, not a claim that every underlying telemetry source may publish at six-hour cadence. The evaluator must preserve each source's `observed_at_utc`, `fresh_until_utc`, `quality` and `source` and reject a mandatory signal that is missing, stale, conflicting or unavailable.

Existing repository artifacts use shorter pilot freshness windows for live telemetry (for example, 60 seconds for the CloudWatcher weather pilot and bounded collector freshness for EAGLE health). Those values may be used only when the specific source contract and runtime evidence are accepted; they must not be silently generalized across domains.

## 4. Owner-approved weather thresholds

The owner approved these BKL-032 readiness thresholds on 2026-09-18. They apply to both opening and continuation. A strict exceedance blocks; equality at the limit passes this threshold check.

| Signal | Blocking condition | Outcome |
|---|---|---|
| Mean wind | `wind_speed > 15 km/h` | `NO_GO` |
| Gust | `wind_gust > 20 km/h` | `NO_GO` |
| Cloudiness | `cloud_cover > 50%` | `NO_GO` |
| Relative humidity | `humidity > 90%` | `NO_GO` |
| Dew-point margin | `ambient_temperature - dew_point < 10 °C` | `NO_GO` |

The dew-point rule means that a margin of exactly `10 °C` passes this threshold check; a smaller margin blocks. Missing, stale, conflicting or unavailable values remain `INDETERMINATE` under the approved fail-closed semantics, rather than being treated as passing.

The older operational weather chapter still contains a generic `DA VALIDARE` note. The BKL-032 decision is scoped to this readiness capability and does not rewrite or promote that chapter into Safety Authority policy. A future safety/interlock change remains separately governed.

Accordingly:

- no value is copied from a sensor, generic astronomy practice, CloudWatcher condition label or historical narrative;
- these thresholds govern only BKL-032 decision support and never command or bypass local interlocks.

## 5. Authority boundary

All sources in this mapping are observational. They cannot open or close the dome, move the mount, control the camera, switch power, alter network equipment, schedule a session or bypass local interlocks. `EAGLE health` is host health and remains distinct from Safety Authority. The BKL-031 Planner remains advisory and is not a readiness source by implication.

## 6. Required next gate

Before implementation of the evaluator or a public readiness consumer:

1. approve one read-only source/transport contract for each mandatory domain;
2. reconcile the N.I.N.A./CloudWatcher, passive network and EAGLE projections into a versioned BKL-032 input contract;
3. approve the exact local wind and gust limit record, including units and authority;
4. define bounded synthetic fixtures for current, stale, missing, conflicting, rain-blocking and wind/gust-blocking cases;
5. repeat ARB and Release Quality review on the resulting exact head.

No provider traffic, device inspection, EAGLE operation or command is performed by this source inventory.

## 7. Traceability

- `docs/architecture/packages/BKL-032-Session-Readiness-Go-No-Go-Decision-Support.md`
- `docs/architecture/ADR-013-Session-Readiness-Go-No-Go-Boundary.md`
- `docs/architecture/telemetry/observatory-status-realtime-telemetry-pilot.md`
- `docs/architecture/telemetry/BKL-030-G1-Source-Inventory.md`
- `docs/architecture/telemetry/BKL-030-EAGLE-Health-Projection-Contract.md`
- `scripts/telemetry/Export-NinaObservatoryStatus.ps1`
- `scripts/telemetry/Export-CloudWatcherObservatoryStatus.ps1`
- `scripts/telemetry/Export-PassiveNetworkTelemetry.ps1`
- `scripts/telemetry/Export-EagleHostHealth.ps1`
- `docs/chapters/26-monitoraggio-meteo-sicurezza-ambientale.md`
