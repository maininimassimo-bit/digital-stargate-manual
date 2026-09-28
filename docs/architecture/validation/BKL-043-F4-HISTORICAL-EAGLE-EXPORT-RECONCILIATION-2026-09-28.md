# BKL-043 F4 — Historical EAGLE export reconciliation (28/09/2026)

| Field | Value |
|---|---|
| Evidence ID | `BKL043-F4-HISTORICAL-EXPORT-RECONCILIATION-2026-09-28` |
| Status | Completed offline, read-only analysis of owner-supplied historical exports; redacted aggregate summary approved for publication by the owner on 2026-09-28 |
| Scope | Historical coverage and timestamp correlation only |
| Authority | `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

## 1. Summary

The available Windows System export contains records beginning on **2 October
2025** and continuing through **27 September 2026**. Its first visible record is
a System event-log-cleared marker. The export therefore provides no Windows
System history before that date, and its coverage cannot be treated as complete
across the full period.

The boot and shutdown evidence in this export reaches **23 September 2026**.
The last represented boot has no later shutdown marker in the export. Other
System events continue through 27 September; that later activity does not extend
the boot/shutdown evidence window.

The available N.I.N.A. log material has timestamped entries from **13 July to
24 September 2026**. These entries correlate with represented host epochs, but
they do not establish continuous host uptime, observatory availability, or
successful scientific operation.

## 2. Evidence and method

- The owner-supplied Windows `.evtx` export was read offline and without
  modification. It contains 26,160 records; timestamps were available for all
  records examined.
- Windows events were selected using provider and event ID together. The
  resulting evidence includes 93 represented startup anchors, 86 adjacent
  boot-to-boot transitions with an orderly-shutdown marker, and six transitions
  without that marker. Each of those six later boots has Windows indicators of
  an unclean prior shutdown. The first represented boot also has such an
  indicator, but no earlier boot is present in the export to bound that event.
- The event-log-cleared record at the start of the export is an explicit
  coverage limitation. No missing interval was classified as planned downtime,
  and no cause was inferred from an unclean-shutdown event.
- N.I.N.A. material was compared by timestamp after deduplicating identical
  content. The resulting 37,588 unique timestamped entries fall within
  represented host epochs: 37,429 within boot-to-orderly-shutdown spans and
  159 in the final open host epoch. These are timestamp correlations, not a
  count of observing attempts or successful sessions.
- Session evidence carries its own time semantics. Twenty manifest windows fall
  within represented boot-to-shutdown spans, two cross a boot marker, and one
  falls in the final open epoch. These windows do not define the complete
  attempted-session population.

Only these redacted aggregates are recorded here. The source exports, local
paths, account or user fields, machine identifiers, raw event payloads, and
source digests are not included in this public report.

## 3. Interpretation limits

This reconciliation describes the historical records present in the supplied
exports. The event-log-cleared marker means earlier history is unavailable from
this export; the marker does not establish why the log was cleared or whether
other records exist elsewhere. A missing shutdown event does not prove that no
shutdown occurred. An unclean-shutdown indicator does not establish its cause.
An orderly-shutdown marker alone does not establish planned intent.

Host boot/shutdown evidence is not evidence of component health or observatory
availability. N.I.N.A. timestamps show recorded application activity, not
continuous availability or science success. No availability percentage,
reliability metric, incident classification, or planned-downtime total is
derived here.

The analysis was offline and read-only. It did not access the live EAGLE, install
or run a recorder, import source logs into the repository, or change runtime,
command, interlock, or Safety Authority behavior. This report does not authorize
any such activity or close the remaining BKL-043 F4 decisions.

## References

- [Microsoft: Troubleshoot unexpected reboots using System event logs](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-unexpected-reboots-system-event-logs)
- [Microsoft: Event ID 41 — The system has rebooted without cleanly shutting down first](https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/event-id-41-restart)
- [BKL-043 F4 shutdown evidence and historical reconciliation design draft](BKL-043-F4-SHUTDOWN-EVIDENCE-AND-HISTORICAL-RECONCILIATION-DRAFT-2026-09-25.md)

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```
