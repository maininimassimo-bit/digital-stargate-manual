# BKL-043 F4 — Exact Pilot Runtime Authorization (Decision Draft)

| Field | Value |
|---|---|
| Gate ID | `M-BKL043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION` |
| Status | **PREPARATION ONLY — SELECTED DESIGN DECISIONS RECORDED; EXACT RUNTIME AUTHORIZATION PENDING** |
| Owner / accountable | Massimo Mainini |
| Predecessor disposition | F3 approved for preparation of a separate exact authorization on 2026-09-24 |
| Authority | Repository-only design; `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

## 1. Purpose and authorization boundary

This draft converts the F3 owner disposition into a distinct runtime decision
template. It is not an implementation plan and does not authorize a pilot,
installation, live source access, polling, a boot trigger, persistent writes,
remote heartbeat, incident registration, network egress or deployment.

The F3 disposition authorizes preparation of this gate only. Every field below
must be resolved, reviewed and explicitly approved by the owner before any
runtime preflight or change. `UNSELECTED` is a stop condition, not permission to
inherit a historical default.

## 2. Candidate scope for owner decision

The stated objective is measuring reliability of the whole observatory system.
The F2 design therefore describes two logical planes: an EAGLE-local observer
and a separately durable witness outside the EAGLE failure domain. Massimo
Mainini selected the two-plane pilot scope for this gate on 2026-09-24. This is a
scope decision only; it does not select a deployable implementation or authorize
runtime activity. The owner selected GitHub as the witness-provider candidate;
the exact private repository/service, durable receipt mechanism, access model,
failure-domain evidence, transport and retention remain unselected. The existing
`maininimassimo-bit/digital-stargate-manual` repository is public and is not an
authorized destination for runtime receipts or operational telemetry.

The incident lifecycle remains excluded: OPSC-ALM-001 is a draft and no incident
register exists. N.I.N.A.-logged activity remains the candidate attempt
population; raw logs are not to be copied into telemetry records. Historical
logs may be used only within the already bounded repository/offline analysis
scope, not as live runtime authorization.

## 3. Exact owner decisions required

| Decision field | Current proposal / evidence | Owner decision |
|---|---|---|
| Pilot scope | Owner selected two-plane observer plus independent witness on 2026-09-24; this selects scope, not runtime activation | **SELECTED — TWO-PLANE; runtime remains unauthorized** |
| Target host and environment | `EAGLE30154`; source-discovery evidence recorded Windows 10 Enterprise LTSC `10.0.17763` x64 as verified on 2026-09-03. This is a historical baseline, not current identity/OS attestation; maintenance window is not documented. | **TARGET SELECTED — EAGLE30154; historical OS baseline recorded; current host/OS confirmation and window UNSELECTED** |
| Service identity and operator | Least privilege is mandatory; no new identity selected | **UNSELECTED** |
| Software artifact and configuration | F3 schema/validator are contract tests, not a runtime collector; implementation and immutable artifact digest do not exist | **UNSELECTED** |
| Included sources/components | Candidate source-owned projections only; no live producer/read-only boundary has been revalidated for this pilot | **UNSELECTED** |
| N.I.N.A. logs | User confirmed logs are available; parsing, event grouping, retry/terminal semantics and population reconciliation are not accepted | **OFFLINE ANALYSIS ONLY; runtime ingestion unselected** |
| Planned EAGLE shutdown evidence | Owner selected a local shutdown-event approach on 2026-09-25. A locally recorded orderly shutdown can evidence shutdown mode/time, but alone does not prove prior planning or rule out an operational incident. | **DESIGN POLICY SELECTED: record local shutdown event; classify intent only with independent supporting evidence or human review; otherwise UNKNOWN** |
| Historical EAGLE operating hours | Windows System event logs are a candidate source for reconstructing host boot/shutdown intervals; actual log contents have not been inspected or imported. Host uptime is not equivalent to observatory availability or scientific session time. | **OFFLINE RECONCILIATION CANDIDATE ONLY; source selection, event semantics, completeness and import approval pending** |
| Production-script health monitoring extension | On 2026-09-25 Massimo Mainini requested that the EAGLE monitoring design also cover scheduled health checks for all scripts currently in production. Repository-only evidence and open population boundaries are documented in `BKL-043-F4-PRODUCTION-SCRIPT-HEALTH-EXTENSION-DRAFT-2026-09-25.md`; no current production inventory is verified. | **OWNER REQUEST RECORDED — DESIGN ONLY; exact population, execution locations/triggers, schedule policies, authoritative run/outcome evidence and missed-run semantics remain unselected. No scheduled check, script execution, task/service installation, or live EAGLE inspection is authorized.** |
| Independent witness | Owner selected GitHub as provider candidate on 2026-09-24. Official GitHub documentation states scheduled workflows have a five-minute minimum and may be delayed or dropped; event-driven runs cannot detect absent events. A private repository could be an archive, but GitHub Actions alone is not an accepted bounded-latency witness. Existing public manual repository is excluded. | **GITHUB SELECTED AS CANDIDATE; archival-vs-independent-receiver disposition, exact private resource, receipt-time contract and failure-domain proof UNSELECTED; see F4 feasibility assessment** |
| Transport, authentication and egress | No endpoint, protocol, credential, network rule or secret provisioning approved | **UNSELECTED** |
| Sampling/heartbeat cadence, timeout, freshness and gap semantics | Historical producer cadence is not transferable; no approved values | **UNSELECTED** |
| Start mode | User-originated concept mentioned starting with EAGLE; F2/F3 do not authorize boot-start, scheduled task or recurring execution | **UNSELECTED** |
| Observation window/checkpoints | No duration or start/end selected | **UNSELECTED** |
| Local/remote data stores | No journal, database or hosted store approved | **UNSELECTED** |
| Data classification, roles, encryption and backup | Minimum-data design exists; target-specific controls not reviewed | **UNSELECTED** |
| Retention/deletion/disposal | No duration, deletion procedure or approver selected | **UNSELECTED** |
| Resource budget and stop limits | Must be measured against an agreed imaging workload; no numeric limits approved | **UNSELECTED** |
| Cost ceiling and billing controls | Preliminary scenarios are recorded in `BKL-043-F4-COST-ESTIMATE-2026-09-25.md`; account plan, quota remaining, billing owner, approved products/region and caps are unknown | **UNSELECTED — no spending or resource creation authorized** |
| Installation, disable, uninstall and rollback | Must be exact for the selected artifact/host; not prepared for runtime | **UNSELECTED** |
| Security/privacy review | Required before any live access or persistence; a separate scoped finding is still required | **PENDING — not covered by the draft-quality approval below** |
| Independent architecture and release-quality review | Leonardo Di Egidio was nominated by the owner on 2026-09-24. On 2026-09-25 Massimo Mainini reported Leonardo's approval of the quality of the BKL-043 F4 drafts. Massimo remains accountable owner and runtime approver, not an independent reviewer of his own decision. | **DRAFT QUALITY APPROVED (owner-reported); full exact-runtime ARB/Release Quality review remains pending** |
| OAT and acceptance criteria | Must be tied to exact sources, coverage, stop conditions and rollback | **UNSELECTED** |
| Incident lifecycle | Separate contract and authorization required; current default excludes it | **EXCLUDED** |

## 4. Required evidence before the runtime decision can be submitted

1. Close the F3 review findings and preserve the offline test evidence.
2. Complete the selected scope and host definition: verify `EAGLE30154`, record
   its OS/build and maintenance window, then select identity, artifact and
   components.
3. Prove every selected source is available through an exact read-only interface;
   exclude direct device probing and command-capable credentials.
4. Define the local shutdown record contract, its provenance and failure cases.
   It must not infer planned intent from an orderly shutdown alone; unknown
   intervals remain `UNKNOWN` unless independently corroborated or human
   classified. Design offline reconciliation of candidate Windows System
   event logs with N.I.N.A. attempts and other evidence; do not equate host
   uptime with observatory availability or science hours. No actual EAGLE log
   access/import is authorized by this draft. The repository-only proposal is
   `BKL-043-F4-SHUTDOWN-EVIDENCE-AND-HISTORICAL-RECONCILIATION-DRAFT-2026-09-25.md`;
   its recording mechanism and any real historical snapshot still require
   separate owner authorization.
5. Continue the owner-requested production-script health extension using the
   repository-only design in
   `BKL-043-F4-PRODUCTION-SCRIPT-HEALTH-EXTENSION-DRAFT-2026-09-25.md`. Resolve
   whether the scope includes EAGLE-local scripts only or external production
   workflows/services too, identify the authoritative inventory and run
   evidence, and define trigger-specific expected-run/missed-run semantics.
   EAGLE is not always on, so absence of a local result must remain `UNKNOWN`
   unless a separately governed witness bounds the relevant receipt gap. Script
   execution health is separate from host uptime, observatory availability and
   scientific activity; it is not a qualifying MTBF failure without accepted
   event and exposure semantics. This request does not authorize live inventory,
   polling, script execution, a scheduled task, persistence, transport, alerting
   or deployment.
6. Close `BKL-043-F4-GITHUB-WITNESS-FEASIBILITY-2026-09-25.md`: owner selects
   the best-effort GitHub archive limitation or a separate independent receiver;
   then demonstrate a durable receipt store outside EAGLE's host, power and
   network failure domains.
7. Define data minimization, privacy/security controls, retention/deletion,
   resource stop limits, observation window and review checkpoints.
8. Review the indicative cost scenarios in
   `BKL-043-F4-COST-ESTIMATE-2026-09-25.md`; verify account plan and quotas,
   then set explicit recurring and one-time cost ceilings, billing owner,
   approved products/region, and stop action. No spend is approved by the
   estimate itself.
9. Specify install/start/stop/uninstall/rollback and recovery verification.
10. Complete Leonardo Di Egidio's independent architecture/release review and
   security/privacy review, plus offline and resource preflight evidence. The
   preflight must not access live sources until separately authorized.
11. Submit a final decision record with every field exact and no `UNSELECTED`,
   then wait for explicit owner approval naming that exact record/version.

## 5. Fixed constraints

### Review disposition — draft quality only (2026-09-25)

Massimo Mainini reported that Leonardo Di Egidio approved the quality of the
BKL-043 F4 drafts. This disposition covers the draft-quality review only; it
does not constitute a GitHub PR review record, security/privacy finding, approval
of an exact runtime design, or authorization to access EAGLE, read real logs,
install or run software, spend, or deploy. The full exact-runtime ARB and Release
Quality gates remain open until their exact scope and evidence are reviewed.

```text
review_scope=draft_quality_for_BKL-043_F4
reviewer=Leonardo_Di_Egidio
review_disposition=approved_as_reported_by_Massimo_Mainini
runtime_authorization=NONE
```

- No device commands, control path, broker, decision scheduler, remediation,
  alert, interlock change, readiness decision or Safety Authority.
- No automatic incident creation or closure; no incident register in this gate.
- Unknown, stale, missing, conflicting and unobserved intervals remain unknown.
- An orderly local shutdown record alone is not proof of planned downtime and
  does not by itself classify an interval as non-incident. Host uptime,
  observatory availability and scientific operating time are distinct measures;
  historical uptime must not be converted to MTBF/MTTR without reconciled,
  coverage-qualified event populations and accepted semantics.
- No whole-system uptime, availability, MTBF, MTTR, SLI/SLO or failure-budget
  claim until the population, denominator, event semantics and coverage are
  separately accepted and validated.
- No runtime operation, pilot deployment or live data access is authorized by
  this draft or by the F3 preparation disposition.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

## References

- `docs/architecture/validation/BKL-043-F3-READONLY-PILOT-READINESS-GATE-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F3-PILOT-SPECIFICATION-DRAFT-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F3-EXACT-PILOT-AUTHORIZATION-DECISION-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-POPULATION-AND-CONTRACT-GAP-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F4-GITHUB-WITNESS-FEASIBILITY-2026-09-25.md`
- `docs/architecture/validation/BKL-043-F4-COST-ESTIMATE-2026-09-25.md`
- `docs/architecture/validation/BKL-043-F4-SHUTDOWN-EVIDENCE-AND-HISTORICAL-RECONCILIATION-DRAFT-2026-09-25.md`
- `docs/architecture/validation/BKL-043-F4-PRODUCTION-SCRIPT-HEALTH-EXTENSION-DRAFT-2026-09-25.md`
- `docs/status/index.md` — identifies the documented EAGLE evidence host as
  `EAGLE30154`; does not establish OS/build or validate current machine identity.
- `docs/architecture/telemetry/evidence/BKL-030-EAGLE-Health-Source-Discovery-2026-09-03.md`
  — records the historical `EAGLE30154` OS baseline as Windows 10 Enterprise
  LTSC `10.0.17763` x64; reconfirmation is required before runtime activity.
- GitHub repository visibility check on 2026-09-24: `maininimassimo-bit/digital-stargate-manual`
  is public; it is explicitly excluded as a destination for pilot telemetry.
