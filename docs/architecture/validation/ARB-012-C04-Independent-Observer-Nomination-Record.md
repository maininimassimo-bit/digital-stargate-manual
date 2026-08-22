# ARB-012-C04 — Independent Observer / Reviewer Nomination Record

| Field | Value |
|---|---|
| Record ID | E-ARB012-C04-07 |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Related work items | C04-W03, C04-W06, C04-W07, C04-W08 |
| Date | 2026-08-22 |
| Status | Pending nomination |
| Runtime effect | None |

## 1. Purpose

Establish the formal evidence record required to nominate an attributable independent observer/reviewer for conflicted ARB-012-C04 controls.

This record does not nominate a person by inference. The repository currently contains no evidence of an accepted independent observer/reviewer nomination. The named individual, independence declaration and approval disposition must therefore be supplied explicitly before this record can move from `Pending nomination` to `Active`.

## 2. Required independence

The nominated observer/reviewer must be a natural person who, for the control being reviewed:

- is not the requester;
- is not the approver;
- is not the executor;
- does not approve their own access, role, training or evidence;
- has no material conflict that would make the review self-benefiting;
- can inspect the evidence needed for the assigned scope;
- has no production command authority implied by this nomination.

The role is evidence/governance authority only. It does not grant observatory runtime access, physical-device control, VPN access, credentials, break-glass authority, local-interlock override or positive C4 authority.

## 3. Nomination register

| Attribute | Required value | Current value |
|---|---|---|
| Observer ID | Stable project identity | Pending |
| Natural person | Full name | Pending |
| Identity verification reference | Non-sensitive evidence reference | Pending |
| Independence statement | Explicit no-conflict declaration for assigned controls | Pending |
| Authorized scope | W03 conflicted checks / `E-ENV011-06` / W07 evidence sufficiency / W08 review as applicable | Pending |
| Start date | Effective date | Pending |
| End/review date | Expiry or next review | Pending |
| Sponsor approval | Attributable approving authority | Pending |
| Observer acceptance | Attributable acceptance of role | Pending |
| Status | Pending / Active / Suspended / Revoked / Expired | Pending |

## 4. Minimum nomination statement

The accepted record must contain an attributable statement equivalent to:

> I accept the ARB-012-C04 independent observer/reviewer role for the stated scope. I confirm that I am not requester, approver or executor for the controls I independently review, and I will declare any conflict before reviewing evidence.

The statement must include the observer identity, date and scope. A GitHub-authenticated comment, signed review record, approved evidence file or other attributable project record may be used, provided the identity and disposition are unambiguous.

## 5. Initial authorized scope

Once nominated and accepted, the observer/reviewer may be used for the following non-operational controls, subject to conflict check per item:

| Scope | Purpose |
|---|---|
| W03 identity assurance | non-self verification for IDV controls where Massimo/Leonardo cannot independently verify themselves |
| W03 training/access sufficiency | independent review of conflicted training and access decisions |
| AR-005 / AR-006 / AR-007 | independent disposition where existing two-person allocation is conflicted |
| REV-002 | witness/reviewer for suspension of Leonardo approval eligibility initiated by Massimo |
| `E-ENV011-06` | attributable independent review of the already complete ENV-011 technical evidence |
| W07 selected FE scenarios | independent witness/reviewer for scenarios where both current participants hold conflicting roles |
| W08 | evidence sufficiency input for final ARB re-review, if independence remains valid |

The observer/reviewer does not become a C3/C4 approver, Safety Authority, Security Authority, Operator or Maintainer by virtue of this record.

## 6. Conflict check

Before each evidence disposition, record:

```text
Control: <IDV/TRN/AR/REV/ENV/FE identifier>
Observer: <project identity>
Requester in this control: yes/no
Approver in this control: yes/no
Executor in this control: yes/no
Material conflict identified: yes/no
Disposition permitted: yes/no
Date-UTC: <timestamp>
```

If any material conflict is identified, the observer must abstain and the control remains `Pending` until another independent reviewer is available.

## 7. Evidence handling

The observer may review:

- repository documents and version history;
- non-sensitive account identifiers and role exports;
- validation logs, timestamps, correlation IDs and audit records;
- screenshots that contain no secrets or sensitive identity-document data;
- simulator configuration and checksum evidence;
- failed as well as successful validation evidence.

The observer must not require passwords, private keys, MFA seeds, recovery codes or identity-document images to be committed to the repository.

## 8. Activation criteria

This nomination record becomes `Active` only when all of the following are recorded:

1. observer project identity and natural-person name;
2. non-sensitive identity-verification reference;
3. explicit independence statement;
4. authorized scope;
5. effective and review dates;
6. sponsor/governance approval;
7. observer acceptance of the role.

Until then, the following remain blocked or pending:

- final W03 sufficiency review;
- AR-007;
- independent disposition for conflicted AR-005/AR-006 controls;
- REV-002 final acceptance;
- `E-ENV011-06` formal disposition;
- W07 scenarios that require an independent witness.

## 9. Revocation and expiry

The nomination must be suspended or revoked if:

- the observer becomes requester, approver or executor for the same control;
- a material conflict emerges;
- identity attribution becomes uncertain;
- review scope expires;
- evidence integrity is challenged and cannot be resolved.

Revocation must not delete prior review evidence; the history and reason remain traceable.

## 10. Current disposition

**PENDING NOMINATION.**

No person is nominated by this document. It establishes the exact evidence contract needed to unblock the independent-review dependency in C04-W03 and `E-ENV011-06` while preserving ARB-012-C04 fail-safe governance.