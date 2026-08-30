# Functional Roadmap Expansion — 2026-08-30

| Campo | Valore |
|---|---|
| Stato | Approved for planning |
| Scope | Digital StarGate future capabilities before BKL-015 implementation |
| Decision | Tutte le capability BKL-029–BKL-046 sono approvate per inserimento nella roadmap; l'ordine di implementazione resta governato dal backlog |

## 1. Principi architetturali

- Il portale, l'AI e gli analytics sono read-only rispetto agli apparati salvo futura introduzione di un command broker governato.
- La Safety Authority resta fisica/locale e non viene sostituita da score, AI o dashboard.
- Telemetria realtime, storico scientifico, processing provenance e knowledge graph devono restare semanticamente distinti ma correlabili.
- Ogni assessment AI deve essere spiegabile, indicare evidence e confidence e distinguere osservazione, inferenza e raccomandazione.
- I collector sull'EAGLE devono essere leggeri; reasoning, analytics storici e AI non devono gravare sul computer operativo.
- La post-produzione PixInsight deve produrre provenance riproducibile senza rendere obbligatorio il trasferimento delle immagini verso servizi AI esterni.
- L'AI di post-processing parte in modalità advisory: propone workflow e parametri ma non modifica automaticamente l'immagine senza approvazione esplicita dell'utente.

## 2. BKL-029 — SQM Sky Quality Telemetry & Scientific History

**Priorità proposta: P1.**

### Gap verificato

Observatory Status contiene già il campo UI `SQM` e `observatory-status.js` renderizza `weather.sqm_mag_arcsec2`. Tuttavia l'adapter canonico `Export-NinaObservatoryStatus.ps1` valorizza oggi esplicitamente `sqm_mag_arcsec2 = $null`.

### Obiettivo

Integrare una sorgente reale e verificata della qualità del cielo in **mag/arcsec²**, pubblicarla nella telemetria realtime e conservarla nelle sessioni scientifiche.

### Work package

1. **Source discovery SQM**
   - verificare se il dato è disponibile dal CloudWatcher/Lunatico, da un eventuale sensore SQM dedicato, da ASCOM ObservingConditions o da altro endpoint read-only già presente;
   - identificare unità, frequenza di campionamento, timestamp, validità e condizioni in cui il valore è assente/non affidabile;
   - non stimare SQM da brightness/cloud cover se non esplicitamente definito come metrica distinta.

2. **Realtime telemetry**
   - aggiungere SQM alla source adapter appropriata;
   - mantenere il campo canonico `weather.sqm_mag_arcsec2`;
   - preservare `UNKNOWN/STALE` quando la misura non è disponibile o non fresca;
   - pubblicare Observatory Status senza cambiare il contratto UI già esistente.

3. **Scientific session history**
   - estendere i metadata scientifici con statistiche SQM della finestra osservativa;
   - almeno: `sqm_start`, `sqm_end`, `sqm_min`, `sqm_max`, `sqm_mean`, `sqm_median`, numero campioni validi e coverage temporale;
   - associare timestamp/source/quality per mantenere provenance;
   - propagare SQM nel catalogo scientifico, nei report di sessione e nella future Target Knowledge Base.

4. **Quality analytics**
   - usare SQM come indicatore descrittivo della qualità del cielo, non come Safety signal;
   - correlare in futuro SQM con background delle immagini, FWHM, guiding, Luna e qualità finale;
   - consentire confronti storici tra sessioni e stagioni.

### Acceptance criteria

- valore realtime visualizzato in Observatory Status con freshness verificata;
- perdita source -> `—`/`UNKNOWN`, mai last-known-good presentato come corrente;
- almeno una sessione reale con SQM storicizzato e provenance completa;
- report/session catalog aggiornati;
- CI e Pages PASS.

## 3. BKL-030 — EAGLE Health & Reliability Telemetry

**Priorità proposta: P1.**

Nuova capability `EAGLE osservato` in Observatory Status con stato spiegabile `HEALTHY / DEGRADED / CRITICAL / UNKNOWN`.

Controlli previsti:

- spazio disco libero e trend;
- previsione esaurimento spazio / notti residue stimate;
- RAM disponibile, commit e memory pressure;
- CPU media, picchi e process pressure;
- uptime e reboot inattesi;
- temperatura hardware/CPU se esposta da fonte verificabile;
- disk/SMART health se disponibile in read-only;
- latenza I/O e test di scrittura non distruttivo sulla working directory;
- time synchronization / clock drift / NTP state;
- Windows Event Log `System` e `Application` con aggregazione Critical/Error;
- crash di N.I.N.A., PHD2, ASCOM LocalServer e componenti Digital StarGate;
- stato Scheduled Task Digital StarGate;
- heartbeat del plugin N.I.N.A.;
- freshness dei producer;
- disponibilità delle directory/log N.I.N.A., PHD2 e CloudWatcher;
- USB/COM error pattern;
- pending reboot / Windows Update state;
- software/configuration drift rispetto alla baseline governata.

Lo score deve mostrare sempre le cause che lo determinano e non deve essere confuso con Safety.

