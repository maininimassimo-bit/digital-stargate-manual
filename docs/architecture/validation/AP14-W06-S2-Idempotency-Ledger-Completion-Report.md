# AP14-W06-S2 — Idempotency Ledger Completion Report

| Campo | Valore |
|---|---|
| Identificativo | DSG-AP14-W06-S2-CLR-001 |
| Versione | 1.0 |
| Stato | Accepted |
| Data chiusura | 05/08/2026 |
| Architecture Package | AP-014 — Scientific Observation Catalog and Search |
| Work Package | AP14-W06 — PixInsight Synchronization Adapter |
| Slice | W06-S2 — Idempotency Ledger and Duplicate Handling |

## 1. Scopo

Registrare la chiusura tecnica e verificabile della slice W06-S2, dedicata a idempotenza, duplicate handling, conflict handling e audit trail del PixInsight Synchronization Adapter.

La chiusura di W06-S2 non chiude AP14-W06: restano da completare W06-S3, W06-S4 e W06-S5.

## 2. Outcome consegnati

- `PixInsightSynchronizationLedger` append-only;
- validazione preventiva tramite il contratto W06-S1;
- digest canonico SHA-256 e idempotency key deterministica;
- esito `accepted` per il primo manifest valido;
- esito `duplicate-noop` per retry identici senza append di nuovi record;
- esito `conflict` per stesso `manifestId` con payload differente;
- esito `rejected` per manifest non conformi;
- lookup per `manifestId` e `idempotencyKey`;
- audit trail append-only per ogni tentativo;
- risoluzione governata dei conflitti senza sovrascrittura del record autorevole;
- prevenzione della doppia risoluzione dello stesso conflitto.

## 3. Boundary di autorità

Il ledger non:

- modifica asset, checksum o provenance governati da AP-013;
- promuove automaticamente prodotti o processing run a `accepted`;
- sostituisce il Scientific Asset Registry;
- interpreta un manifest PixInsight come prova autorevole;
- consente la promozione del payload candidato durante la conflict resolution.

Le sole decisioni di risoluzione ammesse sono:

- `retain-authoritative`;
- `reject-candidate`.

## 4. Evidenze implementative

| Evidenza | Percorso |
|---|---|
| Manifest validator e digest | `.github/scripts/pixinsight-manifest.mjs` |
| Synchronization ledger | `.github/scripts/pixinsight-ledger.mjs` |
| Test manifest | `.github/scripts/test-pixinsight-manifest.mjs` |
| Test ledger | `.github/scripts/test-pixinsight-ledger.mjs` |
| Quality gate | `.github/workflows/developer-foundation.yml` |
| Solution baseline | `docs/architecture/integration/AP14-W06-PixInsight-Synchronization-Adapter.md` |

## 5. Quality gate

La suite automatica verifica:

- accettazione del primo manifest valido;
- immutabilità dei record;
- retry identico come `duplicate-noop`;
- assenza di nuovi record per i duplicati;
- conflitto per payload divergente con stesso `manifestId`;
- conservazione del record autorevole originale;
- rifiuto dei manifest non validi;
- lookup per identificatori governati;
- audit ordinato di accepted, duplicate, conflict e rejected;
- risoluzione governata del conflitto;
- obbligatorietà di decisione supportata, motivazione e operatore;
- rifiuto della doppia risoluzione.

Le suite W06-S1 e W06-S2 sono eseguite dal workflow `Developer Foundation` nel job `quality-gate`.

## 6. Evidenza CI

Il commit di test `f879ca53d65e35f23be508889df2e66ec56c921c` ha completato con esito positivo:

- `quality-gate`;
- `Build MkDocs site`;
- `build-word`;
- `deploy`;
- `Deploy GitHub Pages`.

## 7. Rischi e debito residuo

Non sono ancora parte di W06-S2:

- persistence durevole del ledger;
- gestione concorrente multi-processo;
- retention e compaction governate;
- reconciliation read-only con AP-013 e AP-014;
- processing projection;
- metriche operative, dead-letter e runbook.

Questi elementi sono assegnati alle slice successive e non impediscono la chiusura di W06-S2.

## 8. Acceptance

I criteri della slice W06-S2 risultano soddisfatti:

- retry e duplicati non creano nuovi record autorevoli;
- payload divergenti non sovrascrivono il record accettato;
- ogni tentativo produce un evento di audit;
- la conflict resolution è append-only e governata;
- la copertura automatica è integrata nel quality gate.

W06-S2 è dichiarata **Completed / Accepted**.

## 9. Prossimo incremento

Il prossimo incremento dependency-ordered è **W06-S3 — Reconciliation read-only con AP-013/AP-014**, con classificazione `matched`, `partially-matched`, `unresolved` e `conflict` basata esclusivamente su lookup non mutativi.
