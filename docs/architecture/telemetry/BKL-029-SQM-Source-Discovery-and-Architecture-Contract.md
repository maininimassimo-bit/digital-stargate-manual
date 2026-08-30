# BKL-029 — SQM Source Discovery and Architecture Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-029 |
| Capability | SQM Sky Quality Telemetry & Scientific History |
| Stato | **Blocked — G1 source discovery completed; CloudWatcher native capability verification in progress** |
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

Il secondo inventory passivo, bundle `C:\DigitalStarGate\TelemetryEvidence\cloudwatcher-sqm-capability-20260830-182202\`, ha aggiunto evidence determinante sul software locale:

- `AAG CloudWatcher v.9.5.0`, versione `9.5.0`, publisher Lunático Astronomía, install location `C:\Program Files (x86)\AAG_CloudWatcher\`;
- `AAG_WeatherCenter v2.30` installato;
- ProgID legacy `AAG_CloudWatcher.CloudWatcher` registrato;
- `ASCOM.AAGCloudWatcher.ObservingConditions` non registrato;
- `ASCOM.Lunatico.ObservingConditions` non registrato;
- nessun file passivamente rilevato con metadata SQM;
- nessun file passivamente rilevato con metadata firmware;
- disposition `NO_PASSIVE_SQM_OR_FIRMWARE_METADATA_FOUND`.

Questa evidence **non verifica una source SQM** e non prova che il dispositivo fisico sia privo di sensore sky-quality. Dimostra però che il canale CSV corrente non espone SQM, che non è disponibile un driver ASCOM ObservingConditions noto e che esiste una superficie COM legacy Lunatico da caratterizzare prima di qualsiasi attivazione.

Conclusione corrente: `weather.sqm_mag_arcsec2` deve restare `null`; nessuna stima sostitutiva è ammessa.

## 3. Candidate source discovery

### 3.1 ASCOM ObservingConditions

ASCOM `ObservingConditions.SkyQuality` è semanticamente adatto a una misura in magnitudini per arcsec². Tuttavia l'inventory del 2026-08-30 non ha trovato i ProgID candidati sull'EAGLE. Candidate corrente: `NOT AVAILABLE`.

Se in futuro viene installato/configurato un driver, devono essere verificati ProgID, connessione read-only, implementazione `SkyQuality`, unità, timestamp/cadence, metadata sensore e assenza di command path operativo.

Riferimento esterno di capability, non evidence runtime: <https://ascom-standards.org/library/html/P_ASCOM_Com_DriverAccess_ObservingConditions_SkyQuality.htm>.

### 3.2 Lunatico CloudWatcher

Il software locale verificato è `AAG CloudWatcher v.9.5.0`. È inoltre registrato il ProgID legacy `AAG_CloudWatcher.CloudWatcher`. Nessuno dei due fatti, isolatamente, dimostra che l'unità fisica fornisca SQM.

Il CSV osservato non espone un campo identificabile come SQM/sky quality/mpsas. L'inventory passivo di file e registry non ha trovato metadata SQM o firmware utilizzabili. Pertanto la candidate CloudWatcher resta `UNVERIFIED`.

Il prossimo gate è caratterizzare la registrazione COM legacy **senza istanziare l'oggetto**: CLSID, server COM, type library e metadata registrati. Solo se tale evidence identifica una superficie SQM semanticamente valida verrà progettato un successivo probe read-only con attivazione controllata.

Ordine di preferenza se CloudWatcher risulta compatibile:

1. ASCOM ObservingConditions `SkyQuality` verificato, se reso disponibile;
2. interfaccia nativa Lunatico read-only/documentata e verificata;
3. mai brightness/LDR legacy come sostituto SQM.

Riferimenti esterni di capability, non evidence runtime:

- <https://lunaticoastro.com/aag-cloud-watcher/>
- <https://lunaticoastro.com/cloudwatcher-software-downloads.html>
- <https://lunaticoastro.com/cloudwatcher-moreinfo.html>

### 3.3 SQM dedicato

L'inventory PnP/seriale non ha rilevato un device identificabile come SQM/Unihedron/sky-quality. Candidate corrente: `NOT AVAILABLE`.

### 3.4 Proxy vietati

Non è consentito produrre `sqm_mag_arcsec2` da brightness/LDR non calibrato come SQM, cloud cover, sky temperature, Moon altitude/phase, trasparenza stimata o background fotografico.

## 4. Source selection gate

Una source passa a `VERIFIED` solo con evidence runtime riproducibile di identity/versione, interfaccia, unità mpsas, campioni reali UTC, cadence, error/disconnect behavior, assenza di command path e disposizione finale.

Disposizione corrente:

- ASCOM ObservingConditions: `NOT AVAILABLE`;
- CloudWatcher CSV SQM field: `NOT AVAILABLE` nel canale osservato;
- CloudWatcher legacy COM: `REGISTERED / SURFACE NOT YET CHARACTERIZED`;
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

- **G1 Source discovery:** `IN PROGRESS WITH BLOCK` — inventory generale completato; CloudWatcher legacy COM registrato ma superficie ancora da caratterizzare senza attivazione;
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
Computer: EAGLE30154
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

Il secondo test è stato passivo: nessuna attivazione COM, nessuna connessione device, nessun comando e nessuna modifica di configurazione.

## 10. Prossimo passo governato

È autorizzato il solo inventory della superficie COM registrata mediante registry/type-library/file metadata, senza `New-Object -ComObject`, senza `Activator.CreateInstance` e senza connessione al device.

Script governato: `scripts/telemetry/Inspect-CloudWatcherLegacyComSurface.ps1`.

Se la superficie passiva mostra un membro o contratto SQM/sky-quality/mpsas, l'Architecture Office valuterà un probe read-only controllato. Se non lo mostra, ciò non proverà l'assenza del sensore fisico ma restringerà ulteriormente la discovery verso identificazione hardware/firmware o decisione di introdurre una source SQM dedicata.

Fino a nuova evidence:

- `weather.sqm_mag_arcsec2` resta `null`;
- nessun proxy viene introdotto;
- nessun adapter realtime SQM viene implementato;
- BKL-030 non viene avviato per aggirare questo gate.
