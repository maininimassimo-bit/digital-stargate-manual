# ARB BKL-046 F5-A — AI-Assisted Implementation Re-Review

| Campo | Valore |
|---|---|
| Review ID | ARB-BKL-046-F5A-AI-ASSISTED-R2 |
| Package | BKL-046 F5-A — Evaluation Foundation remediation |
| Review date | 12/09/2026 |
| Pull request | #178 |
| Reviewed head | `5d583ce326af2ed20398f58e7629260f80fe73d6` |
| Technical remediation head | `df1fd85ea2bf2e058bcbca17ca5ace704acbab8a` |
| Base | `main` @ `16e0f101fda50e375bff6d5e9c8ec90d2083bc12` |
| Review mode | AI-assisted governance re-review; not an independent human review |
| Owner authorization | Granted 12/09/2026 for PR #178 re-review publication only |
| Review-independence waiver | `W-BKL046-F5A-REREVIEW-001` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **98/100** |

## 1. Scope and independence disclosure

La re-review verifica esclusivamente la remediation dei finding `ARB-F5A-M01`, `ARB-F5A-M02` e `ARB-F5A-C01` e conferma che il restante package F5-A non abbia subito modifiche materiali incompatibili con la prima review.

La valutazione è AI-assistita, autorizzata dal repository owner e **non equivale a un'approvazione umana indipendente**. Lo stesso ambiente AI ha assistito anche la remediation. La separazione del ruolo reviewer impedisce silent repair durante questa valutazione, ma non crea indipendenza umana o organizzativa.

La nuova deroga una tantum `W-BKL046-F5A-REREVIEW-001` copre il reviewed head indicato e il solo descendant non materiale necessario a pubblicare queste review e la relativa navigazione. Non riusa `W-BKL046-F5A-REVIEW-001`, non autorizza il merge e non deroga a CI o branch protection.

## 2. Repository evidence verified

- PR #178 aperta, non draft, mergeable e clean, con 4 commit, 19 file modificati, 2.943 additions e 37 deletions.
- Head remoto `5d583ce326af2ed20398f58e7629260f80fe73d6`; `main` resta `16e0f101fda50e375bff6d5e9c8ec90d2083bc12`.
- Il remediation delta rispetto al review-publication head `d83675a3307d6bb8275acfbcc2b5b617cc8b404d` contiene due commit e 13 file; le modifiche di codice sono limitate a validatori, test, verifier e workflow.
- I blob dei sette file critici ispezionati localmente coincidono con i blob GitHub del reviewed head.
- Otto workflow pull-request sul reviewed head sono conclusi con successo: F5 `34682979331`, F2 `34682979526`, F3 `34682979300`, F4 `34682979389`, BKL-041 F4 `34682979376`, documentation `34682979434`, Developer Foundation `34682979319` e Word `34682979378`.
- I log F5 registrano 25/25 test F5-A, 17/17 test F2, generator/verifier verdi e regressioni F3/F4/consumer senza failure.
- Il report known-answer rimane invariato: 15 sessioni, 0 provenance eligible, 0 Human Decision Receipt, 0 execution evidence, scientific `NOT_EVALUABLE_CURRENT_EVIDENCE`, production `NOT_READY_FOR_PRODUCTION`, closure `KEEP_OPEN` e `aiModelImplemented=false`.
- `main.protected=false`, repository ruleset assenti, nessuna autorizzazione al merge e nessuna review GitHub formale preesistente.

## 3. Re-review scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Program and dependency alignment | 100 | F5-A resta conforme al design F5 integrato; F5-B/F5-C non vengono promosse |
| Domain and layer integrity | 98 | F5 riusa i validatori canonici F2/F4 e mantiene separati policy, generator, projection e verifier |
| Source authority and provenance | 98 | allowlist, raw validation, exact correlation e sanitizzazione sono chiuse e testate |
| Contract and schema/runtime congruence | 96 | validator F2 canonico riusato; verifier lega i limiti runtime allo schema e verifica il `$ref` F5→F2 |
| Determinism and identity | 98 | canonical JSON SHA-256, stable identity, digest e rebuild comparison verificati |
| Scientific evidence integrity | 100 | assenza di evidenza e ground truth non viene convertita in efficacia |
| Security and privacy | 97 | input bounded e projection pubblica sanitizzata; nessun secret o dato operativo introdotto |
| Safety and authority | 100 | read-only, human-only, nessun apply/command; Safety Authority resta agli interlock fisici locali |
| Operability and observability | 96 | failure esplicite, reason code, count, digest e workflow dedicato disponibili |
| Migration and rollback | 98 | incremento additivo; nessuna mutation dei contratti F1-F4 persistiti |
| Traceability and documentation | 98 | review R1, remediation evidence, plan, backlog, bootstrap e navigation sono correlati |
| Test and CI evidence | 98 | 25 F5-A + 17 F2 e 8 workflow verdi includono i tre probe di remediation |

