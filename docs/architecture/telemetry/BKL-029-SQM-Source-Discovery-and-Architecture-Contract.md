# BKL-029 — SQM Source Discovery and Architecture Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-029 |
| Capability | SQM Sky Quality Telemetry & Scientific History |
| Stato | **Blocked — passive discovery exhausted; direct protocol probe requires controlled design** |
| Data | 2026-08-30 |
| Autorità | Digital StarGate Architecture Office |
| Dipendenze | AP-004; AP-013; AP-014; Observatory Status; scientific session catalog |
| Runtime effect | None — discovery/documentation only; no device configuration changes |

## 1. Scopo

Definire la discovery governata della source SQM e il contratto architetturale per valorizzare realmente `weather.sqm_mag_arcsec2` e storicizzare la qualità del cielo nelle sessioni scientifiche.

BKL-029 non introduce alcun comando verso cupola, montatura, power, router o Safety Authority. SQM è una metrica scientifica di qualità della notte e **non è mai un Safety signal**.

## 2. Repository truth ed evidence runtime

La baseline iniziale mostrava `weather.sqm_mag_arcsec2 = $null`, nessuna evidence sufficiente di SQM calibrato dal CloudWatcher, nessuna istanza ASCOM `ObservingConditions` verificata e nessun SQM dedicato.

