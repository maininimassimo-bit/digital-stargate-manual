# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 2.0 |
| Stato | Active |
| Data | 08/09/2026 |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Current governed package | BKL-038 — Anomaly & Trend Center |

## 1. Scopo

Questa mappa descrive il repository Digital StarGate per domini, responsabilità, authority, projection e principali percorsi di conoscenza. È un indice di orientamento: non sostituisce i documenti canonici sottostanti.

La mandatory reading sequence è definita esclusivamente da `AI_BOOTSTRAP.md`. Handover e baseline datati precedenti restano snapshot storici.

## 2. Prodotti e domini del repository

Il repository contiene quattro insiemi principali e correlati:

1. **Manuale tecnico dell'osservatorio** — procedure operative, infrastruttura, software, safety, recovery e manutenzione.
2. **Enterprise Architecture & Governance Repository** — AP, ADR, capability, assessment, review, evidence, backlog, roadmap, debt, decisions e closure.
3. **Digital StarGate Enterprise Portal** — MkDocs Material, centri enterprise, Scientific Platform, Observatory Status, timeline/read-model e altre projection.
4. **Developer Foundation** — solution .NET, contratti, test, generatori, validator, pipeline e workflow CI/CD.

## 3. Continuity hierarchy

Percorso corrente obbligatorio:

1. `AI_BOOTSTRAP.md`;
2. `docs/project/HANDOVER_2026-09-08.md`;
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-08.md`;
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`;
5. questo Knowledge Map;
6. `docs/project/BACKLOG.md`;
7. `.github/roadmap/roadmap-source.json`;
8. `docs/data/roadmap.json` come generated projection;
9. `docs/project/TECHNICAL_DEBT.md`;
10. `docs/project/DECISION_LOG.md`;
11. `docs/project/DEVELOPMENT_WORKFLOW.md`;
12. `docs/project/CODING_STANDARDS.md`;
13. `docs/project/RELEASE_PLAYBOOK.md`;
14. AMP-002 e package/ADR/review/evidence direttamente coinvolti.

`HANDOVER_2026-09-07.md`, `CURRENT_TECHNICAL_BASELINE_2026-09-07.md` e snapshot precedenti sono materiale storico, non stato live.

## 4. Authority e projection map

### Repository / governance authority

- GitHub repository versionato;
- Architecture Package e ADR approvati;
- capability e standard governati;
- `BACKLOG.md` per stato/priorità/dipendenze correnti;
- `.github/roadmap/roadmap-source.json` per la roadmap funzionale canonica corrente;
- Technical Debt e Decision Log per i rispettivi registri;
- closure, review, evidence e workflow per acceptance/quality claims.

### Projection

- `docs/data/roadmap.json`;
- knowledge/read models;
- scientific catalog e portal datasets;
- Observatory Status projection;
- Night Timeline / Replay consumer projection;
- AI/read-model output.

Una projection non promuove la propria authority e deve preservare source locator, semantic type, lifecycle, Citation e Provenance dove previsti.

## 5. Enterprise Architecture

### Foundation e operations

- AP-001–AP-006 — foundation enterprise;
- AP-007 — Operations and Service Management;
- AP-008 — Enterprise Integration;
- AP-009 — Infrastructure;
- AP-010 — Safety Assurance;
- AP-011 — Analytics Platform;
- AP-012 — Operations Center;
- AP-013 — Scientific Image Repository;
- AP-014 — Scientific Observation Catalog and Search;
- AP-015 — Scientific Knowledge Platform, pianificato.

`AMP-002 — Architecture Program Roadmap Realignment` resta la planning authority per la sequenza/numerazione dell'architecture program successivo ad AP-006. Non è il live status register del backlog 2026-09-08.

## 6. Accepted intelligence and knowledge foundation

### BKL-015 — Knowledge Graph machine-readable foundation

Introduce traceability machine-readable repository-centric fra AP, ADR, componenti ed evidence. Non autorizza un graph database runtime.

### BKL-044 — Knowledge Graph / AI Evidence Contract

Foundation accettata per:

- Observation/Evidence/Claim/Inference/Recommendation semantics;
- Citation;
- Provenance;
- lifecycle;
- source authority;
- confidence/derivation;
- conflict preservation;
- consumer preservation.

La remediation di PR #118 conserva lineage storico immutabile per le transition seed BKL-044 e non dipende da frammenti mutabili del backlog live.

### BKL-035 — Target Knowledge Base

Read model target-centric accettato, projection-only, costruito sopra BKL-015/BKL-044. Non introduce broad ingestion, AI operational authority o Safety Authority.

### BKL-040 — Night Timeline / Observatory Replay

F1-F4 CLOSED / ACCEPTED.

