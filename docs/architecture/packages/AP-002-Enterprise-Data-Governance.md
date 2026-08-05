# AP-002 — Enterprise Data Governance

| Campo | Valore |
|---|---|
| Identificativo | AP-002 |
| Titolo | Enterprise Data Governance |
| Tipo | Architecture Package |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Owner proposto | Digital StarGate Data Governance Owner |
| Autorità | Digital StarGate Enterprise Architect |
| Baseline | `70f7ec1a79d73b1d388ec4009a33cdbc5042f8d7` |
| Mandato | PAA-002, ABC-001, AP-001, ARB-003 |
| Stato | Proposed for independent ARB review |

## 1. Scopo

AP-002 definisce la governance enterprise dei dati di Digital StarGate: ownership, classificazione, contratti, lifecycle, versionamento, compatibilità, qualità, lineage, retention, accesso, evidence e processo di cambiamento.

Il package consolida regole già presenti nella documentazione Warehouse e nei contratti canonici senza sostituire schema eseguibili, codice o validator esistenti.

AP-002 non modifica runtime, pipeline, dataset, protocolli, soglie meteo, controlli dell'osservatorio o interblocchi fisici locali.

## 2. Baseline verificata

La baseline contiene:

- cinque dataset Warehouse documentati: `sessions.parquet`, `targets.parquet`, `equipment.parquet`, `quality.parquet`, `weather.parquet`;
- regole esistenti per identificatori, unità, valori mancanti, versionamento e compatibilità;
- contratti canonici in `DigitalStarGate.Contracts` e `contracts/`;
- Semantic Versioning per API, DTO, Event e JSON Schema;
- metamodel e traceability register introdotti da AP-001;
- ARB-003 `APPROVED WITH CONDITIONS`.

## 3. Driver

1. Evitare definizioni duplicate dello stesso dato.
2. Rendere espliciti owner e steward.
3. Proteggere il canonical data flow Analytics → Warehouse → consumer.
4. Consentire evoluzione compatibile di dataset, API ed eventi.
5. Rendere ripetibili qualità, lineage e decisioni di rilascio.
6. Preparare consumer layer, reporting, telemetry e AI senza pipeline parallele.
7. Separare dati operativi, storici, derivati, configurativi e di safety.

## 4. Scope

### In scope

- dataset Analytics e Warehouse;
- contratti API, DTO, Event e JSON Schema;
- metadata di dataset e build;
- dati operativi, storici e derivati;
- quality rules e data quality evidence;
- lineage producer-transform-consumer;
- retention, archival e disposal policy;
- ownership, stewardship e approvazione delle modifiche;
- classificazione e accesso;
- compatibility e migration policy.

### Out of scope

- implementazione di un data catalog software;
- modifica degli schema eseguibili;
- migrazione fisica dei dati;
- creazione del Warehouse consumer layer;
- live telemetry runtime;
- AI assistant runtime;
- safety certification.

## 5. Principi

1. **One authoritative contract per data product.**
2. **Documentation does not replace executable schema.**
3. **Consumers depend on contracts, not accidental storage layout.**
4. **Missing, zero, false and acquisition error are distinct states.**
5. **Units and time semantics are explicit.**
6. **Breaking changes require a new major version and migration plan.**
7. **Lineage is required before certification.**
8. **Derived data never silently overwrites source data.**
9. **Safety state cannot be inferred from stale, missing or degraded data.**
10. **AI consumes governed data and may not create an uncontrolled raw-log pipeline.**

## 6. Governed data objects

| Oggetto | Identificatore | Owner minimo | Contratto autorevole |
|---|---|---|---|
| Data Product | `DP-nnn` | Data Product Owner | schema + metadata + quality rules |
| Dataset | nome stabile esistente | Dataset Owner | executable schema |
| Data Contract | `DC-nnn` o versione contratto esistente | Contract Owner | JSON Schema/OpenAPI/DTO/Event schema |
| Quality Rule | `DQR-nnn` | Data Steward | validator/test |
| Lineage Relation | `DL-nnn` | Data Steward | producer-transform-consumer locator |
| Retention Rule | `DR-nnn` | Data Owner | policy approvata |
| Data Issue | work item esistente | Data Steward | evidence e remediation |

