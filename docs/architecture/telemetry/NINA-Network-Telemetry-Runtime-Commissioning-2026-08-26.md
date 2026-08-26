# N.I.N.A. Passive Network Telemetry — Runtime Commissioning Evidence

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Runtime host | `EAGLE30154` |
| N.I.N.A. | `3.2.0.9001` |
| Plugin | Digital StarGate Observatory Telemetry Exporter |
| Plugin API directory actually loaded | `NINA\Plugins\3.0.0` |
| Data | 2026-08-26 |
| Stato | **NETWORK ACCEPTANCE PASS — end-to-end visibility, stale handling and recovery verified** |

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

Post-copy hash:

```text
E384539EA2062984E5250CA6AC3FE91BDE05A4B18066C964D0EC33F7E77C55BF
```

## 3. Unified projection evidence

Projection path:

```text
C:\Users\PrimaLuceLab\AppData\Local\DigitalStarGate\telemetry\nina-observatory-status.json
```

The plugin generated `schemaVersion = 2` and `source = nina-observatory-telemetry-exporter`.

Power remains fail-safe:

```text
connected = null
state     = UNKNOWN
reason    = NO_VERIFIED_POWER_SOURCE
```

## 4. Network runtime evidence

Observed Network service under healthy conditions:

```text
connected            = true
state                = ONLINE
reason               = null
interface            = Ethernet 2
gateway              = 192.168.1.254
gatewayReachable     = true
internetTarget       = 1.1.1.1:443
internetReachable    = true
dnsName              = github.com
dnsResolved          = true
activeLink           = null
vpn                  = null
lteFailover          = null
```

A canonical producer cycle verified:

```text
systems.network.state   = ONLINE
systems.network.quality = CURRENT
systems.network.source  = NINA Observatory Telemetry Exporter / Passive Network Adapter
```

Management-only semantics remain unresolved by design:

```text
active_link  = null
vpn          = null
lte_failover = null
```

## 5. Cadence and freshness

The plugin projection was observed updating during the smoke test and the persistent canonical producer is configured with:

```text
poll_seconds      = 15
freshness_seconds = 60
```

The producer remained `RUNNING` with zero consecutive failures during healthy operation.

## 6. Canonical producer and hosted transport evidence

The scheduled runtime task was observed as:

```text
DigitalStarGate-ObservatoryStatusTelemetry = Running
```

Producer health verified:

```text
component             = DSG.ObservatoryStatusTelemetryProducer
computer              = EAGLE30154
state                 = RUNNING
source.primary        = NINA_OBSERVATORY_TELEMETRY
source.active         = NINA_OBSERVATORY_TELEMETRY
source.fallback       = CLOUDWATCHER_CSV
source.fallback_count = 0
consecutive_failures  = 0
last_error            = null
```

Hosted transport verified repeated successful publishes:

```text
PUBLISH RESULT: PASS status=202 attempt=1
```

Therefore this path is runtime-verified:

```text
N.I.N.A. plugin
  -> nina-observatory-status.json
  -> DSG.NinaObservatoryTelemetryAdapter
  -> C:\DigitalStarGate\TelemetryRuntime\observatory-status.json
  -> authenticated hosted publish
  -> Cloud Run relay
```

## 7. Public Observatory Status visibility — PASS

Browser verification on the Digital StarGate Observatory Status page showed live Network telemetry:

```text
Rete | ONLINE
Interfaccia: Ethernet 2
Gateway: 192.168.1.254
Internet: Sì
DNS: Sì
Qualità: CURRENT
Active link: —
VPN: —
LTE failover: —
```

The dedicated upper KPI card `Rete osservata` also renders the same live Network state using the common Observatory Status bindings.

## 8. Stale/source-loss and recovery validation — PASS

A controlled operational test was performed without altering Ethernet, the RUT955, WAN, SIM or failover configuration.

Observed behavior:

```text
N.I.N.A. running
  -> Network telemetry ONLINE/CURRENT

N.I.N.A. closed
  -> Network telemetry transitions to UNKNOWN

N.I.N.A. restarted
  -> Network telemetry resumes automatically
  -> Network returns to live state from fresh observations
```

This verifies the fail-safe requirement that the portal does not retain the last `ONLINE` value as current when the N.I.N.A. telemetry source stops producing.

It also verifies automatic recovery after the source returns, without manual reset of the telemetry producer or network equipment.

## 9. Safety disposition

The Network commissioning remained observational only:

- no dome command;
- no mount command;
- no camera command;
- no power command;
- no router command;
- no WAN/failover/SIM/VPN configuration change;
- no SNMP service enabled;
- local observatory safety chain remains independent and authoritative.

## 10. Network acceptance decision

**PASS.** The Network branch of BKL-027 satisfies the acceptance requirements for the passive N.I.N.A.-integrated source:

1. real runtime source verified on `EAGLE30154`;
2. read-only/passive boundary preserved;
3. Network state rendered end-to-end on Observatory Status;
4. canonical freshness semantics operational;
5. source loss maps to `UNKNOWN` rather than retaining `ONLINE`;
6. telemetry resumes automatically after N.I.N.A. restart;
7. no router management or command path introduced;
8. `activeLink`, `vpn`, and `lteFailover` remain unknown until a separately approved source exists.

The **Network workstream is closed as PASS**. BKL-027 as a combined Power/Network item remains open only because Power has no verified source and therefore remains `UNKNOWN` by design.
