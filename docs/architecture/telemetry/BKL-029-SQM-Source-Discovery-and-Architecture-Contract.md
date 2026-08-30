# BKL-029 — SQM Source Discovery and Architecture Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-029 |
| Capability | SQM Sky Quality Telemetry & Scientific History |
| Stato | **In progress — verified ASCOM ObservingConditions source candidate; runtime SkyQuality read pending** |
| Data | 2026-08-30 |
| Autorità | Digital StarGate Architecture Office |
| Dipendenze | AP-004; AP-013; AP-014; Observatory Status; scientific session catalog |
| Runtime effect | None — discovery/documentation only; no device configuration changes |

## 1. Scopo

Definire la discovery governata della source SQM e il contratto architetturale per valorizzare realmente `weather.sqm_mag_arcsec2` e storicizzare la qualità del cielo nelle sessioni scientifiche.

BKL-029 non introduce alcun comando verso cupola, montatura, power, router o Safety Authority. SQM è una metrica scientifica di qualità della notte e **non è mai un Safety signal**.

## 2. Repository truth ed evidence runtime

La baseline iniziale mostrava `weather.sqm_mag_arcsec2 = $null`, nessuna evidence sufficiente di SQM calibrato dal CloudWatcher, nessuna istanza ASCOM `ObservingConditions` verificata e nessun SQM dedicato.

