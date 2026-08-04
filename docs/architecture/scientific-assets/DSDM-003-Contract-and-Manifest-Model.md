# DSDM-003 — Digital StarGate Contract and Manifest Model

| Campo | Valore |
|---|---|
| Architecture Package | AP-013 — Scientific Image Repository Architecture |
| Documento | Contract and Manifest Model |
| Identificativo | DSDM-003 |
| Data | 04/08/2026 |
| Autorità | Digital StarGate Chief Architect |
| Sponsor | Project Owner / Architecture Sponsor — Massimo Mainini |
| Stato | Contract baseline — JSON schemas not yet implemented |
| Dipendenze | DSDM-001; DSDM-002; SIR-INV-001; E-AP13-W02-01 |

## 1. Scopo

DSDM-003 definisce i contratti machine-readable che collegheranno inventario, Session Importer, Calibration Manager, Processing Provenance e futuro Scientific Data Manager.

La baseline stabilisce:

- struttura comune dei manifest;
- identificazione e versioning degli schemi;
- contratti minimi previsti;
- regole di compatibilità;
- validazione e gestione degli errori;
- relazioni con il modello logico DSDM-002;
- esempi validi e invalidi;
- criteri per la futura implementazione degli schemi JSON.

Il documento non dichiara che gli schemi `.schema.json`, i validator o gli script siano già implementati.

## 2. Principi contrattuali

1. **Schema-first** — ogni payload operativo deve riferirsi a uno schema identificato e versionato.
2. **Observed values preserved** — i valori originali osservati non sono sostituiti dalla normalizzazione.
3. **Stable identity** — gli ID DSDM sono indipendenti da filename e path.
4. **Forward-compatible consumers** — campi opzionali nuovi non devono interrompere i consumer compatibili.
5. **No silent coercion** — stringhe, numeri, timestamp ed enum non vengono convertiti silenziosamente.
6. **UTC where authoritative** — i timestamp autorevoli usano ISO 8601 UTC; valori locali osservati restano separati.
7. **Explicit unknown** — incompletezza e ambiguità sono rappresentate esplicitamente.
8. **Evidence separation** — un manifest descrive una run o un asset, ma non sostituisce log, checksum o evidence.
9. **No embedded secrets** — token, password, connection string e credenziali sono vietati.
10. **Append, do not rewrite history** — una nuova osservazione o run produce un nuovo manifest o una nuova versione governata.

## 3. Namespace e organizzazione prevista

Struttura repository candidata:

```text
contracts/
└── dsdm/
    ├── v1/
    │   ├── common/
    │   │   ├── identifier.schema.json
    │   │   ├── audit.schema.json
    │   │   ├── provenance-value.schema.json
    │   │   ├── storage-locator.schema.json
    │   │   └── integrity-record.schema.json
    │   ├── session-manifest.schema.json
    │   ├── asset-manifest.schema.json
    │   ├── inventory-run.schema.json
    │   ├── processing-run.schema.json
    │   ├── calibration-set.schema.json
    │   └── transfer-run.schema.json
    └── examples/
        ├── valid/
        └── invalid/
```

La posizione definitiva sarà decisa in fase di implementazione. Gli schemi non saranno collocati nel repository documentale se appartengono a un futuro repository applicativo dedicato.

## 4. Envelope comune

Tutti i manifest DSDM adottano un envelope logico comune.

```json
{
  "schemaId": "dsdm:session-manifest",
  "schemaVersion": "1.0.0",
  "manifestId": "DSG-MANIFEST-550e8400-e29b-41d4-a716-446655440000",
  "manifestType": "SESSION_MANIFEST",
  "createdAtUtc": "2026-08-04T07:30:00Z",
  "createdBy": {
    "identityType": "PERSON",
    "identityId": "massimo-mainini"
  },
  "sourceSystem": "DSG-SESSION-IMPORTER",
  "sourceVersion": "0.1.0",
  "correlationId": "DSG-CORR-550e8400-e29b-41d4-a716-446655440001",
  "payload": {}
}
```

