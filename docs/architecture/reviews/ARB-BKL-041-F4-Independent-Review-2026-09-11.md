# ARB-BKL-041-F4 — Independent Architecture Review

| Campo | Valore |
|---|---|
| Review | ARB-BKL-041-F4 |
| Data | 11/09/2026 |
| Proposal | `docs/architecture/scientific-assets/BKL-041-F4-Session-Driven-Projection-and-Portal-Consumer.md` |
| Base | `89d8979fa4e5b151d85ef889efe03ad468efcad1` |
| Reviewed head | `ce896b114e5152cf4554c3d570cff6648d96c962` |
| PR | #162 |
| Decision | APPROVED |
| Score | 98/100 |

## 1. Executive decision

**APPROVED — 98/100.**

BKL-041 F4 realizza il requisito session-driven senza estendere l'authority dello score. La projection viene rigenerata dal catalogo canonico nello stesso commit atomico degli altri derivati di ogni import completato. Il consumer verifica con SHA-256 catalogo, projection, profile e authority prima di rendere i dati e fallisce chiuso senza stale fallback.

Il profilo resta esplicitamente sintetico e gli output sono `EXPERIMENTAL_NOT_ACCEPTED`. I record `INVALID` riflettono il reject dei bounds dimostrativi e non sono trasformati in classi qualitative. Non risultano Blocker, Major o Minor aperti. Le observation sono entry condition per F5, non remediation F4.

## 2. Repository truth verificata

| Elemento | Evidenza | Esito |
|---|---|---|
| Baseline F3 | PR #161, merge `89d8979fa4e5b151d85ef889efe03ad468efcad1`, ARB 98/100 | F3 riconciliata Accepted |
| Source of truth | `docs/data/scientific-session-catalog.json` | unico input session-driven |
| Projection | schema F4 1.0, generator e dataset full-catalog | 15 record deterministici |
| Stato corrente | 5 available, 3 unavailable, 7 invalid | failure semantics esplicite |
| Pipeline | `analyze-session-automatic.yml` | write/check/test e governed path nello stesso ciclo di commit/retry |
| Freshness | digest canonico catalogo, session count/id e projection digest | verificata in CI e Web Crypto |
| Presentation | score, confidence, coverage, decomposition, exclusions e limitazioni | semanticamente congiunti |
| Authority | read-only, no production/acceptance/action authority, Safety locale | conforme e fail-closed |
| Roadmap/continuity | source canonica, projection governata, bootstrap, backlog, handover e baseline | F4 corrente; F5 riservata |

## 3. Scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Scope e semantic integrity | 99 | F4 integra projection/consumer; produzione e closure restano F5. |
| Domain e layer integrity | 99 | generator repository-side puro, projection separata dalla source e consumer senza mutation path. |
| Data contract e provenance | 98 | schema chiuso, evidence sempre `DECLARED`, missing e out-of-range preservati. |
| Determinism e identity | 100 | canonical SHA-256, ordinamento, projection digest e rigenerazione idempotente. |
| Freshness e atomic publication | 100 | catalogo/projection nello stesso commit; retry rigenera; browser confronta il contenuto corrente. |
| Explainability e UX semantics | 98 | score, confidence, coverage, decomposition, exclusions e stato sperimentale co-presenti. |
| Scientific integrity e bias | 96 | nessuna claim produttiva; bounds sintetici e guiding coverage gap restano visibili. |
| Safety, security e authority | 100 | nessun secret/API mutativa/device path; authority esatta e interlock locali invariati. |
| Operability e observability | 98 | failure nel workflow e nel consumer, test stale/tamper e nessun fallback ambiguo. |
| Migration e rollback | 99 | cambiamento additivo e repository-only; F2/F3/catalogo restano compatibili. |
| Traceability e documentation | 99 | proposta, nav, continuity, roadmap, workflow e PR coerenti. |
| Validation evidence | 99 | 43 test locali e nove workflow exact-head verdi, incluso strict docs tramite CI. |

## 4. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

Nessuno.

### Observations

#### O-01 — Calibrazione e cohort F5

