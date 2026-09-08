# RQ-BKL-038-F3-A — Release Quality Review — 2026-09-08

| Field | Value |
|---|---|
| Review ID | `RQ-BKL-038-F3-A` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Scope | F3-A — Deterministic Derived Identity Contract |
| PR | #122 |
| Reviewed HEAD | `97ce7c311ca040a9b5ef493391af8cddb1d2c864` |
| Base | `92cec8ab9b89602960b2cd3ca9369ce52a64e72f` |
| ARB | `ARB-BKL-038-F3-A` — APPROVED 98/100 |
| Decision | **READY FOR MERGE** |
| Waiver | None |

## 1. Release impact report

F3-A is a repository-only, additive architecture/validation increment. It introduces a versioned canonical derived-record identity algorithm, fixed serialization semantics, SHA-256 logical IDs, known-answer/idempotence/fail-closed tests, Developer Foundation integration, and governance documentation.

It does not introduce anomaly thresholds, severity policy, causal/root-cause inference, predictive maintenance, BKL-030 EAGLE history onboarding, runtime collectors/services/schedulers, command execution, automatic remediation or Safety Authority.

## 2. Quality-gate matrix

| Gate | Status | Evidence |
|---|---|---|
| Architecture review | Passed | ARB `APPROVED — 98/100` on package head `0d643f018c725aa2ea0ec58a44e557d75cdd3532` |
| Documentation | Passed | Validate documentation #716 — SUCCESS |
| Word/manual generation | Passed | Genera manuale Word #1141 — SUCCESS |
| Build | Passed | Developer Foundation #1097 — SUCCESS |
| Unit / integration / architecture tests | Passed | Developer Foundation #1097 — SUCCESS |
| Formatting | Passed | Developer Foundation #1097 — formatting verification SUCCESS |
| BKL-038 F2 regression | Passed | Developer Foundation #1097 F2 validator and fail-closed suite SUCCESS |
| BKL-038 F3 deterministic identity | Passed | Developer Foundation #1097 `Test BKL-038 F3 deterministic identity` — SUCCESS |
| Known-answer vector | Passed | F3 test suite reproduces governed SHA-256 expected value |
| Idempotence | Passed | Same identity tuple yields same derived id |
| Identity sensitivity | Passed | source order, semantic type, method version and time window are regression-tested |
| Identity neutrality | Passed | non-identity fields do not perturb logical ID |
| Roadmap / backlog consistency | Passed | Developer Foundation #1097 consistency gates SUCCESS |
| MkDocs / links | Passed | Developer Foundation #1097 MkDocs verification SUCCESS |
| Security | Passed / bounded | No new credentials, endpoint, listener or external execution surface |
| Safety | Passed | Repository projection only; no command/remediation/Safety Authority |
| Observability | Not Applicable | No runtime component introduced |
| Migration | Not Applicable | No runtime/data migration |
| Rollback | Passed | Repository revert is sufficient |
| Operations | Not Applicable | No PC/EAGLE action required |

## 3. Definition of Done

F3-A satisfies its bounded acceptance criteria:

- canonical identity algorithm is versioned;
- exact identity tuple is explicit;
- fixed-order compact JSON serialization is governed;
- SHA-256 output format is fixed;
- known-answer vector passes;
- idempotence passes;
- source order is identity-significant;
- semantic type, method version and time window are identity-significant;
- non-identity fields are identity-neutral;
- malformed identity input fails closed;
- Developer Foundation executes the F3 tests;
- documentation/build/test gates are green;
- independent ARB is approved.

## 4. Risk and waiver register

### Open observation — repository-resolvable BKL-030 EAGLE history

The prior ARB observation remains open. F3-A does not onboard BKL-030 signal history. Any future onboarding requires bounded, accepted, repository-resolvable evidence preserving upstream identity, timestamps, quality, source and provenance.

Disposition: **non-blocking for F3-A; mandatory gate for future EAGLE-history onboarding**.

### TD-012

BKL-040 F1/F2 compatibility debt remains accepted and unchanged. F3-A does not retrofit replay identity semantics or fabricate `source_event_id`.

### PR description baseline prose

The PR body still contains the original F2-A baseline SHA, while GitHub base/head metadata and the ARB evidence reflect the synchronized current base `92cec8ab...`. This is presentation staleness only and does not alter the branch contents or merge authority.

Disposition: **Observation; non-blocking**.

### Waivers

None.

## 5. Safety and authority statement

F3-A cannot operate observatory hardware or software. It introduces no device command, service restart, power action, network change, remediation path or present-time Safety inference.

Local physical interlocks remain independent and authoritative.

## 6. Release recommendation

**READY FOR MERGE.**

Merge is authorized only if:

1. final exact-head CI is green after this Release Quality artifact is committed;
2. PR #122 remains mergeable and unchanged in scope;
3. merge uses expected-head protection;
4. post-merge applicable workflows succeed on the real merge SHA.

This decision does not authorize F3-B implementation by implication.