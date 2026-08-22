# ARB-012-C04 — Training and Briefing Execution Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-TRN-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Target model | Two-Person Limited Operations Model |
| Prepared | 2026-08-23 |
| Status | **Ready for cross-attested execution** |
| Runtime effect | None |

## 1. Purpose

Provide the attributable execution record for TRN-001 through TRN-008. Training/briefing may be cross-attested by the two participants when the assessor is not certifying their own completion. No item is marked Passed by preparation of this record alone.

## 2. Canonical training material

Primary governed material:

- `docs/architecture/operations-command-authorization-model.md` — command classes C0-C4, deny-by-default, approval matrix, separation of duties, delegation, break-glass, Safety Plane, audit and failure handling;
- `docs/architecture/operations-responsibility-matrix.md` — operational role boundaries and accountability;
- `docs/architecture/operational-runbook-standard.md` — maintenance/recovery/runbook governance and evidence expectations;
- `docs/architecture/packages/AP-012-Enterprise-Operations-Center-Architecture.md` — AP-012 scope and Operations Center architecture;
- `docs/architecture/validation/ARB-012-C04-W03-Execution-Package.md` — two-person execution rules;
- `docs/architecture/validation/ARB-012-C04-Sponsor-Nomination-Decision.md` — approved two-person target and unsupported capabilities;
- `docs/architecture/validation/ARB-012-C04-VM-Residual-Checklist.md` — executed technical controls and fail-safe outcomes.

The Command Authorization Model explicitly defines C0 through C4, requester/approver separation for C3/C4, maintenance/return-to-service separation, Safety Authority precedence, audit requirements and deny-by-default behavior.

## 3. Training matrix

| Training ID | Participant | Assessor | Subject | Minimum material | Current result |
|---|---|---|---|---|---|
| TRN-001 | Massimo Mainini | Leonardo Di Egidio | C0-C4 classification, request boundaries, self-approval prohibition | Command Authorization Model; Sponsor Decision | Pending cross-attestation |
| TRN-002 | Massimo Mainini | Leonardo Di Egidio | Maintenance safety, rollback, safe-state preservation, return-to-service handoff | Operational Runbook Standard; Responsibility Matrix; Sponsor Decision | Pending cross-attestation |
| TRN-003 | Massimo Mainini | Leonardo Di Egidio | Incident recording, audit trail, correlation and evidence preservation | Command Authorization Model; VM-R08 evidence; W03 package | Pending cross-attestation |
| TRN-004 | Leonardo Di Egidio | Massimo Mainini | Independent C3 approval criteria and conflict/self-approval rejection | Command Authorization Model; Sponsor Decision; VM-R09 evidence | Pending cross-attestation |
| TRN-005 | Leonardo Di Egidio | Massimo Mainini | Safety Authority permit/deny/stop, safe-state verification and no interlock bypass | Command Authorization Model; AP-012; Sponsor Decision | Pending cross-attestation |
| TRN-006 | Leonardo Di Egidio | Massimo Mainini | Privileged-access approval, least privilege and revocation/suspension | W03 package; Sponsor Decision; VM-R10 evidence | Pending cross-attestation |
| TRN-007 | Leonardo Di Egidio | Massimo Mainini | Return-to-service approval independent from Maintainer | Responsibility Matrix; Operational Runbook Standard; Sponsor Decision | Pending cross-attestation |
| TRN-008 | Both | Reciprocal | Four-eyes workflow, revocation, C4/break-glass denial and audit completeness | Command Authorization Model; VM-R08..VM-R12 evidence; W03 package | Pending reciprocal cross-attestation |

## 4. Required learning outcomes

### TRN-001 — Massimo

Participant can explain:

- difference between C0, C1, C2, C3 and C4;
- why C3 requires a distinct approver;
- why authentication is not authorization;
- why self-approval is prohibited;
- why positive C4 and break-glass are unavailable in the approved two-person validation target.

### TRN-002 — Massimo

Participant can explain:

- maintenance scope and lock boundaries;
- preservation of safe state during maintenance/recovery;
- rollback/recovery responsibility;
- why the Maintainer cannot certify their own return-to-service.

### TRN-003 — Massimo

Participant can explain:

- mandatory correlation/evidence fields;
- preservation of failed and denied outcomes;
- audit/evidence integrity expectations;
- why secrets and credentials are excluded from evidence records.

### TRN-004 — Leonardo

Participant can explain:

- independent C3 approval criteria;
- requester/approver conflict handling;
- deterministic self-approval denial;
- absence of approval-by-silence.

### TRN-005 — Leonardo

Participant can explain:

- Safety Authority permit/deny/stop responsibility;
- distinction between operational authorization and Safety Plane consent;
- fail-safe handling of unknown/stale/conflicting state;
- prohibition on local-interlock bypass.

### TRN-006 — Leonardo

Participant can explain:

- least-privilege scope decisions;
- self-access approval prohibition;
- suspension/revocation effect before execution;
- evidence required for a denied/stale authorization.

### TRN-007 — Leonardo

Participant can explain:

- return-to-service as a distinct approval from maintenance execution;
- why Massimo as Maintainer cannot self-approve return-to-service;
- bounded approval scope and traceability.

### TRN-008 — Both

Each participant can explain:

- the two-person four-eyes model;
- capability suspension when one actor is unavailable;
- no incompatible cross-substitution;
- C4 and break-glass denied by design;
- correlation from request/decision to audit/evidence;
- no runtime authorization implied by completion of C04 validation.

## 5. Attestation format

Each training result must include participant, assessor, date, method, explicit PASS/NOT PASS and a statement that the learning outcomes were reviewed.

### Leonardo assesses Massimo — TRN-001, TRN-002, TRN-003

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

### Massimo assesses Leonardo — TRN-004, TRN-005, TRN-006, TRN-007

```text
Participant: Leonardo Di Egidio
Assessor: Massimo Mainini
Controls: TRN-004, TRN-005, TRN-006, TRN-007
Method: governed-document briefing + question/answer confirmation
Material: OPSC-CMD-001, AP-012, Operational Runbook Standard, Responsibility Matrix, Sponsor Decision, applicable VM evidence
Date: YYYY-MM-DD
Decision: PASS | NOT PASS
Statement: I confirm that Leonardo reviewed the governed material and demonstrated understanding of the required learning outcomes for TRN-004, TRN-005, TRN-006 and TRN-007.
```

### Reciprocal TRN-008

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

**READY FOR CROSS-ATTESTED EXECUTION — TRN-001 THROUGH TRN-008 REMAIN PENDING UNTIL ATTRIBUTABLE ASSESSOR DECISIONS ARE RECORDED.**
