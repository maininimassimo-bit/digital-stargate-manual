# Digital StarGate — Current Technical Baseline — 2026-09-01

| Campo | Valore |
|---|---|
| Stato | Active technical delta baseline |
| Scope | Scientific session pipeline, SQM history, catalog and Home projection |
| Supersedes | Solo le sezioni di stato temporale incompatibili nei documenti di contesto precedenti |
| Does not supersede | Principi, boundary, ADR, Architecture Package o decisioni approvate |

## 1. Finalità

Questo documento colma il drift temporale tra la documentazione enterprise originaria e lo stato tecnico raggiunto il 01/09/2026. `ENTERPRISE_ARCHITECTURE_CONTEXT.md` e `REPOSITORY_KNOWLEDGE_MAP.md` restano validi per struttura, principi e mappa del repository, ma le loro fotografie di milestone del 04/08/2026 non rappresentano più lo stato operativo corrente.

## 2. Scientific session canonical pipeline

La pipeline scientifica corrente tratta manifest/raw evidence e normalized session metrics come input governati per la costruzione di history e projection del portale.

Le projection principali includono:

- `data/analytics/history/sessions.csv`;
- `docs/data/scientific-session-catalog.json`;
- `docs/data/scientific-observation-index.json`;
- `docs/data/realtime/latest-observation.json`;
- projection Home generate dalla pipeline governata.

I JSON del portale restano ricostruibili e non sono source primaria.

## 3. BKL-029 SQM

BKL-029 è completato. La misura SQM scientifica reale viene acquisita da source verificata e storicizzata con provenance. Il contratto storico comprende almeno start/end/min/max/mean/median/valid samples/temporal coverage/source/quality.

Per la sessione reale M 27 `2026-08-31_2026-09-01` risultano nella projection canonica:

- median SQM `18.66 mag/arcsec²`;
- mean SQM `17.5395 mag/arcsec²`;
- valid samples `1301`.

Lo SQM è un indicatore scientifico della qualità del cielo. Non è, e non deve diventare, Safety Authority.

## 4. Catalogo scientifico

Il Scientific Session Catalog deve presentare i metadata canonici disponibili della sessione, incluso SQM quando presente. L'assenza del rendering UI non deve essere interpretata come assenza di storicizzazione: source, analytics, projection e presentation sono boundary distinti.

Il Scientific Data Engine resta l'access layer condiviso; i renderer non devono introdurre una pipeline dati parallela.

## 5. Latest Observation e Home

La sezione “ultima sessione” deve essere derivata dalla sessione/history canonica più recente. Target, coordinate ed equipment non devono dipendere dalla presenza di una entry statica nel metadata registry; il registry può essere usato soltanto come fallback governato.

I timestamp di sessione legacy offset-naive e quelli timezone-aware devono essere normalizzati in UTC prima di confronti/ordinamenti.

Queste regole sono state consolidate dalle correzioni successive a BKL-029 e dalla PR #72, merge SHA `7d69fbfff818c2cedb45126a48f74905ba58c0ab`.

## 6. M 27 — reference projection

Reference scientific session:

- session: `2026-08-31_2026-09-01`;
- target: `M 27`;
- RA: `299.9°`;
- DEC: `+22.72111111°`;
- epoch: `J2000`;
- configuration: `C8_QHY695A_BIN1`;
- telescope: `Celestron C8 XLT`;
- camera: `QHY695A`;
- SQM median: `18.66 mag/arcsec²`.

Questi valori sono reference evidence per i regression test/projection della sessione indicata, non default da applicare ad altre sessioni.

## 7. Publication quality gate

Sulla baseline PR #72 merge SHA `7d69fbfff818c2cedb45126a48f74905ba58c0ab` sono stati verificati `SUCCESS`:

- Validate Digital StarGate History #30;
- Developer Foundation #875;
- Genera manuale Word #882;
- Deploy MkDocs artifact to GitHub Pages #646.

Il deploy Pages ha completato anche refresh latest observation, refresh homepage projections, MkDocs build, published-site integrity, artifact upload e deploy.

## 8. Safety e authority boundary

Restano invariati:

- local physical Safety Authority indipendente;
- telemetry, SQM, health, analytics e AI non sono Safety Authority;
- portale e AI senza controllo diretto dei device nella baseline corrente;
- UNKNOWN/STALE devono essere rappresentati come tali e non sostituiti da last-known-good corrente.

## 9. Evoluzione successiva

La capability successiva è BKL-030 EAGLE Health & Reliability. Il primo incremento è D1/D2 source discovery read-only su `EAGLE30154`. Nessuna soglia HEALTHY/DEGRADED/CRITICAL deve essere definita senza source/evidence e nessuna remediation automatica è autorizzata dalla discovery.

## 10. Relazione con i documenti precedenti

Quando `ENTERPRISE_ARCHITECTURE_CONTEXT.md`, `REPOSITORY_KNOWLEDGE_MAP.md`, `HANDOVER_2026-08-30.md` o `FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md` descrivono AP-014/BKL-029 come pianificati o prossimi, quella informazione è storica. Per lo stato corrente usare repository/evidence, `HANDOVER_2026-09-01.md`, questo technical baseline e backlog/roadmap correnti.
