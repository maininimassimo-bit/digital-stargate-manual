# BKL-043 F1 — Reliability Source Discovery

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F1-SOURCE-DISCOVERY-2026-09-24` |
| Status | Source inventory completed; reliability baseline not yet measurable from eligible current evidence |
| Package | BKL-043 Observatory Reliability Engineering |
| Baseline | `ec17c69cbf350b4952e781525b782128ed293a22` |
| Dependencies | BKL-030, BKL-038 and BKL-042 bounded scope accepted |
| Authority | Repository-only, descriptive, read-only; command/execution/safety `NONE` |

## Purpose and boundary

This first increment inventories existing repository evidence against the BKL-043
candidate metrics. It does not calculate SLO attainment, failure budget, observatory
uptime, fault rate, MTBF, MTTR or weather-vs-technical lost-night rates. Candidate
SLIs are not approved measures until population, event semantics and observation
window are validated. AP-007 explicitly requires measured baseline before SLO
deliberation and prohibits invented numeric thresholds.

## Source inventory

| Source | Observed contents | Reliability disposition |
|---|---|---|
| `docs/data/scientific-session-catalog.json` | Versioned historical analytics projection; 22 sessions, 7 `VALIDATED_ANALYTICS`, 15 `ATTENTION_REQUIRED`; includes session window, integration, light counts and `completionPct` | Descriptive session-history candidate only. No planned-session denominator, declared failure event, service uptime window or incident lifecycle. `ATTENTION_REQUIRED` is analytics state, not an operational fault. |
| `docs/data/session-comparison-projection.json` | BKL-037 historical SQM set, 15 included and 7 excluded records | Scientific comparison, unrelated to service availability or reliability. Explicitly descriptive; no ranking/quality threshold. |
| `docs/data/realtime/eagle-health.json` | Public read-only projection reports `UNAVAILABLE` / `UNKNOWN` / `NO_CURRENT_SNAPSHOT`; zero signals and null observation time | No current health or availability evidence; must remain unknown/unavailable. |
| `docs/data/bkl-036-f4-telemetry-archive.json` | Seven-domain repository archive labelled `repository_archived_snapshot`, synthetic offline fixture, no live transport | Test fixture only; excluded from operational baseline and incident counts. |
| `docs/data/integration/session-completed-shadow-event-2026-09-21_2026-09-22.json` and `contracts/events/observation-session-completed-shadow-v1.schema.json` | One repository-shadow integration artifact; schema states `SHADOW_VALIDATED`, internal classification and `runtime_published=false` | Contract/shadow proof, not a population-complete production event stream. Cannot establish session success rate or telemetry availability. |
| `docs/architecture/alarm-and-incident-model.md` (OPSC-ALM-001) | Draft alarm/incident lifecycle and candidate timestamps/identifiers | Semantics are draft; no correlated observatory incident population with detected/acknowledged/restored timestamps was found in reliability datasets. Not usable for MTBF/MTTR. |
| `docs/architecture/telemetry/BKL-030-G6-EAGLE-Health-History-Persistence-Design.md` | Prior design; explicitly defers MTBF/MTTR/SLO to BKL-043 | Design reference only; no persistent live history writer or current source values are supplied by this artifact. |
| `infrastructure/bkl031-f3-a3-gcp/platform/*INCIDENT*.json` | Governed CI/runner/platform execution incidents | Different service population; do not merge into observatory/device reliability statistics. |

## Candidate metric eligibility

| Candidate | Finding |
|---|---|
| Telemetry/service availability | Not measurable: no eligible continuous observation/heartbeat intervals, agreed service boundary or complete outage ledger. |
| Session completion | Historical `completionPct` exists, but no authoritative planned-session denominator or cancelled/lost-night disposition; descriptive per-record only. |
| Fault frequency / MTBF | Not measurable: no complete, correlated observatory fault-event population and exposure-time denominator. |
| MTTR / recovery time | Not measurable: no eligible incident lifecycle records with validated detection, acknowledgement, restoration and closure times. |
| Weather vs technical lost nights | Not measurable: no complete planned-night population with mutually exclusive, owner-validated loss reason. |
| Failure budget / SLO | Not defined. No numeric target or threshold is inferred; AP-007 requires a measured baseline before deliberation. |
| Telemetry freshness compliance | Current EAGLE projection is unavailable/unknown and historical archive is synthetic; no rate is computed. |

## Decision and next safe increment

The repository supports candidate definitions and historical descriptive session
facts, but does not support an operational reliability baseline. Continue with
source-contract discovery and event-population completeness only. Do not collect
device data, start a live writer, create an alert, publish current health claims,
select thresholds or alter hardware/authority paths. Any metric requiring a numeric
target, a safety/readiness interpretation, or a new live source stops for owner
decision and the applicable architecture/review gate.

## References

- `docs/project/BACKLOG.md` — BKL-043 and BKL-050 sequencing.
- `docs/project/FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md` — BKL-043 candidate metrics.
- `docs/architecture/packages/AP-004-Enterprise-Telemetry-and-Observability-Architecture.md` — measured baseline and telemetry boundary.
- `docs/architecture/packages/AP-007-Enterprise-Operations-and-Service-Management-Architecture.md` — SLI/SLO candidate list; thresholds after measured baseline.
- `docs/architecture/alarm-and-incident-model.md` — draft event and incident lifecycle.
- `docs/project/BKL-042-CLOSURE-2026-09-24.md` — accepted predecessor scope.
