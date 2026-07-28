# Infrastructure Architecture

## Architectural principles

The Digital StarGate infrastructure follows these principles:

1. safety takes precedence over observation continuity;
2. remote operation must remain observable and reversible;
3. critical functions must tolerate loss of the primary Internet path;
4. infrastructure failures must degrade gracefully;
5. configuration and recovery procedures must be documented and testable.

## Logical layers

```text
Remote Operator
      |
Secure VPN Access
      |
Connectivity Layer
Starlink / LTE / LAN
      |
Observatory Compute
EAGLE3 and device services
      |
Automation and Control
      |
Observatory Assets
      |
Scientific Data Storage
```

## Main dependencies

The automation platform depends on:

- local compute availability;
- LAN connectivity;
- device drivers and control services;
- stable power;
- safety telemetry;
- sufficient storage capacity.

Loss of public Internet access must not prevent local safety shutdown actions.
