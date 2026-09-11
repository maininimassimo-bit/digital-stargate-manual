# ARB-BKL-041-F3 — Independent Architecture Review

| Campo | Valore |
|---|---|
| Review | ARB-BKL-041-F3 |
| Data | 11/09/2026 |
| Proposal | `docs/architecture/scientific-assets/BKL-041-F3-Deterministic-Scoring-and-Confidence-Engine.md` |
| Base | `4ca5135043c508288fa2ba41b744f29b3b9032ed` |
| Reviewed head | `98acd8a5c1a3d2b318c4fcf2eec6bb35db7202de` |
| PR | #161 |
| Decision | APPROVED |
| Score | 98/100 |

## 1. Executive decision

**APPROVED — 98/100.**

BKL-041 F3 implementa un motore repository-side puro, deterministico, versionato e spiegabile per normalizzazione, score ed evidence-support confidence. Il profilo ammesso è esclusivamente un dimostratore sintetico con identità e versione fail-closed; non viene presentato come calibrazione scientifica produttiva.

La review iniziale aveva rilevato che il validator non chiudeva l'allow-list sul `profileId`, a differenza di schema e documento. Il finding è stato corretto nel commit `98acd8a5c1a3d2b318c4fcf2eec6bb35db7202de` e coperto da test negativo. Non risultano Blocker, Major o Minor aperti. Le observation sono gate per profili produttivi e F4, non remediation F3.

## 2. Repository truth verificata

| Elemento | Evidenza | Esito |
|---|---|---|
| Baseline F2 | PR #160, merge `4ca5135043c508288fa2ba41b744f29b3b9032ed`, ARB 98/100 | F2 riconciliata Accepted |
| Current package | bootstrap, backlog, handover, baseline, roadmap source e projection indicano BKL-041 F3 | coerente |
| Profile | `DSG-SCIENTIFIC-QUALITY-SYNTHETIC-DEMONSTRATOR` `1.0.0-f3` | unico id/versione autorizzato |
| Algorithm | `DSG-WEIGHTED-LINEAR-SCORE` `1.0.0` | deterministico e versionato |
| Confidence | `DSG-EVIDENCE-SUPPORT-PRODUCT` `1.0.0` | evidence support, non probabilità |
| Known answer | score 77,86; confidence 74; coverage 0,925 | riproducibile |
| Missing evidence | required missing produce assessment unavailable e valori null | no imputazione/reweight |
| Explainability | raw, normalized value, peso, contribution, factor, refs e reason | decomposition completa |
| Authority | read-only, no acceptance/action authority, Safety locale | conforme |
| Dynamic refresh | non implementato F3; requisito esplicito e obbligatorio F4 | boundary preservato |

## 3. Scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Scope e semantic integrity | 100 | formula, profile e confidence F3 sono espliciti; consumer e produzione restano esclusi. |
| Domain e layer integrity | 99 | funzione pura repository-side senza I/O, clock, runtime, presentation o device dependency. |
| Algorithm e versioning | 99 | id/versioni, scale, rounding, bounds, direction e reject policy chiusi fail-closed. |
| Weighting e missing data | 100 | required weights positivi con somma 1; optional/context zero; nessun silent reweighting. |
| Determinism e identity | 100 | canonical JSON F2, profile/snapshot/assessment/fixture digest e input-order invariance. |
| Explainability | 99 | decomposition e exclusions rendono ispezionabili contributi e failure reason. |
| Confidence semantics | 98 | distinta da score e probabilità; fattori espliciti, coverage separata e testata. |
| Scientific integrity e bias | 96 | sensitivity completa per dimensioni required; parametri marcati sintetici e non produttivi. |
| Safety, security e authority | 100 | profilo unico, fixture sintetica, read-only, no action/acceptance/Safety authority. |
| Operability e observability | 96 | errori deterministici e CI dedicata; nessun runtime F3 da osservare. |
| Migration e rollback | 99 | incremento additivo, nessuna persistenza o consumer da migrare. |
| Traceability e validation | 99 | F2, roadmap, continuity, projection e sei workflow exact-head verificati. |

## 4. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

Nessuno aperto.

### Resolved during review

#### R-01 — Profile identity allow-list

