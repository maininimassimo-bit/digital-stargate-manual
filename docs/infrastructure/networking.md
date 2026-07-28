# Networking and Connectivity

## Network model

The observatory network uses the following primary components:

- Starlink as the preferred Internet path;
- Teltonika RUT955 as LTE backup and VPN gateway;
- local wired and wireless LAN for observatory devices;
- secure remote access through VPN;
- controlled failover from Starlink to LTE connectivity.

## Reference addressing

Known reference addresses:

| Component | Address | Role |
|---|---|---|
| Teltonika RUT955 | `192.168.1.1` | Local gateway, VPN and LTE failover |
| Starlink router | `192.168.1.254` | Primary Internet connectivity |

Addressing must be maintained in the configuration registry and updated whenever the topology changes.

## Failover order

```text
Starlink
   ↓
LTE SIM 1
   ↓
LTE SIM 2
```

## Operational controls

- verify routing after each connectivity change;
- test VPN access periodically;
- avoid unmanaged duplicate DHCP services;
- document port-forwarding and firewall exceptions;
- preserve local control even during WAN loss.
