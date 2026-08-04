# AP13-W02 — Current-State Scientific Asset Inventory Specification

| Campo | Valore |
|---|---|
| Architecture Package | AP-013 — Scientific Image Repository Architecture |
| Work item | AP13-W02 |
| Titolo | Current-State Scientific Asset Inventory Specification |
| Identificativo | SIR-INV-001 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `architecture/ap-013-package-initiation` |
| Data | 04/08/2026 |
| Autorità | Digital StarGate Chief Architect |
| Sponsor | Project Owner / Architecture Sponsor — Massimo Mainini |
| Stato | Specification complete — real inventory collection not started |
| Dipendenze | AP-013; SIR-VIS-001; AP-002; AP-006; AP-009 |

## 1. Scopo

SIR-INV-001 definisce il modello, le regole e le evidenze necessarie per censire il patrimonio scientifico corrente di Digital StarGate senza modificare, rinominare, spostare o cancellare alcun file.

L'inventario deve produrre una fotografia verificabile dello stato attuale degli asset scientifici e tecnici, includendo almeno ubicazione logica, formato, dimensione, data, classificazione, sessione o target quando desumibili, stato di integrità e qualità dei metadati.

Questa specifica non costituisce l'inventario reale. Nessun percorso, volume, numero di file, checksum o asset esistente viene dichiarato finché non viene raccolto e verificato.

## 2. Obiettivi

- identificare le sorgenti fisiche e logiche che contengono asset scientifici;
- contare file e volume per formato, classe, anno, target e storage source;
- rilevare duplicati probabili e duplicati verificati;
- rilevare file privi di contesto, metadata o classificazione;
- separare RAW originali, calibration, master, intermedi e prodotti finali;
- raccogliere metadata di filesystem senza alterare gli asset;
- predisporre hashing e verifica di integrità in fasi autorizzate;
- costruire la baseline quantitativa per capacity, retention e migration planning;
- produrre evidence ripetibili e confrontabili nel tempo.

## 3. Principi vincolanti

1. **Read-only first** — la raccolta iniziale utilizza esclusivamente operazioni di lettura.
2. **No silent normalization** — path, nomi e metadata vengono registrati come osservati.
3. **No inferred truth** — target, sessione, strumento o classe non certi sono marcati `unknown` o `candidate`.
4. **Identity is not path** — il path corrente è un locator, non l'identità permanente dell'asset.
5. **Hashing is controlled** — il calcolo checksum è eseguito solo quando autorizzato e con impatto I/O valutato.
6. **Original timestamps are preserved** — nessuna operazione deve modificare access time o altri timestamp quando evitabile.
7. **Evidence is immutable** — ogni run di inventario produce manifest, log, parametri e checksum propri.
8. **Personal and secret data minimization** — credenziali, token e contenuti non necessari non vengono raccolti.
9. **Unknown remains visible** — incompletezza e ambiguità sono parte dell'evidence.
10. **No migration during discovery** — discovery, classificazione e migrazione sono fasi separate.

## 4. Scope dell'inventario

### Asset in scope

- RAW light frame;
- bias, dark, flat e dark-flat originali;
- master calibration frame;
- frame calibrati;
- frame registrati;
- integrazioni e master light;
- file XISF intermedi e finali;
- file FITS e FIT;
- TIFF e TIF;
- JPEG, JPG e PNG finali o di preview;
- progetti PixInsight;
- process icon, process container, script e workflow correlati;
- maschere e immagini di supporto;
- log di acquisizione e processing;
- manifest, note e report associati alle sessioni;
- file sidecar e metadata tecnici utili.

### Sorgenti candidate in scope

- workstation di acquisizione;
- workstation di processing;
- dischi locali;
- NAS o share di rete;
- dischi esterni e supporti rimovibili;
- storage cloud o object storage, se autorizzato;
- directory di esportazione o pubblicazione;
- repository contenenti script, workflow e manifest.

Ogni sorgente deve essere autorizzata esplicitamente prima della scansione.

### Out of scope

- modifica dei file;
- rinomina o riorganizzazione delle directory;
- deduplication automatica;
- eliminazione di asset;
- upload verso nuovi storage;
- modifica dei metadata FITS/XISF;
- accesso a credenziali o aree non autorizzate;
- scansione di dispositivi fisici dell'osservatorio;
- ricostruzione retroattiva della provenance come se fosse evidence originale.

## 5. Unità di inventario

