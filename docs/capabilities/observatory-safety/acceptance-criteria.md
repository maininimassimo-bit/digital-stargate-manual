# CAP-SAF-001 - Acceptance Criteria

## Purpose

Acceptance criteria define measurable governance conditions for accepting Observatory Safety as implementation-ready documentation.

## Criteria

| ID | Criterion | Verification |
|---|---|---|
| `SAF-ACC-001` | Overview defines purpose, business value, scope, stakeholders, dependencies, lifecycle and success criteria. | Review `index.md`. |
| `SAF-ACC-002` | Business process covers monitoring, policy evaluation, risk assessment, operational decision, emergency, recovery, audit and reporting. | Review `business-process.md`. |
| `SAF-ACC-003` | Safety state model includes Unknown, Safe, Warning, Unsafe, Emergency, Recovery, Maintenance and Disabled. | Review `index.md`. |
| `SAF-ACC-004` | Safety inputs include Weather, Session, Equipment, Scheduling, Target, Operator, Maintenance, Power, Roof and Communications. | Review `data-model.md`. |
| `SAF-ACC-005` | Safety outputs include Allow, Suspend, Abort, Close Roof Request, Safe Mode, Recovery Allowed, Operator Notification and Audit Event. | Review `data-model.md`. |
| `SAF-ACC-006` | Requirements include 32 unique `SAF-*` identifiers across required categories. | Review `requirements.md`. |
| `SAF-ACC-007` | Data model remains conceptual and avoids physical implementation. | Review `data-model.md`. |
| `SAF-ACC-008` | Architecture mapping references all existing Core Observatory capability packages, `DOM-001`, `EA-000` and Knowledge Framework. | Review `architecture-mapping.md`. |
| `SAF-ACC-009` | ADRs define Safety Authority and Fail-Safe Behaviour without duplicating enterprise decisions. | Review ADR folder. |
| `SAF-ACC-010` | SOPs exist for Evaluate Safety, Enter Safe Mode, Resume Operations and Emergency Shutdown. | Review SOP folder. |
| `SAF-ACC-011` | Runbooks exist for Emergency Stop, Roof Unsafe, Communications Lost and Power Failure. | Review runbooks folder. |
| `SAF-ACC-012` | Technical manual documents responsibilities, interfaces, dependencies, inputs, outputs, operational considerations and safety principles. | Review `technical-manual.md`. |
| `SAF-ACC-013` | Test plan covers safety rules, emergency, recovery, decision consistency and acceptance tests. | Review `test-plan.md`. |
| `SAF-ACC-014` | Traceability maps artefacts to Roadmap, DSRA, EA-000, Knowledge Framework, DOM-001, REV-001, CAP-000, REL-000 and Core Observatory packages. | Review `traceability.md`. |
| `SAF-ACC-015` | CAP-000 registers `CAP-SAF-001` as Documented / Implementation Ready / version 0.1. | Review `CAP-000`. |
| `SAF-ACC-016` | DOM-001 includes `CAP-SAF-001` and removes it from Future Evolution. | Review `DOM-001`. |
| `SAF-ACC-017` | REV-001 readiness decision is reassessed with Safety package evidence. | Review `REV-001`. |
| `SAF-ACC-018` | MkDocs navigation includes Observatory Safety package pages. | Review `mkdocs.yml`. |

## Non-Acceptance Conditions

The package is not acceptable if it:

- defines hardware implementation or PLC logic;
- introduces software code, API, database, frontend or backend design;
- modifies Roadmap, DSRA or Enterprise Architecture baseline;
- treats Unknown or Disabled as Safe;
- omits traceability to REV-001 and existing Core Observatory packages.

## Acceptance Status

| Field | Value |
|---|---|
| Documentation readiness | Ready after validation |
| Implementation readiness | Implementation Ready after CAP-000, DOM-001 and REV-001 synchronization |
| Operational readiness | Not claimed |
| Open decisions | Safety rule priority, policy versioning, decision freshness, override policy, audit retention |
