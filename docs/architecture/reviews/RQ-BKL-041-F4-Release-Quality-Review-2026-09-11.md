# RQ-BKL-041-F4 — Release Quality Review

| Campo | Valore |
|---|---|
| Review | RQ-BKL-041-F4 |
| Data | 11/09/2026 |
| Capability | BKL-041 — Scientific Data Quality Score |
| Increment | F4 — Session-Driven Projection and Portal Consumer |
| PR | #162 |
| Proposal head | `ce896b114e5152cf4554c3d570cff6648d96c962` |
| Reviewed head | `a4ac9c3a255729b5783859728e61e69eb5f57ca4` |
| ARB | ARB-BKL-041-F4 — APPROVED 98/100 |
| Recommendation | READY FOR MERGE |

## 1. Release impact report

BKL-041 F4 aggiunge una projection deterministica full-catalog, la integra nella pipeline automatica di import e pubblica un consumer moderno read-only. Catalogo e projection sono aggiornati nello stesso commit governato; il browser verifica freshness, identity e authority prima del rendering.

Il profilo resta il dimostratore sintetico F3 e ogni output è `EXPERIMENTAL_NOT_ACCEPTED`. La release non introduce calibrazione produttiva, ranking, threshold, classi GOOD/BAD, recommendation, automatic acceptance, remediation, device command o Safety Authority.

| Area | Impatto |
|---|---|
| Architecture | nuovo solution increment F4; F3 riconciliato Accepted |
| Data contract | schema/projection F4 1.0 additivi, catalogo invariato |
| Pipeline | generazione/check/test nel workflow canonico e nel suo retry atomico |
| Portal | nuova pagina navigabile con verifica freshness client-side |
| Scientific semantics | evidence catalog-driven `DECLARED`; profilo sintetico non produttivo |
| CI/CD | nuovo gate F4 e regressioni F3/F2 preservate |
| Roadmap/continuity | source canonica, projection generate e documenti di ingresso allineati a F4 |
| Operations | nessuna modifica al runtime osservativo; deploy Pages dopo merge |
| Safety | nessun cambiamento; interlock locali restano authority |

## 2. Quality-gate matrix

| Gate | Stato | Evidence |
|---|---|---|
| Scope / non-scope | Passed | produzione, ranking, threshold, acceptance e command path esclusi |
| F3 prerequisite | Passed | PR #161 merge `89d8979fa4e5b151d85ef889efe03ad468efcad1`; lifecycle Accepted |
| Architecture coherence | Passed | ARB-BKL-041-F4 APPROVED 98/100, nessun finding aperto |
| Source/projection separation | Passed | catalogo authority; projection esplicitamente read model |
| Deterministic generation | Passed | ordinamento, canonical digest, semantic idempotency e full rebuild |
| Automatic refresh | Passed | trigger import, generator e governed path nello stesso ciclo atomico/retry |
| Freshness fail-closed | Passed | digest/catalog identity/session set e projection digest verificati |
| Missing/invalid semantics | Passed | unavailable/null e invalid isolati; nessuna imputazione o reweight |
| Explainability e UX | Passed | score, confidence, coverage, decomposition, exclusions e limitation insieme |
| Accessibility/responsiveness | Passed | semantic sections, live status, labels, responsive layout; strict docs build verde |
| Authority / Safety | Passed | read-only, production/acceptance false, action none, interlock locali |
| Security / privacy | Passed | nessun secret, local path o API mutativa; soli dati catalogo già pubblici |
| Observability | Passed | workflow failure + stato consumer non disponibile senza stale fallback |
| Migration / compatibility | Passed | additivo; F2/F3 e consumer esistenti invariati |
| Rollback | Passed | revert repository-only; nessuna azione runtime |
| BKL-041 F4 Governance | Passed | #2, run `34589069937` |
| BKL-041 F3 Governance | Passed | #7, run `34589069941` |
| Developer Foundation | Passed | #1293, run `34589069965` |
| Scientific Platform Governance | Passed | #48, run `34589069983` |
| Validate documentation | Passed | #926, run `34589070050` |
| Genera manuale Word | Passed | #1351, run `34589069998` |
| Analytics Center consistency | Passed | #30, run `34589070191` |
| Session Comparison projection | Passed | #14, run `34589070016` |
| BKL-039 F5 regression | Passed | #49, run `34589070005` |
| Pages deployment | Not Executed pre-merge | obbligatoria verifica sul merge commit |
| Runtime/device/Safety OAT | Not Applicable | nessun componente osservativo o command path modificato |

