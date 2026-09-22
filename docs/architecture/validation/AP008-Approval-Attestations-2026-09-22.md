# AP-008 Approval Attestations — 2026-09-22

| Campo | Valore |
|---|---|
| Evidence type | owner-witnessed attestations |
| Witness | Massimo Mainini |
| GitHub impersonation | none declared |
| Timezone | not specified in the attestations |
| Effect | recorded receipt; not automatic gate closure |

## Security/trust attestation

**Name:** Leonardo di Egidio  
**Role:** security/trust review  
**Decision:** Approvata  
**Conditions:** nessuna  
**Date/time supplied:** 22/09/2026 - 17:52  
**Statement:** “Attestazione resa direttamente alla presenza di Massimo Mainini; nessuna
approvazione GitHub viene simulata.”

## ARB attestation

**Name:** Teresa Mainini  
**Role:** ARB Independent  
**Decision:** Approvata  
**Conditions:** nessuna  
**Date/time supplied:** 22/09/2026 - 17:54  
**Statement:** “Attestazione resa direttamente alla presenza di Massimo Mainini; nessuna
approvazione GitHub viene simulata.”

## Reconciliation note

These attestations are recorded exactly as provided and witnessed by the accountable owner.
They are not GitHub approvals and do not independently verify identity, independence or the
technical basis of either decision.

The security/trust review package still contains open findings concerning secret lifecycle,
IAM/bucket least privilege, public read exposure/CORS, log redaction and supply chain. The
attestation stating “nessuna” condition conflicts with those recorded findings. That conflict
must be resolved by an explicit amended disposition before the readiness gate can be changed.

Until reconciliation is complete:

- G3 and G7 remain conditionally recorded, not closed;
- production traffic remains unchanged;
- no live activation is authorized;
- `runtime_event_published=false`, `safety_authority=NONE` and `command_authority=NONE` remain
  mandatory.

## Amended security disposition

Leonardo Di Egidio provided the following risk dispositions for the security/trust findings:

| Finding | Decision | Residual risk / mitigation |
|---|---|---|
| Secret lifecycle | `ACCETTATO CON RISCHIO` | No automatic expiry; governed manual rotation every 720 days, immediate revocation on suspected compromise, canary verification after rotation |
| IAM/bucket | `ACCETTATO CON RISCHIO` | Periodic IAM verification is not automated; Cloud Run service-account-only access, no public bucket access, uniform bucket-level access, periodic IAM review |
| CORS/data exposure | `ACCETTATO CON RISCHIO` | Public read-only GETs expose current operational observations; payloads remain observational, no browser token, command or Safety Authority data |
| Log redaction | `ACCETTATO CON RISCHIO` | Accidental sensitive header/detail exposure remains possible; application logging excludes tokens, manual post-deploy checks and limited retention |
| Supply chain | `ACCETTATO CON RISCHIO` | Image/dependency compromise remains possible; immutable digests, reproducible build, dependency scanning and rollback |

Teresa Mainini subsequently confirmed ARB acceptance of this risk register and mitigation set
for the read-only/shadow scope, including direct 100% rollout only after the gates and rollback
within one hour when an unresolved technical issue remains. Confirmation time was not supplied.

## Final governed disposition

The owner-witnessed attestations and explicit risk register reconcile the prior “no conditions”
wording. AP-008 is recorded as:

`READY_FOR_LIVE_INTEGRATION_WITH_WAIVER`

This is a readiness decision for the bounded read-only scope only. It is not a traffic-change
record and does not activate command, broker, scheduler, Safety Authority or live event
publication semantics.
