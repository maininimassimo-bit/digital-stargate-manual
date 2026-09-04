# Digital StarGate Telemetry Relay — Hosted Pilot

Provider-neutral hosted runtime for Observatory Status telemetry. The current deployment uses Google Cloud Run.

## Runtime contract

The container listens on HTTP `PORT` (default `8080`). Public TLS **must terminate at the hosting platform ingress/reverse proxy**. Direct public HTTP exposure is not accepted.

Required environment:

- `DSG_TELEMETRY_INGEST_TOKEN`: secret bearer token, required for both ingest channels;
- `DSG_RELAY_ALLOWED_ORIGIN`: exact Observatory Status portal origin.

Optional environment:

- `PORT=8080`;
- `DSG_RELAY_STORE_PATH=/data/observatory-status.json`;
- `DSG_RELAY_EAGLE_HEALTH_STORE_PATH=/data/eagle-health.json`;
- `DSG_RELAY_AUTHORIZED_SOURCE=EAGLE30154`;
- `DSG_RELAY_MAX_BODY_BYTES=65536`.

A writable `/data` volume is recommended for pilot continuity across process restarts. The two snapshots are stored independently. Loss of either snapshot is safe: its GET returns `404` and the portal must render that surface `UNKNOWN` or use its governed static fallback.

## Endpoints

Observatory telemetry:

- `POST /v1/observatory-status` — bearer-authenticated ingest;
- `GET /v1/observatory-status` — latest accepted observatory snapshot.

EAGLE host health:

- `POST /v1/eagle-health` — bearer-authenticated ingest of `DSG.EagleHealthPortalProjection`;
- `GET /v1/eagle-health` — latest accepted public/read-only EAGLE Health projection.

Common:

- `GET /health` — process and per-channel ingest counters;
- `OPTIONS` — CORS preflight.

There are **no command endpoints**.

## EAGLE Health validation

The relay accepts EAGLE Health only when all of the following hold:

- `schema_version = 1.0`;
- `component = DSG.EagleHealthPortalProjection`;
- `host = DSG_RELAY_AUTHORIZED_SOURCE` (currently `EAGLE30154`);
- `source_component = DSG.EagleHostHealthCollector`;
- `summary.state = UNKNOWN` and `summary.reason = POLICY_NOT_ACTIVATED`;
- `diagnostics.projection_mode = READ_ONLY_PUBLIC`;
- `diagnostics.automatic_remediation = false`;
- `diagnostics.safety_authority = OUTSIDE_SCOPE`;
- `Idempotency-Key` equals `source_correlation_id`;
- source `fresh_until_utc` has not expired.

The relay does not calculate host-health severity and does not extend source freshness.

## Unified NINA telemetry

The Observatory Status producer may publish read-only observations sourced from the Digital StarGate NINA Observatory Telemetry Exporter, including dome, mount, camera, weather and NINA SafetyMonitor observations. `safety.observed_state` may therefore be `SAFE`, `UNSAFE` or `UNKNOWN` and `safety.authority` may identify `NINA_SAFETY_MONITOR_OBSERVATION`.

This does **not** transfer safety authority to NINA, the producer, relay, portal or cloud runtime. Local physical interlocks and the Local Safety Authority remain authoritative for equipment protection and command decisions.

Weather state `AVAILABLE` means current weather telemetry is available; it must not be interpreted as weather-safe. Safety is represented separately by the `safety` projection.

## Publication pattern

```text
EAGLE30154
  +-- Observatory Status producer -> Publish-ObservatoryStatusTelemetry.ps1 -> POST /v1/observatory-status
  +-- EAGLE Health collector -> public projection adapter -> Publish-EagleHealthTelemetry.ps1 -> POST /v1/eagle-health

Google Cloud Run relay
  +-- GET /v1/observatory-status -> Observatory Status browser
  +-- GET /v1/eagle-health       -> EAGLE Health section
```

The bearer token exists only on the publishing side and in Cloud Run secret injection. It is never sent to the browser.

## Local container verification

```bash
docker build -t dsg-telemetry-relay infrastructure/telemetry-relay
docker run --rm -p 127.0.0.1:8765:8080 \
  -e DSG_TELEMETRY_INGEST_TOKEN=dsg-localhost-pilot-token \
  -e DSG_RELAY_ALLOWED_ORIGIN=http://localhost \
  dsg-telemetry-relay
```

PowerShell publishers may target loopback HTTP for integration testing only:

```text
http://127.0.0.1:8765/v1/observatory-status
http://127.0.0.1:8765/v1/eagle-health
```

Non-loopback publication requires HTTPS.

## Hosted deployment acceptance

The host must provide evidence for:

1. managed HTTPS endpoint with valid public certificate;
2. TLS 1.2+ and HTTP-to-HTTPS redirect or no public HTTP listener;
3. secret injection without committed token values;
4. outbound reachability from EAGLE30154;
5. exact CORS origin for the published portal;
6. health monitoring and logs without Authorization header/token;
7. restart behavior and independent snapshot-store semantics;
8. negative auth test (`401`) and wrong-source test (`403`);
9. stale snapshot rejection (`422`);
10. EAGLE POST `202` and independent browser/client GET `200` for each enabled channel;
11. EAGLE Health preserves `UNKNOWN / POLICY_NOT_ACTIVATED` and never becomes Safety Authority;
12. relay outage does not affect local collector, NINA, CloudWatcher or Local Safety Authority;
13. each portal surface decays independently to `UNKNOWN` when its hosted snapshot becomes stale/unavailable;
14. static fallback does not override a fresh hosted EAGLE Health projection.

## Safety boundary

This relay is telemetry evidence transport only. It cannot command the EAGLE, dome, mount, camera, network or power systems. EAGLE Health is host evidence, not observatory safety evidence. Safety values received through NINA remain observations only. Overall observatory safety authority remains local; loss of NINA, EAGLE Health, cloud or relay connectivity must not alter local physical safety behavior.