Foundation:

- canonical `event_time_utc`;
- `PLACED | UNPLACED`;
- deterministic ordering;
- Citation/Provenance;
- bounded multi-source synchronization;
- exact temporal delta con `NOT_ASSESSED` senza threshold inventati;
- `READ_ONLY` / `VISUAL_ONLY` consumer.

Executable F3/F4 source coverage materializzata:

- N.I.N.A.;
- PHD2;
- CloudWatcher;
- session projection dove definita.

SQM ed EAGLE health sono foundation separate candidabili a consumer futuri. Power, Network e Safety non sono implicitamente materializzati come BKL-040 historical channels.

`TD-012` registra il compatibility debt F1/F2: F2 non materializza l'intero minimum envelope F1 e usa `replay_event_id` come tie-break invece del F1 `source_event_id`. Nessun retrofit silenzioso della baseline accettata.

## 7. Telemetry, health e Safety

BKL-029 governa SQM realtime/history.

BKL-030 governa EAGLE Health & Reliability Telemetry e la relativa historical foundation. Health evidence non equivale a Safety Authority.

Observatory Status e i relativi dataset sono presentation/read-model projection. `UNKNOWN`, `STALE` e qualità degradata restano espliciti.

La Safety Authority locale e gli interlock fisici sono indipendenti. Portale, replay, anomaly/trend center e AI non possono bypassarli o comandare gli apparati nella baseline corrente.

## 8. Scientific data and processing knowledge

Il dominio scientifico include:

- session package e manifest;
- raw N.I.N.A./PHD2/CloudWatcher evidence;
- SQM/history dove governato;
- catalogo scientifico;
- target knowledge;
- processing provenance pianificata con BKL-045;
- Scientific Knowledge Platform futura AP-015.

GitHub conserva conoscenza, metadata, manifest, checksum, contratti ed evidence governata; non è lo storage bulk dei RAW scientifici.

BKL-045 — PixInsight Workflow Provenance Plugin resta `Planned`. Per questo BKL-037 — Session Comparison & Benchmarking resta `Planned` e non può essere promosso prima di BKL-045 acceptance.

## 9. Current governed package — BKL-038

BKL-038 — Anomaly & Trend Center è il package dependency-ready corrente perché dipende da BKL-030 e BKL-040, entrambi accettati.

Entry conditions:

- PR #118 BKL-040 closure completata;
- exact-head CI verde;
- ARB indipendente APPROVED;
- Release Quality READY;
- merge con SHA reale;
- post-merge workflow verificati.

BKL-038 dovrà preservare explainability, source lineage, temporal lineage, Citation/Provenance, unknown/stale handling e advisory/read-only semantics.

Non può introdurre automaticamente:

- threshold anomaly inventati;
- automatic remediation;
- device commands;
- Safety Authority;
- AI operational authority.

## 10. Roadmap functional sequence

```text
Completed baseline through BKL-030, BKL-015, BKL-044, BKL-035 and BKL-040
  -> BKL-038 Anomaly & Trend Center [CURRENT]
  -> BKL-039 Equipment Performance Registry
  -> BKL-045 PixInsight Workflow Provenance Plugin
  -> BKL-037 Session Comparison & Benchmarking
  -> BKL-041 Scientific Data Quality Score
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

La sequenza va sempre verificata contro il live `BACKLOG.md` e la canonical roadmap source prima di iniziare un package.

## 11. CI/CD e publishing

Workflow principali:

- Developer Foundation — build/test/format, MkDocs e quality gates repository;
- Validate documentation — validation-only;
- Genera manuale Word — artifact documentale;
- Deploy Pages — build/deploy GitHub Pages dove applicabile.

La presenza di un commit non prova build, acceptance o deployment. Le dichiarazioni devono essere legate all'exact HEAD o merge SHA realmente verificato.

## 12. Historical material

Release note, handover, technical baseline, closure e acceptance record precedenti restano immutabili per lineage salvo correzione esplicitamente governata.

Un documento storico può contenere uno stato ormai superato senza essere errato: deve essere interpretato alla propria data e non usato come current authority se esiste un successore.

## 13. Percorso di lettura package-specific

Dopo la mandatory sequence del bootstrap, per il lavoro corrente leggere:

- BKL-040 closure e F1/F2/F3/F4;
- `TD-012`;
- review/evidence ARB e Release Quality applicabili;
- BKL-030 closure/health foundation;
- gli artefatti BKL-038 solo dopo la closure integrata di PR #118.

## 14. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima repository knowledge map |
| 2.0 | 08/09/2026 | Riallineamento a continuity hierarchy, Knowledge/AI foundation, BKL-040 replay, BKL-038 current e authority/projection boundaries |
