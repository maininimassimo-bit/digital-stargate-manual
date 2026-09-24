# BKL-043 F3 — Read-only Reliability Pilot Specification (Decision Draft)

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F3-PILOT-SPECIFICATION-DRAFT-2026-09-24` |
| Gate | `M-BKL043-F3-READONLY-PILOT-READINESS` |
| Status | Repository-only draft; owner decisions and exact runtime authorization pending |
| Owner / accountable | Massimo Mainini |
| Basis | F2 two-plane logical architecture accepted 2026-09-24; no implementation authorized |
| Authority | `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

## 1. Decision summary

This document makes the F2 architecture reviewable as a bounded pilot proposal.
It does **not** authorize a pilot, select a runtime target or source, or permit
live access, installation, startup, polling, persistence, network transmission,
incident registration, or deployment. The separate owner decision sheet is
`BKL-043-F3-EXACT-PILOT-AUTHORIZATION-DECISION-2026-09-24.md`; its fields remain
unapproved until explicitly completed and accepted by Massimo Mainini.

The proposal is deliberately split into independently selectable planes:

1. **Local observation plane (candidate only):** consume already-published,
   source-owned read-only projections and the existing BKL-030 EAGLE host-health
   collector contract; never query devices directly.
2. **Independent witness plane (candidate only):** receive a minimal heartbeat
   outside the EAGLE failure domain and durably record receipts. The existing
   relay is not assumed to satisfy this role; no endpoint, store or transport is
   selected.
3. **Incident lifecycle plane (not in this pilot proposal):** OPSC-ALM-001 is a
   draft and there is no incident register. Creating one needs its own contract,
   privacy/operations review and authorization. Until then, reports may show
   observation gaps and candidate conditions only, never opened/closed incidents.

If plane 2 is not separately authorized and validated, the scope must be called
“EAGLE-observed component telemetry”; it cannot claim whole-system availability,
MTBF or MTTR. No plane can turn `UNKNOWN`, `STALE`, `UNAVAILABLE` or a missing
heartbeat into `HEALTHY`, `SAFE`, restoration, or an incident cause.

## 2. Source eligibility and trust boundaries

The table records repository evidence, not current runtime state. Every source
requires fresh owner-approved preflight evidence before any future live pilot.

| Candidate | Existing evidence / interface | Proposed pilot use | Failure domain and gaps | Disposition |
|---|---|---|---|---|
| EAGLE host health | `DSG.EagleHostHealthCollector` / BKL-030 G1/G2 source map; manual G5/G6 OAT; G6 history contract | Consume its source-owned projection only; preserve source observation time, quality, freshness, cadence class and reason | Same EAGLE host, OS, local storage and power; cannot observe host-off intervals. G5/G6 were manual, not recurring authorization. Public committed projection is `UNKNOWN/UNAVAILABLE/NO_CURRENT_SNAPSHOT`. | Eligible as a design input only; live read and runtime identity/cadence unapproved. |
| N.I.N.A. observatory telemetry | `contracts/telemetry/observatory-status-v1.schema.json`; historical exporter/network/J6 commissioning; local producer projection | Consume existing local projection and provenance if its current producer and read-only boundary are revalidated | Shares EAGLE and relevant network/source dependencies; repository projection is stale/unknown. Commissioned producer settings (including its freshness/cadence) are source-specific and must not be copied as detector policy. | Conditional candidate; no current runtime status established here. |
| N.I.N.A. application logs | Repository snapshot: 35 artifacts / 23 folders / 32 unique contents; owner-defined attempt means N.I.N.A.-logged activity | Offline parser and synthetic contract tests only in this F3 package; no live log tailing | No planned-session denominator or incident lifecycle; duplicate/overlapping files and event/grouping/outcome semantics remain unvalidated. | Excluded from pilot metrics until parser, grouping, retry, terminal-state and reconciliation contract passes a separate review. |
| TS Shelter J6 mains-presence | Historical 2026-08-27 read-only commissioning | At most a distinct mains-presence source if independently revalidated and explicitly selected | Mains-present/lost/restored only; not UPS/battery state, EAGLE power, or safety. Shares parts of the observatory power/network dependency. | Not selected; no direct device query authorized. |
| Passive network observations | Historical 2026-08-26 N.I.N.A. adapter commissioning | At most existing producer output; no new network probes | A failed path can mask the reporting host; interface/VPN/failover fields previously unresolved. | Not selected; no probing or management-plane credentials. |
| Dome, mount, camera, weather projections | Observatory Status schema and historical commissioning | Consume only current, source-attributed producer projection if separately verified | Schema does not prove producer availability; current repository projection reports unknown/expired values. Local Safety Authority is outside scope. | No component-specific source is currently approved by this draft. |
| Hosted telemetry relay | Latest-snapshot `GET`/`POST` interfaces documented in relay README | No pilot witness use in this draft | Latest value and process-local counters do not prove durable independent receipt history; changes imply hosted write/storage and deployment. | Excluded as witness until separate design and runtime gates. |
| Incident register | OPSC-ALM-001 draft only; owner confirmed none exists | None | No correlated event population or validated restoration/closure history. | Explicitly excluded. |

