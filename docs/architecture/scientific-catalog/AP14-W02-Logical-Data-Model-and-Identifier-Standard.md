# AP14-W02 — Logical Data Model and Identifier Standard

| Campo | Valore |
|---|---|
| Architecture Package | AP-014 — Scientific Observation Catalog and Search |
| Work Package | AP14-W02 — Logical Data Model and Identifier Standard |
| Identificativo | SOCS-LDM-001 |
| Versione | 1.0 |
| Data | 05/08/2026 |
| Autorità | Digital StarGate Chief Architect |
| Sponsor | Project Owner / Architecture Sponsor — Massimo Mainini |
| Stato | Logical baseline ready for review |
| Dipendenze | AP14-W01; AP-014; AP-013; DSDM-001; Scientific Data Engine 2.1 |
| Successivo | AP14-W03 — Catalog Projection and Index Build |

## 1. Scopo

Questo documento traduce il modello concettuale `SOCS-CM-001` in uno schema logico implementabile per il Catalogo Osservativo di Digital StarGate.

La baseline definisce:

- entità logiche;
- attributi tipizzati;
- chiavi primarie e riferimenti;
- vincoli di integrità;
- standard degli identificatori;
- versioning e supersession;
- contratti JSON minimi;
- boundary tra record autorevoli e proiezioni derivate.

Il documento non impone ancora un database fisico o un motore di indicizzazione specifico.

## 2. Convenzioni di modellazione

### 2.1 Tipi logici

| Tipo | Significato |
|---|---|
| `string` | testo UTF-8 |
| `identifier` | identificatore stabile conforme a questo standard |
| `timestamp` | ISO 8601 UTC con suffisso `Z` |
| `local-date` | data locale `YYYY-MM-DD` |
| `decimal` | numero decimale senza unità implicita |
| `integer` | intero con segno |
| `boolean` | `true` o `false` |
| `enum` | valore appartenente a un vocabolario controllato |
| `uri` | URI assoluto o relativo governato |
| `digest` | digest nel formato `<algorithm>:<hex>` |
| `object` | oggetto strutturato |
| `array<T>` | collezione ordinata o non ordinata secondo il contratto |

### 2.2 Nullability

- i campi obbligatori non possono essere assenti;
- i campi non noti usano `null`, non stringhe vuote;
- `unknown` è ammesso solo nei vocabolari che lo prevedono esplicitamente;
- un campo `null` non implica errore se il contratto lo dichiara opzionale.

### 2.3 Versioning

Ogni entità catalogata deve includere:

- `schemaVersion`;
- `recordVersion`;
- `createdAtUtc`;
- `updatedAtUtc`;
- `sourceSystem`;
- `sourceVersion`;
- `sourceDigest`.

Le modifiche sostanziali incrementano `recordVersion`. Le correzioni non distruttive non riutilizzano versioni precedenti.

## 3. Standard degli identificatori

### 3.1 Regole generali

Gli identificatori:

- sono stabili e immutabili;
- non dipendono da path, lettere di unità o nomi file;
- usano ASCII maiuscolo, cifre e trattino;
- non contengono spazi;
- non vengono riutilizzati dopo withdrawal o supersession;
- devono essere univoci nel relativo namespace.

### 3.2 Formati canonici

| Entità | Pattern |
|---|---|
| Scientific Project | `^PRJ-[0-9]{4}-[0-9]{3}$` |
| Observation Campaign | `^CAM-[0-9]{4}-[0-9]{3}$` |
| Scientific Target | `^TGT-[A-Z0-9]+-[A-Z0-9-]+$` |
| Observation | `^OBS-[0-9]{8}-[0-9]{3}$` |
| Observation Session | identificatore stabile già governato dal Scientific Data Engine |
| Acquisition Profile | `^ACP-[A-Z0-9-]+-[0-9]{3}$` |
| Acquisition | `^ACQ-[A-Z0-9-]+-[0-9]{3}$` |
| Calibration Set | `^CAL-[0-9]{6}-[0-9]{3}$` |
| Catalog Item | `^CAT-[A-Z]+-[A-Z0-9-]+$` |
| Search Document | `^SRCH-[A-Z0-9-]+-V[0-9]+$` |
| Index Build | `^IDX-[0-9]{8}T[0-9]{6}Z$` |
| Reconciliation Record | `^REC-[A-Z0-9-]+-[0-9]{3}$` |

## 4. Entità logiche

