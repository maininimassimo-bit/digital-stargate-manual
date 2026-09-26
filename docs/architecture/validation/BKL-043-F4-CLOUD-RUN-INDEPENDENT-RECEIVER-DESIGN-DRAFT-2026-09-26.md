# BKL-043 F4 — Cloud Run Independent Receiver Design (Draft)

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F4-CLOUD-RUN-RECEIVER-DESIGN-DRAFT-2026-09-26` |
| Gate | `M-BKL043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION` |
| Status | Repository-only design draft; owner preference recorded; exact design, reviews and runtime authorization pending |
| Owner / accountable | Massimo Mainini |
| Authority | `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |
| Evidence boundary | Public documentation and repository evidence only; no cloud account inspection, resource creation, traffic, EAGLE access or real-log access |

## 1. Purpose and design boundary

On 2026-09-26 Massimo Mainini stated a preference for Cloud Run as the
independent receiver candidate. This draft turns that preference into a
reviewable logical design for minimal, durable EAGLE health receipts. It does
not select a Google Cloud project, region, service, identity, authentication
mechanism, exact storage policy, cost ceiling or runtime configuration. Massimo
Mainini selected a one-minute receipt cadence as a design direction on
2026-09-26; delivery implementation and runtime remain unapproved.

The receiver must remain outside the EAGLE host and its power domain. Its
internet path still depends on EAGLE's local network and upstream connectivity;
loss of that shared path cannot be distinguished from host power loss by a
missing receipt alone. Cloud Run and its receipt store also introduce their own
provider, project, region, identity and storage failure domains, which must be
documented before any reliability claim.

This draft does not authorize a service, bucket, secret, identity, network rule,
scheduled evaluator, alert, installation, data retention, billing change,
deployment or request from EAGLE. The existing hosted telemetry relay is not
silently reused: repository evidence describes latest-snapshot endpoints and
process-local counters, not the durable receipt ledger required for this
witness.

## 2. Recommended logical flow

```text
EAGLE local observer (future; separately authorized)
  -> minimal HTTPS receipt with source sequence and source-observed time
  -> Cloud Run HTTPS receiver (Cloud Run preference; configuration unselected)
  -> validate strict receipt envelope
  -> write immutable-by-application receipt object to private durable storage
  -> acknowledge only after durable write succeeds

Offline reporting (future, separately governed)
  -> reads receipt history using a separate read identity
  -> reports last receipt, coverage and uncertain gaps; never infers cause
```

The ingest service should expose only a receipt-ingest operation. It should
return no stored telemetry to a browser, have no command or remediation
endpoint, and accept no raw Windows or N.I.N.A. log bodies. Acknowledgement
means only that the receiver accepted and durably stored the receipt; it is not
an EAGLE health, observatory readiness, session-success or safety decision.

### 2.1 Receipt envelope candidate

The envelope should be allowlisted and bounded. Candidate fields are:

| Field | Purpose |
|---|---|
| `schema_version`, `record_kind`, `record_id` | Versioning and idempotent receipt identity. |
| `source_id`, `host_identity`, `boot_epoch_id`, `sequence_id` | Bind the receipt to its source and host epoch without accepting caller-selected authority. |
| `source_observed_at_utc`, `source_clock_quality` | Preserve what the local observer reports and its time quality. |
| `receiver_received_at_utc` | Timestamp assigned by the receiver on arrival; never replace the source timestamp with it. |
| `observation_state`, `quality_state`, `reason_codes` | Small, governed observation summary; no raw logs or arbitrary command output. |
| `payload_digest`, `producer_version`, `evidence_reference` | Integrity and parser/producer lineage without embedding private paths. |

Exact enum values, maximum payload size, sequence reset behavior, clock-skew
handling, late/duplicate/conflict policy, deadline handling and schema digest
remain unselected. The owner-selected design cadence is one receipt per minute;
after approximately two minutes without a received receipt, an offline report
may mark a candidate gap. This threshold identifies a possible data interval
only: it does not establish host failure, cause or planned shutdown, and it does
not authorize a real-time evaluator or alert. Exact interval bounds must retain
clock and delivery uncertainty. The source must not be allowed to set receiver
time, receiver identity, a planned/unplanned classification, an incident
outcome or a safety state.

## 3. Candidate Cloud Run and storage pattern

