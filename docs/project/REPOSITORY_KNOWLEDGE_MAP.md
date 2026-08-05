# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 1.0 |
| Stato | Active |
| Baseline analizzata | `fc2a80817fb8216211ed4b5045d8b4e9961fce5a` |
| Data | 04/08/2026 |

## 1. Scopo

Questa mappa descrive l'intero repository Digital StarGate per domini, responsabilità e fonti autorevoli. È un indice di conoscenza: non sostituisce i documenti tecnici sottostanti.

## 2. Struttura generale

Il repository contiene quattro prodotti correlati:

1. **Manuale tecnico dell'osservatorio** — capitoli operativi, infrastrutturali, software, safety e manutenzione.
2. **Enterprise Architecture Repository** — Architecture Package, ADR, capability, assessment, review, evidence e roadmap.
3. **Digital StarGate Enterprise Portal** — sito MkDocs Material, centri enterprise, componenti JavaScript/CSS e dataset di proiezione.
4. **Developer Foundation** — solution .NET, contratti, test, pipeline analytics, workflow CI/CD e tooling.

## 3. Documentazione operativa dell'osservatorio

La serie `docs/chapters/01`–`44` copre:

- introduzione e architettura generale;
- cupola, impianto elettrico, rete ed EAGLE;
- montatura CGX-L, C8 XLT, Quattro 200P, camere e treno ottico;
- N.I.N.A., PHD2, CPWI e ASCOM;
- automazione, avvio, acquisizione e chiusura;
- emergenze, recovery, meteo, AllSky e manutenzione;
- configuration management, backup, asset management e sicurezza informatica;
- dati, KPI, troubleshooting, problem management e obsolescenza;
- schemi, registri, requisiti, FMEA, ruoli, handover e accettazione.

Le appendici mantengono dati da validare e registro revisioni. Le procedure safety e gli interlock locali prevalgono su qualunque funzione del portale.

## 4. Architettura enterprise

### Foundation

- `AP-001` Enterprise Metamodel and Repository Information Architecture.
- `AP-002` Enterprise Data Governance.
- `AP-003` Observatory Automation Architecture.
- `AP-004` Enterprise Telemetry and Observability Architecture.
- `AP-005` Identity, Access and Remote Operations Security.
- `AP-006` Enterprise Configuration and Asset Management.

### Operations, integration, infrastructure e safety

- `AP-007` Enterprise Operations and Service Management.
- `AP-008` Enterprise Integration Architecture.
- `AP-009` Enterprise Infrastructure Architecture.
- `AP-010` Enterprise Safety Assurance Architecture.

### Digital platforms

- `AP-011` Enterprise Analytics Platform — DSAP.
- `AP-012` Enterprise Operations Center — DSOC.

### Scientific platform

- `AP-013` Scientific Image Repository Architecture.
- `AP-014` Scientific Observation Catalog and Search — pianificato.
- `AP-015` Scientific Knowledge Platform — pianificato.

### Decisioni architetturali

- `ADR-001` Session Layer.
- `ADR-002` Analytics Quality Gates.
- `ADR-003` Warehouse Engine.
- `ADR-004` Operational Architecture.
- `ADR-005` Weather Safety Interlock.

Le decisioni nuove che cambiano boundary, contratti, authority o invarianti richiedono un ADR; le scelte operative reversibili possono essere registrate nel Decision Log.

## 5. Governance e assurance

Il repository contiene:

- Enterprise Metamodel e Data Governance Standard;
- Architecture Traceability Register;
- assessment `EA-*` e `PAA-*`;
- review indipendenti `ARB-002`–`ARB-012`;
- Architecture Baseline Certificate `ABC-001`;
- Architecture Master Plan `AMP-001`;
- roadmap autorevole `AMP-002`;
- validation campaign, execution evidence, closure plan e final re-review.

Una review “approved with conditions” non equivale a certificazione runtime. Le condizioni ARB restano aperte finché non esistono evidence, acceptance e re-review esplicite.

## 6. AP-012 e Operations Center

DSOC presenta stato operativo, health, freshness, eventi, allarmi, incidenti e runbook. La baseline resta read-only salvo autorizzazioni future.

Vincoli permanenti:

- nessun comando diretto UI-to-device;
- authorization, four-eyes, audit e safety preconditions obbligatori;
- stato unknown o stale blocca i comandi;
- il controller locale mantiene autorità finale;
- produzione, credenziali reali e apparati fisici non sono implicitamente autorizzati.

La campagna ENV-011 ha evidenza tecnica su ambiente Hyper-V isolato e simulatore, ma l'accettazione complessiva dipende dai controlli e dalle evidence residue registrate nei documenti ARB-012-C04.

## 7. AP-013 e Scientific Data Platform

Il dominio scientifico comprende:

- inventory delle sorgenti;
- Scientific Data Manager `DSDM-001`–`DSDM-004`;
- session discovery;
- manifest, checksum, lineage e provenance;
- importer e safe transfer `COPY_ONLY`;
- readiness gate e execution evidence;
- catalogo sessioni e proiezioni per il portale.

Regole:

