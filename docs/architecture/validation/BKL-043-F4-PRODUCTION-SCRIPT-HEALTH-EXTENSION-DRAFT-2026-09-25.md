# BKL-043 F4 — Production Script Health Monitoring Extension (Draft)

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F4-PRODUCTION-SCRIPT-HEALTH-EXTENSION-DRAFT-2026-09-25` |
| Gate | `M-BKL043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION` |
| Status | Owner-selected repository-wide production-script scope; static inventory incomplete; no runtime monitoring authorized |
| Owner / accountable | Massimo Mainini |
| Authority | `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

## 1. Owner request and purpose

On 2026-09-25 Massimo Mainini requested that the planned EAGLE reliability
monitoring be extended to include scheduled health checks for **all scripts
currently in production across Digital StarGate**. The owner clarified on
2026-09-25 that this includes production scripts beyond the EAGLE-local boundary,
including externally hosted workflow execution where the executed unit is a
script. This scope choice does not make the production population known or
authorize any check. Hosted services that are not scripts are not themselves
script inventory entries; whether their health is a dependency signal is a
separate design decision.

The monitoring must observe execution evidence; it must not rerun a script,
change its schedule, restart a failed process, or infer that a script is healthy
because EAGLE or another host is reachable. A host-local check cannot run while
EAGLE is off. A missing result is therefore not, by itself, proof of a script
failure, planned downtime, observatory unavailability, or healthy operation.

This extension remains within BKL-043's descriptive, read-only design boundary.
It does not approve a collector, scheduler, recurring query, persistence,
transport, alert, remediation or runtime rollout. EAGLE access, live scheduler
inventory and real execution logs remain outside this draft and require separate
explicit authorization.

## 2. Repository evidence and inventory limits

The following are repository-visible candidates, not a verified current list of
production scripts:

| Candidate family | Repository evidence | Current qualification |
|---|---|---|
| EAGLE Task Scheduler entries | BKL-030 G1 records a historical `Scheduled Tasks DSG` source. The EAGLE health projection contract exposes task name/path, state, last/next run and raw `last_task_result`; `result_classification` is null. The current collector source shown in `scripts/telemetry/Export-EagleHostHealth.ps1` selects tasks whose names match `Digital StarGate*`. | A partial, source-specific read-only contract exists. It does not prove the full production task population or govern task-specific success/failure semantics. |
| `Daily Session Upload` and `OneDrive Export` | Named in the 2026-09-03 EAGLE source-discovery record as tasks visible during that historical discovery. | Historical task-name evidence only; it does not establish current installation, production ownership, exact action/script, trigger, current status or run history. |
| EAGLE health collector/history scripts | `Export-EagleHostHealth.ps1` and `Write-EagleHealthHistory.ps1` implement source collection and history writing. BKL-030 G6 records a bounded manual persistence OAT and explicitly says no permanent Scheduled Task or service was activated. | Validated component scripts, but no recurring production schedule is established by that OAT. Do not count the manual OAT as a production schedule. |
| Observatory status telemetry scripts | Repository contains producer, publisher, installer and startup-task scripts under `scripts/telemetry/`. | File presence and historical commissioning do not prove which versions/tasks are installed now or whether each is classified as production. |
| Scheduled GitHub Actions production workflows | `.github/workflows/bkl-031-f9-refresh.yml` defines scheduled runs and invokes the F9 refresh script on GitHub-hosted runners. | A possible external production execution source, distinct from EAGLE-local scripts. Whether it belongs in the owner's requested inventory is an unresolved boundary decision. GitHub schedule/run history does not provide a bounded-latency EAGLE witness. |
| CI, test, inspection and deployment helpers | Repository contains many `.github/scripts/`, test scripts, source inspectors, installers and manual-only workflows. | Exclude from the production population unless an authoritative owner/source explicitly identifies a production execution. Repository presence alone is insufficient. |

This repository inventory cannot establish the live contents of Task Scheduler,
the installed script versions, external schedulers, current run history, or
whether a given task is enabled. The current exact population is therefore
`UNKNOWN / NOT INVENTORIED`; do not publish an inventory-completeness claim.

### 2.1 Static source-to-execution evidence map

This map makes the repository evidence more specific without treating historical
reports as current runtime verification:

