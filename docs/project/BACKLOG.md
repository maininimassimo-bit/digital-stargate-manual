# Project Backlog

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 5.28 |
| Stato | Active |
| Data baseline | 15/09/2026 |

## 1. Scopo

Raccogliere il lavoro pianificato del progetto senza sostituire `AMP-002`, i singoli Architecture Package o il sistema di issue tracking. Questo backlog ordina le attività per priorità, dipendenze e milestone.

## 2. Regole

Ogni voce deve includere identificativo, titolo, priorità, stato, dipendenze, risultato atteso e riferimenti. Stati ammessi: `Planned`, `Ready`, `In Progress`, `Blocked`, `Done`, `Cancelled`.

## 3. Backlog prioritario

| ID | Priorità | Titolo | Stato | Dipendenze | Risultato atteso | Riferimenti |
|---|---|---|---|---|---|---|
| BKL-001 | P0 | RC1-HF01 Enterprise Theme Manager | Done | Governance Framework baseline | Theme Service centralizzato, persistenza, Instant Navigation e separazione da `page-enhancements.js` | TD-001, WP-03 Completion Report |
| BKL-002 | P0 | Integrare Project Governance Center nella nav MkDocs | Done | Documenti governance completi | Sezione Project Governance navigabile | TD-006 |
| BKL-003 | P0 | Creare AI_BOOTSTRAP.md in root | Done | BKL-002/BKL-003 | Bootstrap universale | `AI_BOOTSTRAP.md` |
| BKL-004 | P1 | Aggiornare Governance Center | Done | BKL-002/BKL-003 | Documenti canonici e stato package | `docs/project/index.md` |
| BKL-005 | P1 | Governance strict build | Done | BKL-002–004 | Build verificata | Developer Foundation #730 |
| BKL-006 | P1 | Verificare Pages governance | Done | BKL-005 | Governance pubblicata | BKL-025 |
| BKL-007 | P1 | Razionalizzare workflow documentali e Pages | Done | Inventario workflow | Un solo owner deploy | TD-004 |
| BKL-008 | P1 | Riallineare README root | Done | Governance Foundation | Entry point enterprise | TD-003 |
| BKL-009 | P1 | Consistency checks AMP-002/roadmap | Done | Schema projection | Gate anti-drift | TD-005 |
| BKL-010 | P1 | Ridurre script inline nel portale | Done | Inventario JS | Moduli proprietari e gate | TD-002 |
| BKL-011 | P1 | Evidence residue ARB-012-C04 | Done | C04-W01–W08 | ARB Closed/Approved | AP-012 |
| BKL-012 | P1 | Validare unattended AP-013 COPY_ONLY | Done | Scheduler/evidence | Runtime OAT | AP-013 |
| BKL-013 | P1 | Completare AP-014 | Done | AP14-W01-W07 | Catalogo/search accettati | AP-014 |
| BKL-014 | P2 | Preparare AP-015 Scientific Knowledge Platform | Planned | AP-014, BKL-015 e capability foundation | Architecture Package CAP-40 | AMP-002 |
| BKL-015 | P2 | Implementare repository Knowledge Graph machine-readable | Done | BKL-029/BKL-030 architecture requirements; Governance Foundation | Relazioni AP/ADR/component/evidence interrogabili con source locator e gate CI | TD-008 Resolved; F1-F3; PR #96; merge `c1a9f96b34a23407c5804e7fd6facfbad226f8fc` |
| BKL-016 | P2 | Contestualizzare release e guide storiche | Planned | Inventario | Lineage baseline | TD-007 |
| BKL-017 | P2 | Tema system | Planned | RC1-HF01 | Preferenza OS | RC1-HF01 |
| BKL-018 | P0 | EAGLE runtime inspection e M27 OAT | Done | Evidence runtime | OAT accettata | AP-014 |
| BKL-019 | P0 | Logging N.I.N.A. C8 | Done | Evidence N.I.N.A. | INFO attestato | AP-014 |
| BKL-020 | P0 | Data lineage scientifica | Done | BKL-019 | Lineage governata | metadata registry |
| BKL-021 | P0 | Eliminare eredità target da latest-observation | Done | BKL-020 | Projection corretta | AP-014 |
| BKL-022 | P0 | Separare severity da completeness | Done | BKL-020 | Semantiche separate | AP-014 |
| BKL-023 | P1 | Riallineare proiezioni AP-014 | Done | BKL-020–022 | Viste coerenti | AP-014 |
| BKL-024 | P1 | Riallineare Observatory Status e Session Reports | Done | BKL-023 | Realtime/storico separati | AP-014 |
| BKL-025 | P1 | Pages integrity | Done | BKL-023 | Link/asset/sitemap verificati | Pages |
| BKL-026 | P0 | Deep assessment ARB/AP-014 acceptance | Done | BKL-019–025 | AP-014 Accepted | AP-014 |
| BKL-027 | P1 | Power/Network source discovery | Done | EAGLE | Source verificate | AP-004/AP-009 |
| BKL-028 | P1 | Integrare Power/Network telemetry | Done | BKL-027 | Canonical Observatory Status | N.I.N.A. exporter |
| BKL-029 | P1 | SQM Sky Quality Telemetry & Scientific History | Done | Source discovery su CloudWatcher/Lunatico/ASCOM | SQM realtime `mag/arcsec²` e statistiche SQM storicizzate per sessione con provenance | PR #68; merge `0ebf04ec0ba1c4a1236f2a52e8a7e44abe0c6441` |
| BKL-030 | P1 | EAGLE Health & Reliability Telemetry | Done | BKL-029; Windows read-only collectors | Health EAGLE spiegabile con collector, history, portal e hosted read-only transport | PR #89 merge `a15d85b27ebfbe8a6488330920d10dda8db79a78` |
| BKL-031 | P1 | Observation Planner intelligente | In Progress | F3-A3 decisions and ARB-213-MI01/MI02 evidence complete; bootstrap post-verified; reproducible offline container build and network-disabled preflight verified; image unpublished; ADR-010 Proposed; S10 unavailable | Review a separate immutable image-publication and authenticated exact-head platform-plan gate; retain stop before push/plan approval, apply, upload, scientific execution or runtime activation | ADR-010; BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001; BKL-031-F3-A3-CONTAINER-MANIFEST-002; ARB-213-MI02; BKL-031-F3-A3-INFRA-001 |
| BKL-032 | P2 | Session Readiness / Go-No-Go Decision Support | Planned | BKL-029–031, BKL-036 | Readiness pre-sessione spiegabile, non Safety Authority | Functional Roadmap Expansion |
| BKL-033 | P2 | Observatory Digital Twin | Planned | BKL-015/BKL-044, realtime telemetry | Modello visuale asset/dipendenze/stato | Functional Roadmap Expansion |
| BKL-034 | P2 | Scientific Image Gallery evoluta | Planned | BKL-035, BKL-045 | Immagini collegate a lineage scientifica e processing | Functional Roadmap Expansion |
| BKL-035 | P2 | Target Knowledge Base | Done | BKL-015/BKL-044 | Vista target con sessioni, SQM, setup, immagini e workflow | F1-F4 CLOSED/ACCEPTED; PR #112 merge `1eef3e6747d975e40d592933ece655014b808f05`; closure `docs/project/BKL-035-CLOSURE-2026-09-07.md` |
| BKL-036 | P2 | Observatory Health Score | Planned | BKL-030, telemetry history | Score operativo spiegabile distinto da Safety | Functional Roadmap Expansion |
| BKL-037 | P2 | Session Comparison & Benchmarking | Done | BKL-029, BKL-035, BKL-045 | Confronto qualità/acquisizione/processing | F1-F5 e dynamic full-catalog comparison CLOSED/ACCEPTED; closure `docs/project/BKL-037-CLOSURE-2026-09-10.md`; transition package BKL-037 -> BKL-041 |
| BKL-038 | P2 | Anomaly & Trend Center | Done | BKL-030, BKL-040 | Trend e pattern di degrado | F1/F2-A/F3-A/F3-B/F4-A accepted; PR #125 merge `d8249984d63455690b957156060f858eb3cc2713`; closure `docs/project/BKL-038-CLOSURE-2026-09-09.md` |
| BKL-039 | P2 | Equipment Performance Registry | Done | BKL-015, session history | Prestazioni storiche setup/componenti | F4-A/F4-B/F5-A/F5-B/F5-C/F5-D CLOSED/ACCEPTED; PR #132 merge `651fc340fbb5e58ca36409d574bdd09c3ae55790`; closure `docs/project/BKL-039-CLOSURE-2026-09-09.md` |
| BKL-040 | P2 | Night Timeline / Observatory Replay | Done | BKL-015/BKL-044, historical telemetry | Replay sincronizzato della notte | F1-F4 CLOSED/ACCEPTED; PR #117 merge `80d22a255540ac582733c60dfe9bbf7807bcdf9b`; closure `docs/project/BKL-040-CLOSURE-2026-09-08.md` |
| BKL-041 | P2 | Scientific Data Quality Score | Done | BKL-029, BKL-037, BKL-045 | Quality score scientifico spiegabile | F1–F5 CLOSED/ACCEPTED as experimental read-only capability; PR #163 merge `e4ccd216b0a0ca4033277ece513f051b052d2b83`; production readiness remains NOT_READY; closure `docs/project/BKL-041-CLOSURE-2026-09-11.md` |
| BKL-042 | P2 | AI Observatory Assistant | Planned | BKL-015/BKL-044 e intelligence services | Copilot read-only per diagnosis/RCA/planning/science | Functional Roadmap Expansion |
| BKL-043 | P2 | Observatory Reliability Engineering | Planned | BKL-030/BKL-038/BKL-042 | SLI/SLO, MTBF, MTTR, session completion e failure budget | Functional Roadmap Expansion |
| BKL-044 | P1 | Knowledge Graph / AI Evidence Contract | Done | BKL-015 | Provenance stabile per AP/ADR/assets/session/target/incident/telemetry/processing/AI | F1-F4 CLOSED/ACCEPTED; PR #104 merge `b7c01ba7221818e1971403ab3befe38c8e40cc54`; closure `docs/project/BKL-044-CLOSURE-2026-09-07.md` |
| BKL-045 | P2 | PixInsight Workflow Provenance Plugin | Done | BKL-015/BKL-044 | Estensione PixInsight governata per catturare workflow, parametri e lineage | F1-F5 CLOSED/ACCEPTED; closure `docs/project/BKL-045-CLOSURE-2026-09-10.md`; PR #140 merge `a08aed981e5ffa4af6b68fea521ada25a4b2b338`; retained PixInsight history completeness limitation |
| BKL-049 | P2 | PixInsight Native Workflow Capture Module | Planned | BKL-045, BKL-044, AP-013/AP-014, verifica SDK/PCL | Modulo PCL nativo end-to-end per cattura automatica, journal locale, export governato e archivio workflow read-only nel portale | Planning package only; implementazione non avviata; `docs/architecture/assessments/BKL-049-PixInsight-Native-Workflow-Capture-Module-Plan.md` |
| BKL-046 | P2 | AI Post-Processing Assistant for PixInsight | Done | BKL-015/BKL-044/BKL-045 | Assistente advisory per ottimizzare workflow PixInsight | F1-F5 CLOSED/ACCEPTED as deterministic read-only capability; PR #181 merge `3d680dd3a05c70b2a4654c4187c293e36b0af4a7`; 7/7 post-merge workflows and live Pages verified; closure `docs/project/BKL-046-CLOSURE-2026-09-13.md`; scientific effectiveness NOT_EVALUABLE, production NOT_READY, `aiModelImplemented=false` |
| BKL-047 | P1 | AP-013C Verified Transport Cleanup & Convergence Monitoring | Done | AP-013B COPY_ONLY OAT | DRY_RUN/NO_DELETE lifecycle evidence, ACK convergence e fail-closed classification accepted | AP-013C; C8 productive cleanup excluded |

