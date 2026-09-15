# BKL-031 F3-A1-M2 — Site Authority Draft Materialization

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-M2-DRAFT-001 |
| Stato | **REVIEW CANDIDATE / OWNER DIGEST APPROVAL PENDING** |
| Data | 15/09/2026 |
| Baseline | `main@bb11f25192200655427411a46a2e18560a5d9bec` |
| Public protected values | None |
| Runtime / EAGLE | None |

## 1. Decision

The F3-A1-M1 owner-decision gate is complete. The owner selected the protected GitHub registry and authority roles, supplied the exact source facts, fixed orthometric elevation semantics and validation range, selected an internal identity policy, chose unbounded half-open validity from the recorded decision and authorized only municipality-level public generalization.

F3-A1-M2 may therefore enter review as a protected `DRAFT`. This record does not constitute exact-digest lifecycle approval and cannot make S08 available.

## 2. Materialized capability

- protected Site Authority registry outside Pages;
- owner source-decision evidence distinct from lifecycle approval;
- governed record and future approval-receipt schemas;
- deterministic canonicalizer and internal payload digest;
- fail-closed lifecycle, semantics and interval resolver;
- executable 51-case validation suite;
- public allowlist, independent digest boundary and full `docs/` protected-literal scan;
- dedicated pull-request and `main` workflow.

## 3. Boundary

- no protected value is reproduced in public documentation, PR narrative, review narrative or workflow output;
- no current site authority resolves while the lifecycle is DRAFT;
- no `CurrentSetupAssignment` is created or implied;
- S08 remains `UNAVAILABLE`; S09 remains `UNAVAILABLE_CURRENT`;
- no provider, ephemeris computation, ranking, readiness, command, EAGLE activity or Safety Authority is introduced.

## 4. Next decision

After DRAFT integration and post-merge verification, the exact canonical payload digest will be presented to the human Approval Authority through the owner-controlled channel. Only an explicit approval of that digest and validity can authorize the M3/M4 approval receipt and lifecycle promotion.

## 5. Rollback

Revert the DRAFT package through reviewed Git history. The prior state is no protected site record and S08 `UNAVAILABLE`. No runtime, migration, credential, device or observatory rollback is required.
