# BKL-029 — SQM Source Discovery and Architecture Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-029 |
| Capability | SQM Sky Quality Telemetry & Scientific History |
| Stato | **Blocked — ASCOM SkyQuality property reachable but returned implausible zero; valid runtime SQM still unverified** |
| Data | 2026-08-30 |
| Autorità | Digital StarGate Architecture Office |
| Dipendenze | AP-004; AP-013; AP-014; Observatory Status; scientific session catalog |
| Runtime effect | None — discovery/documentation only; no device configuration changes |

## 1. Scopo

Definire la discovery governata della source SQM e il contratto architetturale per valorizzare realmente `weather.sqm_mag_arcsec2` e storicizzare la qualità del cielo nelle sessioni scientifiche.

BKL-029 non introduce alcun comando verso cupola, montatura, power, router o Safety Authority. SQM è una metrica scientifica di qualità della notte e **non è mai un Safety signal**.

## 2. Repository truth ed evidence runtime

La baseline iniziale mostrava `weather.sqm_mag_arcsec2 = $null`, nessuna evidence sufficiente di SQM calibrato dal CloudWatcher, nessuna istanza ASCOM `ObservingConditions` verificata e nessun SQM dedicato.

La discovery del 2026-08-30 ha progressivamente identificato una superficie ASCOM reale, ma la prima lettura runtime non ha prodotto un valore scientificamente valido.