## 3. Definition of Done assessment

| Criterio | Stato |
|---|---|
| projection full-catalog deterministica e versionata | Passed |
| automatic refresh dopo ogni import completato | Passed |
| pubblicazione atomica con il catalogo | Passed |
| stale/tamper/authority failure fail-closed | Passed |
| presentation semantics complete e non fuorvianti | Passed |
| profilo/output sperimentali e non produttivi | Passed |
| test F4 e regressioni F3/F2 | Passed |
| nav, architecture e continuity coerenti | Passed |
| ARB senza Blocker/Major/Minor aperti | Passed |
| CI exact-head applicabile verde | Passed |
| Pages post-merge | Deferred to post-merge verification |

## 4. Risk register

| ID | Rischio | Probabilità | Impatto | Trattamento | Stato |
|---|---|---|---|---|---|
| RQ41F4-R01 | projection stale dopo una nuova importazione | Bassa | Alto | commit atomico, catalog digest/session set e browser reject | Controlled |
| RQ41F4-R02 | score sintetico interpretato come produttivo | Bassa | Alto | lifecycle, notice, limitations e `productionUseAuthorized=false` | Controlled |
| RQ41F4-R03 | record invalid interpretato come qualità negativa | Bassa | Alto | stato/errore espliciti e nessuna classe GOOD/BAD | Controlled |
| RQ41F4-R04 | confidence interpretata come probabilità | Bassa | Alto | label evidence support, coverage e decomposition co-presenti | Controlled |
| RQ41F4-R05 | coverage guiding sovrastimata | Bassa | Medio | coverage zero finché manca un denominatore governato | Controlled |
| RQ41F4-R06 | failure di generazione produce set parziale | Bassa | Alto | generator prima del commit; retry full regeneration; deploy solo dopo push | Controlled |
| RQ41F4-R07 | calibrazione futura introduce bias | Media | Alto | F5 con cohort, nuovo profilo/versione, evidence e nuova ARB/RQ | Deferred with gate |

## 5. Waiver register

Nessun waiver richiesto.

Le observation ARB sono entry condition future o verifica post-merge: cohort/calibrazione F5, eventuale estensione della coverage guiding, telemetry dedicata solo per un futuro servizio con SLO e controllo Pages sul merge SHA.

## 6. Validation commands and evidence

Eseguito localmente:

```text
node .github/scripts/verify-scientific-data-quality-projection.mjs
node .github/scripts/generate-scientific-data-quality-projection.mjs --check
node --test .github/scripts/test-scientific-data-quality-projection.mjs .github/scripts/test-scientific-data-quality-consumer.mjs
node --test .github/scripts/test-scientific-data-quality-scoring.mjs
node --test .github/scripts/test-scientific-data-quality-contract.mjs
node --check docs/javascripts/scientific-data-quality-core.mjs
node --check docs/javascripts/scientific-data-quality.js
node --check docs/javascripts/page-enhancements.js
```

Risultato: verifier/freshness/idempotency PASS; 12/12 test F4, 19/19 F3 e 12/12 F2 PASS; browser syntax PASS. Il build MkDocs locale non è stato eseguito perché il modulo non è installato nel runtime; `Validate documentation #926` e il `Verify MkDocs` del Developer Foundation #1293 lo hanno eseguito con successo in CI.

Eseguito su GitHub Actions sull'exact reviewed head `a4ac9c3a255729b5783859728e61e69eb5f57ca4`: tutti i nove workflow applicabili riportati nella matrice sono `SUCCESS`.

Non eseguito perché non applicabile:

- OAT su EAGLE/N.I.N.A./ASCOM/PLC;
- device, telemetry producer o Safety validation;
- calibrazione scientifica produttiva F5.

Da eseguire post-merge: deployment Pages e verifica dei workflow applicabili sul merge commit.

## 7. Readiness recommendation

**READY FOR MERGE** per il solo incremento BKL-041 F4, senza waiver.

Il merge può pubblicare la projection session-driven, l'integrazione atomica nella pipeline e il consumer read-only con freshness fail-closed. Non autorizza uso produttivo dello score, threshold, ranking, automatic acceptance, recommendation, remediation, device command o Safety Authority.

Il prossimo incremento dependency-ordered è **BKL-041 F5 — Real-Evidence Validation and Capability Closure**. F5 deve validare cohort rappresentative, calibrazione e bias con un nuovo profilo/versione prima di qualunque claim produttiva e deve completare closure, release evidence e post-merge verification.