### Reconciliation note — 10/09/2026

BKL-045 è `Done / Accepted`: F1-F5 sono accettati, la closure formale è `docs/project/BKL-045-CLOSURE-2026-09-10.md`, la PR #140 è integrata con merge `a08aed981e5ffa4af6b68fea521ada25a4b2b338` e i gate post-merge applicabili sono stati verificati con successo.

BKL-037 ha ora tutte le dipendenze dichiarate soddisfatte (`BKL-029`, `BKL-035`, `BKL-045`) ed è promosso come package governato corrente. Il confronto scientifico deve preservare completeness/provenance e non può interpretare una provenance PixInsight `UNAVAILABLE` o `PARTIAL` come assenza di processing.

La canonical roadmap source resta `.github/roadmap/roadmap-source.json`; `docs/data/roadmap.json` è una generated projection e deve essere sincronizzata esclusivamente tramite il generator governato.

### Transition note — 10/09/2026

BKL-037 è chiuso come capability read-only/descriptive-only dopo F1-F5, PR #147 e la riconciliazione di closure. BKL-041 è promosso a package corrente esclusivamente per avviare source discovery e semantic contract dello Scientific Data Quality Score: la promozione non autorizza scoring operativo, soglie implicite, ranking, raccomandazioni, remediation, device command o Safety Authority.

