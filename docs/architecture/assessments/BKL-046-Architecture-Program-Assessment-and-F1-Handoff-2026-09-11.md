# BKL-046 — Architecture Program Assessment and F1 Handoff

| Campo | Valore |
|---|---|
| Package | BKL-046 — AI Post-Processing Assistant for PixInsight |
| Stato | Accepted — F1 handoff completed |
| Data | 11/09/2026 |
| Baseline verificata | `main` @ `249a90265b9cd2323df6e1dfb0ab09c5c64f5f1b` |
| Predecessore | BKL-041 — CLOSED / ACCEPTED / POST-MERGE VERIFIED |
| Dipendenze | BKL-015, BKL-044, BKL-045 — accepted repository baselines |
| Incremento selezionato | BKL-046 F1 — Source Discovery and Advisory Semantic Contract |
| Specialist handoff | Enterprise Architect / Solution Architect after F1 acceptance |

## 1. Decisione di programma

BKL-046 è dependency-ready per iniziare la definizione architetturale. Non è pronto per implementazione o uso operativo: il repository non contiene ancora un contratto specifico di recommendation post-processing, un adapter di inferenza, un modello/provider selezionato, una evaluation scientifica o un percorso autorizzato di applicazione PixInsight.

Il prossimo incremento è quindi F1, limitato a source discovery, ubiquitous language, authority boundary e roadmap incrementale. Il risultato atteso è un contratto semantico reviewable che impedisca di confondere recommendation, decisione umana ed execution evidence.

## 2. Baseline verificata

| Fondazione | Stato verificato | Utilizzo consentito in BKL-046 |
|---|---|---|
| BKL-015 repository/knowledge foundation | Accepted | stable identity, repository citation e document governance |
| BKL-044 Knowledge/AI Evidence Contract | Closed / Accepted | `recommendation`, Citation, Provenance, Confidence, conflict e unknown semantics |
| BKL-045 PixInsight provenance | Closed / Accepted con limitation | provenance `OBSERVED`/`DECLARED`, read model e `SUGGESTED` boundary |
| ADR-008 hybrid provenance strategy | decisione applicata da BKL-045 | PixInsight evidence local-first e governed exporter boundary |
| BKL-041 Scientific Data Quality | Closed come experimental read-only | supporting context soltanto; mai ground truth o production signal |
| `AiRequestContext` / `AiResultReference` | Prepared foundation | correlation e result reference; non costituiscono recommendation contract |
| AI/runtime/model provider | Not selected / not implemented | nessun claim o vincolo tecnologico in F1 |

La limitation BKL-045 è determinante: la real OAT accettata ha `capture.completeness=UNAVAILABLE`. BKL-046 deve quindi poter produrre `unknown`/insufficient evidence senza ricostruire uno storico di processo e senza suggerire come se la provenance fosse completa.

## 3. Maturity assessment

| Dimensione | Score | Razionale |
|---|---:|---|
| Dependency readiness | 100 | tutte le dipendenze dichiarate sono accepted |
| Evidence/provenance foundation | 90 | contratti BKL-044/BKL-045 disponibili; real history completeness resta unavailable |
| Advisory semantic contract | 20 | boundary roadmap presente, contratto BKL-046 assente |
| Recommendation quality/evaluation | 0 | nessun metodo, benchmark o ground truth governati |
| AI runtime/provider architecture | 0 | non selezionati e non necessari per F1 |
| Human approval/apply boundary | 25 | principio approvato; workflow e contratto non ancora definiti |
| Security/privacy model | 30 | local-first stabilito; threat model specifico BKL-046 assente |
| Operability/observability | 10 | correlation foundation presente; SLI, audit ed error model assenti |

Gli score sono una valutazione di maturità architetturale, non soglie di acceptance o qualità scientifica.

## 4. Dependency-ordered increment roadmap