Il validator iniziale accettava un `profileId` alternativo correttamente risigillato pur mantenendo `profileState=SYNTHETIC_DEMONSTRATOR_F3`. Schema e proposta autorizzavano invece un solo profilo. Il commit `98acd8a5c1a3d2b318c4fcf2eec6bb35db7202de` ora impone id e versione esatti; il test negativo prova il reject.

### Observations

#### O-01 — Calibrazione scientifica produttiva

Bounds, pesi e fattori F3 sono synthetic demonstrator parameters. Un profilo produttivo richiede nuovo id/versione, cohort rappresentative per target/filtro/setup, analisi di bias, calibration evidence, acceptance criteria e nuova ARB/RQ review. Non può sostituire implicitamente F3.

#### O-02 — Schema/validator parity

JSON Schema governa la struttura; il validator aggiunge invarianti cross-field come somma pesi, positive/zero weight, bounds ordinati e profile digest. Ogni evoluzione deve mantenere test di parity e unknown-property rejection per entrambi i livelli.

#### O-03 — F4 session-driven publication

F4 deve collegare evidence, assessment e consumer al workflow di import e dimostrare refresh automatico dopo ogni nuova sessione, idempotenza, profile-version recompute, atomic publication, failure/stale marker e assenza di manual data maintenance.

#### O-04 — Presentation semantics

Il futuro consumer deve visualizzare insieme score, confidence, coverage, profile version, decomposition, exclusions e freshness. Confidence non deve essere etichettata come probabilità; uno stato unavailable non deve essere convertito in zero.

## 5. Architecture and authority review

Il modulo riceve un envelope in memoria e restituisce un assessment immutabile. Non introduce persistence, messaging, network, API, port adapter o dipendenza da EAGLE/N.I.N.A./PHD2/PixInsight. L'identity dell'evidence resta ancorata alla canonicalizzazione F2 e il profilo non acquisisce authority sugli asset AP-013/AP-014.

L'authority è esatta: `consumerMode=READ_ONLY`, `acceptanceAuthority=false`, `actionAuthority=NONE`, `safetyAuthority=LOCAL_PHYSICAL_INTERLOCKS`. Weather è context-only a peso zero. Nessun risultato può determinare SAFE/UNSAFE, accettare una sessione, attivare remediation o inviare device command.

## 6. Validation matrix

| Gate | Stato | Evidenza |
|---|---|---|
| Local F3 verifier | Passed | score 77,86; confidence 74; coverage 0,925; assessment digest `ff60a5e8d828d8e4d9cf38337072fdbcb5cbd20d2e4ab15573fadf318a16f57d` |
| Local F3 tests | Passed | 19/19 |
| Local F2 regression | Passed | verifier + 12/12 test |
| BKL-041 F3 Governance | Passed | #2, run `34576406697` |
| BKL-041 F2 Governance | Passed | #9, run `34576406708` |
| Developer Foundation | Passed | #1288, run `34576406707` |
| Scientific Platform Governance | Passed | #43, run `34576406692` |
| Validate documentation | Passed | #921, run `34576406696` |
| Genera manuale Word | Passed | #1346, run `34576406775` |
| Governed projections | Passed | roadmap e scientific-platform status generati sul PR head |
| Runtime/OAT | Not Applicable | nessun runtime o consumer F3 |
| Device/Safety validation | Not Applicable | nessun device o Safety change |

## 7. Migration, compatibility e rollback

- F3 aggiunge schema, fixture, engine, test e workflow senza modificare F2;
- la sola modifica F2 è la riconciliazione di stato Accepted;
- non esistono migrazioni dati, persistenza o consumer;
- rollback mediante revert degli artefatti F3 e dei riferimenti roadmap/continuity;
- l'assenza di F3 non altera pipeline di import o apparati.

## 8. Decision and re-review criteria

Il PR #161 sul reviewed head `98acd8a5c1a3d2b318c4fcf2eec6bb35db7202de` è **APPROVED FOR RELEASE QUALITY REVIEW** per il solo scope F3.

Richiedono nuova review:

- qualunque profilo o calibrazione produttiva;
- modifiche a formula, bounds, pesi, confidence method o identity;
- F4 pipeline/consumer e automatic refresh;
- threshold, ranking, classi qualitative, acceptance o action authority.

L'approvazione F3 non autorizza F4, uso produttivo dello score, remediation, device command o Safety Authority.