### 4.1 Campi comuni

| Campo | Tipo | Obbligatorio | Regola |
|---|---|---:|---|
| `schemaId` | string | sì | identificatore stabile dello schema |
| `schemaVersion` | semver string | sì | versione esatta usata |
| `manifestId` | DSDM identifier | sì | univoco e immutabile |
| `manifestType` | enum | sì | coerente con schemaId |
| `createdAtUtc` | UTC timestamp | sì | ISO 8601 con `Z` |
| `createdBy` | identity object | sì | persona o service identity |
| `sourceSystem` | string | sì | sistema produttore |
| `sourceVersion` | string | sì | versione software/commit/profilo |
| `correlationId` | string | no | collega run e manifest |
| `payload` | object | sì | contenuto specifico |
| `extensions` | object | no | estensioni namespaced |

## 5. Regole di versioning

La versione segue Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

### MAJOR

Incremento obbligatorio quando:

- viene rimosso un campo;
- cambia il significato di un campo;
- un campo opzionale diventa obbligatorio;
- cambia un tipo;
- viene ristretto un enum in modo incompatibile;
- cambia la struttura del payload.

### MINOR

Incremento quando:

- viene aggiunto un campo opzionale;
- viene aggiunto un valore enum che i consumer devono poter ignorare o trattare come unknown;
- viene aggiunto un nuovo blocco opzionale;
- vengono estese regole non incompatibili.

### PATCH

Incremento per:

- correzioni documentali;
- chiarimenti;
- esempi;
- regex equivalenti;
- descrizioni senza modifica del contratto.

## 6. Compatibility policy

| Producer | Consumer | Esito previsto |
|---|---|---|
| stessa major, producer minor <= consumer minor | compatibile |
| stessa major, producer minor > consumer minor | compatibile solo se unknown fields sono tollerati |
| major diversa | non compatibile senza adapter/migration |
| schemaId sconosciuto | rifiuto o quarantena |
| schemaVersion mancante | rifiuto |

Ogni consumer deve registrare:

- schema ricevuto;
- versione;
- esito validation;
- campi sconosciuti;
- warning;
- decisione accept/reject/quarantine.

## 7. Tipi comuni

### 7.1 Identifier

Pattern candidato:

```regex
^DSG-[A-Z0-9-]+-[0-9a-fA-F-]{36}$
```

Il pattern definitivo non deve impedire future strategie di ID, ma la baseline richiede almeno stringa non vuota e namespace DSDM.

### 7.2 Timestamp

- UTC autorevole: `YYYY-MM-DDTHH:mm:ss[.fff]Z`;
- local datetime osservato: stringa separata con `timezoneStatus`;
- nessuna conversione in UTC senza timezone nota.

### 7.3 ProvenanceValue

```json
{
  "observedValue": "LDN 1320",
  "normalizedValue": "LDN 1320",
  "source": "OBSERVED_FROM_FILENAME",
  "confidence": "CONFIRMED",
  "ruleVersion": "nina-filename-parser/1.0.0"
}
```

Campi:

- `observedValue`;
- `normalizedValue` opzionale;
- `source`;
- `confidence`;
- `ruleVersion` opzionale;
- `reviewStatus` opzionale.

### 7.4 IdentityReference

```json
{
  "identityType": "PERSON",
  "identityId": "massimo-mainini",
  "displayName": "Massimo Mainini"
}
```

`displayName` non è l'identificatore autorevole.

## 8. Session Manifest

### 8.1 Scopo

Descrive una sessione osservativa scoperta, acquisita o trasferita.

### 8.2 Payload minimo

