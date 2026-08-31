# BKL-030 — EAGLE Health & Reliability Architecture Assessment

| Campo | Valore |
|---|---|
| Identificativo | BKL-030 |
| Stato | **Planning only — implementation blocked until BKL-029 closure** |
| Data | 2026-08-31 |
| Priorità | P1 |
| Target | EAGLE30154 / Digital StarGate Observatory Status |
| Dipendenza bloccante | BKL-029 |

## 1. Scopo

Preparare il contratto architetturale e il source-discovery plan per la capability **EAGLE Health & Reliability Telemetry**, senza anticiparne l'implementazione prima della chiusura formale di BKL-029.

La capability deve produrre health observability spiegabile del computer operativo EAGLE, mantenendo separati:

- health del computer;
- stato degli apparati astronomici;
- Safety Authority locale;
- Observatory Health Score futuro (BKL-036);
- analytics/AI futuri.

BKL-030 non autorizza alcun comando verso cupola, montatura, power, router o altri apparati.

## 2. Repository truth e vincolo di sequenza

Il backlog canonico mantiene:

```text
BKL-029 -> BKL-030 -> BKL-015 -> BKL-044
```

BKL-030 resta `Planned` finché BKL-029 non è formalmente chiuso. Questo documento è quindi un package di planning/discovery e non modifica lo stato della milestone.

## 3. Decisione di boundary proposta

### 3.1 Non integrare l'intero BKL-030 nel plugin N.I.N.A.

Il plugin Digital StarGate N.I.N.A. resta il boundary appropriato per telemetry vicina al runtime N.I.N.A. e agli adapter già commissionati (dome/mount/camera/weather, Power, Network, SQM, Safety observation).

BKL-030 richiede invece accesso a sorgenti host-level come:

- Windows Event Log;
- filesystem e storage;
- process inventory;
- Windows Scheduled Tasks;
- registry/update state;
- time service / clock synchronization;
- SMART/storage health;
- USB/COM error evidence;
- configuration drift;
- pending reboot/update state.

Caricare queste responsabilità nel processo N.I.N.A. aumenterebbe:

- failure surface del software di acquisizione;
- privilegi richiesti al plugin;
- latenza potenziale nel processo N.I.N.A.;
- dipendenza da API Windows non necessarie al dominio astronomico;
- blast radius di errori del collector health.

### 3.2 Target boundary

La direzione proposta è un **lightweight EAGLE Host Health Collector**, separato da N.I.N.A., read-only e fail-safe.

```mermaid
flowchart LR
    WIN[Windows host sources] --> HC[EAGLE Host Health Collector]
    NINA[N.I.N.A. Telemetry Plugin] --> HB[Plugin heartbeat evidence]
    HB --> HC
    HC --> HP[eagle-health.json]
    HP --> CANON[Canonical Observatory Status Adapter]
    CANON --> PORTAL[Observatory Status]

    SAFETY[Local Physical Safety Authority]
    HC -. no authority / no command .-> SAFETY
```

Il collector deve limitarsi a raccogliere evidence host-side e produrre una projection locale machine-readable. Qualsiasi trend analysis, prediction, Health Score, anomaly detection o AI deve restare downstream e fuori dall'EAGLE quando possibile.

## 4. Source inventory previsto

| Area | Source candidate | Modalità | Note |
|---|---|---|---|
| Disk free/capacity | CIM `Win32_LogicalDisk` / filesystem | read-only | Source primaria prevista |
| Disk trend | history downstream dei campioni | derived | Non calcolare trend pesanti sull'EAGLE |
| RAM | CIM / performance counters | read-only | Available/commit/pressure evidence |
| CPU | performance counters / CIM | read-only | Media/picchi con finestra leggera |
| Uptime | OS boot time | read-only | Baseline per reboot detection |
| Hardware temperature | WMI/vendor source se realmente disponibile | read-only | `UNKNOWN` se non verificabile |
| SMART | `Get-PhysicalDisk`, storage reliability counters o vendor source | read-only | Nessun test distruttivo |
| I/O | small bounded write/read/delete probe in DSG working dir | non-destructive | Mai usare volumi immagine come benchmark aggressivo |
| Time sync | `w32tm /query /status` / Windows Time | read-only | State, source, offset se disponibile |
| System/Application Event Log | Windows Event Log | read-only | Aggregazione bounded Critical/Error |
| N.I.N.A. process | process table + plugin projection freshness | read-only | Nessun restart automatico |
| PHD2 process | process table/log freshness | read-only | Nessun restart automatico |
| ASCOM LocalServer | process/service inventory | read-only | Solo processi verificati |
| DSG components | producer files/process/task state | read-only | Heartbeat/freshness |
| Scheduled Tasks | Task Scheduler read API | read-only | Stato/LastTaskResult/NextRun |
| N.I.N.A./PHD2/CloudWatcher logs | filesystem metadata | read-only | Existence + last write time |
| USB/COM errors | Event Log + device inventory | read-only | Pattern evidence, niente reset device |
| Pending reboot | registry keys documented/verified | read-only | `UNKNOWN` se source non deterministica |
| Windows Update | Windows Update state/API if accessible read-only | read-only | Nessun update trigger |
| Configuration drift | governed baseline manifest vs observed versions/hashes | read-only | Drift evidence, non auto-remediation |

## 5. Contratto di projection locale proposto

