# AP-008 SessionCompleted Live Shadow OAT — Execution Evidence

| Field | Result |
|---|---|
| Operator/accountable | Massimo Mainini |
| Source commit | `298d5578679d50e869a63fe0d40936e58f377687` |
| Project / service / region | `digital-stargate-telemetry` / `dsg-observatory-status-relay` / `europe-west1` |
| Previous production revision | `dsg-observatory-status-relay-00005-rof` |
| Canary revision | `dsg-observatory-status-relay-00007-bik` |
| Image | `europe-west1-docker.pkg.dev/digital-stargate-telemetry/dsg-telemetry/observatory-status-relay:ap008-298d557` |
| Image digest | `sha256:d09b7b181aa133b85e14f72810b6a11aa153a9023ae4e5d8972ee34441725500` |
| Deployment UTC | `2026-09-22T13:49Z` (build/deploy window) |
| Traffic outcome | 0% canary; 100% retained on previous revision |
| Rollback/disable | Canary tag removed; previous revision remained active |
| Corrected canary revision | `dsg-observatory-status-relay-00010-maw` |
| Corrected image digest | `sha256:ec847f5ae724954038f2588ddc9324117d1435852455c1fce80f1ff35f58e416` |

## Executed

- Environment and Cloud Run service inspection.
- Cloud Build from the authoritative AP-008 source tree.
- Controlled Cloud Run deployment with no production traffic.
- Secret/env preservation check.
- Canary readiness check.
- Unauthenticated shadow POST check: HTTP `401`.
- Shadow GET before publication: HTTP `404`.
- Command-route negative checks: HTTP `404`.
- Canary disable/rollback to previous production traffic.
- Corrected canary deployment after multiline-JSON/NDJSON duplicate defect.
- First shadow publish: HTTP `202`.
- Duplicate shadow publish: HTTP `200`, `NO_OP`.
- Read-back: HTTP `200` with matching event identity and shadow safety flags.

## Verified

- Bearer secret injection still references `dsg-telemetry-ingest-token` version `1`.
- `DSG_RELAY_AUTHORIZED_SOURCE=EAGLE30154`.
- `DSG_RELAY_ALLOWED_ORIGIN=*` and `DSG_RELAY_MAX_BODY_BYTES=65536` preserved.
- Previous production revision remained at 100% traffic.
- Canary revision reached `Ready=True`.
- `activation_mode=shadow`.
- `runtime_event_published=false`.
- `safety_authority=NONE`.
- `command_authority=NONE`.

## Not executed

- EAGLE30154 `-ValidateOnly` publisher command.
- First real POST canary.
- Duplicate POST and `NO_OP` verification.
- Authenticated read-back and message/session/digest reconciliation.
- Consumer reconciliation, full negative suite and ARB decision.
- Production promotion.

## Blocked

- EAGLE30154 was not available as an operator session; the current host was `WIN-QOOF3903TQS`.
- `DSG_TELEMETRY_INGEST_TOKEN` was not present in the operator environment.
- The active Cloud Run service had no explicit `/data` volume or mount. On the new revision,
  `/v1/observatory-status` and `/v1/eagle-health` returned `404`, so persistence continuity
  cannot be accepted as verified.
- The initial canary revealed multiline JSON being treated as NDJSON; this was corrected in
  commit `035765c` and the duplicate test then passed.

## Decision

AP-008 is **not live-ready**. The shadow transport remains unpromoted and the live contract,
broker, scheduler, command path, Safety Authority and runtime event publication remain inactive.

## Persistence remediation

- Dedicated bucket: `gs://digital-stargate-telemetry-183451329061-relay-data` in `europe-west1`.
- Service account granted `roles/storage.objectUser` on the bucket.
- Gen2 canary revision `dsg-observatory-status-relay-00012-bit` mounted the bucket at `/data`.
- `session-completed-shadow.ndjson` was observed in the bucket.
- The same event remained readable after deployment of revision `00012-bit`.
- `/v1/observatory-status` and `/v1/eagle-health` remained `404` on the canary because their
  fresh snapshot objects have not yet been republished into the new bucket.
- Production traffic remained 100% on `dsg-observatory-status-relay-00005-rof`.
