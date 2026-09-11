# RQ-BKL-041-F3 — Release Quality Review

| Campo | Valore |
|---|---|
| Review | RQ-BKL-041-F3 |
| Data | 11/09/2026 |
| Capability | BKL-041 — Scientific Data Quality Score |
| Increment | F3 — Deterministic Scoring and Confidence Engine |
| PR | #161 |
| Proposal head | `98acd8a5c1a3d2b318c4fcf2eec6bb35db7202de` |
| Reviewed head | `20edbd24de882727ce0e4547b265051b608332d5` |
| ARB | ARB-BKL-041-F3 — APPROVED 98/100 |
| Recommendation | READY FOR MERGE |

## 1. Release impact report

BKL-041 F3 introduce un motore repository-side puro per normalizzazione, score, evidence-support confidence e decomposition. Profilo, algoritmo, scale, bounds, pesi, fattori e identity sono versionati. Il known answer è bounded e interamente sintetico.

Non introduce profilo o dati produttivi, threshold, classi GOOD/BAD, ranking, recommendation, automatic acceptance, portal consumer, persistenza, migrazione dati, integrazione nella pipeline di import, remediation, device command o Safety Authority.

| Area | Impatto |
|---|---|
| Architecture | nuovo solution increment BKL-041 F3; F2 riconciliato Accepted |
| Data contracts | schema 1.0 e fixture known-answer sintetica additivi |
| Application/Domain | funzione pura deterministica con output immutabile e decomposition |
| Scientific semantics | profilo dimostrativo; nessuna claim di calibrazione produttiva |
| Portal | nessun consumer F3; automatic refresh resta requisito obbligatorio F4 |
| CI/CD | nuovo gate `BKL-041 F3 Governance`; regressione F2 preservata |
| Roadmap/continuity | source canonica e projection generate allineate a F3 |
| Operations | nessuna azione PC/EAGLE o modifica della pipeline sessione |
| Safety | nessun cambiamento; interlock locali restano authority |

## 2. Quality-gate matrix

| Gate | Stato | Evidence |
|---|---|---|
| Scope / non-scope | Passed | produzione, consumer, threshold, ranking, acceptance e runtime esplicitamente esclusi |
| F2 prerequisite | Passed | PR #160 merge `4ca5135043c508288fa2ba41b744f29b3b9032ed`; stato Accepted riconciliato |
| Architecture coherence | Passed | ARB-BKL-041-F3 APPROVED 98/100 |
| Profile/algorithm versioning | Passed | id e versioni esatti; profili alternativi rejected anche se risigillati |
| Weight and scale integrity | Passed | required positive/sum 1; optional/context zero; scale 0–100; rounding esplicito |
| Deterministic identity | Passed | canonical JSON, profile/snapshot/assessment/fixture digest e order-invariance |
| Known answer | Passed | score 77,86; confidence 74; coverage 0,925 |
| Sensitivity / bias boundary | Passed | 4 dimensioni required, optional zero-weight e score/confidence separation testati |
| Fail-closed validation | Passed | range, unità, missing, evidence class, authority, unknown field e tampering coperti |
| Missing-data semantics | Passed | required missing produce unavailable/null senza imputazione o reweighting |
| Explainability | Passed | decomposition, exclusions, refs, factors e limitations materializzati |
| Authority / Safety | Passed | read-only, no acceptance/action authority, local interlocks invariati |
| Security / privacy | Passed | fixture e refs sintetici; nessun secret, path locale o session data produttivo |
| Migration / compatibility | Passed | additivo, F2 invariato salvo lifecycle, nessun consumer o storage esistente |
| Rollback | Passed | revert repository-only; nessuna rollback action runtime |
| BKL-041 F3 Governance | Passed | #3, run `34576805176` |
| BKL-041 F2 Governance | Passed | #10, run `34576805234` |
| Developer Foundation | Passed | #1289, run `34576805233` |
| Scientific Platform Governance | Passed | #44, run `34576805207` |
| Validate documentation | Passed | #922, run `34576805190` |
| Genera manuale Word | Passed | #1347, run `34576805215` |
| Runtime/OAT | Not Applicable | nessun runtime/consumer F3 |
| Pages deployment | Not Applicable pre-merge | nessuna superficie portale modificata |

## 3. Definition of Done assessment

