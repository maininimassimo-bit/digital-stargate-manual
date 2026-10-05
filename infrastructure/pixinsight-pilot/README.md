# P4 — authenticated queue and approved cloud activation

Current 2026-10-05 state: Owner-approved resources/credential provisioned and
reviewed image deployed. Real PC HTTPS and bounded HTTP denial checks PASS;
runtime IAM backup/read-back/separate restore PASS. Google Owner login and native
transport OAT remain pending. See the [activation runbook](../../docs/project/PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md).
The proposal-time instructions below are retained for reproducibility; approval
has already been granted. No P5 production command or new publication is enabled.

Owner choice on 2026-10-05: `SESSION_ASSISTED`, using the current assistant
conversation, with zero new paid AI API requests. This is not an autonomous
cloud model or a promise that a closed conversation keeps processing jobs.
Only the two reviewed recipes from P2/P3 can be requested. Master selection,
parameters and paths are registered in a private local configuration.

## Procedure and boundaries

1. The authenticated Owner submits `POST /v1/jobs` with exactly
   `schemaVersion: "1.0"`, opaque 32-hex `requestId` and `inputRef`, approved
   `recipe`, and `aiMode: "SESSION_ASSISTED"`. No JS, path or parameter is admitted.
   The same request returns the same job; changed content under its identity rejects.
   P5 will add the portal controls and session/version relationships; they are absent here.
2. An operator invokes the PC adapter once. It makes outbound HTTPS requests
   to the exact configured Cloud Run origin. No inbound desktop listener,
   scheduled task or background daemon is installed. Redirects, environment
   proxies, plaintext origins and invalid responses are refused.
3. The queue issues one persistent reservation for the configured worker.
   Its first claim durably binds an opaque local root identity; a fresh root
   cannot adopt the queue even before the first progress report. The PC keeps
   `transport/root-identity.json`; it is an identity nonce, not an authentication
   credential. Never clone it to another root or reconstruct a lost binding.
   A repeated claim returns it unchanged, including after a lost response or
   service restart. `OFFLINE` after 120 seconds is a contact diagnostic, not
   job expiry, cancellation, worker reallocation or scientific freshness.
4. The PC binds the request durably, resolves the local allowlist reference,
   and obtains an acknowledged remote `PREPARING` transition before any copy.
   An advanced claim without local binding is refused, even if the root identity
   is preserved. A lost PREPARING response resends identical data before copying.
   It then invokes the existing trusted coordinator to copy and verify masters.
   It never executes server-supplied code or automatically starts PixInsight.
   The operator runs the prepared `run.js` in PixInsight's script menu.
5. Invoke the adapter again to send bounded progress and receive cancellation.
   Cancellation uses the P2 token-bound local marker; an in-flight native
   process can finish first. A request alone does not immediately stop pixels.
6. After explicitly confirming native execution stopped, invoke with
   `--native-stopped`. The existing collector validates hashes, native journal,
   metadata and final pixels before reporting `COMPLETED`. The queue labels
   reports `WORKER_REPORTED_NOT_ATTESTED`; it cannot independently certify the
   desktop, licenses, scientific quality or imported History completeness.
   Nothing uploads photos or publishes the result.

PC command from repository root:

```text
python -m tools.pixinsight.local_pilot.transport --config <private-config.json>
python -m tools.pixinsight.local_pilot.transport --config <private-config.json> --native-stopped
```

Private config fields: `serviceOrigin`, 32-hex `workerId`, absolute existing
`workerRoot`, `registry` mapping opaque input references to complete previously
reviewed P2/P3 requests. The cloud job ID replaces only the local request job ID.
Set the dedicated 256-bit hex bearer credential in `DSG_PIAI_WORKER_TOKEN` in
the operator's environment, never in CLI arguments, Git, portal storage or logs.
The server stores its SHA-256 digest; rotation/revocation is explicit, no
automatic credential creation. Protect the config, journal, reservation tokens
and environment with the Owner account. Local administrator access and trusted
service administrators remain the trust boundary; neither receipt is attestation.

## Failure and recovery

Each PC cycle uses an exclusive create-only lock. A crash retains it; do not
remove it while another adapter or PixInsight run is active. Private immutable
pending reports are resent identically after a network failure. Durable terminal
acknowledgement is reconciled before claiming another job. A partial preparation,
foreign local reservation, rejected collection or unknown input reference becomes
`RECOVERY_REQUIRED`, which freezes assignment. There is no automatic retry of
pixels, job reassignment, forced unlock or expiry.