- bulk transfer e source cleanup non sono autorizzati senza evidence e gate;
- SHA-256 e manifest sono parte del controllo di integrità;
- le sessioni e i target sono esposti al portale tramite Scientific Data Engine;
- dataset e cataloghi JSON sono proiezioni, non fonti primarie.

## 8. Enterprise Portal

MkDocs Material è il presentation layer documentale. La configurazione è in `mkdocs.yml`.

Centri principali:

- Home Enterprise;
- Mission Control;
- Documentation Center;
- Roadmap Center;
- Architecture Center;
- Scientific Platform;
- Scientific Session Catalog e Detail;
- Repository Intelligence e Analytics;
- Scientific Intelligence;
- Developer e manuale tecnico.

Componenti JavaScript:

- `homepage-effects.js`;
- `latest-observation.js`;
- `mission-control.js`;
- `nav-scroll.js`;
- `page-enhancements.js` — Navigation Manager;
- `roadmap.js`;
- `scientific-data-engine.js`;
- `scientific-session-explorer.js`;
- `scientific-session-detail.js`.

Stili sotto `docs/styles`; dati di proiezione sotto `docs/data`.

## 9. Scientific Data Engine

API condivise:

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

Il motore possiede caricamento, caching, normalizzazione e accesso ai dati scientifici. I renderer non devono implementare pipeline parallele.

## 10. Developer Foundation .NET

La solution `DigitalStarGate.sln` comprende:

- `DigitalStarGate.Api`;
- `DigitalStarGate.Application`;
- `DigitalStarGate.Contracts`;
- `DigitalStarGate.Domain`;
- `DigitalStarGate.Infrastructure`;
- `DigitalStarGate.SharedKernel`;
- Unit Tests;
- Integration Tests;
- Architecture Tests.

Baseline toolchain:

- .NET SDK `10.0.302`;
- target framework `net10.0`;
- C# `14.0`;
- nullable e implicit usings abilitati;
- warnings come errori;
- code style enforced in build;
- build deterministica;
- package versions centralizzate.

Boundary obbligatori:

- Domain indipendente da framework e Infrastructure;
- Application orchestra use case e definisce port;
- Infrastructure implementa adapter;
- Contracts espone DTO, event e API versionate;
- API resta presentation/composition boundary.

## 11. Contratti

Il repository include:

- OpenAPI `contracts/openapi/digital-stargate-v1.yaml`;
- JSON Schema eventi `contracts/events/platform-events.schema.json`;
- documentazione canonica in `docs/developer/platform-contracts.md`.

Concetti principali: ObservationSession, Target, Equipment, Observatory, ImageFrame, WeatherSnapshot, TelemetrySample, SafetyStatus, User, Role, Alert e Configuration.

I contratti seguono Semantic Versioning; errori API usano Problem Details con error code e correlation ID; i secret non devono transitare in DTO, eventi o log.

## 12. Analytics e Warehouse

Il repository contiene:

- warehouse engine e data flow;
- dataset/schema e quality gates;
- pipeline analytics e build history;
- KPI catalog e governance standard;
- dashboard, storico e configuration summary;
- workflow di validazione history e session package.

Ogni KPI deve dichiarare formula, grain, owner, sorgente, freshness, qualità e periodo di validità.

## 13. CI/CD e pubblicazione

Workflow principali:

- `developer-foundation.yml`: restore, build, test, format e `mkdocs build --strict`;
- `deploy-pages.yml`: build MkDocs, artifact e deploy GitHub Pages;
- workflow session analysis e package validation;
- history validation;
- generazione Word.

La pubblicazione è valida solo dopo successo del workflow applicabile e verifica del sito. La presenza di un commit non prova da sola il deployment.

## 14. Dati e proiezioni

Directory principali:

- `data/analytics` — build history e dati analytics;
- `docs/data` — roadmap, scientific catalog, command center e altre proiezioni del portale;
- `session-reports` — report di sessione;
- `contracts` — schemi machine-readable;
- `scripts` e tooling — build, analysis, validation e generation.

Le proiezioni devono indicare authority, schema version e data di aggiornamento quando applicabile.

## 15. Release e materiale storico

Il repository conserva release note, guide di installazione e artefatti di versioni precedenti. Questi documenti sono utili per lineage e migrazione, ma non devono prevalere sulla baseline corrente, sulle release note più recenti o sui documenti architetturali approvati.

## 16. Rischi e incongruenze note

- il README root descrive ancora prevalentemente il manuale tecnico e non l'intera piattaforma enterprise;
- coesistono più workflow di pubblicazione/documentazione, inclusi file disabilitati: occorre mantenere un owner chiaro;
- lo stato del portale e lo stato dei runtime DSOC/AP-013 non devono essere confusi;
- script inline e dipendenze dal DOM interno di Material rappresentano debito da ridurre;
- roadmap JSON e dashboard possono diventare stale rispetto ad AMP-002;
- vecchie release possono sembrare correnti se non contestualizzate.

## 17. Percorso di lettura consigliato

1. `AI_BOOTSTRAP.md`.
2. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`.
3. questo Knowledge Map.
4. `AMP-002` e `docs/data/roadmap.json`.
5. Architecture Package e ADR coinvolti.
6. review/evidence/gate applicabili.
7. backlog, technical debt e decision log.
8. codice, componenti o workflow oggetto della modifica.