## 4. BKL-031 — Observation Planner intelligente

Ranking target per setup con altitudine, transito, Luna, fase, separazione, finestra astronomica, forecast meteo, filtri, camera/OTA e storico scientifico.

## 5. BKL-032 — Session Readiness / Go-No-Go Decision Support

Dashboard pre-sessione con meteo, SQM, Power, Network, Safety osservata, EAGLE health, mount/camera/dome, storage, target e finestra osservativa. Decision support soltanto; nessuna Safety Authority.

## 6. BKL-033 — Observatory Digital Twin

Rappresentazione visuale e navigabile di asset, dipendenze, stato realtime, source, contratti e relazioni. Il Knowledge Graph costituisce il modello strutturale sottostante.

## 7. BKL-034 — Scientific Image Gallery evoluta

Immagini finali collegate a sessioni sorgenti, target, OTA, camera, filtri, integrazione, seeing/FWHM, SQM, condizioni meteo, processing, PixInsight workflow provenance e report.

## 8. BKL-035 — Target Knowledge Base

Scheda per ogni oggetto con tutte le osservazioni Digital StarGate, configurazioni, risultati, SQM, qualità, immagini, sessioni, processing workflow, problemi e benchmark storici.

## 9. BKL-036 — Observatory Health Score

Indicatore operativo spiegabile basato su freshness e qualità di telemetria, EAGLE, rete, power, servizi e pipeline. Non è un Safety Score.

## 10. BKL-037 — Session Comparison & Benchmarking

Confronto fra sessioni per FWHM, guiding RMS, SQM, background, integrazione, frame validi/scartati, temperatura, meteo, errori, workflow di post-produzione e qualità finale.

## 11. BKL-038 — Anomaly & Trend Center

Analisi storica di degradazioni progressive: guiding, autofocus, errori USB, network, EAGLE, camera, meteo, SQM e failure pattern.

## 12. BKL-039 — Equipment Performance Registry

Prestazioni per OTA/camera/filtro/focheggiatore/montatura con statistiche storiche e correlazione con SQM e condizioni ambientali.

## 13. BKL-040 — Night Timeline / Observatory Replay

Timeline sincronizzata N.I.N.A., PHD2, CloudWatcher, SQM, Power, Network, Safety, EAGLE health e session events, con replay temporale della notte.

## 14. BKL-041 — Scientific Data Quality Score

Indicatore separato dalla Safety per completezza metadata, lineage, frame, rejection, guiding, FWHM, background, SQM coverage, processing provenance e qualità scientifica della sessione.

## 15. BKL-042 — AI Observatory Assistant

Operational & Scientific Copilot basato su Knowledge Graph, documentazione, telemetria realtime, storico, log e catalogo scientifico.

Use case approvati:

- diagnosi read-only dello stato dell'osservatorio;
- major incident troubleshooting e timeline automatica;
- root cause analysis con evidence/confidence;
- predictive maintenance basata su trend osservati;
- change impact analysis prima di update/config change;
- Session Readiness Advisor;
- Observation Planner Assistant;
- historical analyst;
- equipment advisor;
- anomaly investigator;
- runbook assistant;
- configuration auditor / drift detection;
- knowledge assistant su architettura e sistema;
- scientific assistant;
- post-session analyst;
- incident pattern detector;
- what-if advisor;
- maintenance planner;
- evidence navigator.

### Boundary iniziale AI

Consentito: leggere telemetria, log, repository, storico; diagnosticare; correlare; raccomandare; preparare incident/RCA.

Non consentito nel primo rilascio: aprire/chiudere cupola, muovere montatura, commutare alimentazioni, modificare router, bypassare Safety o inviare comandi diretti ai device.

## 16. BKL-043 — Observatory Reliability Engineering

SLI/SLO e metriche: availability della telemetria, session completion rate, fault frequency, MTBF, MTTR, recovery time, notti perse per meteo vs guasti tecnici, failure budget e trend di affidabilità.

## 17. BKL-044 — Knowledge Graph / AI Evidence Contract

Estensione della foundation BKL-015 per garantire che AP, ADR, componenti, asset, sessioni, target, incident, evidence, telemetria, workflow PixInsight e recommendation AI siano collegabili con provenance e identificativi stabili.

## 18. BKL-045 — PixInsight Workflow Provenance Plugin

**Priorità proposta: P2, architettura da definire fin dalla foundation Knowledge Graph.**

### Obiettivo

Realizzare un'integrazione nativa per PixInsight che registri e storicizzi il workflow di post-produzione usato per trasformare i dati scientifici acquisiti nell'immagine finale, collegandolo alla sessione Digital StarGate di origine.

### Assessment architetturale iniziale

La fase di design deve scegliere il meccanismo di estensione PixInsight più appropriato e supportabile — modulo/plugin nativo o package script governato — senza assumere a priori una tecnologia specifica. La scelta deve privilegiare stabilità, compatibilità con gli aggiornamenti PixInsight e possibilità di catturare provenance in modo affidabile.

