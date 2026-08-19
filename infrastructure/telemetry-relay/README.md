# Digital StarGate Telemetry Relay — Hosted Pilot

Provider-neutral runtime for T3 of `DSG-SOL-OBS-RT-001`.

## Runtime contract

The container listens on HTTP `PORT` (default `8080`). Public TLS **must terminate at the hosting platform ingress/reverse proxy**. Direct public HTTP exposure is not accepted.

Required environment:

- `DSG_TELEMETRY_INGEST_TOKEN`: secret bearer token, required;
- `DSG_RELAY_ALLOWED_ORIGIN`: exact Observatory Status portal origin for hosted deployment.

Optional environment:

- `PORT=8080`;
- `DSG_RELAY_STORE_PATH=/data/observatory-status.json`;
- `DSG_RELAY_AUTHORIZED_SOURCE=EAGLE30154`;
- `DSG_RELAY_MAX_BODY_BYTES=65536`.

A writable `/data` volume is recommended for pilot continuity across process restarts. Loss of the stored snapshot is safe: query returns 404 and the portal must render UNKNOWN until a new current snapshot arrives.

## Endpoints

- `POST /v1/observatory-status` — bearer-authenticated ingest;
- `GET /v1/observatory-status` — latest accepted snapshot;
- `GET /health` — process/ingest counters;
- `OPTIONS` — CORS preflight.

There are no command endpoints.

## Unified NINA telemetry

The Observatory Status producer may publish read-only observations sourced from the Digital StarGate NINA Observatory Telemetry Exporter, including dome, mount, camera, weather and NINA SafetyMonitor observations. `safety.observed_state` may therefore be `SAFE`, `UNSAFE` or `UNKNOWN` and `safety.authority` may identify `NINA_SAFETY_MONITOR_OBSERVATION`.

This does **not** transfer safety authority to NINA, the producer, relay, portal or cloud runtime. `NINA_SAFETY_MONITOR_OBSERVATION` means only that the displayed state was observed through NINA. Local physical interlocks and the Local Safety Authority remain authoritative for equipment protection and command decisions.

Weather state `AVAILABLE` means that current weather telemetry is available; it must not be interpreted as weather-safe. Safety is represented separately by the `safety` projection.

## Local container verification

```bash
docker build -t dsg-telemetry-relay infrastructure/telemetry-relay
docker run --rm -p 127.0.0.1:8765:8080 \
  -e DSG_TELEMETRY_INGEST_TOKEN=dsg-localhost-pilot-token \
  -e DSG_RELAY_ALLOWED_ORIGIN=http://localhost \
  dsg-telemetry-relay
```

The existing PowerShell publisher can then target `http://127.0.0.1:8765/v1/observatory-status` because HTTP is allowed only for loopback integration testing.

## Hosted deployment acceptance

The selected host must provide evidence for all of the following before T3 can pass:

1. managed HTTPS endpoint with valid public certificate;
2. TLS 1.2+ and HTTP-to-HTTPS redirect or no public HTTP listener;
3. secret injection without committing token values;
4. outbound reachability from EAGLE30154;
5. exact CORS origin for the published portal;
6. health monitoring and application logs without Authorization header/token;
7. restart behavior and snapshot-store semantics documented;
8. negative auth test (`401`) and wrong-source test (`403`);
9. stale snapshot rejection (`422`);
10. EAGLE POST `202` and independent browser/client GET `200` with identical correlation id;
11. `SAFE`, `UNSAFE` and `UNKNOWN` observations are accepted without granting cloud command/safety authority;
12. relay outage does not affect local CloudWatcher, producer or Local Safety Authority;
13. portal decays to UNKNOWN when the hosted snapshot becomes stale/unavailable.

## Hosting selection criteria

The implementation is deliberately provider-neutral. Prefer a managed container/web runtime that supplies TLS termination, secret management, logs, health probes and a stable HTTPS hostname with minimal operational burden. Do not select a provider solely to complete the pilot; record the chosen provider, region, service tier, DNS name, persistence model, backup/recovery expectation and cost boundary as deployment evidence.

## Safety boundary

This relay is telemetry evidence transport only. It cannot command the EAGLE, dome, mount, camera, network or power systems. Safety values received through NINA are observations only. Overall observatory safety authority remains local; loss of NINA, cloud or relay connectivity must not alter local physical safety behavior.
