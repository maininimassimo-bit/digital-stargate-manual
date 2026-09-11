# RQ-BKL-041-F2 — Release Quality Review

| Campo | Valore |
|---|---|
| Review | RQ-BKL-041-F2 |
| Data | 11/09/2026 |
| Capability | BKL-041 — Scientific Data Quality Score |
| Increment | F2 — Machine-readable Quality Evidence and Profile Contract |
| PR | #160 |
| Proposal head | `537df59385359ef95382928fa436dc67e8fd24a0` |
| Reviewed head | `15d08fd1fb99e62851709e138c69a8162b759a75` |
| ARB | ARB-BKL-041-F2 — APPROVED 98/100 |
| Recommendation | READY FOR MERGE |

## 1. Release impact report

BKL-041 F2 introduce un contratto machine-readable repository-side per `QualityEvidence`, `AssessmentProfile` e `DimensionAssessment`, una fixture sintetica bounded, identity SHA-256 deterministica, validator fail-closed e CI dedicata.

Non introduce score, formula, peso numerico, normalization, confidence numerica, threshold, ranking, consumer, persistenza, migrazione dati o modifica della pipeline automatica di import.

| Area | Impatto |
|---|---|
| Architecture | nuovo solution contract BKL-041 F2; F1 riconciliato Accepted |
| Data contracts | nuovo schema additivo 1.0 e fixture sintetica |
| Application/Domain | validator repository-side puro; nessuna dipendenza runtime |
| Portal | nessun consumer F2; automatic refresh resta requisito F4 |
| CI/CD | nuovo gate `BKL-041 F2 Governance` |
| Roadmap/continuity | source canonica e projection governate allineate a F2 |
| Operations | nessuna azione PC/EAGLE |
| Safety | nessun cambiamento; interlock locali restano authority |

## 2. Quality-gate matrix

| Gate | Stato | Evidence |
|---|---|---|
| Scope / non-scope | Passed | score, pesi, normalizzazione, confidence numerica, consumer e runtime esplicitamente esclusi |
| F1 prerequisite | Passed | PR #159 merge `6d48318c460bad040fd0754b0300fbcd76a2d312`; status Accepted riconciliato |
| Architecture coherence | Passed | ARB-BKL-041-F2 APPROVED 98/100 |
| Schema/versioning | Passed | Draft 2020-12, schemaVersion 1.0, contract type e identity method chiusi |
| Deterministic identity | Passed | canonical JSON/SHA-256 e known-answer test |
| Fail-closed validation | Passed | 12 test positivi/negativi; unknown property e tampering inclusi |
| Missing-data semantics | Passed | required missing esplicito `UNAVAILABLE`; no zero/imputation |
| Scientific integrity | Passed | unità SQM/guiding, FWHM calibration, PixInsight completeness ed evidence class validate |
| Authority / Safety | Passed | read-only, no acceptance/action authority, local interlocks invariati |
| Security / privacy | Passed | fixture sintetica; source locator repository-relative; nessun secret/path locale |
| Migration / compatibility | Passed | additivo, nessuna modifica a contratti o consumer esistenti |
| Rollback | Passed | revert repository-only; nessuna rollback action runtime |
| BKL-041 F2 Governance | Passed | #5, run `34567275386` |
| Developer Foundation | Passed | #1284, run `34567275379` |
| Scientific Platform Governance | Passed | #39, run `34567275368` |
| Validate documentation | Passed | #917, run `34567275376` |
| Genera manuale Word | Passed | #1342, run `34567275381` |
| Runtime/OAT | Not Applicable | nessun runtime/consumer introdotto |
| Pages deployment | Not Applicable pre-merge | nessun consumer portale modificato |

## 3. Definition of Done assessment

| Criterio | Stato |
|---|---|
| scope, dipendenze e boundary chiari | Passed |
| schema, fixture e versioning presenti | Passed |
| identity deterministica eseguibile | Passed |
| errori scientifici critici fail-closed | Passed |
| score/pesi/contribution vietati in F2 | Passed |
| authority e Safety preservate | Passed |
| continuity e roadmap sincronizzate | Passed |
| ARB senza Blocker/Major | Passed |
| CI exact-head applicabile verde | Passed |
| runtime/production claim senza evidence | assente |

## 4. Risk register

| ID | Rischio | Probabilità | Impatto | Trattamento | Stato |
|---|---|---|---|---|---|
| RQ41F2-R01 | schema e validator divergono in evoluzioni future | Media | Alto | exact allow-list, schema version e parity test obbligatori a ogni modifica | Controlled |
| RQ41F2-R02 | fixture interpretata come production evidence | Bassa | Alto | `BOUNDED_SYNTHETIC_FIXTURE`, session ID sintetico e limitation esplicite | Controlled |
| RQ41F2-R03 | missing evidence diventa zero o score implicito | Bassa | Alto | required missing `UNAVAILABLE`; score/peso/contribution proibiti | Controlled |
| RQ41F2-R04 | FWHM/PixInsight incompleti promossi a eligible | Bassa | Alto | calibration/completeness gate e test negativi | Controlled |
| RQ41F2-R05 | regressione dell'aggiornamento automatico futuro | Bassa | Alto | acceptance condition F4 con session-driven/idempotency/stale tests | Deferred with gate |

## 5. Waiver register

Nessun waiver richiesto.

Le observation ARB su F3/F4 sono future entry conditions e non deviazioni F2:

1. weight-set e scale semantics;
2. schema/validator parity sulle evoluzioni;
3. automatic session refresh F4;
4. navigation quando esisterà un consumer stabile.

## 6. Validation commands and evidence

Eseguito localmente:

```text
node .github/scripts/verify-scientific-data-quality-contract.mjs
node --test .github/scripts/test-scientific-data-quality-contract.mjs
node --check <tre moduli BKL-041 F2>
python -m json.tool <schema e fixture>
yaml.safe_load(<workflow>)
```

Risultato: verifier PASS, 12/12 test PASS, syntax PASS.

Eseguito su GitHub Actions sull'exact reviewed head `15d08fd1fb99e62851709e138c69a8162b759a75`:

- BKL-041 F2 Governance #5 — SUCCESS;
- Developer Foundation #1284 — SUCCESS;
- Scientific Platform Governance #39 — SUCCESS;
- Validate documentation #917 — SUCCESS;
- Genera manuale Word #1342 — SUCCESS.

Non eseguito perché non applicabile a F2:

- runtime/OAT su EAGLE;
- device, telemetry producer o Safety validation;
- scoring-engine known-answer/sensitivity tests;
- session-driven projection e browser consumer tests.

Gli ultimi due gruppi diventano obbligatori rispettivamente in F3 e F4.

## 7. Readiness recommendation

**READY FOR MERGE** per il solo incremento BKL-041 F2.

Il merge può accettare schema, fixture, identity e validation contract. Non autorizza F3/F4, score operativo, peso numerico, ranking, threshold, automatic acceptance, remediation, device command o Safety Authority.

Il prossimo incremento dependency-ordered è **BKL-041 F3 — Deterministic Scoring and Confidence Engine**, soggetto a nuova definizione/review di profilo, normalizzazione, weight set, scale, confidence, decomposition e bias/sensitivity evidence.

