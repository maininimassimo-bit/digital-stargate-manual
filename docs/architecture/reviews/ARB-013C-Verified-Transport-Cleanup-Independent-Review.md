# ARB-013C — Verified Transport Cleanup Independent Review

| Field | Value |
|---|---|
| Review ID | ARB-013C |
| Package | AP-013C — Verified Transport Cleanup and Convergence Monitoring |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Review date | 04/09/2026 |
| Review authority | Digital StarGate Architecture Review Board |
| Review basis | PR #86 head `43b56ec5171cde4e30b1dd6bc164e9510d8c2422` |
| Decision | **Approved with Conditions** |
| Dry-run decision | Approved to continue non-destructive validation |
| Productive cleanup | **Not approved** |

## 1. Executive decision

The Architecture Review Board independently reviewed AP-013C, DSDM-005, the ACK/evidence implementation, the dry-run evaluator, importer integration, failure-injection tests, GitHub Actions evidence, rollback boundary, program traceability and documentation navigation.

The architecture direction is sound: AP-013B `COPY_ONLY` remains the operational rollback, source RAW on `D:` remains immutable and outside cleanup scope, destination verification is SHA-256 based, ACK is tied to the exact READY manifest, and the initial evaluator is non-destructive with `Deleted=0` hard-coded.

The package is therefore **Approved with Conditions for architecture/dry-run continuation only**.

This review does **not** authorize productive deletion. C8 remains blocked until the conditions below are closed, a controlled real OAT is completed, retention/delete semantics are approved, and a re-review explicitly authorizes promotion.

## 2. Evidence reviewed

The Board verified:

- AP-013C architecture package;
- DSDM-005 solution design;
- AP-013C dry-run and failure-injection acceptance plan;
- `DSG.VerifiedTransportCleanup.psm1`;
- `Invoke-DSGVerifiedTransportCleanupDryRun.ps1`;
- C5 importer ACK integration;
- AP-013C Pester workflow and test suites;
- AP-013/AP-013B governing architecture and rollback boundary;
- `BACKLOG.md`, `roadmap-source.json`, `traceability-register.md`, `mkdocs.yml` and Release Playbook;
- PR #86 branch/base state.

Executed evidence on the reviewed head:

- `AP-013C Verified Transport Cleanup` workflow run #1: **success**;
- Pester 5.9.0: **20 passed, 0 failed, 0 skipped**;
- mandatory synthetic 445 READY / 426 ACK divergence: **19 blocked, Deleted=0**;
- reconvergence to 445/445: **445 technical candidates, Deleted=0**;
- `Validate documentation (no deploy)` #495: **success**;
- `Genera manuale Word` #919: **success**.

A real host-to-host OAT is not yet recorded as executed and is not inferred from synthetic CI.

## 3. Review scores

| Dimension | Score | Assessment |
|---|---:|---|
| Architecture consistency | 95/100 | Clean extension of AP-013/AP-013B; authority and storage boundaries preserved. |
| Domain/layer integrity | 95/100 | ACK producer, evidence reader and future cleanup controller responsibilities are separated. |
| Contract integrity | 91/100 | READY reuse and ACK binding are strong; eligibility semantics need one clarification before productive use. |
| Safety | 99/100 | No observatory Safety Authority change; local interlocks remain independent. |
| Security | 92/100 | Read-only evidence design, no secrets and no new privileged control path; productive principal/ACL review remains future work. |
| Operability | 88/100 | Dry-run evidence and rollback are strong; real OneDrive/OAT and restart/offline matrix are not yet complete. |
| Observability/auditability | 89/100 | JSON/CSV evidence is useful, but current enumeration cannot expose every orphan/inconsistent transport state. |
| Migration/rollback | 96/100 | AP-013B `COPY_ONLY` remains a simple and credible rollback. |
| Test/quality evidence | 94/100 | 20/20 CI tests including the incident-shaped failure injection; real OAT remains open. |
| Documentation/traceability | 72/100 | Backlog, roadmap, traceability register and MkDocs navigation are not yet reconciled with AP-013C execution. |

**Weighted overall score: 91.1/100**

## 4. Findings

### ARB-013C-C01 — Major — Transport inventory coverage is incomplete

The package and acceptance plan require inventory/classification of XISF, READY and ACK states, including cases such as XISF without READY and READY without XISF. The current dry-run runner enumerates only `*.ready.json` and then derives the ACK path.

Consequences:

- orphan XISF without READY is invisible to the evaluator;
- orphan ACK without READY is invisible;
- READY without transport payload can still reach a technical eligibility result if READY+ACK are mutually consistent;
- the evidence bundle does not yet satisfy the stated inventory contract.

