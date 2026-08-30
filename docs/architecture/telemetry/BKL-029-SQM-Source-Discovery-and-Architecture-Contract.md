# BKL-029 — SQM Source Discovery and Architecture Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-029 |
| Capability | SQM Sky Quality Telemetry & Scientific History |
| Stato | **Blocked — G1 source discovery completed; no verified runtime SQM source found on EAGLE30154** |
| Data | 2026-08-30 |
| Autorità | Digital StarGate Architecture Office |
| Dipendenze | AP-004; AP-013; AP-014; Observatory Status; scientific session catalog |
| Runtime effect | None — discovery/documentation only; no device configuration changes |

## 1. Scopo

Definire la discovery governata della source SQM e il contratto architetturale per valorizzare realmente `weather.sqm_mag_arcsec2` e storicizzare la qualità del cielo nelle sessioni scientifiche.

BKL-029 non introduce alcun comando verso cupola, montatura, power, router o Safety Authority. SQM è una metrica scientifica di qualità della notte e **non è mai un Safety signal**.

## 2. Repository truth verificata

Alla baseline `main` verificata all'avvio di BKL-029:

- `scripts/telemetry/Export-NinaObservatoryStatus.ps1` espone già `weather.sqm_mag_arcsec2`, ma lo imposta esplicitamente a `$null`;
- il repository contiene evidence e session manifest relativi a CloudWatcher, ma non contiene evidence sufficiente a dimostrare che l'unità fisica installata esponga una misura SQM calibrata;
- non era presente nel repository evidence di una istanza ASCOM `ObservingConditions` configurata che implementasse `SkyQuality`;
- non era presente evidence di un SQM dedicato installato e leggibile dall'EAGLE;
- `SkyQuality`, `brightness`, cloud cover, sky temperature e altri proxy non devono essere confusi tra loro.

Il runtime inventory eseguito su `EAGLE30154` il 2026-08-30 ha poi confermato:

