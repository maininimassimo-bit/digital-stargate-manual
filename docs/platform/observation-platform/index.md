# PLAT-OBS-001 — Observation Automation Platform

## 1. Overview

The Observation Automation Platform is the reusable software and runtime foundation that supports automated and remotely supervised astronomical observation sessions at Digital StarGate.

It translates the solution architecture defined by `SOL-OSM-001` into implementable platform services, adapters, policies and operational components.

## 2. Mission

The platform coordinates the complete observation lifecycle:

- session preparation;
- safety validation;
- observatory opening;
- equipment initialization;
- target acquisition;
- guiding and autofocus;
- image acquisition;
- telemetry and evidence collection;
- controlled shutdown and recovery.

## 3. Platform boundary

### Included

- orchestration services;
- safety supervision interfaces;
- device and application adapters;
- configuration and policy management;
- event and telemetry collection;
- notification and operational API;
- local runtime and recovery mechanisms.

### Excluded

- astrophotography image processing pipelines;
- long-term scientific archive governance;
- public portal and community services;
- generic enterprise identity management;
- vendor firmware internals.

## 4. Primary users

- observatory operator;
- remote administrator;
- automation maintainer;
- platform developer;
- technical reviewer.

## 5. Supported operational tools

The initial platform architecture assumes integration with the existing observatory ecosystem, including:

- N.I.N.A. for sequence execution;
- PHD2 for guiding;
- CPWI and ASCOM-compatible drivers for mount control;
- dome or roof controllers;
- weather and safety sensors;
- EAGLE3 or equivalent local control host;
- remote access and failover network services.

## 6. Architecture documents

- [Platform Overview](platform-overview.md)
- [Service Decomposition](service-decomposition.md)
- [Component Catalogue](component-catalogue.md)
- [Integration Architecture](integration-architecture.md)
- [Deployment Topology](deployment-topology.md)
- [Operational Model](operational-model.md)

## 7. Status

| Attribute | Value |
|---|---|
| Platform ID | PLAT-OBS-001 |
| Name | Observation Automation Platform |
| Status | Draft |
| Primary solution | SOL-OSM-001 |
| Deployment model | Local-first, remotely supervised |
| Safety model | Independent safety authority |
