# PLAT-OBS-001 — Platform Contracts

## 1. Purpose

This contract set defines the stable technical interfaces used by the Observation Automation Platform. It converts the platform architecture into implementation-ready rules for APIs, events, telemetry, configuration, errors and security.

## 2. Contract domains

- REST resource contracts;
- event envelope and event taxonomy;
- telemetry and health reporting;
- configuration and policy exchange;
- error representation and recovery metadata;
- authentication, authorization and audit context;
- shared JSON schemas;
- end-to-end operational sequences.

## 3. Design principles

1. Contracts are versioned independently from implementations.
2. Safety decisions remain authoritative and cannot be bypassed by orchestration clients.
3. All commands are idempotent where operationally possible.
4. Every request, event and log entry carries a correlation identifier.
5. Device-specific details are isolated behind adapters.
6. Breaking changes require a new major contract version.

## 4. Documents

- [API Governance](api-governance.md)
- [REST API Contract](rest-api.md)
- [Event Contracts](event-contracts.md)
- [Telemetry Contracts](telemetry-contracts.md)
- [Configuration Contracts](configuration-contracts.md)
- [Error Contracts](error-contracts.md)
- [Security Contracts](security-contracts.md)

## 5. Shared schemas

- `event-envelope.schema.json`
- `observation-session.schema.json`
- `safety-state.schema.json`
- `weather-state.schema.json`
- `problem-details.schema.json`

## 6. Status

| Attribute | Value |
|---|---|
| Platform | PLAT-OBS-001 |
| Contract version | 1.0.0-draft |
| Status | Draft |
| Compatibility target | SOL-OSM-001 |
