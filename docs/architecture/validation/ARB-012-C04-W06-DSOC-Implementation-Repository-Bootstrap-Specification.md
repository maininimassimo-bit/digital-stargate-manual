# ARB-012-C04 W06 — DSOC Implementation Repository Bootstrap Specification

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-06 |
| Work item | C04-W06 — Validation Environment Provisioning and Account Setup |
| Status | Proposed bootstrap specification — repository not yet created |
| Date | 2026-07-31 |
| Tracking issue | #29 |
| Runtime effect | None |

## 1. Purpose

This specification defines the minimum repository contract required to establish an authoritative, immutable and non-production DSOC implementation baseline for C04-W06.

It does not create the repository, deploy software, enable runtime commands, connect to physical observatory devices or assert that any validation control has passed.

## 2. Proposed repository identity

| Attribute | Proposed value |
|---|---|
| Owner | `maininimassimo-bit` |
| Repository | `DigitalStarGate.Control` |
| Full name | `maininimassimo-bit/DigitalStarGate.Control` |
| Visibility | Private |
| Default branch | `main` |
| Primary purpose | DSOC application, approval workflow, authorization policy, simulator adapters and validation fixtures |
| Excluded purpose | Reporting ingestion, operational log publication and analytics already assigned to `DigitalStarGate.Reporting` |

The repository name remains proposed until the repository is actually created and recorded in issue #29.

## 3. Architectural scope

The implementation repository shall own the code and tests for the DSOC control plane required by ARB-012-C04, including:

- command request submission;
- authorization evaluation;
- four-eyes approval enforcement;
- self-approval prevention;
- approval expiry and revocation;
- immutable audit recording;
- simulator-only execution adapters;
- deterministic validation fixtures;
- health, diagnostics and correlation identifiers.

The repository shall not contain production credentials, VPN secrets, physical-device addresses, break-glass credentials or procedures that bypass local safety interlocks.

## 4. Layer boundaries

The initial solution structure shall preserve the following dependencies:

```text
Presentation -> Application -> Domain
Infrastructure -> Application
Persistence -> Application
Simulators -> Application ports
Domain -> no framework, infrastructure, persistence or external-system dependencies
```

Minimum logical projects or top-level modules:

```text
src/
  DigitalStarGate.Control.Domain/
  DigitalStarGate.Control.Application/
  DigitalStarGate.Control.Contracts/
  DigitalStarGate.Control.Infrastructure/
  DigitalStarGate.Control.Persistence/
  DigitalStarGate.Control.Api/
  DigitalStarGate.Control.Simulators/
tests/
  DigitalStarGate.Control.Domain.Tests/
  DigitalStarGate.Control.Application.Tests/
  DigitalStarGate.Control.Architecture.Tests/
  DigitalStarGate.Control.IntegrationTests/
  DigitalStarGate.Control.AcceptanceTests/
validation/
  fixtures/
  environments/
  evidence-templates/
docs/
  architecture/
  runbooks/
```

Equivalent language-specific naming is acceptable only if the same dependency rules and ownership boundaries remain explicit.

## 5. Mandatory bootstrap files

The first immutable baseline shall include:

- `README.md`;
- `LICENSE` or explicit private/proprietary notice;
- `.gitignore`;
- dependency and build manifest;
- `SECURITY.md`;
- `CONTRIBUTING.md`;
- `CODEOWNERS`;
- architecture dependency test configuration;
- CI workflow for build, unit tests, architecture tests and secret scanning;
- non-production configuration template containing no secrets;
- simulator manifest;
- fixture manifest with checksums;
- validation evidence template;
- repository-specific ADR or architecture note documenting layer boundaries.

## 6. Non-production baseline contract

The repository shall expose an explicit validation configuration that:

- resolves every external observatory dependency to a simulator or inert stub;
- refuses production hostnames, IP ranges, VPN routes and credentials;
- defaults command execution to disabled;
- enables no physical-device control;
- records audit events locally in the isolated validation environment;
- supports deterministic reset between validation runs;
- carries a stable identifier and SHA-256 checksum.

Suggested identifier format:

`DSOC-VAL-CONFIG-YYYYMMDD-NN`

## 7. Simulator and fixture contract

The baseline shall identify:

- simulator source commit or package version;
- supported device and workflow scenarios;
- deterministic seed or reset procedure;
- canonical fixture bundle version;
- SHA-256 checksums for simulator package and fixture manifest;
- expected negative cases for self-approval, expired approval, revoked approval and unauthorized command execution.

No simulator may silently fall back to a physical adapter.

## 8. Initial CI quality gates

Before the repository can satisfy issue #29, its initial commit shall demonstrate through an executed CI run:

1. source checkout succeeds;
2. dependency restore succeeds;
3. build succeeds;
4. unit tests execute;
5. architecture dependency tests execute;
6. secret scanning executes;
7. non-production configuration validation executes;
8. simulator-only adapter validation executes;
9. fixture checksum validation executes;
10. generated artifacts contain no credentials or production endpoints.

A configured but unexecuted workflow is not evidence of success.

## 9. Immutable baseline record

When the repository exists, issue #29 and the W06 provisioning record shall capture:

| Field | Required value |
|---|---|
| Repository | Exact full repository name |
| Component | Exact service/application under validation |
| Default branch | Exact branch name |
| Commit | Full immutable commit SHA |
| CI run | Workflow name, run number and conclusion |
| Configuration | Identifier and SHA-256 checksum |
| Simulator | Version or commit SHA and checksum |
| Fixtures | Bundle identifier and checksum |
| Runtime mode | Simulator-only, command execution disabled by default |
| Production dependency check | Confirmed absent, with evidence reference |

## 10. Acceptance criteria

This bootstrap specification is satisfied only when:

- the repository exists and is accessible through the connected GitHub installation;
- its purpose and ownership are explicit;
- the initial implementation baseline is committed;
- a successful CI run is verified;
- the full commit SHA and all configuration, simulator and fixture identifiers are recorded;
- no secret or production endpoint is present;
- the W06 provisioning record is updated;
- issue #29 can be closed with repository evidence.

## 11. Restrictions

Until all acceptance criteria are met:

- C04-W06 remains `IN PROGRESS`;
- C04-W07 remains blocked;
- ENV-003 and ENV-011 remain `Not Executed`;
- DSOC runtime enablement is prohibited;
- physical-device control is prohibited;
- production access is prohibited;
- positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.

## 12. Next authorized action

Create the private repository `maininimassimo-bit/DigitalStarGate.Control` through GitHub, grant the connected GitHub application access, and initialize it with the mandatory bootstrap files and simulator-only safety defaults defined above.