```json
{
  "sessionId": "DSG-SESSION-550e8400-e29b-41d4-a716-446655440010",
  "projectId": null,
  "target": {
    "observedName": "LDN 1320",
    "normalizedName": "LDN 1320",
    "targetId": null,
    "matchStatus": "CANDIDATE"
  },
  "source": {
    "host": "EAGLE30154",
    "sourceId": "SRC-EAGLE30154-NINA-001",
    "rootLocator": "D:\\Images NINA\\Target"
  },
  "sessionStatus": "DISCOVERED",
  "transferStatus": "NOT_PLANNED",
  "observingDateLocal": "2026-07-16",
  "startedAtUtc": null,
  "completedAtUtc": null,
  "instrumentConfigurationId": null,
  "frameSummary": {
    "totalFrames": 30,
    "totalBytes": 695792640,
    "totalExposureSeconds": 18000.0,
    "byImageType": {
      "LIGHT": 30
    },
    "byFilter": {
      "LPRO": 30
    }
  },
  "frameManifestReferences": [],
  "limitations": [
    "Target and telescope mapping require alias review"
  ]
}
```

### 8.3 Regole

- `sessionId` obbligatorio;
- `source` obbligatoria;
- almeno un frame o un finding di sessione vuota;
- `totalFrames` deve riconciliarsi con il frame manifest;
- `totalBytes` deve essere >= 0;
- `TRANSFER_VERIFIED` richiede evidence reference;
- sessioni multi-night non vengono fuse automaticamente senza regola approvata.

## 9. Asset Manifest

### 9.1 Scopo

Descrive un singolo asset scientifico o tecnico.

### 9.2 Payload minimo

```json
{
  "assetId": "DSG-ASSET-550e8400-e29b-41d4-a716-446655440020",
  "assetClass": "RAW_ORIGINAL",
  "originalFileName": "LIGHT_1x1_600.00s_910_99_LDN 1320_Skywatcher quattro 200p__-10.00C_LPRO_0163_2026-07-17_04-16-06_FWHM_5.77_Fok_116189.xisf",
  "format": "XISF",
  "sizeBytes": 23193088,
  "registrationStatus": "DISCOVERED",
  "immutabilityStatus": "NOT_ASSESSED",
  "integrityStatus": "NOT_VERIFIED",
  "sourceLocator": {
    "storageVolumeId": "DSG-STORAGE-EAGLE-D",
    "relativePath": "LIGHT_1x1_600.00s_910_99_LDN 1320_Skywatcher quattro 200p__-10.00C_LPRO_0163_2026-07-17_04-16-06_FWHM_5.77_Fok_116189.xisf",
    "locatorType": "SOURCE"
  },
  "acquisition": {
    "imageType": "LIGHT",
    "binningX": 1,
    "binningY": 1,
    "exposureSeconds": 600.0,
    "gain": 910,
    "offset": 99,
    "targetObserved": "LDN 1320",
    "telescopeObserved": "Skywatcher quattro 200p",
    "sensorTemperatureC": -10.0,
    "filterObserved": "LPRO",
    "frameNumber": 163,
    "datetimeObserved": "2026-07-17_04-16-06",
    "fwhmObserved": 5.77,
    "focusPosition": 116189,
    "parseStatus": "PARSED"
  },
  "integrityRecords": [],
  "qualityFlags": []
}
```

### 9.3 Regole

- `originalFileName`, `sizeBytes`, `assetClass` e locator sono obbligatori;
- `sizeBytes` non può essere negativo;
- hash assente è ammesso con `NOT_VERIFIED`;
- `RAW_ORIGINAL` non può essere marcato mutable senza finding;
- parse fallito non impedisce la registrazione dell'asset;
- filename e valori osservati restano invariati.

## 10. Inventory Run Manifest

### 10.1 Scopo

Descrive una run P0–P4 dell'Inventory Engine.

### 10.2 Payload minimo