L'inventario distingue quattro livelli:

| Livello | Descrizione |
|---|---|
| `InventorySource` | volume, share, directory radice, bucket o repository autorizzato |
| `InventoryRun` | singola esecuzione controllata su una o più source |
| `InventoryEntry` | singolo file, oggetto o artefatto osservato |
| `InventoryFinding` | anomalia, rischio, duplicato, gap o qualità insufficiente rilevata |

Un `InventoryRun` non modifica i risultati di una run precedente. Ogni nuova esecuzione produce una nuova evidence set.

## 6. Modello minimo di InventorySource

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `sourceId` | sì | identificatore stabile della sorgente di inventario |
| `sourceType` | sì | `LOCAL_VOLUME`, `NETWORK_SHARE`, `EXTERNAL_MEDIA`, `OBJECT_STORAGE`, `REPOSITORY`, `OTHER` |
| `logicalName` | sì | nome descrittivo non sensibile |
| `rootLocator` | sì | locator autorizzato; può essere sanitizzato nella pubblicazione |
| `hostOrService` | no | host o servizio che espone la sorgente |
| `owner` | sì | responsabile della sorgente |
| `accessMode` | sì | deve essere `READ_ONLY` per la discovery iniziale |
| `authorizationReference` | sì | riferimento all'autorizzazione della scansione |
| `filesystemOrProtocol` | no | NTFS, ext4, SMB, NFS, S3-compatible o altro |
| `estimatedCapacityBytes` | no | capacità nota o rilevata |
| `encryptionState` | no | stato noto, `unknown` se non verificato |
| `backupState` | no | stato dichiarato, non assunto |
| `notes` | no | limitazioni o condizioni operative |

## 7. Modello minimo di InventoryRun

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `inventoryRunId` | sì | identificatore univoco della run |
| `schemaVersion` | sì | versione dello schema usato |
| `startedAtUtc` | sì | inizio raccolta |
| `completedAtUtc` | no | fine raccolta |
| `operator` | sì | persona o service identity che esegue la raccolta |
| `toolName` | sì | strumento o script utilizzato |
| `toolVersion` | sì | versione o commit dello strumento |
| `commandOrProfile` | sì | parametri o profilo di esecuzione sanitizzato |
| `sourceIds` | sì | sorgenti incluse |
| `collectionMode` | sì | `METADATA_ONLY`, `METADATA_AND_HASH`, `SAMPLE_HASH`, `OTHER` |
| `hashAlgorithm` | no | algoritmo usato quando previsto |
| `exclusionRules` | sì | path, estensioni o pattern esclusi |
| `followSymlinks` | sì | deve essere esplicito |
| `resultStatus` | sì | `COMPLETED`, `PARTIAL`, `FAILED`, `CANCELLED` |
| `entryCount` | no | numero totale di entry raccolte |
| `errorCount` | no | numero errori |
| `manifestSha256` | no | checksum del manifest prodotto |
| `logSha256` | no | checksum del log della run |
| `limitations` | no | gap e vincoli osservati |

## 8. Modello minimo di InventoryEntry

### Identità e locator

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `entryId` | sì | identificatore dell'entry nella run |
| `inventoryRunId` | sì | run che ha osservato l'entry |
| `sourceId` | sì | source di provenienza |
| `relativeLocator` | sì | path o key relativo alla source |
| `fileName` | sì | nome osservato |
| `extension` | no | estensione normalizzata separata dal nome |
| `locatorSanitized` | sì | indica se il locator pubblicato è sanitizzato |

### Caratteristiche fisiche

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `sizeBytes` | sì | dimensione osservata |
| `createdAt` | no | timestamp disponibile dal filesystem |
| `modifiedAt` | no | timestamp disponibile dal filesystem |
| `accessedAtCollected` | no | raccolto solo se non altera la source o se già disponibile |
| `readOnlyFlag` | no | attributo osservato, non prova di immutabilità |
| `hiddenFlag` | no | attributo osservato |
| `filesystemId` | no | inode, file ID o equivalente quando disponibile e non sensibile |

### Formato e classificazione

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `detectedFormat` | sì | formato rilevato o `UNKNOWN` |
| `formatDetectionMethod` | sì | `EXTENSION`, `SIGNATURE`, `HEADER`, `MANUAL`, `UNKNOWN` |
| `assetClass` | sì | classificazione AP-013 o `UNCLASSIFIED` |
| `classificationConfidence` | sì | `CONFIRMED`, `PROBABLE`, `CANDIDATE`, `UNKNOWN` |
| `mediaType` | no | MIME o media type quando rilevabile |
| `compressionState` | no | compresso, non compresso o unknown |

