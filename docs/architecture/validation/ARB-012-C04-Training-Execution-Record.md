# ARB-012-C04 — Training and Briefing Execution Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-TRN-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Target model | Two-Person Limited Operations Model |
| Prepared | 2026-08-23 |
| Status | **Partial PASS — Leonardo TRN-004..007 cross-attested; Massimo training and TRN-008 pending** |
| Runtime effect | None |

## 1. Purpose

Provide the attributable execution record for TRN-001 through TRN-008. Training/briefing may be cross-attested by the two participants when the assessor is not certifying their own completion. No runtime privilege is granted by this record.

## 2. Canonical training material

Primary governed material:

- `docs/architecture/operations-command-authorization-model.md` — command classes C0-C4, deny-by-default, approval matrix, separation of duties, delegation, break-glass, Safety Plane, audit and failure handling;
- `docs/architecture/operations-responsibility-matrix.md` — operational role boundaries and accountability;
- `docs/architecture/operational-runbook-standard.md` — maintenance/recovery/runbook governance and evidence expectations;
- `docs/architecture/packages/AP-012-Enterprise-Operations-Center-Architecture.md` — AP-012 scope and Operations Center architecture;
- `docs/architecture/validation/ARB-012-C04-W03-Execution-Package.md` — two-person execution rules;
- `docs/architecture/validation/ARB-012-C04-Sponsor-Nomination-Decision.md` — approved two-person target and unsupported capabilities;
- `docs/architecture/validation/ARB-012-C04-VM-Residual-Checklist.md` — executed technical controls and fail-safe outcomes.

## 3. Training matrix

| Training ID | Participant | Assessor | Subject | Current result |
|---|---|---|---|---|
| TRN-001 | Massimo Mainini | Leonardo Di Egidio | C0-C4 classification, request boundaries, self-approval prohibition | **Pending Leonardo assessment** |
| TRN-002 | Massimo Mainini | Leonardo Di Egidio | Maintenance safety, rollback, safe-state preservation, return-to-service handoff | **Pending Leonardo assessment** |
| TRN-003 | Massimo Mainini | Leonardo Di Egidio | Incident recording, audit trail, correlation and evidence preservation | **Pending Leonardo assessment** |
| TRN-004 | Leonardo Di Egidio | Massimo Mainini | Independent C3 approval criteria and conflict/self-approval rejection | **PASS — 2026-08-23** |
| TRN-005 | Leonardo Di Egidio | Massimo Mainini | Safety Authority permit/deny/stop, safe-state verification and no interlock bypass | **PASS — 2026-08-23** |
| TRN-006 | Leonardo Di Egidio | Massimo Mainini | Privileged-access approval, least privilege and revocation/suspension | **PASS — 2026-08-23** |
| TRN-007 | Leonardo Di Egidio | Massimo Mainini | Return-to-service approval independent from Maintainer | **PASS — 2026-08-23** |
| TRN-008 | Both | Reciprocal | Four-eyes workflow, revocation, C4/break-glass denial and audit completeness | **Pending reciprocal cross-attestation** |

## 4. Required learning outcomes

### TRN-001 — Massimo
- difference between C0, C1, C2, C3 and C4;
- why C3 requires a distinct approver;
- authentication is not authorization;
- self-approval prohibition;
- positive C4 and break-glass unavailable in the approved two-person validation target.

### TRN-002 — Massimo
- maintenance scope and lock boundaries;
- preservation of safe state during maintenance/recovery;
- rollback/recovery responsibility;
- Maintainer cannot certify own return-to-service.

### TRN-003 — Massimo
- mandatory correlation/evidence fields;
- preservation of failed and denied outcomes;
- audit/evidence integrity expectations;
- secrets and credentials excluded from evidence records.

### TRN-004 — Leonardo
- independent C3 approval criteria;
- requester/approver conflict handling;
- deterministic self-approval denial;
- absence of approval-by-silence.

### TRN-005 — Leonardo
- Safety Authority permit/deny/stop responsibility;
- distinction between operational authorization and Safety Plane consent;
- fail-safe handling of unknown/stale/conflicting state;
- prohibition on local-interlock bypass.

### TRN-006 — Leonardo
- least-privilege scope decisions;
- self-access approval prohibition;
- suspension/revocation effect before execution;
- evidence required for denied/stale authorization.

### TRN-007 — Leonardo
- return-to-service as a distinct approval from maintenance execution;
- Maintainer cannot self-approve return-to-service;
- bounded approval scope and traceability.

### TRN-008 — Both
- two-person four-eyes model;
- capability suspension when one actor is unavailable;
- no incompatible cross-substitution;
- C4 and break-glass denied by design;
- correlation from request/decision to audit/evidence;
- validation closure does not imply runtime authorization.

## 5. Recorded training attestations

### 5.1 Massimo assesses Leonardo — RECORDED PASS

```text
Participant: Leonardo Di Egidio
Assessor: Massimo Mainini
Controls: TRN-004, TRN-005, TRN-006, TRN-007
Method: governed-document briefing + confirmation of required learning outcomes
Material: OPSC-CMD-001, AP-012, Operational Runbook Standard, Responsibility Matrix, Sponsor Decision, applicable VM evidence
Date: 2026-08-23
Decision: PASS
Statement: Massimo Mainini confirms that the governed material was reviewed with Leonardo Di Egidio and that Leonardo demonstrated understanding of the required learning outcomes for TRN-004, TRN-005, TRN-006 and TRN-007.
Source of attestation: direct assessor confirmation recorded in the governed ARB-012-C04 workflow.
```

This closes TRN-004, TRN-005, TRN-006 and TRN-007 as PASS.

### 5.2 Leonardo assesses Massimo — PENDING

```text
Participant: Massimo Mainini
Assessor: Leonardo Di Egidio
Controls: TRN-001, TRN-002, TRN-003
Method: governed-document briefing + question/answer confirmation
Material: OPSC-CMD-001, Operational Runbook Standard, Responsibility Matrix, Sponsor Decision, applicable VM evidence
Date: YYYY-MM-DD
Decision: PASS | NOT PASS
Statement: I confirm that Massimo reviewed the governed material and demonstrated understanding of the required learning outcomes for TRN-001, TRN-002 and TRN-003.
```

### 5.3 Reciprocal TRN-008 — PENDING

```text
Participants: Massimo Mainini + Leonardo Di Egidio
Control: TRN-008
Method: reciprocal governed-document briefing and confirmation
Material: OPSC-CMD-001, W03 package, Sponsor Decision, VM-R08 through VM-R12 evidence
Date: YYYY-MM-DD
Massimo decision on Leonardo: PASS | NOT PASS
Leonardo decision on Massimo: PASS | NOT PASS
Result: PASS only if both reciprocal decisions are PASS
Statement: Both participants confirm understanding of the two-person four-eyes model, denial-by-design limitations, revocation behavior, audit/evidence obligations and the separation between validation closure and runtime authorization.
```

## 6. Acceptance rules

- assessor must be the other person for individual completion;
- self-certification is not sufficient;
- TRN-008 requires reciprocal PASS;
- a failed training item remains Failed/Pending until re-assessed;
- no third person is required;
- no runtime privilege is granted by training completion.

## 7. Current disposition

**PARTIAL PASS — TRN-004, TRN-005, TRN-006 AND TRN-007 PASS. TRN-001, TRN-002, TRN-003 AND RECIPROCAL TRN-008 REMAIN PENDING.**
