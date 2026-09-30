# TIME-01 follow-up candidate — no new runtime authorization

This revision mitigates inconsistent Task Scheduler last-run timestamps: capture UTC immediately before and after the task-info read, preserve full timestamp precision for comparison, and emit `last_run_utc: null` plus `BKL043_TASK_LAST_RUN_UNVERIFIABLE` if the timestamp is later than the read end or the local clock moves backwards during the read. Other task fields remain unchanged. No automatic COM fallback is introduced. The receiver already accepts null last-run timestamps.

This is a mitigation, not a diagnosis of the underlying CIM discrepancy. Incorrect past timestamps and constant external clock offset are not detected by this guard. Task result zero does not prove delivery. Six synthetic cases cover future/past timestamps, execution during acquisition, exact boundary, subsecond future values and a backwards clock. They run in the existing offline validation workflow.

Private evidence includes an offline replay of an observed discrepant sample and an Owner-executed read-only check of all three tasks using this candidate. The latter returned ordinary timestamps and no warnings: it does not exercise the anomalous branch live or prove end-to-end delivery. Raw/private evidence is not included in this repository.

Owner proposed availability on 30 September 2026 **23:29:55 through 1 October 2026 03:29:55 Europe/Rome**. Admission ends 03:29:25; supervisor cutoff is 03:29:50. A late start shortens the run and never moves its end. Do not launch without applicable exact-package review and explicit runtime authorization. F4 remains OPEN; this change does not merge or authorize the pending runtime PRs. The manifest collector hash has been updated for this candidate only.

---

# BKL-043 F4 â€” night-window candidate

## Unreleased OAT remediation

This branch adds two corrections after offline/observational review: preserve high-bit Task Scheduler return values without Int32 overflow, and measure projection freshness after reading its metadata instead of before task enumeration. Six task-result regression cases preserve numeric/hex values and NONZERO_REVIEW semantics; four heartbeat cases cover concurrent update, current observation, future timestamp and unreadable metadata. The receiver contract and freshness threshold are unchanged. This is **not** the approved running commit `53394ea35e499662a3c0a86513261e995a805776`; do not replace or restart the active pilot with these files. A new exact review and runtime authorization are required. Original PR438 and its ZIP remain unchanged. The updated dates below record Owner availability, not exact-package approval.

**DRAFT / NOT AUTHORIZED FOR RUNTIME.** Owner supplied availability: 30 September 2026 23:29:55 through 1 October 2026 03:29:55 Europe/Rome. This is preparation, not permission to launch a changed artifact. The previous source approval does not automatically cover this candidate. PR #428 remains draft.

## Exact scope

Collector baseline: `2b3f5a31d17868ae7c06696bf4bb676b60ba9649`. Changed only the window, stopped new admission within the final30 seconds, rechecked that guard after sampling, and bounded loop sleep to the admission cutoff. The existing three-task/OS/disk/heartbeat metadata sources, receiver payload contract, durable ACK and outbox preservation semantics remain as in the baseline.

`Invoke-BKL043-F4Window.ps1` is the only intended launch entry point. It verifies host, timezone, window and collector hash. A separate PowerShell job hosts the collector. The supervisor uses a monotonic timeout ending five seconds before03:29:55. At timeout it verifies the PID and start timestamp of its own child and terminates that process tree, including a native token command blocked inside it. It does not select processes by shared names or touch other observatory jobs. OS suspension or failure can defeat timely scheduling; this is not a hardware real-time guarantee. Review this process termination addition explicitly before approving runtime.

No launch before23:29:55 or at/after03:29:25. Normal collector admission ends03:29:25; supervisor cutoff03:29:50. No new services, scheduler tasks, firewall changes, clock changes, raw log reads, scientific workflow launches, device commands or safety changes. Only the existing outbox is written. Existing unacknowledged receipts may be retried: that recovery must be explicitly included in final authorization. Never manually delete pending or atomic temporary files. A forced stop may leave pending/temp evidence: inspect and preserve it.

At most240 new one-minute samples fit in the four-hour window; final prior outbox count was zero; retry request count is separate and follows existing backoff. A late start shortens the run; it never extends the end time. Recheck budget/clock/host before launching; stop on source, outbox or deadline errors and do not bypass guards.

## Offline verification

Run `Test-CollectorFunctions.ps1` and `Test-WindowSupervisor.ps1` in Windows PowerShell5.1. They import selected function ASTs only; neither executes collector top-level. Seventeen collector checks cover existing heartbeat/queue/ACK/backoff rules. Seven supervisor checks cover normal completion, argument transport, sleeping operation timeout, blocked native operation timeout, native child exit, expired duration and no remaining test job. No tokens, HTTP, EAGLE sources or real outbox are used. These are synthetic checks, not complete EAGLE OAT.

The first supervisor prototype failed the blocked-native-command deadline test because Stop-Job alone waited on native work; the retained implementation uses owned-process-tree termination and passes the regression. No failed prototype is a runtime release.

## Review and release

Before release: record immutable commit and ZIP digest; independent architecture/security/quality review of this changed package; Owner approval of this exact version, retry scope, operator and window. Package approval must not be inferred from the earlier review. Operator remains Massimo Mainini. No launch command is approved by this README. Do not run the collector directly to bypass its supervisor.

Full F4 acceptance still needs the remaining task/clock/gap/heartbeat/retry/identity and reporter scenarios, cost-stop evidence and lifecycle evidence. This package covers a bounded recovery/baseline run and offline checks; it does not manufacture those missing PASS results. Identify the authoritative gap-detection component before claiming its test is ready. No public runtime receipt/log belongs in this folder.

Rollback: stop the supervising console and verify its child has exited; preserve outbox and all receipts. Do not merge PR #428 or restart outside this window. Changes to runtime approval or missed window require a new exact record.

### Additional isolated filesystem acceptance

Test-IsolatedFilesystem.ps1 imports selected functions through AST only. It creates a fresh temporary synthetic directory, verifies real atomic receipt writes, exact/over 24-hour admission, 16 MiB cap and preservation, plus real file timestamps at 60/61 seconds and absent metadata. Retry and ACK use a simulated transport and no token credentials; these checks do not prove cloud end-to-end or EAGLE runtime behavior. Eleven cases passed locally in Windows PowerShell 5.1. Synthetic files are preserved, with no recursive cleanup or interaction with the production outbox. The two runtime fixes and new window require exact-package review before launch.

