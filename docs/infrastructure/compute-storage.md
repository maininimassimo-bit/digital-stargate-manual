# Compute and Storage

## Compute

The primary observatory compute node hosts the control software, automation services, device drivers and acquisition workflows.

Core responsibilities include:

- NINA orchestration;
- ASCOM device integration;
- mount control;
- camera and focuser control;
- guiding support;
- local telemetry and logging;
- acquisition staging.

## Storage tiers

| Tier | Purpose | Retention expectation |
|---|---|---|
| Acquisition | Raw files generated during observing sessions | Immediate operational retention |
| Staging | Files awaiting validation, transfer or processing | Short-term |
| Archive | Curated scientific and operational data | Long-term |
| Backup | Configuration, documentation and recovery artifacts | Policy-driven |

## Capacity safeguards

The automation layer must prevent new imaging sessions when the available storage falls below the configured safety threshold.

Required controls:

- free-space monitoring;
- session-level capacity estimation;
- log rotation;
- archival transfer verification;
- controlled cleanup procedures.
