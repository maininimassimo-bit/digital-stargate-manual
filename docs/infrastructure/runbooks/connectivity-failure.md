# Runbook — Connectivity Failure

## Trigger

Loss of primary WAN connectivity or inability to reach the observatory remotely.

## Procedure

1. verify whether Starlink is unavailable;
2. confirm RUT955 power and LTE registration;
3. verify activation of SIM 1, then SIM 2 if required;
4. test VPN reachability;
5. confirm local automation remains active;
6. avoid unnecessary remote restarts during an active safety event;
7. record the failure and recovery path.

## Escalation

Escalate when all WAN paths are unavailable or when local automation status cannot be confirmed.
