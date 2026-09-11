# ARB BKL-046 F4 — AI-Assisted Architecture Review

| Campo | Valore |
|---|---|
| Review ID | ARB-BKL-046-F4-AI-ASSISTED-R1 |
| Package | BKL-046 F4 — Session/Provenance-Driven Read-Only Consumer |
| Review date | 11/09/2026 |
| Pull request | #172 |
| Reviewed proposal head | `1ccb6970ee2789663d32e01d188e8f974393ffbf` |
| Base | `main` @ `ec4eb991bd9e20bcd34b00e111400a5ac07fd750` |
| Review mode | AI-assisted governance assessment; not an independent human review |
| Owner authorization | Required before treating this assessment as an approved governance review |
| Decision | APPROVED WITH CONDITIONS — architecture proposal only |
| Score | 97/100 |

## 1. Review scope

La review valuta esclusivamente la proposta architetturale della PR #172. Non attribuisce implementazione a schema, generator, projection, workflow, consumer, test o runtime descritti come futuri. Non approva qualità scientifica, model/provider, confidence calibrata, PixInsight apply, automatic acceptance o Safety Authority.

L'assessment è AI-assistito e separato logicamente dall'authoring, ma non è una review umana indipendente. La sua eventuale adozione come gate di governance richiede autorizzazione esplicita del repository owner.

## 2. Repository evidence verified

- F3 è Accepted tramite PR #169 e merge `8339aecf0b6b7fa19396561b20253c0411fd7ee7`.
- La riconciliazione F3/F4 è su `main` tramite PR #171 e merge `ec4eb991bd9e20bcd34b00e111400a5ac07fd750`.
- ADR-008 è Accepted e prescrive capture ibrida, evidence class preservate e missingness fail-closed.
- BKL-045 F5 espone un read model read-only e conserva `UNAVAILABLE` senza ricostruire process history.
- L'evidence OAT BKL-045 corrente contiene zero step osservati/dichiarati e `capture.completeness=UNAVAILABLE`.
- `analyze-session-automatic.yml` contiene un first generation path, un retry `regenerate()` dopo reset a `origin/main`, `governed_paths` e deploy Pages successivo al push.
- BKL-041 F4 fornisce un pattern accettato per projection full-catalog, atomic publication e freshness browser-side.
- La PR #172 modifica tre file: primary architecture document, governance index e MkDocs navigation.

## 3. Architecture scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Program and dependency alignment | 100 | F4 segue F3 Accepted e mantiene F5 come successor |
| Domain and layer integrity | 98 | adapter/application/domain/contract/presentation separati; Domain policy indipendente |
| Source authority and provenance | 96 | AP-013/AP-014/BKL-045 ownership preservata; allowlist concreto ancora da chiudere |
| Contract and determinism | 98 | schema chiuso, stable ordering, digest e clock-neutral semantics definiti |
| Dynamic update and atomicity | 99 | first path, retry path, governed paths e Pages ordering sono acceptance gates espliciti |
| Failure behavior | 99 | missing, ambiguous, invalid, stale e tamper falliscono chiuso |
| Security and privacy | 94 | local-first e no image/secret corretti; raw OAT metadata richiedono una public-view decision esplicita |
| Safety and authority | 100 | HUMAN_ONLY, action/execution NONE, interlock locali invariati |
| UX and accessibility | 97 | stati semantici, no-color-only, keyboard/focus/live-region e no mutative controls |
| Observability and operations | 96 | metriche/reason code definiti; nessun nuovo servizio o runbook hardware |
| Migration and rollback | 98 | delivery additiva e rollback senza data/runtime migration |
| Traceability and documentation | 98 | ADR, F2/F3, BKL-045, BKL-041 pattern, roadmap, index e navigation tracciati |

## 4. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

**ARB-F4-C01 — BKL-045 source allowlist non ancora concretizzato**

La proposta richiede un pattern repository-relative chiuso ma non ne stabilisce la forma eseguibile né distingue sidecar runtime da altri JSON di review, fixture o validation. Prima dell'exit gate F4-A, l'implementazione deve definire un allowlist deterministico, validare schema/authority prima dell'inclusione e testare unknown file, traversal, duplicati e ordering.

**ARB-F4-C02 — Public source verification versus OAT host metadata**

Il consumer è descritto come privo di hostname e dati locali, mentre l'evidence OAT BKL-045 corrente contiene un `hostId`. La strategia client-side non deve richiedere di replicare o renderizzare metadati non necessari. Prima dell'exit gate F4-C deve essere scelta e testata una delle seguenti opzioni equivalenti:

1. projection/source snapshot pubblico sanitizzato, derivato e digest-protected;
2. raw-source validation build-time con browser freshness limitata a catalogo, source-set digest pubblicato e projection digest.

In entrambi i casi il portale non deve mostrare hostId, path locali, payload completi, secret o credential.

### Observations

**ARB-F4-O01 — Empty matched population is an acceptable initial result**  
La baseline può produrre zero provenance match esatti. Questo non blocca F4 se tutte le sessioni restano visibili come `PROVENANCE_UNAVAILABLE` e le regole F3 falliscono chiuso.

**ARB-F4-O02 — Clock treatment is appropriate**  
La separazione di `generatedAt` dall'identità scientifica e il no-write quando cambia solo il clock riducono churn e preservano idempotenza.

**ARB-F4-O03 — No new ADR is currently required**  
ADR-008 e il pattern BKL-041 F4 coprono la decisione proposta. Un nuovo store/service, fuzzy correlation o cambio capture strategy richiederebbero una nuova decisione.

## 5. Safety, security and authority assessment

La proposta non introduce canali mutativi, token browser, image upload, PixInsight execution o controllo apparati. Gli interlock fisici locali restano indipendenti. Le condizioni C01/C02 sono defense-in-depth e privacy-by-design; non autorizzano una deroga temporanea.

## 6. Migration and operational assessment

La delivery F4-A/F4-B/F4-C è dependency-ordered e reversibile. Il requisito di rigenerare dopo il reset su `origin/main` è essenziale: una sola invocazione prima del retry non soddisfarebbe l'atomicità. Nessuna migrazione dati, database o servizio residente è giustificato dalla baseline corrente.

## 7. Decision

**APPROVED WITH CONDITIONS — AI-assisted architecture assessment, proposal scope only.**

La PR #172 è architetturalmente idonea al merge come proposta, subordinatamente all'autorizzazione esplicita del repository owner sulla natura AI-assistita della review. L'implementazione F4 non è approvata né accettata da questa decisione.

## 8. Mandatory conditions and re-review criteria

Prima della acceptance F4:

1. `ARB-F4-C01` deve essere chiusa con allowlist eseguibile e negative tests;
2. `ARB-F4-C02` deve essere chiusa con public-data boundary e consumer tests;
3. F4-A/F4-B/F4-C devono produrre evidence implementativa reale;
4. dynamic post-import, retry regeneration e atomic commit devono essere verificati, non soltanto documentati;
5. stale/tamper/correlation/authority failure paths devono essere eseguiti;
6. regressioni F2/F3, exact-head CI, Release Quality, protected merge e post-merge Pages devono essere verdi.

La re-review dovrà distinguere il reviewed implementation head dall'eventuale review-publication head e non potrà convertire la documentazione in prova di runtime.