Il primo inventory runtime su `EAGLE30154`, bundle `C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\`, aveva rilevato:

- nessuna istanza ASCOM `ObservingConditions` tra i ProgID allora ricercati;
- nessun campo SQM candidato nel CSV CloudWatcher osservato;
- nessun device SQM candidato via PnP/serial;
- disposition `NO_VERIFIED_SOURCE_FOUND`.

Quella conclusione ASCOM era incompleta: la discovery successiva ha identificato il ProgID reale `ASCOM.CloudWatcher.ObservingConditions`, non incluso nei candidati iniziali.

Gli inventory passivi successivi hanno verificato:

- `AAG CloudWatcher v.9.5.0` e `AAG_WeatherCenter v2.30` installati;
- ProgID legacy `AAG_CloudWatcher.CloudWatcher` registrato;
- nessun metadata locale sufficiente a verificare firmware/revisione hardware/SQM;
- nessuna porta enumerata tramite `Win32_SerialPort` nel preflight seriale;
- `AAG_CloudWatcher.exe` e `ASCOM.CloudWatcher.Server.exe` in esecuzione;
- nessuna porta seriale aperta dai probe DSG.

L'inventory ASCOM passivo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-surface-20260830-192856\`, ha identificato:

- ProgID `ASCOM.CloudWatcher.ObservingConditions` registrato;
- CLSID `{efef952b-d34c-4d25-bdbf-0a0a58a2414e}`;
- server multi-interface `ASCOM.CloudWatcher.Server.exe` registrato e in esecuzione;
- ProgID `ASCOM.CloudWatcher.SafetyMonitor` distinto;
- interfacce ASCOM `IObservingConditions` / `IObservingConditionsV2` presenti nella registrazione;
- OCH/ASCOM mapping che include `SkyQuality` per la source CloudWatcher.

Il preflight dedicato SkyQuality, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-skyquality-20260830-193734\`, ha confermato:

- driver `Lunatico CloudWatcher Observing Conditions`;
- `DataFile = C:\Users\PrimaLuceLab\Documents\aag_json.dat`;
- `MaxSecsDiff = 60`;
- nessuna istanziazione ASCOM o connessione durante il preflight.

Il probe runtime controllato, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-skyquality-20260830-194200\`, ha poi verificato tecnicamente il driver:

- oggetto ASCOM creato con successo;
- `Connected` inizialmente `False`, impostato a `True` dal probe e ripristinato a `False` al termine;
- `Name = CloudWatcher ObsCond`;
- `Description = ASCOM ObservingConditions Driver for CloudWatcher.`;
- `DriverInfo = CloudWatcher specific driver. Version: 1.1`;
- `DriverVersion = 1.1`;
- `InterfaceVersion = 1`;
- property `SkyQuality` leggibile senza eccezioni;
- valore restituito `SkyQuality = 0`;
- `SensorDescription('SkyQuality')` non ha prodotto metadata;
- `TimeSinceLastUpdate('SkyQuality')` non ha prodotto un valore utilizzabile;
- nessun accesso seriale diretto, nessun SafetyMonitor interaction, nessuna modifica di configurazione.

Il valore `0` non è accettato come misura SQM reale. Per il contratto DSG è trattato come **non valido/unknown**, non come cielo reale a 0 mag/arcsec².

Conclusione corrente: la superficie ASCOM e la property `SkyQuality` sono raggiungibili, ma una source SQM scientificamente valida non è ancora verificata. `weather.sqm_mag_arcsec2` resta `null`.

## 3. Candidate source discovery

### 3.1 ASCOM ObservingConditions

Candidate corrente: `TECHNICALLY REACHABLE / SCIENTIFIC VALUE INVALID`.

Source:

```text
ProgID: ASCOM.CloudWatcher.ObservingConditions
Driver: Lunatico CloudWatcher Observing Conditions
DriverVersion: 1.1
DataFile: C:\Users\PrimaLuceLab\Documents\aag_json.dat
MaxSecsDiff: 60
```

La property standard `SkyQuality` è implementata e leggibile, ma il primo runtime sample è `0`, privo di sensor description e freshness evidence. Questo non soddisfa il gate di validità scientifica.

Prima di qualunque integrazione production occorre determinare se `0` significa sensore non disponibile/non supportato nel file sorgente, valore non popolato dal software CloudWatcher, stale/default sentinel, oppure altra condizione documentata.

### 3.2 Lunatico CloudWatcher native protocol

Il protocollo seriale diretto resta una fallback diagnostic path. Non viene aperto mentre `AAG_CloudWatcher.exe`/server ASCOM stanno gestendo il device, salvo finestra controllata esplicitamente governata.

La documentazione Lunatico pubblica indica che:

- i CloudWatcher recenti includono un sensore sky-quality e misurano in mpsas;
- il protocollo seriale v1.4 documenta il blocco `!8` come raw frequency del nuovo light sensor;
- `!4` è LDR/backward compatibility e non è una source SQM valida.

### 3.3 SQM dedicato

Nessun device SQM dedicato è stato rilevato. Candidate corrente: `NOT AVAILABLE`.

### 3.4 Proxy vietati

Non è consentito produrre `sqm_mag_arcsec2` da brightness/LDR non calibrato come SQM, cloud cover, sky temperature, Moon altitude/phase, trasparenza stimata o background fotografico.

## 4. Source selection gate

Una source passa a `VERIFIED` per uso realtime solo con evidence runtime riproducibile di identity/versione, interfaccia, unità mpsas, campioni reali plausibili UTC, freshness, error behavior e provenance.

Disposizione corrente:

- ASCOM CloudWatcher ObservingConditions: `REACHABLE / SKYQUALITY=0 INVALID`;
- CloudWatcher CSV SQM field: `NOT AVAILABLE` nel canale osservato;
- CloudWatcher legacy COM: `REGISTERED / PASSIVE SURFACE NON-DESCRIPTIVE`;
- CloudWatcher direct serial protocol: `FALLBACK / NOT PROBED`;
- SQM dedicato: `NOT AVAILABLE`;
- source SQM complessiva: `NO VALID RUNTIME VALUE VERIFIED`.

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

1. valore numerico solo da misura strumentale verificata e plausibile;
2. `0` dal driver corrente non viene pubblicato come SQM reale;
3. source assente/non valida -> `null`, quality `UNKNOWN`;
4. campione oltre freshness -> `STALE`;
5. `MaxSecsDiff=60` è evidence di configurazione, non automaticamente freshness canonica DSG;
6. freshness DSG richiede evidence runtime affidabile;
7. il portale visualizza assenza/staleness senza inventare valori;
8. SQM non modifica Safety Authority o interlock.

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

Il campione `SkyQuality = 0` del 2026-08-30 **non entra** nelle statistiche scientifiche.

## 7. Boundary e responsabilità

### EAGLE

Consentito: discovery read-only, lettura ASCOM `ObservingConditions.SkyQuality`, campionamento leggero, normalizzazione minima/timestamp e spool locale resiliente se necessario.

Vietato: analytics pesanti, inferenza SQM da proxy, modifica configurazione weather come effetto collaterale, uso SQM per Safety o command path.

### Safety boundary

`ASCOM.CloudWatcher.SafetyMonitor` è un'interfaccia separata e non viene usata da BKL-029.

### Repository / Scientific Data Engine

Responsabile di schema/provenance versionati, associazione campioni-sessione, statistiche storiche, projection portale/catalogo e validazioni anti-drift/fail-safe.

## 8. Acceptance gates BKL-029

- **G1 Source discovery:** `BLOCKED ON VALID VALUE` — driver/property identificati e raggiungibili, ma il campione `0` non è accettabile come misura SQM;
- **G2 Realtime contract:** `BLOCKED` — nessun valore runtime valido;
- **G3 Historical contract:** `BLOCKED` — nessun campione SQM valido;
- **G4 Regression:** non eseguito per runtime production SQM;
- **G5 CI/docs:** da verificare sui commit; nessun successo assunto senza evidence GitHub reale;
- **G6 Runtime OAT:** `BLOCKED ON VALID VALUE`.

## 9. Evidence runtime 2026-08-30

### 9.1 Inventory generale SQM

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\
Disposition at time: NO_VERIFIED_SOURCE_FOUND
```

