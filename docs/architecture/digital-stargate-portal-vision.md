# Digital StarGate Portal Vision

| Campo | Valore |
|---|---|
| Documento | Digital StarGate Portal Vision |
| Identificativo | DSGP-VIS-001 |
| Stato | Active reference — incremental implementation |
| Data | 30/07/2026 |
| Ultima revisione | 10/09/2026 |
| Sponsor | Massimo Mainini |
| Roadmap | AMP-002 |
| Package correlati | AP-007, AP-008, AP-009, AP-010, AP-011, AP-012 |

## 1. Visione

Digital StarGate Portal (DSGP) è il punto di accesso unificato all'ecosistema Digital StarGate. Ospita due esperienze distinte:

- **Digital StarGate Analytics Platform (DSAP)** per dati storici, KPI, trend, reporting e analisi;
- **Digital StarGate Operations Center (DSOC)** per stato live, health, eventi, allarmi, incidenti e operazioni autorizzate.

Il portale è un presentation boundary. Non è la fonte autorevole del dominio, non accede direttamente agli apparati e non sostituisce gli interblocchi locali.

UI 7.0 realizza il Portal shell e la information architecture sul canale corrente GitHub Pages/MkDocs. Le evoluzioni applicative future rimangono governate separatamente.

## 2. Obiettivi

- offrire una vista coerente dell'osservatorio;
- separare chiaramente analisi storica e operazioni live;
- riusare dati, contratti, identità e audit governati;
- rendere freshness, qualità e stato degradato sempre visibili;
- supportare desktop, tablet e future viste mobile;
- consentire evoluzione multi-osservatorio senza duplicare logica di dominio.

## 3. Information architecture

```text
Digital StarGate Portal
|
+-- Home
+-- Observatory Live
+-- Operations Center (DSOC)
|   +-- System status
|   +-- Weather and safety
|   +-- Equipment health
|   +-- Events and alarms
|   +-- Incident console
|   +-- Runbooks
|   +-- Authorized commands
|
+-- Analytics Platform (DSAP)
|   +-- Session analytics
|   +-- Weather and sky quality
|   +-- Equipment performance
|   +-- Reliability and maintenance
|   +-- Incident analytics
|   +-- Scientific analytics
|   +-- Executive dashboard
|   +-- Reports and exports
|
+-- Maintenance
+-- Inventory and configuration
+-- Documentation
+-- Administration
+-- AI Assistant (future, read-only first)
```

## 4. Architectural boundaries

### Presentation

- rendering, navigation, interaction e accessibility;
- role-based views;
- visualizzazione di freshness, provenance e stato degradato;
- nessuna logica safety o device-specific.

### Application

- query e command use case;
- authorization e policy enforcement;
- orchestration, validation e audit;
- mapping verso read model e port infrastrutturali.

### Domain

- stati, invarianti, eventi e policy dell'osservatorio;
- nessuna dipendenza da framework UI, database, broker o driver.

### Infrastructure

- adapter per N.I.N.A., PHD2, CPWI, ASCOM/Alpaca, rete, meteo, AllSky, telemetry store e notification channel;
- implementazione dei port applicativi;
- resilienza, retry, buffering e health.

## 5. DSAP — Analytics Platform

DSAP consuma dati curati e governati. Non legge direttamente log grezzi quando esiste un data product o access layer autorevole.

Ambiti iniziali:

- sessioni osservative;
- target e risultati acquisizione;
- qualità del cielo, meteo e seeing;
- performance di montatura, guida, camere e autofocus;
- affidabilità, incidenti, manutenzione e obsolescenza;
- KPI operativi, scientifici ed executive;
- data quality, lineage e completezza;
- trend e analisi predittive future.

Ogni metrica deve dichiarare formula, grain, owner, sorgente, freshness, qualità e periodo di validità.

## 6. DSOC — Operations Center

DSOC presenta lo stato operativo corrente con timestamp, freshness e health espliciti.

Ambiti iniziali:

