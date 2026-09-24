# BKL-043 F1 — Population and Contract Gap Discovery

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F1-POPULATION-CONTRACT-GAPS-2026-09-24` |
| Status | Repository-only gap discovery complete; no metric contract approved |
| Package | BKL-043 Observatory Reliability Engineering |
| Baseline | `e25bd6682dfd95825c205f4b8bbf99b50fdb2d16` |
| Owner / accountable | Massimo Mainini |
| Authority | Descriptive, repository-only, read-only; command/execution/safety `NONE` |

## Purpose and limits

This addendum tests whether existing repository contracts provide complete,
well-defined populations for future reliability measurement. It records gaps and
evidence eligibility only. It does not approve an event schema, service boundary,
SLI/SLO, numerical target, collection cadence, live publisher, writer, alert or
operational process.

## Population and source findings

| Candidate population/source | Repository evidence | What it supports | Gap that prevents reliability measurement |
|---|---|---|---|
| Completed scientific sessions | `docs/data/scientific-session-catalog.json`, schema 1.5, 22 historical records; 7 `VALIDATED_ANALYTICS`, 15 `ATTENTION_REQUIRED` | Descriptive facts for catalogued sessions | Catalog is not an authoritative record of all planned/attempted nights; no complete cancelled, failed, weather-lost or not-started denominator. `ATTENTION_REQUIRED` is not an operational incident. |
| N.I.N.A. application logs | Repository inventory under `data/sessions/**/raw/nina/*.log`: 35 file artifacts across 23 session folders; 32 distinct file contents by SHA-256 in this snapshot | Evidence that N.I.N.A. emitted local application-log activity over the timestamps recorded in each file; a candidate source for later, parser-validated activity summaries | Not a planned-session register and cannot represent a session that never started N.I.N.A. Some identical contents occur under different session folders, and observed log timestamps can cross folder/session-window boundaries. File/line counts or lexical `error`/`start`/`complete` matches are not validated attempt, fault, completion, or incident counts. No N.I.N.A.-specific lifecycle parser/contract or reconciliation to a complete planned/attempted population was found. |
| Session completion event | `contracts/events/observation-session-completed-shadow-v1.schema.json` and one artifact at `docs/data/integration/session-completed-shadow-event-2026-09-21_2026-09-22.json` | Contract/shadow validation for one completed session | `event_state=SHADOW_VALIDATED`, `runtime_published=false`, `transport=repository-shadow-artifact`; the payload fixes `report_status=COMPLETE`. It cannot represent or count unsuccessful attempts. `occurred_at_utc` and `published_at_utc` are declared properties but are not in the schema's required list. No authoritative planned-session ID, attempt lifecycle, terminal disposition or complete population reconciliation is evidenced. |
| EAGLE host-health history | `docs/architecture/telemetry/evidence/BKL-030-G6-Runtime-OAT-2026-09-04.md`; linked design and independent review | A real read-only collector projection at `2026-09-04T16:37:19.443Z`; one manual persistence cycle appended 14 signal samples; identical replay appended 0 and skipped 14 duplicates; segment remained 14 records / 13,945 bytes | OAT is a bounded point-in-time pilot. No permanent Scheduled Task/service cadence was authorized. The runtime history is not a repository-complete continuous observation series; no coverage intervals, outage ledger or exposure denominator can be derived. The independent review explicitly leaves recurring orchestration separately governed. |
| Current EAGLE public projection | `docs/data/realtime/eagle-health.json` | Current public snapshot disposition | `UNKNOWN` / `UNAVAILABLE` / `NO_CURRENT_SNAPSHOT` is not healthy evidence and supplies no historical continuity. |
| Archived BKL-036 F4 telemetry | `docs/data/bkl-036-f4-telemetry-archive.json` and its schema | Contract and offline fixture behavior | The archive is synthetic/offline and its seven domains are `UNAVAILABLE`; excluded from live reliability counts. |
| Alarm / incident population | `docs/architecture/alarm-and-incident-model.md` (OPSC-ALM-001, draft) and AP-007 incident model | Candidate event and incident lifecycle fields | No correlated, complete observatory incident records were found. The draft proposes `detected_at` and `acknowledged_at` plus timeline evidence, but does not establish a populated, validated `restored_at`/resolution-time series or incident denominator. |
| Platform CI incidents | `infrastructure/bkl031-f3-a3-gcp/platform/*INCIDENT*.json` | Incidents about governed CI/runner/platform execution | Wrong service population; cannot be included in observatory/device reliability. |

## Contract readiness by candidate measure

| Measure candidate | Minimum population/semantics still missing | Disposition |
|---|---|---|
| Service availability / telemetry freshness | Approved service/component boundary; continuous observation intervals; explicit unknown/gap treatment; source cadence and coverage evidence; outage start/end semantics | Not measurable; no percentage or SLO. |
| Session completion | Owner-authoritative planned/attempted-night register; stable plan/attempt IDs; mutually exclusive terminal dispositions including not-started/cancelled/weather/technical/complete; reconciliation to observed sessions | Not measurable; completed-session catalog is survivor-only descriptive context. |
| N.I.N.A.-observed attempt outcome | Owner accepted on 2026-09-24 that an attempt means activity recorded in N.I.N.A. logs; planned sessions with no N.I.N.A.-recorded activity are excluded. Still missing: validated lifecycle parser, attempt grouping/identity, retry and duplicate rules, and terminal outcome semantics | Definition accepted for a bounded observed-activity measure only; no count or rate yet. It must not be represented as completion of all planned sessions. |
| Fault frequency / MTBF | Validated fault taxonomy; event identity and correlation; repeat/duplicate rules; eligible service exposure interval; inclusion/exclusion policy | Not measurable; no fault population or exposure denominator. |
| Acknowledgement / restoration / MTTR | Populated incident lifecycle with reliable detected, acknowledged, restored/resolved and closed transitions; reopen and clock-quality semantics; service linkage | Not measurable; draft process model is not operational event evidence. |
| Failure budget / SLO | Approved SLI definition, measured representative baseline, observation window and accountable service owner | Not defined; AP-007 requires measurement before SLO deliberation. |

These are contract-completeness prerequisites derived from AP-004/AP-007 and
existing repository evidence. They are not a proposed schema, target, service
cadence or authorization to create a live source.

## N.I.N.A. log inventory — read-only qualification

The repository contains 35 N.I.N.A. `.log` artifacts in 23 session folders; a
SHA-256 comparison of the file contents found 32 distinct contents in the
inventory snapshot. Identical content stored under more than one folder means
folder/file counts are not independent session counts. In addition, timestamp
ranges in some logs extend across the folder's nominal session window. A folder
name or log filename therefore cannot be treated as a validated session/attempt
identifier without an owner-approved correlation rule.

The logs are useful evidence of application activity that was actually recorded
by N.I.N.A. They do not enumerate planned nights, attempts that ended before
N.I.N.A. started, or nights absent from the repository. Generic lexical matches
such as `start`, `complete`, `abort`, `error`, or `shutdown` have not been
validated against N.I.N.A.'s event semantics and are deliberately not reported as
counts of attempts, successful sequences, faults, or incidents. The user
confirmed that no incident register is present; accordingly the logs do not
provide a complete correlated incident lifecycle or support MTBF/MTTR.

The owner accepted on 2026-09-24 the following bounded definition for any future
N.I.N.A.-based attempt analysis: an attempt exists only when activity is
recorded in a N.I.N.A. log. A planned session with no such recorded activity is
excluded. Any resulting statistic must be labelled as applying only to
N.I.N.A.-observed attempts, never as a completion rate for all planned
sessions. This definition does not itself validate how multiple log files,
restarts, retries, or sequence lifecycle events map to one attempt or outcome;
those semantics still require a validated parser and reconciliation rules.

No raw log lines, credentials, or personal data are reproduced here. This
inventory is a bounded repository snapshot, not evidence of a complete external
or live log source.

## Safe next gate

Continue repository-only analysis to identify whether an already approved,
authoritative planned-session population exists outside the current projections.
The N.I.N.A. logs are now identified as an observed-activity source, not that
planned-session population. The owner has confirmed there is no incident
register. If no already-approved source is found, stop before creating one: a new authoritative
register, a recurring EAGLE writer, or publication of operational events
requires separate owner/architecture authorization and its own
safety/privacy/release gates.
Only after a source and population are approved may a non-numeric descriptive
baseline plan be considered. Numeric SLI/SLO thresholds remain explicitly deferred.

No device data was collected, no runtime was contacted, and no scheduler, writer,
alert, command path or authority was changed.

## References

- `docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md`
- `docs/architecture/packages/AP-004-Enterprise-Telemetry-and-Observability-Architecture.md`
- `docs/architecture/packages/AP-007-Enterprise-Operations-and-Service-Management-Architecture.md`
- `docs/architecture/telemetry/BKL-030-G6-EAGLE-Health-History-Persistence-Design.md`
- `docs/architecture/telemetry/evidence/BKL-030-G6-Runtime-OAT-2026-09-04.md`
- `docs/architecture/reviews/ARB-BKL-030-G6-Independent-Review-2026-09-04.md`
- `docs/architecture/alarm-and-incident-model.md`