- nessuna istanza ASCOM `ObservingConditions` rilevata;
- nessun campo SQM candidato rilevato nell'header/dati CloudWatcher osservati;
- nessun device SQM candidato rilevato via PnP/serial inventory;
- disposizione finale dello script: `NO_VERIFIED_SOURCE_FOUND`;
- bundle evidence runtime: `C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\`.

Conclusione corrente: **nessuna source SQM runtime è VERIFIED**. Il valore operativo deve restare `null`; non è ammessa alcuna stima sostitutiva. BKL-029 è bloccato prima di G2 finché non viene resa disponibile una sorgente strumentale reale o installata una nuova sorgente governata.

## 3. Candidate source discovery

### 3.1 ASCOM ObservingConditions — candidate preferita se già configurata

ASCOM definisce la proprietà read-only `ObservingConditions.SkyQuality` come sky quality misurata in magnitudini per arcsec². Questa interfaccia è semanticamente aderente al campo canonico Digital StarGate e consente un collector leggero sull'EAGLE.

L'inventory del 2026-08-30 non ha trovato istanze `ObservingConditions` registrate sull'EAGLE. Pertanto questa candidate è attualmente `NOT AVAILABLE` nel runtime osservato.

Se in futuro viene installato/configurato un driver, prima dell'uso devono essere verificati almeno:

1. ProgID/driver effettivamente configurato sull'EAGLE;
2. connessione read-only riuscita;
3. `SkyQuality` implementato senza `NotImplementedException`;
4. valore numerico plausibile e timestamp/cadence osservabili;
5. `SensorDescription("SkyQuality")` o metadata equivalenti quando disponibili;
6. nessun effetto collaterale di configurazione o command path.

Riferimento esterno di capability, non evidence runtime: <https://ascom-standards.org/library/html/P_ASCOM_Com_DriverAccess_ObservingConditions_SkyQuality.htm>.

### 3.2 Lunatico CloudWatcher — candidate se hardware/firmware reale supporta sky quality

La documentazione Lunatico corrente descrive CloudWatcher con sensore sky-quality grade e misura in mpsas; la documentazione firmware specifica inoltre che unità aggiornate con il sensore sky-quality possono produrre letture di sky quality.

L'inventory runtime del 2026-08-30 non ha trovato nell'output CloudWatcher osservato alcun campo identificabile come SQM/sky quality/mpsas. Questa evidence non dimostra l'assenza fisica del sensore nell'hardware, ma dimostra che **l'attuale canale CSV osservato non espone una misura SQM utilizzabile**.

Questa capability esterna non autorizza alcuna inferenza sull'unità installata. Per riaprire la candidate sono richieste evidence locali di modello/revisione, firmware, canale dati e campo SQM effettivamente prodotto.

Ordine di preferenza, se CloudWatcher risulta compatibile in futuro:

1. ASCOM ObservingConditions `SkyQuality` verificato;
2. interfaccia nativa Lunatico read-only/documentata, se necessaria e verificata;
3. nessun parsing di brightness legacy come sostituto SQM.

Riferimenti esterni di capability, non evidence runtime:

- <https://lunaticoastro.com/aag-cloud-watcher/>
- <https://lunaticoastro.com/cloudwatcher-software-downloads.html>
- <https://lunaticoastro.com/cloudwatcher-moreinfo.html>

### 3.3 SQM dedicato — candidate alternativa

Un misuratore SQM dedicato può essere adottato se fisicamente presente e dotato di interfaccia read-only verificabile. L'inventory PnP/seriale del 2026-08-30 non ha rilevato un device nominato o identificabile come SQM/Unihedron/sky-quality. Questa candidate è quindi attualmente `NOT AVAILABLE` nel runtime osservato.

### 3.4 Proxy esplicitamente vietati

Non è consentito produrre `sqm_mag_arcsec2` da:

- brightness condition o valori light non calibrati come SQM;
- cloud cover;
- sky temperature;
- Moon altitude/phase;
- trasparenza stimata;
- immagini o background fotografico, salvo futura capability scientifica distinta e governata che non impersoni una misura strumentale SQM.

## 4. Source selection gate

Una source può passare a `VERIFIED` solo con evidence runtime riproducibile che registri almeno:

- computer/source instance;
- device/driver identity e versione quando disponibili;
- interfaccia usata;
- unità `mag/arcsec²` / mpsas;
- campioni reali con UTC timestamp;
- cadence osservata;
- comportamento in assenza/disconnessione/source error;
- assenza di command path operativo;
- disposizione finale `VERIFIED`, `REJECTED` o `NOT AVAILABLE`.

Per il runtime inventory del 2026-08-30 la disposizione governata è:

- ASCOM ObservingConditions: `NOT AVAILABLE`;
- CloudWatcher CSV SQM field: `NOT AVAILABLE` nel canale osservato;
- SQM dedicato: `NOT AVAILABLE` nell'inventory osservato;
- source SQM complessiva: `NO_VERIFIED_SOURCE_FOUND`.

La preferenza architetturale resta riusare una source standard read-only già installata; una nuova dipendenza hardware/software richiede decisione esplicita e nuovo evidence cycle.

## 5. Contratto realtime

Il valore canonico resta:

```text
weather.sqm_mag_arcsec2: number | null
```

Poiché SQM può avere una source e una cadence diverse dagli altri segnali weather, BKL-029 richiede provenance field-level. Il target contract deve rendere disponibili, direttamente o tramite un oggetto SQM versionato equivalente:

```text
sqm_mag_arcsec2
sqm_observed_at_utc
sqm_fresh_until_utc
sqm_quality        CURRENT | STALE | UNKNOWN
sqm_source
```

Regole:

1. `sqm_mag_arcsec2` è numerico solo quando deriva da una misura strumentale verificata;
2. source non disponibile o property non implementata -> valore `null`, quality `UNKNOWN`;
3. ultimo campione oltre freshness -> valore operativo non affidabile, quality `STALE` e nessuna promozione implicita a CURRENT;
4. freshness viene fissata dopo misura della cadence reale; baseline di progetto: almeno `2 x` il worst observed normal update interval, con margine validato in OAT;
5. timestamp della projection generale non sostituisce il timestamp del campione SQM quando le source differiscono;
6. il portale deve visualizzare assenza/staleness senza inventare un valore;
7. SQM non modifica `safety.observed_state`, interlock o decisioni della Safety Authority.

Nel runtime corrente, non essendo disponibile una source verificata, l'unico comportamento conforme è mantenere `sqm_mag_arcsec2 = null` e non avviare G2.

## 6. Contratto storico scientifico

Per ogni sessione con campioni SQM validi il catalogo/session manifest deve poter rappresentare almeno:

```text
sqm.start
sqm.end
sqm.min
sqm.max
sqm.mean
sqm.median
sqm.valid_samples
sqm.temporal_coverage
sqm.source
sqm.quality
```

Vincoli:

- statistiche calcolate solo da campioni validi e temporalmente attribuibili alla sessione;
- `temporal_coverage` deve descrivere la copertura effettiva della finestra scientifica, non la sola presenza di almeno un campione;
- source/provenance devono consentire di risalire al collector e alla source strumentale;
- una sessione priva di SQM resta scientificamente valida: i campi SQM risultano assenti/UNKNOWN e non vengono sintetizzati;
- eventuali cambi di source durante una sessione devono essere preservati come provenance o produrre quality degradato secondo il contratto di aggregazione che sarà implementato.

## 7. Boundary e responsabilità

### EAGLE

Consentito:

- discovery read-only;
- campionamento leggero;
- normalizzazione minima e timestamp;
- spool locale resiliente se necessario.

Non consentito:

- analytics pesanti;
- inferenza SQM da proxy;
- modifica configurazione del weather system come effetto collaterale della lettura;
- uso di SQM per comandare apparati o Safety.

### Repository / Scientific Data Engine

Responsabile di:

- schema/provenance versionati;
- associazione campioni-sessione;
- statistiche storiche;
- projection per portale/catalogo;
- validazioni anti-drift e fail-safe.

## 8. Acceptance gates BKL-029

BKL-029 non può essere marcato `Done` finché non esistono evidence reali per tutti i gate applicabili:

- **G1 Source discovery:** **COMPLETED WITH BLOCK** — inventory read-only eseguito su `EAGLE30154`; nessuna source SQM verificata trovata; disposition `NO_VERIFIED_SOURCE_FOUND`;
- **G2 Realtime contract:** `BLOCKED` — nessuna source reale da collegare a `weather.sqm_mag_arcsec2`;
- **G3 Historical contract:** `BLOCKED` — nessun campione SQM reale disponibile;
- **G4 Regression:** non eseguito per implementazione runtime SQM, perché nessuna implementazione è stata autorizzata dopo G1;
- **G5 CI/docs:** da verificare sul commit che registra questa evidence; nessun successo viene assunto senza GitHub evidence reale;
- **G6 Runtime OAT:** `BLOCKED` — richiede una source strumentale reale.

## 9. Evidenza runtime 2026-08-30

Comando eseguito sull'EAGLE:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\telemetry\Inspect-SqmTelemetrySources.ps1
```