```json
{
  "inventoryRunId": "DSG-INVENTORY-RUN-550e8400-e29b-41d4-a716-446655440030",
  "profile": "P1_METADATA_ONLY",
  "startedAtUtc": "2026-08-04T07:35:00Z",
  "completedAtUtc": "2026-08-04T07:36:20Z",
  "resultStatus": "COMPLETED",
  "tool": {
    "name": "DSG-Inventory",
    "version": "0.1.0",
    "commit": null
  },
  "sources": [
    {
      "sourceId": "SRC-EAGLE30154-NINA-001",
      "accessMode": "READ_ONLY"
    }
  ],
  "exclusions": [],
  "followSymlinks": false,
  "summary": {
    "entryCount": 30,
    "totalBytes": 695792640,
    "errorCount": 0,
    "unclassifiedCount": 0
  },
  "outputArtifacts": [],
  "limitations": []
}
```

### 10.3 Profili

- `P0_SOURCE_DISCOVERY`;
- `P1_METADATA_ONLY`;
- `P2_HEADER_ENRICHED`;
- `P3_SAMPLE_HASHING`;
- `P4_FULL_HASHING`.

La presenza del profilo non prova che l'operazione sia autorizzata: il manifest deve includere `authorizationReference`.

## 11. Transfer Run Manifest

### 11.1 Scopo

Descrive pianificazione, staging, copia e verifica di una sessione.

### 11.2 Stati

`PLANNED`, `PRECHECK_FAILED`, `STAGING`, `COPYING`, `VERIFYING`, `VERIFIED`, `PARTIAL`, `FAILED`, `CANCELLED`.

### 11.3 Payload minimo

```json
{
  "transferRunId": "DSG-TRANSFER-RUN-550e8400-e29b-41d4-a716-446655440040",
  "sessionId": "DSG-SESSION-550e8400-e29b-41d4-a716-446655440010",
  "status": "PLANNED",
  "source": {
    "sourceId": "SRC-EAGLE30154-NINA-001",
    "host": "EAGLE30154"
  },
  "destination": {
    "storageVolumeId": "DSG-STORAGE-ACTIVE-F",
    "targetRoot": "<sanitized>"
  },
  "window": {
    "notBeforeLocal": "07:35",
    "doNotStartAfterLocal": "08:10",
    "mustFinishBeforeLocal": "08:25"
  },
  "prechecks": [],
  "fileResults": [],
  "verification": {
    "fileCountMatched": false,
    "totalBytesMatched": false,
    "hashMode": "NONE",
    "verifiedAtUtc": null
  },
  "sourceCleanup": {
    "authorized": false,
    "performed": false
  }
}
```

### 11.4 Vincoli

- `sourceCleanup.authorized` deve essere `false` nel pilot;
- stato `VERIFIED` richiede count e byte match;
- se hashing è abilitato, tutti gli hash richiesti devono essere coerenti;
- una collisione non può essere risolta con overwrite silenzioso;
- destinazione deve essere verificata tramite volume identity, non solo drive letter.

## 12. Calibration Set Manifest

Descrive un set candidato o validato di calibrazioni.

Campi minimi:

- `calibrationSetId`;
- camera reference;
- image type;
- gain;
- offset;
- binning;
- temperatura;
- esposizione;
- filtro, quando applicabile;
- membri;
- master asset opzionale;
- compatibility rule version;
- quality status;
- validità temporale;
- limitations.

Un set non diventa `VALID` soltanto perché i file condividono una cartella.

## 13. Processing Run Manifest

### 13.1 Scopo

Registra una specifica esecuzione di processing.

### 13.2 Payload minimo

```json
{
  "processingRunId": "DSG-RUN-550e8400-e29b-41d4-a716-446655440050",
  "projectId": "DSG-PROJECT-550e8400-e29b-41d4-a716-446655440051",
  "workflowVersionId": null,
  "processingEnvironmentId": null,
  "operator": {
    "identityType": "PERSON",
    "identityId": "massimo-mainini"
  },
  "status": "PLANNED",
  "startedAtUtc": null,
  "completedAtUtc": null,
  "inputs": [],
  "steps": [],
  "outputs": [],
  "manualStepsDeclared": false,
  "warnings": [],
  "limitations": [
    "PixInsight process history not yet captured"
  ]
}
```

