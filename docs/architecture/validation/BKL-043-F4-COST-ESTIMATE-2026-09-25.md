# BKL-043 F4 — Preliminary Cost Estimate

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F4-COST-ESTIMATE-2026-09-25` |
| Gate | `M-BKL043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION` |
| Status | Indicative estimate only; no provider, resource, spending limit or runtime activity authorized |
| Owner / accountable | Massimo Mainini |
| Currency / price basis | USD list rates reviewed 2026-09-25; taxes, exchange-rate effects and account-specific discounts excluded |

## Purpose and limits

This is an order-of-magnitude comparison to inform the exact pilot decision. It
does not select an exact hosting configuration, create resources, authorize
charges, or replace the provider pricing calculator and billing-account review.
On 2026-09-26 Massimo Mainini stated a preference for Cloud Run as the receiver
candidate; this does not select its scaling mode, region, storage, or billing
configuration. On 2026-09-26 he selected one receipt per minute as a design
cadence, matching the illustrative workload below; this does not authorize a
schedule or runtime activity. The cadence implementation, payload size, region,
logs, retention, storage volume, egress, implementation shape, account plan and
remaining free quotas are not known; owner-selected local outbox retries and
backfill may also create catch-up request bursts after network recovery. Actual
costs can therefore be higher or lower. No charge ceiling has been approved.

## Indicative monthly scenarios

| Scenario | Workload assumptions | Indicative recurring cost | Important limitation |
|---|---|---|---|
| GitHub Actions scheduled check | Private repository; every 5 minutes for 30 days; one Linux 2-core hosted job billed as one minute per run (8,640 runs/minutes) | $51.84 gross at $0.006/minute. If all 2,000 GitHub Free minutes remain unused: about $39.84 incremental; if none remain: up to $51.84. Artifact/storage overages are additional. | **Not suitable as a bounded-latency witness:** scheduled runs may be delayed or dropped. This is only a best-effort archive/check scenario, not a recommendation. Actual billed duration rounds to runner billing units and should be verified against the account. |
| Cloud Run request-based receiver, scale to zero | One lightweight request/minute (43,200/month), 0.167 vCPU, 256 MiB RAM, 100 ms processing/request; no minimum instances | Illustratively, about 721 vCPU-seconds, 1,080 GiB-seconds and 43,200 requests. These are below the published request-based free allowances (180,000 vCPU-seconds, 360,000 GiB-seconds, 2 million requests/month), **if the billing account has those quotas unused**. Not a guaranteed $0 bill. | Add durable storage, logging, networking/egress, image builds/artifact storage, monitoring, and other account usage. Cold starts and service availability still need a separately reviewed receipt-time contract. |
| Same Cloud Run receiver with one minimum warm instance | Above request workload plus one continuously configured minimum instance at 1 vCPU / 256 MiB for a 30-day month | Rough idle list-rate arithmetic: 2,592,000 seconds × ($0.0000025/vCPU-s + 0.25 × $0.0000025/GiB-s) = **about $8.10/month** idle compute, before active requests and other products. This is not a quote and free-tier treatment/account discounts must be checked in the calculator. | Keeping an instance warm does not itself create an availability or latency SLA. Minimum-instance configuration and its cost would require explicit approval. |
| Cloud Storage receipt objects (single-region Standard, flat namespace) | One new receipt object/minute, 43,200 Class A writes/month; illustrative European single region such as Milan | At $0.005 per 1,000 Class A operations: **about $0.22/month** for those writes. Data storage at $0.000027397/GiB-hour is about $0.02/GiB for 30 days. Reads, listing, metadata operations, retention/versioning and transfer add cost. | Simplified object-per-receipt model only; actual API/client behavior can issue multiple operations. The published always-free Cloud Storage allowance does not apply to European regions. |

As a rough combination only, scale-to-zero Cloud Run plus the modeled writes
could be around $0.22/month plus stored data and other charges if all relevant
Cloud Run free quotas are available. With one continuously warm minimum
instance, the same simplified model is around $8.32/month plus stored data and
other charges. Neither figure is a bill estimate or cost cap.

## One-time and non-cloud effort

Implementation, offline/owner-witnessed OAT, security/privacy review, Leonardo
Di Egidio's independent review, owner review, operational runbook and rollback
work are not priced here. They are human effort, not included in the cloud
figures. A credible person-day or labor-cost estimate needs the final design,
scope and applicable internal rates; none is supplied, so no monetary value is
invented.

## Exclusions and controls required before any runtime approval

- Existing Cloud Run relay reuse is not assumed; it currently does not provide
  the durable receipt ledger required by this candidate design.
- Excluded from the figures: engineering and review labor, logging/metrics
  ingestion and retention, network egress, secrets/identity products,
  repository plan charges, build and image storage, backup/replication,
  support, taxes, currency conversion and account-wide quota consumption.
- Confirm the paying account/project, billing region, account plan and remaining
  quota. Apply provider budgets/alerts and review hard-stop behavior; alerts
  alone are not authorization or a guaranteed spend cap.
- Before runtime authorization, Massimo must set an explicit monthly ceiling,
  any one-time ceiling, billing owner, allowed products/region, and stop action
  if the ceiling or a resource limit is reached. Those fields remain
  **UNSELECTED**. No procurement, resource creation or charge is authorized by
  this estimate.

## Sources

- [GitHub Docs — GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions): plan allowances, Linux runner rate and storage overage rates. Reviewed 2026-09-25.
- [GitHub Docs — workflow trigger events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): scheduled workflow cadence and delay/drop caveats. Reviewed 2026-09-25.
- [Google Cloud — Cloud Run pricing](https://cloud.google.com/run/pricing): request/instance rates, billing modes and aggregated free-tier notes. Reviewed 2026-09-25.
- [Google Cloud — Cloud Storage pricing](https://cloud.google.com/storage/pricing): regional storage and operation rates. Reviewed 2026-09-25.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```