**Required remediation before productive-cleanup design approval:** build a non-hydrating metadata inventory over XISF/READY/ACK, classify orphan/missing combinations explicitly, and add regression tests. The evaluator must not bulk-hash XISF on EAGLE merely to discover state.

### ARB-013C-C02 — Major — `CleanupEligible` currently conflates technical proof with policy authorization

The solution design states that retention is not approved and lists `RETENTION_NOT_APPROVED`, but `Test-DSGCleanupEvidence` returns:

```text
State = CLEANUP_ELIGIBLE_DRY_RUN
CleanupEligible = true
ReasonCode = ELIGIBLE_DRY_RUN
```

once READY/ACK hash evidence is valid.

This is safe in the current implementation because `Deleted=0`, but the boolean name can be misread by a future cleanup controller as authorization.

**Required remediation before C8:** either keep `CleanupEligible=false` until retention/promotion policy is approved, or split the model into an unambiguous pair such as `TechnicalCandidate=true` and `CleanupAuthorized=false`. Productive code must never infer authorization from the dry-run candidate flag.

### ARB-013C-C03 — Major — Real OAT remains unexecuted

The synthetic CI reproduces the incident shape and is accepted as C5/C6 test evidence, but the acceptance plan explicitly requires real OAT before promotion. No independent evidence reviewed here proves live PC/EAGLE OneDrive ACK reconvergence, host restart/offline behavior, F: temporary unavailability or repeated retries in the actual environment.

**Required remediation:** execute controlled non-destructive OAT with `Deleted=0`, preserve run evidence and re-review the result.

### ARB-013C-C04 — Major — Governance traceability is stale

`BACKLOG.md` still reports BKL-047 as `Ready` even though C1-C6 implementation/test work is active. `roadmap-source.json` is dated 2026-09-01, has no BKL-047 entry and still presents BKL-030 as the next milestone. `traceability-register.md` does not register AP-013C/DSDM-005/ARB-013C.

**Required remediation before merge/architecture package release:** reconcile backlog, roadmap source/projection and traceability register with the actual AP-013C state, preserving BKL-030 G6 dependency ordering.

### ARB-013C-C05 — Minor — MkDocs navigation does not expose the new governed artifacts

`mkdocs build --strict` succeeds, but the explicit navigation currently lists AP-013 and DSDM-001..004 and does not list AP-013C, DSDM-005, the AP-013C acceptance plan or this ARB review.

**Required remediation before package release:** add the governed artifacts to the appropriate Architecture / Scientific Image Repository / Validation & Review navigation sections and re-run strict documentation validation.

### ARB-013C-C06 — Minor — ACK schema status should be frozen explicitly

The package still says ACK names are subject to solution review while implementation already emits schema `1.0`. This is not a runtime defect, but contract maturity is ambiguous.

**Required remediation:** after C01/C02 resolution, mark ACK schema 1.0 as the accepted dry-run contract or version it if fields/semantics change.

### Observation — Safety and rollback boundaries are strong

No source cleanup, no productive transport cleanup and no Safety Authority modification were introduced. AP-013B COPY_ONLY remains independently usable.

## 5. Condition status

| Condition | Severity | Status | Blocks |
|---|---|---|---|
| ARB-013C-C01 inventory coverage | Major | Open | productive cleanup / full OAT acceptance |
| ARB-013C-C02 authorization semantics | Major | Open | productive cleanup |
| ARB-013C-C03 real OAT | Major | Open | C8 promotion |
| ARB-013C-C04 governance reconciliation | Major | Open | package release/merge readiness |
| ARB-013C-C05 MkDocs navigation | Minor | Open | documentation closure |
| ARB-013C-C06 ACK schema freeze | Minor | Open | contract closure |

## 6. Re-review criteria

ARB-013C may be re-reviewed when:

1. XISF/READY/ACK inventory coverage includes orphan/missing combinations without forcing bulk hydration;
2. dry-run technical candidacy is unmistakably separated from productive cleanup authorization;
3. controlled real OAT evidence exists with `Deleted=0` for nominal, delayed convergence, unavailable destination, restart and retry scenarios applicable to the environment;
4. BKL-047, roadmap source/projection, traceability register and MkDocs navigation are reconciled;
5. ACK schema status is frozen/versioned;
6. all applicable CI remains green.

A separate approval is required before any code capable of deleting transport XISF is introduced or enabled.

## 7. Final decision

**APPROVED WITH CONDITIONS — DRY-RUN / NO-DELETE ONLY**

Architecture and non-destructive validation may continue. AP-013B remains the production rollback/baseline. Productive cleanup remains **NO-GO** until all blocking conditions are closed and an explicit ARB re-review authorizes C8 promotion.
