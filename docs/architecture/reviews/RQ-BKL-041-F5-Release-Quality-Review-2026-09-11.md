# RQ-BKL-041-F5 — Release Quality Review

| Campo | Valore |
|---|---|
| Review | RQ-BKL-041-F5 |
| Data | 11/09/2026 |
| Capability | BKL-041 — Scientific Data Quality Score |
| Increment | F5 — Real-Evidence Validation and Capability Closure |
| PR | #163 |
| Proposal head | `060caae867c5f98a91c7c6a314ca272aeb91733d` |
| Reviewed head | `12abeaa3ac98ee4b23234e1f63e161ff003c84ac` |
| ARB | ARB-BKL-041-F5-R1 — APPROVED 98/100 |
| Recommendation | READY FOR MERGE |

## 1. Release impact report

BKL-041 F5 aggiunge una validation deterministica sull'intera cohort canonica reale, concatenata tramite digest a catalogo e projection F4 e rigenerata nello stesso commit atomico dopo ogni import. Il portale espone la distinzione fra acceptance tecnica della capability sperimentale read-only, readiness degli input di calibrazione e autorizzazione produttiva.

L'evidence corrente descrive 15 sessioni, 2 target noti, 5 assessment disponibili, 3 unavailable, 7 invalid, SQM su 8 sessioni e guiding temporal coverage governata assente. Questi numeri non sono threshold. I sette stati richiesti non sono dimostrati; `productionReadiness` resta invariabilmente `NOT_READY_FOR_PRODUCTION` e nessuna authority produttiva, operativa o di sicurezza è introdotta.

| Area | Impatto |
|---|---|
| Architecture | solution increment F5 e closure proposta della capability sperimentale read-only |
| Data contract | nuovo schema F5 chiuso e additivo; catalogo e projection F4 invariati |
| Pipeline | validation F5 generata e verificata nel workflow canonico e nel retry atomico |
| Portal | banner e freshness chain fino al report F5; failure stale/tamper fail-closed |
| Scientific semantics | stati governati senza soglie inventate; bias, missingness e limitation espliciti |
| CI/CD | gate F5, test negativi e regressioni F2–F4 |
| Roadmap/continuity | F4 riconciliato Accepted; F5 corrente; BKL-046 solo dopo closure verificata |
| Operations | nessuna modifica al runtime osservativo; deploy Pages dopo merge |
| Safety | nessun cambiamento; interlock locali restano authority indipendente |

## 2. Quality-gate matrix

| Gate | Stato | Evidence |
|---|---|---|
| Scope / non-scope | Passed | validation e closure sperimentale; produzione, ranking, acceptance e command path esclusi |
| F4 prerequisite | Passed | PR #162 merge `ed9ffcc92e1a5252b0d8c37634bc652397f3cde1` |
| Architecture coherence | Passed | ARB R1 APPROVED 98/100; nessun finding aperto |
| Cohort completeness | Passed | tutte le 15 sessioni incluse con selection rule machine-readable e senza outcome filtering |
| Scientific integrity | Passed | threshold non governati rimossi; conteggi soltanto descrittivi |
| Contract closure | Passed | root e oggetti governati chiusi; requirement/result/metric tipizzati; unknown-property reject |
| Lifecycle compatibility | Passed | input eligibility separata; production readiness e authority restano false in ogni ramo |
| Deterministic generation | Passed | report riproducibile, canonical digest e idempotency check |
| Automatic refresh | Passed | catalogo, F4 e F5 rigenerati nello stesso ciclo atomico/retry |
| Freshness fail-closed | Passed | digest catalogo/projection/validation e session identity verificati |
| Explainability e UX | Passed | cohort, bias, gap, capability acceptance e non-production outcome co-presenti |
| Accessibility/responsiveness | Passed | markup semantico e strict documentation build verde |
| Authority / Safety | Passed | read-only; production/acceptance false; action none; interlock locali |
| Security / privacy | Passed | nessun secret, endpoint mutativo o dato aggiuntivo rispetto al catalogo pubblicato |
| Observability | Passed | failure di workflow e stato consumer non disponibile senza fallback stale |
| Migration / compatibility | Passed | incremento additivo; F2–F4 e dati canonici preservati |
| Rollback | Passed | revert repository-only; nessuna azione su runtime o apparati |
| BKL-041 F5 Governance | Passed | run `34601373339` |
| BKL-041 F4 Governance | Passed | run `34601373506` |
| Developer Foundation | Passed | run `34601373412` |
| Scientific Platform Governance | Passed | run `34601373294` |
| Validate documentation | Passed | run `34601373423` |
| Genera manuale Word | Passed | run `34601373355` |
| Analytics Center consistency | Passed | run `34601373331` |
| Session Comparison projection | Passed | run `34601373299` |
| BKL-039 F5 regression | Passed | run `34601373373` |
| PR integration state | Passed | exact head, base F4, mergeable clean, non-draft |
| Pages deployment | Not Executed pre-merge | obbligatoria verifica sul merge commit |
| Runtime/device/Safety OAT | Not Applicable | nessun componente osservativo o command path modificato |

