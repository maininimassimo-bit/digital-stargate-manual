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