### 13.3 Regole

- `COMPLETED` richiede almeno un output;
- step manuali devono essere dichiarati;
- input/output usano asset ID stabili;
- la workflow definition è distinta dalla run;
- modifiche successive generano una nuova run o amendment append-only.

## 14. Estensioni vendor-specific

Le estensioni sono consentite solo in namespace espliciti:

```json
{
  "extensions": {
    "nina": {},
    "pixinsight": {},
    "xisf": {},
    "fits": {}
  }
}
```

Regole:

- non duplicano campi canonici senza motivazione;
- non diventano obbligatorie per consumer generici;
- devono avere una propria versione;
- non contengono secret;
- eventuali payload binari non sono incorporati direttamente.

## 15. Error model

Formato logico comune:

```json
{
  "errorCode": "DSDM-CONTRACT-VALIDATION-001",
  "severity": "ERROR",
  "path": "$.payload.acquisition.exposureSeconds",
  "message": "Value must be greater than zero",
  "observedValue": -1,
  "rule": "exclusiveMinimum: 0",
  "recoverability": "REQUIRES_REVIEW"
}
```

### Severità

- `INFO`;
- `WARNING`;
- `ERROR`;
- `CRITICAL`.

### Recoverability

- `AUTO_RECOVERABLE`;
- `REQUIRES_REVIEW`;
- `REQUIRES_SOURCE_CORRECTION`;
- `NOT_RECOVERABLE`.

Gli errori non devono essere sanitizzati al punto da perdere la causa, ma locator e valori sensibili devono essere protetti.

## 16. Validation strategy

Ogni manifest attraversa:

1. validazione JSON sintattica;
2. risoluzione `schemaId` e `schemaVersion`;
3. JSON Schema validation;
4. semantic validation cross-field;
5. referential validation, se il catalogo è disponibile;
6. policy validation;
7. esito `ACCEPT`, `ACCEPT_WITH_WARNINGS`, `QUARANTINE`, `REJECT`.

JSON Schema non è sufficiente per regole come:

- `completedAtUtc >= startedAtUtc`;
- `VERIFIED` richiede evidence;
- frame summary riconciliato con i frame;
- calibration compatibility;
- identità del volume;
- lineage senza cicli.

## 17. Canonical serialization e checksum

Quando un manifest deve essere checksummed:

- encoding UTF-8 senza BOM, salvo standard differente approvato;
- line ending e canonical JSON definiti;
- ordine semantico delle proprietà non deve alterare il significato;
- il checksum pubblicato indica algoritmo e profilo di canonicalizzazione;
- timestamp dinamici non vengono rigenerati durante la verifica.

Il profilo canonico definitivo resta da scegliere.

## 18. Valid example requirements

Ogni schema implementato dovrà includere almeno:

- esempio minimo valido;
- esempio completo valido;
- esempio con unknown ammessi;
- esempio con estensione vendor-specific;
- esempio di versione minor successiva compatibile.

## 19. Invalid example requirements

Almeno:

- schemaVersion mancante;
- ID non valido;
- enum sconosciuto non gestito;
- size negativa;
- timestamp non UTC dove richiesto;
- `TRANSFER_VERIFIED` senza evidence;
- processing completed senza output;
- source cleanup autorizzato nel profilo pilot;
- asset RAW senza locator;
- manifest contenente campo sospetto `password`, `token` o `secret`.

## 20. Security controls

- secret-pattern scan sui manifest;
- URI con credenziali embedded vietati;
- path pubblicati sanitizzabili;
- seriali hardware classificabili come metadata protetti;
- identity display name non sostituisce identity ID;
- manifest pubblicabili e manifest operativi possono avere profili distinti;
- sanitizzazione deve preservare conteggi, ID, checksum degli asset e relazioni.

## 21. Mapping con DSDM-002