### BKL-041 closure and BKL-046 transition — 11/09/2026

BKL-041 F1–F5 sono CLOSED / ACCEPTED come capability sperimentale read-only con limitation tramite PR #163, merge `e4ccd216b0a0ca4033277ece513f051b052d2b83`, ARB R1 98/100, Release Quality `READY FOR MERGE`, workflow post-merge e Pages `34602219671` verdi. I 7 stati richiesti per una futura calibration review non sono dimostrati; nessun threshold quantitativo, profilo o uso produttivo è autorizzato. BKL-046 è promosso a package corrente esclusivamente per la definizione architetturale.

### BKL-046 F1 note — 11/09/2026

F1 è CLOSED / ACCEPTED tramite PR #165, merge `3f2e3edae93b009f5800a58a4ac5afc4f04e9bb7`, exact-head CI 7/7, ARB 99/100, Release Quality `READY FOR MERGE` e verifica live Pages/search. Ha inventariato le source eleggibili e definito il semantic boundary fra recommendation, decisione umana ed execution evidence, preservando BKL-044/BKL-045 e missingness fail-closed. I confini sono stati resi machine-readable in F2; nessun modello, provider, RAG/vector store, image upload o PixInsight apply path è autorizzato.

### BKL-046 F2 note — 11/09/2026

F2 è CLOSED / ACCEPTED tramite PR #167, merge `b8a9025fdfc9b5254b9c79a5c37a775b4f8fd083`, exact-head CI 5/5, ARB 98/100, Release Quality `READY FOR MERGE` e 6/6 workflow post-merge inclusa Pages `34634735881`. Recommendation e Human Decision Receipt sono contratti separati, deterministici, bounded e fail-closed; execution evidence resta BKL-045. All'acceptance F2, F3 fu promosso esclusivamente come demonstrator deterministico read-only sulle fixture F2, senza model/provider, real-session ingestion, confidence numerica o PixInsight apply.

### BKL-046 F3 note — 11/09/2026

F3 è CLOSED / ACCEPTED tramite PR #169, merge `8339aecf0b6b7fa19396561b20253c0411fd7ee7`, con 21/21 test F3, review ARB/RQ AI-assistite autorizzate dal repository owner e dichiarate non equivalenti ad approvazioni umane indipendenti, e 7/7 workflow post-merge inclusa Pages `34643716214`. Il demonstrator resta deterministico, sintetico, bounded e read-only; il known-answer digest è `a97f7ff5a394b6f714efc8a55b1b1ab6cd6c6865c9a58ea6b9ec5120e98a4070`. F4 è corrente esclusivamente per un consumer session/provenance-driven read-only, collegato automaticamente alla pipeline post-import con pubblicazione atomica e freshness/digest fail-closed. Nessun model/provider, automatic acceptance, PixInsight apply, remediation, device command o Safety Authority è autorizzato.

### BKL-046 F4 acceptance and F5 transition — 12/09/2026

F4 è CLOSED / ACCEPTED / POST-MERGE VERIFIED tramite PR #175, technical head `b2f8543d0a7fd3e354c40d9acb0206ef7e6edea4`, review-publication head `ae1b8f2ae04fc9c4891e794bc930ec0e09fcf640` e merge `af48cc2441cf956d88c13c81845fc2a2f7c599f2`. Le review ARB/RQ sono AI-assistite, owner-authorized e non equivalenti ad approvazioni umane indipendenti. La deroga `W-BKL046-F4-001` era limitata alla branch protection della sola PR #175 ed è scaduta al merge. Sono verdi 6/6 workflow post-merge; la Pages live conferma 15 sessioni, 0 provenance matched, 15 provenance unavailable e 15 processing-history fail-closed.

F5 è promosso soltanto come incremento di architettura/design per definire la valutazione su evidence reale e i criteri di una possibile closure read-only con limitation. Nessun model/provider, confidence scientifica, automatic acceptance, PixInsight apply, remediation, device command o Safety Authority è autorizzato.

### BKL-046 F5 architecture note — 12/09/2026

Il package F5 proposto separa technical capability acceptance, scientific effectiveness, human-decision evidence e production readiness. La baseline osservata ha 15 sessioni, 0 provenance matched, 15 unavailable, 0 decision receipt e 15 processing-history fail-closed; scientific effectiveness resta `NOT_EVALUABLE_CURRENT_EVIDENCE`. Le slice pianificate sono F5-A contract/evaluator/report, F5-B atomic update/consumer e F5-C review/closure. Alla pubblicazione del solo design nessuna slice era implementata o accettata.

