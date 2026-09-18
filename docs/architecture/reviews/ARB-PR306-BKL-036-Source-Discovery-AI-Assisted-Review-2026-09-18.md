# ARB PR #306 — BKL-036 Source Discovery and Semantic Contract

| Review target | PR #306, candidate head `d4b31785326e3bbc1872d3e446d3b56830463d42` |
|---|---|
| Scope | BKL-036 repository-only source discovery and semantic contract |
| Review mode | AI-assisted Architecture Review Board review; **not equivalent to independent human approval** |
| Disposition | **APPROVED WITH CONDITIONS FOR MERGE** |

## Review findings

| Dimension | Result | Evidence |
|---|---|---|
| Program and roadmap alignment | PASS | BKL-032 is preserved as closed; BKL-036 is the current governed package in backlog, baseline, enterprise context and knowledge map. |
| Boundary integrity | PASS | The package separates planner advisory output, readiness/go-no-go, scheduling, apparatus commands and the local Safety Authority. |
| Semantic/domain integrity | PASS | Evidence, dimensions and descriptive health status are defined separately from any aggregate score, recommendation or Safety State. |
| Layer and integration integrity | PASS | No adapter, live transport, runtime service, persistence path or device command is introduced. |
| Safety and authority | PASS WITH LIMITATION | Local physical interlocks remain authoritative; Safety Score, remediation and command authority are explicitly out of scope. |
| Security and privacy | PASS | No credentials, private coordinates, retained GRIB or external runtime traffic is introduced; provenance and retention are part of the contract. |
| Operability and observability | CONDITIONAL | Mandatory source domains, freshness, retention and comparability remain open discovery issues, as expected for this gate. |
| Migration and rollback | PASS | Documentation-only increment; revert of the package commit is sufficient rollback. |
| Traceability | PASS | ADR-014, architecture package, validation plan, source-discovery record, backlog, baseline, register, navigation and knowledge graph are linked. |
| Validation evidence | PASS | Exact-head CI is 14/14 green on the candidate commit; local knowledge-graph, coverage, material-relation, roadmap and whitespace checks pass. MkDocs was not available locally, while the CI documentation workflow passed. |

## Conditions for merge

1. Keep this increment limited to source discovery and semantic contract. Do not add a score, weights, thresholds, RAG bands, Safety Score, runtime transport, remediation or apparatus commands under PR #306.
2. Resolve the open source-mapping questions—mandatory domains, freshness and retention, missingness, comparability and authority—before any implementation increment.
3. Treat any future aggregate health score or live-source integration as a separately reviewed increment, with a new validation package and an explicit safety/authority review where applicable.
4. Preserve the distinction between descriptive health evidence and BKL-032 readiness/go-no-go. BKL-031, BKL-032 and local interlocks remain unchanged.
5. An independent human ARB decision remains required where the governance process calls for it; this AI-assisted review is supporting evidence only.

## Recommendation

The package is architecturally coherent for the proposed documentation gate and may proceed to expected-head merge once the normal human/governance approval path is satisfied. The next governed activity is source inventory and contract verification, not score implementation or runtime activation.
