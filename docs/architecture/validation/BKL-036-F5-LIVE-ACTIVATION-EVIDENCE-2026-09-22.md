# BKL-036-F5 — Live Relay Activation Evidence

| Field | Value |
|---|---|
| Project | `digital-stargate-telemetry` |
| Service | `dsg-observatory-status-relay` |
| Region | `europe-west1` |
| Production revision | `dsg-observatory-status-relay-00017-lak` |
| Rollback revision | `dsg-observatory-status-relay-00005-rof` |
| Image digest | `sha256:93a44aa6b5ecb3514d0c201f795a61fc0f03d9faba9c8e8fdb7b804ed8685a55` |
| Production traffic | `100%` |
| Owner/accountable | Massimo Mainini |

## Controlled activation

The BKL-036-F5-compatible relay was built from main merge
`4d32c641ba21e5f35d7e3a2b81ef8c62d6ff6cc6`, deployed first with the
`bkl036-f5` tag at 0% traffic, and promoted only after the canary checks
passed. The relay retains temporary transport compatibility with the legacy
`UNKNOWN/POLICY_NOT_ACTIVATED` producer while EAGLE30154 is migrated.

## Production read-back

| Check | Result |
|---|---|
| `GET /health` | `200` |
| `GET /v1/observatory-status` | `200`, `CURRENT` |
| `GET /v1/eagle-health` | `200`, current legacy `UNKNOWN/POLICY_NOT_ACTIVATED` |
| `GET /v1/command` | `404` |
| Relay rejected counter at verification | `0` |

The live relay transport is therefore active and backward-compatible. The
EAGLE aggregate remains non-comparable until the updated collector/projection
path is executed on EAGLE30154. No bearer token was printed or copied into
the evidence.

## Remaining OAT gate

On EAGLE30154, update the authorized worktree to main merge
`4d32c641ba21e5f35d7e3a2b81ef8c62d6ff6cc6`, run the existing read-only
`Invoke-EagleHealthTelemetryPublish.ps1` once against the production
`/v1/eagle-health` endpoint, and verify that the public read-back becomes
`HEALTHY`, `DEGRADED` or fail-closed `UNAVAILABLE`. The bearer token remains
local to the existing DPAPI secret path.
