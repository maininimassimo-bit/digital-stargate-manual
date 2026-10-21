# BKL-043 F4 portable EAGLE pilot package

**Scope:** manual, read-only, two-hour pilot for EAGLE30154. This package does
not install a Windows service or scheduled task and does not issue device,
shutdown, scheduling, remediation, or safety commands.

## Build and immutable identity

The pull-request workflow builds a ZIP containing only
`Start-BKL043-F4Pilot.ps1` and this document. Its SHA-256 is emitted in the
GitHub Actions job summary and the ZIP is retained as a workflow artifact.
Before any EAGLE use, record the exact workflow run, commit SHA, ZIP SHA-256,
and collector/configuration revision in the exact runtime authorization record.

## Manual installation and start

1. Download the ZIP artifact from the reviewed workflow run.
2. Verify its SHA-256 against the workflow summary.
3. Extract it to `C:\DigitalStarGate\TelemetryPilot\F4`.
4. At the approved start time, open an interactive PowerShell session as
   `eagle30154\primalucelab` (no elevation) and run:

   ```powershell
   powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\DigitalStarGate\TelemetryPilot\F4\Start-BKL043-F4Pilot.ps1" -ReceiverUrl "https://<approved-cloud-run-service-url>"
   ```

   The receiver URL is a non-secret runtime parameter and must be the exact
   IAM-authenticated Cloud Run service base URL approved for this package.
   Cloud Run's IAM layer must reject unauthenticated invocations.

The collector checks EAGLE30154, the approved Europe/Rome time zone and the
2026-09-29 10:00–12:00 Europe/Rome window before starting. It samples once per
minute, admits new durable receipts only while Windows Time synchronization is
within 24 hours and root dispersion is at most one second, and stops at noon.
Each receipt is at most 4 KiB. The only durable local write is the receipt
outbox at `D:\DigitalStarGate\Telemetry\Outbox`; temporary atomic-write
files are confined to that same directory. The outbox cap is 16 MiB and the
queue-age limit is 24 hours while EAGLE is operating. A full, unreadable,
over-age, or time-uncertain queue pauses new receipt admission, preserves its
contents, and is surfaced in the interactive console.

The sample contains only the approved host/build/uptime, C:/D: free space,
three named DGS task state/results, task-launched process presence, and N.I.N.A.
projection metadata. It does not read local logs or the N.I.N.A. projection
contents, and it does not transmit usernames, paths, command arguments or
secrets. Task result zero is shown as `SUCCESS`; nonzero results are shown as
`NONZERO_REVIEW` and are not automatically classified as failures.

Receipts use a UUID object key `v1/<receipt-id>.json`. The sender removes an
outbox item only after Cloud Run returns an explicit acknowledgement that the
object was durably created, or that the same ID and payload were already
stored. Unacknowledged receipts are retried with backoff up to five minutes.
The GitHub outcome reporter is limited to the two approved F9 workflow names on the repository's default branch. It preserves success, failure, cancelled, skipped, and other completed conclusions distinctly. It uses GitHub OIDC with Google Workload Identity Federation and a dedicated reporter service account; it sends the workflow run metadata only, never workflow logs or artifacts. Configure the receiver base URL as the GitHub Actions variable `DSG_F4_RECEIVER_URL`, and the provider resource and reporter service-account email as the secrets `DSG_F4_WIF_PROVIDER` and `DSG_F4_REPORTER_SERVICE_ACCOUNT`. The runtime URL, provider and service-account IAM bindings must be reviewed before enabling those settings. The reporter has no local queue, so a failed report remains visible as a failed GitHub Actions run and must be reconciled from its run metadata and Usage Logs.

The collector removes an outbox receipt only after durable acknowledgement. Unacknowledged receipts are never deleted.

## Stop and rollback

- Press Ctrl+C to stop the interactive collector early. At noon it exits on its
  own. It creates no background process, Windows service, or scheduled task.
- After confirming the collector process has exited, rollback removes only
  `C:\DigitalStarGate\TelemetryPilot\F4`.
- Never remove or edit `D:\DigitalStarGate\Telemetry\Outbox` during rollback.
  It contains unacknowledged evidence and is retained for a later separately
  authorized manual launch.

## Activation prerequisites still required

This package is a review artifact, not runtime authorization. Before the pilot,
the gate still requires exact receiver and audience URLs, service/storage IAM
configuration, Usage Logs lifecycle evidence, the GitHub reporter's WIF provider, invoker IAM and repository Actions configuration, permitted identity-token
endpoint egress, security/privacy and independent architecture/release-quality
reviews, failure-injection/acceptance evidence, and Massimo Mainini's approval
of the exact final authorization revision. No Cloud resource or EAGLE run is
activated by building this ZIP.
