# ARB BKL-046 F4-C — AI-Assisted Implementation Review

| Campo | Valore |
|---|---|
| Review ID | ARB-BKL-046-F4-AI-ASSISTED-R2 |
| Package | BKL-046 F4 — Session/Provenance-Driven Read-Only Consumer, implementation F4-C |
| Review date | 12/09/2026 |
| Pull request | #175 |
| Reviewed implementation head | `b2f8543d0a7fd3e354c40d9acb0206ef7e6edea4` |
| Base | `main` @ `a7db5c95f413282109174d7d8662a57c4ed9590c` |
| Review mode | **AI-assisted governance assessment; not an independent human review** |
| Publication authority | Repository owner authorization recorded 12/09/2026 |
| Decision | **APPROVED WITH CONDITIONS — AI-assisted, owner-authorized** |
| Score | **99/100** |
| Active findings | Blocker 0 · Major 0 · Minor 0 · Observation 2 |

## 1. Review scope and independence statement

La review valuta l'implementazione F4-C della PR #175 e la sua coerenza con le baseline F4-A/F4-B già integrate. L'assessment è stato prodotto nella stessa sessione AI che ha assistito l'authoring: non è quindi una review umana indipendente e non viene rappresentato come tale. Il repository owner ne ha autorizzato la pubblicazione e l'uso come gate AI-assistito.

La decisione non approva model/provider, inferenza AI, confidence scientifica, Human Decision Receipt automatico, PixInsight apply, remediation, device command o modifica della Safety Authority.

## 2. Evidence verificata

- PR #175 aperta e mergeable sul reviewed head `b2f8543d0a7fd3e354c40d9acb0206ef7e6edea4`;
- 9 file di implementazione sul technical head, con consumer, core validator, CSS, pagina, test, workflow, navigazione e documentazione;
- BKL-046 F4 governance run `34663056036`: SUCCESS;
- BKL-041 F4 regression run `34663056057`: SUCCESS;
- Developer Foundation run `34663056032`: SUCCESS;
- Validate documentation run `34663056031`: SUCCESS;
- Word build run `34663056037`: SUCCESS;
- F4 projection suite: 24/24 PASS;
- F4 consumer suite sulla projection persistita: 11/11 PASS, 0 skipped;
- F2 regression: 16/16 PASS; F3 regression: 21/21 PASS;
- projection F4 allineata a 15 sessioni, 0 provenance matched e 15 processing-history gate fail-closed;
- verifier F4-B: projection e integrazione atomica first/retry path verificate.

## 3. Architecture scorecard

| Dimensione | Score | Evidenza |
|---|---:|---|
| Program and dependency alignment | 100 | F4-C segue F4-A/F4-B e non anticipa F5 |
| Domain and layer integrity | 99 | validator/presentation separati dalle regole F3 e dagli adapter build-time |
| Source authority and provenance | 100 | catalogo AP-014 e snapshot BKL-045 sanitizzato mantengono ownership distinti |
| Contract closure and determinism | 100 | contratti top-level e F2 annidati chiusi; digest chain completa |
| Failure behavior | 100 | stale, tamper, unknown property, authority drift e Web Crypto assente falliscono chiuso |
| Security and privacy | 100 | raw sidecar, hostId, path locali, image data e secret non raggiungono il browser |
| Safety and authority | 100 | READ_ONLY, HUMAN_ONLY, action/execution NONE, interlock locali invariati |
| UX and accessibility | 97 | tastiera, focus, live region, non-color label e reduced motion testati staticamente |
| Observability and operations | 97 | reason code, summary, limitation e hard-failure visibili; nessun nuovo servizio |
| Migration and rollback | 100 | cambiamento additivo e revert isolato dal catalogo/provenance |
| Traceability and quality evidence | 99 | architecture, test, workflow, PR e run exact-head correlati |

**Score complessivo: 99/100.**

## 4. Findings

### Blocker

Nessuno.

### Major

Nessun finding attivo.

**ARB-F4C-M01 — CLOSED BEFORE DECISION — contratto F2 annidato non completamente chiuso**

