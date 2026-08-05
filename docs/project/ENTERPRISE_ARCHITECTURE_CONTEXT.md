# Digital StarGate Enterprise Architecture Context

| Campo | Valore |
|---|---|
| Identificativo | DSG-CTX-001 |
| Versione | 1.0 |
| Stato | Active context baseline |
| Data baseline | 04/08/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch autorevole | `main` |
| Baseline iniziale | `bcf8947049506eba08bd2b14f18fa99e06cded1d` |
| Release portale | Digital StarGate Enterprise Portal RC1 |
| Owner | Massimo Mainini |

## 1. Scopo

Questo documento è il punto di ingresso versionato per riprendere lo sviluppo di Digital StarGate in una nuova sessione di lavoro o in una nuova chat.

Riassume visione, principi, componenti, convenzioni, milestone e backlog. Non sostituisce Architecture Package, ADR, assessment, evidence, roadmap o release note: orienta il lavoro e indica quali fonti verificare prima di proporre modifiche.

### Regola di bootstrap

All'inizio di ogni nuova attività:

1. leggere questo documento;
2. verificare branch `main` e commit corrente;
3. confrontare il contesto con roadmap, Architecture Package, ADR, release note ed evidence più recenti;
4. segnalare eventuali divergenze prima di modificare il repository;
5. aggiornare questa baseline quando cambia una milestone, una regola stabile o un componente del portale.

## 2. Gerarchia delle fonti

Ordine di prevalenza:

1. Architecture Package, ADR, capability e standard approvati;
2. assessment ARB, validation record, evidence e gate;
3. `AMP-002 — Architecture Program Roadmap Realignment`;
4. release note e commit effettivamente pubblicati;
5. dataset JSON come proiezioni;
6. questo documento di contesto;
7. contenuto delle conversazioni.

Il repository GitHub è l'unica fonte autorevole. I dataset JSON devono essere ricostruibili e non possono modificare lo stato architetturale.

## 3. Visione del progetto

Digital StarGate è una piattaforma enterprise per documentare, governare ed evolvere l'osservatorio astronomico remoto di Manciano.

Il progetto è evoluto da manuale tecnico MkDocs a Enterprise Documentation Portal con centri tematici, componenti dinamici, intelligence di repository e piattaforma scientifica integrata.

Obiettivi permanenti:

- documentazione come codice;
- architettura modulare, tracciabile e revisionabile;
- separazione tra Presentation, Application, Domain e Infrastructure;
- safety, security e observability by design;
- lineage e provenance dei dati scientifici;
- evoluzione incrementale senza regressioni;
- futuro supporto multi-osservatorio senza duplicare logica di dominio.

Il portale è un presentation boundary. Non sostituisce gli interblocchi locali, non possiede autorità safety e non deve accedere direttamente agli apparati fisici.

## 4. Principi architetturali

1. **Repository as source of truth**.
2. **Modularità e responsabilità singola**.
3. **Nessuna duplicazione di logica, dati o stili**.
4. **JavaScript e CSS separati per responsabilità o componente**.
5. **Dataset JSON come projection, mai come fonte primaria**.
6. **Scientific Data Engine come layer dati condiviso**.
7. **Consegna incrementale: architettura, mockup, implementazione, test, commit, push, verifica Pages**.
8. **No regressions** su navigazione, responsive layout, tema e Instant Navigation.
9. **Safety first**: nessun bypass di interlock o safe state.
10. **Traceability** tra roadmap, release, decisioni, evidence e commit.
11. **Idempotenza** dei componenti caricati con Instant Navigation.
12. **Progressive enhancement** per contenuti e navigazione.

## 5. Architettura del portale

### Presentation layer

Responsabilità:

- rendering, navigazione e interazione;
- accessibilità e responsive design;
- freshness, provenance, stato di caricamento, errore e degraded mode;
- composizione dei centri enterprise.

Non contiene logica safety o device-specific.

### Scientific Data Engine

Lo Scientific Data Engine è il layer dati condiviso della piattaforma scientifica.

API pubbliche:

```javascript
loadCatalog()
getSessions()
getSession()
getTargets()
getYears()
getKPIs()
filterSessions()
getKnowledgeGraph()
getLineage()
```