For ambiguous/crashed work: confirm the adapter and PixInsight have stopped,
preserve all PC evidence and the committed cloud state and recovery copy, inspect
the last verified transition, then quarantine the old root. New root and queue
identity/configuration require deliberate operator recovery; never edit a live
reservation or use a newer uncommitted backup as the current state. Availability
of local state is required: loss of a binding is refused, not rebuilt by replay.

The queue holds at most 16 jobs in one generation-guarded object of at most
1 MiB. Report sequence is bounded to 128 changes. Capacity rejects without
deleting anything. `BackedUpStore` retains a separate immutable candidate before
primary CAS; only the committed primary generation is authoritative. No memory
fallback exists in the deployment. MemoryStore and loopback plaintext are test-only.
Polling/updates create storage operations and retained versions/backups: capacity
bounds are not a cloud spending cap or an infinite-storage guarantee.

## Approved concrete activation proposal

Exact resources and limits: [deployment-plan.json](deployment-plan.json).
Separate Cloud Run `dsg-pixinsight-pilot` (1 CPU/512 MiB, min=0/max=1,
concurrency=1, timeout 60 s), dedicated identity/registry and two private versioned
buckets in europe-west1. No change to the photo ingestion runtime or its buckets.
No scientific images/models are stored in these buckets. Use request-based billing.
Zero paid AI calls does not mean zero infrastructure cost: request CPU, storage
operations/retained versions/recovery candidates, registry/builds and possible
egress are billable. No hard spending cap is supplied. No continuous polling
is enabled; requests are bounded operator invocations.

Owner approval for the new resources and dedicated credential was received on
2026-10-05 under DSG-AEM-001 section 5. Installed PixInsight
licenses remain for this personal single-Owner pilot; no commercial/multiuser rights
are asserted. Partial live cloud OAT is documented separately; no complete OAT is claimed.

After approval and reviewed merge:

1. Read-only verify project/account and absence of the exact resources; create
   only the proposed resources. Buckets: public access prevention, UBLA, versioning,
   no deletion or automatic lifecycle. Identity: primary objectCreator/viewer,
   conditional objectUser only for `control/piai-state.json`; backup creator/viewer
   without delete/overwrite. No access to photo buckets.
2. Generate the credential privately and provision only its digest to the service;
   retain the bearer only on the PC. Reuse the existing Google web client/Owner
   identity with exact portal origin; do not extract any browser token.
3. Build the allowlisted context, retain build receipt and deploy the resolved
   digest with `DSG_PIAI_ACTIVATION=OWNER_AUTHORIZED` plus the seven settings
   checked by `app.py`. Expose service HTTP surface with application authentication;
   buckets remain private. Missing settings or activation refuses startup.
4. Verify actual TLS, anonymous/non-Owner/worker role denial, token provisioning,
   Google Owner login, primary/backup IAM, generation conflicts, committed-state
   restore/read-back, restart/offline/lost-response and cancellation with labelled
   synthetic inputs. Only then register private M27 references for supervised OAT.
5. Use the hidden P4 diagnostic page for the required live Owner-auth check. Its
   destination is pinned by digest; no default service URL or scientific command.
   Review production portal activation as P5 only after live gates; complete P6
   native end-to-end/recovery and Owner acceptance.

Rollback: stop new invocations and revoke the worker credential/server digest,
disable service traffic, retain both buckets and PC evidence. Revert code through
a reviewed commit; never restore an old publication head or delete scientific files.

Primary references: [Cloud Run billing](https://docs.cloud.google.com/run/docs/configuring/billing-settings),
[pricing](https://cloud.google.com/run/pricing),
[service identity](https://docs.cloud.google.com/run/docs/securing/service-identity).

## Verification

```text
python -m unittest tools.pixinsight.local_pilot.test_transport
```

Synthetic persistence and actual loopback HTTP cover Owner/worker separation,
idempotency, loss/restart, offline without reassignment, cancellation, conflict,
backup failure, capacity, privacy, redirect denial, one-time local preparation,
supervised collection and recovery. They do not establish deployed Google auth,
TLS/cloud IAM/durability, actual native transport OAT or new scientific acceptance.
