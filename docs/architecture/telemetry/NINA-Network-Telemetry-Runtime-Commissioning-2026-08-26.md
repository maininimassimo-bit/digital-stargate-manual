# N.I.N.A. Passive Network Telemetry — Runtime Commissioning Evidence

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Runtime host | `EAGLE30154` |
| N.I.N.A. | `3.2.0.9001` |
| Plugin | Digital StarGate Observatory Telemetry Exporter |
| Plugin API directory actually loaded | `NINA\Plugins\3.0.0` |
| Data | 2026-08-26 |
| Stato | **END-TO-END NETWORK VISIBILITY PASS — stale/failure-mode validation pending** |

## 1. CI artifact

Validated GitHub Actions build:

```text
Workflow : NINA Dome Telemetry Exporter
Run      : 42
Commit   : 97a540ad979befe0d4b9765fc6beda2bac0193ae
Result   : SUCCESS
Build    : 0 warnings / 0 errors
```

Validated commissioning DLL:

```text
DigitalStarGate.Nina.DomeTelemetryExporter.dll
Length : 23040 bytes
SHA256 : E384539EA2062984E5250CA6AC3FE91BDE05A4B18066C964D0EC33F7E77C55BF
```

## 2. Deployment evidence

Pilot installer completed on `EAGLE30154` with:

```text
PILOT INSTALL RESULT: PASS
```

The previous plugin binary was backed up automatically.

N.I.N.A. `3.2.0.9001` was observed to load the plugin from the compatibility/API directory:

```text
C:\Users\PrimaLuceLab\AppData\Local\NINA\Plugins\3.0.0\Digital StarGate Dome Telemetry Exporter\DigitalStarGate.Nina.DomeTelemetryExporter.dll
```

The initially deployed copy under `Plugins\3.2.0` was not the assembly selected by N.I.N.A. The validated DLL was therefore copied, with an additional backup of the old binary, into the actually loaded `3.0.0` plugin API directory.

Post-copy hash:

```text
E384539EA2062984E5250CA6AC3FE91BDE05A4B18066C964D0EC33F7E77C55BF
```

The loaded module path was then verified from the running N.I.N.A. process and pointed to the `3.0.0` directory.

## 3. Unified projection evidence

Projection path:

```text
C:\Users\PrimaLuceLab\AppData\Local\DigitalStarGate\telemetry\nina-observatory-status.json
```

The plugin generated `schemaVersion = 2` and `source = nina-observatory-telemetry-exporter`.

During the initial smoke test all astronomy devices remained disconnected. Their states correctly degraded to `UNKNOWN`; no connection or equipment command was issued.

Power remained fail-safe:

```text
connected = null
state     = UNKNOWN
reason    = NO_VERIFIED_POWER_SOURCE
```

## 4. Network runtime evidence

Initial observed network service:

```text
connected            = true
state                = ONLINE
reason               = null
interface            = Ethernet 2
gateway              = 192.168.1.254
gatewayReachable     = true
gatewayLatencyMs     = 1
internetTarget       = 1.1.1.1:443
internetReachable    = true
internetLatencyMs    = 52
dnsName              = github.com
dnsResolved          = true
dnsLatencyMs         = 1
dnsAddressCount      = 1
activeLink           = null
vpn                  = null
lteFailover          = null
```

A subsequent canonical producer cycle on 2026-08-26 verified:

```text
systems.network.state           = ONLINE
systems.network.quality         = CURRENT
systems.network.source          = NINA Observatory Telemetry Exporter / Passive Network Adapter
systems.network.observed_at_utc = 2026-08-26T20:13:31.4381218Z
systems.network.fresh_until_utc = 2026-08-26T20:14:31.4381218Z

network_interface           = Ethernet 2
network_gateway             = 192.168.1.254
network_gateway_reachable   = true
network_gateway_latency_ms  = 1
network_internet_target     = 1.1.1.1:443
network_internet_reachable  = true
network_internet_latency_ms = 36
network_dns_name            = github.com
network_dns_resolved        = true
network_dns_latency_ms      = 33
network_dns_address_count   = 1

active_link  = null
vpn          = null
lte_failover = null
```

This validates the intended passive semantics:

- `ONLINE` is supported by local route/gateway evidence plus independent Internet TCP and DNS checks;
- no RUT955 management protocol is used;
- no router configuration is changed;
- `activeLink`, `vpn`, and `lteFailover` remain unresolved because passive host evidence cannot prove those management semantics.