Regole:

- tutti i componenti scientifici devono usare queste API;
- nessun componente deve replicare caricamento o parsing del catalogo;
- caching, normalizzazione ed error handling appartengono allo Scientific Data Engine;
- il catalogo JSON resta una proiezione ricostruibile.

### Navigation Manager

`docs/javascripts/page-enhancements.js` gestisce Enterprise Navigation, menu, ricerca e drawer documentale.

La gestione del tema non appartiene a questo componente. RC1-HF01 introdurrà un Theme Manager indipendente.

## 6. Componenti sviluppati nella RC1

| Componente | Responsabilità |
|---|---|
| Home Enterprise | ingresso principale del portale |
| Enterprise Navigation | navigazione globale, mega-menu, ricerca e drawer |
| Documentation Center | catalogo visuale del patrimonio documentale |
| Roadmap Center | proiezione dinamica di roadmap e milestone |
| Architecture Center | accesso ad AP, ADR, assessment e validation |
| Scientific Platform | accesso al patrimonio scientifico e ad AP-013 |
| Scientific Session Catalog | ricerca e filtro delle sessioni |
| Scientific Session Detail | dettaglio della singola sessione |
| Scientific Data Engine | accesso condiviso ai dati scientifici |
| Mission Control | dashboard enterprise di sintesi |
| Repository Intelligence | lettura strutturata del repository |
| Scientific Intelligence | knowledge graph, lineage e relazioni scientifiche |

Componenti JavaScript verificati nella baseline RC1:

- `homepage-effects.js`;
- `latest-observation.js`;
- `mission-control.js`;
- `nav-scroll.js`;
- `page-enhancements.js`;
- `roadmap.js`;
- `scientific-data-engine.js`;
- `scientific-session-detail.js`;
- `scientific-session-explorer.js`.

## 7. Convenzioni UI/UX

- design enterprise coerente tra tutti i centri;
- gerarchia tipografica chiara;
- pattern riusabili per hero, KPI, card, sezioni e call-to-action;
- stati active, loading, empty, error e degraded espliciti;
- HTML semantico, focus visibile e navigazione da tastiera;
- nessuna informazione affidata esclusivamente al colore;
- light e dark mode verificate per ogni nuova vista;
- desktop e tablet supportati; mobile governato come evoluzione dedicata;
- testo dei controlli coerente con l'azione disponibile.

## 8. Standard JavaScript

1. Un file per responsabilità o componente.
2. Nessuna nuova logica tema in `page-enhancements.js`.
3. Nessun accesso diretto ai dataset scientifici fuori dallo Scientific Data Engine.
4. Stato locale incapsulato e funzioni con nomi espliciti.
5. Nessuna variabile globale salvo API intenzionali e documentate.
6. Inizializzazione idempotente su `DOMContentLoaded` e `document$.subscribe(...)`.
7. Event delegation quando riduce duplicazioni e coupling.
8. Selettori basati su contratti `data-dsg-*`, non sulla posizione accidentale nel DOM.
9. Errori, assenza dati e caricamenti falliti gestiti esplicitamente.
10. Eventi custom `dsg:*` ammessi per comunicazione disaccoppiata.
11. Evitare nuova logica inline nelle pagine.
12. Compatibilità con Material for MkDocs e Instant Navigation obbligatoria.

## 9. Standard CSS

1. CSS condiviso in `docs/styles`.
2. Un file per componente complesso o dominio visuale.
3. Classi con prefisso `dsg-`.
4. Nessuna dipendenza da selettori fragili interni a Material.
5. Variabili CSS e design token preferiti a valori duplicati.
6. Responsive rules nel componente responsabile.
7. Light e dark mode senza duplicazioni incontrollate.
8. Nessuna regola generica che alteri componenti non correlati.
9. Stati `is-active`, `is-open`, `is-loading`, `is-empty`, `is-error`, `is-degraded` usati coerentemente.
10. Nuovi pattern condivisi consolidati prima di essere replicati.

## 10. Roadmap sintetica