### 4.1 `scientific_project`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `projectId` | identifier | sì | PK |
| `projectName` | string | sì | lunghezza 1..200 |
| `objective` | string | no | max 4000 |
| `projectType` | enum | sì | vocabolario governato |
| `priority` | integer | sì | 1..5 |
| `status` | enum | sì | ProjectStatus |
| `ownerId` | identifier | no | riferimento esterno |
| `startedAt` | local-date | no | |
| `targetCompletionDate` | local-date | no | >= `startedAt` |
| `completedAt` | local-date | no | >= `startedAt` |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.2 `observation_campaign`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `campaignId` | identifier | sì | PK |
| `projectId` | identifier | sì | FK → scientific_project |
| `campaignName` | string | sì | 1..200 |
| `objective` | string | no | max 4000 |
| `validFrom` | local-date | no | |
| `validTo` | local-date | no | >= `validFrom` |
| `status` | enum | sì | CampaignStatus |
| `completionCriteria` | object | no | schema versionato |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.3 `scientific_target`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `targetId` | identifier | sì | PK |
| `canonicalName` | string | sì | univoco nel namespace |
| `alternativeNames` | array<string> | no | valori univoci |
| `targetType` | enum | sì | TargetType |
| `rightAscensionDeg` | decimal | no | 0 <= x < 360 |
| `declinationDeg` | decimal | no | -90 <= x <= 90 |
| `constellation` | string | no | codice o nome governato |
| `catalogReferences` | array<object> | no | namespace + value |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.4 `observation`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `observationId` | identifier | sì | PK |
| `campaignId` | identifier | sì | FK → observation_campaign |
| `targetId` | identifier | sì | FK → scientific_target |
| `observationTitle` | string | sì | 1..250 |
| `scientificObjective` | string | no | max 4000 |
| `observationMode` | enum | sì | ObservationMode |
| `priority` | integer | sì | 1..5 |
| `status` | enum | sì | ObservationStatus |
| `requiredIntegrationByFilter` | object | no | secondi per filterId |
| `achievedIntegrationByFilter` | object | no | secondi per filterId |
| `completionState` | enum | sì | CompletionState |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.5 `observation_session`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `sessionId` | identifier | sì | PK |
| `observationId` | identifier | sì | FK → observation |
| `startedAtUtc` | timestamp | no | |
| `completedAtUtc` | timestamp | no | >= `startedAtUtc` |
| `localObservingDate` | local-date | sì | |
| `observatoryId` | identifier | sì | riferimento AP-006 |
| `instrumentConfigurationId` | identifier | sì | FK logica |
| `operatorId` | identifier | no | |
| `sessionStatus` | enum | sì | SessionStatus |
| `qualityState` | enum | sì | QualityState |
| `sourceReference` | uri | no | |
| `transferState` | enum | no | TransferState |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.6 `acquisition_profile`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `acquisitionProfileId` | identifier | sì | PK |
| `instrumentConfigurationId` | identifier | sì | |
| `imageType` | enum | sì | ImageType |
| `filterId` | identifier | no | obbligatorio per LIGHT/FLAT |
| `exposureSeconds` | decimal | sì | > 0 |
| `binningX` | integer | sì | >= 1 |
| `binningY` | integer | sì | >= 1 |
| `gain` | decimal | no | |
| `offset` | decimal | no | |
| `sensorTemperatureC` | decimal | no | |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.7 `acquisition`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `acquisitionId` | identifier | sì | PK |
| `sessionId` | identifier | sì | FK → observation_session |
| `acquisitionProfileId` | identifier | sì | FK → acquisition_profile |
| `sequenceNumber` | integer | sì | >= 1; unico per sessione |
| `startedAtUtc` | timestamp | no | |
| `completedAtUtc` | timestamp | no | >= `startedAtUtc` |
| `frameCountPlanned` | integer | no | >= 0 |
| `frameCountCaptured` | integer | sì | >= 0 |
| `frameCountAccepted` | integer | sì | >= 0 |
| `frameCountRejected` | integer | sì | >= 0 |
| `integrationSecondsCaptured` | decimal | sì | >= 0 |
| `integrationSecondsAccepted` | decimal | sì | 0..captured |
| `qualityState` | enum | sì | QualityState |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.8 `calibration_set`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `calibrationSetId` | identifier | sì | PK |
| `calibrationType` | enum | sì | DARK, FLAT, BIAS, DARKFLAT |
| `instrumentConfigurationId` | identifier | sì | |
| `cameraId` | identifier | sì | |
| `filterId` | identifier | no | richiesto per FLAT |
| `exposureSeconds` | decimal | no | richiesto per DARK/DARKFLAT |
| `gain` | decimal | no | |
| `offset` | decimal | no | |
| `sensorTemperatureC` | decimal | no | |
| `validFrom` | local-date | no | |
| `validTo` | local-date | no | >= `validFrom` |
| `qualityState` | enum | sì | QualityState |
| `recordVersion` | integer | sì | >= 1 |
| `sourceDigest` | digest | sì | |