La prima ispezione del consumer ha rilevato che `subject`, `sourceBinding`, `recommendation`, `confidence` e `parameterAdvice` non rifiutavano ogni proprietà o stato sconosciuto. Il commit `b2f8543d0a7fd3e354c40d9acb0206ef7e6edea4` ha chiuso i key-set e gli enum annidati e ha aggiunto un test negativo che verifica il rifiuto anche quando i valori aggiunti hanno forma digest-valid. La consumer suite exact-head è 11/11 PASS. Il finding è chiuso.

### Minor

Nessuno.

### Observations

**ARB-F4C-O01 — Popolazione reale senza provenance correlata**

Le 15 sessioni correnti hanno zero match BKL-045 esatti. Il risultato è accettabile perché tutte restano visibili come `PROVENANCE_UNAVAILABLE` e il processing-history gate è `FAIL_CLOSED`; non viene creato alcun fuzzy match.

**ARB-F4C-O02 — Verifica visuale Pages post-merge**

La struttura accessibility è coperta da test e MkDocs strict, ma la verifica visuale/interattiva sul sito Pages può essere eseguita soltanto dopo la pubblicazione del merge. È una condizione di acceptance, non prova già acquisita.

## 5. Architecture integrity

Il browser consuma esclusivamente `docs/data/scientific-session-catalog.json` e `docs/data/ai-post-processing-advisory-projection.json` con `cache: no-store`. Prima del rendering valida schema chiuso, catalog digest, session set, source-set digest, projection identity, authority, binding/recommendation/record digest, summary e projection digest.

Il raw evidence BKL-045 resta build-time; il client riceve soltanto lo snapshot pubblico sanitizzato. Il consumer non modifica catalogo, recommendation, decisione o immagini e non espone controlli Apply, Execute o Accept.

## 6. Safety, security and operational assessment

- nessun comando verso EAGLE, PixInsight o apparati;
- nessun token, secret, path locale o immagine introdotto;
- stato non verificabile o Web Crypto assente producono hard fail-closed;
- la Safety Authority resta `LOCAL_PHYSICAL_INTERLOCKS`;
- rollback tramite revert degli artefatti F4-C, senza migrazione dati.

## 7. Governance exception

`main` è risultato non protetto. Il repository owner ha autorizzato il 12/09/2026 una deroga una tantum limitata alla PR #175. La deroga non modifica l'architettura né l'authority del prodotto e non costituisce precedente permanente.

I controlli compensativi obbligatori sono: PR aperta, review pubblicate, CI completa sul publication head, merge con `expected_head_sha`, verifica dei workflow post-merge e verifica Pages. La formalizzazione del rischio e la disposition della waiver sono affidate alla Release Quality review associata.

## 8. Decision

**APPROVED WITH CONDITIONS — AI-assisted, owner-authorized.**

Non risultano Blocker, Major o Minor aperti. L'implementazione F4-C è architetturalmente idonea al merge con la deroga una tantum, subordinatamente a:

1. tutti i workflow applicabili verdi sul commit che pubblica le review;
2. merge della sola PR #175 con SHA atteso;
3. workflow `main` e deploy Pages verdi sul merge SHA;
4. verifica visuale/interattiva del consumer pubblicato;
5. acceptance record F4 separato, basato su evidence post-merge.

## 9. Re-review criteria

È obbligatoria una nuova review se cambiano contract/digest, source authority, correlation, recommendation rules, model/provider, dati immagine, decision/action/execution authority, PixInsight apply, apparati o Safety Authority.

## 10. Traceability

- [F4 architecture](../scientific-assets/BKL-046-F4-Session-Provenance-Driven-Read-Only-Consumer.md)
- [F4 proposal ARB](ARB-BKL-046-F4-AI-Assisted-Architecture-Review-2026-09-11.md)
- [F4-C Release Quality](RQ-BKL-046-F4C-AI-Assisted-Release-Quality-Review-2026-09-12.md)
- [F3 acceptance](../../project/BKL-046-F3-ACCEPTANCE-2026-09-11.md)
- [PR #175](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/175)