### Contesto scientifico candidato

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `targetNameObserved` | no | valore osservato da path, filename o header |
| `observationDateObserved` | no | data osservata, non corretta automaticamente |
| `sessionCandidate` | no | raggruppamento candidato |
| `frameTypeObserved` | no | LIGHT, DARK, FLAT, BIAS, DARKFLAT o unknown |
| `filterObserved` | no | filtro osservato |
| `exposureSecondsObserved` | no | esposizione osservata |
| `binningObserved` | no | binning osservato |
| `cameraObserved` | no | camera osservata |
| `telescopeObserved` | no | telescopio o OTA osservato |
| `gainObserved` | no | gain osservato |
| `offsetObserved` | no | offset osservato |
| `temperatureObserved` | no | temperatura sensore osservata |
| `metadataSource` | no | filesystem, FITS header, XISF property, filename, manual o altro |

I campi scientifici sono registrati come osservati. La normalizzazione canonica appartiene ad AP13-W04.

### Integrità

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `hashStatus` | sì | `NOT_REQUESTED`, `COMPUTED`, `FAILED`, `PARTIAL` |
| `hashAlgorithm` | no | algoritmo usato |
| `hashValue` | no | valore del checksum |
| `hashComputedAtUtc` | no | timestamp del calcolo |
| `readError` | no | errore di lettura sanitizzato |
| `integrityStatus` | sì | `NOT_VERIFIED`, `VERIFIED_ONCE`, `MISMATCH`, `UNREADABLE`, `UNKNOWN` |

Un checksum calcolato una sola volta identifica il contenuto osservato, ma non dimostra da solo durabilità o integrità nel tempo.

### Provenance e qualità dell'inventario

| Campo | Obbligatorio | Descrizione |
|---|---:|---|
| `discoveryMethod` | sì | scanner, repository query, manual record o altro |
| `metadataCompleteness` | sì | percentuale o classe definita dal profilo |
| `qualityFlags` | sì | lista anche vuota di flag |
| `duplicateCandidateGroup` | no | gruppo di duplicati candidati |
| `duplicateStatus` | sì | `NOT_EVALUATED`, `CANDIDATE`, `HASH_CONFIRMED`, `NOT_DUPLICATE` |
| `reviewStatus` | sì | `NOT_REVIEWED`, `REVIEWED`, `NEEDS_REVIEW` |
| `notes` | no | note dell'operatore o del curator |

## 9. Classificazione iniziale

Il campo `assetClass` usa inizialmente i valori definiti da AP-013:

- `RAW_ORIGINAL`
- `CALIBRATION_ORIGINAL`
- `CALIBRATION_MASTER`
- `CALIBRATED`
- `REGISTERED`
- `INTEGRATED`
- `PROCESSING_INTERMEDIATE`
- `FINAL_SCIENTIFIC`
- `FINAL_PUBLICATION`
- `DOCUMENTATION`
- `UNCLASSIFIED`

La classificazione automatica deve produrre una confidence. Nessuna regola basata soltanto sul nome del file può produrre `CONFIRMED` senza un criterio aggiuntivo approvato.

## 10. Quality flags iniziali

| Flag | Significato |
|---|---|
| `MISSING_EXTENSION` | estensione assente |
| `UNKNOWN_FORMAT` | formato non identificato |
| `UNREADABLE` | file non leggibile |
| `ZERO_LENGTH` | dimensione pari a zero |
| `MISSING_DATE` | nessuna data scientifica o di sessione ricavabile |
| `MISSING_TARGET` | target non ricavabile |
| `MISSING_FRAME_TYPE` | tipo frame non ricavabile |
| `PATH_AMBIGUOUS` | path non sufficiente a classificare l'asset |
| `NAME_COLLISION` | stesso nome in locator differenti |
| `DUPLICATE_CANDIDATE` | possibile duplicato non ancora confermato |
| `HASH_MISMATCH` | checksum differente rispetto a evidence precedente |
| `ORPHAN_DERIVED_ASSET` | prodotto derivato senza input o sessione identificabili |
| `ORPHAN_CALIBRATION` | calibration non collegabile a setup o periodo |
| `UNSUPPORTED_FORMAT` | formato riconosciuto ma non incluso nel profilo corrente |
| `METADATA_CONFLICT` | valori discordanti tra fonti |
| `MANUAL_REVIEW_REQUIRED` | revisione umana necessaria |