### BKL-046 F5-A acceptance and F5-B transition — 12/09/2026

Il design F5 è integrato tramite PR #177 e merge `16e0f101fda50e375bff6d5e9c8ec90d2083bc12`; le relative deroghe sono consumate. F5-A è CLOSED / ACCEPTED / POST-MERGE VERIFIED tramite PR #178, authorized head `74603bedad088dcf9f2cb33b9769658f4a9e639a` e merge `46b956f0a6ceb04442ffd80447f810ef6463b5a8`. La re-review ARB R2 ha assegnato 98/100 e Release Quality ha emesso `CONDITIONALLY READY FOR MERGE`; entrambe sono review AI-assistite, owner-authorized e non equivalenti ad approvazioni umane indipendenti. La deroga una tantum per assenza di branch protection `W-BKL046-F5A-MERGE-001` è consumata/scaduta. I nove workflow post-merge sono verdi.

F5-B è promosso come incremento corrente sulla PR #179. Il technical head `f6555e80760f9c5d179df3dc0ee4e02c7e265a21` integra il generator F5 nei path automatici first/retry, include il report nel commit atomico e rende il consumer fail-closed sulla catena catalogo/F4/F5; i 10 workflow exact-head sono verdi, mentre ARB/RQ e acceptance restano pending. F5-C resta non iniziato. L'acceptance F5-A non modifica l'outcome dati: scientific effectiveness `NOT_EVALUABLE_CURRENT_EVIDENCE`, production `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false` e closure `KEEP_OPEN`.

### BKL-046 F5-B post-merge evidence and F5-C transition — 13/09/2026

F5-B è integrata tramite PR #179 e merge `eb1827e2cc6e957080c6d1e928a7b13652261851`. Il growth-safety hotfix PR #180, merge `2edb44d1d26b36f9381a3796483efe9c105a679d`, ha consentito la fresh analysis run `34766534178`; il commit analytics `8ed6085d15f6af9e466a90167f19e970e8c526a7` e Pages `34766571069` sono verdi. Catalogo, F4 e F5 risultano allineati su 16 sessioni e il consumer live mostra `FRESHNESS CHAIN VERIFIED`, chiudendo l'observation `ARB-F5B-O01`.

F5-C è promosso come candidato di closure deterministica read-only. La proposta è `ACCEPTED_READ_ONLY_WITH_LIMITATIONS` / `CLOSE_DETERMINISTIC_CAPABILITY`; restano obbligatori `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION` e `aiModelImplemented=false`. BKL-046 rimane `In Progress` fino a exact-head CI, review specifiche F5-C, merge autorizzato e post-merge verification.

### BKL-046 closure and BKL-031 F1 transition — 13/09/2026

BKL-046 è CLOSED / ACCEPTED / POST-MERGE VERIFIED tramite PR #181, technical head `36a72f12a050d5330e8a966c68f8f7d25709d843`, review-publication head `d0ad9f0c05e2040ba31e44dfc470eb3c4810b7f0` e merge `3d680dd3a05c70b2a4654c4187c293e36b0af4a7`. ARB 98/100 e Release Quality `CONDITIONALLY READY FOR MERGE` erano review AI-assistite, owner-authorized e non equivalenti ad approvazioni umane indipendenti. Le deroghe una tantum `W-BKL046-F5C-REVIEW-001` e `W-BKL046-F5C-MERGE-001` sono consumate/scadute. I sette workflow post-merge e Pages live sono verdi.

BKL-031 è promosso esclusivamente a F1 source discovery e semantic boundary. La promozione non autorizza algoritmo, ranking, score, soglie, scheduler automatico, go/no-go, device command, workload pesante su EAGLE o Safety Authority.
### BKL-031 F1 acceptance and F2 handoff — 14/09/2026

F1 è ACCEPTED / POST-MERGE VERIFIED tramite PR #183, technical head `55b502fb4e47ef92975767ceb444078cae36caf8`, publication head `7a4d020b59186c4b05b9741bb12689050e2b7e8d` e merge `b14d9cdd991b5eef74dd9b972958e74c5903a32d`. Le review ARB/RQ sono AI-assistite, owner-authorized e non equivalenti ad approvazioni umane indipendenti. I sei workflow post-merge sono verdi.

F2 è promosso esclusivamente come handoff per un futuro machine-readable context/source contract e bounded fixtures. Schema, fixture, validator, provider, ranking e runtime restano non autorizzati. Le condizioni F1, inclusi S07–S11 unavailable/unknown e i 20 casi negativi, sono trasferite.

### BKL-031 F2 implementation candidate — 14/09/2026

Il repository owner ha autorizzato il solo incremento F2. Il candidate package materializza schema, fixture bounded, validator fail-closed, test N01–N20 e quality gate senza provider, pesi, score, ranking, readiness, scheduling, comandi, carichi EAGLE o Safety Authority. ARB, Release Quality e merge restano separatamente non autorizzati.

## 4. Sequenza di esecuzione raccomandata

```text
Completed baseline through BKL-037
  -> BKL-041 Scientific Data Quality Score [CLOSED]
  -> BKL-046 AI Post-Processing Assistant [CLOSED]
  -> BKL-031 Observation Planner [F1/F2 ACCEPTED / F3 SA/F3-A1 ACCEPTED / F3-A2-D5 ACCEPTED / REPOSITORY AVAILABLE / RUNTIME ADAPTER ABSENT / SUCCESSOR SELECTION]
  -> BKL-032 Session Readiness
  -> BKL-036 Observatory Health Score
  -> BKL-033 Digital Twin
  -> BKL-034 Scientific Image Gallery
  -> BKL-042 AI Observatory Assistant
  -> BKL-043 Reliability Engineering
  -> BKL-014 / AP-015 Scientific Knowledge Platform
```