## 3. Definition of Done assessment

| Criterio | Stato |
|---|---|
| cohort completa e selection rule versionata | Passed |
| validation deterministica, generated e freshness-linked | Passed |
| aggiornamento automatico dopo ogni import | Passed |
| stati di readiness governati senza threshold inventati | Passed |
| future-input path compatibile e non autorizzativo | Passed |
| schema/browser fail-closed su proprietà sconosciute | Passed |
| authority e limitation non produttive | Passed |
| test F5 e regressioni F2–F4 | Passed |
| architecture, closure proposta, backlog e bootstrap coerenti | Passed |
| ARB senza Blocker/Major/Minor aperti | Passed |
| CI exact-head applicabile verde | Passed |
| protected merge e Pages post-merge | Deferred to integration verification |

## 4. Risk register

| ID | Rischio | Probabilità | Impatto | Trattamento | Stato |
|---|---|---|---|---|---|
| RQ41F5-R01 | report stale dopo nuova importazione | Bassa | Alto | rigenerazione atomica, digest chain e browser reject | Controlled |
| RQ41F5-R02 | conteggi descrittivi interpretati come threshold | Bassa | Alto | policy state-based, documentazione e test anti-threshold | Controlled |
| RQ41F5-R03 | input eligibility interpretata come production approval | Bassa | Alto | campi separati; production state costante; authority false | Controlled |
| RQ41F5-R04 | capability acceptance interpretata come qualità delle immagini | Bassa | Alto | banner, limitation e assenza di ranking/classificazione | Controlled |
| RQ41F5-R05 | schema/consumer drift | Bassa | Alto | exact-key validator, typed schema, digest e regressioni | Controlled |
| RQ41F5-R06 | failure di generazione produce set parziale | Bassa | Alto | generator prima del commit; retry full regeneration | Controlled |
| RQ41F5-R07 | futura calibrazione riusa implicitamente F3 | Media | Alto | nuovo contratto/profile/version e nuove ARB/RQ obbligatorie | Deferred with gate |

## 5. Waiver register

Nessun waiver richiesto.

Il deployment Pages e la chiusura effettiva sono gate post-merge dichiarati, non waiver. La calibrazione produttiva resta fuori scope e richiede una futura iniziativa separata.

## 6. Validation commands and evidence

Eseguito localmente:

```text
node .github/scripts/generate-scientific-data-quality-f5-validation.mjs --write
node .github/scripts/verify-scientific-data-quality-f5-validation.mjs
node .github/scripts/generate-scientific-data-quality-f5-validation.mjs --check
node --test .github/scripts/test-scientific-data-quality-f5-validation.mjs
node --test .github/scripts/test-scientific-data-quality-projection.mjs .github/scripts/test-scientific-data-quality-consumer.mjs .github/scripts/test-scientific-data-quality-scoring.mjs .github/scripts/test-scientific-data-quality-contract.mjs
node --check docs/javascripts/scientific-data-quality-core.mjs
node --check docs/javascripts/scientific-data-quality.js
```

Risultato: verifier/freshness/idempotency PASS; 12/12 test F5 e 43/43 regressioni F2–F4 PASS; browser syntax e JSON syntax PASS. Il build MkDocs locale e una validazione JSON Schema mediante engine esterno non sono stati eseguiti nel runtime locale; il contratto persisted è verificato contro il builder e `Validate documentation` più `Developer Foundation` hanno eseguito con successo i gate repository/MkDocs in CI.

Eseguito su GitHub Actions sull'exact reviewed head `12abeaa3ac98ee4b23234e1f63e161ff003c84ac`: tutti i nove workflow applicabili riportati nella matrice sono `SUCCESS`.

Non eseguito perché non applicabile:

- OAT su EAGLE/N.I.N.A./ASCOM/PLC;
- device, telemetry producer o Safety validation;
- calibrazione scientifica produttiva.

Da eseguire post-merge: workflow applicabili, deployment Pages e riconciliazione della closure sul merge SHA.

## 7. Readiness recommendation

**READY FOR MERGE** per il solo incremento BKL-041 F5, senza waiver.

Il merge può pubblicare la validation completa e automatica e accettare la capability esclusivamente come sperimentale read-only con limitation. Non autorizza un profilo produttivo, threshold, ranking, automatic acceptance, recommendation, remediation, device command o Safety Authority.

La closure BKL-041 diventa effettiva solo dopo protected merge, workflow e Pages verdi sul merge commit. Soltanto allora la continuità può passare a **BKL-046 — AI Post-Processing Assistant for PixInsight**.
