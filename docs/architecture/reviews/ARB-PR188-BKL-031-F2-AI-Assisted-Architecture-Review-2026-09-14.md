# ARB — PR #188 BKL-031 F2 Machine-Readable Context Contract

| Field | Value |
|---|---|
| Review ID | ARB-PR188-BKL031-F2-AI-001 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-14 |
| Pull request | #188 |
| Exact head reviewed | `ec5fbcce854485e595b825ea74f9e9e7e91f9c1e` |
| Base | `f6c4b253a56406c930f009af0658b46a12bc088a` |
| Decision | **REWORK REQUIRED** |
| Score | **90 / 100** |

## 1. Independence and authorization disclosure

This review was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization scoped to PR #188 at exact head `ec5fbcce854485e595b825ea74f9e9e7e91f9c1e`.

It is AI-assisted and is **not equivalent to an independent human approval**. It does not authorize repair, merge, waiver, BKL-031 F3, provider integration, ranking or runtime activity. The reviewer did not modify the proposal while assessing it.

## 2. Reviewed scope and repository truth

- F2 JSON Schema and bounded M 27 fixture;
- normative structural/semantic/source validator and N01–N20 tests;
- Developer Foundation integration;
- F2 architecture, validation evidence and handoff reconciliation;
- backlog, canonical roadmap source, governed projections and MkDocs navigation;
- exact-head workflow evidence and branch/PR state.

Verified repository state:

- `main`: `f6c4b253a56406c930f009af0658b46a12bc088a`;
- PR #188: open, draft, mergeable, not merged;
- reviewed head: three commits ahead / zero behind, 13 changed files;
- no existing PR reviews or review threads;
- no repository ruleset protects `main` at review time;
- exact-head workflows: 7/7 SUCCESS;
- BKL-031 F2 implementation is authorized; review publication is authorized; merge and F3 are not.

## 3. Architecture alignment

The proposal correctly preserves the accepted F1 capability boundary:

- all eleven source identities are explicit;
- S07–S11 remain unavailable/current-unknown;
- the fixture is bounded to one candidate, one context and seven dimensions;
- authority remains `projection` with action and Safety authority `NONE`;
- no provider, external call, UI consumer, scheduler, device command or EAGLE computation is introduced;
- migration and rollback are repository-only;
- BKL-032 readiness and local physical Safety Authority remain separate.

The architecture direction is sound. The rework decision is caused by executable contract gaps: the current validator does not yet make all advertised source, traceability and prohibited-semantic rules fail closed.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 100 | exact F2 scope; later increments and BKL-032 remain separate |
| Source authority and ownership | 88 | S01–S11 states are preserved, but fact values are not bound to their cited source fields |
| Domain and semantic integrity | 86 | five objects are separated, but open fact semantics permit prohibited advisory/readiness payloads |
| Layer and dependency integrity | 100 | repository/CI only; no provider, portal runtime or EAGLE dependency |
| Safety | 88 | no command path exists, but operational semantics can be smuggled through allowed fact values |
| Security and privacy | 98 | public locator allowlist and raw-path rejection are present |
| Freshness, missingness and conflict | 96 | current/forecast separation is strong; coordinate conflict enforcement is incomplete |
| Contract integrity and fail-closed behavior | 72 | malformed structures can throw; several semantic misbindings validate successfully |
| Traceability and documentation | 94 | coverage and navigation are strong; executable Citation/Provenance binding is incomplete |
| Migration and rollback | 100 | additive repository change with revert-only rollback |
| Validation evidence | 78 | 7/7 CI and 21/21 tests are real, but exploratory negative cases expose untested gaps |

Rounded ARB score: **90 / 100**.

## 5. Findings

### Blocker

None.

### Major

**M-01 — The normative validator is not total for structurally invalid input.**

The validator throws uncaught `TypeError` for schema-invalid shapes instead of returning bounded validation errors. Reproduced examples:

- replacing `sources` with an object throws because `entries` is invoked on a non-array;
- deleting `sources[0].reason_codes` throws because `some` is invoked on `undefined`.

Because the package explicitly relies on this validator instead of a governed JSON Schema runtime, a crash is a contract gap rather than an acceptable secondary failure mode.

Required disposition:

1. make every structural path type-safe before iteration/property access;
2. return deterministic validation errors for arbitrary JSON values;
3. add malformed-root, wrong-container-type, missing-property and null-field regression cases;
4. verify schema/validator parity for the complete published surface.

**M-02 — Citation and Provenance are resolvable but not semantically bound to fact values.**

