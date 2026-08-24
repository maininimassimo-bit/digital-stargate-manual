# ARB-012-C04 — Revocation and Suspension Reconciliation Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-REV-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Target model | Two-Person Limited Operations Model |
| Prepared | 2026-08-24 |
| Status | **In Progress — REV-001 and REV-004 PASS; REV-002 governance PASS / technical residual pending; REV-003 pending** |
| Runtime effect | None |

## 1. Purpose

Reconcile REV-001 through REV-004 against existing repository and VM evidence, avoiding duplicate execution while preserving actor attribution and explicit stale-approval invalidation requirements.

## 2. Existing technical evidence

VM-R10 / ENV-007 (`E-ARB012-C04-VM-R10`) proves the following Application-policy behavior against validation principal `dsgmassimo`:

```text
BASELINE_DECISION=ALLOW
SUSPENDED=true
DECISION=DENY
REASON=principal-suspended
EXECUTION_ATTEMPTED=false
CORRELATION_ID=c1d35282-e64d-4b2d-a793-750c4b8c950d
```

The result is independently correlated across JSONL log, SQLite audit persistence and exported evidence. Evidence SHA-256:

```text
cf7e2f52783b69cd96898ca032d9eb70c5d7262ab4d7333f475a1f37b7b319bb
```

This proves deterministic denial after suspension and no downstream execution. It does not, by itself, prove a Leonardo-specific suspension scenario or invalidation of an already-pending approval object.

## 3. REV reconciliation matrix

| Control | Required scenario | Existing evidence | Reconciliation result | Residual requirement |
|---|---|---|---|---|
| REV-001 | Leonardo revokes Massimo Operator/requester eligibility | VM-R10 + attributable Leonardo governance attestation | **PASS — 2026-08-24** | None |
| REV-002 | Massimo Sponsor suspends Leonardo approval eligibility | VM-R10 generic suspension substrate + attributable Massimo governance attestation | **Partial PASS — governance complete** | Leonardo-specific validation-policy DENY after suspension with `execution_attempted=false` |
| REV-003 | Pending approval becomes unusable after relevant principal suspension/revocation | No accepted evidence currently proves a pre-existing pending approval becoming invalid | **Pending** | Explicit test showing pending/stale approval invalidation and no execution |
| REV-004 | Deterministic denied access after revocation/suspension | VM-R10 / ENV-007 | **PASS — technical evidence accepted** | None, provided baseline does not regress |

## 4. REV-001 governance attestation — RECORDED PASS

```text
Actor: Leonardo Di Egidio
Subject: Massimo Mainini / DSG-PERSON-001 / dsgmassimo
Control: REV-001
Date: 2026-08-24
Decision: PASS
Statement: Leonardo Di Egidio confirms that, for the bounded ARB-012-C04 validation model, he can revoke/suspend Massimo Mainini's Operator/requester eligibility and that while such suspension is active Massimo must not be eligible for the affected validation capability. Leonardo accepts VM-R10/ENV-007 as the technical evidence of ALLOW -> suspended -> DENY enforcement with no downstream execution. This attestation applies only to the validation model and does not revoke production accounts or authorize runtime/physical-device control.
Source of attestation: direct governance confirmation recorded in the governed ARB-012-C04 workflow.
```

REV-001 is closed as PASS by the combination of governance attribution and accepted technical enforcement evidence.

## 5. REV-002 governance attestation — RECORDED PASS; technical residual pending

```text
Actor: Massimo Mainini — Project Owner / Architecture Sponsor
Subject: Leonardo Di Egidio / DSG-PERSON-002 / dsgleonardo
Control: REV-002
Date: 2026-08-24
Decision: PASS
Statement: Massimo Mainini confirms that, for the bounded ARB-012-C04 validation model, he can suspend Leonardo Di Egidio's C3-approval, return-to-service, Safety Authority and Security Authority validation eligibility and that while such suspension is active Leonardo must not be eligible for the affected validation capabilities. This attestation applies only to the validation model and does not revoke production accounts or authorize runtime/physical-device control.
Source of attestation: direct Sponsor confirmation recorded in the governed ARB-012-C04 workflow.
```

The governance component of REV-002 is complete. REV-002 remains open until a Leonardo-specific non-production policy test demonstrates deterministic DENY after suspension and `execution_attempted=false`.

## 6. REV-003 technical residual — pending approval invalidation

REV-003 requires evidence stronger than a generic new authorization denial. The validation harness must demonstrate all of the following in one correlated scenario:

1. create or represent a pending approval while relevant principals are eligible;
2. suspend/revoke the applicable requester or approver eligibility;
3. attempt to use the already-pending approval;
4. receive deterministic DENY because the approval is stale/invalid after suspension;
5. record `execution_attempted=false`;
6. persist correlated log, audit and exported JSON evidence.

The exact denial reason should use the existing canonical Application-policy reason if one exists; do not invent production behavior solely for the validation record.

## 7. Safety and scope constraints

- validation environment only;
- simulator-only baseline remains mandatory;
- no production credentials, routes or physical devices;
- no positive C4 or break-glass;
- no local-interlock bypass;
- no runtime privilege is granted by completion of these controls.

## 8. Current disposition

**REV-001 = PASS. REV-004 = PASS from VM-R10. REV-002 governance = PASS, with Leonardo-specific technical denial still required. REV-003 requires explicit pending-approval invalidation evidence.**