## 5. Criteri di priorità

- **P0**: blocco release, regressione, safety/security o governance essenziale.
- **P1**: rischio elevato, dipendenza diretta della roadmap o gap attuale.
- **P2**: evoluzione pianificata o miglioramento strutturale.
- **P3**: ottimizzazione futura.

## 6. Definition of Ready

Scope e outcome chiari, dipendenze esplicite, fonti autorevoli identificabili, acceptance criteria definibili e rischi noti.

## 7. Definition of Done

Implementazione/documentazione, test applicabili, commit/push, deployment rilevante, evidence e registri coerenti.

## 8. Aggiornamento

Il backlog va riesaminato dopo ogni milestone, release, hotfix, ARB o variazione di AMP-002/roadmap funzionale. Quando cambia la canonical roadmap source, la generated projection deve essere sincronizzata dal workflow governato `Roadmap Projection Sync`; la projection non è una seconda authority e non deve essere mantenuta manualmente.

### BKL-031 F2 acceptance — 14/09/2026

BKL-031 F2 è ACCEPTED / POST-MERGE VERIFIED tramite PR #188 e merge `7f861f7399079858c9744e69b6c773664b6b5b54`. Il technical head `8e46ae3eccdaca5763aee7103063e020f97e2946` ha ottenuto ARB AI-assisted 99/100 e Release Quality `CONDITIONALLY READY`; il review-publication head `09b6e2272f40688c7ead0eba964b8eb6f64a0920` è 7/7 verde e il merge è 9/9 verde. La deroga `W-BKL031-F2-MERGE-001` è consumata/scaduta. BKL-031 resta In Progress, ma nessun F3 o altro successore è promosso; provider, pesi, score, ranking, readiness, runtime, device command e Safety Authority restano non autorizzati.

### BKL-031 F3 handoff promotion — 14/09/2026

Dopo la closure F2, F3 è promosso come handoff governato per source discovery e decisioni su sito, setup corrente ed ephemeris/lunare. La sequenza F1 resta F3 → F4 forecast → F5 ranking/consumer read-only → F6 closure. La promozione non autorizza design dettagliato, selezione provider, implementazione, schema, fixture, adapter, credenziali, chiamate esterne, forecast, ranking, readiness, runtime, device command o Safety Authority.

### BKL-031 F3 Solution Architecture AI-assisted reviews — 14/09/2026

L'handoff F3 è integrato/post-merge verified tramite PR #190, technical head `5706924c07c3a9fb9d04897c0aaaec4257d514d0`, review-publication head `979523f6c65c86450f7dac8335452aac370ea834` e merge `2ffc77917bcd3fc25a3c5657e8f12e62c9284303`, con ARB 99/100, Release Quality `CONDITIONALLY READY` e 9/9 workflow post-merge. La deroga `W-BKL031-F3-HANDOFF-MERGE-001` è consumata/scaduta.

Il Solution Architecture Package F3 e il validation plan sono stati valutati sulla PR #191 technical head `43a46ac28c30badc40e4cb180ed98924ebcf74a1`. ARB AI-assisted: `APPROVED WITH CONDITIONS`, 98/100; Release Quality AI-assisted: `CONDITIONALLY READY`. Le review non equivalgono ad approvazioni umane indipendenti e registrano due condizioni Minor: separazione tra digest interno del record sito e riferimento pubblico, e semantica half-open degli intervalli di validità. Restano pendenti la CI dell'head di pubblicazione e una separata autorizzazione owner per merge/ruleset. ADR/provider selection, record reali, schema/fixture/validator/adapter e implementazione restano non autorizzati.


### BKL-031 F3 Solution Architecture acceptance — 14/09/2026

La PR #191 è confluita in `main` tramite merge `3a79bb93c9a0925280eba5214d517107804cb13c` e ha completato 9/9 workflow post-merge, inclusi Pages, Developer Foundation e Governed Projection Sync. La deroga `W-BKL031-F3-SA-MERGE-001` è consumata/scaduta.

Il Solution Architecture Package F3 è accettato con condizioni come baseline documentale source-neutral; BKL-031 resta `In Progress` e nessuna slice F3-A1/A2/A3/B/C è promossa. `ARB-191-MI01` e `ARB-191-MI02` restano gate obbligatori. Il prossimo passo è una decisione owner separata sull'eventuale handoff F3-A1; provider/ADR, record reali, schema/fixture/validator/adapter, forecast, ranking, readiness, runtime, PC/EAGLE e Safety Authority restano non autorizzati.

### BKL-031 F3-A1 Site Authority Contract promotion — 15/09/2026

Dopo il merge della PR #192 in `21524c687a1fa6a9d840a3951c7ef4fe298f9c3c` e 9/9 workflow post-merge, l'owner ha autorizzato F3-A1 come review candidate esclusivamente documentale. Il package definisce intervalli UTC half-open, end unbounded esplicita, overlap fail-closed e separazione interno/pubblico. `ARB-191-MI02` può essere chiusa solo dalla review ARB; `ARB-191-MI01` resta gate di enforcement. Nessun record reale, schema, fixture, validator, adapter, storage, provider, runtime, EAGLE o Safety Authority è autorizzato.

### BKL-031 F3-A1 Site Authority Contract acceptance — 15/09/2026

La PR #193 è confluita in `main` come `b9d08a7cf6b6287825907cab6a846b1ec70f0378` dopo review ARB AI-assisted `APPROVED WITH CONDITIONS — 96/100` e Release Quality AI-assisted `CONDITIONALLY READY FOR MERGE`. La verifica post-merge ha concluso 9/9 workflow SUCCESS, inclusi Pages e Governed Projection Sync. Le review non equivalgono ad approvazioni umane indipendenti.