| Contratto | Entità logiche principali |
|---|---|
| Session Manifest | ScientificProject, ObservationSession, AcquisitionFrame summary |
| Asset Manifest | ScientificAsset, AcquisitionFrame, StorageLocator, IntegrityRecord |
| Inventory Run | InventorySource, InventoryRun, InventoryEntry summary, Finding |
| Transfer Run | ObservationSession, StorageLocator, IntegrityRecord, audit events |
| Calibration Set | CalibrationSet, CalibrationSetMember |
| Processing Run | ProcessingRun, ProcessingStep, ProcessingInput, ProcessingOutput |

Il manifest può denormalizzare dati per portabilità; il catalogo resta responsabile della normalizzazione e della referential integrity.

## 22. Contract registry

Il futuro registry dovrà registrare:

- schema ID;
- versione;
- stato (`DRAFT`, `ACTIVE`, `DEPRECATED`, `RETIRED`);
- owner;
- repository path;
- checksum;
- data pubblicazione;
- predecessor e successor;
- compatibilità dichiarata;
- consumer noti;
- migration guide.

Nessuno schema `DRAFT` è autorizzato in produzione.

## 23. Evidence previste

| Evidence ID | Descrizione | Stato |
|---|---|---|
| `E-DSDM003-01` | schema inventory e checksum | Not produced |
| `E-DSDM003-02` | valid example validation report | Not produced |
| `E-DSDM003-03` | invalid example rejection report | Not produced |
| `E-DSDM003-04` | compatibility test matrix | Not produced |
| `E-DSDM003-05` | secret-pattern scan | Not produced |
| `E-DSDM003-06` | semantic validator report | Not produced |
| `E-DSDM003-07` | independent contract review | Not produced |

## 24. Validation matrix

| ID | Verifica | Stato |
|---|---|---|
| CT-01 | tutti i manifest hanno envelope comune | Documentale |
| CT-02 | versioning segue regole MAJOR/MINOR/PATCH | Documentale |
| CT-03 | mapping DSDM-002 completo | Documentale |
| CT-04 | session manifest riconcilia summary e frame | Da implementare |
| CT-05 | asset manifest supporta sample NINA reale | Da testare |
| CT-06 | transfer manifest impedisce cleanup pilot | Da implementare |
| CT-07 | processing completed richiede output | Da implementare |
| CT-08 | unknown fields compatibili nella stessa major | Da testare |
| CT-09 | major incompatibile rifiutata | Da testare |
| CT-10 | secret scan blocca payload vietati | Da implementare |
| CT-11 | canonical serialization ripetibile | Da definire/testare |
| CT-12 | esempi invalidi rifiutati | Da implementare |

## 25. Acceptance criteria DSDM-003

La baseline documentale è completa quando:

- envelope e tipi comuni sono definiti;
- i manifest principali sono identificati;
- versioning e compatibility policy sono espliciti;
- i contratti sono mappati a DSDM-002;
- validation sintattica e semantica sono separate;
- error model e security controls sono definiti;
- esempi validi e invalidi sono specificati;
- nessuno schema o validator non esistente è dichiarato implementato.

La chiusura implementativa richiederà invece schemi reali, test automatici ed evidence.

## 26. Stato corrente

La baseline dei contratti è definita a livello documentale.

Non sono ancora presenti:

- file `.schema.json`;
- contract registry operativo;
- validator;
- test suite;
- manifest prodotti da script reali;
- canonical serialization profile;
- migration adapter;
- CI contract validation.

## 27. Prossimo passo

Il prossimo deliverable è **DSDM-004 — Session Importer Architecture and Safe Transfer Design**.

Dovrà definire:

- precheck PC → EAGLE;
- accesso SMB read-only;
- parser filename NINA;
- grouping sessioni e target;
- directory staging;
- struttura destinazione;
- collision policy;
- count/byte/hash verification;
- dry-run e `-WhatIf`;
- finestra 07:35–08:25;
- recovery e resume;
- manifest prodotti;
- stop conditions;
- piano di test prima della copia reale.
