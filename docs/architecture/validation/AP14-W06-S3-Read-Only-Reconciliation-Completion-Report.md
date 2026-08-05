# AP14-W06-S3 — Read-Only Reconciliation Completion Report

| Campo | Valore |
|---|---|
| Identificativo | DSG-AP14-W06-S3-CLR-001 |
| Versione | 1.0 |
| Stato | Accepted |
| Data chiusura | 06/08/2026 |
| Architecture Package | AP-014 — Scientific Observation Catalog and Search |
| Work Package | AP14-W06 — PixInsight Synchronization Adapter |
| Slice | W06-S3 — Read-Only Reconciliation with AP-013/AP-014 |

## 1. Scopo

Registrare la chiusura tecnica e verificabile della slice W06-S3, dedicata alla riconciliazione non mutativa dei manifest PixInsight con il catalogo osservativo AP-014 e con i riferimenti asset/provenance AP-013.

La chiusura di W06-S3 non chiude AP14-W06: restano da completare W06-S4 e W06-S5.

## 2. Outcome consegnati

- `PixInsightReconciliationService` read-only;
- lookup della sessione tramite `entityId` del catalogo AP-014;
- lookup degli input e output rispetto al registro asset AP-013 fornito al servizio;
- classificazione degli esiti `matched`, `partially-matched`, `unresolved` e `conflict`;
- rilevazione di riferimenti asset mancanti;
- rilevazione di conflitti autorevoli tramite `integrityState: CONFLICT`;
- risultato immutabile con dichiarazione esplicita delle autorità AP-013/AP-014;
- assenza di modifiche al manifest candidato e alle fonti autorevoli.

## 3. Boundary di autorità

La reconciliation:

- usa esclusivamente lookup in memoria su snapshot forniti dai registri autorevoli;
- non modifica il catalogo AP-014;
- non modifica asset, checksum, provenance o integrity state AP-013;
- non promuove automaticamente manifest, sessioni, processing run o prodotti;
- non risolve i conflitti sostituendo dati autorevoli;
- non produce effetti operativi sui sistemi dell'osservatorio.

## 4. Regole di classificazione

| Stato | Regola |
|---|---|
| `matched` | sessione e tutti i riferimenti input/output risultano correlati senza conflitti autorevoli |
| `partially-matched` | almeno una correlazione è valida, ma sessione o uno o più riferimenti risultano mancanti |
| `unresolved` | nessuna sessione è correlata e non sono presenti riferimenti asset utili |
| `conflict` | almeno un riferimento correlato è marcato in conflitto dalla fonte autorevole AP-013 |

La precedenza è: `unresolved` per candidato privo di correlazioni, quindi `conflict`, quindi `partially-matched`, infine `matched`.

## 5. Evidenze implementative

| Evidenza | Percorso |
|---|---|
| Reconciliation service | `.github/scripts/pixinsight-reconciliation.mjs` |
| Test reconciliation | `.github/scripts/test-pixinsight-reconciliation.mjs` |
| Manifest contract | `.github/scripts/pixinsight-manifest.mjs` |
| Idempotency ledger | `.github/scripts/pixinsight-ledger.mjs` |
| Quality gate | `.github/workflows/developer-foundation.yml` |
| AP14-W06 solution baseline | `docs/architecture/integration/AP14-W06-PixInsight-Synchronization-Adapter.md` |
| AP-014 catalog index | `docs/data/scientific-observation-index.json` |
| AP-013 contract baseline | `docs/architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model.md` |

## 6. Quality gate

La suite automatica verifica:

- classificazione `matched`;
- classificazione `partially-matched` per riferimenti mancanti;
- classificazione `unresolved` per candidati senza correlazioni;
- classificazione `conflict` per conflitti dichiarati dalla fonte autorevole;
- immutabilità del risultato;
- assenza di mutazioni su catalogo, asset registry e manifest candidato;
- dichiarazione `mode: read-only` nel risultato.

Il workflow `Developer Foundation` esegue la suite con lo step `Test PixInsight Read-Only Reconciliation` nel job `quality-gate`.

## 7. Evidenza CI

Il commit di integrazione CI `0df61e66e246f3547ef1f0ebcaab6150f74d3095` ha completato con esito positivo:

- `quality-gate`;
- `Build MkDocs site`;
- `build-word`;
- `deploy`;
- `Deploy GitHub Pages`.

## 8. Rischi e debito residuo

Non sono ancora parte di W06-S3:

- adapter runtime verso un registro AP-013 persistente;
- gestione concorrente e snapshot consistency;
- processing projection derivata;
- eventi di proiezione e correlation ID end-to-end;
- metriche operative, dead-letter e runbook;
- persistence durevole del reconciliation outcome.

Questi elementi sono assegnati a W06-S4 e W06-S5 e non impediscono la chiusura di W06-S3.

## 9. Acceptance

I criteri della slice W06-S3 risultano soddisfatti:

- la reconciliation usa lookup esclusivamente read-only;
- gli stati `matched`, `partially-matched`, `unresolved` e `conflict` sono testati;
- AP-013 e AP-014 restano le fonti autorevoli;
- nessun payload candidato modifica le fonti;
- la copertura automatica è integrata nel quality gate.

W06-S3 è dichiarata **Completed / Accepted**.

## 10. Prossimo incremento

Il prossimo incremento dependency-ordered è **W06-S4 — Processing Projection & Audit Events**, con produzione di una proiezione derivata ricostruibile e di eventi informativi privi di autorità di acceptance.
