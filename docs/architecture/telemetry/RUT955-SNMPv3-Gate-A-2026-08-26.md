# RUT955 SNMPv3 Gate A — Pre-check Evidence

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Device | Teltonika RUT955 — `192.168.1.254` |
| Firmware | `RUT9XX_R_00.06.09.5` |
| Gate | A — package availability and inert installation |
| Stato | **PRE-CHECK PASS — package installation authorized; service enablement not authorized** |
| Data | 2026-08-26 |

## 1. Backup

Configuration backup completed before change.

## 2. EAGLE30154 baseline

Observed at approximately 2026-08-26 20:00 local time:

```text
RUT955 HTTP/80 reachability  : PASS
RUT955 HTTPS/443 reachability: PASS
Default route                : 0.0.0.0/0 via 192.168.1.254
Route state                  : Alive
Internet 1.1.1.1:443         : PASS
DNS github.com               : PASS
```

Source host:

```text
EAGLE30154
SourceAddress = 192.168.1.144
Interface     = Ethernet 2
```

## 3. RUT955 authenticated baseline

```text
Uptime                  : 1d 8h 38m 41s
Since                   : 2026-08-25 11:24:07
Active WAN IP           : 192.168.1.171
Active WAN description  : Starlink router in failover
SIM in use              : SIM 1 — Ready
Mobile registration     : Registered (home)
Mobile operator         : Iliad
Mobile radio            : 4G (LTE)
OpenVPN state           : not present in current WebUI/status evidence
```

`OpenVPN state = not present` is recorded only as UI evidence; it is not used to infer absence of every possible VPN mechanism.

## 4. Package Manager evidence

```text
Package name : SNMP
Version      : 5.8 Based
Status       : Available
```

## 5. Gate A decision

PRE-CHECK PASS.

Authorized next action:

1. install the available `SNMP` package only;
2. do not enable SNMP service;
3. do not enable Remote Access;
4. do not configure traps;
5. do not change WAN, failover, SIM or VPN settings.

After package installation, Gate A acceptance requires re-verification of WebUI, WAN, Internet/DNS, package state and confirmation that SNMP service remains Disabled.

SNMP runtime use and service enablement remain NOT AUTHORIZED pending Gate B read-only-boundary verification.
