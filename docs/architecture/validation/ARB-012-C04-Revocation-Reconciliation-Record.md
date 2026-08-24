# ARB-012-C04 — Revocation and Suspension Reconciliation Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-REV-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Target model | Two-Person Limited Operations Model |
| Prepared | 2026-08-24 |
| Status | **PASS — REV-001..REV-004 complete** |
| Runtime effect | None |

## 1. Purpose

Reconcile REV-001 through REV-004 against governance and isolated-VM technical evidence while preserving actor attribution and stale-approval invalidation requirements.

## 2. Accepted evidence

VM-R10 / ENV-007 established the generic suspension enforcement substrate against `dsgmassimo`: `ALLOW -> suspended -> DENY`, reason `principal-suspended`, with `execution_attempted=false`.

The dedicated revocation harness at DigitalStarGate.Control commit `9c69fe1d1d5cea5c777293a1ddac2eeb31aa2fe3` subsequently executed the complete REV-001..REV-004 scenario on `dsg-arb012-c04-val` and returned:

```text
REV_RESULT=PASS
REV001_RESULT=PASS
REV002_RESULT=PASS
REV003_RESULT=PASS
REV004_RESULT=PASS
REV001_DECISION=DENY
REV002_STALE_APPROVAL_VALID=false
REV003_INVALIDATED=true
REV004_DETERMINISTIC=true
PHYSICAL_COMMAND_SENT=false
PRODUCTION_ACCESS_USED=false
RUN_CORRELATION_ID=c3e9b339-f341-4723-b96b-8e0f507297f6
OCCURRED_AT_UTC=2026-08-24T12:06:41.2709906+00:00
```

Detailed technical record: `ARB-012-C04-REV001-004-Evidence.md`.

## 3. REV reconciliation matrix

| Control | Required scenario | Accepted evidence | Result |
|---|---|---|---|
| REV-001 | Leonardo revokes Massimo Operator/requester eligibility | Leonardo governance attestation + VM-R10 + dedicated REV harness | **PASS — 2026-08-24** |
| REV-002 | Massimo Sponsor suspends Leonardo approval eligibility | Massimo governance attestation + dedicated REV harness | **PASS — 2026-08-24** |
| REV-003 | Pending approval becomes unusable after relevant suspension/revocation | Dedicated REV harness: `REV002_STALE_APPROVAL_VALID=false`, `REV003_INVALIDATED=true` | **PASS — 2026-08-24** |
| REV-004 | Deterministic denied access after revocation/suspension | VM-R10 + dedicated REV harness: `REV004_DETERMINISTIC=true` | **PASS — 2026-08-24** |

## 4. REV-001 governance attestation — RECORDED PASS

Leonardo Di Egidio confirmed that, within the bounded ARB-012-C04 validation model, he can revoke/suspend Massimo Mainini's Operator/requester eligibility and that the affected capability must be denied while suspension is active. The attestation does not affect production accounts or authorize runtime/physical-device control.

## 5. REV-002 governance attestation — RECORDED PASS

Massimo Mainini, as Project Owner / Architecture Sponsor, confirmed that within the bounded ARB-012-C04 validation model he can suspend Leonardo Di Egidio's C3-approval, return-to-service, Safety Authority and Security Authority validation eligibility and that affected capabilities must be denied while suspension is active. The attestation does not affect production accounts or authorize runtime/physical-device control.

## 6. REV-003 stale-approval invalidation

The dedicated harness demonstrates that a previously usable approval becomes unusable after the relevant suspension:

```text
REV002_STALE_APPROVAL_VALID=false
REV003_INVALIDATED=true
```

The scenario completed without production access or physical commands.

## 7. REV-004 deterministic denial

The dedicated harness confirms deterministic denial after revocation/suspension:

```text
REV004_DETERMINISTIC=true
REV_RESULT=PASS
```

## 8. Safety and scope constraints

- validation environment only;
- simulator-only baseline remains mandatory;
- no production credentials, routes or physical devices;
- no positive C4 or break-glass;
- no local-interlock bypass;
- no runtime privilege is granted by completion of these controls.

## 9. Current disposition

**PASS — REV-001 THROUGH REV-004 COMPLETE (4/4).**

The revocation/suspension residual for C04-W03 is closed. Runtime authorization remains a separate gate.