**Provenance fields to preserve where a source already supplies them:** stable
source/component identity, source observation UTC, receiver UTC (if applicable),
freshness/quality/reason, source version, host boot/process identity where
available, sequence or source event identity, correlation/evidence reference,
payload digest, and clock-quality. Missing fields remain missing/unknown; the
observer must not synthesize source freshness or replace source time with
collector time.

## 3. Proposed topology and scope variants

```text
Existing source-owned local projections (conditional, read-only)
                │
                ▼
      Local observer on EAGLE (candidate)
                │ append-only local journal (not authorized)
                ├────────► coverage-qualified local report (offline prototype only)
                │
                └────────► minimal heartbeat (not authorized)
                              │
                              ▼
                   Independent witness outside EAGLE
                              │ durable receipt journal (not authorized)
                              └────────► receipt/gap report

Operator-confirmed incident register: excluded; separate future gate.
No path to N.I.N.A. control, device commands, scheduler, remediation or Safety Authority.
```

The only currently authorized activity is repository design and offline
synthetic validation. A later owner decision may select either a local-only
scope or both observation and witness planes. A local-only result must state
that host-offline coverage is absent. Selecting the witness plane entails a new
external persistence and privacy boundary, not merely reusing the existing
snapshot relay.

## 4. Data minimization and privacy contract proposal

Proposed record envelope (logical, not an implemented or approved schema):

```text
schema_version, record_id, component_id, source_id, source_instance_id
source_observed_at_utc, received_at_utc, clock_quality
source_quality, freshness_state, reason_code, coverage_state
host_boot_id, process_run_id, source_sequence_or_event_id
correlation_id, evidence_reference, payload_digest
```

- Store only normalized status/provenance needed to qualify observation and
  coverage. Do not copy raw N.I.N.A. logs, chat prompts, tokens, API keys,
  environment variables, personal data, arbitrary command output or source file
  paths into records.
- Do not infer telemetry from secrets/configuration, or include secret values in
  errors and diagnostics. Any future transport credential is separately
  provisioned and never placed in payloads or repository artifacts.
- Candidate identity and idempotency are deterministic. Replays with identical
  identity and digest are duplicates; same identity with different content is a
  conflict preserved for review, never overwrite-last-wins.
- Preserve original UTC values. Pair with monotonic elapsed time only within a
  boot/process epoch; clock jump, absent synchronization, future timestamp or
  contradictory ordering makes affected duration/coverage `UNKNOWN`.
- Retention duration, data residency, encryption, access roles, backup/export,
  deletion and disposal are **unselected owner/security/privacy decisions**.
  Until decided, no durable store is to be created. G6's
  `retention_deletion_enabled=false` is precedent, not a newly approved policy.

## 5. Offline validation cases and acceptance criteria

All cases below are synthetic fixtures or pure contract tests; none may contact
EAGLE, N.I.N.A., hardware, relay, network endpoints, or user data.

| Case | Required expected result |
|---|---|
| Current / stale / absent / unavailable / conflicting source | Preserve source quality; missing/stale/conflict is never rendered healthy or safe; report reason and interval as unknown where needed. |
| Duplicate and reordered receipt; exact replay | Deterministic idempotent replay; no double-count; retain original observation/receive times and lineage. |
| Identity reused with altered payload | Mark conflict; preserve both evidence digests; do not overwrite or choose one silently. |
| Clock unsynchronized, backward/forward jump, future or missing timestamp | Set affected clock/coverage to unknown; do not calculate negative duration or repair timestamps silently. |
| EAGLE shutdown / restart / new boot ID | Close local coverage only at last evidenced sample; start a new epoch after restart; gap is not healthy exposure. |
| EAGLE unavailable while independent witness continues | Witness may bound receipt gap only; it cannot identify cause or exact onset/restoration. |
| Network partition / witness outage | Local and remote coverage reported separately; remote gap is unknown, queued receipts cannot backdate proof of continuous availability. |
| Journal full, corrupt, interrupted append or recovery | Preserve prior valid records; expose explicit coverage loss; fail closed; no truncation/overwrite and no automatic cleanup. |
| Append/replay/reconciliation after recovery | Deterministic, repeatable reconciliation with conflicts and uncertain intervals visible. |
| Candidate incident acknowledge/restore/reopen transitions | Contract rejects automatic restore/close; actor, reason, evidence, clock quality and prior/new state required. Incident tests remain synthetic only. |
| Prohibited data in payload/diagnostic | Validator rejects known secret fields and raw-log/body fields; tests use dummy values only and never print them. |
| Authority boundary | Contract and generated report contain no command, execution, scheduler, remediation, safety or control action; all three authority fields remain `NONE`. |

