# Digital StarGate — Current Technical Baseline — 2026-09-07

| Campo | Valore |
|---|---|
| Stato | Current |
| Repository authority | GitHub `main` |
| Baseline verificata | `ea36179882f05ce53581b80e5d5e8e70c560dcd9` |
| Current governed package | BKL-044 Knowledge Graph / AI Evidence Contract |
| BKL-044 state | In Progress — F1/F2 accepted; F3 next |
| BKL-015 | Done / Accepted |
| TD-008 | Resolved |
| Runtime EAGLE | unchanged |
| Safety Authority | local / outside Knowledge Graph and AI scope |

## 1. Current package

BKL-044 è il package corrente. F1 è integrato tramite PR #98. F2 è integrato tramite PR #100 e merge `ea36179882f05ce53581b80e5d5e8e70c560dcd9`.

Contratto:

`docs/architecture/knowledge/BKL-044-Knowledge-Graph-AI-Evidence-Contract.md`

F2 governance:

- `docs/architecture/reviews/ARB-BKL-044-F2-ReReview-2026-09-07.md` — APPROVED;
- `docs/architecture/reviews/RQ-BKL-044-F2-Release-Quality-Review-2026-09-07.md` — READY;
- `docs/project/BKL-044-F2-CLOSURE-2026-09-07.md` — closure record.

Post-merge sul commit F2: Developer Foundation #982, documentation #591, Word #1016 e Pages #693 risultano SUCCESS.

## 2. Repository Knowledge Graph foundation

BKL-015 rimane la foundation repository-centric accettata.

Projection:

`docs/data/knowledge-graph.json`

Schema foundation:

`schemas/knowledge-graph-foundation.schema.json`

Il Knowledge Graph resta una projection non autorevole e ricostruibile dalle fonti repository.

## 3. BKL-044 machine-readable evidence baseline

F2 aggiunge:

- `schemas/knowledge-ai-evidence-contract.schema.json`;
- `docs/data/knowledge-ai-evidence-contract.json`;
- `.github/scripts/verify-knowledge-ai-evidence-contract.mjs`;
- `.github/scripts/test-knowledge-ai-evidence-contract.mjs`;
- Developer Foundation gate.

Le classi restano semanticamente distinte:

`Observation -> Evidence -> Claim -> Inference -> Recommendation`

con Confidence, Citation, Provenance, Conflict e Unknown come concetti trasversali governati.

Regole permanenti:

- una Observation non è automaticamente Evidence;
- Evidence validata deve avere Citation/locator governato;
- Claim/Inference/Recommendation validati richiedono evidence, citation, provenance e method;
- AI-derived validato richiede inoltre producer version;
- confidence non sostituisce evidence/provenance e deve risolvere un contratto versionato;
- missing/conflicting provenance non viene auto-risolta;
- nessun contenuto AI acquisisce authority per il solo fatto di essere nel graph.

## 4. Roadmap state

Authority: `.github/roadmap/roadmap-source.json`.

Projection: `docs/data/roadmap.json`.

BKL-044 resta current/active e `In Progress`; F2 è chiuso ma BKL-044 non è Done. F3 è il prossimo incremento. BKL-015 resta completato e TD-008 resta risolto.

## 5. Observatory runtime

Nessuna modifica BKL-044 F1/F2 interessa EAGLE runtime, N.I.N.A., PHD2, CPWI, ASCOM, roof/safety interlock, telemetry producer, OneDrive scientific transport o cleanup policy. Il repository operativo EAGLE deve restare su `main` per la session automation.

## 6. Scientific transport invariants

Restano validi final authoritative storage `F:\Astrofotografia`, transfer mode `COPY_ONLY`, SHA-256 verification, ACK come prova di import verificato, cleanup produttivo C8 non autorizzato e `F:\Astrofotografia` escluso dai cleanup target.

## 7. EAGLE Health invariants

BKL-030 resta Done/Accepted nel perimetro read-only telemetry/history/portal: nessuna remediation automatica, nessun command endpoint, severity policy non attivata implicitamente, Safety Authority fuori scope e cloud outage non sostituisce gli interlock locali.

## 8. Documentation authority

Per la continuità corrente usare `AI_BOOTSTRAP.md`, handover 07/09/2026, questo documento, backlog, roadmap authority, technical debt/decision log e package/review/evidence direttamente applicabili. I documenti storici non prevalgono sul repository truth corrente.

## 9. Next governed increment

**BKL-044 F3 — Governed Seed Projection & Reconciliation.**

Acceptance minima attesa:

- seed bounded e governati, non broad ingestion;
- riconciliazione deterministica con fonti repository autorevoli selezionate;
- ogni seed conserva semantic type, lifecycle e source authority;
- Citation e Provenance F2 usate con riferimenti risolvibili;
- Confidence solo attraverso contract identity stabile/versionata;
- incomplete/conflicting source material resta esplicito e fail-closed;
- nessuna selezione graph/vector/RAG/runtime AI;
- nessun impatto Safety Authority o runtime EAGLE.