# ARB-012-C04 W03 — Identity, Training and Access Review Execution Package

| Field | Value |
|---|---|
| Package ID | ARB-012-C04-W03-EXEC-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Parent condition | ARB-012-C04 |
| Updated | 2026-08-22 |
| Target model | Two-Person Limited Operations Model |
| Status | Ready for attributable two-person execution |
| Runtime effect | None |

## 1. Purpose

Provide the evidence package for the Sponsor-approved two-person target without requiring a third observer. No control is marked Passed by this document.

## 2. Evidence blocks

1. IDV-001–IDV-005 — identity and distinct-account assurance;
2. TRN-001–TRN-008 — role-specific training/briefing;
3. AR-001–AR-006 — least-privilege decisions for supported two-person roles;
4. REV-001–REV-004 — revocation/suspension and stale-authorization denial.

Former AR-007 independent internal audit closure is **N/A by governance design**. Positive C4 and break-glass remain denied.

## 3. Review rules

- Massimo may not approve his own privileged access or C3 request.
- Leonardo may review Massimo access within his Security Authority scope.
- Leonardo may not approve his own access; such a request must be denied under the two-person model.
- Each person may attest the other person's identity/account evidence where the reviewer is not the beneficiary.
- Training may be cross-attested between the two participants when the assessor is not certifying their own completion.
- No evidence may be labelled independent internal audit.

## 4. Identity assurance

| Check | Subject | Reviewer model | Target |
|---|---|---|---|
| IDV-001 | Massimo natural person -> project identity | Leonardo | Passed/Failed after attributable review |
| IDV-002 | Leonardo natural person -> project identity | Massimo | Passed/Failed after attributable review |
| IDV-003 | Massimo owns unique non-production account | Leonardo | unique, non-shared account |
| IDV-004 | Leonardo owns unique non-production account | Massimo | unique, non-shared account |
| IDV-005 | credentials/sessions are distinct | reciprocal evidence, no secrets | deterministic separation |

Repository records must not contain identity-document numbers/images, passwords, MFA seeds, recovery codes or private keys.

## 5. Training

TRN-001–TRN-008 remain required unless a bounded exception is explicitly approved. Training covers C0–C4 boundaries, self-approval prohibition, maintenance/safe state, incident evidence, C3 approval, Safety Authority, least privilege/revocation, return-to-service separation and four-eyes/audit traceability.

For each item record participant, assessor, date, material reference, method and result. A person cannot be the sole assessor of their own completion.

## 6. Least-privilege access review

| Review | Target decision |
|---|---|
| AR-001 Massimo C0–C2 request/execution | Allow only within separately authorized scope |
| AR-002 Massimo C3 request/execution | Allow request/execution only after Leonardo approval |
| AR-003 Massimo maintenance | Allow within test scope; own return-to-service denied |
| AR-004 Leonardo C3 approval | Allow for Massimo requests; same-action requester role denied |
| AR-005 Leonardo Safety Authority | Allow bounded safety governance; no physical-interlock bypass |
| AR-006 Leonardo Security Authority | Allow Massimo access governance; Leonardo self-access approval denied |
| AR-007 independent internal audit | **N/A by governance design** |
| AR-008 positive C4 | **DENIED by governance design** |
| AR-009 break-glass | **DENIED by governance design** |

## 7. Revocation/suspension verification

| Test | Two-person target |
|---|---|
| REV-001 | Leonardo revokes/suspends Massimo eligibility; later execution denied |
| REV-002 | Massimo as Sponsor suspends Leonardo approval eligibility; stale approval becomes invalid; no third witness required, but full audit trail is mandatory |
| REV-003 | pending approval invalidated after role suspension |
| REV-004 | denied access after revocation is deterministic and audited |

If a scenario creates a self-benefiting authorization instead of a denial, it fails.

## 8. Execution order

1. complete IDV-001–IDV-005;
2. complete TRN-001–TRN-008;
3. decide AR-001–AR-006 and record AR-007 N/A / AR-008-009 denied;
4. create/evidence ACC-001 and ACC-002 distinct non-production accounts;
5. execute REV-001–REV-004 in the isolated environment;
6. update `ARB-012-C04-Identity-Training-Access-Review.md`;
7. reconcile W06/ENV evidence to the same two-person target;
8. evaluate W04/W07 entry criteria.

## 9. Exit criteria

W03 completes when:

- IDV-001–IDV-005 pass;
- TRN-001–TRN-008 pass or have approved bounded exceptions;
- AR-001–AR-006 have attributable decisions;
- AR-007 is recorded N/A, AR-008 and AR-009 denied;
- ACC-001/ACC-002 prove distinct non-production sessions;
- REV-001–REV-004 pass;
- no self-approval or incompatible cross-substitution succeeds.

A third person, independent substitute or independent internal audit is not an exit criterion.

## 10. Current disposition

**READY FOR ATTRIBUTABLE TWO-PERSON EXECUTION — NO CONTROLS ARE MARKED PASSED BY THIS PACKAGE.**

Runtime activation, production credentials, physical-device control, positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.