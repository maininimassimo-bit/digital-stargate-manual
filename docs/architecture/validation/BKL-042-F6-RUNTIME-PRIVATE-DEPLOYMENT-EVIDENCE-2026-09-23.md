# BKL-042 F6 — private runtime deployment evidence

Status: **DEPLOYED PRIVATE — PROVIDER OAT NOT EXECUTED**

Owner/accountable: Massimo Mainini  
Project: `digital-stargate-telemetry`  
Region: `europe-west1`  
Service: `dsg-bkl042-ai-relay`  
Revision: `dsg-bkl042-ai-relay-00002-hq5`

## Verified

- Secret Manager binding: `dsg-bkl042-openai-api-key`, version `1`;
- Firestore Native ledger: `(default)`, `europe-west1`;
- quota collection: `bkl042-pilot-quota`;
- maximum instances: `1`;
- unauthenticated request: rejected with HTTP `403`;
- authenticated `/health`: HTTP `200`, `status=READY`;
- `bounded_read_only=true`;
- `tools_enabled=false`;
- `command_authority=NONE`;
- `safety_authority=NONE`;
- `runtime_event_published=false` remains enforced by the response contract.

No request was sent to `/v1/bkl042-chat`; no provider inference, portal traffic,
retrieval, command, scheduling, remediation or Safety Authority action was
executed. The public GitHub Pages consumer remains separately gated because it
does not yet have an approved authenticated ingress to the private relay.