### 4.9 `acquisition_calibration`

Tabella logica di associazione N:M.

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `acquisitionId` | identifier | sì | PK parziale; FK |
| `calibrationSetId` | identifier | sì | PK parziale; FK |
| `compatibilityState` | enum | sì | COMPATIBLE, CONDITIONAL, INCOMPATIBLE, UNKNOWN |
| `compatibilityEvidence` | uri | no | |

### 4.10 `scientific_asset_reference`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `assetId` | identifier | sì | PK logica da AP-013 |
| `sourceEntityType` | enum | sì | SESSION, ACQUISITION, CALIBRATION, PRODUCT |
| `sourceEntityId` | identifier | sì | |
| `assetClass` | enum | sì | vocabolario AP-013 |
| `format` | string | no | |
| `sizeBytes` | integer | no | >= 0 |
| `integrityState` | enum | sì | vocabolario AP-013 |
| `qualityState` | enum | sì | QualityState |
| `authoritativeRegistry` | uri | sì | |
| `sourceDigest` | digest | sì | digest dell'asset record |

### 4.11 `processing_run_reference`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `processingRunId` | identifier | sì | PK logica da AP-013 |
| `workflowDefinitionId` | identifier | sì | |
| `processingEnvironmentId` | identifier | no | |
| `startedAtUtc` | timestamp | no | |
| `completedAtUtc` | timestamp | no | >= `startedAtUtc` |
| `runStatus` | enum | sì | ProcessingState |
| `qualityState` | enum | sì | QualityState |
| `inputAssetIds` | array<identifier> | sì | almeno 1 |
| `outputAssetIds` | array<identifier> | no | |
| `evidenceReference` | uri | no | |
| `sourceDigest` | digest | sì | |

### 4.12 `catalog_item`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `catalogItemId` | identifier | sì | PK |
| `entityType` | enum | sì | CatalogEntityType |
| `entityId` | identifier | sì | univoco con entityType/version |
| `sourceSystem` | string | sì | |
| `sourceVersion` | string | sì | |
| `sourceDigest` | digest | sì | |
| `catalogState` | enum | sì | CatalogState |
| `qualityState` | enum | sì | QualityState |
| `recordVersion` | integer | sì | >= 1 |
| `indexedAtUtc` | timestamp | no | |
| `lastReconciledAtUtc` | timestamp | no | |
| `reconciliationState` | enum | sì | ReconciliationState |
| `supersedesCatalogItemId` | identifier | no | self-reference |

### 4.13 `search_document`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `searchDocumentId` | identifier | sì | PK |
| `catalogItemId` | identifier | sì | FK → catalog_item |
| `indexBuildId` | identifier | sì | FK → index_build |
| `documentType` | enum | sì | |
| `title` | string | sì | 1..300 |
| `summary` | string | no | max 4000 |
| `normalizedText` | string | sì | |
| `keywords` | array<string> | no | valori normalizzati |
| `facetValues` | object | no | schema versionato |
| `sourceUrl` | uri | sì | |
| `rankingSignals` | object | no | explainable |
| `sourceDigest` | digest | sì | |

### 4.14 `index_build`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `indexBuildId` | identifier | sì | PK |
| `algorithmVersion` | string | sì | |
| `sourceSnapshotDigest` | digest | sì | |
| `startedAtUtc` | timestamp | sì | |
| `completedAtUtc` | timestamp | no | >= started |
| `documentCount` | integer | sì | >= 0 |
| `failureCount` | integer | sì | >= 0 |
| `outputDigest` | digest | no | richiesto se COMPLETED |
| `buildStatus` | enum | sì | STARTED, COMPLETED, PARTIAL, FAILED |
| `evidenceReference` | uri | no | |

### 4.15 `reconciliation_record`

| Campo | Tipo | Obbligatorio | Vincolo |
|---|---|---:|---|
| `reconciliationRecordId` | identifier | sì | PK |
| `indexBuildId` | identifier | sì | FK → index_build |
| `catalogItemId` | identifier | no | FK → catalog_item |
| `sourceDigestExpected` | digest | no | |
| `sourceDigestObserved` | digest | no | |
| `reconciliationState` | enum | sì | ReconciliationState |
| `differenceType` | enum | no | |
| `detectedAtUtc` | timestamp | sì | |
| `resolvedAtUtc` | timestamp | no | >= detected |
| `resolutionReference` | uri | no | |

## 5. Vincoli trasversali

