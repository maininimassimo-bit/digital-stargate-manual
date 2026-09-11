# ARB-BKL-041-F5-R1 — Independent Architecture Re-Review

| Campo | Valore |
|---|---|
| Review | ARB-BKL-041-F5-R1 |
| Data | 11/09/2026 |
| Proposal | `docs/architecture/scientific-assets/BKL-041-F5-Real-Evidence-Validation-and-Capability-Closure.md` |
| Base | `ed9ffcc92e1a5252b0d8c37634bc652397f3cde1` |
| Reviewed head | `060caae867c5f98a91c7c6a314ca272aeb91733d` |
| PR | #163 |
| Previous review | `ARB-BKL-041-F5-Independent-Review-2026-09-11.md` — REWORK REQUIRED, 84/100 |
| Decision | APPROVED |
| Score | 98/100 |

## 1. Executive decision

**APPROVED — 98/100.**

La remediation chiude M-01, M-02 e m-01 della review iniziale. F5 non contiene più threshold quantitativi di readiness privi di provenance: i conteggi della cohort sono esclusivamente evidence descrittiva e i sette criteri confrontano stati governati. La readiness degli input di calibrazione è separata dalla production readiness, che resta invariabilmente `NOT_READY_FOR_PRODUCTION`; nessun ramo autorizza profilo o uso produttivo.

Schema e browser validator chiudono le sezioni governate, verificano identità, cardinalità, forma esatta, authority e digest, e includono un negative test per proprietà annidate sconosciute. L'aggiornamento atomico dopo ogni import resta invariato e tutti i nove workflow applicabili sono verdi sull'exact head esaminato.

## 2. Resolution of previous findings

| Finding | Stato | Evidence di chiusura |
|---|---|---|
| M-01 — threshold non governati | RESOLVED | policy a sette stati; nessun minimo, massimo o ratio nella policy/report; conteggi conservati solo come metriche descrittive |
| M-02 — stato futuro incompatibile | RESOLVED | `buildF5Decision` separa `calibrationInputReadiness`; `productionReadiness` resta sempre `NOT_READY_FOR_PRODUCTION`; positive future-input test verde |
| m-01 — schema/validator parity | RESOLVED | oggetti governati con `additionalProperties:false`, requirement/result/metric tipizzati, exact-key browser validation e unknown-property negative test |

## 3. Scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Scope e semantic integrity | 100 | closure sperimentale distinta in modo permanente dall'autorizzazione produttiva |
| Cohort integrity | 98 | tutte le 15 sessioni incluse senza outcome filtering; distribuzione e bias espliciti |
| Scientific integrity e bias | 100 | nessuna soglia inventata; stati non dimostrati rimangono failure esplicite |
| Contract integrity | 98 | schema chiuso e tipizzato; browser verifica forma, identità, cardinalità e authority |
| Determinism e identity | 100 | report riproducibile e concatenato con digest a catalogo e projection |
| Dynamic update safety | 100 | catalogo, F4 e F5 rigenerati nello stesso workflow/commit; stale e drift falliscono chiusi |
| Explainability e UX | 98 | stato non produttivo e limitation visibili senza ranking o implicita valutazione scientifica |
| Authority e Safety | 100 | read-only; nessuna acceptance/action/production authority; interlock locali invariati |
| Operability e rollback | 96 | failure atomica e rollback additivo documentati |
| Traceability e validation | 96 | package, closure proposta, backlog, bootstrap, test e CI coerenti; merge/post-merge ancora gate successivi |

## 4. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

Nessuno.

### Observations

#### O-01 — Il contratto F5 non è una futura autorizzazione produttiva

Lo stato `ELIGIBLE_FOR_CALIBRATION_REVIEW` può soltanto aprire una review separata. Un profilo produttivo richiede nuovo identificativo/versione, metodo ed evidence, quindi una nuova decisione architetturale e Release Quality.

#### O-02 — Closure ancora condizionata ai gate di integrazione

L'approvazione ARB non rende effettiva la closure. Restano richiesti Release Quality, merge protetto e workflow/Pages post-merge verdi come dichiarato dal documento di closure.

## 5. Validation evidence

| Gate | Stato | Evidenza |
|---|---|---|
| Local F5 verifier/idempotency | Passed | 15 sessioni; 7/7 stati non soddisfatti; report deterministico |
| Local F5 tests | Passed | 12/12 |
| Local F2–F4 regression | Passed | 43/43 |
| BKL-041 F5 Governance | Passed | run `34600813514` |
| BKL-041 F4 Governance | Passed | run `34600813498` |
| Developer Foundation | Passed | run `34600813586` |
| Scientific Platform Governance | Passed | run `34600813535` |
| Validate documentation | Passed | run `34600813617` |
| Genera manuale Word | Passed | run `34600813543` |
| Analytics consistency | Passed | run `34600813501` |
| Session Comparison | Passed | run `34600813494` |
| BKL-039 regression | Passed | run `34600813539` |

## 6. Decision and next gate

La proposta può passare a Release Quality sul contenuto dell'exact head `060caae867c5f98a91c7c6a314ca272aeb91733d`. Non sono concessi waiver e non restano finding Blocker, Major o Minor aperti.