File target indicativo:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json
```

Schema di principio:

```json
{
  "schema_version": "1.0",
  "component": "DSG.EagleHostHealthCollector",
  "computer": "EAGLE30154",
  "observed_at_utc": "...",
  "fresh_until_utc": "...",
  "quality": "CURRENT | STALE | UNKNOWN",
  "summary": {
    "state": "HEALTHY | DEGRADED | CRITICAL | UNKNOWN",
    "reasons": []
  },
  "signals": {
    "storage": {},
    "memory": {},
    "cpu": {},
    "uptime": {},
    "time_sync": {},
    "event_log": {},
    "processes": {},
    "scheduled_tasks": {},
    "log_sources": {},
    "usb_com": {},
    "pending_reboot": {},
    "configuration_drift": {}
  }
}
```

Il dettaglio finale dello schema deve essere definito solo dopo source discovery reale su `EAGLE30154`.

## 6. Health state: regole di governance

`HEALTHY / DEGRADED / CRITICAL / UNKNOWN` deve essere **spiegabile**.

Regole obbligatorie:

1. nessun unico numero opaco come source of truth;
2. ogni stato non-HEALTHY deve indicare le evidence/reasons che lo determinano;
3. `UNKNOWN` quando una source obbligatoria non è osservabile o è stale;
4. nessuna soglia hardware inventata: threshold e severity devono provenire da policy documentata o evidence operativa;
5. valori quantitativi raw devono essere preservati separatamente dalla classificazione;
6. BKL-036 potrà in futuro costruire un Observatory Health Score downstream, ma non modifica il contratto BKL-030;
7. nessuno stato health può autorizzare operazioni Safety.

## 7. Collection cadence proposta

La cadence non viene ancora fissata come acceptance.

Principio:

- segnali economici (CPU/RAM/storage/process heartbeat): polling leggero nell'ordine delle decine di secondi/minuti;
- Event Log, Scheduled Tasks, update/reboot/drift: scansioni meno frequenti;
- SMART e I/O probe: frequenza bassa e bounded;
- analytics/trend: downstream.

La cadence finale deve essere misurata in pilot verificando overhead CPU/RAM/I/O sull'EAGLE durante N.I.N.A. attivo.

## 8. Safety e security boundary

Il collector è strettamente read-only salvo il bounded I/O self-test sulla sola working directory Digital StarGate.

Vietato:

- kill/restart automatico di N.I.N.A./PHD2/ASCOM;
- reset USB/COM;
- riavvio Windows;
- installazione Windows Update;
- modifica Scheduled Tasks;
- modifica registry/config;
- cambio power/network;
- uso health state come Safety Authority.

Credenziali o segreti non devono essere copiati nella projection.

## 9. Source-discovery gates

Prima di implementare la capability:

### D1 — Host baseline inventory

Verificare realmente su EAGLE30154:

- Windows edition/build;
- storage topology;
- memory/CPU identifiers;
- availability SMART/reliability counters;
- Windows Time source;
- relevant Task Scheduler entries;
- N.I.N.A./PHD2/ASCOM/DSG process names;
- relevant Event Log providers;
- directory/log locations;
- pending reboot sources;
- update-state visibility;
- USB/COM inventory.

### D2 — Privilege assessment

Per ogni source verificare se è leggibile come utente operativo `PrimaLuceLab` senza elevazione. Le source che richiedono privilegi amministrativi devono essere isolate e giustificate; la baseline preferisce funzionamento non elevato.

### D3 — Overhead pilot

Misurare overhead collector mentre N.I.N.A. è attivo:

- CPU;
- working set;
- I/O;
- latency;
- failures/timeouts.

### D4 — Failure model

Verificare almeno:

- source non disponibile -> `UNKNOWN`, non valore sintetico;
- collector fermo -> projection stale;
- Event Log access denied -> solo relativo signal `UNKNOWN`;
- SMART non disponibile -> `UNKNOWN`, capability non bloccata se non mandatory;
- malformed source -> evidence diagnostica, niente crash loop.

## 10. Acceptance plan BKL-030

Proposta di gate, da attivare solo dopo chiusura BKL-029:

- **G1 Source inventory:** tutte le source candidate classificate `VERIFIED / UNAVAILABLE / REJECTED`;
- **G2 Contract:** projection e field provenance definiti;
- **G3 Collector:** lightweight collector implementato con bounded work;
- **G4 CI:** lint/build/test applicabili GREEN;
- **G5 Runtime OAT:** EAGLE30154 nominal/failure/recovery;
- **G6 History:** campioni conservati downstream per trend/capacity;
- **G7 Portal:** Observatory Status mostra EAGLE health e reasons;
- **G8 Safety review:** nessun command path e separazione Safety verificata.

## 11. Open questions da risolvere nel discovery

1. SMART/reliability counters sono esposti in modo utile sull'hardware EAGLE3?
2. Esiste una temperatura CPU/hardware verificabile senza software/vendor driver invasivo?
3. Quale Windows Time source è attivo e quale offset è esposto realmente?
4. Quali Event Log provider identificano crash N.I.N.A., PHD2 e ASCOM in modo affidabile?
5. Quale baseline governata usare per configuration drift: file manifest, hash/version inventory o entrambi?
6. Quali Scheduled Tasks DSG sono realmente presenti sul computer corrente?
7. Pending reboot/update state è leggibile in modo affidabile senza elevation?
8. Quale retention dei raw health samples è sostenibile localmente prima del relay downstream?

## 12. Prossimo passo consentito prima della chiusura BKL-029

È consentito preparare e revisionare un **read-only discovery script** che raccolga esclusivamente metadata e capability availability, ma non deve essere commissionato come producer né modificare `BKL-030` da `Planned` a `In Progress` prima della chiusura di BKL-029.

Il primo runtime step, quando BKL-029 sarà chiuso, sarà D1/D2: inventory source/privilege su `EAGLE30154`.
