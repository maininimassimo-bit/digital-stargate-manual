# AP-015 — Validation Plan

| Campo | Valore |
|---|---|
| Validation ID | `AP015-CAP40-VAL-001` |
| Stato | Accepted / Post-Merge Verified |
| Scope | Semantic contract and bounded repository fixture |
| Runtime | Not executed / not required |

## Gates

| Gate | Metodo | Criterio |
|---|---|---|
| Schema | JSON parse and structural inspection | version 1.0, authority projection |
| Fixture | `verify-ap015-semantic-contract.mjs` | 3 entities, 2 relations, citation/provenance/conflict/unknown present |
| Locator safety | repository-relative access check | no absolute path or traversal |
| Authority boundary | forbidden semantic markers and contract review | no command, remediation, provider, runtime or Safety Authority |
| Documentation | `mkdocs build --strict` | success |
| Governance | Developer Foundation, Pages, Word and projection workflows | success on exact merge SHA |

## Exclusions

No ingest, graph database, vector store, RAG, model/provider, runtime API, scheduler, command, readiness or physical observatory operation is part of this validation.
