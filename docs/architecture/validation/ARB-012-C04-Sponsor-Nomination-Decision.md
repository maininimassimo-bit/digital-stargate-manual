# ARB-012-C04 — Sponsor Nomination Decision

| Field | Value |
|---|---|
| Decision ID | ARB-012-C04-DEC-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Decision authority | Massimo Mainini — Project Owner / Architecture Sponsor |
| Status | **Approved — Two-Person Limited Operations Model** |
| Effective date | 2026-08-22 |
| Runtime effect | None — runtime authorization remains a separate gate |

## 1. Decision

The Project Owner / Architecture Sponsor adopts a **Two-Person Limited Operations Model** as the target governance model for ARB-012-C04.

The model intentionally uses two natural persons only:

- **Massimo Mainini** — operational, service, technical, requester/executor and maintenance-side responsibilities;
- **Leonardo Di Egidio** — C3 approval, return-to-service approval, Safety Authority and Security Authority responsibilities within the separately authorized scope.

A third permanent actor, independent substitute or independent internal Auditor is **not a closure requirement** for this target model.

This is a governance redesign, not a waiver of segregation. Controls that cannot be satisfied safely with two persons are not weakened: they are explicitly **denied or classified N/A by governance design**.

## 2. Supported and unsupported capabilities

| Capability | Target disposition |
|---|---|
| C0–C2 | May be separately authorized under applicable policy and safety controls |
| C3 request + approval | **Supported** with Massimo requester/executor and Leonardo independent approver |
| Self-approval | **DENIED** |
| Maintainer / Return-to-Service separation | **Supported** — Massimo / Leonardo |
| Safety Authority separation from Operations | **Supported** — Leonardo / Massimo |
| Security Authority self-access approval | **DENIED** |
| Positive C4 | **DENIED by governance design** |
| Break-glass | **DENIED by governance design** |
| Independent internal audit closure | **N/A by governance design** |
| Cross-substitution of incompatible roles | **DENIED** |
| Local safety/interlock bypass | **DENIED** |

## 3. Role assignments

| Role | Primary identity | Substitute | Target disposition |
|---|---|---|---|
| Operations Lead / Service Owner / Technical Owner | Massimo Mainini | None | Approved |
| Operator / Requester | Massimo Mainini | None | Approved within separately authorized scope |
| Incident Coordinator | Massimo Mainini | None | Approved |
| Maintainer | Massimo Mainini | None | Approved; cannot self-approve return to service |
| C3 Approver | Leonardo Di Egidio | None | Approved; cannot be requester for same action |
| Return-to-Service Approver | Leonardo Di Egidio | None | Approved; independent from Maintainer |
| Safety Authority | Leonardo Di Egidio | None | Approved for permit/deny/stop governance; local interlocks remain authoritative |
| Security Authority | Leonardo Di Egidio | None | Approved for Massimo access decisions; self-access approval denied |
| C4 Second Approver | Not part of target model | N/A | Positive C4 denied |
| Independent internal Auditor | Not part of target model | N/A | Independent audit closure not claimed |

## 4. Conflict disposition

| Conflict | Disposition under two-person model |
|---|---|
| Operational/technical concentration in Massimo | Accepted with self-approval prohibition and independent C3/return-to-service decisions by Leonardo |
| Approval/safety/security concentration in Leonardo | Accepted only within bounded two-person scope; Leonardo cannot approve own access or independently audit controls he operated |
| No third C4 actor | **Resolved by prohibition** — positive C4 remains denied, not pending staffing |
| No independent internal Auditor | **Resolved by scope limitation** — independent audit closure is not claimed as a C04 target |
| No substitutes | **Accepted degraded-availability model** — absence of either actor suspends capabilities requiring both; no incompatible cross-substitution |

## 5. Evidence still required

Adoption of the two-person target does not complete C04. The following still require attributable evidence:

- IDV-001 through IDV-005 identity/account separation;
- TRN-001 through TRN-008 training/briefing evidence;
- least-privilege decisions for the two-person supported scope;
- distinct non-production validation accounts;
- revocation/suspension enforcement;
- remaining environment controls and formal disposition of ENV-011 under the revised target;
- FE scenarios proving C3 separation, self-approval denial, revocation, return-to-service separation, safety/security conflict denial, C4 denial and break-glass denial;
- repository quality gates and final ARB re-review of the revised target model.

## 6. Explicit N/A classifications

The following requirements from the earlier three-person closure design are superseded and must no longer block C04:

- independent substitutes for critical roles;
- a third actor for positive C4;
- independent internal Auditor appointment;
- third-party observer nomination solely to close two-person controls;
- positive C4 execution/validation;
- independent internal audit closure.

These items are **N/A by governance design**, not `Passed`.

## 7. Sponsor attestation

```text
Decision: Adopt Two-Person Limited Operations Model for ARB-012-C04
Decision date: 2026-08-22
Approved by: Massimo Mainini — Project Owner / Architecture Sponsor
Scope: Governance and controlled validation model; no runtime authorization implied
Rationale: Digital StarGate will operate the C04 governance boundary with two natural persons. C3 four-eyes, maintenance/return-to-service separation and safety/security separation remain mandatory. Positive C4, break-glass, incompatible cross-substitution and independent internal audit closure are outside the supported target and remain denied or N/A rather than creating an artificial third-person dependency.
```

## 8. Current decision

**TWO-PERSON LIMITED OPERATIONS MODEL APPROVED.**

ARB-012-C04 remains `Blocked` only for the evidence and validation work applicable to this revised two-person target. A third person is no longer a closure prerequisite.