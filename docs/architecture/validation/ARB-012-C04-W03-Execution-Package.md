# ARB-012-C04 W03 — Identity, Training and Access Review Execution Package

| Field | Value |
|---|---|
| Package ID | ARB-012-C04-W03-EXEC-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Parent condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Date | 2026-08-22 |
| Status | Ready for attributable execution |
| Runtime effect | None |
| Environment | Organizational review plus isolated non-operational validation only |

## 1. Purpose

Provide the executable evidence package required to move C04-W03 from a planning framework to an attributable validation campaign without asserting results that have not been performed.

This package does not grant operational authority. It prepares four evidence blocks:

1. identity assurance (`IDV-001`–`IDV-005`);
2. role-specific training (`TRN-001`–`TRN-008`);
3. least-privilege access review (`AR-001`–`AR-007`);
4. revocation/suspension verification required by W03 and later FE-04/FE-05.

`AR-008` positive C4 and `AR-009` break-glass remain denied by governance and are not candidates for enablement.

## 2. Safety and evidence rules

The campaign is evidence-only and non-operational. It must not:

- enable DSOC runtime commands against physical devices;
- import production credentials, VPN profiles or observatory routes;
- bypass local interlocks or safety authorities;
- store passwords, MFA secrets, identity documents, private keys or recovery codes in Git;
- treat self-attestation as independent evidence where a material conflict exists;
- use an AI technical review as substitute for an attributable human reviewer where the ARB condition requires one.

Repository evidence records only the verification outcome, assessor, date, scope and stable reference.

## 3. Execution roles

| Role | Permitted activity in W03 | Prohibited activity |
|---|---|---|
| Massimo Mainini | provide identity/account evidence; complete training; participate in access review; perform non-conflicted sponsor attestations | approve own privileged access; independently verify own identity; close controls from which he materially benefits |
| Leonardo Di Egidio | provide identity/account evidence; complete training; review Massimo access where conflict permits; Security/Safety review in isolated scope | approve own access; independently audit controls he operates; request and approve same operation |
| Independent observer/reviewer | verify conflicted IDV/access/revocation evidence and W03 sufficiency | act as requester, approver or executor in the same witnessed control |

An independent observer is therefore required before W03 can exit `IN PROGRESS`.

## 4. Block A — Identity assurance

### Required evidence

| Check | Evidence to capture | Allowed repository record | Acceptance |
|---|---|---|---|
| IDV-001 | Massimo natural-person identity mapped to unique project identity | reviewer, date, authoritative-source class, project identity reference; no document image/number | Passed only by non-self reviewer |
| IDV-002 | Leonardo natural-person identity mapped to unique project identity | same structure as IDV-001 | Passed only by non-self reviewer |
| IDV-003 | Massimo owns the named non-production authentication account | account identifier/username, ownership verification method, reviewer, date | account must be unique and non-shared |
| IDV-004 | Leonardo owns the named non-production authentication account | same structure as IDV-003 | account must be unique and non-shared |
| IDV-005 | credentials and authentication factors are distinct | attestation of separation only; never secret material | both identities must use distinct credentials/sessions |

### Evidence template

For each IDV item record:

```text
Evidence-ID: E-C04-W03-IDV-<nnn>
Control: IDV-00x
Subject: <identity/project account>
Verification-source-class: <project register / account platform / in-person confirmation / other approved source>
Verified-by: <reviewer>
Date-UTC: <timestamp>
Result: Passed | Failed | Pending
Repository-reference: <stable path/issue/commit>
Notes: <non-sensitive rationale>
```

## 5. Block B — Role-specific training

Training may be a documented briefing, walkthrough or tabletop exercise. Completion requires an assessor and an explicit outcome.

| Training | Subject | Minimum completion evidence |
|---|---|---|
| TRN-001 | C0–C4 classification, boundaries, self-approval prohibition | attendee, assessor, date, material references, explicit Passed/Pending |
| TRN-002 | maintenance safety, rollback, safe state, return-to-service handoff | same |
| TRN-003 | incident recording, audit trail, evidence preservation | same |
| TRN-004 | independent C3 approval and conflict rejection | same |
| TRN-005 | Safety Authority permit/deny/stop and safe-state verification | same |
| TRN-006 | privileged access, least privilege and revocation | same |
| TRN-007 | return-to-service separation from Maintainer | same |
| TRN-008 | four-eyes workflow, approver revocation and audit completeness | both participants plus assessor; conflicts recorded |

A participant must not be the sole assessor for their own training when that training is later used to justify privileged authority.

### Training evidence template

```text
Evidence-ID: E-C04-W03-TRN-<nnn>
Training-Control: TRN-00x
Participant: <identity>
Assessor: <identity>
Date-UTC: <timestamp>
Materials: <repository references>
Assessment-method: briefing | walkthrough | tabletop | course
Result: Passed | Failed | Pending
Notes: <scope and limitations>
```

