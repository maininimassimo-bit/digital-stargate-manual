# BKL-043 F4 — Shutdown Evidence Contract and Historical Reconciliation Plan (Draft)

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F4-SHUTDOWN-RECONCILIATION-DRAFT-2026-09-25` |
| Gate | `M-BKL043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION` |
| Status | Repository-only design draft; no recorder, log access, import, or runtime action authorized |
| Owner / accountable | Massimo Mainini |
| Authority | `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

## 1. Purpose and fixed interpretation

This draft defines a reviewable local shutdown evidence contract and an offline
method for considering historical Windows System events alongside N.I.N.A.
activity and session evidence. It records the owner decisions of 2026-09-25 and
2026-09-27: policy B, record shutdown evidence locally, include a local
pre-shutdown request marker in the proposed evidence sequence, and preserve the
source timestamp with its timezone/offset while deriving UTC only when
defensible (DLG-140).

A local orderly-shutdown record can support the fact and recorded time of an
orderly shutdown. By itself it does not show that the shutdown was planned, rule
out an incident, prove that the host actually lost power, or establish when
observatory service became unavailable. Planned intent requires independent
corroboration or human review. Otherwise cause and affected interval remain
`UNKNOWN`.

This is a design proposal, not approval to select or install a recorder, register
a task, read/import EAGLE logs, process real N.I.N.A. logs, or access EAGLE. The
Windows System log remains a candidate historical source only. Any later access
or import requires a separate, explicit authorization defining source, period,
custody, processing, and destination.

## 2. Local event contract proposal

### 2.1 Evidence classes

Keep these distinct; do not merge them into one inferred “planned shutdown” fact:

1. **Shutdown request marker (owner-selected design element, 2026-09-27):** a
   local writer records that an orderly shutdown request was issued, preserving
   only one controlled mechanism category. The owner selected these values on
   2026-09-27: `INTERACTIVE_LOCAL_REQUEST`,
   `APPROVED_AUTOMATED_REQUEST`, and `UNKNOWN`. Do not record a person's name,
   account name, SID, or other individual identifier. `UNKNOWN` is required when
   the mechanism class cannot be established from the marker. This proves only
   that the writer recorded a request; it does not prove the OS completed
   shutdown or that the shutdown was planned. Tying the request to a reviewed
   plan still requires independent corroboration or human review.
2. **OS shutdown evidence:** a validated Windows System event from an approved
   provider/event allowlist indicating an orderly shutdown transition. Preserve
   provider, event identity, native record identity and timestamp provenance.
   Event IDs and message text must be validated against the applicable Windows
   build and event manifest before a parser relies on them; this draft does not
   establish an allowlist.
3. **Restart/boot evidence:** a separately validated OS startup/boot marker.
   It starts a new host observation epoch only when identity and timestamp quality
   are adequate. A boot marker does not prove observatory availability.

The owner-selected design direction includes an append-only, non-elevated
request marker produced by a dedicated local command used interactively by a
local operator. Before confirmation, the command must display the target host
identity and state that it will request an orderly shutdown of that host. It
presents an explicit Yes/No confirmation with No selected by default; only an
affirmative Yes proceeds to persist the marker and then issue the shutdown
request. No, blank, invalid, or canceled input issues no request and records no
request marker. Pair the marker where available with
OS-native shutdown and subsequent boot evidence. The marker remains distinct
from evidence that the OS completed shutdown. The three mechanism categories
are selected; writer placement, trigger, storage path, permissions, durability,
and failure handling remain unselected implementation decisions. The owner
selected a fail-closed design direction for the writer-controlled shutdown path:
if the marker cannot be durably persisted, that path must not issue the orderly
shutdown request and must surface the persistence failure for human choice.
This does not disable independent/manual OS controls, prove persistence is
durable, or authorize a hook, task, service, or writer. Whether and how such a
design can be implemented without interfering with operating-system or safety
controls remains subject to review. This selection
does not authorize configuring a shutdown hook, scheduled task, service, or
writer. The owner selected interactive use either at the target's local console
or through an interactive remote session such as RDP. Here “local command” means
the command runs on the target host; it does not require the operator to be
physically at its console. Any account that already has interactive access to
the host may invoke it; this design does not add or change OS accounts, groups,
or access controls. Automation must not invoke it, and the event record must not
store an account name, SID, or other individual identifier. The
`APPROVED_AUTOMATED_REQUEST` value remains part of the
controlled vocabulary but has no selected or authorized production trigger in
this design. Shutdowns initiated through other paths may lack a request marker
and must be reconciled from their own evidence without inferring intent. The
owner also selected not to record whether invocation came from the local
console or an interactive remote session. The marker must not imply or encode
that distinction, and later reconciliation must not infer it from the marker.
The command's implementation, invocation details, storage and permissions
remain unselected.

### 2.2 Minimum normalized record fields