## 5. Projection cadence evidence

A 10-second observation window showed:

```text
Updated = True
```

The file timestamp changed between the beginning and end of the window, consistent with the plugin's configured 5-second projection timer.

The persistent canonical producer is configured and observed with:

```text
poll_seconds      = 15
freshness_seconds = 60
state             = RUNNING
consecutive_failures = 0
```

## 6. Canonical producer and hosted transport evidence

The scheduled runtime task was observed before and after a controlled restart as:

```text
DigitalStarGate-ObservatoryStatusTelemetry = Running
```

Producer health after restart:

```text
component            = DSG.ObservatoryStatusTelemetryProducer
computer             = EAGLE30154
state                = RUNNING
source.primary       = NINA_OBSERVATORY_TELEMETRY
source.active        = NINA_OBSERVATORY_TELEMETRY
source.fallback      = CLOUDWATCHER_CSV
source.fallback_count = 0
consecutive_failures = 0
last_error           = null
```

Hosted transport evidence:

```text
transport.enabled              = true
transport.endpoint             = https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app/v1/observatory-status
transport.consecutive_failures = 0
transport.last_error           = null
transport.last_success_utc     = 2026-08-26T20:13:32.3826277Z
```

Producer log repeatedly reported:

```text
PUBLISH RESULT: PASS status=202 attempt=1
```

including correlation ID:

```text
1ae21944-4ce7-45b2-bf1f-05012e6518f6
```

Therefore the following runtime path is verified from EAGLE evidence:

```text
N.I.N.A. plugin
  -> nina-observatory-status.json
  -> DSG.NinaObservatoryTelemetryAdapter
  -> C:\DigitalStarGate\TelemetryRuntime\observatory-status.json
  -> authenticated hosted publish
  -> Cloud Run relay HTTP 202 accepted
```

## 7. Public Observatory Status visibility — PASS

Browser verification on the Digital StarGate Observatory Status page showed the Network row populated from live telemetry:

```text
Rete | ONLINE
Interfaccia: Ethernet 2
Gateway: 192.168.1.254 (Sì, 1 ms)
Internet: Sì (23 ms)
DNS: Sì (1 ms)
Qualità: CURRENT
Active link: —
VPN: —
LTE failover: —
```

This closes the hosted/public consumer visibility gate. The visible values are consistent with the canonical projection semantics: live passive Network evidence is rendered, while management-only semantics remain unresolved.

The end-to-end path is therefore verified:

```text
EAGLE30154
  -> N.I.N.A. plugin
  -> local unified projection
  -> canonical Observatory Status adapter
  -> persistent producer
  -> Cloud Run ingest/relay
  -> Observatory Status browser UI
```

## 8. Observatory Status mapping

Repository integration maps `projection.services.network` into the canonical Observatory Status `systems.network` signal with freshness semantics.

The portal renderer exposes:

- network state and quality;
- local interface;
- gateway reachability and latency;
- Internet reachability and latency;
- DNS reachability and latency;
- unresolved `active_link`, `vpn`, and `lte_failover` as unknown/null.

The browser continues to force stale signals to `UNKNOWN/STALE` after `fresh_until_utc` expires.

## 9. Safety disposition

The commissioning was observational only:

- no dome command;
- no mount command;
- no camera command;
- no power command;
- no router command;
- no WAN/failover/SIM/VPN configuration change;
- no SNMP service enabled;
- local observatory safety chain remains independent and authoritative.

## 10. Remaining acceptance work

Before the Network branch of BKL-027 can be fully closed:

1. validate stale/source-loss behavior when N.I.N.A. stops producing, without altering the physical network;
2. confirm Observatory Status maps expired projection to `UNKNOWN/STALE` rather than retaining `ONLINE` indefinitely;
3. retain the current 60-second freshness unless longer cadence evidence requires a governed adjustment;
4. keep `activeLink`, `vpn`, and `lteFailover` null/unknown unless a separately approved source becomes available.

## 11. Current decision

**Passive Network telemetry is verified end-to-end from the N.I.N.A. plugin on EAGLE30154 through the canonical producer and Cloud Run relay to the public Observatory Status page.**

BKL-027 Network remains open only for non-invasive stale/source-loss validation. Power remains `UNKNOWN` by design.
