# BKL-031 F3-A2-D4 — CurrentSetupAssignment DRAFT Materialization Handoff

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D4-PROGRAM-001 |
| Stato | **AUTHORIZED HANDOFF AFTER D3 INTEGRATION — NOT MATERIALIZED** |
| Data | 15/09/2026 |
| Baseline | `main@d5f403bbe6a39731213c372cb22296324d10b03d` |
| Predecessor | F3-A2-D3 owner decisions complete; protected evidence pending integration |
| Specialist role | Digital StarGate Solution Architect |
| Runtime / EAGLE | None |

## 1. Program decision

F3-A2-D4 is the dependency-ordered successor to the F3-A2-D3 decision-evidence package. Work may begin only after D3 merge and post-merge verification. Scope is a protected, resolver-ineligible DRAFT materialization; it is not lifecycle approval and not runtime integration.

## 2. Required outputs

1. versioned closed schema for the assignment envelope and payload;
2. immutable DRAFT bound to the exact approved Site Authority revision and setup baseline version;
3. canonical JSON/SHA-256 implementation consistent with ADR-009;
4. validator for identity, roles, exact references, lifecycle and half-open validity;
5. positive, negative, conflict, privacy and mutation tests from the accepted F3-A2 validation plan;
6. generic workflow output that never prints protected content;
7. migration, retirement and reviewed Git-revert procedure;
8. public evidence that omits internal identifiers, digests and locators.

## 3. Dependency and implementation order

1. integrate and verify F3-A2-D3 decision evidence;
2. materialize schema and synthetic fixtures;
3. create the protected DRAFT with `eligibleForResolution=false`;
4. verify canonical identity and exact reference binding;
5. execute interval, conflict, authority and privacy cases;
6. integrate the DRAFT through exact-head review and post-merge verification;
7. present the exact assignment digest to the human Approval Authority in a later gate.

## 4. Acceptance criteria

- payload and envelope keys are closed and versioned;
- Site Authority and baseline references resolve to the already approved exact revisions;
- owner, custodian and Approval Authority match the D3 decision;
- validity start matches the approved baseline effective start; end mode is `UNBOUNDED`;
- DRAFT is never returned as current;
- gaps remain `UNAVAILABLE_CURRENT`; overlaps remain `CONFLICTED`;
- no latest-wins, projection, history, host, EAGLE or N.I.N.A. fallback;
- public/log output contains no protected references or exact site facts;
- approval receipt and `APPROVED` lifecycle are absent;
- no runtime or Safety Authority delta.

## 5. Risks and controls

| Rischio | Controllo |
|---|---|
| assignment inferred from two approved authorities | require separate DRAFT and later human receipt |
| reference drift | exact version/digest binding and mutation tests |
| overlap or latest-wins ambiguity | evaluate all approved interval candidates and fail closed |
| protected-data disclosure | deny-by-default publication and log leak tests |
| premature runtime claim | keep S08/S09 unavailable and adapter out of scope |

## 6. Quality gates

Exact-head CI, AI-assisted ARB and Release Quality review, no open Blocker/Major, expected-head merge and post-merge verification are mandatory under DSG-AEM-001. `ARB-204-MI02` remains a precondition for any later runtime adapter, not for this repository-only DRAFT.

## 7. Decision summary

**Decision:** prepare a protected DRAFT only after D3 integration.

**Not authorized:** assignment approval, approval receipt, runtime adapter, provider, forecast, ranking, readiness, command, EAGLE activity or Safety Authority change.
