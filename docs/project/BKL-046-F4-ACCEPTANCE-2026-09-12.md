# BKL-046 F4 — Acceptance Record

| Campo | Valore |
|---|---|
| Incremento | BKL-046 F4 — Session/Provenance-Driven Read-Only Consumer |
| Stato | CLOSED / ACCEPTED / POST-MERGE VERIFIED |
| Data | 12/09/2026 |
| Pull request | #175 |
| Accepted merge | `af48cc2441cf956d88c13c81845fc2a2f7c599f2` |
| Reviewed implementation head | `b2f8543d0a7fd3e354c40d9acb0206ef7e6edea4` |
| Review-publication head | `ae1b8f2ae04fc9c4891e794bc930ec0e09fcf640` |
| Review mode | AI-assisted, repository-owner authorized; not an independent human approval |
| Branch-protection waiver | `W-BKL046-F4-001` — PR #175 only; consumed and expired at merge |
| Successore | BKL-046 F5 — Real-Evidence Evaluation and Capability Closure design |

## 1. Acceptance decision

BKL-046 F4 è accettato come consumer deterministico, session/provenance-driven, read-only, pre-decisione e freshness-verified. L'incremento porta le regole F3 sulle 15 sessioni del catalogo canonico, pubblica la projection nello stesso commit governato del post-import e rende visibili source state, rationale, reason code, citation e limitation senza inferire evidence mancante.

Le valutazioni ARB e Release Quality sono review AI-assistite autorizzate dal repository owner. Non costituiscono approvazioni umane indipendenti e non ampliano l'authority tecnica o scientifica dell'incremento.

## 2. Evidence verificata

| Evidenza | Esito |
|---|---|
| F4 projection suite | 24/24 test PASS |
| F4 consumer suite | 11/11 test PASS |
| F2 regression | 16/16 test PASS |
| F3 regression | 21/21 test PASS |
| Persisted projection | 15 sessioni; 0 provenance matched; 15 provenance unavailable; 15 history fail-closed |
| Atomic workflow verifier | first path, retry path e `governed_paths` PASS |
| ARB F4-C R2 | APPROVED WITH CONDITIONS, 99/100, 0 Blocker/Major/Minor attivi |
| Release Quality F4-C R2 | READY FOR MERGE con owner-approved one-time waiver |
| Post-merge workflows | 6/6 SUCCESS sul merge accettato |
| Live Pages | freshness verificata; ricerca, filtri e dettaglio sessione operativi |

Workflow post-merge verificati sul commit `af48cc2441cf956d88c13c81845fc2a2f7c599f2`:

| Workflow | Run | Esito |
|---|---:|---|
| Deploy Pages #776 | `34664520952` | SUCCESS |
| BKL-041 F4 Governance #39 | `34664520962` | SUCCESS |
| BKL-046 F4 governance #9 | `34664520958` | SUCCESS |
| Validate documentation #969 | `34664520964` | SUCCESS |
| Genera manuale Word #1394 | `34664520981` | SUCCESS |
| Developer Foundation #1333 | `34664520999` | SUCCESS |

## 3. Live acceptance

La pagina `https://maininimassimo-bit.github.io/digital-stargate-manual/ai-post-processing-assistant/` è stata verificata dopo il merge. Il consumer ha confermato freshness e digest, 15 sessioni, 0 provenance matched, 15 provenance unavailable e 15 history fail-closed. La ricerca ha restituito la sessione attesa; i filtri hanno preservato gli stati reali; il link di dettaglio ha aperto `scientific-session-detail/?sessionId=2026-09-07_2026-09-08`. Non sono stati osservati errori applicativi in console né overflow orizzontale a 1348 px.

## 4. Quality gate matrix

| Gate | Esito | Evidenza / decisione |
|---|---|---|
| Scope e authority | PASS | READ_ONLY, HUMAN_ONLY, action/execution NONE |
| Source authority | PASS | catalogo AP-014 e provenance BKL-045 separati e sanitizzati |
| Determinismo | PASS | identity, ordering, record/source/projection digest verificati |
| Fail-closed | PASS | stale, tampering, missing, ambiguous, unknown schema/authority e Web Crypto assente |
| Dynamic update | PASS | generator in first/retry path e pubblicazione atomica |
| UX/accessibility | PASS | ricerca, filtri, rationale, citation, focus, live region, reduced motion |
| Security/privacy | PASS | nessuna immagine, secret, path locale, upload o raw sidecar nel browser |
| Safety | PASS | interlock fisici locali invariati; nessuna command authority |
| Review independence | DISCLOSED LIMITATION | review AI-assistite, owner-authorized, non umane indipendenti |
| Branch protection | ONE-TIME WAIVER CONSUMED | `W-BKL046-F4-001`, valida soltanto per PR #175 |

## 5. Contratti e comportamento accettati

- popolazione completa determinata dal catalogo AP-014;
- correlation exact-match; nessun fuzzy match per target, data o pathname;
- regole F3 riusate senza secondo rule set;
- projection persistita e digest-protected rigenerata dopo ogni import;
- consumer browser `cache: no-store` con verifica di catalog, session set, source set e projection digest;
- Recommendation distinta da Human Decision Receipt ed execution evidence;
- nessun controllo Apply, Execute o automatic acceptance.

## 6. Limitation e rischi trattenuti

- le 15 sessioni non hanno provenance BKL-045 correlabile esattamente nella baseline accettata;
- la completezza automatica della processing history PixInsight resta `UNAVAILABLE` dove non osservata;
- F4 non dimostra quality/confidence scientifica, outcome improvement, ground truth o production readiness;
- nessun modello, provider, RAG/vector store, image transfer o PixInsight apply path è selezionato;
- una Recommendation validata contrattualmente non equivale a decisione umana o prova di esecuzione.

## 7. Chiusura della deroga

La deroga `W-BKL046-F4-001` ha coperto esclusivamente l'assenza di branch protection server-side per la PR #175. Il merge è stato eseguito con controllo dell'expected head e seguito dalla verifica post-merge. La deroga è consumata e scaduta: non autorizza merge successivi e non si trasferisce alla PR di acceptance o a F5.

## 8. Transition decision

È promosso esclusivamente BKL-046 F5 — Real-Evidence Evaluation and Capability Closure come incremento di architettura/design. F5 deve definire cohort, sufficienza delle evidenze, criteri di valutazione e limitation trattenute prima di qualsiasi decisione di closure.

Restano fuori scope model/provider, confidence scientifica, automatic acceptance, PixInsight apply, remediation, device command e Safety Authority.
