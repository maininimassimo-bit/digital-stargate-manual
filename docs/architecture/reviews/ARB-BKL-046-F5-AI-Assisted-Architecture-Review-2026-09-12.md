# ARB BKL-046 F5 — AI-Assisted Architecture Review

| Campo | Valore |
|---|---|
| Review ID | ARB-BKL-046-F5-AI-ASSISTED-R1 |
| Package | BKL-046 F5 — Real-Evidence Evaluation and Capability Closure |
| Review date | 12/09/2026 |
| Pull request | #177 |
| Reviewed proposal head | `5758c9193ff0160e8ece54e56470e2d5ed5ecdd1` |
| Base | `main` @ `bc86264a4a689492087182e121820aa6cce06025` |
| Review mode | AI-assisted governance assessment; not an independent human review |
| Owner authorization | Granted 12/09/2026 for PR #177 only |
| Review-independence waiver | `W-BKL046-F5-ARCH-REVIEW-001` |
| Decision | **APPROVED WITH CONDITIONS — architecture/design proposal only** |
| Score | **97/100** |

## 1. Review scope and independence disclosure

La review valuta esclusivamente il package architetturale proposto nella PR #177. Non attribuisce implementazione al contratto F5, evaluator, generator, projection, workflow, consumer, test o runtime descritti come futuri e non approva una closure della capability.

La valutazione è AI-assistita, autorizzata dal repository owner e **non equivale a un'approvazione umana indipendente**. La deroga `W-BKL046-F5-ARCH-REVIEW-001` consente una sola pubblicazione delle review ARB/RQ per questa PR e per il proposal head indicato. Non sostituisce l'autorizzazione al merge, non deroga alla CI, non autorizza branch-protection bypass e non può essere riusata.

## 2. Repository evidence verified

- F4 è CLOSED / ACCEPTED / POST-MERGE VERIFIED tramite PR #175 e merge `af48cc2441cf956d88c13c81845fc2a2f7c599f2`.
- La baseline repository della proposta è `bc86264a4a689492087182e121820aa6cce06025`.
- La PR #177, al proposal head verificato, contiene un commit e nove file: 466 addition e 8 deletion; è mergeable e non è draft.
- Il catalogo canonico contiene 15 sessioni: LDN 1320 = 3, M 27 = 11, UNKNOWN = 1.
- La projection F4 `BKL046-F4-1D2BB9C8F92DAADB836A6137` contiene 0 provenance matched, 15 unavailable, 2 source non correlate, 15 processing-history FAIL_CLOSED e nessuna Human Decision Receipt.
- Il package separa technical capability, scientific effectiveness, human-decision evidence e production readiness.
- Le cohort scientifica, decisionale ed execution correnti sono vuote e vengono rappresentate come `NOT_EVALUABLE` / `NOT_AVAILABLE`, senza percentuali permissive.
- `aiModelImplemented=false`, `NOT_READY_FOR_PRODUCTION`, assenza di apply/command e Safety Authority locale sono vincoli espliciti.
- I comandi F5 e gli artefatti F5-A/F5-B sono dichiarati proposed/not executed.
- Cinque workflow sul proposal head sono conclusi con successo: BKL-046 F4 governance `34678320967`, BKL-041 F4 Governance `34678320934`, Validate documentation `34678320957`, Developer Foundation `34678320960`, Genera manuale Word `34678320955`.
- Le deroghe F4 precedenti sono consumate/scadute e non vengono riutilizzate.

## 3. Architecture scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Program and dependency alignment | 100 | F5 segue F4 Accepted e preserva la sequenza F5-A/F5-B/F5-C |
| Domain and layer integrity | 98 | policy pura separata da filesystem, workflow, persistence e browser |
| Source authority and provenance | 94 | authority e exact-correlation preservate; discovery concreta delle future receipt/evidence resta da chiudere |
| Contract and determinism | 96 | schema chiuso, identity e digest previsti; registry di stati/reason code non ancora enumerato |
| Evidence and scientific integrity | 100 | missingness, cohort vuote e assenza di ground truth non diventano risultati positivi |
| Dynamic update and atomicity | 99 | first/retry, `governed_paths`, drift e freshness chain sono gate espliciti |
| Failure behavior | 99 | tamper, stale, unknown authority ed evidence inventata falliscono chiuso |
| Security and privacy | 98 | vietati raw sidecar, path locali, hostname, immagini, secret, token e upload |
| Safety and authority | 100 | read-only, human-only, non-production; interlock fisici locali invariati |
| Observability and operations | 95 | conteggi/digest/reason code previsti; catalogo eseguibile dei reason code ancora da produrre |
| Migration and rollback | 98 | incremento additivo e rimozione F5 senza regressione di F1-F4 |
| Traceability and documentation | 99 | handoff, architecture, validation, F4 baseline, backlog, index e navigation coerenti |