Gli identificatori esistenti non vengono rinumerati retroattivamente. I nuovi identificatori devono essere registrati nel traceability register.

## 7. Ownership model

| Ruolo | Responsabilità |
|---|---|
| Data Governance Owner | mantiene policy, approva eccezioni e coordina review |
| Data Product Owner | accountability su finalità, qualità, consumer e lifecycle |
| Data Steward | schema, metadata, glossary, lineage e issue management |
| Producer Owner | correttezza del dato prodotto e dei cambiamenti |
| Consumer Owner | test di compatibilità e uso conforme al contratto |
| Release Authority | decide inclusione in release sulla base delle evidenze |
| ARB | review indipendente di cambiamenti architetturali o incompatibili |

La stessa persona può coprire più ruoli nel progetto, ma autore e reviewer devono restare distinti per le decisioni ARB.

## 8. Data classification

| Classe | Descrizione | Esempi |
|---|---|---|
| Operational | stato corrente o recente usato dalle operazioni | stato sessione, weather snapshot |
| Historical | record consolidati e append-only o ricostruibili | dataset Warehouse |
| Reference | valori normalizzati e tassonomie | equipment names, filter catalog |
| Configuration | valori che influenzano il comportamento | configurazioni versionate |
| Derived | aggregati, indicatori e projection | KPI, quality metrics |
| Security-sensitive | identità, autorizzazioni, riferimenti a secret | User, Role, Permission, SecretReference |
| Safety-relevant | dati osservati da processi safety ma non autorità fisica | weather safe/unsafe, roof/mount status |

I secret non sono data product e non devono transitare in dataset, DTO, Event o log.

## 9. Contract and schema policy

Ogni data product deve dichiarare:

- nome e scopo;
- owner e steward;
- schema e versione;
- grain;
- chiavi e identificatori;
- timezone e unità;
- nullability e semantica dei valori mancanti;
- producer e consumer;
- quality rules;
- lineage;
- retention;
- classificazione;
- compatibility policy;
- evidence locator.

### Compatibilità

- modifica additiva opzionale: minor version;
- correzione editoriale non osservabile: patch version;
- rimozione, rinomina, cambio tipo, significato, grain o unità: major version;
- restrizioni che possono rifiutare dati prima validi richiedono analisi consumer;
- un cambiamento è completo solo dopo test producer, validator e consumer.

## 10. Data quality

Dimensioni minime:

- completeness;
- validity;
- uniqueness;
- consistency;
- timeliness/freshness;
- accuracy quando verificabile;
- referential integrity;
- unit and time correctness.

Ogni quality rule deve indicare severity, soglia o condizione, dataset, campo, owner, comando di verifica, esito e comportamento in caso di fallimento.

Un quality gate può essere:

- `Block` — impedisce pubblicazione o release;
- `Warn` — consente pubblicazione con rischio registrato;
- `Observe` — misura senza decisione automatica.

## 11. Lineage

Il lineage minimo è:

```text
Producer → Source artifact → Transformation → Data product → Consumer
```

Per ogni passaggio devono essere registrati:

- repository path;
- commit o build identifier;
- input e output;
- trasformazione o comando;
- schema version;
- evidence type;
- owner.

Dashboard, reporting e AI devono consumare Warehouse o contratti governati. Accessi diretti ai log grezzi richiedono eccezione esplicita e non possono diventare pipeline parallele autorevoli.

## 12. Retention, archival and disposal

Ogni data product deve avere una retention rule che distingua:

- working data;
- published/current data;
- historical data;
- backup;
- generated artifacts;
- logs and diagnostics.

La durata concreta non viene inventata da AP-002: deve essere proposta dal Data Product Owner, verificata contro esigenze operative, capacità di storage, privacy e riproducibilità, quindi approvata dalla Release Authority o dall'ARB quando architetturalmente rilevante.

La cancellazione deve essere verificabile e non deve eliminare evidenze necessarie a audit, incident review o riproducibilità delle release.

## 13. Security and access

- least privilege;
- separazione read/write/admin;
- secret solo tramite `SecretReference`;
- audit per modifiche a schema, configurazione e policy;
- dati personali minimizzati;
- export e pubblicazione coerenti con classificazione;
- AI read-only first, senza tool execution implicita.

