# Digital StarGate — Current Technical Baseline — 2026-09-07

| Campo | Valore |
|---|---|
| Stato | Current |
| Repository authority | GitHub `main` |
| Baseline di partenza verificata | `6b9db9b342144645da62381d6833ff1ebff3c22c` |
| Current governed package | BKL-044 Knowledge Graph / AI Evidence Contract |
| BKL-044 state | In Progress — F1 merged |
| BKL-015 | Done / Accepted |
| TD-008 | Resolved |
| Runtime EAGLE | unchanged |
| Safety Authority | local / outside Knowledge Graph and AI scope |

## 1. Current package

BKL-044 è il package corrente. F1 è integrato in `main` tramite PR #98 e merge `6b9db9b342144645da62381d6833ff1ebff3c22c`.

Contratto:

`docs/architecture/knowledge/BKL-044-Knowledge-Graph-AI-Evidence-Contract.md`

Review:

- `docs/architecture/reviews/ARB-BKL-044-F1-Independent-Review-2026-09-07.md`;
- `docs/architecture/reviews/RQ-BKL-044-F1-Release-Quality-Review-2026-09-07.md`.

F1 stabilisce il modello semantico e i boundary. F2 deve trasformare il contratto in schema machine-readable e validation fail-closed senza introdurre runtime AI o storage technology.

## 2. Repository Knowledge Graph foundation

BKL-015 rimane la foundation repository-centric accettata.

Projection:

`docs/data/knowledge-graph.json`

Schema:

`schemas/knowledge-graph-foundation.schema.json`

Validation:

- `.github/scripts/verify-knowledge-graph.mjs`;
- `.github/scripts/verify-knowledge-graph-coverage.mjs`;
- `.github/scripts/verify-knowledge-graph-material-relations.mjs`.

Il Knowledge Graph resta una projection non autorevole e ricostruibile dalle fonti repository.

## 3. BKL-044 F1 semantic boundary

Le classi introdotte dal contratto sono semanticamente distinte:

`Observation -> Evidence -> Claim -> Inference -> Recommendation`

con Confidence, Citation, Provenance, Conflict e Unknown come concetti trasversali governati.

Regole permanenti:

- una Observation non è automaticamente una Evidence;
- una Evidence non è automaticamente una Claim;
- una Inference non è un fatto autorevole;
- una Recommendation resta advisory;
- confidence non sostituisce evidence/provenance;
- missing/conflicting provenance non viene auto-risolta;
- nessun contenuto AI acquisisce authority per il solo fatto di essere nel graph.

## 4. Roadmap state

Authority:

`.github/roadmap/roadmap-source.json`

Projection:

`docs/data/roadmap.json`

BKL-044 è il current package/active package. BKL-015 è completato. TD-008 resta risolto.

## 5. Observatory runtime

Nessuna modifica BKL-044 F1 interessa:

- EAGLE runtime;
- N.I.N.A.;
- PHD2;
- CPWI;
- ASCOM;
- roof/safety interlock;
- telemetry producer;
- OneDrive scientific transport;
- cleanup policy.

Il repository operativo EAGLE deve restare su `main` per la session automation.

## 6. Scientific transport invariants

Restano validi:

- final authoritative storage `F:\Astrofotografia`;
- transfer mode `COPY_ONLY`;
- SHA-256 verification;
- ACK come prova di import verificato;
- cleanup produttivo C8 non autorizzato;
- `F:\Astrofotografia` non è cleanup target.

## 7. EAGLE Health invariants

BKL-030 resta Done/Accepted nel perimetro read-only telemetry/history/portal:

- nessuna remediation automatica;
- nessun command endpoint;
- severity policy non attivata implicitamente;
- Safety Authority fuori scope;
- cloud outage non sostituisce gli interlock locali.

## 8. Documentation authority

Per la continuità corrente usare:

1. `AI_BOOTSTRAP.md`;
2. `docs/project/HANDOVER_2026-09-07.md`;
3. questo documento;
4. `docs/project/BACKLOG.md`;
5. roadmap authority;
6. technical debt e decision log;
7. package/review/evidence direttamente applicabili.

`ENTERPRISE_ARCHITECTURE_CONTEXT.md` e `REPOSITORY_KNOWLEDGE_MAP.md` conservano valore storico/strutturale ma la loro baseline 04/08/2026 non deve prevalere sullo stato corrente.

## 9. Next governed increment

**BKL-044 F2 — Machine-readable schema and fail-closed validation.**

Acceptance minima attesa:

- schema versionato;
- identità stabile per gli oggetti semantici;
- required provenance/citation/evidence dove previsto;
- validation fail-closed per incompletezza materiale;
- confidence contract stabile/versionato;
- nessun graph/vector/RAG/runtime AI introdotto implicitamente;
- nessun impatto Safety Authority o runtime EAGLE.