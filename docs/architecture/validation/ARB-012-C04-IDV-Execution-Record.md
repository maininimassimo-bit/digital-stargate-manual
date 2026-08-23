# ARB-012-C04 — Identity Assurance Execution Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-IDV-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Target model | Two-Person Limited Operations Model |
| Date | 2026-08-23 |
| Status | **PASS — IDV-001..IDV-005 complete** |
| Runtime effect | None |

## 1. Purpose

Provide the attributable execution record for IDV-001 through IDV-005 under the approved two-person model. This file records only non-sensitive identity/account assurance evidence. It must never contain passwords, PATs, MFA seeds, recovery codes, private keys or identity-document images/numbers.

This record separates technical account/session evidence demonstrated on the isolated validation VM from reciprocal natural-person ownership attestations.

## 2. Governed project identities

| Project identity | Natural person | Validation account | Governed role group | Repository/technical basis |
|---|---|---|---|---|
| DSG-PERSON-001 | Massimo Mainini | `dsgmassimo` | Sponsor, Architecture, Operations, Service, Technical Owner, Operator, Maintainer | Sponsor decision + VM-R03 / ACC-001 PASS |
| DSG-PERSON-002 | Leonardo Di Egidio | `dsgleonardo` | C3 Approver, Return-to-Service Approver, Safety Authority, Security Authority | Sponsor decision + VM-R04 / ACC-002 PASS |

The VM evidence demonstrates distinct Unix identities and distinct authenticated validation sessions. Reciprocal human attestations establish the natural-person/account ownership mapping without storing sensitive identity or credential material.

## 3. IDV execution matrix

| Check | Subject | Reciprocal verifier | Evidence | Result |
|---|---|---|---|---|
| IDV-001 | Massimo / DSG-PERSON-001 | Leonardo | Sponsor/governance mapping + Leonardo reciprocal attestation | **PASS — 2026-08-23** |
| IDV-002 | Leonardo / DSG-PERSON-002 | Massimo | Sponsor/governance mapping + Massimo reciprocal attestation | **PASS — 2026-08-22** |
| IDV-003 | Massimo / `dsgmassimo` | Leonardo | VM-R03 / ACC-001 + Leonardo ownership attestation | **PASS — 2026-08-23** |
| IDV-004 | Leonardo / `dsgleonardo` | Massimo | VM-R04 / ACC-002 + Massimo ownership attestation | **PASS — 2026-08-22** |
| IDV-005 | Both | Reciprocal | VM-R03 + VM-R04 + reciprocal confirmation of non-shared credentials/factors | **PASS — 2026-08-23** |

## 4. Recorded reciprocal attestations

### 4.1 Massimo verifies Leonardo — RECORDED PASS

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

### 4.2 Leonardo verifies Massimo — RECORDED PASS

```text
Control set: IDV-001, IDV-003, reciprocal part of IDV-005
Subject: Massimo Mainini / DSG-PERSON-001 / dsgmassimo
Verified-by: Leonardo Di Egidio
Verification-source-class: known-person verification + isolated validation account/session evidence
Shared-account: No
Distinct-credentials/factors from Leonardo: Yes
Decision: PASS
Date: 2026-08-23
Statement: Leonardo Di Egidio confirms that Massimo Mainini is the natural person mapped to DSG-PERSON-001, that dsgmassimo is Massimo's assigned non-shared non-production validation account, and that credentials/authentication factors are not shared with Leonardo.
Source of attestation: direct reciprocal verifier confirmation recorded in the governed ARB-012-C04 workflow.
```

## 5. Evidence handling rules

Do not commit or paste identity-document scans/numbers, passwords, PATs/API tokens, MFA seeds, recovery codes, private keys or screenshots containing secret material.

The attributable attestation text, verifier, date and explicit result are sufficient for this bounded validation governance record.

## 6. Acceptance rules

IDV-001 through IDV-005 require reciprocal verification across distinct subjects. Neither person may self-verify their own natural-person/account ownership mapping.

## 7. Current disposition

**PASS — IDV-001 THROUGH IDV-005 COMPLETE. IDENTITY ASSURANCE BLOCK 5/5 PASS.**