## 14. Safety boundary

- `safe` o `unsafe` nei dataset è una rappresentazione osservata, non l'autorità fisica di sicurezza;
- dati mancanti, stale o degradati non equivalgono a safe;
- local physical interlocks restano indipendenti da applicazione, rete, Warehouse, dashboard e AI;
- retention o trasformazione non deve alterare il significato originale degli eventi safety-relevant.

## 15. Change process

1. proposta del cambiamento con owner, motivazione e impatto;
2. classificazione compatibility;
3. aggiornamento schema e metadata;
4. aggiornamento validator e test;
5. verifica producer e consumer;
6. migration e rollback plan per breaking change;
7. aggiornamento lineage e traceability;
8. ARB review quando cambia semantic meaning, canonical flow, safety boundary o major version;
9. release decision con evidenze.

## 16. Transition plan

### Fase 1 — Baseline documentale

- pubblicare AP-002 e Data Governance Standard;
- registrare i cinque dataset Warehouse come data product candidati;
- assegnare owner proposti senza promuovere stati.

### Fase 2 — Inventario e schema

- collegare schema eseguibili e metadata generator;
- registrare grain, chiavi, unità, timezone e consumer;
- individuare duplicazioni e gap.

### Fase 3 — Quality e lineage

- registrare quality rule esistenti;
- produrre lineage per Analytics → Warehouse → Dashboard;
- introdurre evidence locator immutabili.

### Fase 4 — Automazione

- validazione machine-readable;
- compatibility checks;
- traceability drift report;
- release gate automatizzati.

## 17. Acceptance criteria

AP-002 è accettabile quando:

1. policy e ruoli sono pubblicati;
2. i cinque dataset Warehouse sono registrati con owner proposto, grain e contratto autorevole;
3. compatibility e quality policy sono definite;
4. lineage minimo è definito;
5. retention richiede approvazione esplicita e non usa durate inventate;
6. safety boundary è preservato;
7. traceability register collega AP-002, artefatti e review;
8. validazioni eseguite e non eseguite sono dichiarate;
9. una review ARB indipendente valuta il package.

## 18. Rischi e debito

| ID | Tipo | Descrizione | Trattamento |
|---|---|---|---|
| AP2-R01 | Risk | Owner solo proposti e non formalmente assegnati | approvazione e registro RACI |
| AP2-R02 | Risk | Schema documentale diverge da schema eseguibile | schema executable authoritative + check |
| AP2-R03 | Risk | Retention non definita per i data product | decisione owner-specific senza inventare soglie |
| AP2-R04 | Risk | Lineage manuale soggetto a drift | automazione futura |
| AP2-R05 | Risk | Consumer non testati su breaking change | compatibility matrix e release gate |
| AP2-R06 | Risk | Safety-relevant data interpretati come autorità safety | boundary e review obbligatoria |
| AP2-TD01 | Technical debt | Nessun catalogo machine-readable completo | backlog governance automation |
| AP2-TD02 | Technical debt | Nessun test CI osservato per questo package | validation before closure |

## 19. Validazioni

### Eseguite

- verifica del branch `main`;
- ispezione AP-001 e ARB-003;
- ispezione documentazione Warehouse dataset/schema;
- ispezione contratti canonici e policy di versionamento;
- verifica per ispezione di coerenza con canonical data flow e safety boundary.

### Non eseguite

- `mkdocs build --strict`;
- link checker e lint YAML/Markdown;
- inventario completo degli schema eseguibili;
- test producer, validator e consumer;
- compatibility test;
- test Warehouse/Analytics;
- GitHub Actions CI;
- test runtime, rete, hardware o safety.

## 20. Handoff ARB

L'Architecture Review Board deve verificare:

- assenza di duplicazioni rispetto a Warehouse e platform contracts;
- chiarezza di ownership e stewardship;
- sufficienza di classification, compatibility, quality, lineage e retention;
- adeguatezza del processo di breaking change;
- protezione del canonical data flow;
- separazione tra dati safety-relevant e autorità safety;
- gestione delle condizioni ARB-003 rilevanti.

**Esito del package: PROPOSED FOR INDEPENDENT ARB REVIEW.**