### Provenance minima da acquisire

- `processing_workflow_id` e versione schema;
- sessione/i scientifiche e file/input lineage;
- versione PixInsight e, quando disponibili, versioni di moduli/script coinvolti;
- processo/strumento utilizzato e ordine di esecuzione;
- parametri significativi del processo;
- timestamp e durata;
- immagini/input/output logici e loro identificativi/hash quando sostenibile;
- maschere, preview o reference image usate quando rilevanti e tecnicamente osservabili;
- trasformazioni lineari/non lineari e milestone del workflow;
- processi/plugin terzi dichiarati nel workflow;
- note manuali dell'astrofotografo per operazioni non catturabili automaticamente;
- metriche immagine pre/post processo quando disponibili e non invasive.

### Modello di persistenza

La provenance deve essere salvata in un formato machine-readable versionato, preferibilmente come sidecar governato e collegabile al Knowledge Graph. Quando tecnicamente sicuro e compatibile, potrà essere duplicata una reference minima nei metadata dell'immagine, ma il file immagine non deve diventare l'unica source of truth.

Il modello deve consentire:

```text
Scientific Session
   -> calibrated/integrated data
   -> Processing Workflow
       -> Processing Step 1
       -> Processing Step 2
       -> ...
   -> Final Image
```

### Requisiti

- nessun lock-in su una singola versione PixInsight;
- possibilità di registrare workflow parzialmente manuali;
- distinzione fra processo realmente osservato, processo dichiarato manualmente e processo suggerito dall'AI;
- correlazione con SQM, setup, session quality e target;
- possibilità di confrontare workflow diversi applicati allo stesso target/dataset;
- export/import di un workflow quando tecnicamente riproducibile;
- privacy/local-first per immagini e dati voluminosi.

## 19. BKL-046 — AI Post-Processing Assistant for PixInsight

**Dipendenze: BKL-015, BKL-044 e BKL-045.**

### Obiettivo

Integrare un assistente AI specializzato nella post-produzione che utilizzi la provenance PixInsight, le caratteristiche dell'immagine, il target, il setup, SQM/condizioni della notte e lo storico Digital StarGate per ottimizzare il workflow di elaborazione.

### Modalità iniziale

`ADVISORY ONLY`: l'assistente propone il prossimo processo, spiega perché, suggerisce intervalli di parametri e mostra evidence/comparazioni storiche. L'applicazione di un processo resta sotto controllo dell'utente.

### Use case

- analizzare lo stato corrente dell'immagine e suggerire il prossimo step;
- proporre workflow diversi per broadband, LRGB, SHO e OSC;
- confrontare il workflow corrente con elaborazioni storiche dello stesso target/setup;
- identificare step ridondanti o potenzialmente distruttivi;
- suggerire parameter range con motivazione, senza presentare il suggerimento come valore certo;
- correlare problemi di processing con qualità dei dati sorgenti, SQM, guiding e background;
- individuare quando un difetto non è correggibile in post-produzione perché deriva dall'acquisizione;
- generare una processing checklist riproducibile;
- documentare automaticamente decisioni, varianti e risultato finale;
- confrontare versioni A/B della stessa immagine;
- aiutare a ricostruire un workflow precedente;
- proporre ottimizzazioni sulla base dei risultati storici Digital StarGate;
- fornire un `confidence` e le evidence usate per ogni raccomandazione.

### Boundary AI

Nel primo rilascio l'AI non deve applicare autonomamente trasformazioni irreversibili. Un'eventuale modalità futura `ASSISTED APPLY` richiederà conferma umana per ogni gruppo di operazioni, rollback/checkpoint e registrazione completa della provenance.

## 20. Ordine proposto

```text
BKL-029 SQM integration
  -> BKL-030 EAGLE Health & Reliability
  -> BKL-015 Knowledge Graph foundation
  -> BKL-044 Knowledge/AI evidence contract
  -> BKL-035 Target Knowledge Base
  -> BKL-040 Night Timeline / Replay
  -> BKL-037 Session Comparison
  -> BKL-038 Anomaly & Trend Center
  -> BKL-039 Equipment Performance Registry
  -> BKL-041 Scientific Data Quality Score
  -> BKL-045 PixInsight Workflow Provenance Plugin
  -> BKL-046 AI Post-Processing Assistant
  -> BKL-031 Observation Planner
  -> BKL-032 Session Readiness
  -> BKL-036 Observatory Health Score
  -> BKL-033 Digital Twin
  -> BKL-034 Scientific Image Gallery
  -> BKL-042 AI Observatory Assistant
  -> BKL-043 Reliability Engineering
  -> BKL-014 / AP-015 Scientific Knowledge Platform
```

L'ordine potrà essere raffinato durante architecture review. BKL-029 è deliberatamente posto prima del Knowledge Graph perché SQM è già un gap reale della telemetria e diventerà un attributo fondamentale del modello scientifico futuro. BKL-045 e BKL-046 sono invece modellati già dalla foundation per evitare che processing provenance e AI post-processing vengano aggiunti come silos separati in una fase successiva.