La roadmap autorevole è `AMP-002`. Il Roadmap Center e `docs/data/roadmap.json` ne sono proiezioni.

| Wave | Stato sintetico al 04/08/2026 |
|---|---|
| AP-001–AP-006 Foundation | completata con condizioni ARB aperte |
| AP-007 Operations | package prodotto; review indipendente non registrata |
| AP-008 Integration | package prodotto; review indipendente non registrata |
| AP-009 Infrastructure | completato con condizioni; runtime non certificato |
| AP-010 Safety | completato con condizioni; safety runtime non certificata |
| AP-011 Analytics Platform | completato con condizioni |
| AP-012 Operations Center | completato con condizioni; acceptance residue aperte; comandi runtime proibiti |
| AP-013 Scientific Image Repository | attivo; COPY_ONLY limitato validato |
| AP-014 Observation Catalog and Search | pianificato |
| AP-015 Scientific Knowledge Platform | pianificato |

## 11. Stato milestone del portale

| Milestone | Stato |
|---|---|
| Enterprise Portal RC1 | pubblicata con commit `22d8e92f79e326585da12a5852a680766094c590` |
| GitHub Pages RC1 deployment | configurato con commit `bcf8947049506eba08bd2b14f18fa99e06cded1d` |
| RC1 Release Acceptance Review | completata con difetto tema aperto |
| RC1-HF01 Theme Manager | pianificata; implementazione non ancora eseguita |

## 12. Backlog prioritario

### P0 — RC1-HF01 Enterprise Theme Manager

Creare:

```text
docs/javascripts/dsg-theme-manager.js
```

Requisiti:

- unico responsabile del tema;
- Light/Dark con persistenza;
- compatibilità Material for MkDocs;
- compatibilità Instant Navigation;
- aggiornamento automatico del pulsante;
- estendibilità alla modalità System;
- rimozione della logica tema da `page-enhancements.js`.

### P1 — Consolidamento RC1

- `mkdocs build --strict` dopo ogni modifica;
- test light/dark, refresh diretto e Instant Navigation;
- verifica desktop, tablet e breakpoint principali;
- controllo link, pagine orfane e duplicazioni;
- checklist riusabile di Release Acceptance Review.

### P2 — Evoluzione piattaforma

- evidence dell'esecuzione unattended COPY_ONLY per AP-013;
- completamento acceptance residue AP-012;
- preparazione AP-014;
- consolidamento knowledge graph e lineage verso AP-015;
- futura modalità tema `system`;
- riduzione progressiva di script inline e dipendenze dal DOM interno di Material.

## 13. Processo di sviluppo

Per ogni milestone:

1. verificare repository, branch, commit e portale pubblicato;
2. individuare fonti e componenti coinvolti;
3. proporre l'architettura;
4. preparare il mockup quando necessario;
5. implementare con impatto minimo;
6. eseguire build e test applicabili;
7. verificare assenza di regressioni;
8. commit e push;
9. verificare workflow GitHub Pages e sito pubblicato;
10. aggiornare roadmap, release note, backlog e questo contesto quando necessario.

## 14. Definition of Done

Una modifica è completata solo quando:

- lo stato reale del repository è stato verificato;
- architettura e responsabilità restano coerenti;
- non è stata introdotta duplicazione;
- JavaScript e CSS rispettano gli standard;
- build e test applicabili sono documentati;
- Instant Navigation e due temi sono stati considerati;
- collegamenti e navigazione sono coerenti;
- commit e push sono effettivi;
- GitHub Pages è stato verificato;
- contesto e backlog sono aggiornati se lo stato è cambiato.

## 15. Riferimenti

- [Roadmap Center](../roadmap/index.md)
- [AMP-002](../architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md)
- [Digital StarGate Portal Vision](../architecture/digital-stargate-portal-vision.md)
- [Architecture Center](../architecture/index.md)
- [Documentation Center](../documentation/index.md)
- [Scientific Platform](../scientific-platform/index.md)
- [Platform Contracts](../developer/platform-contracts.md)
- [Portal Publication Guidelines](../developer/portal-publication-guidelines.md)

## 16. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima baseline enterprise allineata alla RC1 e al backlog RC1-HF01 |