F3-A1 è accettato con condizioni come baseline documentale non implementata. `ARB-193-MI01`, `ARB-193-MI02` e `ARB-191-MI01` restano gate; `ARB-191-MI02` è soddisfatta a livello normativo, con test eseguibili ancora obbligatori prima della materializzazione. Il waiver `W-BKL031-F3A1-MERGE-001` è consumato/scaduto. Nessun successore, record reale, schema, fixture, validator, adapter, storage, provider, runtime, EAGLE o Safety Authority è autorizzato automaticamente.

### BKL-031 F3-A1 Acceptance Reconciliation closure — 15/09/2026

PR #194 è merged in `main` come `1fd771632239cdca38d7527c55b974d805ffd1b9` dopo ARB AI-assisted `APPROVED WITH CONDITIONS — 99/100`, Release Quality AI-assisted `CONDITIONALLY READY FOR MERGE` e 7/7 workflow sul review-publication head. Il merge ha concluso 9/9 workflow SUCCESS, inclusi Pages e Governed Projection Sync. Il waiver `W-BKL031-F3A1-ACCEPTANCE-MERGE-001` è consumato/scaduto.

### BKL-031 F3-A2 Setup Authority handoff — 15/09/2026

L'owner ha autorizzato il passo successivo e il Program Architect ha selezionato F3-A2 come successore dependency-ready, limitatamente a Program Assessment/Handoff documentale. Il futuro Solution Architect dovrà definire il contratto `CurrentSetupAssignment`, la reference AP-006, lifecycle, validità half-open e failure semantics. Nessun assignment reale, contratto dettagliato, schema, fixture, validator, adapter, runtime, F3-A3/B/C, EAGLE o Safety Authority è autorizzato.


### BKL-031 F3-A2 handoff acceptance — 15/09/2026

PR #195 è merged in `main` come `8520f4272d31f5578769e8d12ac34101e1c044e8` dopo ARB AI-assisted `APPROVED WITH CONDITIONS — 98/100`, Release Quality AI-assisted `CONDITIONALLY READY FOR MERGE` e 7/7 workflow sul review-publication head `09c0ba25fa8c4bc0649deaa6aee3bdeee61dbd60`. Il merge ha concluso 9/9 workflow SUCCESS, inclusi Pages e Governed Projection Sync.

`ARB-195-MI01` resta obbligatoria prima dell'approvazione del detailed F3-A2 contract. Nessun assignment, baseline concreta, schema, fixture, validator, adapter, provider, runtime, EAGLE o Safety Authority è stato introdotto.

### DSG-AEM-001 activation — 15/09/2026

L'owner ha attivato `DSG-AEM-001` e `W-DSG-AEM-RULESET-001` fino al completamento del progetto o revoca. Il programma procede autonomamente attraverso package dependency-ready; ogni merge senza ruleset richiede i gate sostitutivi exact-head e la relativa evidence. Il detailed F3-A2 Setup Authority Contract è il prossimo package.


### DSG-AEM-001 integration — 15/09/2026

PR #196 è merged in `main` come `357a5edfbd39346b10a1a2d751018ff6d1dd208f` dopo ARB AI-assisted `APPROVED — 99/100`, Release Quality `CONDITIONALLY READY` e 7/7 workflow sull'exact publication head. Il merge ha completato 9/9 workflow SUCCESS, inclusi Pages e Governed Projection Sync.

### BKL-031 F3-A2 detailed contract — 15/09/2026

Il Solution Architect ha prodotto `BKL-031-F3-A2-CONTRACT-001` e `BKL-031-F3-A2-VAL-001` come review candidate documentali. Il contratto risolve normativamente `ARB-195-MI01` distinguendo AP-006 architecture authority, concrete approved baseline instance, current assignment e observed evidence. Nessuna baseline o assignment reale è attestata; schema, fixture, validator, adapter, provider, runtime, EAGLE e Safety Authority restano fuori scope.


### BKL-031 F3-A2 detailed contract acceptance — 15/09/2026

PR #197 è merged in `main` come `64ecee230431de95fd892849757649da87314e7e` dopo ARB AI-assisted `APPROVED WITH CONDITIONS — 97/100`, Release Quality AI-assisted `CONDITIONALLY READY FOR MERGE` e 7/7 workflow sull'exact publication head `7d917fada3e6048940984bcf21d54dddb84b69d3`. Il merge ha completato 9/9 workflow SUCCESS, inclusi Pages e Governed Projection Sync.

F3-A2 è accettato con condizioni come contratto documentale source-neutral non implementato. `ARB-195-MI01` è chiuso normativamente; `ARB-197-MI01` richiede una decisione owner/architetturale su concrete Configuration Baseline Authority, Assignment Authority, approval evidence source e prima approved baseline instance prima di qualsiasi schema, fixture, validator, adapter, assignment reale o F3-B.

S08/S09/S10 restano unavailable. F3-A3/B/C, provider/ADR, runtime, EAGLE, ranking, readiness, go/no-go e Safety Authority non sono promossi.


### BKL-031 F3-A2-D1 GitHub authority and first baseline DRAFT — 15/09/2026

The Repository Owner authorized the GitHub-governed authority model. ADR-009 assigns owner/approval authority to `Repository Owner (protected authority ref)`, custodianship without approval power to the Digital StarGate Architecture Office, and stores protected records outside `docs/`. The first candidate payload is `[protected digest recorded outside docs]`; it remains `DRAFT`, unpublished and resolver-ineligible pending explicit owner approval or correction. No site record, assignment, schema, adapter, runtime or EAGLE operation is introduced.


### BKL-031 F3-A2-D1 integration — 15/09/2026

PR #199 merged as `4e8802c80359efce28d8d75521a1b9cc4cb44b05` and completed 9/9 post-merge workflows, including Pages and Governed Projection Sync. Authority model and protected DRAFT are integrated. The backlog is intentionally `Blocked` only on mandatory human approval/correction of exact payload `[protected digest recorded outside docs]`; baseline approval will not imply site or assignment approval.


### BKL-031 F3-A2-D2 exact baseline approval — 15/09/2026