| Field | Meaning |
|---|---|
| `schema_version`, `record_kind`, `record_id` | Versioned envelope; kind distinguishes request, OS shutdown, and boot evidence. `record_id` is deterministic from source identity, native record identity and content digest where available. |
| `host_identity`, `boot_epoch_id` | Host as evidenced by the source and the boot epoch to which the record is attributed; missing or conflicting identity remains unknown. |
| `source_provider`, `source_event_id`, `source_record_id` | Native provider/event and record identity, or the named local writer identity for a request marker. Preserve native identifiers; do not manufacture them. |
| `event_time_raw`, `event_time_utc`, `time_zone_or_offset`, `clock_quality` | Preserve the source's original timestamp representation and the evidenced timezone/offset. Derive UTC only when timezone/offset, source semantics and clock quality are defensible; otherwise leave normalized UTC unknown. Never overwrite the raw value or silently repair clock drift. |
| `recorded_at_raw`, `recorded_at_utc`, `recorded_time_zone_or_offset`, `recording_outcome` | Preserve the recorder's original persistence-time representation and timezone/offset; derive UTC only when defensible. This is distinct from event time and must not replace or imply the OS shutdown event time. |
| `shutdown_mode_observed`, `request_mechanism_class` | Only values directly evidenced by the source. `request_mechanism_class` is one of `INTERACTIVE_LOCAL_REQUEST`, `APPROVED_AUTOMATED_REQUEST`, or `UNKNOWN`; it must not include an individual identity. Do not infer intent from a generic orderly event. |
| `evidence_digest`, `evidence_reference`, `parser_or_writer_version` | Integrity and lineage to the locally retained evidence, parser/writer version, and any approved evidence locator. Do not embed private file paths or raw log bodies in a report. |
| `quality_state`, `ambiguity_codes` | `CURRENT`, `CONFLICTING`, `INCOMPLETE`, or `UNKNOWN` evidence quality and explicit reasons. Quality is not incident severity or safety state. |

The normalized record must not contain credentials, arbitrary command output,
raw N.I.N.A. log lines, unrelated Windows event payloads, personal data, or
unnecessary local paths. Local storage format, ACL, encryption, retention,
backup, deletion, and tamper evidence remain open decisions.

### 2.3 Loss and ambiguity cases

| Case | Required disposition |
|---|---|
| Power loss, crash, forced reset, or OS failure before a marker is persisted | No marker is not evidence that no shutdown occurred. Leave the transition and preceding interval open/unknown until corroborated. |
| Marker persisted but orderly shutdown evidence absent | Preserve “request recorded”; do not claim shutdown completion. Classify transition `UNKNOWN`/incomplete. |
| OS shutdown evidence present but no request marker | Record the OS evidence; cause and prior planning remain `UNKNOWN`. |
| Marker says orderly request, but later evidence conflicts or shows unexpected interruption | Preserve both lineages as a conflict; no last-write-wins or automatic incident classification. |
| Local event log rolled over, cleared, truncated, inaccessible, or has gaps | Mark source coverage incomplete for the affected period; absence of an event is not proof of absence of a shutdown. |
| Duplicate native record or repeated import | Deduplicate only on stable native identity plus content digest; reused identity with changed content is a conflict. |
| Clock unsynchronized, timezone/DST unresolved, time moved, timestamp absent, or order impossible | Preserve raw value; normalized time and duration are `UNKNOWN` for the affected evidence. Do not repair silently. |
| Boot/shutdown pair is unmatched or more than one candidate pair exists | Keep interval open or ambiguous; do not select a convenient pairing. |
| Host identity or boot epoch cannot be bound confidently | Do not join records across epochs or hosts; mark `UNKNOWN`. |

## 3. Offline historical reconciliation plan

### 3.1 Inputs and eligibility

If a separate owner authorization is later given, reconcile only bounded,
owner-supplied copies or exports with documented provenance:

- Windows System event records selected by a reviewed provider/event allowlist
  for boot, orderly shutdown, unexpected termination, and log continuity;
- N.I.N.A. activity summaries produced by a separately validated parser. The
  accepted population definition remains “an attempt exists only when activity
  is recorded in a N.I.N.A. log”; grouping, retries, terminal outcomes and
  duplicate rules remain unvalidated until separately reviewed;
- session manifests or other existing session evidence, retaining their own
  source authority and time quality; and
- independent corroboration, if available and specifically authorized, such as
  an owner-confirmed plan or a separately sourced power/network observation.

Repository schemas and historic commissioning evidence are not proof that any
source is currently complete or available. Do not read, enumerate, copy, or
import actual EAGLE logs or N.I.N.A. logs as part of this gate.

### 3.2 Processing sequence

1. **Authorize and inventory the supplied snapshot.** Record source owner,
   export method, host identity claim, covered period, export time, original
   timezone/clock context, file counts/sizes and cryptographic digests. Preserve
   originals read-only; do not upload them to the public manual repository.
