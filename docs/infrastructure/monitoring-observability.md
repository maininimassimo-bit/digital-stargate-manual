# Monitoring and Observability

## Monitoring scope

Infrastructure monitoring must cover:

- WAN connectivity;
- LAN reachability;
- VPN availability;
- compute health;
- disk capacity;
- power state;
- service availability;
- device connectivity;
- automation status;
- environmental and safety telemetry.

## Signal model

| Signal | Example | Severity |
|---|---|---|
| Metric | Disk free percentage | Informational to Critical |
| Event | Failover to LTE | Warning |
| Log | Driver restart failure | Error |
| Alert | Dome open with unsafe weather | Critical |

## Alerting principles

Alerts must be actionable, deduplicated and assigned a clear severity. Critical safety alerts must not depend solely on a public cloud service.