| Execution candidate | Repository-visible entry point | Last documented evidence found in this repository | What remains unverified |
|---|---|---|---|
| EAGLE Health publisher | `DigitalStarGate-EagleHealthTelemetry` is documented with wrapper `scripts/telemetry/Invoke-EagleHealthTelemetryPublish.ps1`, which composes `Export-EagleHostHealth.ps1`, `Export-EagleHealthPortalProjection.ps1` and `Publish-EagleHealthTelemetry.ps1`. | `HANDOVER_2026-09-22-AP-008-BKL-036.md` reports that the task pointed to the AP-008 worktree and had `LastTaskResult = 0`; the 2026-09-04 baseline records a one-minute schedule. | Current task definition, enabled state, action path/revision, task history and present execution state. The report is documentary evidence dated 2026-09-22, not a fresh host observation. |
| Observatory Status publisher | Installer `scripts/telemetry/Install-ObservatoryStatusTelemetryScheduledTask.ps1` defines a default task name and boot trigger; its runtime launcher is `Start-ObservatoryStatusTelemetryRuntime.ps1`, composing the producer, N.I.N.A./CloudWatcher adapters and publisher. | `CURRENT_TECHNICAL_BASELINE_2026-09-22.md` reports an EAGLE Scheduled Task continuously publishing Observatory Status and successful continuous read-back at that time. | Whether the reported task is the installer default, whether it remains installed/enabled, which scripts/revision it runs now, and current run receipts. Installer code alone does not prove it was executed or remains installed. |
| Session upload / reporting | Historical handovers name `DigitalStarGate - Daily Session Upload` and the preflight `scripts/eagle/Invoke-DSGSessionPreflight.ps1`; downstream action/artifact boundaries require confirmation from the authoritative installed task definition. | `HANDOVER_2026-09-03.md` reports a successful upload for the 2026-09-02/03 session. | Current task presence, exact launcher/action, cadence, current production owner and run history. This historical single execution is not a present health signal. |
| OneDrive export | No authoritative repository action mapping was identified in this static pass. | The 2026-09-03 source-discovery record lists `OneDrive Export` among the tasks observed during that historical discovery. | Current presence, action/script identity, intended schedule, owner and results; keep as unresolved task candidate only. |
| GitHub-hosted forecast refresh | `.github/workflows/bkl-031-f9-refresh.yml` invokes `.github/scripts/observation_planner_f9.py` on two UTC schedules, with `workflow_dispatch` also available. | The workflow file defines these triggers and guards the job on `main` plus `F9_ZERO_EUR_GUARD == CONFIRMED`; its existence establishes configuration, not current guard value or successful/expected runs. | Whether external GitHub workflows/services belong in the requested population; current guard/runner state and source run evidence. Scheduled Actions remains unsuitable as a bounded-latency EAGLE witness. |
| N.I.N.A. dome telemetry exporter | `.github/workflows/nina-dome-telemetry-exporter.yml` builds an exporter artifact and runs a regression check for push, pull request or manual dispatch. | The workflow proves a repository CI/build path only. | It does not prove plugin installation, activation, or execution in N.I.N.A.; include only if an authoritative production inventory confirms the deployed plugin and its run evidence. |
| Analytics Center synchronization | `.github/workflows/analytics-center-sync.yml` calls `.github/scripts/refresh-analytics-center.sh`, writes generated views, pushes to `main`, then dispatches Pages deployment. | The repository configures `push` and `workflow_dispatch` triggers and write/deploy steps. | Whether the workflow is part of the accepted production-script population, its expected-run semantics, and run outcomes for the relevant period. A push-triggered workflow has no fixed periodic cadence. |
| Session analysis/projection pipeline | `.github/workflows/analyze-session-automatic.yml` invokes multiple `.github/scripts/` generators and validators on session-manifest pushes or manual dispatch. | The repository configures event-driven and manually triggered execution with write-capable generated projections. | Per-script production ownership, expected trigger population, successful output consumption and run evidence; do not turn a missing event into a missed periodic run. |
| Governed projection sync | `.github/workflows/roadmap-projection-sync.yml` runs roadmap/status generators on pushes or manual dispatch and may commit generated projections. | Workflow trigger and action definitions are repository-visible. | Whether each generator is a production script or governance/maintenance automation; current usage and per-run receipts. |
| Session package promotion | `.github/workflows/promote-session-package.yml` runs on session-branch pushes and promotes validated packages to `main`. | Workflow definition shows an event-driven promotion path. | Whether to inventory as a production script or release pipeline, its event population and authoritative per-run evidence. |
| Pages publication | `.github/workflows/deploy-pages.yml` builds and publishes the public manual on `main` pushes, explicit dispatch or selected workflow completion. | Workflow definition identifies an external production publishing path. | Whether publishing scripts belong in the health-monitoring population or release governance only; no periodic cadence is implied. |
| Other gated BKL-031 F3-A3 workflows | Multiple workflow files contain schedule and/or manual triggers for exact acquisition, infrastructure, execution or recovery operations. | Repository-visible workflow configuration only. | Do not classify them as ordinary production health checks. Their authorization, active state, ownership and production status require separate governance evidence; do not dispatch or execute them as part of inventory discovery. |