2. **Validate custody and coverage.** Establish whether records are continuous
   for the requested period, and whether logs rolled, cleared, were copied
   partially, or crossed host rebuild/clock-change boundaries. If not
   established, represent coverage gaps explicitly.
3. **Normalize without erasing source time.** Preserve native timestamp text,
   source timezone/offset and provider/record identity. Derive UTC only when
   conversion is defensible, including source timestamp semantics and clock
   quality; otherwise retain the raw value and mark normalized time unknown.
   Keep recorder persistence time separate from source event time. Flag DST
   ambiguity, clock steps, missing offsets, impossible ordering, duplicates and
   conflicting identities.
4. **Build a host-epoch event ledger.** Pair validated boot and shutdown events
   only when identity, epoch, ordering and source continuity support a unique
   pairing. Label outputs as bounded host-on intervals, open-ended intervals,
   or ambiguous/unknown gaps. Keep OS evidence distinct from the local request
   marker.
5. **Reconcile application/session evidence.** Place parsed N.I.N.A. activity
   and session-window evidence on the same timeline only with validated time
   semantics. Correlation supports temporal overlap or discrepancy review; it
   does not turn a N.I.N.A. event into proof of host uptime, observatory
   availability, successful science, or incident cause.
6. **Review discrepancies and intent.** Preserve unmatched events and competing
   explanations. Any planned/unplanned or incident interpretation requires
   independent corroboration or named human review with rationale. Otherwise
   retain `UNKNOWN`.
7. **Publish a bounded reconciliation report.** Include scope, provenance,
   coverage limitations, parser versions, event counts by evidence class,
   unmatched/conflicting records, unknown intervals, decisions and reviewer.
   Do not publish raw logs or unsupported reliability metrics.

### 3.3 Output classes and prohibited equivalences

The result must report three separate concepts:

- **Host-on evidence:** intervals bounded by validated host boot/shutdown
  evidence. Missing endpoints, incomplete logs and clock uncertainty reduce
  coverage and remain unknown.
- **Observatory availability:** requires validated component/service evidence
  and its own failure and coverage semantics. Host-on time alone is insufficient.
- **Scientific activity:** requires validated N.I.N.A./session evidence and
  event semantics. Host-on time, N.I.N.A. process activity and successful
  scientific operation are not interchangeable.

Do not subtract unobserved gaps as planned downtime. Do not classify orderly
shutdown as planned downtime without independent support or human review. Do not
infer an incident, failure onset, restoration, MTBF, MTTR, availability rate,
SLI/SLO, or failure budget from host boot/shutdown reconstruction alone.

## 4. Synthetic offline validation plan

Before reviewing real historical material, the proposed parser/reconciler should
be exercised only with synthetic fixtures covering:

1. unique orderly shutdown request + OS shutdown + boot sequence;
2. OS shutdown without request marker and request marker without OS completion;
3. crash/power-loss pattern with missing shutdown record;
4. unmatched boot/shutdown, multiple possible pairings, duplicate and conflicting
   native record identity;
5. event-log rollover/clear, partial export and explicit coverage holes;
6. local timezone, daylight-saving transition, absent offset, clock step and
   impossible timestamp ordering;
7. N.I.N.A. activity overlapping or outside a host-on candidate interval,
   duplicate log content, retries and unresolved grouping;
8. session evidence with missing/uncertain times and no N.I.N.A. activity;
9. independently corroborated versus unsupported planned intent;
10. report assertions that host uptime, observatory availability and scientific
    activity are separate, and that unknown intervals never become healthy,
    planned, or non-incident by default.

Expected result: deterministic records and classifications with provenance,
unknowns, conflicts and coverage limitations preserved; no network, hardware,
EAGLE, live log, credential or runtime calls. These cases validate semantics,
not the completeness or accuracy of real source data.

## 5. Gate decisions still required

This draft resolves no runtime decision. Before a real historical reconciliation,
Massimo Mainini must separately authorize the exact source snapshot, period,
custody/transfer, processing environment, retention and report destination.
Before any future local recorder, the owner and reviewers must select its exact
trigger/mechanism, identity, artifact, storage, durability guarantees, stop and
rollback behavior, data controls, and OAT. Windows provider/event allowlists,
parser semantics, N.I.N.A. attempt grouping and classification policy need
independent review. This document does not satisfy the other open F4 decisions.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

## References

- `docs/architecture/validation/BKL-043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION-DRAFT-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F4-GITHUB-WITNESS-FEASIBILITY-2026-09-25.md`
- `docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-POPULATION-AND-CONTRACT-GAP-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`
- `docs/architecture/telemetry/evidence/BKL-030-EAGLE-Health-Source-Discovery-2026-09-03.md` — historical source-discovery evidence, not current host attestation.
- `docs/architecture/telemetry/BKL-030-G6-EAGLE-Health-History-Persistence-Design.md` — precedent for local append-only evidence; not authorization for a new writer.
