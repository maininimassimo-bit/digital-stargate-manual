# AP-008 Production Read-Only Rollout — 2026-09-22

| Campo | Valore |
|---|---|
| Service | `dsg-observatory-status-relay` |
| Project / region | `digital-stargate-telemetry` / `europe-west1` |
| Promoted revision | `dsg-observatory-status-relay-00015-hak` |
| Previous rollback revision | `dsg-observatory-status-relay-00005-rof` |
| Traffic outcome | 100% promoted revision; previous revision retained at 0% for rollback |
| Scope | bounded read-only portal telemetry and SessionCompleted shadow read-back |
| Rollout decision | direct 100% under `READY_FOR_LIVE_INTEGRATION_WITH_WAIVER` |

## Preflight executed

- Observatory Status fresh snapshot published to the canary.
- EAGLE Health fresh projection published to the canary.
- Canary Observatory Status: HTTP `200`, schema `1.1`.
- Canary EAGLE Health: HTTP `200`, component `DSG.EagleHealthPortalProjection`, host
  `EAGLE30154`.
- Canary SessionCompleted shadow: HTTP `200`, expected message identity retained.
- Existing production traffic was 100% on `00005-rof` before promotion.

## Promotion executed

Cloud Run traffic was updated with:

`--to-revisions dsg-observatory-status-relay-00015-hak=100`

The service reported 100% traffic on `00015-hak` and retained `00005-rof` as the rollback
revision.

## Post-rollout verification

- Production `GET /v1/observatory-status`: HTTP `200`, schema `1.1`.
- Production `GET /v1/eagle-health`: HTTP `200`, component
  `DSG.EagleHealthPortalProjection`, host `EAGLE30154`.
- Production `GET /v1/session-completed-shadow`: HTTP `200`, same shadow message ID
  `shadow-2026-09-21_2026-09-22-714a67f66799824e`.
- Production `GET /v1/command`: HTTP `404`.
- No broker, scheduler, command path or Safety Authority integration was introduced.
- `runtime_event_published=false`, `safety_authority=NONE` and `command_authority=NONE`
  remain unchanged.

## Rollback rule

If a technical issue cannot be resolved within one hour, restore 100% traffic to
`dsg-observatory-status-relay-00005-rof`.
