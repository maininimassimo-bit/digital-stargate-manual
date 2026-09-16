# ARB PR 213 — BKL-031 F3-A3 Google Cloud IaC AI-Assisted Review

| Field | Value |
|---|---|
| Review | ARB-PR213-BKL-031-F3-A3-GCP-001 |
| Date | 2026-09-16 |
| Pull request | #213 |
| Exact reviewed head | `6a21abcaa012ca6c6043451b485150325a16e6d3` |
| Scope | Partial owner decision, Terraform/WIF scaffolding and validation-only CI |
| Decision | **APPROVED WITH CONDITIONS — 96/100** |
| Independence note | AI-assisted process-separated review; not equivalent to independent human approval |

## Repository truth verified

- ADR-010 remains Proposed and explicitly leaves F3-OD05 open.
- S10 remains `UNAVAILABLE`.
- No GCP authentication, plan, apply, artifact acquisition or execution is claimed.
- The existing EAGLE/N.I.N.A. and telemetry boundaries are unchanged.
- Exact-head CI completed 7/7 successful workflows.
- Both Terraform roots passed `fmt -check`, `init -backend=false` and `validate`.
- Static policy passed for no public principal, no static credential, digest pinning, approved region/resources, zero retries and no Cloud NAT.

## Architecture scorecard

| Dimension | Score | Evidence |
|---|---:|---|
| governing ADR/capability consistency | 98 | partial owner decision is explicit; F3-OD05 blocks progression |
| domain and layer integrity | 98 | infrastructure remains outside source-neutral Domain/Application contracts |
| safety boundary | 100 | no device command, readiness, EAGLE or Safety Authority dependency |
| security and privacy | 96 | repository/ref-scoped WIF, separate identities, private buckets, no-NAT local profile |
| operability and cost control | 91 | bounded Cloud Run Job and no idle VM; bootstrap-state recovery needs strengthening |
| traceability | 97 | ADR, owner record, infrastructure plan, validation plan, backlog and navigation aligned |
| migration and rollback | 94 | phased bootstrap/platform path and deletion protection; bootstrap state migration pending |
| validation evidence | 96 | exact-head Terraform and repository workflows pass; cloud/scientific execution correctly not executed |
| **Overall** | **96** | **Approved with pre-apply conditions** |

## Findings

### Blocker

None.

### Major

None.

### Minor

| ID | Finding | Required remediation | Re-review gate |
|---|---|---|---|
| ARB-213-MI01 | The Terraform job encodes core capacity limits, but concurrency, IERS refresh policy and scientific thresholds are not yet an immutable container/method-profile input. | Before authenticated plan/apply, add a content-addressed method-profile artifact or explicit immutable configuration carrying every approved F3-OD06/F3-OD07/F3-OD10 value. | Static validation proves the exact profile digest and the container rejects drift. |
| ARB-213-MI02 | The bootstrap creates a remote state bucket but its own initial state is local. | Before a second operator or automated change, migrate bootstrap state to the protected bucket and document state recovery/locking procedure. | Reviewed backend migration evidence and recovery drill/checklist. |

### Observation

- No Cloud NAT intentionally prevents Horizons access from the local job. A remote-reference campaign requires a separate reviewed profile.
- Project-level deployer roles are acceptable for bootstrap/platform creation but should be re-evaluated after first apply for steady-state reduction.
- Scientific accuracy, cost and cold-start behavior remain unexecuted and cannot be inferred from Terraform validation.

## Decision

Approved with Conditions for repository integration only. This decision does not authorize GCP bootstrap/apply, artifact acquisition, Cloud Run execution, Horizons use or runtime integration.

## Re-review criteria

Re-review is required before cloud mutation. It must include:

1. closed F3-OD05 with exact SPK identity, coverage, provenance/notices and SHA-256;
2. immutable full method-profile evidence satisfying ARB-213-MI01;
3. bootstrap-state migration/recovery evidence satisfying ARB-213-MI02;
4. authenticated Terraform plan on the exact reviewed head;
5. unchanged safety/privacy boundaries.