F3 offline readiness passes only when each case is reproducible from committed
synthetic fixtures, validators fail closed as stated, and tests assert no network
or hardware access. These criteria validate semantics, not runtime performance,
source freshness, resource budgets, or MTBF/MTTR.

## 6. Coverage and metric reporting

- Report each component and each plane independently, with window start/end,
  eligible observed intervals, unknown gaps, evidence age, source quality and
  exclusion reason. Do not merge denominators across components.
- Host-local observation cannot cover EAGLE-off intervals. Witness receipt gaps
  are bounded between a last accepted receipt and a later confirmed missing
  condition only if an approved contract defines that condition; absent cadence
  and thresholds, no gap detector can be configured in F3.
- Unknown time is excluded from eligible exposure and never presumed healthy.
  Receipt time is not source observation time; missing heartbeat does not prove
  device failure, cause, or exact onset.
- Do not publish availability percentage, SLO, failure budget, overall-system
  scalar, or MTBF/MTTR in this pilot. Component metrics remain deferred until
  validated event taxonomy, unique fault population, exposure denominator,
  representative coverage and owner-approved observation window exist.
- Detection-to-restoration may later be reported only from an approved incident
  lifecycle with human/independent confirmation and clock-quality evidence; no
  incident register presently exists.

## 7. Non-interference, security and rollback proposal

No numeric CPU, memory, disk-I/O, storage, network, polling or duration budget is
set here. Candidate preflight for a separately authorized runtime gate must
measure baseline and pilot deltas during a representative imaging workload,
define a stop threshold before starting, and prove stop/rollback recovery. Values
must be selected and approved for the exact target; historical producer cadence
and freshness are not transferable.

Before runtime consideration, the separate gate must specify:

1. exact host/service identity, software artifact/hash, owner and support contact;
2. least-privilege read-only access proof per selected source;
3. explicit components/planes in scope and excluded coverage;
4. selected cadence, timeout, maximum resource use, observation window and stop
   conditions;
5. local and remote data stores, network egress, encryption/access controls,
   backup, retention and deletion policy;
6. install/start/stop/disable/uninstall steps, configuration backup, rollback
   owner and recovery verification;
7. offline fixture pass, security/privacy review, non-interference OAT,
   independent review, and post-change evidence plan.

If any selected source can mutate state, requires a command-capable credential,
cannot be bounded to read-only behavior, or threatens imaging/control workloads,
exclude it and report the coverage limitation. Stop/fail-closed behavior must not
interfere with EAGLE, N.I.N.A., PHD2, the relay or observatory control paths.

## 8. Open decisions and gate disposition

The accompanying decision sheet records unresolved owner choices. At minimum,
the following are not selected by this draft: local-only vs two-plane pilot,
target host and identity, source list, source access method, heartbeat transport
and independent witness, cadence/timeout/observation window, local/remote store,
retention/deletion, privacy/security controls, deployment/rollback, and stop
conditions. Incident lifecycle remains out of scope unless separately authorized.

The proposed machine-readable envelope is
`contracts/telemetry/bkl-043-reliability-observation-v1.schema.json`; its
synthetic contract tests are
`.github/scripts/test-bkl043-f3-offline-contract.mjs`. The validator is an
offline design/contract test only, not a collector, journal, heartbeat client,
incident system or runtime package. The tests cover current/stale/missing and
conflicting evidence, replay identity, ordering, clock issues, forbidden
payload/control fields and fixed `NONE` authorities. CI runs the same test from
Developer Foundation. These tests validate the proposal's envelope semantics;
they do not prove any source is available, fresh or read-only on a live host.

**Disposition: OWNER APPROVED PREPARATION OF A SEPARATE EXACT PILOT AUTHORIZATION;
NOT READY FOR RUNTIME.** The ten offline tests pass locally and in post-merge CI.
F3 review findings remain to be recorded. Massimo Mainini's 2026-09-24 owner
disposition permits preparation of the distinct F4 exact-authorization draft;
it does not select runtime parameters or authorize installation, live source
reads, polling, persistence, network transmission or deployment. The separate
exact runtime decision and its own reviews, preflight, OAT and release gate remain
mandatory.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

## References

- `docs/architecture/validation/BKL-043-F3-READONLY-PILOT-READINESS-GATE-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-POPULATION-AND-CONTRACT-GAP-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`
- `docs/architecture/telemetry/BKL-030-EAGLE-Health-Projection-Contract.md`
- `docs/architecture/telemetry/BKL-030-G6-EAGLE-Health-History-Persistence-Design.md`
- `docs/architecture/telemetry/observatory-status-realtime-telemetry-pilot.md`
- `docs/architecture/alarm-and-incident-model.md` (OPSC-ALM-001 draft)
- `docs/architecture/packages/AP-004-Enterprise-Telemetry-and-Observability-Architecture.md`
- `docs/architecture/packages/AP-007-Enterprise-Operations-and-Service-Management-Architecture.md`
