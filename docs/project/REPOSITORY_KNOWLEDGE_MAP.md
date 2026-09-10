# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 2.1 |
| Stato | Active |
| Data | 10/09/2026 |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Current governed package | BKL-037 — Session Comparison & Benchmarking |

## 1. Scopo

Questa mappa orienta tra domini, authority, projection e percorsi di conoscenza del repository. Non sostituisce i documenti canonici sottostanti. La mandatory reading sequence è definita esclusivamente da `AI_BOOTSTRAP.md`.

## 2. Continuity hierarchy

1. `AI_BOOTSTRAP.md`;
2. `docs/project/HANDOVER_2026-09-10.md`;
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-10.md`;
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`;
5. questo Knowledge Map;
6. `docs/project/BACKLOG.md`;
7. `.github/roadmap/roadmap-source.json`;
8. `docs/data/roadmap.json` come generated projection;
9. Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook;
10. AMP-002 e package/ADR/review/evidence direttamente coinvolti.

Snapshot datati precedenti restano materiale storico e non stato live.

## 3. Authority e projection map

### Authority / governance

- repository GitHub versionato;
- Architecture Package e ADR approvati;
- `BACKLOG.md` per stato/priorità/dipendenze correnti;
- `.github/roadmap/roadmap-source.json` per roadmap funzionale canonica;
- Technical Debt e Decision Log per i rispettivi registri;
- closure, review, evidence e workflow per acceptance/quality claim.

### Projection

- `docs/data/roadmap.json`;
- knowledge/read models;
- scientific catalog e portal datasets;
- Observatory Status, Timeline/Replay, Equipment Performance, Session Comparison e Analytics Center.

Una projection non promuove la propria authority e deve preservare source locator, semantic type, lifecycle, Citation e Provenance dove previsti.

## 4. Accepted intelligence/scientific foundation

- BKL-015 — Knowledge Graph machine-readable foundation: accepted, repository-centric, nessun graph DB runtime implicito.
- BKL-044 — Knowledge Graph / AI Evidence Contract: accepted; Observation/Evidence/Claim/Inference/Recommendation, Citation, Provenance, lifecycle/conflict preservation.
- BKL-035 — Target Knowledge Base: accepted, projection-only.
- BKL-040 — Night Timeline / Observatory Replay: accepted, bounded/read-only.
- BKL-038 — Anomaly & Trend Center: accepted.
- BKL-039 — Equipment Performance Registry: accepted, descriptive-only.
- BKL-045 — PixInsight Workflow Provenance Plugin: accepted; `OBSERVED`, `DECLARED`, `SUGGESTED` restano distinti e la completezza della storia PixInsight non osservabile resta `UNAVAILABLE`.

## 5. Current package — BKL-037

BKL-037 — Session Comparison & Benchmarking è il package corrente secondo backlog e canonical roadmap. Le dipendenze BKL-029, BKL-035 e BKL-045 sono accepted.

Il comparison layer è read-only/descriptive-only e deve preservare unità, source, provenance, quality, completeness e exclusion reason. Comparabilità non dimostrata resta fail-closed. Nessun quality score, ranking, threshold, recommendation, remediation o Safety Authority coupling è autorizzato.

BKL-041 — Scientific Data Quality Score è il successore pianificato e possiede la futura semantica di scoring; non deve essere anticipato in BKL-037.

## 6. Scientific data and processing knowledge

AP-013 resta authority per scientific asset identity/checksum/lifecycle; AP-014 resta boundary di catalogo/sincronizzazione. GitHub conserva metadata, manifest, contratti ed evidence governata, non bulk RAW storage.

PixInsight fornisce candidate processing evidence entro il contratto BKL-045. Provenance storica mancante non può essere inventata o promossa a `OBSERVED`.

## 7. Analytics Center

Le correzioni integrate fino alla PR #151 rendono le viste analytics session-driven e coerenti con history/configuration/weather evidence governata. Weather/severity analytics e GREEN/YELLOW/RED sono presentation/analytical semantics e non Safety Authority.

## 8. Roadmap functional sequence

```text
Completed baseline through BKL-045
  -> BKL-037 Session Comparison & Benchmarking [CURRENT]
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

## 9. CI/CD e publishing

Commit o file presenti non provano build, acceptance o deployment. Le dichiarazioni devono essere legate all'exact HEAD/merge SHA e ai workflow realmente verificati.

## 10. Safety boundary

Portale, telemetry, analytics, replay, comparison e AI non sono Safety Authority. Gli interlock fisici e la Safety Authority locale restano indipendenti e autorevoli; nessun consumer read-only può comandare apparati o autorizzare remediation.

## 11. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima repository knowledge map |
| 2.0 | 08/09/2026 | Continuity hierarchy e knowledge/AI foundation |
| 2.1 | 10/09/2026 | Reconciliation a BKL-045 accepted, BKL-037 current, BKL-041 next e Analytics Center fino a PR #151 |
