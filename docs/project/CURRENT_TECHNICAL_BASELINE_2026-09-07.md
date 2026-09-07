# Digital StarGate — Current Technical Baseline — 2026-09-07

| Campo | Valore |
|---|---|
| Stato | Current |
| Repository authority | GitHub `main` |
| Baseline verificata | `b7c01ba7221818e1971403ab3befe38c8e40cc54` |
| Current governed package | BKL-035 Target Knowledge Base |
| BKL-044 | Done / Accepted — F1-F4 |
| BKL-015 | Done / Accepted |
| TD-008 | Resolved |
| Runtime EAGLE | unchanged |
| Safety Authority | local / outside Knowledge Graph and AI scope |

## 1. Accepted knowledge foundation

BKL-015 remains Done/Accepted and supplies repository-centric machine-readable traceability. BKL-044 is Done/Accepted and supplies the scientific/AI evidence semantic contract, deterministic validation, bounded reconciliation and consumer/read-model preservation rules.

F4 was merged via PR #104 as `b7c01ba7221818e1971403ab3befe38c8e40cc54`. Post-merge Developer Foundation #1004, Docs #613, Word #1038 and Pages #697 are SUCCESS.

## 2. Machine-readable evidence baseline

The accepted evidence contract remains `schemas/knowledge-ai-evidence-contract.schema.json` with governed dataset `docs/data/knowledge-ai-evidence-contract.json`. Semantic classes remain distinct: Observation, Evidence, Claim, Inference, Recommendation, Confidence, Citation, Provenance, Conflict and Unknown.

## 3. Reconciliation and consumer baseline

F3 bounded reconciliation remains limited to the governed seed/source set and is not broad-ingestion authorization. F4 adds `schemas/knowledge-ai-read-model.schema.json`, `docs/data/knowledge-ai-read-model.json` and deterministic validator/tests preserving semantic type, lifecycle, source authority, Citation, Provenance, Confidence and AI-derived markers.

## 4. Current package — BKL-035

**BKL-035 Target Knowledge Base** is the current governed package.

Target state: a target-centric projection/read model linking governed astronomical target identity to available session, SQM, setup, image and processing provenance, while preserving the authority of each source.

BKL-035 must not manufacture missing lineage, infer certainty from unknown data, promote derived content to repository authority, or authorize broad ingestion merely because a source is technically accessible.

## 5. First increment

The next dependency-ordered increment is **BKL-035 F1 — Target Knowledge Base Source Discovery & Semantic Contract**.

F1 must:

- inventory existing governed target/session/SQM/setup/image/processing sources;
- define canonical target identity and alias rules without duplicating source authority;
- define relation semantics and observation/derived boundaries;
- define provenance and citation requirements;
- define bounded seed and fail-closed acceptance criteria;
- identify unknowns/conflicts explicitly;
- remain repository-only unless a later package separately governs runtime impact.

## 6. Runtime, security and safety invariants

No BKL-035 F1 runtime change is authorized. No command endpoint, remediation, graph/vector persistence, RAG runtime, AI provider, inference engine or Safety Authority coupling is authorized by this baseline. Existing EAGLE/session automation and local interlocks remain unchanged.

## 7. Scientific/runtime invariants

Existing scientific transport, AP-013C cleanup exclusions, EAGLE Health read-only rules and session automation branch discipline remain unchanged. Runtime EAGLE must operate from `main`, not a feature/governance worktree.