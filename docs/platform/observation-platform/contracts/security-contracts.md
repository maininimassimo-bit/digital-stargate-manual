# Security Contracts

## 1. Trust boundaries

The platform distinguishes:

- remote operator clients;
- local platform services;
- independent safety controller;
- device adapters;
- external applications and vendor software.

## 2. Authentication

Remote API access requires authenticated identities. Service-to-service calls use workload identities or mutually authenticated transport where supported.

## 3. Authorization roles

| Role | Typical permissions |
|---|---|
| Observer | Read state and manage owned session plans |
| Operator | Start, pause and stop sessions within policy |
| Maintainer | Execute maintenance commands and diagnostics |
| Safety Administrator | Manage approved safety policies |
| Platform Administrator | Manage platform configuration and identities |
| Auditor | Read logs, events and configuration history |

## 4. Safety enforcement

Authorization does not override physical safety. The independent safety authority can deny or interrupt commands regardless of caller role.

## 5. Audit context

Every state-changing request records:

- authenticated subject;
- effective role;
- source address or client identifier;
- requested operation;
- target resource;
- correlation identifier;
- policy decision;
- outcome and timestamp.

## 6. Secret handling

Secrets are stored outside documentation and configuration payloads. Documentation may contain secret references and rotation procedures but never live credentials, VPN keys, tokens or passwords.