The Repository Owner explicitly approved `DSG-SETUP-BASELINE-001` at payload `[protected digest recorded outside docs]`, valid from `2026-09-16T00:00:00Z`. PR #201 records the separate receipt and promotes only the lifecycle envelope to `APPROVED`; the payload is unchanged. No site record or assignment is inferred, and S09 remains `UNAVAILABLE_CURRENT`.


### BKL-031 F3-A2-D2 acceptance and F3-A1-M1 transition — 15/09/2026

PR #201 merged as `9932bace989565a10fd8e0d6f4a9c3b2cc057c46` after ARB AI-assisted `APPROVED WITH CONDITIONS — 99/100`, Release Quality `CONDITIONALLY READY FOR MERGE` and 4/4 exact-head workflows. Post-merge verification completed 6/6 workflows, including Pages and Governed Projection Sync.

The approved setup baseline does not resolve current setup. F3-A1-M1 is selected as the next dependency-ordered owner decision gate for protected site authority materialization. Exact site facts, authority, elevation semantics, resolver identity/scope and publication policy are not present and must not be inferred. BKL-031 is therefore `Blocked` on explicit owner input. S08 remains `UNAVAILABLE`; S09 remains `UNAVAILABLE_CURRENT`.

### BKL-031 F3-A1-M2 protected Site Authority DRAFT — 15/09/2026

The Repository Owner completed the F3-A1-M1 source and authority decisions and authorized protected repository registration without public disclosure of exact coordinates, elevation or address. F3-A1-M2 is a review candidate containing a protected, ineligible `DRAFT`, source-decision evidence, versioned schemas, deterministic digest validation, privacy enforcement and the executable A1-P01–P10/A1-N01–N41 suite. Local evidence is 51/51 PASS; exact-head CI, ARB and Release Quality remain required. Source authorization is not exact-digest lifecycle approval. S08 remains `UNAVAILABLE`, S09 remains `UNAVAILABLE_CURRENT`, and assignment/adapter/runtime/EAGLE/Safety remain outside scope.

### BKL-031 F3-A1-M3 owner approval and M4 promotion candidate — 15/09/2026

PR #203 merged as `d5750ce160c5f80d20a72bc35dee321200647d03` with 10/10 post-merge workflows. The Repository Owner subsequently approved the exact canonical Site Authority digest and acknowledged its unbounded validity while preserving the prohibition on public coordinates, elevation and exact address. F3-A1-M4 adds the protected receipt and a separate APPROVED envelope with an unchanged payload, plus eight receipt/promotion tests for a 59-case suite. Exact-head CI, ARB, Release Quality, expected-head merge and post-merge reconciliation remain required. No runtime adapter or assignment is included; S08/S09 remain unavailable to runtime consumers.

### BKL-031 F3-A1-M4 acceptance and F3-A2-D3 transition — 15/09/2026

PR #204 was reviewed at `f394ef5c3b5ad089e18fa3c4c431e2fcbd556e38` with 8/8 exact-head workflows, ARB `APPROVED WITH CONDITIONS — 98/100` and Release Quality `CONDITIONALLY READY`, without waiver, Blocker or Major. Expected-head merge produced `e73b1aa631c41dff97b9e5ededb6d6be02a667d4`; 10/10 post-merge workflows succeeded. The protected Site Authority is APPROVED and repository-resolver eligible for authorized callers, while protected values remain omitted publicly.

F3-A2-D3 is selected as the separate `CurrentSetupAssignment` owner decision gate. No assignment, schema, adapter or runtime is authorized. S08 remains `UNAVAILABLE`; S09 remains `UNAVAILABLE_CURRENT`. `ARB-204-MI01` is due before a second site revision/receipt and `ARB-204-MI02` before any runtime adapter.

### BKL-031 F3-A2-D3 owner decisions and D4 handoff — 15/09/2026

PR #205 merged as `d5f403bbe6a39731213c372cb22296324d10b03d` with 9/9 post-merge workflows. The Repository Owner selected the protected GitHub registry outside `docs/`, retained the Repository Owner as assignment owner and human Approval Authority, retained the Architecture Office as non-approving custodian, and selected half-open unbounded validity from the approved setup-baseline effective start.

F3-A2-D3 may record those decisions as protected evidence only. After its integration, F3-A2-D4 is the bounded Solution Architect handoff for a resolver-ineligible DRAFT with schema, canonicalization, validator and tests. No assignment approval, receipt, adapter, runtime, EAGLE activity or Safety Authority change is authorized.

### BKL-031 F3-A2-D4 protected assignment DRAFT — 15/09/2026

PR #207 was reviewed at exact head `d845042c1e2094cd82de762e7e2de60e9c54b2c5` with 5/5 workflows, Documentation `ACCEPTED WITH OBSERVATION`, ARB `APPROVED WITH CONDITIONS — 99/100` and Release Quality `CONDITIONALLY READY`, without Blocker or Major. Expected-head merge produced `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b`; 7/7 post-merge workflows succeeded, including the dedicated D4 gate and Pages.

The protected resolver-ineligible DRAFT, closed decision and assignment schemas, canonical identity, exact authority binding, deterministic interval/conflict behavior, privacy enforcement and 57/57 tests are integrated. The package does not add an approval receipt, APPROVED lifecycle, runtime adapter, EAGLE activity, readiness/go-no-go, commands or Safety Authority changes. BKL-031 is blocked only on mandatory human approval or rejection of the exact protected assignment digest.


### BKL-031 F3-A2-D5 exact-digest assignment approval — 15/09/2026

The Repository Owner explicitly approved the exact protected `CurrentSetupAssignment` digest and unbounded validity from the setup-baseline effective start, while preserving the prohibition on public digest and site facts. PR #209 records a separate protected receipt and creates an `APPROVED` lifecycle envelope without changing the assignment payload or digest. The implementation head passed 65/65 cases in the redacted governance workflow. Exact-head repository CI, Documentation governance, AI-assisted ARB/RQ, expected-head merge and post-merge verification remain required. No runtime adapter, EAGLE activity, command, readiness/go-no-go or Safety Authority change is included; S09 remains `UNAVAILABLE_CURRENT`.

