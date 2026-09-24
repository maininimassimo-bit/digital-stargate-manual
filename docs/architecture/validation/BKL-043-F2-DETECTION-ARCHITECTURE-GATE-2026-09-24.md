# BKL-043 F2 — System Detection Architecture Gate

| Field | Value |
|---|---|
| Gate ID | `M-BKL043-F2-DETECTION-ARCHITECTURE` |
| Status | Repository-evidence architecture proposal prepared; owner/ARB disposition pending; implementation not authorized |
| Package | BKL-043 Observatory Reliability Engineering |
| Owner / accountable | Massimo Mainini |
| Authority | Architecture-design only; command/execution/safety `NONE` |
| Authorization | Owner authorization received 2026-09-24 |

## Objective

Define and review an architecture for a possible system-wide observability and
reliability-detection tool, potentially started when the EAGLE host boots. The
gate must determine whether available component signals can support meaningful
availability, failure, MTBF, and MTTR observations, and specify how gaps and
unknown states will be represented. A host-start trigger alone is not evidence
that the whole observatory is healthy or continuously observed.

The accepted N.I.N.A. attempt definition remains bounded: an attempt exists only
when activity is recorded in an N.I.N.A. log; planned sessions with no recorded
N.I.N.A. activity are excluded. Any future statistic using this population must
be labelled as N.I.N.A.-observed and must not be called a planned-session
completion rate.

## Scope of this gate

Architecture/design work only. The review package must compare viable options
and document:

1. **System boundary and ownership:** included components (for example EAGLE,
   N.I.N.A., network, power, weather and dome), accountable source for each,
   and explicit exclusions.
2. **Detection sources and contracts:** existing read-only interfaces,
   heartbeat/observation cadence assumptions, source identity, timestamp and
   quality metadata, freshness limits to be decided later, and behavior when a
   source is absent or unreachable.
3. **State and event semantics:** healthy/degraded/unknown/unavailable
   distinctions; fault identity and correlation; duplicate/retry handling;
   detection, acknowledgement, restoration and closure transitions; and which
   transitions require human confirmation.
4. **Time and exposure model:** UTC and monotonic-clock use, clock drift and
   reboot handling, observation coverage intervals, and valid denominators for
   any future MTBF/MTTR computation. No numeric targets are set by this gate.
5. **Persistence and recovery:** whether a local append-only journal is needed,
   durability across restart/power loss, idempotent replay, corruption handling,
   retention, backup/export and recovery behavior.
6. **Isolation and security:** least privilege, read-only source access, local
   data protection, update/uninstall/rollback, resource impact, and assurance
   that the detector cannot reach command, scheduler, remediation or safety
   authority paths.
7. **Failure modes and validation:** missed/false detections, collector or
   storage failure, EAGLE offline intervals, network partitions, source clock
   errors, and offline/synthetic tests that demonstrate fail-closed behavior.
8. **Operations and lifecycle:** boot/start behavior, service ownership,
   diagnostics, maintenance, and explicit separation between a design approval
   and any later pilot/runtime authorization.

## Explicit exclusions

This gate does not authorize or perform a collector implementation, service or
scheduled task installation, automatic startup, recurring polling, live device
or network probes, persistent operational event writes, alert/notification
routing, cloud deployment/promotion, or changes to telemetry publishers. It
does not establish an incident register, reliability baseline, service SLI/SLO,
failure budget, numeric threshold, or operational MTBF/MTTR result. It does not
alter command or safety authority.

Throughout this gate:

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

## Entry evidence

- BKL-043 F1 source inventory and population/contract gap discovery.
- Repository N.I.N.A. log inventory and the owner's accepted observed-attempt
  definition.
- BKL-030 G6 manual persistence OAT, explicitly not evidence of continuous
  uptime or a recurring writer.
- Owner confirmation that no observatory incident register is currently
  available.

## Exit criteria

The gate may pass only when an architecture review records an explicit decision
(approved, conditionally approved, or returned for revision) and the package
contains:

- a system-boundary and source-eligibility matrix with unknown/unavailable
  handling;
- proposed event and incident lifecycle semantics, including clock quality,
  coverage gaps, deduplication and human-confirmed restoration rules;
- a data-flow and trust-boundary diagram, threat/privacy review, and persistence
  and recovery decision;
- offline validation cases and measurable acceptance criteria for a future
  read-only pilot;
- operational ownership, maintenance, rollback and resource-impact analysis;
- a separate, explicit follow-on gate for any implementation, startup
  installation, recurring writer, or live data collection.

Passing this architecture gate alone will not authorize the follow-on runtime
gate. Any numeric MTBF/MTTR result remains deferred until eligible source
coverage, event semantics, exposure denominators and representative evidence
have been validated.

## Current disposition

The gate is created and owner-authorized for architecture work. The evidence-
based proposal is recorded in
`docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`.
The recommended two-plane design is proposed, not accepted. Owner/ARB disposition
and any required independent review remain pending. No implementation has been
started and no live source has been contacted.
