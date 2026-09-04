# Project Backlog

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 3.5 |
| Stato | Active |
| Data baseline | 04/09/2026 |

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
| BKL-015 | P2 | Implementare repository Knowledge Graph machine-readable | Planned | BKL-029/BKL-030 architecture requirements; Governance Foundation | Relazioni AP/ADR/component/evidence e future entità scientifiche interrogabili | TD-008, GP-003, BKL-044 |
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
| BKL-029 | P1 | SQM Sky Quality Telemetry & Scientific History | Done | Source discovery su CloudWatcher/Lunatico/ASCOM | SQM realtime `mag/arcsec²` e statistiche SQM storicizzate per sessione con provenance | PR #68; merge `0ebf04ec0ba1c4a1236f2a52e8a7e44abe0c6441`; `docs/architecture/telemetry/BKL-029-SQM-Source-Discovery-and-Architecture-Contract.md` |
| BKL-030 | P1 | EAGLE Health & Reliability Telemetry | In Progress | BKL-029; Windows read-only collectors | Health EAGLE spiegabile: disk/RAM/CPU/event log/processi/time sync/USB/pending reboot/drift/capacity | G1-G5 complete; `docs/architecture/telemetry/evidence/BKL-030-G5-Runtime-OAT-2026-09-03.md`; G6 history/persistence resumes after BKL-047 closure |
| BKL-031 | P2 | Observation Planner intelligente | Planned | BKL-015, BKL-035, meteo/SQM | Ranking target per setup e condizioni | Functional Roadmap Expansion |
| BKL-032 | P2 | Session Readiness / Go-No-Go Decision Support | Planned | BKL-029–031, BKL-036 | Readiness pre-sessione spiegabile, non Safety Authority | Functional Roadmap Expansion |
| BKL-033 | P2 | Observatory Digital Twin | Planned | BKL-015/BKL-044, realtime telemetry | Modello visuale asset/dipendenze/stato | Functional Roadmap Expansion |
| BKL-034 | P2 | Scientific Image Gallery evoluta | Planned | BKL-035, BKL-045 | Immagini collegate a lineage scientifica e processing | Functional Roadmap Expansion |
| BKL-035 | P2 | Target Knowledge Base | Planned | BKL-015/BKL-044 | Vista target con sessioni, SQM, setup, immagini e workflow | Functional Roadmap Expansion |
| BKL-036 | P2 | Observatory Health Score | Planned | BKL-030, telemetry history | Score operativo spiegabile distinto da Safety | Functional Roadmap Expansion |
| BKL-037 | P2 | Session Comparison & Benchmarking | Planned | BKL-029, BKL-035, BKL-045 | Confronto qualità/acquisizione/processing | Functional Roadmap Expansion |
| BKL-038 | P2 | Anomaly & Trend Center | Planned | BKL-030, BKL-040 | Trend e pattern di degrado | Functional Roadmap Expansion |
| BKL-039 | P2 | Equipment Performance Registry | Planned | BKL-015, session history | Prestazioni storiche setup/componenti | Functional Roadmap Expansion |
| BKL-040 | P2 | Night Timeline / Observatory Replay | Planned | BKL-015/BKL-044, historical telemetry | Replay sincronizzato della notte | Functional Roadmap Expansion |
| BKL-041 | P2 | Scientific Data Quality Score | Planned | BKL-029, BKL-037, BKL-045 | Quality score scientifico spiegabile | Functional Roadmap Expansion |
| BKL-042 | P2 | AI Observatory Assistant | Planned | BKL-015/BKL-044 e intelligence services | Copilot read-only per diagnosis/RCA/planning/science | Functional Roadmap Expansion |
| BKL-043 | P2 | Observatory Reliability Engineering | Planned | BKL-030/BKL-038/BKL-042 | SLI/SLO, MTBF, MTTR, session completion e failure budget | Functional Roadmap Expansion |
| BKL-044 | P1 | Knowledge Graph / AI Evidence Contract | Planned | BKL-015 | Provenance stabile per AP/ADR/assets/session/target/incident/telemetry/processing/AI | Functional Roadmap Expansion |
| BKL-045 | P2 | PixInsight Workflow Provenance Plugin | Planned | BKL-015/BKL-044 | Estensione PixInsight governata per catturare e storicizzare workflow, step, parametri, input/output e lineage | Functional Roadmap Expansion |
| BKL-046 | P2 | AI Post-Processing Assistant for PixInsight | Planned | BKL-015/BKL-044/BKL-045 | Assistente advisory per ottimizzare workflow PixInsight con evidence, confidence e provenance | Functional Roadmap Expansion |
| BKL-047 | P1 | AP-013C Verified Transport Cleanup & Convergence Monitoring | Done | AP-013B COPY_ONLY OAT; OneDrive incident/recovery 04/09; PC destination verification | DRY_RUN/NO_DELETE lifecycle evidence, ACK convergence e fail-closed classification accepted; productive cleanup excluded | AP-013C v0.3; DSDM-005 v0.2; `E-AP013C-OAT-2026-09-04`; `ARB-013C-R1`; PR #86; C8 NO-GO |

