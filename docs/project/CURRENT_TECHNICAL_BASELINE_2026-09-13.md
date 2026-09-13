# Digital StarGate Current Technical Baseline — 13/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 13/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Current main baseline | `3d680dd3a05c70b2a4654c4187c293e36b0af4a7` |
| Current governed package | BKL-031 — Observation Planner intelligente |
| Current increment | F1 — Source Discovery and Semantic Boundary |
| Accepted predecessor | BKL-046, PR #181; post-merge and Pages verified |

## 1. BKL-046 accepted baseline

| Elemento | Valore |
|---|---|
| Canonical sessions / F4 records / F5 snapshot | 16 / 16 / 16 |
| Evaluation ID | `BKL046-F5C-4EC171591C20E469B6302B7E` |
| Schema / state | `2.0` / `F5C_CLOSURE_EVALUATED` |
| Technical outcome | `ACCEPTED_READ_ONLY_WITH_LIMITATIONS` |
| Closure recommendation | `CLOSE_DETERMINISTIC_CAPABILITY` |
| Scientific state | `NOT_EVALUABLE_CURRENT_EVIDENCE` |
| Production state | `NOT_READY_FOR_PRODUCTION` |
| AI model implemented | `false` |
| Main / merge SHA | `3d680dd3a05c70b2a4654c4187c293e36b0af4a7` |
| Post-merge | 7/7 workflow SUCCESS; Pages freshness verified |

La closure formale è `docs/project/BKL-046-CLOSURE-2026-09-13.md`. Le review ARB/RQ erano AI-assistite, owner-authorized e non equivalenti ad approvazioni umane indipendenti.

## 2. Retained BKL-046 limitations

- provenance eligible: 0;
- Human Decision Receipt: 0;
- execution evidence: 0;
- source processing non correlate: 2;
- nessun model/provider, confidence scientifica, automatic acceptance o PixInsight apply;
- nessuna production authority o Safety Authority.

## 3. BKL-031 current baseline

Dipendenze dichiarate disponibili: BKL-015 machine-readable knowledge foundation, BKL-035 Target Knowledge Base, BKL-029 meteo/SQM e storico sessioni. Restano da verificare le authority e i contratti concreti per geometria celeste, transito, Luna, forecast e identità setup.

L'incremento corrente produce soltanto inventario source e semantic boundary. Nessun motore di ranking o scheduling è implementato o autorizzato.

## 4. Quality and governance state

La closure BKL-046 ha superato 85/85 test reviewer, exact-head CI, ARB/RQ AI-assistite autorizzate, merge owner-authorized e sette workflow post-merge. La branch protection non è configurata; la deroga `W-BKL046-F5C-MERGE-001` era una tantum ed è scaduta al merge.

BKL-031 deve ottenere evidence e gate propri; non eredita review, acceptance o deroghe da BKL-046.

## 5. Operational limitation

Il rerun manuale duplicato della stessa finestra EAGLE termina con `DEFERRED/PARTIAL` invece di `NOOP/ALREADY_PUBLISHED`. È un miglioramento operativo separato e non autorizza modifiche runtime in BKL-031.

## 6. Next gate

BKL-031 F1 architecture package: source authority inventory, semantic contract, missingness/freshness, explainability, security/privacy/safety boundary e validation plan. Fermarsi prima di implementazione e review.