### BKL-031 F3-A2-D5 acceptance reconciliation — 15/09/2026

PR #209 passed 5/5 exact-head workflows at `6947e79a53282db2a7f6d879643e51840ed9e553`, received Documentation `ACCEPTED WITH OBSERVATION`, AI-assisted process-separated ARB `APPROVED WITH CONDITIONS — 99/100` and Release Quality `CONDITIONALLY READY FOR MERGE`, then merged with expected-head control as `bc4307c2042a45985622044e11631421de5b2c3d`. All 7 post-merge workflows succeeded. The reviews are not equivalent to independent human approval.

F3-A2-D5 is ACCEPTED / POST-MERGE VERIFIED. The historical DRAFT remains immutable; the protected receipt and separate `APPROVED` envelope preserve the assignment payload/digest; 65/65 cases pass. Repository authority resolves `AVAILABLE` for authorized validated input. Runtime S09 remains `UNAVAILABLE_CURRENT` because no adapter exists. No EAGLE activity, device command, readiness/go-no-go or Safety Authority change occurred.

The Program Architect must now select the next dependency-ready BKL-031 package from repository evidence. Any runtime adapter requires a separate architecture package and satisfaction of `ARB-204-MI02`.


### BKL-031 F3-A3 Program Handoff — 15/09/2026

F3-A3 è il successore dependency-ready selezionato. Lo scope corrente è esclusivamente documentale: confronto source-neutral tra Astropy+pinned JPL, Skyfield+pinned JPL e JPL Horizons; ADR structure; validation-spike plan; decision evidence per F3-OD04–F3-OD10. Nessun candidato è selezionato. Provider/terms, kernel/data, error budget, privacy, host e bounded execution richiedono decisioni tracciate prima di uno spike eseguibile. S10 resta `UNAVAILABLE`; F3-B/C e ogni runtime adapter restano bloccati.


### BKL-031 F3-A3 Decision Preparation — 15/09/2026

BKL-031-F3-A3-SOLUTION-001, proposed ADR-010 and BKL-031-F3-A3-VAL-001 are the current documentation review package. Official sources and observed candidate versions are refreshed, but no artifact is approved or acquired. The package recommends evaluating a local primary with an explicit cross-check and keeping Horizons restricted to validation unless privacy approval states otherwise. F3-OD04–F3-OD10 remain owner decisions; spike execution, F3-B/C and runtime remain blocked; S10 remains `UNAVAILABLE`.

### BKL-031 F3-A3 partial owner decision and GCP preparation — 15/09/2026

The owner approved the prudent method roles, numeric accuracy budget, pinned IERS policy, synthetic-site privacy boundary, Cloud Run Job profile and bounded request envelope. F3-OD05 remains open for the exact JPL SPK, coverage, provenance, notices and SHA-256. Repository-only Terraform and validation CI are the current increment; GCP bootstrap/apply, artifact acquisition and spike execution remain blocked. S10 remains `UNAVAILABLE`.

### BKL-031 F3-A3 exact SPK owner decision — 16/09/2026

F3-OD05 is owner-approved at the artifact identity and provenance level using `de442s.bsp` and its exact SHA-256/content-addressed future private URI. That repository package introduced no kernel binary, upload, cloud mutation or scientific execution. ARB-213-MI01 and ARB-213-MI02 were then satisfied through separate reviewed increments. ADR-010 remains Proposed and S10 remains `UNAVAILABLE`.


### BKL-031 F3-A3 immutable method profile — 16/09/2026

`BKL-031-F3-A3-METHOD-PROFILE-001` is the repository-level ARB-213-MI01 evidence candidate. Its SHA-256 is `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`; it carries every approved F3-OD06/F3-OD07/F3-OD10 value plus the related method, SPK, privacy, hosting and fail-closed boundaries. Terraform supplies only the exact profile ID/path/digest, and CI proves that mutated bytes or an unreviewed digest are rejected before calculation. No container build, IERS acquisition, platform mutation or scientific execution is authorized. ARB-213-MI02 is satisfied; exact container/IERS inclusion and authenticated platform-plan review remain open.

### BKL-031 F3-A3 bootstrap and MI02 closure — 16/09/2026

The authenticated saved bootstrap plan for `main@af8b18f2f4e96642f453a30ead1e60e24ac8bd46` added 27 resources with no update or destroy. Bootstrap state is active in protected versioned GCS. Fail-closed incident `ARB-213-MI02-I01` identified Terraform's expected single serial increment during remote persistence while lineage and managed content remained unchanged. PR #219 promoted the permanent backend as `6c6a9454f1f1f13f72b4ae5098c0f2475b537d60`; 7/7 post-merge workflows, preserved lineage/content/generation, a read-only recovery candidate, clean locking and zero-drift exit code `0` satisfy ARB-213-MI02. Platform plan/apply, artifact upload, container build/push and scientific execution remain unauthorized.

### BKL-031 F3-A3 reproducible offline container-build gate — 16/09/2026

CI run `35122782246` acquired the ten exact manifest artifacts into an ignored ephemeral build area, verified every SHA-256, and built the isolated linux/amd64 container twice with pinned BuildKit and no RUN network. Both no-cache builds produced image config ID `sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0`. The network-disabled preflight verified the immutable method profile, installed package versions, the exact IERS-A wheel and campaign-date coverage (`MJD 41684.0..61659.0`, campaign preparation `MJD 61299.0`). The default scientific runner remained absent and exited `78`. `BKL-031-F3-A3-CONTAINER-BUILD-EVIDENCE-001` records the result; the image config ID is not a registry digest. Image push, artifact upload, platform plan/apply, scientific execution, external traffic, protected-site use and runtime activation remain `NOT_EXECUTED`.
