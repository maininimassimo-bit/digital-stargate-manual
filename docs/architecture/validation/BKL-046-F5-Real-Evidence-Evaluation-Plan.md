# BKL-046 F5 — Real-Evidence Evaluation Plan

| Campo | Valore |
|---|---|
| Identificativo | BKL-046-F5-EVP-001 |
| Stato | F5-A accepted/post-merge verified; F5-B implementation candidate; F5-C not executed |
| Versione | 0.4 |
| Data | 12/09/2026 |
| Architecture | `docs/architecture/scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md` |
| Baseline | F5-A merge `46b956f0a6ceb04442ffd80447f810ef6463b5a8` |

## 1. Purpose

Definire evidence, test e stop conditions per F5. La slice F5-A è accepted e post-merge verified. F5-B implementa come candidato dynamic update, atomicity, browser freshness e accessibility; exact-head CI e ARB/RQ F5-B restano obbligatori prima dell'acceptance. F5-C closure non è eseguita.

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
| F5-EVAL-016 | regression | F2, F3 e F4 projection/consumer integralmente verdi | gate fail |

## 5. Decision matrix tests

| Scenario | Technical | Scientific | Closure |
|---|---|---|---|
| baseline reale e gate tecnici verdi | accepted with limitations | not evaluable | closure tecnica candidabile |
| cohort scientifica vuota | invariato | not evaluable | nessuna scientific claim |
| digest/freshness drift | not accepted | invalid | keep open |
| unknown authority/apply true | rejected | invalid | do not close |
| future exact match senza ground truth | accepted with limitations | not evaluable | nessuna effectiveness claim |
| future exact match con metodo approvato | separatamente valutabile | evaluation required | nuova review, mai auto-promozione |

### 5.1 F5-A accepted evidence

La suite F5-A implementata contiene 25 test e ha prodotto 25 PASS / 0 FAIL sul remediation head. Copre schema-shaped closed contract, popolazione completa, known answer, empty cohort, allowlist/traversal, determinism, tamper e catalog drift, authority, receipt orfane/duplicate, execution correlation/ordering, source BKL-045 esatta, registry/reason-code rejection, public-report tamper, closure escalation, directory assenti, unknown/non-file entries, full F2 receipt bounds, source-set metadata pinning e canonical F4 validation. La regressione F2 contiene 17 test con 17 PASS / 0 FAIL.

Il report persistito `BKL046-F5A-F4FEB5E207DD3F7D3E4F6C87` ha digest `174f8d75a27160b476c65d2670c50e4089811834dd1e5867418c77dfbac41f70` e conserva il known answer: 15 sessioni, 0 provenance eligible, 0 Human Decision Receipt, 0 execution evidence, 2 source processing non correlate. Gli esiti restano `READY_FOR_F5_EVALUATION`, `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION`, `KEEP_OPEN` e `aiModelImplemented=false`.

F5-A è stata accettata tramite PR #178, authorized head `74603bedad088dcf9f2cb33b9769658f4a9e639a` e merge `46b956f0a6ceb04442ffd80447f810ef6463b5a8`, con ARB R2 98/100, Release Quality `CONDITIONALLY READY FOR MERGE` e 9/9 workflow post-merge verdi. Le review sono AI-assistite e non equivalenti ad approvazioni umane indipendenti; la deroga `W-BKL046-F5A-MERGE-001` è consumata/scaduta.

### 5.2 F5-B candidate evidence

Il candidato copre `F5-EVAL-011`–`014`: generator/check/verifier F5 nei path first e retry dopo F4; report F5 nel medesimo `governed_paths`; browser con fetch `no-store` dei tre snapshot e verifica catalog/F4/F5; stato `EVALUATION UNAVAILABLE · FAIL-CLOSED`; outcome e limitation non basati solo sul colore; focus, live region e responsive layout. La verifica locale conta 28/28 test evaluator/workflow e 16/16 test consumer; sul technical head `f6555e80760f9c5d179df3dc0ee4e02c7e265a21` sono verdi 10/10 workflow. Il record è `BKL-046-F5B-Atomic-Update-and-Consumer-Evidence-2026-09-12.md`; publication-head CI e review F5-B sono pending.

## 6. Validation commands

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

I comandi F5 e consumer sono verdi localmente sul candidato F5-B. La validazione completa, l'exact-head CI e la nuova ARB/RQ saranno registrate nel record F5-B; nessuna review o acceptance F5-B è ancora eseguita.

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
