# ARB-012-C04 — Identity Assurance Execution Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-IDV-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Target model | Two-Person Limited Operations Model |
| Date | 2026-08-22 |
| Status | **Partial PASS — Massimo attestation recorded; Leonardo attestation pending** |
| Runtime effect | None |

## 1. Purpose

Provide the attributable execution record for IDV-001 through IDV-005 under the approved two-person model. This file records only non-sensitive identity/account assurance evidence. It must never contain passwords, PATs, MFA seeds, recovery codes, private keys or identity-document images/numbers.

This record separates technical account/session evidence already demonstrated on the isolated validation VM from natural-person ownership attestations that must be made by the other person.

## 2. Governed project identities

| Project identity | Natural person | Validation account | Governed role group | Repository/technical basis |
|---|---|---|---|---|
| DSG-PERSON-001 | Massimo Mainini | `dsgmassimo` | Sponsor, Architecture, Operations, Service, Technical Owner, Operator, Maintainer | Sponsor decision + VM-R03 / ACC-001 PASS |
| DSG-PERSON-002 | Leonardo Di Egidio | `dsgleonardo` | C3 Approver, Return-to-Service Approver, Safety Authority, Security Authority | Sponsor decision + VM-R04 / ACC-002 PASS |

The VM evidence demonstrates distinct Unix identities and distinct authenticated validation sessions. Governance mapping and technical account existence do not by themselves prove natural-person ownership.

## 3. IDV execution matrix

| Check | Subject | Reciprocal verifier | Evidence already proven | Human attestation | Current result |
|---|---|---|---|---|---|
| IDV-001 | Massimo / DSG-PERSON-001 | Leonardo | Sponsor/governance mapping exists | Leonardo confirmation required | **Pending Leonardo attestation** |
| IDV-002 | Leonardo / DSG-PERSON-002 | Massimo | Sponsor/governance mapping exists | Massimo attested PASS on 2026-08-22 | **PASS** |
| IDV-003 | Massimo / `dsgmassimo` | Leonardo | VM-R03 / ACC-001 proves distinct non-production account/session, UID 1001, no sudo | Leonardo ownership confirmation required | **Technical PASS / Leonardo ownership pending** |
| IDV-004 | Leonardo / `dsgleonardo` | Massimo | VM-R04 / ACC-002 proves distinct non-production account/session, UID 1002, no sudo | Massimo attested PASS on 2026-08-22 | **PASS** |
| IDV-005 | Both | Reciprocal | VM-R03 + VM-R04 prove distinct usernames and sessions | Massimo half PASS; Leonardo half pending | **Partial PASS** |

## 4. Recorded reciprocal attestations

### 4.1 Massimo verifies Leonardo — RECORDED

```text
Control set: IDV-002, IDV-004, reciprocal part of IDV-005
Subject: Leonardo Di Egidio / DSG-PERSON-002 / dsgleonardo
Verified-by: Massimo Mainini
Verification-source-class: known-person verification + isolated validation account/session evidence
Shared-account: No
Distinct-credentials/factors from Massimo: Yes
Decision: PASS
Date: 2026-08-22
Statement: Massimo Mainini confirms that Leonardo Di Egidio is the natural person mapped to DSG-PERSON-002, that dsgleonardo is Leonardo's assigned non-shared non-production validation account, and that credentials/authentication factors are not shared with Massimo.
Source of attestation: direct project-owner confirmation recorded in the governed ARB-012-C04 workflow.
```

This attestation satisfies IDV-002 and IDV-004 and the Massimo reciprocal half of IDV-005.

### 4.2 Leonardo verifies Massimo — PENDING

```text
Control set: IDV-001, IDV-003, reciprocal part of IDV-005
Subject: Massimo Mainini / DSG-PERSON-001 / dsgmassimo
Verified-by: Leonardo Di Egidio
Verification-source-class: known-person verification + isolated validation account/session evidence
Shared-account: No
Distinct-credentials/factors from Leonardo: Yes
Decision: PASS | NOT PASS
Date: YYYY-MM-DD
Statement: I confirm that Massimo Mainini is the natural person mapped to DSG-PERSON-001, that dsgmassimo is Massimo's assigned non-shared non-production validation account, and that credentials/authentication factors are not shared with Leonardo.
Notes: <non-sensitive notes only>
```

## 5. Evidence handling rules

Do not commit or paste identity-document scans/numbers, passwords, PATs/API tokens, MFA seeds, recovery codes, private keys or screenshots containing secret material.

The attributable attestation text, verifier, date and explicit result are sufficient for this bounded validation governance record.

## 6. Acceptance rules

IDV-001 through IDV-005 may be marked fully `Passed` only after both reciprocal attestations are recorded with explicit `PASS` decisions and dates. Neither person may self-verify their own natural-person/account ownership mapping.

Technical account/session evidence remains valid independently and must not be downgraded while the Leonardo attestation is pending.

## 7. Current disposition

**PARTIAL PASS — IDV-002 AND IDV-004 PASS; MASSIMO HALF OF IDV-005 PASS. IDV-001, IDV-003 AND LEONARDO HALF OF IDV-005 REMAIN PENDING.**
