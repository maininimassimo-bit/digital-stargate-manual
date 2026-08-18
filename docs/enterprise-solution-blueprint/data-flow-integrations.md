# DSG-ESB-003 - Data Flow and External Integrations

| Campo | Valore |
|---|---|
| Documento | Data Flow and External Integrations |
| Identificativo | `DSG-ESB-003` |
| Stato | Proposed architecture baseline |
| Versione | 0.1 |
| Data | 2026-07-26 |
| Roadmap | `DSG-MR-001` |
| Documento padre | [DSG-ESB-001](index.md) |

## Scopo

Documentare i principali flussi dati della piattaforma Digital StarGate e le integrazioni esterne previste, distinguendo cio che e gia documentato da cio che richiede validazione o decisione architetturale futura.

## Principi dei flussi dati

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-ESB-FLW-PRN-001` | Fonte identificabile | Ogni dato deve avere origine, timestamp e dominio sorgente |
| `DSG-ESB-FLW-PRN-002` | Raw preservation | I dati grezzi non vengono eliminati prima della copia e verifica |
| `DSG-ESB-FLW-PRN-003` | Integrity first | Trasferimenti critici richiedono conteggio, hash o controllo equivalente |
| `DSG-ESB-FLW-PRN-004` | Publication after validation | Dashboard e portale pubblicano solo output con quality gate superato o stato esplicito |
| `DSG-ESB-FLW-PRN-005` | Sensitive data minimization | Log e configurazioni pubblicabili devono essere sanitizzati |

## Classi informative principali

| ID | Classe dati | Origine | Destinazione | Retention indicativa | Stato |
|---|---|---|---|---|---|
| `DSG-DATA-RAW-FITS` | FITS grezzi | N.I.N.A. / camere | Raw Data Repository, backup | Lungo termine per frame selezionati | Transition |
| `DSG-DATA-CAL` | Master e dati calibrati | Processing Workspace | Processing Repository, archive | Secondo valore scientifico | Transition |
| `DSG-DATA-IMG-PUB` | Immagini finali | PixInsight / processing | User Portal, archive | Permanente | Transition |
| `DSG-DATA-LOG-APP` | Log N.I.N.A., PHD2, CPWI, ASCOM, Windows | EAGLE | Logging, Data Platform | Allineata alla sessione | Transition |
| `DSG-DATA-ENV` | Meteo e AllSky | Weather Station, AllSky | Monitoring, Analytics, Knowledge Graph | Da validare | Da validare |
| `DSG-DATA-SESSION` | Report sessione | Automation / operatori | Documentation, Analytics, registry | Permanente | Transition |
| `DSG-DATA-KPI` | KPI e quality gates | Analytics | Dashboard, release evidence | Permanente per release | Transition |
| `DSG-DATA-KG` | Entita e relazioni semantiche | Registri, docs, data catalog | Knowledge Graph, AI | TBD | TO-BE |
| `DSG-DATA-AI-AUDIT` | Prompt, output, revisione | AI Assistant | AI audit, governance | Da definire | TBD |
| `DSG-DATA-BACKUP` | Manifest e prove restore | Backup & Recovery | Governance, release evidence | Permanente o policy DR | Transition |

## Flusso 1 - Acquisizione immagini

```text
Target / Session Plan
        |
        v
N.I.N.A. on EAGLE
        |
        +-- ASCOM -> CPWI -> CGX-L
        +-- PHD2 -> guida e dithering
        +-- Camera / focuser / filter wheel
        |
        v
FITS raw + log sessione + metadata
        |
        v