The latest time-stamped production-oriented repository record found in this pass
is the 2026-09-22 handover. The owner has selected the population boundary as all
Digital StarGate production scripts, including scripts executed outside EAGLE.
The exact production classification for event-driven pipelines, release
automation, and scripts supporting hosted services still needs review. All
entries above need a dated, authoritative current inventory snapshot before they
can be called the complete population “currently in production.” Do not query
Task Scheduler, workflow secrets/variables, live run history, EAGLE or remote
services as part of this repository-only pass.

## 3. Proposed inventory and run-evidence fields

Before defining a health rule for any script, create a controlled inventory with
at least:

| Field | Purpose |
|---|---|
| `script_id`, `display_name`, `owner` | Stable identity and accountable owner; do not rely on a file name alone. |
| `execution_boundary`, `host_or_service_id` | Distinguish EAGLE-local, other host, GitHub Actions or another approved runtime. Keep private host/path detail out of public projections. |
| `artifact_version_or_digest` | Identify which script revision actually ran; missing identity prevents version-specific health claims. |
| `trigger_type`, `expected_schedule_source` | Distinguish timer, startup, event, manual and dependency-triggered runs. A script may have no fixed interval. |
| `expected_run_policy`, `grace_policy` | Define when an execution is due and how lateness is treated. Both remain unselected until the population and operating policy are reviewed. |
| `execution_evidence_source` | Name the authoritative scheduler/workflow/run receipt and its read-only access boundary. Self-reported script output alone is not sufficient proof that a run began or completed. |
| `run_id`, `started_at`, `completed_at`, `result`, `exit_code` | Attribute each execution and preserve raw source outcomes before any governed classification. |
| `output_evidence`, `output_freshness`, `dependency_refs` | Determine whether the run produced the expected bounded output and expose dependency/monitoring gaps without copying raw logs or secrets. |
| `source_time_quality`, `coverage_state`, `evidence_ref`, `payload_digest` | Preserve timestamp quality, missing coverage and provenance for reconciliation. |

Inventory records and runtime evidence must not contain credentials, arbitrary
arguments/environment, raw log bodies, personal data or unnecessary local file
paths. Any private evidence locator remains in its approved store and is not
copied to the public manual repository.

## 4. Proposed status semantics — not accepted policy

These labels are design candidates only. They do not set cadence, lateness
thresholds or alert severity:

| Candidate status | Minimum evidence | Interpretation limit |
|---|---|---|
| `SUCCESS_OBSERVED` | An authoritative scheduler/workflow receipt identifies the script revision and run, reports completion and a source-defined successful result. | Proves only that execution result was recorded. It does not prove the observatory or scientific activity was successful. |
| `FAILURE_OBSERVED` | An authoritative run receipt reports a non-success result under a reviewed, script-specific result mapping. | A failed script run is not automatically a qualifying observatory fault or MTBF failure. |
| `SKIP_OBSERVED` | The authoritative source records an intentional skip and its governed reason. | Absence of a run is not an observed skip. |
| `LATE_OR_MISSING_CANDIDATE` | A reviewed expected-run policy and grace period exist, and the designated evidence source is known to be available through the interval. | Candidate missing execution only. If host or evidence-source availability is unknown, the result remains `UNKNOWN`. |
| `HOST_OFF_OBSERVED` | Separately validated host shutdown/offline evidence with adequate identity, epoch and time quality. | Does not classify a script as failed or the interval as planned downtime; it explains a possible coverage gap only. |
| `CONFLICTING` | Competing receipts, reused run identity with changed content, or incompatible source times/results. | Preserve lineage; do not choose last-write-wins. |
| `UNKNOWN` | No authoritative receipt, unavailable source, uncertain host state, uncovered time, or missing policy needed to classify the observation. | Never convert to success, failure, planned downtime, or healthy observatory state by default. |

