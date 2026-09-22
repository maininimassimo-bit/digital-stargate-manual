# AP-008 SessionCompleted Live Shadow OAT Plan — 2026-09-22

| Campo | Valore |
|---|---|
| Package | AP-008 |
| Owner / Accountable | Massimo Mainini |
| Scope | live transport of validated shadow evidence |
| Runtime mode | shadow event, read-only transport |
| Current gate | BLOCKED — shadow canary passed; persistence/consumer continuity open |
| Safety Authority | local and independent |
| Command authority | NONE |

## 1. Objective

Validate the first operational vertical slice of AP-008:

```text
existing SessionCompleted.shadow.json
  -> EAGLE publisher
  -> HTTPS POST /v1/session-completed-shadow
  -> Cloud Run relay append-only store
  -> HTTPS GET /v1/session-completed-shadow
  -> read-only reconciliation
```

This OAT transports shadow evidence only. It does not activate the live contract, a broker,
a scheduler, a command path or any Safety Authority integration.

## 2. Preconditions

- relay image containing the isolated `/v1/session-completed-shadow` channel is deployed
  through the existing controlled Cloud Run process;
- bearer token is injected through the existing secret path and is not committed;
- relay endpoint remains HTTPS;
- `EAGLE30154` is the authorized source;
- the existing shadow event and its evidence remain unchanged;
- no telescope session or device command is started by this test.

## 3. EAGLE validation command

Run on EAGLE30154 from the repository root:

```powershell
$event = ".\data\sessions\2026\09\2026-09-21_2026-09-22\events\SessionCompleted.shadow.json"
$endpoint = "https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app/v1/session-completed-shadow"

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File ".\scripts\telemetry\Publish-SessionCompletedShadowEvent.ps1" `
  -EventPath $event `
  -Endpoint $endpoint `
  -ValidateOnly
```

Expected result:

```text
VALIDATION RESULT: PASS
```

## 4. Canary publication

After validation passes:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File ".\scripts\telemetry\Publish-SessionCompletedShadowEvent.ps1" `
  -EventPath $event `
  -Endpoint $endpoint
```

Expected result:

- HTTP `202` and `PUBLISH RESULT: PASS`;
- no token or Authorization header in output;
- no N.I.N.A., PHD2, CPWI, ASCOM, dome, mount, camera, relay or PLC command;
- source event remains byte-identical.

## 5. Duplicate and read-back checks

Repeat the same publication once. Expected result:

- HTTP `200`;
- relay result `NO_OP`;
- no second line with the same `message_id` in the append-only store.

Then perform a read-only GET using an approved operator/client path and verify:

- same `message_id`;
- same `subject.session_id`;
- same `payload.manifest_sha256`;
- `activation_mode=shadow`;
- `runtime_event_published=false`;
- `safety_authority=NONE`;
- `command_authority=NONE`.

## 6. Negative tests

The OAT is NO-GO if any of the following is accepted:

- missing or invalid bearer token;
- wrong producer instance;
- non-shadow activation mode;
- `runtime_event_published=true`;
- `safety_authority` different from `NONE`;
- `command_authority` different from `NONE`;
- mismatched subject/payload session identity;
- invalid manifest SHA-256;
- duplicate event appended twice.

## 7. Rollback / disable

Rollback is bounded:

1. stop invoking the publisher;
2. verify no new shadow event is accepted;
3. verify existing append-only evidence remains readable;
4. route the relay back to the previous revision using the existing Cloud Run procedure;
5. verify existing Observatory Status and EAGLE Health channels are unaffected;
6. record operator, UTC timestamp, revision, HTTP results and outcome.

Rollback does not delete the repository event or modify local safety controls.

## 8. Evidence record

Record at minimum:

- relay revision and deployment timestamp;
- endpoint host;
- validation output;
- first publication status and response;
- duplicate publication status and response;
- read-back event identity and digest;
- negative-test statuses;
- rollback/disable result;
- operator and UTC timestamps.

## 9. Decision

The OAT can advance the AP-008 shadow transport gate only if every positive and negative
check passes. It does not by itself change the status of the live contract. A separate
security review and ARB decision remain required before `runtime_event_published=true`
or any live activation semantics are introduced.

## 10. Execution record — 2026-09-22

The controlled Cloud Run canary deployment was executed from commit `298d5578679d50e869a63fe0d40936e58f377687`.
Cloud Build produced image digest `sha256:d09b7b181aa133b85e14f72810b6a11aa153a9023ae4e5d8972ee34441725500`.
Revision `dsg-observatory-status-relay-00007-bik` became Ready with 0% production traffic, while
`dsg-observatory-status-relay-00005-rof` remained at 100% and was retained as rollback.

Observed canary checks:

- `GET /v1/session-completed-shadow`: `404` before publication, as expected;
- unauthenticated `POST /v1/session-completed-shadow`: `401`;
- command-like GET paths `/v1/command`, `/v1/control`, `/v1/remediate`, `/v1/reboot`: `404`;
- secret injection `dsg-telemetry-ingest-token`, authorized source `EAGLE30154`, allowed origin and body limit were preserved;
- canary `GET /v1/observatory-status` and `GET /v1/eagle-health`: `404`, demonstrating that `/data` persistence was not available across the new revision;
- the canary tag was removed and production traffic remained 100% on `dsg-observatory-status-relay-00005-rof`.

The EAGLE30154 publisher validation, real canary, duplicate delivery, read-back, negative tests,
and consumer reconciliation were not executed because the EAGLE30154 session and bearer token
were not available from the operator environment. AP-008 remains blocked and is not live-ready.

## 11. Continued execution — 2026-09-22

After EAGLE30154 access and secret injection became available, the shadow canary was rerun on
revision `dsg-observatory-status-relay-00010-maw` with image digest
`sha256:ec847f5ae724954038f2588ddc9324117d1435852455c1fce80f1ff35f58e416`.

Observed results:

- first publish: HTTP `202`;
- duplicate publish: HTTP `200`, `NO_OP`;
- read-back: HTTP `200`, with matching `message_id`, `session_id` and `manifest_sha256`;
- read-back flags: `activation_mode=shadow`, `runtime_event_published=false`,
  `safety_authority=NONE`, `command_authority=NONE`;
- command route probe: HTTP `404`;
- production traffic remained at 100% on `dsg-observatory-status-relay-00005-rof`;
- canary `/v1/observatory-status` and `/v1/eagle-health` remained HTTP `404`, so persistence
  and consumer continuity across revisions remain unverified.

The first canary revision exposed a multiline-JSON/NDJSON defect on duplicate delivery. The
relay was corrected in commit `035765c` to normalize events to one JSON object per line and to
ignore non-object legacy fragments during deduplication.
