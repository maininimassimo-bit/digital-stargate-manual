# BKL-043 F3 — Read-only Pilot Readiness and Authorization Gate

| Field | Value |
|---|---|
| Gate ID | `M-BKL043-F3-READONLY-PILOT-READINESS` |
| Status | Owner approved preparation of a separate exact pilot authorization on 2026-09-24; F3 review findings and runtime authorization remain open |
| Package | BKL-043 Observatory Reliability Engineering |
| Owner / accountable | Massimo Mainini |
| Entry baseline | BKL-043 F2 two-plane logical architecture, owner-approved 2026-09-24 |
| Authority | Repository-only design; command/execution/safety `NONE` |

## Purpose

Convert the accepted F2 logical design into a reviewable, bounded pilot
specification and a separate exact authorization decision. F3 does not run the
pilot. It identifies what must be proven, what decisions remain open, and how a
later pilot can be authorized without silently activating persistent collection
or changing observatory behavior.

The F2 approval accepts the architecture target only. It does not select a host,
service, witness provider, transport, cadence, retention period, data store,
production source, or deployment. It does not authorize access to EAGLE, N.I.N.A.,
the relay, or any other live system.

## Scope and non-goals

F3 may use committed documents, contracts, schemas, source code, synthetic
fixtures, and offline tests. It may document alternatives and propose exact
pilot values for later review. It must not test those proposals against live
hardware, logs, services, credentials, networks, or current telemetry.

F3 does not authorize or perform:

- a local collector, service, scheduled task, boot trigger, recurring polling,
  or persistent observation / incident writer;
- live source access, device/network probes, remote heartbeat transmission,
  or modifications to the telemetry relay or its deployment;
- creation or population of an authoritative incident register;
- alerts, remediation, scheduler decisions, commands, interlock changes,
  readiness decisions, or Safety Authority;
- numeric SLI/SLO targets or MTBF/MTTR claims.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

## Required design package

The F3 review candidate must include:

1. **Source and boundary matrix.** Exact proposed component, source owner,
   existing read-only contract, evidence age, provenance fields, failure domain,
   and behavior when the source is stale, absent, conflicting, or unreachable.
   Repository schemas do not prove a current producer. Historical commissioning
   settings must not be generalized into new cadence or freshness values.
2. **Two-plane pilot topology.** Local observer and journal, independent witness
   and durable receipt journal, incident lifecycle, trust boundaries, data flows,
   and explicit no-control-path invariant. Identify which plane is intentionally
   omitted if it cannot be separately authorized; report resulting coverage as
   incomplete rather than whole-system.
3. **Data and privacy contract.** Minimum record fields, stable identity,
   idempotency/replay behavior, UTC and clock-quality handling, allowed payloads,
   secret exclusion, access controls, backup/export, retention alternatives and
   disposal decision owner. Do not copy raw N.I.N.A. logs or personal data into
   telemetry records.
4. **Offline validation plan.** Synthetic tests for current/stale/missing and
   conflicting source values; duplicate/reordered receipts; clock drift/jump;
   host restart; EAGLE offline; network partition; witness outage; journal
   corruption/disk-full; replay/reconciliation; and human-confirmed
   acknowledge/restore/reopen transitions. Tests must show unknown is never
   converted to healthy and that no incident closes automatically.
5. **Non-interference and rollback.** Proposed resource budget and measurement
   method for CPU, memory, disk, and network; least-privilege identity; install,
   stop, uninstall, rollback, backup, and recovery procedure. No numeric budget
   is accepted until explicitly reviewed for the selected target.
6. **Coverage-qualified reporting.** Component-level coverage intervals,
   unknown-gap display, bounded missing-heartbeat interval semantics, and
   report language. No system-wide scalar, failure cause, exact onset, MTBF,
   MTTR, SLO, or availability percentage may be implied without an approved
   population and sufficient validated evidence.
7. **Decision record.** Separate dispositions for architecture/security/privacy
   and release quality, plus a human owner decision naming the exact target,
   sources, access mode, cadence, retention, transport, deployment, rollback,
   observation window, and stop conditions before any runtime action.

## Evidence constraints carried forward

- The committed public EAGLE projection is `UNKNOWN/UNAVAILABLE` with no current
  snapshot; it is not a current health source.
- BKL-030 G5/G6 evidence is a manual, bounded OAT and one persistence cycle;
  there is no approved permanent recurring writer.
- N.I.N.A. runtime telemetry commissioning records are historical. The producer's
  source-specific settings are not approval for a new detector cadence.
- Repository N.I.N.A. logs are not a complete planned-session or incident
  register; the accepted attempt definition remains N.I.N.A.-logged activity
  only, with unvalidated grouping/outcome semantics.
- The current relay is a latest-snapshot path, not evidence of durable witness
  or incident history.
- No incident register is present; OPSC-ALM-001 remains a draft.

## Exit criteria

F3 may exit with a **pilot specification ready for decision** only when the
design package above is internally consistent, synthetic/offline cases are
reproducible, limitations and unmade decisions are explicit, and review findings
are recorded. Owner disposition may be `APPROVED FOR A SEPARATE EXACT PILOT
AUTHORIZATION`, `APPROVED WITH CONDITIONS`, or `RETURNED`; none by itself
activates runtime work unless it names the exact authorized change.

Massimo Mainini selected `APPROVED FOR A SEPARATE EXACT PILOT AUTHORIZATION`
on 2026-09-24. This permits preparation of the distinct F4 authorization draft
only. F3 review findings remain open, and no runtime parameter or operation is
approved. See `BKL-043-F3-EXACT-PILOT-AUTHORIZATION-DECISION-2026-09-24.md`
and `BKL-043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION-DRAFT-2026-09-24.md`.

Any local observer pilot, durable witness, incident journal, live source read,
scheduled/boot execution, recurring write, hosted relay change, or deployment
must be a separately scoped runtime gate with explicit owner authorization and
its own preflight, OAT, rollback, and post-change verification. A rejection or
absence of an independent witness narrows the scope to locally observed
component telemetry; it must not be called whole-system reliability.

## References

- `docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-POPULATION-AND-CONTRACT-GAP-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F2-DETECTION-ARCHITECTURE-GATE-2026-09-24.md`
- `docs/architecture/telemetry/BKL-030-G6-EAGLE-Health-History-Persistence-Design.md`
- `docs/architecture/telemetry/evidence/BKL-030-G5-Runtime-OAT-2026-09-03.md`
- `docs/architecture/telemetry/evidence/BKL-030-G6-Runtime-OAT-2026-09-04.md`
- `docs/architecture/packages/AP-004-Enterprise-Telemetry-and-Observability-Architecture.md`
- `docs/architecture/packages/AP-007-Enterprise-Operations-and-Service-Management-Architecture.md`
- `docs/architecture/alarm-and-incident-model.md` (OPSC-ALM-001 draft)