## 5. Coverage and reliability boundaries

- Host uptime, observatory availability, scientific activity and script execution
  status are separate evidence dimensions.
- EAGLE commonly being shut down means local-only checks have no coverage while
  the host is off. A missing local record must remain `UNKNOWN` unless a
  separately governed source bounds the relevant receipt gap. Even then, the
  witness bounds receipt visibility, not cause or exact failure onset.
- The GitHub feasibility assessment remains binding: scheduled Actions can be
  delayed or dropped and are not an accepted bounded-latency witness. Actions
  history may be an execution receipt for a GitHub-hosted script only if the
  script is explicitly included in the approved inventory.
- Do not aggregate script failures into host uptime, availability, incident
  count, MTBF or MTTR without separately accepted fault taxonomy, event
  correlation, eligible exposure denominator, coverage floor and population
  rules. No result may be labelled “MTBF” solely from the sum of script runtime
  or host-on hours.
- A successful check of a script's scheduler metadata is not proof that the
  script itself ran successfully. A script run result is not proof that its
  output was consumed or that downstream science succeeded.

## 6. Offline validation cases for a future contract

Use synthetic receipts only to validate:

1. successful, failed, skipped, delayed, duplicate, reordered and conflicting
   run receipts;
2. version/hash mismatch between expected and observed script artifact;
3. EAGLE intentionally off, unexpectedly absent, rebooted, or without a
   trustworthy host-state receipt;
4. missing, delayed or unavailable execution-evidence source;
5. scheduled, startup, event-driven and manual triggers without treating all of
   them as periodic;
6. output absent/stale despite a successful process exit;
7. clock shift, timezone ambiguity, missing timestamp and cross-boot ordering;
8. repeated script failure without manufacturing unique observatory incidents;
9. forbidden secret, raw-log and private-path fields in normalized records;
10. report assertions keeping host uptime, observatory availability, scientific
    activity and script execution status separate and retaining unknown gaps.

Expected result: deterministic, provenance-preserving classifications with no
network, device, EAGLE, real log, credential, scheduled task or production script
access. Synthetic validation can test semantics only; it cannot prove inventory
completeness or live source quality.

## 7. Decisions and next gate

Before a complete inventory or health check can be claimed, the owner/reviewers
must resolve:

1. owner-selected population is all Digital StarGate production scripts across
   EAGLE and external execution boundaries; decide which event-driven/release
   workflows qualify as production script executions, without counting a hosted
   service itself as a script;
2. the authoritative current inventory source and responsible owner for each
   execution boundary;
3. which receipts count as authoritative and how task-specific raw result codes
   map to success, failure, skip or unknown;
4. expected-run and lateness policies for scheduled, startup and event-driven
   scripts, including intended shutdown periods;
5. the independent coverage model when EAGLE or the receipt source is offline;
6. privacy, retention, resource, cost, installation, stop and rollback controls.

This draft selects none of those runtime decisions. It does not authorize
inspection of EAGLE, actual Task Scheduler inventory, real execution logs,
script execution, recurring checks, new writers, transport, alerts, spending or
deployment. `command_authority=NONE`, `execution_authority=NONE` and
`safety_authority=NONE` remain invariant.

## References

- `docs/architecture/validation/BKL-043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION-DRAFT-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F4-SHUTDOWN-EVIDENCE-AND-HISTORICAL-RECONCILIATION-DRAFT-2026-09-25.md`
- `docs/architecture/validation/BKL-043-F4-GITHUB-WITNESS-FEASIBILITY-2026-09-25.md`
- `docs/architecture/telemetry/BKL-030-G1-Source-Inventory.md`
- `docs/architecture/telemetry/BKL-030-EAGLE-Health-Projection-Contract.md`
- `docs/architecture/telemetry/BKL-030-G6-EAGLE-Health-History-Persistence-Design.md`
- `docs/architecture/telemetry/evidence/BKL-030-EAGLE-Health-Source-Discovery-2026-09-03.md`
- `scripts/telemetry/Export-EagleHostHealth.ps1`
- `scripts/telemetry/Write-EagleHealthHistory.ps1`
- `.github/workflows/bkl-031-f9-refresh.yml`
