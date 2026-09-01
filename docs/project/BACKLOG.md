# Project Backlog

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 3.0 |
| Stato | Active |
| Data baseline | 30/08/2026 |

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
| BKL-029 | P1 | SQM Sky Quality Telemetry & Scientific History | In Progress | Source discovery su CloudWatcher/Lunatico/ASCOM | SQM realtime `mag/arcsec²` e statistiche SQM storicizzate per sessione con provenance | Functional Roadmap Expansion; Observatory Status; `docs/architecture/telemetry/BKL-029-SQM-Source-Discovery-and-Architecture-Contract.md` |
| BKL-030 | P1 | EAGLE Health & Reliability Telemetry | Planned | BKL-029; Windows read-only collectors | Health EAGLE spiegabile: disk/RAM/CPU/event log/processi/time sync/USB/pending reboot/drift/capacity | Functional Roadmap Expansion |
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

### Reconciliation note — 01/09/2026

BKL-001–BKL-028 mantengono le closure già accettate. BKL-010/TD-002 sono chiusi. La functional roadmap review del 30/08/2026 ha approvato BKL-029–BKL-046. BKL-029 resta `In Progress` fino alla closure formale della PR #68: source SQM CloudWatcher SOLO, adapter runtime N.I.N.A., canonical realtime projection e G6 OAT sono verificati; il contratto storico G3 completo è implementato e ha superato Developer Foundation #867, Validate Digital StarGate History #24, il real-session scientific E2E M27, la validazione documentale e la re-review ARB, con solo la presente reconciliation di traceability residua prima della closure. BKL-030 prepara l'health observability dell'EAGLE e resta `Planned` fino alla chiusura di BKL-029. BKL-015 resta la foundation Knowledge Graph, ma deve incorporare fin dal design le entità e relazioni necessarie alle capability approvate. BKL-045 introduce processing provenance PixInsight; BKL-046 viene solo dopo il plugin/provenance layer ed è inizialmente advisory-only. AI, health score e readiness non sostituiscono mai la Safety Authority locale.

## 4. Sequenza di esecuzione raccomandata

```text
Completed baseline through BKL-028
  -> BKL-029 SQM integration
  -> BKL-030 EAGLE Health & Reliability
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