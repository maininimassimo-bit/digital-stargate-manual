# INT-SESSION-METADATA-PILOT-001 — Shadow Diagnostic Evidence

| Campo | Valore |
|---|---|
| Session | `2026-09-21_2026-09-22` |
| Baseline | `main @ 3859f584fcb8568b14a04c78d9de02127d5c4b7f` |
| Mode | Shadow/offline, read-only |
| Event | `DSG.Observation.Event.SessionCompleted` v1.0.0 |
| Decision | `SHADOW_VALIDATED`; runtime publication disabled |

## Evidence verified

- Manifest status: `COMPLETE`.
- Evidence files: 6; manifest Git blob SHA: `3ca0f4a55ed4549f383968c5929fc3c0d359f046`.
- Every manifest evidence file carries a SHA-256 digest.
- Configuration: `QUATTRO200_TOUPTEK294_BIN1`.
- Telescope: `Sky-Watcher Quattro 200P`.
- Camera: `ToupTek 294MC PRO`.
- Target: `NGC 281`.
- Normalized metrics and session report are present.
- Diagnostic outcome: `YELLOW`.
- Diagnostic reason: Pose LIGHT da verificare: fallite=0, non abbinate=3.
- The shadow event references the manifest, file hashes and downstream projections.
- No broker, live relay, command path or additional scheduler was used.

## Fail-closed checks

| Check | Result |
|---|---|
| Session status must be COMPLETE | PASS |
| Manifest evidence file list must be non-empty | PASS |
| Manifest file hashes must be SHA-256 | PASS |
| Session/equipment identity must match normalized metrics | PASS |
| Shadow event must remain runtime-disabled | PASS |
| Hardware command authority must be NONE | PASS |
| Duplicate event identity must reconcile to NO_OP | PASS |
| PARTIAL/missing/corrupted evidence must reject completion | PASS |

## Interpretation

This is a real-session shadow event artifact, not a live event publication. The session is analytically `YELLOW` because Pose LIGHT da verificare: fallite=0, non abbinate=3. That condition is preserved in the event and does not invalidate the evidence of a completed repository session.

The artifact does not authorize runtime integration, command execution, N.I.N.A. Safety Authority, or changes to local interlocks.