- tetto/cupola e sensori open, closed e safe;
- meteo e safety status;
- montatura, telescopio, camere, focuser e flat panel;
- N.I.N.A., PHD2, CPWI e scheduler;
- EAGLE, Raspberry Pi, UPS e alimentazione;
- Starlink, Teltonika, VPN e failover;
- AllSky;
- heartbeat, eventi, allarmi e incidenti;
- timeline e live logs governati;
- runbook e recovery guidance.

La prima release deve essere **read-only**. I comandi vengono introdotti soltanto dopo AP-005, AP-007, AP-008, AP-010 e review safety/security dedicate.

## 7. Command model

```text
User
  |
  v
Portal UI
  |
  v
Authorized Application Use Case
  |
  +--> Policy / Identity / Session checks
  +--> Safety precondition checks
  +--> Audit intent
  |
  v
Infrastructure Port / Adapter
  |
  v
Local controller or external system
```

Regole:

1. nessun comando diretto dalla UI a relay, device o driver;
2. ogni comando ha identity, role, reason, correlation ID e timestamp;
3. precondizioni unknown o stale impediscono il comando;
4. il controller locale può rifiutare il comando;
5. la UI non può bypassare interlock o safe state;
6. esito e stato successivo sono verificati e auditati.

## 8. Real-time and historical data

Lo stesso fatto operativo può alimentare due viste senza duplicare la logica:

```text
Authoritative producer
        |
        v
Versioned operational contract
        |
        +--> Live projection / DSOC
        |
        +--> Curated historical data product / DSAP
```

La projection live è derivata e ricostruibile. Il Warehouse storico conserva lineage, quality e retention secondo AP-002.

## 9. Security, safety and privacy

- least privilege e deny by default;
- MFA e session assurance per operazioni privilegiate;
- audit immutabile per accessi e comandi;
- separation of duties per amministrazione e safety override;
- secret mai esposti nel browser;
- protezione di immagini, log e metadati sensibili;
- fail-safe locale indipendente da portale, rete e cloud.

## 10. Observability

DSGP, DSAP e DSOC devono produrre:

- structured logs;
- metrics e SLI/SLO;
- distributed traces dove applicabile;
- health e dependency checks;
- correlation e causation IDs;
- alert e runbook locator;
- audit separato dai log diagnostici.

## 11. Delivery increments

1. **Portal shell** — navigazione, identity e design system.
2. **DSOC read-only** — stato live, freshness, health ed eventi.
3. **DSAP baseline** — KPI storici e report governati.
4. **Operational workflows** — incidenti, maintenance e runbook.
5. **Controlled commands** — solo dopo evidence e review.
6. **Advanced analytics and AI** — read-only first, provenance e evaluation.

## 12. Acceptance criteria

- DSAP e DSOC hanno boundary e ownership distinti;
- il portale usa application use case e contratti versionati;
- freshness e unknown state sono visibili;
- nessun accesso diretto UI-to-device;
- nessuna pipeline Analytics parallela dai log grezzi;
- authorization, audit e safety precondition sono testabili;
- desktop, tablet e mobile sono supportati dal presentation layer corrente;
- multi-observatory tenancy non è implementata implicitamente ma il modello non la impedisce.

## 13. Open issues

- scelta dello stack frontend e del Backend for Frontend per le future capability applicative oltre GitHub Pages/MkDocs;
- protocollo live e modello subscription;
- time-series/event storage;
- SLI/SLO e budget di cardinalità;
- matrice ruoli e comandi;
- tassonomia widget e design tokens;
- ownership KPI e data product;
- strategia multi-osservatorio;
- modalità offline/degraded del portale.

## 14. Validazioni

### Eseguite

- coerenza per ispezione con AP-002…AP-006 e AMP-002;
- verifica della separazione Presentation/Application/Domain/Infrastructure;
- verifica del principio di indipendenza safety.

### Non eseguite

- prototipo UI;
- usability/accessibility test;
- threat model eseguibile;
- performance, load, failover o runtime test;
- `mkdocs build --strict` e link checking automatico.
