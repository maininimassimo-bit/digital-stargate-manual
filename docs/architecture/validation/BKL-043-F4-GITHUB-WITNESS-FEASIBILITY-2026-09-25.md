# BKL-043 F4 — GitHub Witness Feasibility Assessment

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F4-GITHUB-WITNESS-FEASIBILITY-2026-09-25` |
| Gate | `M-BKL043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION` |
| Status | Repository-only feasibility assessment; no service or repository created |
| Owner / accountable | Massimo Mainini |
| Review nominee | Leonardo Di Egidio; review not yet performed |
| Authority | `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

## Decision question

Massimo selected GitHub as the preferred platform for the independent witness
plane. This assessment distinguishes durable receipt storage from timely
independent detection of missing receipts. Those are separate capabilities.

## Findings

1. GitHub Actions scheduled workflows have a documented minimum interval of
   once every five minutes. GitHub also warns scheduled starts can be delayed
   during high load and that some queued jobs can be dropped.
2. A workflow triggered by a repository event can process an event that arrived,
   but no event is generated when EAGLE is offline or cannot transmit. Such a
   trigger does not independently detect the absence of future receipts.
3. A scheduled GitHub workflow could inspect stored receipts on a best-effort
   basis, but its schedule does not provide a hard maximum detection latency.
   A delayed or skipped run must therefore produce `UNKNOWN`/unbounded gap, not
   an inferred exact outage time or a healthy interval.
4. A private repository might be used as an archival store only after its exact
   owner, visibility, permissions, append/immutability model, access identity,
   retention, recovery, and account/Actions billing are reviewed. The existing
   `maininimassimo-bit/digital-stargate-manual` repository is public and is
   excluded for pilot data.
5. GitHub Actions is not an always-on receiver. A private repository plus a
   scheduled workflow alone is not accepted as evidence of a durable remote
   receipt journal or bounded independent liveness monitor.

## Disposition

**GitHub remains a candidate receipt archive, not an accepted independent
time-bounded witness.** The F4 runtime authorization cannot claim an upper
bound for missing-heartbeat detection based solely on GitHub Actions scheduling.
Any skipped/delayed scheduled run, unavailable API, missing receipt or uncertain
receiver timestamp remains an unknown coverage interval.

The owner must choose one of these design dispositions before the exact runtime
record can be prepared:

- accept GitHub as best-effort receipt archive and explicitly accept that
  witness gaps have no guaranteed detection latency; or
- require a separate independent receiver with a documented availability and
  receipt-time contract, while GitHub remains archival storage only.

Neither choice authorizes repository creation, workflow activation, credential
provisioning, EAGLE access, network transmission, data persistence, deployment,
or a runtime pilot. If a future design uses a private repository, raw N.I.N.A.
logs, secrets, personal information, private local paths and arbitrary command
output remain prohibited from receipts.

## Evidence and sources

- [GitHub Docs — Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
  documents the five-minute minimum for `schedule`, possible high-load delays,
  possible dropped jobs, and the requirement that a scheduled workflow exist on
  the default branch. Reviewed 2026-09-25.
- [GitHub Docs — Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)
  describes event, schedule and manual workflow triggers, including
  `repository_dispatch`. Reviewed 2026-09-25.
- Repository visibility check: `maininimassimo-bit/digital-stargate-manual` is
  public (observed 2026-09-24); it is not a runtime telemetry destination.
- `docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`
  explains the independent-witness trust boundary and limits of missing-heartbeat
  evidence.
- `docs/architecture/validation/BKL-043-F3-PILOT-SPECIFICATION-DRAFT-2026-09-24.md`
  excludes the current latest-snapshot relay as durable receipt history without
  a separate gate.

## Required follow-up

Leonardo Di Egidio must review the feasibility assessment and record findings.
Massimo Mainini must select one of the two dispositions above. A separate
runtime authorization must still specify the exact private repository/service,
receiver contract, identity, transport, cadence, unknown-gap rule, source list,
retention, resource limits, observation window, installation/rollback and OAT.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```