I 5 risultati available sono prove d'integrazione su un profilo sintetico, non validation evidence scientifica. F5 deve definire cohort rappresentative per target, filtro, setup e condizioni, un nuovo profile id/version, criteri di calibrazione e analisi dei bias prima di qualsiasi uso produttivo.

#### O-02 — Guiding temporal coverage

Il catalogo espone RMS e sample count ma non un denominatore temporale governato. F4 usa correttamente coverage zero e lascia che la confidence rappresenti il gap. Una futura coverage diversa da zero richiede un'estensione versionata della source e nuova review.

#### O-03 — Operational monitoring

Il failure è visibile nei log Actions e nel consumer. Se in futuro la projection diventa un servizio con SLO, sarà necessario introdurre telemetry/alerting dedicati; non è richiesto per questa projection statica read-only.

#### O-04 — Pages post-merge

La superficie portale richiede verifica del deployment Pages sul merge commit. Il deployment non è una precondizione architetturale del PR, ma è evidence obbligatoria di chiusura operativa F4.

## 5. Architecture, security and authority review

Il generator mappa soltanto dati già governati nel catalogo e invoca l'engine F3 senza accesso a rete, credenziali o apparati. La projection è un read model sostituibile e non modifica AP-013/AP-014. Il browser usa `cache: no-store`, ma la garanzia sostanziale deriva dal digest del contenuto e non dalla cache policy.

L'authority ammessa è esatta: `consumerMode=READ_ONLY`, `productionUseAuthorized=false`, `acceptanceAuthority=false`, `actionAuthority=NONE`, `safetyAuthority=LOCAL_PHYSICAL_INTERLOCKS`. Qualsiasi escalation fa fallire il consumer prima del rendering. Non esistono command path, recommendation, remediation o dipendenze dalla Safety Authority.

## 6. Validation matrix

| Gate | Stato | Evidenza |
|---|---|---|
| Local F4 verifier/idempotency | Passed | 15 sessioni; 5 available, 3 unavailable, 7 invalid; freshness match |
| Local automated tests | Passed | 12 F4 + 19 F3 + 12 F2 = 43/43 |
| Local browser syntax | Passed | core module, consumer e page enhancements |
| Local MkDocs strict build | Not Executed | dipendenza MkDocs assente nel runtime locale; coperta dalla CI |
| BKL-041 F4 Governance | Passed | #1, run `34588699494` |
| BKL-041 F3 Governance | Passed | #6, run `34588699404` |
| Developer Foundation | Passed | #1292, run `34588699467` |
| Scientific Platform Governance | Passed | #47, run `34588699457` |
| Validate documentation | Passed | #925, run `34588699459` |
| Genera manuale Word | Passed | #1350, run `34588699461` |
| Analytics Center consistency | Passed | #29, run `34588699435` |
| Session Comparison projection | Passed | #13, run `34588699516` |
| BKL-039 F5 regression | Passed | #48, run `34588699472` |
| Runtime/device/Safety OAT | Not Applicable | nessun runtime osservativo o command path modificato |
| Pages deployment | Pending post-merge | superficie portale nuova; verificare sul merge SHA |

## 7. Failure, migration e rollback

- catalogo nuovo con projection vecchia: browser reject per digest/count/id mismatch;
- catalogo variato a parità di session id: browser reject per digest mismatch;
- projection o authority alterata: reject prima del rendering;
- evidence required mancante: record unavailable con score/confidence null;
- valore fuori profilo: record invalid isolato, senza bloccare gli altri record;
- failure di generazione: il workflow non committa un set parziale e non richiede il deploy;
- rollback: revert di consumer, projection e integrazione F4; catalogo e motore F3 restano validi.

## 8. Decision and re-review criteria

Il PR #162 sul reviewed head `ce896b114e5152cf4554c3d570cff6648d96c962` è **APPROVED FOR RELEASE QUALITY REVIEW** per il solo scope F4.

Richiedono nuova review:

- profilo, bounds, pesi o calibrazione produttivi;
- estensione della coverage guiding o del mapping evidence;
- modifica di identity, freshness o atomic publication;
- threshold, ranking, classi qualitative, recommendation o acceptance;
- API mutative, remediation, device command o Safety Authority;
- F5 validation/closure.

L'approvazione F4 non autorizza uso produttivo dello score né anticipa l'acceptance F5.