### 9.2 CloudWatcher passive capability inventory

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-capability-20260830-182202\
Disposition: NO_PASSIVE_SQM_OR_FIRMWARE_METADATA_FOUND
```

### 9.3 Legacy COM passive surface

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-legacy-com-surface-20260830-183012\
Disposition: LEGACY_COM_REGISTERED_NO_SQM_TERM_FOUND_IN_PASSIVE_METADATA
```

### 9.4 Hardware / firmware local metadata inventory

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-hardware-firmware-inventory-20260830-183508\
Disposition: NO_LOCAL_HARDWARE_FIRMWARE_OR_SQM_METADATA_FOUND
```

### 9.5 Serial protocol preflight

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-protocol-probe-20260830-190848\
Disposition: PREFLIGHT_ONLY_NO_SERIAL_ACCESS
```

### 9.6 ASCOM surface inventory

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-surface-20260830-192856\
ASCOM.CloudWatcher.ObservingConditions registered
ASCOM.CloudWatcher.SafetyMonitor separately registered
```

### 9.7 ASCOM SkyQuality preflight

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-skyquality-20260830-193734\
Disposition: PREFLIGHT_ONLY_NO_ASCOM_ACTIVATION
```

### 9.8 ASCOM SkyQuality runtime probe

```text
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-ascom-skyquality-20260830-194200\
Name: CloudWatcher ObsCond
DriverVersion: 1.1
InterfaceVersion: 1
Connected before: False
Connected after connect: True
Connection restored after probe: True
SkyQuality read: True
SkyQuality: 0
SensorDescription(SkyQuality): unavailable/empty
TimeSinceLastUpdate(SkyQuality): unavailable/empty
Disposition: ASCOM_SKYQUALITY_READ_SUCCEEDED_REQUIRES_PLAUSIBILITY_AND_FRESHNESS_REVIEW
DSG disposition: INVALID_SQM_SAMPLE_ZERO
```

## 10. Prossimo passo governato

Non implementare ancora l'adapter realtime e non avviare BKL-030.

Il prossimo passo deve essere **passivo sul data path ASCOM**: ispezionare `C:\Users\PrimaLuceLab\Documents\aag_json.dat` e la configurazione/metadata del driver CloudWatcher per determinare se il file contiene un campo sky-quality/SQM/mpsas e quale semantica abbia il valore `0` restituito dal driver.

Regole:

1. nessuna modifica del file `aag_json.dat`;
2. nessun cambio di configurazione CloudWatcher/ASCOM;
3. nessun accesso seriale diretto;
4. nessun utilizzo di `0` come valore scientifico;
5. se il data file contiene un valore SQM reale e plausibile, correlare esattamente campo -> driver -> property ASCOM;
6. se il campo non esiste o è sempre zero/default, la source ASCOM non passa G1 e si valuta la fallback protocol path o una source SQM dedicata.
