# BKL-046 F5 — Real-Evidence Evaluation Plan

| Campo | Valore |
|---|---|
| Identificativo | BKL-046-F5-EVP-001 |
| Stato | Proposed / not executed |
| Versione | 0.1 |
| Data | 12/09/2026 |
| Architecture | `docs/architecture/scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md` |
| Baseline | `bc86264a4a689492087182e121820aa6cce06025` |

## 1. Purpose

Definire evidence, test e stop conditions per F5. Questo documento è un piano: nessun test F5, report, closure o outcome qui descritto è dichiarato eseguito.

## 2. Governed inputs

| Input | Authority | Uso consentito |
|---|---|---|
| `docs/data/scientific-session-catalog.json` | AP-014 projection governata | popolazione e identità sessione |
| `docs/data/ai-post-processing-advisory-projection.json` | BKL-046 F4 accepted projection | record, rule outcome, source state e digest |
| sidecar BKL-045 allowlisted | BKL-045 | exact correlation e execution evidence, se presente |
| Human Decision Receipt F2 | HUMAN_ONLY record separato | disposition, mai execution proof |
| BKL-041 quality report | experimental context only | limitation/bias context; vietato come ground truth |

## 3. Baseline known answer

| Misura descrittiva | Expected |
|---|---:|
| catalog sessions / F4 records | 15 / 15 |
| provenance matched / unavailable | 0 / 15 |
| uncorrelated sources | 2 |
| governance PASS | 15 |
| processing-history FAIL_CLOSED | 15 |
| validated / incomplete Recommendation | 15 / 15 |
| decision receipts | 0 |
| LDN 1320 / M 27 / UNKNOWN | 3 / 11 / 1 |

Il known answer deve produrre scientific effectiveness `NOT_EVALUABLE_CURRENT_EVIDENCE`, non `PASS`, `ZERO_DEFECTS` o una percentuale di successo.

## 4. Test matrix

| Test ID | Gate | Expected evidence | Failure behavior |
|---|---|---|---|
| F5-EVAL-001 | schema chiuso | report conforme, unknown property reject | hard fail |
| F5-EVAL-002 | full population | session set F5 = catalog session set | `COHORT_SESSION_SET_MISMATCH` |
| F5-EVAL-003 | baseline known answer | conteggi esatti della sezione 3 | drift fail |
| F5-EVAL-004 | empty matched cohort | eligible=0 e `NOT_EVALUABLE` | nessun ratio permissivo |
| F5-EVAL-005 | exact correlation | target/data/path similarity non ammesse | candidate reject/fail-closed |
| F5-EVAL-006 | deterministic identity | stesso input/versione -> stesso ID/digest | drift fail |
| F5-EVAL-007 | anti-tampering | catalog/F4/cohort/report digest verificati | hard fail |
| F5-EVAL-008 | no self-evidence | Recommendation e BKL-041 non sono ground truth | source reject |
| F5-EVAL-009 | decision separation | receipt non prova execution | semantic reject |
| F5-EVAL-010 | authority | apply/production/automatic acceptance false | authority drift reject |
| F5-EVAL-011 | first/retry workflow | generator/check/test in entrambi i path | verifier fail |
| F5-EVAL-012 | atomicity | report in `governed_paths` | merge gate fail |
| F5-EVAL-013 | stale projection | catalog o F4 più recenti del report | browser fail-closed |
| F5-EVAL-014 | accessibility | stato non solo colore, focus, live region | test fail |
| F5-EVAL-015 | privacy/security | no raw sidecar, local path, image, secret | test fail |
| F5-EVAL-016 | regression | F2 16/16, F3 21/21, F4 projection/consumer integralmente verdi | gate fail |

## 5. Decision matrix tests

| Scenario | Technical | Scientific | Closure |
|---|---|---|---|
| baseline reale e gate tecnici verdi | accepted with limitations | not evaluable | closure tecnica candidabile |
| cohort scientifica vuota | invariato | not evaluable | nessuna scientific claim |
| digest/freshness drift | not accepted | invalid | keep open |
| unknown authority/apply true | rejected | invalid | do not close |
| future exact match senza ground truth | accepted with limitations | not evaluable | nessuna effectiveness claim |
| future exact match con metodo approvato | separatamente valutabile | evaluation required | nuova review, mai auto-promozione |

## 6. Validation commands proposed

```text
node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs
node --test .github/scripts/test-ai-post-processing-advisory-f5-evaluation.mjs
node --test .github/scripts/test-ai-post-processing-advisory-contract.mjs
node --test .github/scripts/test-ai-post-processing-advisory-demonstrator.mjs
node --test .github/scripts/test-ai-post-processing-advisory-projection.mjs
node --test .github/scripts/test-ai-post-processing-assistant-consumer.mjs
mkdocs build --strict
```

I primi tre comandi sono pianificati e non esistono finché F5-A non li implementa. Gli altri sono regressioni esistenti da mantenere.

## 7. CI and review gates

1. local tests e generator `--check`;
2. exact-head CI sul technical head;
3. ARB con findings classificati e modalità di review dichiarata;
4. Release Quality con matrix, rischi e waiver espliciti;
5. final publication head CI;
6. merge protetto oppure nuova deroga owner-authorized limitata alla singola PR e all'expected head;
7. post-merge workflow e Pages verification;
8. closure record soltanto dopo evidence completa.

## 8. Stop conditions

F5 deve fermarsi senza closure se:

- una sessione canonica manca dal report;
- una cohort vuota è rappresentata come successo;
- un dato missing viene imputato o inferito;
- BKL-041, una Recommendation o una decisione umana viene usata come ground truth/esecuzione;
- l'authority abilita produzione, apply, automatic acceptance o command path;
- generator first/retry o atomicity non sono dimostrati;
- ARB/RQ, exact-head CI o post-merge evidence non sono completi.

## 9. Evidence record template

Ogni esecuzione F5 deve registrare exact SHA, input identity/digest, evaluation ID/digest, conteggi di tutte le cohort, reason code, test result, workflow run ID, reviewer mode, waiver e retained limitation. I campi non osservati restano `UNAVAILABLE` o `NOT_EXECUTED`.
