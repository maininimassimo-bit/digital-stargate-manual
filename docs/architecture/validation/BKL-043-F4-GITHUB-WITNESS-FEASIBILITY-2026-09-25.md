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

On 2026-09-26 Massimo Mainini stated a preference for Cloud Run as the
independent receiver candidate. This supersedes GitHub Actions as the preferred
missing-receipt detection mechanism; it does not authorize a Cloud Run service,
resource, network path, or spend. GitHub may still be considered separately as
an archive, but that role is not selected here. This assessment distinguishes
durable receipt storage from timely independent detection of missing receipts.
Those are separate capabilities.

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
6. Cloud Run is the owner's preferred receiver candidate, but the service alone
   does not define durable receipt history or prove a bounded receipt-time
   contract. The receiver design must specify write-before-ack persistence,
   receiver timestamps, availability and cold-start behavior, retry/idempotency,
   and the failure domains of the receiver, storage, and EAGLE's outbound path.
   Any provider SLA or cost assumption must be verified against the exact future
   service configuration and account; none is accepted by this preference.

## Disposition

**Owner preference recorded: Cloud Run as the independent receiver candidate.**
This is a planning choice, not a selected service configuration or an accepted
time-bounded witness. The F4 runtime authorization cannot claim bounded
missing-heartbeat detection until the exact receiver, durable receipt store,
receipt-time contract, failure domains, availability assumptions and unknown-gap
behavior have been reviewed. Cloud Run scale-to-zero/cold-start behavior,
receiver or storage unavailability, network loss, retries, or uncertain
timestamps must leave affected coverage `UNKNOWN` unless a later exact contract
establishes a defensible bound.

GitHub Actions is not accepted as the independent liveness witness because its
scheduled runs may be delayed or dropped. GitHub may be evaluated as a separate
archive only after its exact private resource, access, retention and cost are
reviewed; the public manual repository remains excluded from pilot data.

The Cloud Run preference authorizes no project or service creation, workflow
activation, credential provisioning, EAGLE access, network transmission, data
persistence, deployment, or runtime pilot. Raw N.I.N.A. logs, secrets, personal
information, private local paths and arbitrary command output remain prohibited
from receipts.

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

Leonardo Di Egidio must review the updated feasibility assessment and record
findings. The exact runtime authorization must still specify the Cloud Run
service shape and region, receiver and durable-store contract, identity,
transport, cadence, unknown-gap rule, source list, retention, resource and cost
ceilings, billing owner, observation window, installation/rollback and OAT.
Any GitHub archive remains a separate, unselected decision. The recorder and
historical-log authorizations documented in the shutdown/reconciliation draft
remain separate from this witness preference.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```