| Incremento | Scopo | Entry condition | Exit evidence |
|---|---|---|---|
| F1 | source discovery e advisory semantic contract | dipendenze accepted | inventory, authority model, semantics, risks, ARB/RQ |
| F2 | machine-readable recommendation contract | F1 accepted | schema chiuso, bounded fixtures, validator e negative tests |
| F3 | deterministic advisory demonstrator | F2 accepted | bounded generator, explicit method/version, explainability and regression tests |
| F4 | session/provenance-driven read-only consumer | F3 accepted | freshness-verified projection and accessible portal consumer |
| F5 | real-evidence advisory validation and closure | F4 accepted | real PixInsight evaluation, retained limitations, ARB/RQ and post-merge evidence |

La roadmap non seleziona un LLM, provider, RAG/vector store o modalità `ASSISTED APPLY`. Ogni scelta richiede evidence e decisione successiva; nessun incremento può saltare il boundary human-in-the-loop.

## 5. Prioritized package backlog

1. **P0 — semantic integrity:** Recommendation non è Observation, Evidence, decisione umana o execution evidence.
2. **P0 — fail-closed missingness:** provenance incompleta/stale/unknown impedisce claim specifiche non supportate.
3. **P0 — authority:** nessuna image mutation, PixInsight command, automatic acceptance o Safety Authority.
4. **P1 — provenance/citation:** ogni recommendation deve risolvere evidence, method e producer/version prima di `validated`.
5. **P1 — privacy/security:** local-first, no mandatory image upload, prompt/content isolation e no secrets/local paths in published artifacts.
6. **P1 — human approval:** user decision separata dalla recommendation; acceptance non prova execution.
7. **P2 — provider/runtime:** selezione differita fino a requisiti, privacy, costi, evaluation e rollback verificabili.
8. **P2 — assisted apply:** fuori scope iniziale; richiede checkpoint, preview, rollback e nuova architecture/safety review.

## 6. Specialist handoff brief

L'Enterprise Architect deve produrre BKL-046 F1 riusando BKL-044 e BKL-045, senza introdurre un ontology, provenance store o ingestion path paralleli. Il Solution Architect potrà intervenire solo dopo F1 per trasformare le semantiche accettate in contratti implementabili.

Required inputs:

- functional objective in `FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md`;
- accepted BKL-044 semantic contract;
- accepted BKL-045 provenance/consumer boundary and retained limitation;
- ADR-008 local-first hybrid capture decision;
- BKL-041 closure and non-production limitation;
- existing `AiRequestContext` and `AiResultReference` foundation.

Required F1 outputs:

- verified source inventory and eligibility rules;
- recommendation/advice/human-decision/execution semantics;
- authority, privacy, security, safety and observability boundaries;
- migration path and increment roadmap;
- acceptance criteria and open issues;
- repository traceability and navigation.

## 7. Risks and decisions

| ID | Rischio | Trattamento F1 |
|---|---|---|
| BKL046-R01 | AI hallucination presented as processing fact | recommendation semantic type, citations, lifecycle and explicit unknown |
| BKL046-R02 | incomplete PixInsight history inferred as complete | BKL-045 completeness preserved fail-closed |
| BKL046-R03 | BKL-041 score used as ground truth | supporting-context-only rule and production-state preservation |
| BKL046-R04 | parameter advice causes destructive processing | advisory only, no apply path, ranges only with governed method/evidence |
| BKL046-R05 | external processing leaks image data or local paths | local-first default and future explicit privacy decision |
| BKL046-R06 | prompt/content injection changes authority | repository evidence treated as data; no tool execution or source mutation |
| BKL046-R07 | user approval confused with executed provenance | separate decision receipt; execution requires new observed/declared evidence |

## 8. Quality gates

- F1 document and repository sources agree;
- no duplicate AI/provenance contract is introduced;
- BKL-045 lifecycle stale references are reconciled against its closure;
- roadmap, bootstrap, backlog, handover, knowledge map and navigation are coherent;
- links/Mermaid/documentation build pass;
- exact-head CI is green;
- independent ARB has no Blocker/Major;
- Release Quality is `READY FOR MERGE` before protected merge.

## 9. Completion status

Program assessment and F1 handoff: accepted. BKL-046 F1 was integrated via PR #165, merge `3f2e3edae93b009f5800a58a4ac5afc4f04e9bb7`, after ARB 99/100, Release Quality `READY FOR MERGE` and exact-head CI 7/7; live Pages and search were verified after merge. F2 is the next dependency-ordered increment.
