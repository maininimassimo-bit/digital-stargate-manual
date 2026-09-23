# AP-015 — Scientific Knowledge Platform Architecture

| Campo | Valore |
|---|---|
| Identificativo | `AP-015` |
| Capability | `CAP-40 — Scientific Knowledge Layer` |
| Stato | CLOSED / ACCEPTED / POST-MERGE VERIFIED |
| Versione | 1.0 |
| Data | 23/09/2026 |
| Autorità | DSG-AEM-001 v1.2; AMP-002 |
| Owner | Massimo Mainini |

## Scopo e limite

Definire il modello semantico minimo per collegare osservazioni, sessioni, asset, strumenti, workflow, processing run, report, claim e citation senza sostituire le fonti autorevoli. Il package chiude il design contract di CAP-40; non seleziona graph database, document store, vector database, RAG, provider, modello AI o API runtime.

## Autorità

| Dominio | Fonte autorevole | Ruolo SKL |
|---|---|---|
| File binari scientifici | storage scientifico esterno | riferimento tramite locator, mai copia obbligatoria |
| Asset, manifest e provenance | Scientific Catalog / AP-013/AP-014 | riferimento canonico |
| Data product analitici | Warehouse / AP-011 | riferimento per misure curate |
| Architettura e report | repository GitHub | authority documentale |
| Relazioni e proiezioni | SKL | projection governata, non source authority |

## Modello minimo

- `KnowledgeEntity`: identità stabile, tipo, stato lifecycle, source authority e citation;
- `KnowledgeRelation`: relazione tipizzata, direzionale, versionata e con evidence locator;
- `ScientificClaim`: claim o inference esplicita, producer/method, citations e confidence contract;
- `CitationLocator`: path/URI, digest opzionale, locator secondario e authority;
- `ProvenanceChain`: input/output, metodo, producer e citazioni;
- `KnowledgeConflict`: assertions incompatibili mantenute senza risoluzione automatica;
- `Unknown`: dato mancante o non verificabile, mai trasformato in certezza.

Schema e fixture bounded: `schemas/ap015-knowledge-semantic-contract.schema.json` e `docs/data/ap015-knowledge-semantic-fixture.json`.

## Query target governate

1. risalire da un prodotto a sessione, asset, processing run e citation;
2. trovare claim con provenance incompleta o conflitto aperto;
3. confrontare target, sessione, setup e condizioni senza calcolare readiness;
4. produrre un elenco di evidence citabile per un consumer read-only.

Le query sono descrittive e non producono comando, remediation, ranking operativo, go/no-go o Safety Authority.

## Acceptance e rollback

Il contract è validato da `.github/scripts/verify-ap015-semantic-contract.mjs` con fixture sintetica, boundary assertions e locator repository-relative. Il rollback è un revert dei soli artefatti AP-015; nessuna migrazione o modifica a fonti runtime è prevista.