## 4. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

**ARB-F5-C01 — Discovery e correlazione delle future Human Decision Receipt ed execution evidence**

Il package definisce correttamente le cohort `HUMAN-DECISION-RECEIPTS-F5` ed `EXECUTION-EVIDENCE-F5`, ma rimanda a F5-A la forma eseguibile delle source. Prima dell'exit gate F5-A devono essere definiti path/allowlist canonici, schema e authority ammessi, chiavi di correlazione esatte, ordering, duplicate policy e negative test per file sconosciuti, traversal, receipt orfane e correlation mismatch. In assenza di una source valida lo stato deve restare `NOT_AVAILABLE`, senza inferenza.

**ARB-F5-C02 — Registro chiuso di stati e reason code**

La proposta richiede reason code chiusi ma non ne enumera ancora il catalogo. F5-A deve introdurre una registry machine-readable per cohort, technical gates e quattro outcome, con mapping deterministico, unknown-value rejection e test che impediscano di convertire `NOT_EVALUABLE`, `NOT_AVAILABLE` o `NOT_READY_FOR_PRODUCTION` in PASS impliciti.

### Observations

**ARB-F5-O01 — Closure tecnica separata dall'efficacia scientifica**  
La decision table consente correttamente una closure della capability deterministica read-only con limitation senza dichiarare efficacia scientifica o AI runtime.

**ARB-F5-O02 — Nessuna soglia scientifica inventata**  
La scelta di lasciare aperti ground truth, protocollo umano e rappresentatività evita una falsa precisione. Tali decisioni richiedono evidence e review future.

**ARB-F5-O03 — Nessuna nuova ADR richiesta per il proposal scope**  
Il package riusa exact correlation, contratti, atomic projection e authority già accettati. Model/provider, fuzzy matching, nuovo store/service, image transfer o apply path richiederebbero un package separato e una nuova ADR.

## 5. Domain, contract and dependency assessment

Le dipendenze procedono dai contratti e dalla projection F4 verso una domain policy deterministica, quindi verso generator, projection, verifier e consumer. Non emerge una dipendenza UI-to-domain né un nuovo bounded context. Il report F5 è una projection derivata e non acquisisce ownership su catalogo, provenance, Human Decision o Safety.

L'uso di BKL-041 come solo contesto sperimentale, esplicitamente vietato come ground truth, previene dipendenza circolare e self-supporting evidence.

## 6. Security, privacy, safety and operability

Il design è local-first e non introduce rete esterna, provider, credenziali, dati immagine, endpoint mutativi o processi residenti. Nessun elemento F5 comanda EAGLE, N.I.N.A., PHD2, PixInsight, ASCOM o apparati. `LOCAL_PHYSICAL_INTERLOCKS` resta l'unica Safety Authority.

L'operabilità proposta è coerente con il percorso automatico esistente: generazione e verifica sia nel first path sia dopo il retry, commit atomico con gli input governati, failure esplicita e rollback additivo.

## 7. Decision

**APPROVED WITH CONDITIONS — AI-assisted architecture/design assessment only.**

Il package è architetturalmente idoneo al merge come proposta. L'autorizzazione owner sulla modalità AI-assistita è stata ricevuta ed è registrata mediante `W-BKL046-F5-ARCH-REVIEW-001`. Restano obbligatori:

1. CI verde sull'exact head che pubblica le review;
2. assenza di modifiche materiali al proposal head, oppure nuova review;
3. autorizzazione al merge separata;
4. disposizione esplicita della branch protection, senza deroga implicita.

Questa decisione non approva F5-A/F5-B/F5-C, non chiude BKL-046 e non autorizza model/provider, confidence scientifica, produzione, automatic acceptance, PixInsight apply, remediation, command path o Safety Authority.

## 8. Mandatory conditions and re-review criteria

Prima dell'exit gate F5-A:

1. chiudere `ARB-F5-C01` con source allowlist, exact-correlation e negative tests;
2. chiudere `ARB-F5-C02` con registry machine-readable e unknown rejection;
3. implementare contratto, evaluator, generator, persisted report, verifier e test senza rappresentarli come già esistenti;
4. dimostrare known answer, empty-cohort semantics, determinism, anti-tampering e no-self-evidence;
5. mantenere verdi le regressioni F2-F4.

Prima di una closure F5 servono inoltre evidence F5-B/F5-C, publication/merge/post-merge CI e un closure record che mantenga separati capability acceptance, scientific evidence e production authorization.

Una modifica materiale a cohort, authority, source ownership, decision table, model/provider, persistence, image transfer, apply path o Safety boundary invalida questa review e richiede re-review.
