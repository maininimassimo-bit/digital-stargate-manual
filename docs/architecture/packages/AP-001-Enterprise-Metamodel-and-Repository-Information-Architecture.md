# AP-001 — Enterprise Metamodel and Repository Information Architecture

| Campo | Valore |
|---|---|
| Identificativo | AP-001 |
| Titolo | Enterprise Metamodel and Repository Information Architecture |
| Tipo | Architecture Package |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Responsabile | Digital StarGate Enterprise Architect |
| Mandato | PAA-002, ARB-002, ABC-001 |
| Piano di riferimento | AMP-001, con incompletezza documentale registrata |
| Stato | Proposed for independent ARB review |

---

## 1. Scopo

AP-001 definisce il metamodel enterprise e l'architettura informativa del repository Digital StarGate. Il package stabilisce oggetti governati, identificatori, relazioni, ownership, stati, locator di evidenza e regole di pubblicazione necessarie per mantenere tracciabilità tra architettura, implementazione, review e release.

Il package non promuove capability operative, non modifica runtime, non introduce controllo remoto e non cambia i local physical interlocks.

## 2. Baseline verificata

La baseline autorevole è costituita da:

- PAA-002 v1.1 — capability e gap;
- ARB-002 — review indipendente `APPROVED WITH CONDITIONS`;
- ABC-001 — baseline `CONDITIONALLY CERTIFIED`;
- ABC-001 Evidence Annex — locator immutabili per CAP-01…CAP-04;
- `docs/architecture/index.md` — panoramica corrente;
- `mkdocs.yml` — struttura di pubblicazione.

AMP-001 è presente nel repository ma il contenuto verificato è incompleto rispetto al riepilogo dichiarato nel precedente ciclo. AP-001 usa quindi AMP-001 solo come indicazione di priorità e non come fonte sufficiente per dettagli, dipendenze o acceptance criteria.

## 3. Driver

1. Eliminare duplicazioni di capability, documenti e pipeline.
2. Rendere ripetibile la relazione tra decisione, implementazione, evidenza e approvazione.
3. Separare stato documentale, stato implementativo e stato operativo.
4. Proteggere il canonical data flow Analytics → Warehouse → consumer.
5. Conservare l'indipendenza della safety locale.
6. Consentire review e release evidence-driven.

## 4. Current state

Il repository contiene ADR, assessment, capability documentation, capitoli operativi, release note, codice e configurazioni. La governance è tuttavia distribuita e usa convenzioni non ancora uniformi. PAA-002 classifica Architecture Governance, Documentation Governance e Release Quality Governance come `Partial`.

Problemi principali:

- identificatori e metadati non uniformi;
- relazioni tra artefatti spesso espresse solo nel testo;
- assenza di un registro canonico unico;
- rischio di confondere documentazione con evidenza runtime;
- collocazione non uniforme di ADR e documenti architetturali;
- assenza di regole esplicite per supersession, deprecation e re-review.

## 5. Target state

Il repository adotta un modello in cui ogni elemento governato ha:

- un identificativo stabile;
- un tipo esplicito;
- un owner;
- uno stato documentale;
- uno stato di capability quando applicabile;
- relazioni tracciabili;
- locator verso evidenze ripetibili;
- criteri di approvazione e re-review;
- impatto su roadmap e release.

## 6. Metamodel enterprise

### 6.1 Entità governate

| Entità | Identificatore | Scopo |
|---|---|---|
| Capability | `CAP-nn` | Risultato o capacità della piattaforma |
| Architecture Package | `AP-nnn` | Insieme coerente di cambiamenti architetturali |
| Architecture Decision Record | `ADR-nnn` | Decisione architetturale e alternative |
| Assessment | prefisso specifico, es. `PAA`, `EA` | Valutazione della baseline o di uno scope |
| Architecture Review | `ARB-nnn` | Review indipendente |
| Baseline Certificate | `ABC-nnn` | Certificazione condizionata di una baseline |
| Evidence | `EV-nnn` o locator package-specific | Prova DOC/CFG/SRC/TST/INT/OPS/GOV |
| Risk | prefisso package + `Rnn` | Rischio tracciabile |
| Waiver | prefisso package + `Wnn` | Eccezione approvata e limitata |
| Release | versione esistente del repository | Unità di rilascio documentata |
| Work Item | identificativo del sistema di lavoro, se presente | Unità esecutiva collegata a un package |

Gli identificatori esistenti non vengono rinumerati retroattivamente.

### 6.2 Relazioni canoniche

```text
Driver / Risk
      |
      v
Capability <---- Assessment
      |
      v
Architecture Package ----> ADR
      |                       |
      v                       v
Implementation ----------> Evidence
      |                       |
      +--------> ARB Review <-+
                       |
                       v
             Baseline / Release decision
```

Relazioni obbligatorie:

- un AP deve indicare capability interessate, driver, rischi e dipendenze;
- un ADR deve indicare AP o capability di origine quando esistono;
- una review ARB deve indicare commit e artefatti sottoposti a review;
- una capability non può essere promossa senza evidenza conforme al modello PAA-002;
- una release deve indicare package inclusi, validazioni e rischi residui.

## 7. Stati

### 7.1 Stato documentale

- `Draft`
- `Proposed for review`
- `Approved`
- `Approved with conditions`
- `Superseded`
- `Deprecated`

### 7.2 Stato capability