Il primo inventory runtime su `EAGLE30154`, bundle `C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\`, aveva rilevato:

- nessuna istanza ASCOM `ObservingConditions` tra i ProgID allora ricercati;
- nessun campo SQM candidato nel CSV CloudWatcher osservato;
- nessun device SQM candidato via PnP/serial;
- disposition `NO_VERIFIED_SOURCE_FOUND`.

Quella conclusione ASCOM era incompleta: la discovery successiva ha identificato il ProgID reale `ASCOM.CloudWatcher.ObservingConditions`, non incluso nei candidati iniziali.

Il secondo inventory passivo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-capability-20260830-182202\`, ha rilevato:

- `AAG CloudWatcher v.9.5.0`, versione `9.5.0`, publisher Lunático Astronomía, install location `C:\Program Files (x86)\AAG_CloudWatcher\`;
- `AAG_WeatherCenter v2.30` installato;
- ProgID legacy `AAG_CloudWatcher.CloudWatcher` registrato;
- `ASCOM.AAGCloudWatcher.ObservingConditions` non registrato;
- `ASCOM.Lunatico.ObservingConditions` non registrato;
- nessun file passivamente rilevato con metadata SQM;
- nessun file passivamente rilevato con metadata firmware;
- disposition `NO_PASSIVE_SQM_OR_FIRMWARE_METADATA_FOUND`.

Il terzo inventory passivo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-legacy-com-surface-20260830-183012\`, ha caratterizzato il ProgID legacy senza attivarlo:

- ProgID `AAG_CloudWatcher.CloudWatcher` registrato;
- CLSID `{F8D7A9ED-D0E2-45F8-BAC6-88DBB322475B}`;
- nessun `InprocServer32` o `LocalServer32` risolto dalla registrazione osservata;
- nessuna TypeLib associata a quel percorso di registrazione legacy;
- nessun termine SQM/sky-quality/mpsas nella metadata surface passivamente visibile;
- disposition `LEGACY_COM_REGISTERED_NO_SQM_TERM_FOUND_IN_PASSIVE_METADATA`.

Il quarto inventory passivo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-hardware-firmware-inventory-20260830-183508\`, ha rilevato:

- `AAG_CloudWatcher.exe` file/product version `9.05`;
- altri componenti Lunatico/AAG locali, incluso `AAG_ACPWeatherFeed.exe` 7.20 e `AAG_HASFileLoader.exe` 2.22;
- nessun metadata locale di modello, seriale, revisione hardware o firmware dispositivo;
- nessun metadata locale SQM/mpsas;
- disposition `NO_LOCAL_HARDWARE_FIRMWARE_OR_SQM_METADATA_FOUND`.

Il preflight protocollo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-protocol-probe-20260830-190848\`, ha rilevato:

- nessuna porta enumerata tramite `Win32_SerialPort`;
- `AAG_CloudWatcher.exe` in esecuzione;
- `ASCOM.CloudWatcher.Server.exe` in esecuzione;
- nessuna porta seriale aperta dal probe;
- disposition `PREFLIGHT_ONLY_NO_SERIAL_ACCESS`.

Questa evidence ha spostato la discovery verso la superficie ASCOM già attiva, evitando contesa seriale.

L'inventory ASCOM passivo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-surface-20260830-192856\`, ha identificato la source candidata determinante:

- ProgID `ASCOM.CloudWatcher.ObservingConditions` registrato;
- CLSID `{efef952b-d34c-4d25-bdbf-0a0a58a2414e}`;
- server multi-interface `ASCOM.CloudWatcher.Server.exe` registrato e in esecuzione;
- ProgID `ASCOM.CloudWatcher.SafetyMonitor` distinto, quindi il boundary Safety resta separato;
- interfacce ASCOM `IObservingConditions` / `IObservingConditionsV2` presenti nella registrazione;
- OCH/ASCOM mapping include `SkyQuality` per la source CloudWatcher;
- nessuna attivazione ASCOM eseguita durante l'inventory.

Il preflight dedicato SkyQuality, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-skyquality-20260830-193734\`, ha confermato:

- `ASCOM.CloudWatcher.ObservingConditions` registrato in HKCR;
- driver registrato come `Lunatico CloudWatcher Observing Conditions`;
- `DataFile = C:\Users\PrimaLuceLab\Documents\aag_json.dat`;
- `MaxSecsDiff = 60`;
- `AAG_CloudWatcher.exe` e `ASCOM.CloudWatcher.Server.exe` attivi;
- nessuna istanziazione ASCOM, nessuna connessione, nessun accesso seriale diretto;
- disposition `PREFLIGHT_ONLY_NO_ASCOM_ACTIVATION`.

Conclusione corrente: esiste una source ASCOM ObservingConditions reale e configurata, ma `SkyQuality` non è ancora stato letto a runtime. `weather.sqm_mag_arcsec2` resta quindi `null` fino alla singola lettura controllata e alla validazione di plausibilità/freshness.

## 3. Candidate source discovery

### 3.1 ASCOM ObservingConditions

Candidate corrente: `VERIFIED REGISTRATION / RUNTIME VALUE PENDING`.

La source selezionata per il prossimo gate è:

```text
ProgID: ASCOM.CloudWatcher.ObservingConditions
Driver: Lunatico CloudWatcher Observing Conditions
DataFile: C:\Users\PrimaLuceLab\Documents\aag_json.dat
MaxSecsDiff: 60
```

ASCOM `ObservingConditions.SkyQuality` è semanticamente adatto a una misura in magnitudini per arcsec². Il server è già attivo e consente di evitare accesso seriale diretto concorrente.

Il prossimo probe deve leggere solo metadata ASCOM e `SkyQuality`, senza chiamare SafetyMonitor e senza accesso seriale diretto.

### 3.2 Lunatico CloudWatcher native protocol

Il protocollo seriale diretto resta una fallback diagnostic path e non è più il percorso preferito finché la source ASCOM è disponibile.

La documentazione Lunatico pubblica indica che:

- i CloudWatcher recenti includono un sensore sky-quality e misurano in mpsas;
- per unità aggiornate con sensore sky-quality grade è disponibile firmware 5.8.9 con sky-quality readings;
- il protocollo seriale v1.4 documenta il blocco `!8` come raw frequency del nuovo light sensor, da convertire in MPSAS dal software Windows/SOLO;
- il blocco `!4` rimane un LDR voltage stimato per backward compatibility e non è una source SQM valida.

Il direct serial probe non viene eseguito mentre il percorso ASCOM può soddisfare G1 senza contesa sulla porta.

### 3.3 SQM dedicato

L'inventory PnP/seriale non ha rilevato un device identificabile come SQM/Unihedron/sky-quality. Candidate corrente: `NOT AVAILABLE`.

### 3.4 Proxy vietati

Non è consentito produrre `sqm_mag_arcsec2` da brightness/LDR non calibrato come SQM, cloud cover, sky temperature, Moon altitude/phase, trasparenza stimata o background fotografico.

## 4. Source selection gate

Una source passa a `VERIFIED` per uso realtime solo con evidence runtime riproducibile di identity/versione, interfaccia, unità mpsas, campioni reali UTC, freshness, error behavior e provenance.

Disposizione corrente:

- ASCOM CloudWatcher ObservingConditions: `REGISTERED / CONFIGURED / SKYQUALITY READ PENDING`;
- CloudWatcher CSV SQM field: `NOT AVAILABLE` nel canale CSV osservato;
- CloudWatcher legacy COM: `REGISTERED / PASSIVE SURFACE NON-DESCRIPTIVE`;
- CloudWatcher direct serial protocol: `FALLBACK / NOT PROBED`;
- SQM dedicato: `NOT AVAILABLE`;
- source SQM complessiva: `CANDIDATE SOURCE VERIFIED; VALUE NOT YET VERIFIED`.

## 5. Contratto realtime

Il valore canonico resta:

```text
weather.sqm_mag_arcsec2: number | null
```

Il target richiede provenance field-level:

```text
sqm_mag_arcsec2
sqm_observed_at_utc
sqm_fresh_until_utc
sqm_quality        CURRENT | STALE | UNKNOWN
sqm_source
```

Regole:

1. valore numerico solo da misura strumentale verificata;
2. source assente/non implementata -> `null`, quality `UNKNOWN`;
3. campione oltre freshness -> `STALE`;
4. per il driver corrente `MaxSecsDiff=60` è evidence di configurazione, non ancora automaticamente la freshness canonica DSG;
5. freshness DSG viene fissata dopo verifica di `TimeSinceLastUpdate('SkyQuality')` e cadence reale;
6. timestamp projection generale non sostituisce timestamp SQM;
7. il portale visualizza assenza/staleness senza inventare valori;
8. SQM non modifica Safety Authority o interlock.

Nel runtime corrente `sqm_mag_arcsec2` resta `null` fino al probe SkyQuality.

## 6. Contratto storico scientifico

Per sessioni con campioni SQM validi il catalogo deve poter rappresentare almeno:

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

Le statistiche usano solo campioni validi e temporalmente attribuibili; la provenance deve essere preservata. Una sessione priva di SQM resta valida e non riceve valori sintetici.

## 7. Boundary e responsabilità

### EAGLE

Consentito: discovery read-only, lettura ASCOM `ObservingConditions.SkyQuality`, campionamento leggero, normalizzazione minima/timestamp e spool locale resiliente se necessario.

Vietato: analytics pesanti, inferenza SQM da proxy, modifica configurazione weather come effetto collaterale, uso SQM per Safety o command path.

### Safety boundary

`ASCOM.CloudWatcher.SafetyMonitor` è un'interfaccia separata e non viene usata da BKL-029. Nessun test SQM deve invocarla o alterarne comportamento/stato.

### Repository / Scientific Data Engine

Responsabile di schema/provenance versionati, associazione campioni-sessione, statistiche storiche, projection portale/catalogo e validazioni anti-drift/fail-safe.

## 8. Acceptance gates BKL-029

- **G1 Source discovery:** `NEAR COMPLETE` — source ASCOM reale identificata/configurata; manca una lettura SkyQuality runtime riuscita;
- **G2 Realtime contract:** `BLOCKED ON RUNTIME SAMPLE` — schema definito, source candidate disponibile;
- **G3 Historical contract:** `BLOCKED` — nessun campione SQM reale ancora acquisito;
- **G4 Regression:** non eseguito per runtime SQM perché l'adapter production non è ancora implementato;
- **G5 CI/docs:** da verificare sui commit; nessun successo assunto senza evidence GitHub reale;
- **G6 Runtime OAT:** `BLOCKED ON RUNTIME SAMPLE`.

## 9. Evidence runtime 2026-08-30

### 9.1 Inventory generale SQM

```text
Computer: EAGLE30154
ASCOM OBSERVING CONDITIONS CANDIDATES: none found among the initial candidate ProgIDs
CLOUDWATCHER SQM CANDIDATE FIELDS: none found
PNP / SERIAL CANDIDATES: no named SQM candidates found via PnP
SOURCE DISPOSITION: NO_VERIFIED_SOURCE_FOUND (superseded for ASCOM discovery by later evidence)
Evidence: C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\
```

### 9.2 CloudWatcher passive capability inventory

```text
AAG CloudWatcher v.9.5.0 / 9.5.0 / Lunático Astronomía
AAG_WeatherCenter v2.30
DISPOSITION: NO_PASSIVE_SQM_OR_FIRMWARE_METADATA_FOUND
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-capability-20260830-182202\
```

### 9.3 Legacy COM passive surface

```text
ProgID: AAG_CloudWatcher.CloudWatcher
CLSID: {F8D7A9ED-D0E2-45F8-BAC6-88DBB322475B}
DISPOSITION: LEGACY_COM_REGISTERED_NO_SQM_TERM_FOUND_IN_PASSIVE_METADATA
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-legacy-com-surface-20260830-183012\
```

### 9.4 Hardware / firmware local metadata inventory

```text
AAG_CloudWatcher.exe: file_version=9.05 product_version=9.05
HARDWARE / FIRMWARE METADATA entries: 0
SQM METADATA entries: 0
DISPOSITION: NO_LOCAL_HARDWARE_FIRMWARE_OR_SQM_METADATA_FOUND
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-hardware-firmware-inventory-20260830-183508\
```

### 9.5 Serial protocol preflight

```text
Win32_SerialPort candidates: none enumerated
AAG_CloudWatcher.exe: running
ASCOM.CloudWatcher.Server.exe: running
Port opened: False
DISPOSITION: PREFLIGHT_ONLY_NO_SERIAL_ACCESS
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-protocol-probe-20260830-190848\
```

### 9.6 ASCOM surface inventory

```text
ASCOM.CloudWatcher.ObservingConditions: registered
CLSID: {efef952b-d34c-4d25-bdbf-0a0a58a2414e}
ASCOM.CloudWatcher.SafetyMonitor: separately registered
ASCOM.CloudWatcher.Server.exe: running
IObservingConditions / IObservingConditionsV2: registered interfaces
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-surface-20260830-192856\
```

### 9.7 ASCOM SkyQuality preflight

```text
ProgID: ASCOM.CloudWatcher.ObservingConditions
Driver: Lunatico CloudWatcher Observing Conditions
DataFile: C:\Users\PrimaLuceLab\Documents\aag_json.dat
MaxSecsDiff: 60
AAG_CloudWatcher.exe: running
ASCOM.CloudWatcher.Server.exe: running
ASCOM object created: False
Serial access: False
DISPOSITION: PREFLIGHT_ONLY_NO_ASCOM_ACTIVATION
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-skyquality-20260830-193734\
```

## 10. Prossimo passo governato

È autorizzato un singolo probe read-only via `ASCOM.CloudWatcher.ObservingConditions` usando `scripts/telemetry/Invoke-CloudWatcherAscomSkyQualityProbe.ps1 -ExecuteProbe`.

Il probe deve:

1. istanziare esclusivamente il ProgID ObservingConditions;
2. non istanziare `ASCOM.CloudWatcher.SafetyMonitor`;
3. usare la property standard `Connected` solo per la durata necessaria, ripristinando lo stato se aperto dal probe;
4. leggere `SkyQuality` una sola volta;
5. leggere, se implementati, `SensorDescription('SkyQuality')` e `TimeSinceLastUpdate('SkyQuality')`;
6. non aprire direttamente porte seriali;
7. non cambiare configurazione, soglie, relay, firmware o Safety state;
8. salvare evidence JSON/TXT;
9. non promuovere automaticamente il valore in produzione: prima devono essere validate plausibilità, provenance e freshness.

Se il probe restituisce un valore numerico plausibile e freshness coerente, G1 può essere chiuso e si può procedere a G2/G6. Se `SkyQuality` non è implementato o risulta stale/non plausibile, la source resta non accettata e si rivaluta la fallback native protocol path.