Il primo inventory runtime su `EAGLE30154`, bundle `C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\`, ha rilevato:

- nessuna istanza ASCOM `ObservingConditions`;
- nessun campo SQM candidato nel CSV CloudWatcher osservato;
- nessun device SQM candidato via PnP/serial;
- disposition `NO_VERIFIED_SOURCE_FOUND`.

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
- nessuna TypeLib associata;
- nessun termine SQM/sky-quality/mpsas nella metadata surface passivamente visibile;
- disposition `LEGACY_COM_REGISTERED_NO_SQM_TERM_FOUND_IN_PASSIVE_METADATA`.

Il quarto inventory passivo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-hardware-firmware-inventory-20260830-183508\`, ha rilevato:

- `AAG_CloudWatcher.exe` file/product version `9.05`;
- altri componenti Lunatico/AAG locali, incluso `AAG_ACPWeatherFeed.exe` 7.20 e `AAG_HASFileLoader.exe` 2.22;
- nessun metadata locale di modello, seriale, revisione hardware o firmware dispositivo;
- nessun metadata locale SQM/mpsas;
- disposition `NO_LOCAL_HARDWARE_FIRMWARE_OR_SQM_METADATA_FOUND`.

Conclusione corrente: la discovery passiva locale è esaurita senza una source SQM verificata. `weather.sqm_mag_arcsec2` deve restare `null`; nessuna stima sostitutiva è ammessa.

## 3. Candidate source discovery

### 3.1 ASCOM ObservingConditions

ASCOM `ObservingConditions.SkyQuality` è semanticamente adatto a una misura in magnitudini per arcsec². L'inventory del 2026-08-30 non ha trovato driver/ProgID candidati sull'EAGLE. Candidate corrente: `NOT AVAILABLE`.

### 3.2 Lunatico CloudWatcher

Il software locale verificato è `AAG CloudWatcher v.9.5.0`. Il ProgID legacy è registrato ma non espone passivamente TypeLib o metadata SQM. Il CSV corrente non espone SQM. I file/registry locali non identificano firmware o revisione hardware.

La documentazione Lunatico pubblica corrente indica che:

- i CloudWatcher recenti includono un sensore sky-quality e misurano in mpsas;
- per unità aggiornate con sensore sky-quality grade è disponibile firmware 5.8.9 con sky-quality readings;
- il protocollo seriale v1.4 documenta il blocco `!8` come raw frequency del nuovo light sensor, da convertire in MPSAS dal software Windows/SOLO; il blocco `!4` rimane invece un LDR voltage stimato per backward compatibility quando il nuovo sensore è presente;
- pertanto `!4` non è una source SQM valida e non deve essere usato come proxy.

Queste informazioni sono capability documentation, non evidence del dispositivo fisico installato su EAGLE30154.

Il prossimo possibile passo è un **direct protocol probe read-only** per ottenere identità/versione e, se documentato e disponibile, il blocco `!8`. Tale probe non è ancora autorizzato operativamente finché non viene verificato il command set esatto e il rischio di collisione con il software CloudWatcher che potrebbe detenere la porta seriale.

Riferimenti esterni:

- <https://lunaticoastro.com/aag-cloud-watcher/>
- <https://lunaticoastro.com/cloudwatcher-software-downloads.html>
- <https://lunaticoastro.com/aagcw/TechInfo/Rs232_Comms_v140.pdf>

### 3.3 SQM dedicato

L'inventory PnP/seriale non ha rilevato un device identificabile come SQM/Unihedron/sky-quality. Candidate corrente: `NOT AVAILABLE`.

### 3.4 Proxy vietati

Non è consentito produrre `sqm_mag_arcsec2` da brightness/LDR non calibrato come SQM, cloud cover, sky temperature, Moon altitude/phase, trasparenza stimata o background fotografico.

## 4. Source selection gate

Una source passa a `VERIFIED` solo con evidence runtime riproducibile di identity/versione, interfaccia, unità mpsas, campioni reali UTC, cadence, error/disconnect behavior, assenza di command path e disposizione finale.

Disposizione corrente:

- ASCOM ObservingConditions: `NOT AVAILABLE`;
- CloudWatcher CSV SQM field: `NOT AVAILABLE` nel canale osservato;
- CloudWatcher legacy COM: `REGISTERED / PASSIVE SURFACE NON-DESCRIPTIVE`;
- CloudWatcher direct serial protocol: `CANDIDATE / NOT YET PROBED`;
- SQM dedicato: `NOT AVAILABLE`;
- source SQM complessiva: `NO_VERIFIED_SOURCE_FOUND`.

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
4. freshness fissata dopo misura della cadence reale;
5. timestamp projection generale non sostituisce timestamp SQM;
6. il portale visualizza assenza/staleness senza inventare valori;
7. SQM non modifica Safety Authority o interlock.

Nel runtime corrente `sqm_mag_arcsec2` resta `null` e G2 non parte.

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

Consentito: discovery read-only, campionamento leggero, normalizzazione minima/timestamp e spool locale resiliente se necessario.

Vietato: analytics pesanti, inferenza SQM da proxy, modifica configurazione weather come effetto collaterale, uso SQM per Safety o command path.

### Repository / Scientific Data Engine

Responsabile di schema/provenance versionati, associazione campioni-sessione, statistiche storiche, projection portale/catalogo e validazioni anti-drift/fail-safe.

## 8. Acceptance gates BKL-029

- **G1 Source discovery:** `IN PROGRESS WITH BLOCK` — passive discovery completata; resta solo direct protocol discovery controllata oppure decisione esplicita di indisponibilità;
- **G2 Realtime contract:** `BLOCKED` — nessuna source SQM reale verificata;
- **G3 Historical contract:** `BLOCKED` — nessun campione SQM reale disponibile;
- **G4 Regression:** non eseguito per runtime SQM perché nessuna implementazione è autorizzata;
- **G5 CI/docs:** da verificare sui commit; nessun successo assunto senza evidence GitHub reale;
- **G6 Runtime OAT:** `BLOCKED`.

## 9. Evidence runtime 2026-08-30

### 9.1 Inventory generale SQM

```text
Computer: EAGLE30154
ASCOM OBSERVING CONDITIONS CANDIDATES: none found
CLOUDWATCHER SQM CANDIDATE FIELDS: none found
PNP / SERIAL CANDIDATES: no named SQM candidates found via PnP
SOURCE DISPOSITION: NO_VERIFIED_SOURCE_FOUND
Evidence: C:\DigitalStarGate\TelemetryEvidence\sqm-source-inventory-20260830-181223\
```

### 9.2 CloudWatcher passive capability inventory

```text
AAG CloudWatcher v.9.5.0 / 9.5.0 / Lunático Astronomía
AAG_WeatherCenter v2.30
AAG_CloudWatcher.CloudWatcher: registered=True
ASCOM.AAGCloudWatcher.ObservingConditions: registered=False
ASCOM.Lunatico.ObservingConditions: registered=False
SQM evidence files: 0
Firmware metadata files: 0
DISPOSITION: NO_PASSIVE_SQM_OR_FIRMWARE_METADATA_FOUND
Evidence: C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-capability-20260830-182202\
```

### 9.3 Legacy COM passive surface

```text
ProgID: AAG_CloudWatcher.CloudWatcher
CLSID: {F8D7A9ED-D0E2-45F8-BAC6-88DBB322475B}
TypeLib evidence entries: 0
SQM-related entries: 0
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

Tutti gli inventory sopra sono stati eseguiti senza modifica configurazione; gli ultimi tre senza attivazione COM e senza accesso seriale diretto.

## 10. Prossimo passo governato

La discovery passiva è conclusa. Prima di qualsiasi apertura seriale occorre definire un probe conforme al protocollo Lunatico v1.4 che:

1. usi esclusivamente comandi/letture documentati come non distruttivi;
2. non modifichi parametri o firmware;
3. non usi `!4`/LDR come SQM;
4. acquisisca identity/version e, solo se realmente presente, il blocco `!8`;
5. rilevi se la porta seriale è già occupata dal software CloudWatcher e **non forzi** l'accesso se in uso;
6. produca evidence JSON/TXT con timestamp e raw response;
7. non venga eseguito durante condizioni operative critiche dell'osservatorio.

Fino alla progettazione e validazione di tale probe:

- `weather.sqm_mag_arcsec2` resta `null`;
- nessun proxy viene introdotto;
- nessun adapter realtime SQM viene implementato;
- BKL-030 non viene avviato per aggirare questo gate.
