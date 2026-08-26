# N.I.N.A. Passive Network Telemetry — Runtime Commissioning Evidence

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Runtime host | `EAGLE30154` |
| N.I.N.A. | `3.2.0.9001` |
| Plugin | Digital StarGate Observatory Telemetry Exporter |
| Plugin API directory actually loaded | `NINA\Plugins\3.0.0` |
| Data | 2026-08-26 |
| Stato | **RUNTIME SMOKE TEST PASS — cadence/failure-mode validation pending** |

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

During the smoke test all astronomy devices remained disconnected. Their states correctly degraded to `UNKNOWN`; no connection or equipment command was issued.

Power remained fail-safe:

```text
connected = null
state     = UNKNOWN
reason    = NO_VERIFIED_POWER_SOURCE
```

## 4. Network runtime evidence

Observed network service:

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

This validates the intended passive semantics:

- `ONLINE` is supported by local route/gateway evidence plus independent Internet TCP and DNS checks;
- no RUT955 management protocol is used;
- no router configuration is changed;
- `activeLink`, `vpn`, and `lteFailover` remain unresolved because passive host evidence cannot prove those management semantics.

## 5. Projection update evidence

A 10-second observation window showed:

```text
Updated = True
```

The file timestamp changed between the beginning and end of the window, consistent with the plugin's configured 5-second projection timer.

This is a smoke-test indication only; it is not yet the formal cadence/freshness acceptance evidence.

## 6. Safety disposition

The commissioning was observational only:

- no dome command;
- no mount command;
- no camera command;
- no power command;
- no router command;
- no WAN/failover/SIM/VPN configuration change;
- no SNMP service enabled;
- local observatory safety chain remains independent and authoritative.

## 7. Remaining acceptance work

Before the Network branch of BKL-027 can be considered complete:

1. measure projection cadence across a longer representative window;
2. validate stale/source-loss behavior when the plugin/N.I.N.A. producer stops, without altering the network;
3. confirm downstream Observatory Status freshness handling maps stopped/stale projection to `UNKNOWN/STALE` rather than retaining `ONLINE` indefinitely;
4. document final freshness threshold;
5. keep `activeLink`, `vpn`, and `lteFailover` null/unknown unless a separately approved source becomes available.

## 8. Current decision

**Passive Network source through the N.I.N.A. plugin is runtime-verified for `network.state = ONLINE` under healthy conditions.**

BKL-027 remains open only for cadence/freshness and non-invasive failure-mode validation. Power remains `UNKNOWN` by design.
