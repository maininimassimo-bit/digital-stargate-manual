# Digital StarGate Enterprise Architecture Context

| Campo | Valore |
|---|---|
| Identificativo | DSG-CTX-001 |
| Versione | 2.0 |
| Stato | Active context baseline |
| Data baseline | 08/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch autorevole | `main` |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Continuity handover | `docs/project/HANDOVER_2026-09-08.md` |
| Technical baseline | `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-08.md` |
| Current governed package | BKL-038 — Anomaly & Trend Center |
| Owner | Massimo Mainini |

## 1. Scopo

Questo documento fornisce il contesto architetturale enterprise corrente del Digital StarGate. Non è il root bootstrap e non sostituisce Architecture Package, ADR, assessment, evidence, backlog, roadmap o release record.

Il punto di ingresso unico è `AI_BOOTSTRAP.md`. La sequenza corrente parte dal bootstrap, prosegue con handover e technical baseline 08/09/2026, quindi con questo Context, Repository Knowledge Map e le ulteriori authority dichiarate dal bootstrap.

I documenti handover/baseline datati 07/09/2026 o precedenti restano snapshot storici e non devono essere riscritti per rappresentare lo stato corrente.

## 2. Gerarchia e source authority

Principi di prevalenza:

1. il repository GitHub e i suoi artefatti versionati costituiscono la source of truth;
2. Architecture Package, ADR, capability, standard e registri governati mantengono la propria authority di dominio;
3. review ARB, Release Quality, validation record, workflow ed evidence provano esclusivamente ciò che hanno realmente verificato;
4. `docs/project/BACKLOG.md` e `.github/roadmap/roadmap-source.json` rappresentano lo stato governato corrente delle attività e della roadmap funzionale;
5. `docs/data/roadmap.json` e gli altri dataset sotto `docs/data` sono projection generate e non authority autonome;
6. AMP-002 resta l'architecture-program planning authority per numerazione e wave AP-007–AP-015, ma non va usato come live status register quando backlog/roadmap/evidence più recenti governano lo stato corrente;
7. conversazioni, prompt e snapshot storici non prevalgono sul repository corrente.

Nessuna projection può promuovere la propria authority o sostituire la fonte da cui deriva.

## 3. Visione e boundary permanenti

Digital StarGate governa documentazione operativa, architettura enterprise, portale, telemetry, scientific data, session reporting, knowledge/evidence lineage e foundation software dell'osservatorio remoto di Manciano.

Boundary permanenti:

- il portale è un Presentation boundary;
- Domain, Application e Infrastructure restano separati secondo Clean Architecture;
- i dataset e read model sono projection ricostruibili;
- source identity, source authority, semantic type, lifecycle, Citation e Provenance devono essere preservati nei consumer;
- `unknown`, `stale`, `degraded` e assenza dati non possono essere convertiti in valori validi inventati;
- i consumer AI restano advisory/read-only salvo governance futura esplicita.

## 4. Safety Authority

La Safety Authority fisica/locale resta indipendente e autorevole.

Portale, telemetry, Knowledge Graph, replay, anomaly/trend analysis e AI:

- non sono Safety Authority;
- non possono bypassare interlock locali;
- non possono trasformare historical evidence in command authorization corrente;
- non introducono automatic remediation authority;
- non possono comandare direttamente roof, mount, camera, power, network o altri apparati nella baseline corrente.

Qualunque futura modifica a command path, remediation o Safety Authority richiede governance architetturale separata.

## 5. Foundation accettate al 08/09/2026

Le foundation di intelligence e knowledge attualmente accettate includono:

- **BKL-015 — Knowledge Graph machine-readable foundation**: traceability repository-centric machine-readable;
- **BKL-044 — Knowledge Graph / AI Evidence Contract**: Citation, Provenance, semantic type, lifecycle, evidence/claim/inference boundaries e consumer preservation;
- **BKL-035 — Target Knowledge Base**: target-centric read model governato, projection-only;
- **BKL-040 — Night Timeline / Observatory Replay**: historical timeline/replay bounded, deterministico, `READ_ONLY` / `VISUAL_ONLY`.

BKL-030 — EAGLE Health & Reliability Telemetry resta una foundation accettata per health history e per i package successivi, distinta dalla Safety Authority.