### Reconciliation note — 04/09/2026

BKL-030 resta `In Progress`, con G1-G5 completati. G5 Runtime OAT su EAGLE30154 ha verificato FAST, MEDIUM e SLOW_ON_CHANGE con collector read-only, bounded probes, non-overlap e projection atomica. Il finding Event Log empty-window è stato corretto tramite PR #83/#84 e il rerun finale ha prodotto `OBSERVED/CURRENT`, `reason=null`, `events=[]`. C: è stato osservato con 672,124,928 byte liberi (0.301%): è un operational capacity risk candidate, senza severity inventata. Windows Time era `Stopped`; `PendingFileRenameOperations` presente; SMART dettagliato resta non verificato non-elevated; configuration drift resta `BASELINE_NOT_APPROVED`. Nessun Scheduled Task/service permanente, cadence numerica, health threshold, remediation automatica o Safety Authority è approvato. Il checkpoint AP-013C è ora chiuso per il perimetro no-delete e G6 history/persistence può riprendere secondo roadmap.

Il 04/09 l'incidente raw transport ha evidenziato un gap di convergenza OneDrive: EAGLE 445 XISF/445 READY contro PC 426/426, successivamente recuperato a 445/445 senza perdita osservata; tutti i 19 frame M 27 `0123–0141` sono stati verificati anche in `F:\Astrofotografia`. AP-013B resta `COPY_ONLY`.

BKL-047/AP-013C è `Done` per il solo incremento `DRY_RUN/NO_DELETE`: real OAT `E-AP013C-OAT-2026-09-04` completata, ACK PC riconvergenti su EAGLE, evaluator live fail-closed, ARB re-review `ARB-013C-R1` favorevole e CI finale del precedente documentation head verificata verde. `CleanupEligible=0`, `CleanupAuthorized=0` e `Deleted=0` restano invarianti. Qualunque C8 productive cleanup è escluso da questa closure e richiede un nuovo change-set governato, retention/grace policy, crash-safe delete semantics, test, ARB/release-quality e autorizzazione esplicita.

## 4. Sequenza di esecuzione raccomandata

```text
Completed baseline through BKL-029
  -> BKL-047 / AP-013C DRY_RUN/NO_DELETE (Done; C8 productive cleanup excluded)
  -> BKL-030 EAGLE Health & Reliability (In Progress: resume G6 history/persistence)
  -> BKL-015 Knowledge Graph foundation
  -> BKL-044 Knowledge/AI Evidence Contract
  -> BKL-035 Target Knowledge Base
  -> BKL-040 Night Timeline / Replay
  -> BKL-037 Session Comparison
  -> BKL-038 Anomaly & Trend Center
  -> BKL-039 Equipment Performance Registry
  -> BKL-041 Scientific Data Quality Score
  -> BKL-045 PixInsight Workflow Provenance Plugin
  -> BKL-046 AI Post-Processing Assistant
  -> BKL-031 Observation Planner
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

Il backlog va riesaminato dopo ogni milestone, release, hotfix, ARB o variazione di AMP-002/roadmap funzionale.