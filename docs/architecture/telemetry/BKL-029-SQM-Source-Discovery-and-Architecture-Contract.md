# BKL-029 — SQM Source Discovery and Architecture Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-029 |
| Capability | SQM Sky Quality Telemetry & Scientific History |
| Stato | **In Progress — architecture contract established; runtime source verification pending** |
| Data | 2026-08-30 |
| Autorità | Digital StarGate Architecture Office |
| Dipendenze | AP-004; AP-013; AP-014; Observatory Status; scientific session catalog |
| Runtime effect | None — documentation/architecture only |

## 1. Scopo

Definire la discovery governata della source SQM e il contratto architetturale per valorizzare realmente `weather.sqm_mag_arcsec2` e storicizzare la qualità del cielo nelle sessioni scientifiche.

BKL-029 non introduce alcun comando verso cupola, montatura, power, router o Safety Authority. SQM è una metrica scientifica di qualità della notte e **non è mai un Safety signal**.

## 2. Repository truth verificata

Alla baseline `main` verificata all'avvio di BKL-029:

- `scripts/telemetry/Export-NinaObservatoryStatus.ps1` espone già `weather.sqm_mag_arcsec2`, ma lo imposta esplicitamente a `$null`;
- il repository contiene evidence e session manifest relativi a CloudWatcher, ma non contiene evidence sufficiente a dimostrare che l'unità fisica installata esponga una misura SQM calibrata;
- non è presente nel repository evidence di una istanza ASCOM `ObservingConditions` configurata che implementi `SkyQuality`;
- non è presente evidence di un SQM dedicato installato e leggibile dall'EAGLE;
- `SkyQuality`, `brightness`, cloud cover, sky temperature e altri proxy non devono essere confusi tra loro.

Conclusione: **nessuna source SQM runtime è ancora VERIFIED**. Fino alla verifica, il valore operativo deve restare `null` e la semantica SQM deve degradare a `UNKNOWN`/`STALE` secondo il contratto sotto.

## 3. Candidate source discovery

### 3.1 ASCOM ObservingConditions — candidate preferita se già configurata

ASCOM definisce la proprietà read-only `ObservingConditions.SkyQuality` come sky quality misurata in magnitudini per arcsec². Questa interfaccia è semanticamente aderente al campo canonico Digital StarGate e consente un collector leggero sull'EAGLE.

La sola esistenza dello standard non prova che il driver installato a Manciano implementi la proprietà. Prima dell'uso devono essere verificati almeno:

1. ProgID/driver effettivamente configurato sull'EAGLE;
2. connessione read-only riuscita;
3. `SkyQuality` implementato senza `NotImplementedException`;
4. valore numerico plausibile e timestamp/cadence osservabili;
5. `SensorDescription("SkyQuality")` o metadata equivalenti quando disponibili;
6. nessun effetto collaterale di configurazione o command path.

Riferimento esterno di capability, non evidence runtime: <https://ascom-standards.org/library/html/P_ASCOM_Com_DriverAccess_ObservingConditions_SkyQuality.htm>.

### 3.2 Lunatico CloudWatcher — candidate se hardware/firmware reale supporta sky quality

La documentazione Lunatico corrente descrive CloudWatcher con sensore sky-quality grade e misura in mpsas; la documentazione firmware specifica inoltre che unità aggiornate con il sensore sky-quality possono produrre letture di sky quality.

Questa capability **non autorizza alcuna inferenza** sull'unità installata. Sono richieste evidence locali di modello/revisione, firmware, canale dati e campo SQM effettivamente prodotto.

Ordine di preferenza, se CloudWatcher risulta compatibile:

1. ASCOM ObservingConditions `SkyQuality` già configurato e verificato;
2. interfaccia nativa Lunatico read-only/documentata, se necessaria e verificata;
3. nessun parsing di brightness legacy come sostituto SQM.

Riferimenti esterni di capability, non evidence runtime:

- <https://lunaticoastro.com/aag-cloud-watcher/>
- <https://lunaticoastro.com/cloudwatcher-software-downloads.html>
- <https://lunaticoastro.com/cloudwatcher-moreinfo.html>

### 3.3 SQM dedicato — candidate alternativa

Un misuratore SQM dedicato può essere adottato se fisicamente presente e dotato di interfaccia read-only verificabile. Il repository corrente non documenta una simile unità installata; pertanto questa opzione resta `NOT VERIFIED`.

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

La preferenza architetturale è riusare una source standard read-only già installata; non si introduce una nuova dipendenza hardware o software solo per evitare la discovery.

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

- **G1 Source discovery:** almeno una source SQM `VERIFIED` oppure decisione esplicita di blocco se nessuna source esiste;
- **G2 Realtime contract:** `weather.sqm_mag_arcsec2` e provenance/freshness valorizzati da source reale, con test UNKNOWN/STALE;
- **G3 Historical contract:** statistiche start/end/min/max/mean/median, valid samples, temporal coverage, source e quality prodotte da campioni reali;
- **G4 Regression:** telemetry, session promotion/catalog e safety boundary senza regressioni;
- **G5 CI/docs:** gate applicabili e documentazione verdi con evidence GitHub reale;
- **G6 Runtime OAT:** evidence su EAGLE per cadence, freshness, disconnect/stale e almeno una sessione/campione scientifico correlabile.

## 9. Prossimo passo operativo governato

Eseguire su EAGLE una **SQM source inventory read-only** che:

1. enumera le istanze ASCOM ObservingConditions configurate senza modificarle;
2. verifica se la property `SkyQuality` è implementata e leggibile;
3. identifica versione/model/firmware CloudWatcher e l'eventuale campo SQM nativo senza cambiare configurazione;
4. rileva eventuali device SQM dedicati già presenti;
5. cattura campioni/timestamp/cadence solo dalla prima source reale verificabile;
6. produce un evidence bundle senza secret.

Solo dopo G1 si implementa l'adapter realtime. BKL-030 resta fuori scope e non deve iniziare prima della chiusura BKL-029.
