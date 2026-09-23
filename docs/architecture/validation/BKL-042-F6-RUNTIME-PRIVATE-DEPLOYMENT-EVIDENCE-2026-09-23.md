# BKL-042 F6 — private runtime deployment evidence

Status: **DEPLOYED PRIVATE — PROVIDER OAT PASSED — PORTAL INGRESS GATED**

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
- quota ledger after controlled attempts: `3/100`;
- owner-authenticated provider OAT: HTTP `200`;
- selected model: `gpt-6-luna`;
- correlation id: `bkl042-owner-oat-20260923-003`;
- response contract: `bounded_read_only=true`, `runtime_event_published=false`,
  `command_authority=NONE`, `safety_authority=NONE`.

Two initial owner-authenticated attempts were rejected while the API project
had no credit; after credit was added, the single controlled OAT above returned
successfully. No portal traffic, retrieval, command, scheduling, remediation or
Safety Authority action was executed. The public GitHub Pages consumer remains
separately gated because it does not yet have an approved authenticated ingress
to the private relay.
