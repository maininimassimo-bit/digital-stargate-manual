# ARB-BKL-041-F1 — Independent Architecture Review

| Campo | Valore |
|---|---|
| Review | ARB-BKL-041-F1 |
| Data | 10/09/2026 |
| Proposal | `docs/architecture/scientific-assets/BKL-041-F1-Scientific-Data-Quality-Score-Source-Discovery-and-Semantic-Contract.md` |
| Proposal commit | `82699865e61e6e8259d73115ba5bc5651336abd3` |
| Base | `97dc8250fcd2ccc90cf17657c7e637f599c1c175` |
| PR | #159 |
| Decision | APPROVED |
| Score | 98/100 |

## 1. Executive decision

**APPROVED — 98/100.**

Il contratto BKL-041 F1 è coerente con la roadmap e con le baseline accettate BKL-029, BKL-037, BKL-044 e BKL-045. Separa correttamente score, dimension assessment, evidence coverage, confidence ed explainability; non anticipa formula, pesi numerici, threshold, ranking o consumer; mantiene il default fail-closed e preserva le authority AP-013/AP-014 e la Safety Authority locale.

Non risultano Blocker, Major o Minor finding aperti. Le observation indicate in questa review sono requisiti di ingresso per F2/F3 e non remediation necessarie per F1.

## 2. Repository truth verificata

| Elemento | Evidenza | Esito |
|---|---|---|
| Current package | `AI_BOOTSTRAP.md`, backlog e continuity baseline indicano BKL-041 | conforme |
| Entry condition | BKL-029, BKL-037 e BKL-045 risultano Accepted/Done | conforme |
| Catalogo | 15 sessioni; 15 source metrics, 13 guiding, 8 SQM, 14 weather | inventario F1 coerente |
| Comparison | BKL-037 projection limita l'aggregazione a SQM e mantiene 7 exclusions | boundary preservato |
| PixInsight | OAT BKL-045 dichiara `UNAVAILABLE` e zero step observed/declared | nessuna provenance inventata |
| Source authority | AP-013/AP-014 restano authority; catalogo/score sono projection | conforme |
| Safety | `LOCAL_PHYSICAL_INTERLOCKS`; nessun command path | conforme |

## 3. Scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Scope e semantic clarity | 100 | F1 distingue esplicitamente in-scope/non-scope e definisce lo score come profile-bound assessment, non verità assoluta. |
| Source discovery e repository truth | 99 | Fonti e coverage correnti sono coerenti con catalogo, comparison projection e PixInsight OAT. |
| Domain e layer integrity | 100 | Solo contratto/read model futuro; nessuna dipendenza Domain verso Infrastructure/Presentation. |
| Data contract e fail-closed behavior | 99 | Missing, partial, stale, incompatible e context-only restano distinti; default `UNAVAILABLE`. |
| Normalization e weighting governance | 97 | Metodo/versione, cohort, unità, motivazione e no silent reweighting sono obbligatori; i dettagli eseguibili restano correttamente rinviati a F2/F3. |
| Confidence, explainability e bias | 99 | Confidence separata dallo score; decomposition, coverage, limitations e bias disclosure obbligatori. |
| Safety, security e authority | 100 | `READ_ONLY`, `acceptanceAuthority=false`, `actionAuthority=NONE`, interlock locali invariati. |
| Migration, operations e rollback | 98 | Sequenza F1-F5 incrementale; F1 repository-only; rollback senza runtime migration. |
| Traceability e documentazione | 97 | Driver e contratti principali sono mappati; nessun ADR è necessario prima della scelta di formula/pesi. |
| Validation evidence | 95 | Invariant check locale e due workflow PR applicabili verdi; runtime/OAT non applicabili a F1. |

## 4. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

Nessuno.

### Observations

#### O-01 — Deterministic identity

F2 deve rendere eseguibile l'identità di profilo, evidence snapshot e assessment, incluse canonicalization, versioning e known-answer digest. F1 non deve essere modificato per anticipare tale scelta.

#### O-02 — Weight-set invariant

F2/F3 devono fissare e testare l'invariante della somma dei pesi, la scale semantics e il comportamento out-of-range. Nessun valore o total è approvato da F1.

#### O-03 — Negative fixtures

F2 deve includere casi negativi per required evidence mancante, optional evidence mancante, unità incompatibile, FWHM non calibrato, PixInsight `PARTIAL/UNAVAILABLE`, silent reweighting e authority escalation.

#### O-04 — Discoverability

La navigazione MkDocs può essere aggiornata quando esisterà un consumer/release surface stabile. L'assenza del documento F1 dalla navigation corrente non blocca un contratto Proposed ed è compatibile con i package scientific-assets esistenti.

## 5. Architecture and authority review

### Domain/layer boundary

F1 definisce tipi concettuali e invarianti senza introdurre dipendenze runtime. Le future projection restano derivate; AP-013/AP-014 non vengono mutate. Nessun nuovo persistence, messaging o external-system contract è implementato.

### Safety

Meteo e storico operativo restano context evidence. Lo score non può dichiarare SAFE/UNSAFE, comandare apparati, modificare severity o sostituire gli interlock fisici/locali.

### Scientific integrity

Il contratto evita tre errori critici: FWHM non calibrato promosso ad arcsec, missing evidence convertita in zero e processing completeness reinterpretata come qualità finale. Profilo e cohort versionati riducono il rischio di confronti scientificamente incoerenti.

## 6. Validation matrix

| Gate | Stato | Evidenza |
|---|---|---|
| Semantic invariant check | Passed | 9 invariants, 5 fenced blocks bilanciati |
| Validate documentation (no deploy) | Passed | workflow #909, run `34540951883` |
| Genera manuale Word | Passed | workflow #1334, run `34540951870` |
| Developer Foundation | Not triggered | change documentation-only; non richiesto dal path filter |
| Runtime/OAT | Not applicable | F1 non implementa runtime, schema, algoritmo o consumer |
| Device/Safety validation | Not applicable | nessuna modifica a device, telemetry producer o Safety Authority |

## 7. Migration and compatibility

- nessuna migrazione dati;
- nessuna modifica schema o consumer;
- nessuna modifica alla pipeline session-driven;
- nessuna incompatibilità con BKL-029/BKL-037/BKL-045;
- rollback tramite revert del solo documento F1.

## 8. Decision and re-review criteria

Il PR #159 è **APPROVED FOR MERGE** per il solo scope F1.

F2 richiede nuova review quando introdurrà schema/fixture/validator machine-readable. La re-review deve verificare almeno le observation O-01/O-03 e confermare che nessun peso numerico o score aggregato venga materializzato oltre lo scope approvato.

L'approvazione F1 non autorizza F3 scoring engine, F4 portal projection o alcuna acceptance/Safety authority.