Restano vincolanti gli stati PAA-002:

- `Implemented`
- `Partial`
- `Prepared`
- `Planned`
- `Missing`

`Operationally Verified` non è uno stato sostitutivo: è un attributo aggiuntivo consentito solo con evidenza OPS, test, health, runbook e criteri di rollback applicabili.

## 8. Repository information architecture

### 8.1 Collocazioni canoniche

| Artefatto | Percorso canonico |
|---|---|
| Panoramica architettura | `docs/architecture/index.md` |
| ADR | `docs/architecture/ADR-*.md` |
| Assessment, review e certificate | `docs/architecture/assessments/` |
| Architecture Package | `docs/architecture/packages/` |
| Metamodel e registri | `docs/architecture/` |
| Warehouse architecture | `docs/architecture/warehouse/` |
| Capability developer-facing | `docs/developer/` |
| Release notes | `docs/releases/` |
| Manuale operativo | `docs/chapters/` |

La posizione storica di `ADR-004-Operational-Architecture.md` sotto `assessments` è registrata come anomalia da valutare, non spostata da AP-001.

### 8.2 Metadati minimi

Ogni nuovo artefatto architetturale deve dichiarare almeno:

- identificativo;
- titolo;
- repository e branch;
- data/versione;
- owner o autorità;
- stato;
- baseline o commit di riferimento;
- documenti correlati;
- validazioni eseguite e non eseguite.

## 9. Traceability policy

Il registro canonico è `docs/architecture/traceability-register.md`.

Ogni riga deve collegare almeno:

- capability;
- package o decisione;
- artefatto implementativo;
- evidenza;
- review;
- release o disposizione;
- stato verificato.

I wildcard sono ammessi per inventario descrittivo, non come locator di evidenza definitivo.

## 10. Safety, security e operations

- I local physical interlocks restano indipendenti da applicazione, rete, cloud, portale e AI.
- Nessun metadato o stato documentale può essere interpretato come stato sicuro dell'osservatorio.
- Le capability remote o AI richiedono package, ADR, audit, autorizzazione e review dedicati.
- Dati stale, mancanti o degradati non equivalgono a stato sicuro.
- AP-001 non modifica protocolli, soglie, dispositivi o procedure operative.

## 11. Migration plan

### Fase 1 — Introduzione non distruttiva

- aggiungere metamodel e registro;
- aggiungere AP-001 alla navigazione;
- collegare gli artefatti certificati esistenti;
- non rinominare né spostare file storici.

### Fase 2 — Normalizzazione progressiva

- applicare metadati minimi ai documenti modificati in futuro;
- sostituire locator generici con riferimenti puntuali;
- registrare supersession e deprecation;
- collegare release e review.

### Fase 3 — Automazione dei controlli

- validare identificatori duplicati;
- verificare link e presenza nella navigazione;
- verificare campi minimi;
- produrre report di traceability drift.

L'automazione non è implementata da AP-001.

## 12. Acceptance criteria

AP-001 è accettabile quando:

1. il metamodel è pubblicato;
2. il registro di tracciabilità è pubblicato e inizializzato con la baseline certificata;
3. l'indice architetturale collega i nuovi artefatti;
4. MkDocs espone package, metamodel e registro;
5. nessuna capability viene promossa;
6. le anomalie e le validazioni non eseguite sono dichiarate;
7. una review ARB indipendente valuta coerenza, scalabilità, manutenibilità e traceability.

## 13. Rischi e debito

| ID | Tipo | Descrizione | Trattamento |
|---|---|---|---|
| AP1-R01 | Risk | Metadati introdotti ma non mantenuti | Ownership e controlli automatici futuri |
| AP1-R02 | Risk | Registro manuale soggetto a drift | Validation tool in package successivo |
| AP1-R03 | Risk | Confusione tra capability e componente | Definizioni e review ARB |
| AP1-R04 | Risk | AMP-001 incompleto rispetto al riepilogo dichiarato | Correggere AMP-001 con package separato o remediation ARB |
| AP1-R05 | Risk | ADR collocati in directory non uniforme | Normalizzazione non distruttiva dopo inventario |
| AP1-TD01 | Technical debt | Nessun controllo automatico degli ID | Backlog documentation governance |
| AP1-TD02 | Technical debt | Traceability release-package incompleta | Aggiornamento incrementale delle release note |

## 14. Validazioni

### Eseguite

- verifica del branch `main`;
- ispezione PAA-002, ARB-002, ABC-001, AMP-001, architecture index e MkDocs;
- verifica dell'assenza di un AP-001 o metamodel equivalente nei risultati del repository;
- controllo per ispezione delle relazioni e dei percorsi introdotti.

### Non eseguite

- `mkdocs build --strict`;
- link checker automatico;
- lint Markdown/YAML;
- test applicativi;
- GitHub Actions CI;
- test runtime, rete, hardware o safety.

## 15. Handoff ARB

L'Architecture Review Board deve verificare:

- compatibilità con PAA-002 e ABC-001;
- sufficienza delle entità e relazioni del metamodel;
- assenza di duplicazioni concettuali;
- adeguatezza delle regole di stato ed evidenza;
- scalabilità della information architecture;
- trattamento dell'incompletezza AMP-001;
- permanenza del boundary fail-safe locale.

**Esito del package:** PROPOSED FOR INDEPENDENT ARB REVIEW.