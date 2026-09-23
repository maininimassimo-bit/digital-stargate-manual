# BKL-042 F6 — runtime pilot implementation

Status: **IMPLEMENTED — PRIVATE DEPLOYMENT READY — PROVIDER OAT PASSED**

The bounded server-side adapter is prepared under
`infrastructure/bkl042-ai-relay/`. It is separate from the observability
telemetry relay and accepts only a question, supplied evidence, citations,
correlation id and an explicit read-only mode. It does not expose tools, actions,
command paths, scheduling, remediation or Safety Authority.

The controlled economic pilot is configured by design for a maximum of 100
requests and the target mix Luna 80%, Sol 18%, Astra 2%. The provider request
uses `store=false`; no browser-held key is supported.

Activation is intentionally blocked until all runtime gates are satisfied:

1. OpenAI API key provisioned to a dedicated Secret Manager secret;
2. Firestore quota ledger collection `bkl042-pilot-quota` provisioned and monitored;
3. separate Cloud Run service deployment reviewed and approved;
4. bounded live OAT performed without command or safety authority.

The private relay deployment is recorded in
`BKL-042-F6-RUNTIME-PRIVATE-DEPLOYMENT-EVIDENCE-2026-09-23.md`. The public
portal ingress remains separately gated. After API credit was provisioned, one
owner-authenticated bounded OAT succeeded on `gpt-6-luna`; the two earlier
credit-failed attempts remain recorded in the quota ledger and no other
provider traffic was generated.
