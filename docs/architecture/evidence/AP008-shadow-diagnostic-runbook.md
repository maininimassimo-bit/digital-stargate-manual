# AP-008 — Shadow diagnostic runbook

This runbook executes the first AP-008 read-only pilot against the real session fixture
\`2026-09-21_2026-09-22\`.

It validates the imported manifest, all six evidence files and their SHA-256 values, then
writes a deterministic file-based shadow artifact:

- \`data/sessions/2026/09/2026-09-21_2026-09-22/events/SessionCompleted.shadow.json\`
- \`docs/architecture/evidence/AP008-SHADOW-DIAGNOSTIC-2026-09-21_2026-09-22.json\`

The artifact is **not** a runtime event. It is not sent to a broker, does not activate a
scheduler, does not call N.I.N.A., PHD2, ASCOM, the dome, the mount or any relay, and does
not modify the local Safety Authority.

## Command

Run on EAGLE30154 after updating the clone to this branch:

\`\`\`powershell
cd C:\\DigitalStarGate\\digital-stargate-manual-ap14-runtime

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass \`
  -File .\\tools\\ap008\\Invoke-SessionCompletedShadowDiagnostic.ps1 \`
  -RepositoryRoot (Get-Location).Path \`
  -SessionId '2026-09-21_2026-09-22'
\`\`\`

Expected nominal result:

\`\`\`text
AP-008 shadow diagnostic: SHADOW_EVENT_WRITTEN
\`\`\`

A repeated execution must return:

\`\`\`text
AP-008 shadow diagnostic: NO_OP existing event=...
\`\`\`

If a file is missing, its size differs, a SHA-256 differs, or the session identity is
inconsistent, the script writes only a diagnostic with outcome \`REJECT_NO_EVENT\` and exits
with code \`2\`.

## Evidence interpretation

For the current fixture the expected diagnostic status is \`YELLOW\`, because the session
contains three unmatched LIGHT poses and one PHD2 settling failure. This does not prevent
the session-completion metadata from being represented in shadow mode, but it prevents
interpreting the event as proof of a scientifically perfect session.

AP-008 remains \`Rework Required\` until the shadow artifact, fail-closed evidence,
reconciliation, security review, ownership and rollback evidence are reviewed. No runtime
activation is implied by this artifact.
