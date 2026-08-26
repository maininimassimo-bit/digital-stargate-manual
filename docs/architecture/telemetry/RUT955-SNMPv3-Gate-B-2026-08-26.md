# RUT955 SNMPv3 Gate B — Read-Only Boundary Verification

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Device | Teltonika RUT955 — `192.168.1.254` |
| Firmware | `RUT9XX_R_00.06.09.5` |
| Package | SNMP — installed |
| Gate | B — read-only boundary verification |
| Stato | **NO-GO — read-only boundary not demonstrable on current legacy WebUI** |
| Data | 2026-08-26 |

## 1. Runtime evidence after package installation

Observed configuration immediately after installing the SNMP package:

```text
Package SNMP          : Installed
SNMP service          : Disabled
Remote access         : Disabled
Port                  : 161
SNMP version selector : reported by operator as `v1/v1/v3`
Community             : present
SNMPv3 user fields    : not visible
Authentication fields : not visible
Privacy fields        : not visible
Trap host/IP field    : present
Trap port             : 162
Trap community field  : present
Trap rules            : none
```

The reported version label `v1/v1/v3` is preserved as operator evidence and is not normalized by inference. Vendor documentation for the same legacy firmware documents the available selector values as `v1/v2`, `v1/v2/v3`, or `v3`.

No secret value is required for this evidence and none is recorded in this file.

## 2. Vendor evidence

For `RUT9XX_R_00.06.09.5`, Teltonika's legacy SNMP documentation describes:

- `Enable SNMP service`;
- `Enable remote access`;
- port 161;
- community selection;
- version selection including v3;
- trap configuration.

The legacy page does **not** document per-user SNMPv3 configuration, authentication/privacy controls, or an `Access Mode = Read-Only` control.

By contrast, the newer RUT955 SNMP documentation for later firmware explicitly documents SNMPv3 users and `Access Mode = Read-Only | Read-Write`.

This difference is material to BKL-027 because the project requires a technically verifiable read-only boundary and does not accept an assumption that the legacy agent rejects `SET` operations.

## 3. Gate B decision

**NO-GO for runtime enablement on the current legacy configuration.**

Reason:

1. the installed package is real and available;
2. SNMP service remains disabled;
3. Remote Access remains disabled;
4. the current WebUI does not expose a read-only user/access-mode boundary;
5. no write test is authorized on the production router;
6. therefore non-writability cannot be proven safely.

## 4. Required runtime state after NO-GO

```text
SNMP service      = Disabled
Remote Access     = Disabled
SNMP traps        = Not configured
systems.network   = UNKNOWN
```

No SNMP collector installation on `EAGLE30154` is authorized under this Gate B result because the source itself has not passed the read-only boundary requirement.

## 5. Next architecture options

BKL-027 may proceed only through a separate governed decision. Candidate options, in priority order:

1. vendor-confirmed method to enforce read-only behavior on this exact legacy firmware/package;
2. firmware upgrade/change package that exposes an explicit read-only access mode, subject to an independent network-change assessment and rollback plan;
3. alternative external/passive network telemetry source that does not require a write-capable management protocol;
4. maintain `systems.network = UNKNOWN` if no safe source is available.

A firmware upgrade is **not authorized by this Gate B document**.

## 6. Safety and security disposition

- no WAN exposure introduced;
- no SNMP service enabled;
- no trap configured;
- no SNMP `SET` test executed;
- no WAN/failover/SIM/VPN configuration changed;
- local observatory safety remains independent;
- telemetry remains fail-safe `UNKNOWN`.