Esito osservato:

```text
Computer: EAGLE30154
ASCOM probe requested: False
ASCOM OBSERVING CONDITIONS CANDIDATES: none found
CLOUDWATCHER SQM CANDIDATE FIELDS: none found
PNP / SERIAL CANDIDATES: no named SQM candidates found via PnP
SOURCE DISPOSITION: NO_VERIFIED_SOURCE_FOUND
Evidence JSON: C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\sqm-source-inventory.json
Evidence TXT : C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\sqm-source-inventory.txt
SQM SOURCE INVENTORY RESULT: PASS (inventory/probe status recorded; not BKL-029 acceptance)
```

Lo script è stato eseguito senza `-ProbeAscomSkyQuality`; pertanto non è stata aperta alcuna connessione device ASCOM durante questo inventory.

## 10. Prossimo passo governato

BKL-029 resta bloccato fino a una decisione esplicita su una delle seguenti opzioni:

1. verificare modello/revisione/firmware del CloudWatcher installato per stabilire se possiede realmente il sensore sky-quality ma non lo espone nel CSV corrente;
2. verificare se esiste un'interfaccia Lunatico nativa read-only che espone SQM sull'unità installata;
3. installare/configurare una source ASCOM ObservingConditions che fornisca `SkyQuality`, se supportata dal dispositivo reale;
4. introdurre un SQM dedicato con interfaccia read-only governata.

Fino a quella decisione:

- `weather.sqm_mag_arcsec2` resta `null`;
- nessun proxy viene introdotto;
- nessun adapter realtime SQM viene implementato;
- BKL-030 non viene avviato per aggirare questo gate.