Acquisition Workspace on EAGLE
```

| Campo | Valore |
|---|---|
| Owner logico | Operations Owner / Data Owner |
| Trigger | Sessione osservativa approvata o test controllato |
| Input | Piano sessione, profilo N.I.N.A., stato osservatorio, meteo, readiness |
| Output | FITS raw, log applicativi, report iniziale, anomalie |
| Controlli | Connessione dispositivi, spazio disco, ora sincronizzata, stato Park/Unpark, profilo corretto |
| Errori principali | disconnessione camera, guida persa, plate solving fallito, storage insufficiente |
| Evidenze | Log N.I.N.A., PHD2, CPWI, ASCOM, checklist sessione |

## Flusso 2 - Pipeline elaborazione

```text
FITS raw / calibration frames
        |
        v
Processing Workspace
        |
        +-- calibrazione
        +-- registrazione / integrazione
        +-- quality measurement
        +-- export pubblicabili
        |
        v
Processed dataset + metrics + processing log
```

| Campo | Valore |
|---|---|
| Owner logico | Imaging Owner / Data Owner |
| Tecnologie suggerite | PixInsight, ASTAP per solve, tool FITS approvati, script report controllati |
| Input | FITS raw, dark, flat, bias, metadata sessione |
| Output | master, immagini calibrate, integrazioni, metriche qualita, export PNG/TIFF/JPEG |
| Controlli | Compatibilita calibrazioni, conteggio frame, qualita subframe, versioni tool |
| Dati persistenti | Raw preservati, processed, processing manifest, metriche |
| Stato | Transition; dettagli script e standard output da validare |

## Flusso 3 - Catalogazione

```text
Session report + manifest + dataset
        |
        v
Curated Data Catalog
        |
        +-- dataset registry
        +-- target registry
        +-- quality status
        +-- lineage links
        |
        v
Analytics / Knowledge Graph / Release evidence
```

| Campo | Valore |
|---|---|
| Owner logico | Data Owner |
| Input | Manifest trasferimento, report sessione, metadata FITS, processing output |
| Output | Record catalogo, stato qualita, riferimenti archivio, link a report |
| Controlli | ID sessione univoco, hash o verifica integrita, stato `RAW`, `PROCESSED`, `ARCHIVED`, `PUBLISHED` |
| Interfacce | Markdown registry, CSV/Parquet, warehouse locale, GitHub per evidenze documentali |
| TBD | Schema finale catalogo e livelli di classificazione scientifica |

## Flusso 4 - Knowledge Graph

```text
Roadmap / ADR / DSRA / registri / sessioni / dataset
        |
        v
Traceability Mapper
        |
        v
Knowledge Graph
        |
        +-- query impatto
        +-- supporto AI
        +-- navigazione conoscenza
```

| Campo | Valore |
|---|---|
| Stato | TO-BE / TBD |
| Owner logico | Architecture Owner / Knowledge Owner |
| Input | Documenti MkDocs, registri, ADR, risk/control register, dataset catalog |
| Output | Entita, relazioni, provenance, mapping roadmap -> componenti -> evidenze |
| Controlli | Ogni relazione deve avere fonte; nessuna inferenza non marcata come tale |
| Vincoli | Non sostituisce i documenti ufficiali; li collega semanticamente |

## Flusso 5 - AI Analysis

```text
Domanda / anomalia / report
        |
        v
AI Assistant Runtime
        |
        +-- Retrieval Layer su fonti approvate
        +-- policy IAM e sanitizzazione
        +-- human review quando richiesto
        |
        v
Suggerimento revisionabile + riferimenti + audit
```

| Campo | Valore |
|---|---|
| Stato | TO-BE / TBD |
| Owner logico | Governance Owner / Data Owner |
| Input | Knowledge base approvata, report sessione, log sanitizzati, KPI |
| Output | Sintesi, ipotesi, classificazioni, raccomandazioni non safety |
| Controlli | Human-in-the-loop, audit prompt/output, divieto di azioni autonome su safety |
| Integrazione prevista | OpenAI API o provider approvato; modello e retention da decidere |

## Flusso 6 - Dashboard

```text
Data Catalog / Warehouse / KPI Engine
        |
        v
Dashboard Publisher
        |
        v