1. `frameCountAccepted + frameCountRejected <= frameCountCaptured`.
2. `integrationSecondsAccepted <= integrationSecondsCaptured`.
3. ogni `search_document` deve riferirsi a un `catalog_item` esistente.
4. ogni `catalog_item` deve conservare `sourceDigest` e `sourceVersion`.
5. un record con `reconciliationState = CONFLICT` non può essere pubblicato come `INDEXED` senza override governato.
6. `outputDigest` è obbligatorio per un `index_build` completato.
7. un `catalog_item` superseded deve indicare il successore o essere referenziato dal nuovo record.
8. i riferimenti ad asset e processing run devono essere risolvibili verso AP-013.
9. il catalogo non può modificare checksum, locator o provenance autorevoli.
10. i timestamp persistiti sono UTC; le date osservative locali sono separate.

## 6. Contratto JSON minimo — Observation Session

```json
{
  "schemaVersion": "1.0",
  "recordVersion": 1,
  "sessionId": "SES-20260709-001",
  "observationId": "OBS-20260709-001",
  "startedAtUtc": "2026-07-09T20:15:00Z",
  "completedAtUtc": "2026-07-10T02:45:00Z",
  "localObservingDate": "2026-07-09",
  "observatoryId": "OBS-MANCIANO-001",
  "instrumentConfigurationId": "IC-SWQ200P-ASI2600MM-001",
  "operatorId": "USR-MASSIMO-MAININI",
  "sessionStatus": "COMPLETED",
  "qualityState": "ACCEPTED",
  "sourceReference": "data/scientific-session-catalog.json#SES-20260709-001",
  "transferState": "COPY_ONLY_COMPLETED",
  "sourceSystem": "Scientific Data Engine",
  "sourceVersion": "2.1",
  "sourceDigest": "sha256:example"
}
```

## 7. Contratto JSON minimo — Catalog Item

```json
{
  "schemaVersion": "1.0",
  "catalogItemId": "CAT-SESSION-SES-20260709-001",
  "entityType": "OBSERVATION_SESSION",
  "entityId": "SES-20260709-001",
  "sourceSystem": "Scientific Data Engine",
  "sourceVersion": "2.1",
  "sourceDigest": "sha256:example",
  "catalogState": "INDEXABLE",
  "qualityState": "ACCEPTED",
  "recordVersion": 1,
  "indexedAtUtc": null,
  "lastReconciledAtUtc": "2026-08-05T16:00:00Z",
  "reconciliationState": "MATCHED",
  "supersedesCatalogItemId": null
}
```

## 8. Contratto JSON minimo — Search Document

```json
{
  "schemaVersion": "1.0",
  "searchDocumentId": "SRCH-CAT-SESSION-SES-20260709-001-V1",
  "catalogItemId": "CAT-SESSION-SES-20260709-001",
  "indexBuildId": "IDX-20260805T160000Z",
  "documentType": "SCIENTIFIC_SESSION",
  "title": "LDN1320 · sessione 2026-07-09",
  "summary": "Sessione LPRO acquisita con Sky-Watcher Quattro 200P.",
  "normalizedText": "ldn1320 lpro sky watcher quattro 200p sessione 2026 07 09",
  "keywords": ["ldn1320", "lpro", "quattro-200p", "2026"],
  "facetValues": {
    "target": ["LDN1320"],
    "year": ["2026"],
    "filter": ["LPRO"],
    "quality": ["ACCEPTED"]
  },
  "sourceUrl": "scientific-session-detail/?sessionId=SES-20260709-001",
  "rankingSignals": {
    "qualityWeight": 1.0,
    "metadataCompleteness": 0.92
  },
  "sourceDigest": "sha256:example"
}
```

## 9. Compatibility e migrazione

La baseline deve poter rappresentare i dataset già usati dal Scientific Data Engine senza richiedere la modifica immediata delle fonti esistenti.

La migrazione iniziale userà adapter di proiezione:

```text
scientific-session-catalog.json
        ↓
Catalog Projection Adapter
        ↓
CatalogItem + SearchDocument
```

Campi mancanti saranno valorizzati a `null` o `UNKNOWN` secondo contratto. Non saranno inventati identificatori autorevoli diversi da quelli dichiarati dalla fonte.

## 10. Acceptance criteria AP14-W02

AP14-W02 può essere dichiarato completato quando:

- le entità logiche principali sono tipizzate;
- chiavi e riferimenti sono espliciti;
- gli identificatori sono standardizzati;
- i vincoli trasversali sono documentati;
- i contratti JSON minimi sono disponibili;
- la compatibilità con il Scientific Data Engine è preservata;
- il modello è accettato come input per AP14-W03.

## 11. Decisione

Il modello logico `SOCS-LDM-001` è dichiarato **ready for review**.

Il prossimo incremento è `AP14-W03 — Catalog Projection and Index Build`.