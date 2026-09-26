# Architecture Review Board — BKL-043 F4 Cloud Run receiver design

| Field | Value |
|---|---|
| Review ID | `ARB-BKL043-F4-CLOUD-RUN-RECEIVER-AI-001` |
| Review mode | AI-assisted, process-separated under `DSG-AEM-001`; not independent human approval |
| Date | 2026-09-26 |
| Technical head reviewed | `652f5c56fbe5cc29e1245f21350cb958b512685d` |
| Base | `b91d21257c1549c0ea227ce49f4c0bea3cf9a3c7` |
| Decision | **APPROVED for design preparation only, with open decisions** |

## Scope and evidence boundary

Reviewed the Cloud Run receiver design draft, its authorization-draft reference,
and decision-log entry at the exact head above. This is a repository and public
documentation review only. No Google Cloud account, deployed service, EAGLE
host, Windows/N.I.N.A. log, credential, or real telemetry was accessed.
The package does not create resources, send traffic, deploy, poll, or spend.

## Architecture findings

The proposed receiver is properly separated from the EAGLE host and its power
domain. It acknowledges only after a durable write, limits the ingest envelope,
and preserves source and receiver time separately. It does not grant command,
execution, remediation, or safety authority. The draft correctly distinguishes
receipt gaps from host failure, planned shutdown, observatory availability,
and scientific activity; the absence of a receipt remains `UNKNOWN` absent
independent evidence or human review.

Cloud Run scale-to-zero and warm-instance trade-offs are presented without a
false hard-latency claim. The monthly Cloud Run SLA is not treated as a
per-receipt guarantee. Storage create preconditions are not mislabeled as
immutability, and irreversible Bucket Lock is not the default. Keyless identity
is conditional on source capability; no service-account key is proposed.

The receiver is not itself a missing-heartbeat detector. Any bounded alert
objective needs a separate evaluator, schedule, failure model, identity, cost
and review. Existing snapshot-relay evidence does not satisfy an append-only
receipt ledger contract. These are sound separation and scope controls.

## Findings and conditions

### Blocker / Major

None for repository-only design preparation.

### Open items before exact runtime authorization

- `ARB-043-F4-CR01` — Purpose and any bounded missing-heartbeat/alert objective
  remain undecided; receipt archive plus offline gap reporting is the bounded
  current proposal.
- `ARB-043-F4-CR02` — Exact project, region, ingress, authentication, identity
  prerequisites, limits, transport, cadence, source clock/sequence rules and
  retry/outbox contract remain unselected.
- `ARB-043-F4-CR03` — Storage location, replication, retention/deletion,
  report-reader identity, recovery and exact IAM permissions require owner and
  security/privacy review.
- `ARB-043-F4-CR04` — Cost inputs and monthly/one-time ceilings, stop action,
  and billing owner remain open; existing estimate is indicative only.
- `ARB-043-F4-CR05` — Leonardo Di Egidio's review of this exact design and a
  runtime-specific security/privacy review have not been evidenced. AI review
  does not substitute for either.
- `ARB-043-F4-CR06` — Separate owner approvals for local shutdown recording
  and any real historical log snapshot/reconciliation remain outstanding.

These conditions block exact-runtime authorization and any reliability claim,
but do not block integrating a clearly labeled design draft.

## Authority and disposition

No command path, broker, decision scheduler, automatic remediation, or Safety
Authority is changed. The package preserves:

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

**APPROVED for design preparation only.** Proceed to a process-separated Release
Quality review for documentation publication. Do not treat this review as
approval to create a Cloud Run service, configure billing, send requests, access
EAGLE, read/import real logs, install a local recorder, or begin runtime/OAT.