## 6. BKL-040 — bounded accepted baseline

BKL-040 F1-F4 è CLOSED / ACCEPTED. La foundation conserva canonical UTC event time, `PLACED | UNPLACED`, deterministic ordering, Citation/Provenance e source authority.

La materializzazione eseguibile accettata è bounded:

- N.I.N.A.;
- PHD2;
- CloudWatcher;
- session projection dove definita.

SQM ed EAGLE health sono foundation governate candidabili a incrementi successivi, ma non sono stati silenziosamente materializzati come channel F3/F4. Power, Network e Safety non devono essere dichiarati come channel storici BKL-040 implementati senza un contratto storico governato specifico.

Il debito `TD-012 — Night Timeline F1/F2 Contract Compatibility` è `Accepted`: F2 non riproduce integralmente l'envelope minimo F1 e usa `replay_event_id` come tie-break mentre F1 definiva `source_event_id`. La baseline F2 accettata non va retrofittata silenziosamente; una normalizzazione futura richiede un incremento compatibile, migration contract, test fail-closed e review ARB.

## 7. Knowledge / AI evidence architecture

La knowledge architecture corrente è repository-centric e projection-oriented.

BKL-044 e BKL-035 impongono che ogni consumer preservi:

- source locator e source authority;
- Citation;
- Provenance;
- semantic type;
- lifecycle state;
- confidence/derivation semantics quando applicabili;
- conflitti e unknown senza silent resolution.

La remediation BKL-044 di PR #118 lega le transition seed storiche a evidence immutabile invece che a frammenti di un backlog live mutabile.

Graph DB, vector DB, RAG provider/runtime e AI operational authority non sono autorizzati dalla baseline corrente.

## 8. Roadmap e sequencing corrente

La source canonica `.github/roadmap/roadmap-source.json` e il live `BACKLOG.md` identificano:

- BKL-040: completed / accepted;
- BKL-038: current dependency-ready package;
- BKL-037: Planned, perché dipende anche da BKL-045;
- BKL-045: Planned.

Sequenza governata corrente:

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

BKL-038 può iniziare solo dopo la closure PR #118, review indipendente, Release Quality, merge e post-merge verification.

## 9. AMP-002 e roadmap live

`AMP-002 — Architecture Program Roadmap Realignment` resta la planning authority approvata per l'architecture program successivo ad AP-006 e per la numerazione AP-007–AP-015.

Non deve essere riscritto come registro di stato live. Lo stato corrente delle attività viene riconciliato attraverso backlog, canonical roadmap source, generated roadmap projection, package closure, evidence e workflow.

## 10. Delivery e validation

Per ogni milestone:

1. applicare la mandatory reading sequence di `AI_BOOTSTRAP.md`;
2. verificare branch, exact HEAD, diff e workflow reali;
3. identificare authority, projection e dependency boundary;
4. progettare e implementare soltanto lo scope approvato;
5. aggiornare documentazione/registri proprietari;
6. eseguire quality gate sull'exact HEAD;
7. eseguire review ARB indipendente quando richiesta;
8. eseguire Release Quality solo dopo ARB approval;
9. effettuare merge con expected-head protection quando possibile;
10. verificare i workflow sul merge SHA reale.

Nessuna acceptance o readiness può essere dedotta da un commit o da workflow eseguiti su un HEAD precedente.

## 11. Runtime impact della closure corrente

La closure BKL-040 / PR #118 è repository-only. Non richiede comandi su PC principale o EAGLE e non modifica collector, scheduler, Safety Authority o apparati fisici.

## 12. Riferimenti correnti

- `AI_BOOTSTRAP.md`
- `docs/project/HANDOVER_2026-09-08.md`
- `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-08.md`
- `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
- `docs/project/BACKLOG.md`
- `.github/roadmap/roadmap-source.json`
- `docs/data/roadmap.json`
- `docs/project/TECHNICAL_DEBT.md`
- `docs/project/DECISION_LOG.md`
- `docs/project/BKL-040-CLOSURE-2026-09-08.md`
- `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`

## 13. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima baseline enterprise allineata alla RC1 |
| 2.0 | 08/09/2026 | Riallineamento alla continuity hierarchy corrente, foundation BKL-044/BKL-035/BKL-040, BKL-038 current, authority/projection e Safety boundaries |
