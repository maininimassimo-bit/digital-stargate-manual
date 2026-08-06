# Cronologia verificata del progetto

| Campo | Valore |
|---|---|
| Identificativo | DSG-BOOK-TIME-001 |
| Collegamento | DSG-BOOK-001 |
| Stato | Baseline di ricerca |
| Data di verifica | 5 agosto 2026 |
| Perimetro | 13 luglio - 5 agosto 2026 |

## Regola di utilizzo

Questa cronologia sostiene il racconto editoriale. Registra soltanto eventi riconducibili a commit, documenti, release o Pull Request del repository.

Il commit dimostra che una modifica è stata registrata nel repository. Non dimostra automaticamente deployment, accettazione operativa o motivazione personale. Questi significati vengono attribuiti solo quando esiste un'evidenza specifica.

## Fase 1 - Il manuale diventa Docs-as-Code

### 13 luglio 2026

- `cf4535f` configura Docs-as-Code con MkDocs e Pandoc.
- `baf31f4` aggiunge la pubblicazione automatica MkDocs.
- `a76fa25` aggiunge la build automatica del manuale Word.
- `57de947` completa i capitoli 1-5 su introduzione e infrastruttura.
- `2945d7d` completa i capitoli 16-19 su operations, recovery e manutenzione.
- `67f0a77` completa i capitoli 20-24 su governance, continuità e sicurezza.
- `3bb6bce` completa i capitoli 25-29 su operations avanzate e dati.
- `afbd508` completa i capitoli 30-34 su affidabilità, governance e release.
- `ecb5515` completa i capitoli 35-39 su engineering e allegati.
- `93ba824` completa i capitoli 40-44 su requisiti, rischi, handover e release.

**Lettura consentita:** entro questa data il repository contiene un corpus tecnico esteso e un processo di pubblicazione.

**Lettura non consentita:** il repository non documenta in questi commit la data iniziale dell'osservatorio fisico o tutte le motivazioni che hanno guidato la redazione.

## Fase 2 - Le sessioni diventano dati osservabili

### 15-17 luglio 2026

- `d96150a` aggiunge il report della sessione 14-15 luglio.
- `6f4c78f` rigenera un report analytics per la sessione 15-16 luglio.
- `9d976b9` introduce il reporting completamente automatico delle sessioni.
- `a4939d1` registra l'ingestion della sessione 16-17 luglio.
- `d70210f` registra l'analisi della stessa sessione.
- `b87700e` aggiunge workflow di validazione e strumenti di reporting analytics.

**Lettura consentita:** documentazione, sessioni e analytics iniziano a essere collegate in una pipeline ripetibile.

**Lettura non consentita:** la presenza del report non prova da sola la completezza scientifica o operativa di ogni sessione.

## Fase 3 - Dati, Warehouse e architettura

### 19 luglio 2026

- `10e0edf` aggiunge l'architettura della piattaforma Digital StarGate.

### 23-24 luglio 2026

- `8669bb4` introduce dataset Warehouse per sessioni e target.
- `1a3ecde` aggiunge equipment e quality con validazione e test.
- `a79f8cb` aggiunge il dataset weather.
- `5128a72` pubblica EA-001 sull'ambiente e il repository.
- `cc98567` pubblica EA-002 sull'integrazione repository/Warehouse.
- `b77a157` ed `ef81cd0` consolidano la documentazione architetturale del Warehouse.
- `9a702bd` aggiunge il deployment MkDocs su GitHub Pages.
- `110522c` evolve la homepage verso una release più strutturata.

**Lettura consentita:** il progetto passa dalla produzione di report a una piattaforma dati valutata e documentata.

**Lettura non consentita:** Warehouse implementato non significa che tutti i consumer, reporting e capability live siano integrati.

## Fase 4 - Baseline enterprise

### 26 luglio 2026

- viene datata e approvata `DSG-MR-001`, Master Roadmap 2026-2030;
- vengono pubblicate baseline EAM/DSRA, portfolio, registri e governance;
- `4ce05cf` aggiunge Foundation architecture, design system e publication guidelines;
- `840dd64` integra la milestone Foundation.

**Lettura consentita:** la documentazione e le iniziative vengono organizzate come programma enterprise con AS-IS, Transition e TO-BE.

## Fase 5 - Dalle fondamenta alle capability

### 28 luglio 2026

- la Release 1.5 consolida Developer Foundation, contratti e Observation Session;
- `7842126` integra il vertical slice Observation Session;
- `000f775` completa l'integrazione dei platform contracts.

### 29 luglio 2026

- `23fa674` propone la Release 2.0 Safety Foundation;
- il Weather Safety Interlock viene trattato come capacità progressiva e fail-safe.

**Lettura consentita:** il repository contiene una prima capability applicativa e, separatamente, una proposta safety priva di dichiarazioni runtime.

## Fase 6 - Architecture Program e assurance

### 30 luglio 2026

- PAA-002, ARB-002 e ABC-001 consolidano assessment, review e certificazione condizionata.
- `ef5629c` aggiunge `AMP-001`.
- `bd258b7` avvia gli Architecture Package con AP-001.
- seguono metamodel, data governance, automation, observability, identity, configuration, operations, integration, infrastructure, safety, analytics e Operations Center.
- `AMP-002` riallinea la numerazione e diventa roadmap autorevole per le wave successive.
- le review ARB mantengono visibili le condizioni aperte.

**Lettura consentita:** il programma adotta una catena formalizzata fra package, review, evidence e stato.

## Fase 7 - Evidence, repository scientifico e portale

### 31 luglio - 3 agosto 2026

- la campagna ENV-011 passa da preparazione e provisioning a esecuzione tecnica documentata;
- il risultato rimane limitato all'ambiente isolato e al simulatore;
- accettazione generale e controllo di apparati fisici restano separati.

### 4 agosto 2026

- la PR #38 pubblica la baseline AP-013 e il pilot protetto `COPY_ONLY`;
- la PR #39 integra navigation, command center ed Enterprise Portal;
- `22d8e92` registra Digital StarGate Enterprise Portal RC1;
- viene creato il Project Governance Center.

### 5 agosto 2026

- BootAI diventa punto di ingresso obbligatorio;
- il Decision Log registra repository truth, responsabilità modulari e delega AI entro boundary approvati;
- framework di foundation, tema, ricerca, operations dashboard e plugin SDK proseguono l'evoluzione controllata.
- AP-014 viene avviato e sviluppato attraverso modello concettuale e logico, proiezione deterministica, indice scientifico, query e ranking spiegabile, integrazione Enterprise Search e boundary PixInsight;
- l'evidence manifest AP-014 registra sette elementi richiesti presenti e accettati su otto; l'Operational Acceptance rimane aperta e AP-015 resta planned.

**Lettura consentita:** il progetto integra documentazione, portale, piattaforma scientifica, governance e AI-assisted engineering.

**Lettura non consentita:** portale pubblicato, simulatori validati e AI-assisted engineering non equivalgono a controllo autonomo dell'osservatorio.

## Questioni aperte

La cronologia dovrà essere estesa con:

- origine e prime fasi dell'osservatorio fisico;
- motivazioni dell'autore, tramite testimonianza separata dalle evidenze repository;
- relazione tra release visuali precedenti e baseline enterprise;
- sessioni osservative rappresentative;
- stato di AP-012/AP-015 alla chiusura editoriale.

Le informazioni future verranno aggiunte senza modificare retroattivamente il significato delle fonti correnti.