| Criterio | Stato |
|---|---|
| scope, dipendenze e boundary chiari | Passed |
| formula, profile, weights, scale e confidence versionati | Passed |
| identity e known answer riproducibili | Passed |
| decomposition ed exclusions verificabili | Passed |
| sensitivity e failure behavior coperti | Passed |
| profilo esclusivamente sintetico fail-closed | Passed |
| authority e Safety preservate | Passed |
| continuity e roadmap sincronizzate automaticamente | Passed |
| ARB senza Blocker/Major/Minor aperti | Passed |
| CI exact-head applicabile verde | Passed |
| runtime/production claim senza evidence | assente |

## 4. Risk register

| ID | Rischio | Probabilità | Impatto | Trattamento | Stato |
|---|---|---|---|---|---|
| RQ41F3-R01 | parametri sintetici interpretati come calibrazione produttiva | Bassa | Alto | id/state/limitations dedicati, profile allow-list e nessun consumer | Controlled |
| RQ41F3-R02 | weight set introduce bias target/filtro/setup | Media | Alto | sensitivity F3; nuovo profilo/cohort/calibration e ARB obbligatori prima della produzione | Deferred with gate |
| RQ41F3-R03 | confidence interpretata come probabilità | Bassa | Alto | semantic machine-readable, formula separata e presentation gate F4 | Controlled |
| RQ41F3-R04 | missing evidence produce score fuorviante | Bassa | Alto | assessment unavailable, valori null, reason esplicita e no reweight | Controlled |
| RQ41F3-R05 | schema e validator divergono | Media | Medio | exact allow-list, versioni chiuse, negative tests e parity obbligatoria sulle evoluzioni | Controlled |
| RQ41F3-R06 | consumer mostra score stale dopo nuova importazione | Media | Alto | F4 bloccato su session-driven automatic refresh, stale/failure e E2E evidence | Deferred with gate |

## 5. Waiver register

Nessun waiver richiesto.

Le observation ARB sono future entry conditions, non deviazioni F3:

1. calibrazione produttiva con nuovo profilo e cohort evidence;
2. schema/validator parity a ogni evoluzione;
3. automatic session refresh e stale behavior in F4;
4. presentation con score, confidence, coverage, version, decomposition ed exclusions insieme.

## 6. Validation commands and evidence

Eseguito localmente:

```text
node .github/scripts/verify-scientific-data-quality-scoring.mjs
node --test .github/scripts/test-scientific-data-quality-scoring.mjs
node .github/scripts/verify-scientific-data-quality-contract.mjs
node --test .github/scripts/test-scientific-data-quality-contract.mjs
```

Risultato: F3 verifier PASS, 19/19 test F3 PASS, F2 verifier PASS, 12/12 test F2 PASS.

Eseguito su GitHub Actions sull'exact reviewed head `20edbd24de882727ce0e4547b265051b608332d5`:

- BKL-041 F3 Governance #3 — SUCCESS;
- BKL-041 F2 Governance #10 — SUCCESS;
- Developer Foundation #1289 — SUCCESS;
- Scientific Platform Governance #44 — SUCCESS;
- Validate documentation #922 — SUCCESS;
- Genera manuale Word #1347 — SUCCESS.

Non eseguito perché non applicabile a F3:

- runtime/OAT su EAGLE;
- device, telemetry producer o Safety validation;
- profilo/calibrazione su sessioni scientifiche produttive;
- session-driven assessment projection e browser consumer tests;
- Pages deployment pre-merge.

Gli ultimi due gruppi diventano obbligatori prima di qualsiasi uso produttivo e in F4.

## 7. Readiness recommendation

**READY FOR MERGE** per il solo incremento BKL-041 F3.

Il merge può accettare il motore deterministico, il profilo dimostrativo sintetico, known answer, decomposition, sensitivity evidence e governance. Non autorizza un profilo produttivo, threshold, ranking, classi qualitative, automatic acceptance, recommendation, portal consumer, remediation, device command o Safety Authority.

Il prossimo incremento dependency-ordered è **BKL-041 F4 — Session-driven Projection and Portal Consumer**, che deve dimostrare la rigenerazione automatica dopo ogni nuova sessione scientifica importata, idempotenza, profile-version recompute, atomic publication, stale/failure behavior e presentazione non fuorviante.