MkDocs / User Portal / Release evidence
```

| Campo | Valore |
|---|---|
| Owner logico | Analytics Owner / Release Owner |
| Input | Dataset validati, KPI, quality gate, log aggregati |
| Output | Dashboard statiche, report, trend, stato qualita |
| Controlli | Quality gate ADR-002, definizione KPI, dataset versionati |
| Vincoli | Le dashboard non sono fonte unica di decisione safety |

## Flusso 7 - Pubblicazione

```text
Documentazione / dashboard / release evidence
        |
        v
GitHub branch / review / build
        |
        v
GitHub Pages or static portal
```

| Campo | Valore |
|---|---|
| Owner logico | Documentation Owner / Release Owner |
| Input | Documenti MkDocs, dashboard, release notes, registri |
| Output | Portale pubblicato, changelog, evidenze review |
| Controlli | Build MkDocs, link relativi, assenza segreti, freeze policy |
| Dipendenze | GitHub, MkDocs, governance release |

## Flusso 8 - Archiviazione

```text
EAGLE Acquisition Workspace
        |
        v
Primary Storage on PC / NAS / local archive
        |
        v
Secondary Backup / Cloud Storage / offline copy
        |
        v
Restore evidence and retention registry
```

| Campo | Valore |
|---|---|
| Owner logico | Data Owner / Infrastructure Owner |
| Input | FITS, log, report, processed data, configurations sanitizzate |
| Output | Copie verificate, manifest, prove restore, stato archive |
| Controlli | Due copie su supporti differenti, verifica integrita, restore test periodico |
| TBD | Provider cloud, RTO/RPO, frequenza backup, retention per classi dati |

## Flusso 9 - Alert

```text
Monitoring / Automation / Weather / Storage
        |
        v
Alert Router
        |
        v
Notification channel + escalation log
```

| Campo | Valore |
|---|---|
| Stato | TO-BE / Da validare |
| Trigger | Meteo critico, storage insufficiente, perdita guida, trasferimento fallito, backup fallito |
| Output | Notifica, evento log, issue o entry incident se necessario |
| Vincoli | Gli alert non devono comandare azioni meccaniche non validate |
| TBD | Canali, destinatari, severita e finestre di silenzio |

## Flusso 10 - Logging

```text
N.I.N.A. / PHD2 / CPWI / ASCOM / Windows / RUT955 / AllSky
        |
        v
Local Log Collector
        |
        v
Correlation Index
        |
        v
