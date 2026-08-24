# ARB-012-C04 — Revocation and Suspension Reconciliation Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-REV-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Target model | Two-Person Limited Operations Model |
| Prepared | 2026-08-24 |
| Status | **In Progress — REV-004 technical PASS; REV-001..REV-003 residual evidence pending** |
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

This proves deterministic denial after suspension and no downstream execution. It does not, by itself, identify which governance actor initiated a revocation, prove a Leonardo-specific suspension scenario, or prove invalidation of an already-pending approval object.

## 3. REV reconciliation matrix

| Control | Required scenario | Existing evidence | Reconciliation result | Residual requirement |
|---|---|---|---|---|
| REV-001 | Leonardo revokes Massimo Operator/requester eligibility | VM-R10 proves Massimo technical principal denial after suspension | **Partial — technical enforcement PASS** | Attributable Leonardo governance revocation decision mapped to Massimo validation eligibility |
| REV-002 | Massimo Sponsor suspends Leonardo approval eligibility | Generic suspension substrate demonstrated by VM-R10 | **Partial — mechanism proven, subject-specific evidence absent** | Attributable Massimo suspension decision plus Leonardo-specific validation-policy denial evidence |
| REV-003 | Pending approval becomes unusable after relevant principal suspension/revocation | No accepted evidence currently proves a pre-existing pending approval becoming invalid | **Pending** | Explicit test showing pending/stale approval invalidation and no execution |
| REV-004 | Deterministic denied access after revocation/suspension | VM-R10 / ENV-007 | **PASS — technical evidence accepted** | None, provided baseline does not regress |

## 4. REV-001 governance attestation — Leonardo revokes Massimo

This is a governance/effective-eligibility decision, not a request to modify production credentials or operate physical devices.

```text
Actor: Leonardo Di Egidio
Subject: Massimo Mainini / DSG-PERSON-001 / dsgmassimo
Control: REV-001
Date: YYYY-MM-DD
Decision: PASS | NOT PASS

I confirm that, for the bounded ARB-012-C04 validation model, I can revoke/suspend Massimo's Operator/requester eligibility and that while such suspension is active Massimo must not be eligible for the affected validation capability. VM-R10 provides the accepted technical enforcement evidence that a previously ALLOW-eligible Massimo principal is deterministically denied with reason principal-suspended and no downstream execution.

This attestation does not revoke any production account and does not authorize runtime or physical-device control.
```

Acceptance: explicit PASS + VM-R10 mapping.

## 5. REV-002 governance attestation and technical residual — Massimo suspends Leonardo

```text
Actor: Massimo Mainini — Project Owner / Architecture Sponsor
Subject: Leonardo Di Egidio / DSG-PERSON-002 / dsgleonardo
Control: REV-002
Date: YYYY-MM-DD
Decision: PASS | NOT PASS

I confirm that, for the bounded ARB-012-C04 validation model, I can suspend Leonardo's C3-approval/return-to-service/safety/security validation eligibility and that while such suspension is active Leonardo must not be eligible for the affected validation capability.

This attestation does not revoke any production account and does not authorize runtime or physical-device control.
```

Governance attestation alone is insufficient to close REV-002: a Leonardo-specific non-production policy test must also demonstrate deterministic DENY after suspension and `execution_attempted=false`.

## 6. REV-003 technical residual — pending approval invalidation

REV-003 requires evidence stronger than a generic new authorization denial. The validation harness must demonstrate all of the following in one correlated scenario:

1. create or represent a pending approval while relevant principals are eligible;
2. suspend/revoke the applicable requester or approver eligibility;
3. attempt to use the already-pending approval;
4. receive deterministic DENY because the approval is stale/invalid after suspension;
5. record `execution_attempted=false`;
6. persist correlated log, audit and exported JSON evidence.

The exact denial reason should be a governed deterministic reason such as `approval-invalid-after-suspension` or the existing canonical equivalent used by the Application policy; do not invent a new production behavior solely for the validation record.

## 7. Safety and scope constraints

- validation environment only;
- simulator-only baseline remains mandatory;
- no production credentials, routes or physical devices;
- no positive C4 or break-glass;
- no local-interlock bypass;
- no runtime privilege is granted by completion of these controls.

## 8. Current disposition

**REV-004 = PASS from VM-R10. REV-001 = technical enforcement proven, Leonardo governance attestation pending. REV-002 = governance attestation plus Leonardo-specific technical denial pending. REV-003 = explicit pending-approval invalidation test pending.**
