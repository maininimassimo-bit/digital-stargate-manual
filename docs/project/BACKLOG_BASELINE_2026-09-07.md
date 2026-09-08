# Project Backlog — Historical Baseline 07/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 4.2 |
| Stato | Historical snapshot |
| Data baseline | 07/09/2026 |
| Source commit | `80d22a255540ac582733c60dfe9bbf7807bcdf9b` |

Questo documento preserva la baseline storica del backlog usata dalla Citation governata `CIT-BKL044-BACKLOG@1.0`. Non rappresenta lo stato corrente del programma e non deve essere aggiornato dopo la creazione.

## Reconciliation note — 07/09/2026

BKL-015 è `Done / Accepted` e TD-008 resta `Resolved`.

BKL-044 è `Done / Accepted`: F1-F4 sono completati. F4 è stato integrato via PR #104 con merge `b7c01ba7221818e1971403ab3befe38c8e40cc54`; post-merge Developer Foundation #1004, Docs #613, Word #1038 e Pages #697 sono `SUCCESS`. BKL-044 non autorizza graph DB, vector DB, RAG, inference runtime, AI authority o modifica della Safety Authority.

BKL-035 è `Done / Accepted`: F1-F4 sono completati. F4 è stato integrato via PR #112 con merge `1eef3e6747d975e40d592933ece655014b808f05`; post-merge Developer Foundation #1035, Docs #650, Word #1075 e Pages #705 sono `SUCCESS`. BKL-035 resta projection-only e non autorizza broad ingestion, fuzzy identity merge, runtime AI o modifica della Safety Authority.

BKL-040 è il nuovo package governato `In Progress` secondo la sequenza dependency-ordered corrente.

## Sequenza di esecuzione raccomandata alla baseline

```text
Completed baseline through BKL-030, BKL-015, BKL-044 and BKL-035
  -> BKL-040 Night Timeline / Replay [CURRENT]
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

## Historical BKL rows relevant to BKL-044 lineage

| ID | Priorità | Titolo | Stato | Dipendenze | Risultato atteso | Riferimenti |
|---|---|---|---|---|---|---|
| BKL-035 | P2 | Target Knowledge Base | Done | BKL-015/BKL-044 | Vista target con sessioni, SQM, setup, immagini e workflow | F1-F4 CLOSED/ACCEPTED; PR #112 merge `1eef3e6747d975e40d592933ece655014b808f05`; closure `docs/project/BKL-035-CLOSURE-2026-09-07.md` |
| BKL-040 | P2 | Night Timeline / Observatory Replay | In Progress | BKL-015/BKL-044, historical telemetry | Replay sincronizzato della notte | Current governed package after BKL-035 closure |
| BKL-044 | P1 | Knowledge Graph / AI Evidence Contract | Done | BKL-015 | Provenance stabile per AP/ADR/assets/session/target/incident/telemetry/processing/AI | F1-F4 CLOSED/ACCEPTED; PR #104 merge `b7c01ba7221818e1971403ab3befe38c8e40cc54`; closure `docs/project/BKL-044-CLOSURE-2026-09-07.md` |