## 6. Block C — Least-privilege access review

The target state remains deny-by-default. W03 reviews eligibility; it does not authorize production access.

| Review | Subject | Maximum allowed before C04 closure | Required reviewer disposition |
|---|---|---|---|
| AR-001 | Massimo C0–C2 request/execution | isolated simulator context only | explicit Allow/Deny with rationale |
| AR-002 | Massimo C3 request creation | submit only; no approval/execution authority implied | explicit Allow/Deny |
| AR-003 | Massimo maintenance | isolated test activity; no own return-to-service | explicit Allow/Deny |
| AR-004 | Leonardo C3 approval | non-operational validation only; cannot be requester | explicit Allow/Deny with conflict check |
| AR-005 | Leonardo Safety Authority | documented validation decisions only; no physical authority | independent verification required |
| AR-006 | Leonardo Security approval | may approve Massimo scope; cannot approve own access | independent verification required |
| AR-007 | Leonardo audit evidence access | read-only repository evidence only | independent reviewer required; cannot constitute independent audit closure while Leonardo holds control roles |

### Access review evidence template

```text
Evidence-ID: E-C04-W03-AR-<nnn>
Review-Control: AR-00x
Identity: <identity>
Requested-scope: <scope>
Maximum-permitted-scope: <scope>
Reviewer: <identity>
Conflict-check: Passed | Failed | Pending
Decision: Allow | Deny | Pending
Expiry-or-review-date: <date if applicable>
Repository-reference: <stable reference>
Rationale: <non-sensitive explanation>
```

## 7. Block D — Revocation and suspension verification

These checks are non-operational and must use the isolated validation environment once ACC-001/ACC-002 and required authorization plumbing exist.

| Test | Actor / reviewer | Expected result | W04 relationship |
|---|---|---|---|
| REV-001 | Leonardo revokes Massimo Operator eligibility | later execution denied; audit evidence preserved | prerequisite/support for FE-05 |
| REV-002 | Massimo initiates suspension of Leonardo approval eligibility, witnessed by independent observer | prior approval becomes invalid before execution | prerequisite/support for FE-04 |
| REV-003 | validation campaign invalidates pending approval after role suspension | request cannot execute using stale approval | FE-04/FE-05 |
| REV-004 | validation campaign verifies denied access after revocation | denied deterministically and audited | FE-04/FE-05 |

Evidence must include account IDs, role before/after, timestamp, request/correlation ID, policy result, no-execution proof and reviewer disposition. A failure is preserved and blocks later positive FE scenarios.

## 8. Independent observer requirement

An independent observer/reviewer must be nominated before final acceptance of controls where both currently nominated project actors are conflicted.

Minimum nomination record:

```text
Observer-ID: <project identity>
Natural-person verification: <reference, no sensitive document data>
Independence statement: <no requester/approver/executor role in witnessed scenario>
Authorized scope: W03 conflicted checks / E-ENV011-06 / W04 evidence sufficiency
Start date: <date>
End/review date: <date or ongoing>
Approved by: <sponsor/governance authority>
```

Until this role is filled:

- AR-007 remains blocked;
- final acceptance of AR-005/AR-006 remains pending where independent verification is required;
- REV-002 cannot receive final evidence acceptance;
- `E-ENV011-06` cannot receive the required attributable independent disposition;
- W03 cannot complete.

## 9. Execution order

1. nominate independent observer/reviewer;
2. complete IDV-001–IDV-005;
3. complete TRN-001–TRN-008;
4. decide AR-001–AR-007 with conflict checks;
5. create/evidence ACC-001 and ACC-002 under accepted least-privilege decisions;
6. execute REV-001–REV-004 in the isolated environment;
7. update `ARB-012-C04-Identity-Training-Access-Review.md` with attributable results;
8. obtain independent W03 sufficiency disposition;
9. only then evaluate W04/W07 entry criteria.

## 10. Exit criteria

C04-W03 may be marked complete only when:

- IDV-001–IDV-005 are Passed;
- TRN-001–TRN-008 are Passed or have an approved time-bound exception;
- AR-001–AR-007 have explicit attributable decisions;
- ACC-001 and ACC-002 evidence supports distinct non-production sessions;
- REV-001–REV-004 are executed and accepted;
- prohibited C4 and break-glass capabilities remain denied;
- conflicts and limitations are explicitly recorded;
- an independent reviewer declares the W03 evidence sufficient for W04 execution.

## 11. Current disposition

**READY FOR ATTRIBUTABLE EXECUTION — NO CONTROLS ARE MARKED PASSED BY THIS PACKAGE.**

C04-W03 remains `IN PROGRESS`; C04-W07 remains blocked. Runtime activation, production credentials, physical-device control, positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.