I flag non autorizzano correzioni automatiche.

## 11. Strategia di duplicazione

La valutazione dei duplicati avviene per livelli:

1. stesso `sizeBytes` e stesso nome — candidato debole;
2. stesso `sizeBytes` e metadata compatibili — candidato;
3. stesso checksum — contenuto binario identico;
4. stesso contenuto ma metadata esterni differenti — richiede review;
5. asset derivati visivamente simili — non classificati come duplicati senza prova binaria o semantica approvata.

Nessun file viene eliminato o consolidato durante AP13-W02.

## 12. Profili di raccolta

### Profilo P0 — Source discovery

Raccoglie:

- source autorizzate;
- capacità disponibile, se leggibile;
- filesystem o protocollo;
- accessibilità;
- limitazioni.

Non enumera ancora tutti i file.

### Profilo P1 — Metadata-only inventory

Raccoglie:

- locator relativo;
- nome;
- dimensione;
- timestamp disponibili;
- estensione e formato candidato;
- classificazione candidata.

Non legge il contenuto completo e non calcola checksum.

### Profilo P2 — Header-enriched inventory

Aggiunge lettura controllata di:

- header FITS;
- proprietà XISF supportate;
- metadata di progetto o sidecar approvati.

Non modifica i file.

### Profilo P3 — Sample hashing

Calcola checksum su un campione approvato per:

- valutare performance e impatto I/O;
- verificare la procedura;
- stimare la durata della full hash campaign.

### Profilo P4 — Full hashing

Calcola checksum degli asset autorizzati. Richiede:

- finestra approvata;
- impatto valutato;
- algoritmo approvato;
- log ed evidence completi;
- gestione di retry e file unreadable.

Il passaggio tra profili richiede autorizzazione esplicita.

## 13. Regole di esclusione

Le esclusioni devono essere versionate e motivate. Categorie candidate:

- directory temporanee del sistema;
- cache applicative;
- cestini e recycle bin;
- thumbnail rigenerabili non governate;
- file lock e temporary file;
- backup tecnici duplicativi già coperti da una source separata;
- directory contenenti secret o profili utente non necessari;
- mount non autorizzati;
- symlink che escono dalla source autorizzata.

Il numero di file esclusi per regola deve essere registrato quando tecnicamente possibile.

## 14. Gestione symlink, junction e hard link

- il comportamento `followSymlinks` deve essere esplicito;
- default iniziale: non seguire link simbolici fuori dalla root autorizzata;
- junction e mount point devono essere rilevati e registrati;
- hard link non devono essere conteggiati automaticamente come contenuti indipendenti senza verifica dell'identità filesystem;
- loop di filesystem devono essere prevenuti.

## 15. Privacy e sanitizzazione

Il manifest operativo può contenere locator completi quando necessario e autorizzato. La versione pubblicata nel repository documentale deve poter sostituire:

- username locali;
- nomi host sensibili;
- lettere di unità o share riservate;
- token embedded in URI;
- informazioni personali non necessarie.

La sanitizzazione non deve alterare conteggi, dimensioni, hash o relazioni tra entry. Deve essere documentata e ripetibile.

## 16. Output obbligatori di una run reale

Ogni run autorizzata dovrà produrre almeno:

1. `inventory-run.json` — metadata della run;
2. `inventory-sources.json` — source incluse;
3. `inventory-entries.csv` oppure formato equivalente approvato;
4. `inventory-findings.csv` o JSON;
5. `inventory-summary.json` — aggregati quantitativi;
6. `inventory-errors.log` — errori sanitizzati;
7. `inventory-checksums.txt` — hash degli output di evidence;
8. `README.md` — scope, comando, limitazioni e interpretazione;
9. eventuale `sanitization-map` conservata in area protetta, non pubblicata se sensibile.

## 17. Summary metrics minime

- numero di source;
- numero totale di file;
- volume totale in byte;
- conteggio e volume per estensione;
- conteggio e volume per `assetClass`;
- conteggio per anno o periodo osservato;
- conteggio per target candidato;
- file non classificati;
- file unreadable;
- file zero-length;
- duplicati candidati;
- duplicati confermati tramite hash;
- asset senza target;
- asset senza data;
- asset derivati orfani;
- distribuzione della metadata completeness;
- errori per source;
- durata della run e throughput osservato.