The following altered documents return zero validation errors:

- changing the published SQM median from `20.84` to `19.99` while retaining the original session Citation;
- changing the target-identity fact value to `dsg-target:ldn-1320` while the candidate remains M 27;
- changing `PRV-OP-M27-SQM-DIM.output_ref` to `DIM-OTHER`;
- changing a historical session fact value while retaining a Citation to a different session.

The validator proves that a cited row exists, but not that the published fact equals the cited field or that Provenance input/output/Citation sets bind to the exact object.

Required disposition:

1. define a closed mapping from every fixture fact type to source locator, record and field;
2. compare source-backed values and units deterministically;
3. bind every candidate, dimension, fact and explanation to exact Provenance output/input/Citation sets;
4. add mismatched-but-existing Citation and Provenance regressions.

**M-03 — Prohibited ranking/readiness semantics can enter through allowed fact fields.**

Changing an allowed identity fact to `semantic_type=READINESS` and `value=READY` returns zero errors. The prohibited-key scan checks field names, while `semantic_type` and scalar values remain open. This bypasses the F1 rule excluding score, ordering, readiness and operational conclusions.

Required disposition:

1. define a closed fact semantic vocabulary per evidence dimension;
2. restrict units, source classes and value domains per semantic type;
3. reject readiness, safety, authorization, score, threshold, normalization and ordering semantics across keys and values;
4. add semantic-smuggling regressions for every prohibited class.

**M-04 — N06 does not cover or enforce the full accepted coordinate conflict/authority rule.**

The N06 test proves only that an injected RA/Dec pair requires an epoch. It does not prove rejection of coordinates that conflict with governed S02/S04 evidence, and the validator does not bind coordinate facts to those accepted source classes or validate RA/Dec domains.

Required disposition:

1. reconcile coordinate values and epoch against eligible S02/S04 evidence;
2. reject wrong source class, out-of-domain coordinates and mismatched governed coordinates;
3. preserve `CONFLICTED`/`UNAVAILABLE` without silent selection;
4. extend N06 to cover both missing epoch and conflicting governed evidence.

### Minor

None beyond the Major findings.

### Observations

- O-01 — The bounded fixture itself is consistent with current repository evidence.
- O-02 — S07–S11 missingness is explicit and no synthetic provider data is present.
- O-03 — The F2-specific CI steps and all repository workflows succeed on the reviewed head.
- O-04 — No runtime, device, network, power, EAGLE or physical Safety behavior changes.
- O-05 — Absent `main` rulesets remain a merge-control risk; this review grants no waiver.

## 6. Executed validation evidence

Exact-head GitHub Actions on `ec5fbcce854485e595b825ea74f9e9e7e91f9c1e`:

- Developer Foundation #1385 — SUCCESS;
- Validate documentation #1022 — SUCCESS;
- Genera manuale Word #1448 — SUCCESS;
- Scientific Platform Governance #85 — SUCCESS;
- BKL-041 F4 Governance #87 — SUCCESS;
- BKL-046 F4 governance #61 — SUCCESS;
- BKL-046 F5 governance #46 — SUCCESS.

Within Developer Foundation:

- Verify Observation Planner F2 context contract — SUCCESS;
- Test Observation Planner F2 fail-closed rules — SUCCESS.

Independent exploratory mutations were executed against the reviewed validator and repository sources. Two malformed inputs threw `TypeError` and five semantically misbound/prohibited mutations returned an empty error set, providing the evidence for M-01 through M-04.

Not executed or claimed:

- provider/API, ephemeris, lunar or forecast validation;
- ranking effectiveness or target-order validation;
- PC Principale/EAGLE/runtime OAT;
- independent human review;
- repair, merge or post-merge validation.

## 7. Re-review criteria

ARB re-review is required after:

1. M-01 through M-04 are remediated without expanding F2 scope;
2. the schema, validator and tests remain mutually consistent;
3. all twenty transferred cases retain explicit traceability and the uncovered subcases are added;
4. the bounded fixture still preserves S07–S11 as unavailable/current-unknown;
5. exact-head Developer Foundation and documentation workflows succeed;
6. the remediated exact head receives a new explicit review authorization.

## 8. Decision

**REWORK REQUIRED.** PR #188 must not merge at reviewed head `ec5fbcce854485e595b825ea74f9e9e7e91f9c1e`.

The findings are remediable within BKL-031 F2 and do not require a new ADR, provider decision, runtime deployment or Safety change. Remediation is not authorized by this review.

