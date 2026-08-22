# ARB-012-C04 — Identity Assurance Execution Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-IDV-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Target model | Two-Person Limited Operations Model |
| Date | 2026-08-22 |
| Status | Ready for reciprocal attestation |
| Runtime effect | None |

## 1. Purpose

Provide the attributable execution record for IDV-001 through IDV-005 under the approved two-person model. This file records only non-sensitive identity/account assurance evidence. It must never contain passwords, MFA seeds, recovery codes, private keys or identity-document images/numbers.

## 2. Governed project identities

The repository already establishes the following nominative governance mapping:

| Project identity | Natural person | Governed role group | Repository basis |
|---|---|---|---|
| DSG-PERSON-001 | Massimo Mainini | Sponsor, Architecture, Operations, Service, Technical Owner, Operator, Maintainer | `ARB-012-C04-Sponsor-Nomination-Decision.md` |
| DSG-PERSON-002 | Leonardo Di Egidio | C3 Approver, Return-to-Service Approver, Safety Authority, Security Authority | `ARB-012-C04-Sponsor-Nomination-Decision.md` |

These mappings are governance records, not identity-verification results. They support the subject names for IDV execution but do not make IDV-001/002 `Passed` by themselves.

## 3. IDV execution matrix

| Check | Subject | Required reciprocal verifier | Evidence required | Current result |
|---|---|---|---|---|
| IDV-001 | Massimo Mainini / `DSG-PERSON-001` | Leonardo Di Egidio | Leonardo confirms natural-person identity and project mapping using an authoritative project-context source; no sensitive document data committed | Pending attestation |
| IDV-002 | Leonardo Di Egidio / `DSG-PERSON-002` | Massimo Mainini | Massimo confirms natural-person identity and project mapping using an authoritative project-context source; no sensitive document data committed | Pending attestation |
| IDV-003 | Massimo validation authentication account | Leonardo Di Egidio | account identifier/username, non-shared ownership confirmation, authentication context | Pending account evidence |
| IDV-004 | Leonardo validation authentication account | Massimo Mainini | account identifier/username, non-shared ownership confirmation, authentication context | Pending account evidence |
| IDV-005 | Both validation accounts | Reciprocal confirmation | explicit statement that usernames, credentials, sessions and authentication factors are distinct; no secret values recorded | Pending account evidence |

## 4. Reciprocal attestation templates

### IDV-001 — Massimo identity

```text
Control: IDV-001
Subject: Massimo Mainini / DSG-PERSON-001
Verified-by: Leonardo Di Egidio
Verification-source-class: <project register / known-person verification / approved account platform / other>
Date-UTC: <timestamp>
Result: Passed | Failed
Statement: I confirm that Massimo Mainini is the natural person mapped to DSG-PERSON-001 for the Digital StarGate project.
Notes: <non-sensitive notes>
```

### IDV-002 — Leonardo identity

```text
Control: IDV-002
Subject: Leonardo Di Egidio / DSG-PERSON-002
Verified-by: Massimo Mainini
Verification-source-class: <project register / known-person verification / approved account platform / other>
Date-UTC: <timestamp>
Result: Passed | Failed
Statement: I confirm that Leonardo Di Egidio is the natural person mapped to DSG-PERSON-002 for the Digital StarGate project.
Notes: <non-sensitive notes>
```

### IDV-003 — Massimo account ownership

```text
Control: IDV-003
Subject: DSG-PERSON-001
Validation-account-id: <non-production username/account ID>
Verified-by: Leonardo Di Egidio
Shared-account: No
Ownership-verification-method: <interactive login witnessed / platform ownership record / other>
Date-UTC: <timestamp>
Result: Passed | Failed
Notes: <no secrets>
```

### IDV-004 — Leonardo account ownership

```text
Control: IDV-004
Subject: DSG-PERSON-002
Validation-account-id: <non-production username/account ID>
Verified-by: Massimo Mainini
Shared-account: No
Ownership-verification-method: <interactive login witnessed / platform ownership record / other>
Date-UTC: <timestamp>
Result: Passed | Failed
Notes: <no secrets>
```

### IDV-005 — distinct credentials and factors

```text
Control: IDV-005
Massimo-account-id: <non-production username/account ID>
Leonardo-account-id: <non-production username/account ID>
Distinct-usernames: Yes | No
Distinct-credentials: Yes | No
Distinct-authentication-factors: Yes | No | Not Applicable with rationale
Distinct-sessions-demonstrated: Yes | No
Verified-by: Massimo Mainini + Leonardo Di Egidio (reciprocal attestation)
Date-UTC: <timestamp>
Result: Passed | Failed
Notes: <never record secret values>
```

## 5. Acceptance rules

IDV-001 through IDV-005 may be marked `Passed` only when:

- neither person self-verifies their own natural-person mapping;
- account identifiers are non-production and unique;
- shared accounts are prohibited;
- distinct credentials/sessions are attested without exposing secrets;
- failed checks remain preserved and are not overwritten;
- every result has verifier and date attribution.

No third person is required under the approved Two-Person Limited Operations Model.

## 6. Current disposition

**READY FOR RECIPROCAL ATTESTATION.**

The repository establishes the governed subject identities, but does not contain enough attributable human/account evidence to mark IDV-001 through IDV-005 as `Passed`. All five checks remain `Pending` until the reciprocal attestations above are completed.