Le metriche sono descrittive e non costituiscono automaticamente KPI di qualità approvati.

## 18. Evidence identifiers candidati

| Evidence ID | Descrizione | Stato |
|---|---|---|
| `E-AP13-W02-01` | autorizzazione e scope delle source | Not collected |
| `E-AP13-W02-02` | tool, versione e profilo di raccolta | Not collected |
| `E-AP13-W02-03` | source discovery output | Not collected |
| `E-AP13-W02-04` | metadata-only inventory manifest | Not collected |
| `E-AP13-W02-05` | header-enriched sample | Not collected |
| `E-AP13-W02-06` | sample hashing result | Not collected |
| `E-AP13-W02-07` | summary and findings | Not collected |
| `E-AP13-W02-08` | independent inventory review | Not collected |

Questi identificatori definiscono l'evidence set previsto; non attestano che le prove siano state eseguite.

## 19. Validation matrix

| ID | Verifica | Evidence attesa | Stato |
|---|---|---|---|
| INV-01 | source autorizzate e identificate | E-AP13-W02-01 | Not executed |
| INV-02 | accesso read-only dimostrato | log e permission check | Not executed |
| INV-03 | tool e parametri riproducibili | E-AP13-W02-02 | Not executed |
| INV-04 | nessuna modifica dei file durante P1 | before/after sample metadata | Not executed |
| INV-05 | esclusioni applicate e contate | run log e summary | Not executed |
| INV-06 | symlink e mount gestiti in sicurezza | scenario test | Not executed |
| INV-07 | formati rilevati correttamente su sample | E-AP13-W02-05 | Not executed |
| INV-08 | classificazione con confidence | sample review | Not executed |
| INV-09 | hashing ripetibile sul campione | E-AP13-W02-06 | Not executed |
| INV-10 | duplicati hash-confirmed corretti | sample review | Not executed |
| INV-11 | errori e unreadable non interrompono silentemente la run | failure test | Not executed |
| INV-12 | sanitizzazione non altera aggregati e hash asset | comparison evidence | Not executed |
| INV-13 | summary riconciliata con entries | reconciliation test | Not executed |
| INV-14 | review indipendente | E-AP13-W02-08 | Not executed |

## 20. Stop conditions

La raccolta deve essere interrotta se:

- la source non è quella autorizzata;
- il tool richiede permessi di scrittura non previsti;
- vengono rilevate modifiche ai file;
- il carico I/O impatta attività operative o acquisizioni;
- compaiono secret o dati non previsti negli output;
- il path attraversa mount o link non autorizzati;
- gli errori rendono il risultato non interpretabile;
- l'algoritmo o il tool differiscono dalla baseline approvata;
- non è possibile preservare log e evidence della run.

## 21. Acceptance criteria AP13-W02

AP13-W02 può essere dichiarato completato soltanto quando:

- questa specifica è approvata e pubblicata;
- almeno una source reale è autorizzata e identificata;
- viene eseguito almeno il profilo P1 in modalità read-only;
- tool, versione, parametri ed esclusioni sono registrati;
- gli output obbligatori sono prodotti e checksummed;
- summary ed entries sono riconciliati;
- gap, unknown e limitazioni sono espliciti;
- non viene effettuata alcuna migrazione o modifica degli asset;
- una review indipendente verifica completezza e coerenza dell'inventario.

Fino a quel momento lo stato resta `SPECIFICATION COMPLETE — COLLECTION NOT STARTED`.

## 22. Stato corrente

La specifica del modello di inventario è completa.

Non sono state ancora identificate o scansionate source reali. Non sono noti o dichiarati:

- numero di file;
- volume totale;
- formati effettivamente presenti;
- distribuzione per target o anno;
- numero di duplicati;
- stato di integrità;
- qualità dei metadata;
- stato di backup;
- capacità o crescita dello storage.

## 23. Prossimo passo autorizzato

Il prossimo passo è predisporre **E-AP13-W02-01 — Source Authorization and Scope Record**.

Prima della raccolta reale devono essere indicati:

- source da censire;
- owner;
- locator o descrizione della root;
- host o supporto;
- modalità di accesso read-only;
- finestre operative;
- esclusioni;
- eventuale necessità di sanitizzazione;
- approvazione esplicita alla sola discovery P0/P1.
