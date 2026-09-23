# BKL-042 F6 — runtime pilot implementation

Status: **IMPLEMENTED — NOT ACTIVATED**

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
2. persistent quota ledger provisioned and monitored;
3. separate Cloud Run service deployment reviewed and approved;
4. bounded live OAT performed without command or safety authority.

At this baseline, the GCP project contains the telemetry ingest secret only and
no OpenAI key. No Cloud Run deployment or external provider request was made.
