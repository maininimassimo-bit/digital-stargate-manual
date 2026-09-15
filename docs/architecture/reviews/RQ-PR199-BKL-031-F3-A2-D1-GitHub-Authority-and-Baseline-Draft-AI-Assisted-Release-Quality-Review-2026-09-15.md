# Release Quality PR #199 — BKL-031 F3-A2-D1 GitHub Authority and Baseline Draft

| Campo | Valore |
|---|---|
| Review ID | RQ-PR199-BKL031-F3A2-D1 |
| Data | 15/09/2026 |
| Role | Release Quality — process-separated AI-assisted reviewer |
| Independence limitation | Not equivalent to an independent human approval |
| PR | #199 |
| Base | `main@687f966fa544f7c4b31eaa29433cfa8ab48e52fe` |
| Technical head | `b595680a0dcc042bc2046e0fdc166ed0d075f97b` |
| ARB publication commit | `cc67f7699b5f0bbe4afcf80df3df99d266feda6e` |
| ARB | Approved with Conditions — 99/100 |
| Recommendation | **CONDITIONALLY READY FOR MERGE** |
| Runtime / EAGLE | None |

## 1. Release impact

This is a governance/documentation increment plus one protected DRAFT record. It determines the setup-authority system and roles, persists the mandatory stop-notification rule, updates governed roadmap/knowledge projections and prepares the first exact payload for later human approval.

It does not release an approved configuration, resolver, assignment, public dataset, API or runtime behavior. S09 remains `UNAVAILABLE_CURRENT`.

## 2. Quality-gate matrix

| Gate | Stato | Evidence |
|---|---|---|
| Scope and dependency readiness | Passed | F3-A2 accepted; owner authority/definition decisions recorded |
| Architecture/ADR | Passed | ADR-009; ARB PR #199 Approved with Conditions — 99/100 |
| Documentation and navigation | Passed | MkDocs nav and Project Governance Center updated |
| Build | Passed | Developer Foundation #1441 |
| Automated tests | Passed | 61 unit + 2 integration + 1 architecture; downstream governed tests passed |
| Formatting | Passed | `dotnet format --verify-no-changes` |
| Links/MkDocs | Passed | Validate documentation #1078 and Developer Foundation |
| Roadmap projections | Passed | canonical source plus generated roadmap/platform projections aligned |
| Knowledge graph | Passed | ADR coverage 100%; material relations passed after remediation |
| JSON parse and digest | Passed | JSON parse verified; independent SHA-256 recomputation matches exact payload |
| Security/privacy | Passed | private repository; registry outside `docs/`; no secrets, coordinates or serials |
| Safety | Passed | fail-closed; no command, readiness, go/no-go or Safety Authority |
| Observability | Not Applicable | no runtime component |
| Migration/OAT | Not Executed | explicitly out of scope for DRAFT; required before materialization |
| Rollback | Passed | repository revert; future retirement without fallback |
| Pages deployment | Not Applicable pre-merge | no protected registry input; post-merge Pages check required for documentation changes |
| Final publication-head CI | Blocked pending | must run after this RQ evidence commit |

## 3. Risk and waiver register

| ID | Risk / waiver | Stato | Control |
|---|---|---|---|
| RQ-199-R01 | DRAFT could be mistaken for approved authority | Controlled | lifecycle DRAFT, `eligibleForResolution=false`, no receipt, explicit docs |
| RQ-199-R02 | Projection facts could be treated as desired state by inference | Controlled | source authority retained; human exact-digest approval required |
| RQ-199-R03 | Protected data could enter Pages | Controlled | private repository; registry outside `docs_dir`; no public projection |
| RQ-199-R04 | Baseline approval could imply assignment | Controlled | separate lifecycles/receipts; S09 unavailable |
| W-DSG-AEM-RULESET-001 | No repository ruleset returned; branch-protection administration endpoint unavailable to the GitHub App | Active / conditioned | exact-head CI, zero-behind, no Blocker/Major, expected-head merge, rollback and post-merge verification |

## 4. Validation evidence

Exact technical-head workflows: **7/7 SUCCESS**.

- Developer Foundation run 34975120063 / #1441;
- Validate documentation run 34975119982 / #1078;
- Genera manuale Word run 34975119929 / #1504;
- Scientific Platform Governance run 34975120000 / #141;
- BKL-041 F4 Governance run 34975120125 / #143;
- BKL-046 F4 governance run 34975120054 / #117;
- BKL-046 F5 governance run 34975119949 / #102.

Not executed: approved-schema validation, adapter/runtime tests, OAT, physical inventory and Pages post-merge deployment. These are either explicitly outside this DRAFT package or mandatory later gates.

## 5. Readiness recommendation

**CONDITIONALLY READY FOR MERGE.**

Merge is allowed under `DSG-AEM-001` and `W-DSG-AEM-RULESET-001` only when the exact publication head containing ARB and this RQ report is:

- mergeable and zero commits behind `main`;
- green on every applicable workflow;
- unchanged in scope after review;
- free of unresolved Blocker/Major findings;
- merged with expected-head protection.

Post-merge workflow, Pages, projection and continuity verification remain mandatory. The merge does not approve `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`.