| Concern | Candidate design for review | Still unresolved |
|---|---|---|
| Receiver | One non-GPU Cloud Run HTTP service dedicated to minimal receipts. | Project, service name, region, ingress, concurrency, CPU/memory, request timeout, instance maximum and artifact digest. |
| Scaling and billing | Request-based billing and zero minimum instances is the low-idle-cost candidate. This accepts cold-start and variable request latency; it cannot be described as a hard per-receipt time bound. | Whether this latency is acceptable; minimum instances change idle cost but do not create a complete end-to-end receipt-time guarantee. Exact cost model and ceilings remain open. |
| Authentication | Owner-selected design direction (2026-09-26): prefer keyless Cloud Run IAM invocation through Workload Identity Federation, conditional on the EAGLE-side environment having a supported, governed identity provider. Never introduce a long-lived service-account key. | Capability is unverified and no live inspection is authorized by this draft. No identity, ingress or authentication is configured. If federation is unavailable, an application-level signed request remains an unselected fallback requiring separate threat, secret storage, rotation, replay and revocation review. |
| Receipt storage | Owner-selected direction (2026-09-26): private Cloud Storage in a single region, with one small object per accepted receipt and a 90-day retention horizon. Use a unique object name and a create-only generation precondition (`ifGenerationMatch=0`) so retries cannot overwrite a live object. | Project and concrete region, Cloud Run co-location, object naming, lifecycle implementation/deletion controls, read identity, backup, audit and recovery remain unselected. Single-region storage reduces replication complexity/cost but leaves regional interruption as a documented availability risk. The 90-day horizon is a design preference, not a configured or runtime-approved retention policy. A conditional create does not make the bucket immutable against administrators. |
| Runtime identity | Dedicated Cloud Run service identity with only the permissions required to create receipt objects; a separate identity would read data for offline reports. | Exact service account and IAM bindings require security review. Google’s predefined Storage Object Creator role is a candidate because it allows object creation without object read, delete or overwrite permissions; verify the final permission set against the exact write API. |
| Write/ack behavior | Validate, assign receiver time, attempt durable object creation, then return success only after storage acknowledges the write. Return retryable failure if validation-independent infrastructure/storage errors prevent persistence. | HTTP codes, timeout, retries/backoff, replay handling, conflict evidence and client outbox behavior require contract tests. |
| Retention | A finite, owner-selected retention and deletion policy is required. Do not lock a bucket retention policy by default. | Retention duration, deletion authority, backup and account-disposal process remain open. Bucket Lock is irreversible and requires a separate explicit decision if ever proposed. |
| Ingress protection | HTTPS and strict request validation, bounded body/rate, no GET/list access on the public ingest surface, and logs that exclude credentials and payload secrets. | Public versus restricted ingress, rate-limiting/WAF controls, abuse handling, credential lifecycle and privacy classification require security review. |

The Cloud Storage write-before-ack pattern is a design candidate, not an
assertion that the service is already durable, immutable or authorized. A
storage outage, quota error, receiver timeout or authentication failure must
not be acknowledged as a stored receipt. Any retry must preserve source
identity and event time.

## 4. Receipt history is not missing-heartbeat detection

Cloud Run receives a request when one arrives. It does not, by itself, create a
record when EAGLE sends nothing. Cloud Run scale-to-zero can add request startup
latency, while configured minimum instances can reduce cold starts at an idle
cost. Google's Cloud Run SLA is expressed as monthly service uptime and is not a
per-request receipt-latency guarantee. Neither setting bounds EAGLE-to-report
latency end to end.

The receiver and durable ledger can support retrospective coverage analysis:
compare consecutive receiver timestamps and source sequence/time evidence,
then preserve any missing interval as uncertain. That yields evidence of
receipt gaps, not proof of why the source went quiet or the exact time EAGLE
failed.

If the product requirement is an alert or independent missing-heartbeat
classification within a bounded time, a separate evaluator/monitor and alert
path would be required. A scheduled evaluator would itself have delay, failure,
identity, billing and unknown-gap semantics; it cannot be assumed to provide a
hard deadline. That extension is outside this receiver-only draft and requires
its own exact design and review. Until then, absence after the last receipt is
`UNKNOWN` at report time, not a confirmed outage, planned shutdown, incident or
healthy interval.

## 5. Option trade-offs

| Option | Pros | Cons / limits |
|---|---|---|
| Cloud Run request-based, min instances 0 | Lowest idle-compute exposure; scales with receipt traffic; simple HTTPS request/response. | Cold starts and variable latency; does not self-detect silence; no hard end-to-end receipt deadline; still needs durable storage. |
| Cloud Run with minimum instance(s) | Can reduce startup latency and maintain a warm receiver. | Recurring idle charges; still cannot guarantee source/network delivery, storage availability or absence detection; does not alone justify a hard bound. |
| Cloud Run IAM + external Workload Identity Federation | Avoids a static long-lived service key when the source has a supported external identity. | Requires an identity provider and token exchange on EAGLE; this capability and operational complexity are unverified. |
| Public HTTPS + application-level request signature | Can authenticate an on-premise publisher without a cloud service-account key; compatible in principle with a source that can protect a dedicated secret. | Increases exposure to secret theft/replay; needs nonce/sequence, rotation, revocation, rate control and protected local secret storage. Not selected. |
| Cloud Storage object per receipt | Durable object history; create-only identity and generation precondition can prevent normal overwrites; simple append pattern. | Additional storage/request/egress/audit costs; retention and regional durability choices remain; privileged administrators can still alter/delete unless stronger controls are explicitly configured. |
| Existing telemetry relay snapshot | Reuses a known repository contract and avoids another receiver service. | Not accepted for witness history: latest-snapshot storage/process-local counters do not constitute a durable append-only receipt ledger. Reuse would require a separately reviewed change. |