Incident evidence / analytics / audit archive
```

| Campo | Valore |
|---|---|
| Owner logico | Operations Owner / Security Owner |
| Input | Log applicativi, eventi Windows, eventi rete, log router, log sync |
| Output | Timeline sessione, incident evidence, KPI affidabilita, audit accessi |
| Controlli | Timestamp coerenti, sanitizzazione, retention, correlazione per ID sessione |
| TBD | Formato standard log correlation e soglie alert |

## Integrazioni esterne previste

| ID | Sistema | Tipo | Direzione | Uso previsto | Dati scambiati | Criticita | Stato |
|---|---|---|---|---|---|---|---|
| `DSG-INT-NINA` | N.I.N.A. | Software locale | EAGLE <-> dispositivi / file | Sequenze, acquisizione, profili, log | Sequenze, FITS, log, stato dispositivi | Alta | AS-IS / Transition |
| `DSG-INT-ASCOM` | ASCOM Platform / Alpaca | Middleware | App <-> dispositivi | Driver e controllo strumenti | Comandi, stati, eventi | Alta | AS-IS; Alpaca da validare |
| `DSG-INT-CPWI` | Celestron CPWI | Software locale | EAGLE <-> CGX-L | Controllo montatura e disponibilita driver | Stato mount, tracking, Park, slew | Alta | AS-IS |
| `DSG-INT-PHD2` | PHD2 | Software locale | N.I.N.A. <-> guida | Autoguida e dithering | Comandi guida, log, metriche RMS | Alta | AS-IS |
| `DSG-INT-PIX` | PixInsight | Processing | PC Principale / workstation | Calibrazione ed elaborazione immagini | FITS/XISF, process logs, metriche | Media | Transition |
| `DSG-INT-ALLSKY` | AllSky | Osservazione ausiliaria | AllSky -> Monitoring/Data | Cielo, timelapse, contesto meteo-visivo | Immagini, timestamp, logs | Media | AS-IS / Da validare |
| `DSG-INT-WX` | Weather Station | Sensori | Meteo -> Monitoring/Automation | Condizioni ambientali e safety decision support | Temperatura, umidita, vento, pioggia/cloud | Alta | Da validare |
| `DSG-INT-CLOUD-STG` | Cloud Storage | Storage remoto | PC/EAGLE -> Cloud | Backup, archive, condivisione controllata | Dati, manifest, hash | Alta | TBD |
| `DSG-INT-GH` | GitHub | SCM / publishing | PC -> GitHub -> Portal | Repository, review, Pages, release evidence | Markdown, dashboard, issue, commit | Alta | AS-IS / Transition |
| `DSG-INT-OAI` | OpenAI | AI provider | PC/Cloud -> OpenAI | AI assistiva e analisi documentale | Prompt sanitizzati, risposte, riferimenti | Alta | TO-BE / TBD |
| `DSG-INT-ASTNET` | Astrometry.net | Plate solving / reference | PC/EAGLE -> Service | Solving o validazioni astronomiche quando approvate | Immagini ridotte, coordinate, solution | Media | TBD |
| `DSG-INT-TNS` | Transient Name Server | Scientific registry | PC -> TNS | Consultazione o submission eventi transitori | Metadata evento, immagini, report | Media | TBD |
| `DSG-INT-AAVSO` | AAVSO | Scientific community | PC -> AAVSO | Fotometria, campagne, submission validate | Misure, target, report | Media | TBD |
| `DSG-INT-ASTAP` | ASTAP | Solver locale | N.I.N.A. -> ASTAP | Plate solving locale | Immagine solve, coordinate, database stelle | Alta | AS-IS |
| `DSG-INT-RUT955` | Teltonika RUT955 | Network gateway | VPN/WAN/LAN | Accesso remoto, failover, firewall, log | Stato rete, eventi, VPN | Alta | AS-IS / Transition |

## Regole di integrazione

| ID | Regola | Applicazione |
|---|---|---|
| `DSG-ESB-INT-001` | Single control path | Un dispositivo critico deve avere una catena di controllo primaria, evitando accessi concorrenti. |
| `DSG-ESB-INT-002` | Local safety | Servizi cloud e AI non sono prerequisito per mettere in sicurezza l'osservatorio. |
| `DSG-ESB-INT-003` | Sanitized external exchange | Dati inviati a servizi esterni devono essere minimizzati e privi di segreti. |
| `DSG-ESB-INT-004` | Version traceability | Versioni software, driver e profili devono essere registrati per sessioni rilevanti. |
| `DSG-ESB-INT-005` | Failure evidence | Ogni integrazione critica deve produrre log o evidenza utile al troubleshooting. |

## TBD e decisioni future

| ID | Elemento | Impatto | Azione richiesta |
|---|---|---|---|
| `DSG-ESB-FLW-TBD-001` | Contratto standard del session manifest | Lineage e automazione data catalog | Definizione schema e quality gate |
| `DSG-ESB-FLW-TBD-002` | Canali alert e matrice escalation | Operations e incident response | Governance notification |
| `DSG-ESB-FLW-TBD-003` | Uso operativo Astrometry.net | Privacy, banda, dipendenza esterna | ADR se usato in workflow critico |
| `DSG-ESB-FLW-TBD-004` | Submission TNS/AAVSO | Qualita scientifica e responsabilita | SOP dedicata e approvazione |
| `DSG-ESB-FLW-TBD-005` | Provider storage cloud | Costi, security, retention, DR | Technology ADR futura |
