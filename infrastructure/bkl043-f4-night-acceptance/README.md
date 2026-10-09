# BKL-043 F4 — night-window candidate

**DRAFT / NOT AUTHORIZED FOR RUNTIME.** Owner supplied availability: 29 September 2026 22:00 through 30 September 2026 02:00 Europe/Rome. This is preparation, not permission to launch a changed artifact. The previous source approval does not automatically cover this candidate. PR #428 remains draft.

## Exact scope

Collector baseline: `2b3f5a31d17868ae7c06696bf4bb676b60ba9649`. Changed only the window, stopped new admission within the final30 seconds, rechecked that guard after sampling, and bounded loop sleep to the admission cutoff. The existing three-task/OS/disk/heartbeat metadata sources, receiver payload contract, durable ACK and outbox preservation semantics remain as in the baseline.

`Invoke-BKL043-F4Window.ps1` is the only intended launch entry point. It verifies host, timezone, window and collector hash. A separate PowerShell job hosts the collector. The supervisor uses a monotonic timeout ending five seconds before02:00. At timeout it verifies the PID and start timestamp of its own child and terminates that process tree, including a native token command blocked inside it. It does not select processes by shared names or touch other observatory jobs. OS suspension or failure can defeat timely scheduling; this is not a hardware real-time guarantee. Review this process termination addition explicitly before approving runtime.

No launch before22:00 or at/after01:59:30. Normal collector admission ends01:59:30; supervisor cutoff01:59:55. No new services, scheduler tasks, firewall changes, clock changes, raw log reads, scientific workflow launches, device commands or safety changes. Only the existing outbox is written. Existing unacknowledged receipts may be retried: that recovery must be explicitly included in final authorization. Never manually delete pending or atomic temporary files. A forced stop may leave pending/temp evidence: inspect and preserve it.

At most240 new one-minute samples fit in the four-hour window, plus the pre-existing pending item; retry request count is separate and follows existing backoff. A late start shortens the run; it never extends the end time. Recheck budget/clock/host before launching; stop on source, outbox or deadline errors and do not bypass guards.

## Offline verification

Run `Test-CollectorFunctions.ps1` and `Test-WindowSupervisor.ps1` in Windows PowerShell5.1. They import selected function ASTs only; neither executes collector top-level. Seventeen collector checks cover existing heartbeat/queue/ACK/backoff rules. Seven supervisor checks cover normal completion, argument transport, sleeping operation timeout, blocked native operation timeout, native child exit, expired duration and no remaining test job. No tokens, HTTP, EAGLE sources or real outbox are used. These are synthetic checks, not complete EAGLE OAT.

The first supervisor prototype failed the blocked-native-command deadline test because Stop-Job alone waited on native work; the retained implementation uses owned-process-tree termination and passes the regression. No failed prototype is a runtime release.

## Review and release

Before release: record immutable commit and ZIP digest; independent architecture/security/quality review of this changed package; Owner approval of this exact version, retry scope, operator and window. Package approval must not be inferred from the earlier review. Operator remains Massimo Mainini. No launch command is approved by this README. Do not run the collector directly to bypass its supervisor.

Full F4 acceptance still needs the remaining task/clock/gap/heartbeat/retry/identity and reporter scenarios, cost-stop evidence and lifecycle evidence. This package covers a bounded recovery/baseline run and offline checks; it does not manufacture those missing PASS results. Identify the authoritative gap-detection component before claiming its test is ready. No public runtime receipt/log belongs in this folder.

Rollback: stop the supervising console and verify its child has exited; preserve outbox and all receipts. Do not merge PR #428 or restart outside this window. Changes to runtime approval or missed window require a new exact record.