## 6. Cost and control implications

The 2026-09-25 estimate models Cloud Run request-based, scale-to-zero and a
separate warm-instance case, plus Cloud Storage writes. It is order-of-magnitude
only: cadence, payload size, region, request duration, authentication, storage
retention, egress, logging, monitoring, build artifacts and account quotas are
not known. Recalculate with the official pricing calculator only after those
inputs are defined and the billing account/remaining quotas are verified.
Massimo Mainini selected (2026-09-26) to set the monthly ceiling after this
configuration-specific cost comparison. No numerical monthly ceiling is set by
that decision; a one-time ceiling, billing owner and allowed products remain
open as well.

The estimate's one-receipt-per-minute workload now matches the owner's selected
design cadence (2026-09-26). This alignment does not convert the old illustrative
rates into a quote or authorize a schedule, endpoint, resource or charge.

Before any runtime authorization Massimo must set monthly and one-time ceilings,
allowed project/products/region, billing owner, resource caps, stop action and
alert behavior. Budget alerts are not a guaranteed hard spending cap. Preference
for Cloud Run is not consent to use free-tier quota, create a project, or incur
any charge.

## 7. Decisions required to close the design gate

1. Owner selected receipt archive and offline gap reconstruction only
   (2026-09-26); no bounded missing-heartbeat alert is in scope for this design.
2. Select ingress/authentication after an authorized identity-capability
   review; keyless federation is the preferred direction only if its
   prerequisites are proven. No live capability inspection is authorized.
3. Owner selected single-region receipt storage and chose to select the
   concrete region only after comparing cost, latency and data-residency
   requirements (2026-09-26). No EU-only constraint or region is assumed. Then
   select project, Cloud Run placement, failure-domain treatment and scaling
   mode (minimum/maximum instances).
4. Owner selected a 90-day retention horizon (2026-09-26); define lifecycle
   implementation, deletion authority/evidence, object naming/idempotency,
   report-reader identity and recovery requirements. Do not enable irreversible
   Bucket Lock by default.
5. Owner selected a one-minute receipt cadence and an approximately two-minute
   threshold for marking a candidate silent interval (2026-09-26); define exact
   receipt fields, timestamp/clock-quality rules, timeout/retry/outbox behavior
   and `UNKNOWN` interval boundaries. The threshold does not establish cause or
   authorize a live evaluator/alert.
6. Recalculate the estimate after selecting the concrete region and configuration;
   then set the monthly ceiling as directed by the owner, plus one-time ceiling,
   billing owner, allowed products, resource limits and stop action.
7. Complete Leonardo Di Egidio's independent review and security/privacy review
   of the exact design; then produce a versioned exact-runtime authorization and
   wait for Massimo's explicit approval of that exact record before any runtime
   preflight or deployment.

The separate owner authorizations for a future local shutdown recorder and for
any real historical Windows/N.I.N.A. log snapshot remain open. Neither is
included in this Cloud Run receiver design or in the witness preference.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

## References

- `docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F3-PILOT-SPECIFICATION-DRAFT-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F4-GITHUB-WITNESS-FEASIBILITY-2026-09-25.md`
- `docs/architecture/validation/BKL-043-F4-COST-ESTIMATE-2026-09-25.md`
- `infrastructure/telemetry-relay/README.md` — snapshot relay precedent only; not a durable witness approval.
- [Cloud Run billing settings](https://docs.cloud.google.com/run/docs/configuring/billing-settings) — request/instance billing and min-instance considerations; reviewed 2026-09-26.
- [Cloud Run autoscaling](https://docs.cloud.google.com/run/docs/about-instance-autoscaling) — on-demand startup and scale-to-zero behavior; reviewed 2026-09-26.
- [Cloud Run service-to-service authentication](https://docs.cloud.google.com/run/docs/authenticating/service-to-service) — IAM invocation and external Workload Identity Federation options; reviewed 2026-09-26.
- [Cloud Run Service Level Agreement](https://cloud.google.com/run/sla) — monthly uptime SLO, not per-receipt latency; reviewed 2026-09-26.
- [Cloud Run pricing](https://cloud.google.com/run/pricing) — request/instance billing; reviewed 2026-09-26.
- [Cloud Storage request preconditions](https://docs.cloud.google.com/storage/docs/request-preconditions) — generation-match `0` prevents overwriting an existing live object; reviewed 2026-09-26.
- [Cloud Storage IAM roles](https://docs.cloud.google.com/storage/docs/access-control/iam-roles) — Storage Object Creator permissions; reviewed 2026-09-26.
- [Cloud Storage Bucket Lock](https://docs.cloud.google.com/storage/docs/bucket-lock) — retention and irreversible lock behavior; reviewed 2026-09-26.
