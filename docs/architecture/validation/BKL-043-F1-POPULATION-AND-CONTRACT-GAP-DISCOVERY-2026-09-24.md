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
| Fault frequency / MTBF | Validated fault taxonomy; event identity and correlation; repeat/duplicate rules; eligible service exposure interval; inclusion/exclusion policy | Not measurable; no fault population or exposure denominator. |
| Acknowledgement / restoration / MTTR | Populated incident lifecycle with reliable detected, acknowledged, restored/resolved and closed transitions; reopen and clock-quality semantics; service linkage | Not measurable; draft process model is not operational event evidence. |
| Failure budget / SLO | Approved SLI definition, measured representative baseline, observation window and accountable service owner | Not defined; AP-007 requires measurement before SLO deliberation. |

These are contract-completeness prerequisites derived from AP-004/AP-007 and
existing repository evidence. They are not a proposed schema, target, service
cadence or authorization to create a live source.

## Safe next gate

Continue repository-only analysis to identify whether an already approved,
authoritative planned-session or incident population exists outside the current
projections. If none is found, stop before creating one: a new authoritative
register, a recurring EAGLE writer, or publication of operational events requires
separate owner/architecture authorization and its own safety/privacy/release gates.
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
