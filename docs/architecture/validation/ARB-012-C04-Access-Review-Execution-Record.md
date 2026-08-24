# ARB-012-C04 — Least-Privilege Access Review Execution Record

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-AR-001 |
| Work item | C04-W03 — Identity, Training and Access Review Evidence |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Target model | Two-Person Limited Operations Model |
| Prepared | 2026-08-23 |
| Updated | 2026-08-24 |
| Status | **Partial PASS — AR-004..AR-006 complete; AR-001..AR-003 pending Leonardo decision** |
| Runtime effect | None |

## 1. Purpose

Record attributable least-privilege decisions for AR-001 through AR-006. This record does not grant runtime access and does not replace technical authorization policy. Each reviewer assesses only the other person's bounded target scope.

## 2. Governing basis

The Sponsor Nomination Decision establishes the approved two-person target:

- Massimo Mainini owns operational/requester/maintenance-side responsibilities;
- Leonardo Di Egidio owns C3 approval, return-to-service, Safety Authority and Security Authority responsibilities;
- self-approval, own-access approval, positive C4, break-glass, incompatible cross-substitution and local-interlock bypass remain denied;
- runtime authorization is a separate gate.

Technical evidence already proves distinct validation accounts, self-approval denial, suspension enforcement, C4/break-glass denial and simulator-only/no-production-fallback behavior.

## 3. Access-review matrix

| Review | Subject | Maximum target scope | Reviewer | Required least-privilege decision | Current result |
|---|---|---|---|---|---|
| AR-001 | Massimo | C0-C2 validation | Leonardo | Isolated simulator context only; no production/physical-device access | Pending Leonardo decision |
| AR-002 | Massimo | C3 request | Leonardo | Submit/request only under validated four-eyes workflow; no self-approval | Pending Leonardo decision |
| AR-003 | Massimo | Maintenance | Leonardo | Isolated maintenance only; cannot approve own return-to-service | Pending Leonardo decision |
| AR-004 | Leonardo | C3 approval | Massimo | May approve Massimo C3 request; cannot request/approve same action | **PASS — 2026-08-24** |
| AR-005 | Leonardo | Safety Authority | Massimo | Bounded permit/deny/stop validation decisions; no local-interlock bypass | **PASS — 2026-08-24** |
| AR-006 | Leonardo | Security Authority | Massimo | May approve Massimo scope; own-access approval prohibited | **PASS — 2026-08-24** |
| AR-007 | Independent internal audit | N/A | N/A | Outside approved target | **N/A by governance design** |
| AR-008 | Positive C4 | Unsupported | Policy enforcement | Must remain unavailable | **DENIED — VM-R11 PASS** |
| AR-009 | Break-glass | Unsupported | Policy enforcement | Must remain unavailable | **DENIED — VM-R11 PASS** |

## 4. Massimo reviews Leonardo — RECORDED PASS

```text
Reviewer: Massimo Mainini — Project Owner / Architecture Sponsor
Subject: Leonardo Di Egidio
Controls: AR-004, AR-005, AR-006
Date: 2026-08-24
Decision: PASS
Statement: Massimo Mainini confirms that Leonardo Di Egidio's least-privilege scope is limited to independent approval of Massimo C3 requests without being requester and approver for the same action; bounded Safety Authority permit/deny/stop decisions without bypassing local interlocks; and Security Authority decisions on Massimo's scope without approving Leonardo's own access. This review does not authorize runtime, production, physical-device-control, positive-C4 or break-glass privileges.
Source of attestation: direct reviewer confirmation recorded in the governed ARB-012-C04 workflow.
```

This closes AR-004, AR-005 and AR-006 as PASS.

## 5. Leonardo reviews Massimo — AR-001, AR-002, AR-003

```text
Reviewer: Leonardo Di Egidio
Subject: Massimo Mainini
Controls: AR-001, AR-002, AR-003
Date: YYYY-MM-DD
Decision: PASS | NOT PASS

I confirm that the maximum least-privilege scope for Massimo is limited to:
- AR-001: C0-C2 validation in the isolated simulator context only, with no production or physical-device access;
- AR-002: C3 submit/request capability only under the validated four-eyes workflow; self-approval remains prohibited;
- AR-003: isolated maintenance activity only; Massimo cannot approve his own return-to-service.

I confirm that no broader runtime, production, physical-device, positive-C4 or break-glass privilege is authorized by this review.
```

## 6. Acceptance rules

- AR-001 through AR-006 require explicit reviewer decisions;
- each reviewer assesses only the other person's scope;
- PASS means the maximum target scope is accepted as least-privilege, not that runtime access is activated;
- any requested broader scope requires a new governed decision;
- AR-007 remains N/A; AR-008 and AR-009 remain denied.

## 7. Current disposition

**PARTIAL PASS — AR-004 THROUGH AR-006 COMPLETE; AR-001 THROUGH AR-003 REQUIRE LEONARDO'S ATTRIBUTABLE DECISION.**