## 4. Finding disposition

| Finding R1 | Evidence verificata | Disposition R2 |
|---|---|---|
| `ARB-F5A-M01` — raw Human Decision validator più debole di F2 | `validateHumanDecisionReceipt()` e `validateStableId()` canonici riusati; F5A-UT-024 e test F2 coprono stable ID, shape, edit count e bound | **Closed** |
| `ARB-F5A-M02` — source-set metadata non canonici accettati | `validateSourceSet()` richiede equality di directory e regex; F5A-UT-025 usa digest ricalcolato | **Closed** |
| `ARB-F5A-C01` — trust chain F4 parziale e duplicata | F5 invoca `validateAdvisoryProjection()` canonico; F5A-UT-023 altera stato e digest e osserva fail-closed | **Closed** |

### Nuovi finding

- Blocker: nessuno.
- Major: nessuno.
- Minor: nessuno.

## 5. Architecture assessment

Il boundary F5 ammette le future Human Decision source solo dopo il controllo completo del receipt F2, incluso digest, shape, stable ID, timestamp, disposition, edit e authority. La correlazione con la recommendation F4 effettiva viene poi verificata nel build path prima della sanitizzazione.

Il report esportato non può più accettare metadata arbitrari per i due source-set anche quando l'attaccante ricalcola l'`evaluationDigest`. Analogamente, una projection F4 con soli digest ricalcolati non supera più il boundary F5 perché viene validata integralmente dal validator F4 canonico.

Non risultano dipendenze inverse, mutation path, canali di esecuzione o cambi alla Safety Authority. L'assenza di un motore JSON Schema Draft 2020-12 nel workflow è compensata dal validator runtime canonico e dal binding verifier schema/runtime; non costituisce un finding per il contratto corrente.

## 6. Decision

**APPROVED WITH CONDITIONS.**

Le remediation dei due Major e del Minor della R1 sono adeguate e i finding sono chiusi sul reviewed head. F5-A può avanzare al gate di merge come evaluation-foundation implementation, alle seguenti condizioni:

1. il commit che pubblica questa re-review deve contenere soltanto review e navigazione non materiali e ottenere CI verde sul proprio exact head;
2. qualsiasi modifica materiale successiva a validator, schema, registry, cohort, authority, decision table o Safety boundary invalida questa decisione e richiede nuova review;
3. il merge richiede autorizzazione owner separata e disposizione esplicita per l'assenza di branch protection;
4. F5-B/F5-C restano `NOT_EXECUTED` e non sono autorizzate da questa decisione;
5. scientific effectiveness resta `NOT_EVALUABLE_CURRENT_EVIDENCE`, production resta `NOT_READY_FOR_PRODUCTION`, closure resta `KEEP_OPEN` e nessun AI model è implementato.

## 7. Validation evidence

| Verifica | Risultato |
|---|---|
| Blob parity GitHub/local sui file critici | PASS |
| F5-A local re-execution | 25/25 PASS |
| F2 local re-execution | 17/17 PASS |
| Persisted F5 generator `--check` | PASS |
| F5 deterministic verifier | PASS |
| F5A-UT-023 F4 internal drift | FAIL_CLOSED as expected |
| F5A-UT-024 F2 receipt violations | FAIL_CLOSED as expected |
| F5A-UT-025 source-set metadata drift | FAIL_CLOSED as expected |
| Full exact-head GitHub CI | 8/8 SUCCESS |

La copia locale di review è un sottoinsieme e non contiene gli script F3/F4/consumer non modificati; tali regressioni sono state quindi verificate nei log della CI GitHub exact-head, non dichiarate come eseguite localmente.

## 8. Traceability

- [ARB F5-A R1](ARB-BKL-046-F5A-AI-Assisted-Implementation-Review-2026-09-12.md)
- [RQ F5-A R1](RQ-BKL-046-F5A-AI-Assisted-Release-Quality-Review-2026-09-12.md)
- [F5-A remediation evidence](../validation/BKL-046-F5A-Validation-Remediation-Evidence-2026-09-12.md)
- [F5 validation plan](../validation/BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
- [F5 architecture](../scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md)
- [PR #178](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/178)
