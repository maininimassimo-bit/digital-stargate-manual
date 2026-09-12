# RQ BKL-046 F5-A — AI-Assisted Release Quality Re-Review

| Campo | Valore |
|---|---|
| Review ID | RQ-BKL-046-F5A-AI-ASSISTED-R2 |
| Package | BKL-046 F5-A — Evaluation Foundation remediation |
| Pull request | #178 |
| Reviewed head | `5d583ce326af2ed20398f58e7629260f80fe73d6` |
| Technical remediation head | `df1fd85ea2bf2e058bcbca17ca5ace704acbab8a` |
| Base | `main` @ `16e0f101fda50e375bff6d5e9c8ec90d2083bc12` |
| Review date | 12/09/2026 |
| Review mode | AI-assisted release-quality re-review; not an independent human approval |
| Owner authorization | Granted 12/09/2026 for PR #178 re-review publication only |
| Review-independence waiver | `W-BKL046-F5A-REREVIEW-001` |
| ARB decision | **APPROVED WITH CONDITIONS — 98/100** |
| Recommendation | **CONDITIONALLY READY FOR MERGE** |

## 1. Release impact report

La remediation rafforza i boundary esistenti senza modificare il known-answer report o ampliare lo scope funzionale. Il runtime F2 espone limiti riusabili; F5 riusa il validator F2 per i receipt e il validator F4 per la projection; source directory e path pattern sono fissati al contratto canonico. Test e verifier proteggono i tre finding R1 dalla regressione.

Non sono introdotti consumer, workflow automatici, AI model/provider, image transfer, PixInsight apply, device command o production authority. Non è richiesto un semantic version bump né una release note applicativa per questa slice documentale/tooling.

## 2. Verified evidence

| Evidence | Result |
|---|---|
| PR state | open, non-draft, mergeable, clean |
| PR scope | 4 commit; 19 file; 2.943 additions; 37 deletions |
| Reviewed head | `5d583ce326af2ed20398f58e7629260f80fe73d6` |
| Merge base | `16e0f101fda50e375bff6d5e9c8ec90d2083bc12`; branch 0 behind |
| F5-A tests | PASS — 25/25 |
| F2 tests | PASS — 17/17 |
| F5 persisted check/verifier | PASS |
| F5 governance | SUCCESS — `34682979331` |
| F2 governance | SUCCESS — `34682979526` |
| F3 governance | SUCCESS — `34682979300` |
| F4 governance | SUCCESS — `34682979389` |
| BKL-041 F4 Governance | SUCCESS — `34682979376` |
| Validate documentation | SUCCESS — `34682979434` |
| Developer Foundation | SUCCESS — `34682979319` |
| Word publication build | SUCCESS — `34682979378` |
| ARB R2 | APPROVED WITH CONDITIONS; no open Blocker/Major/Minor |
| Branch protection | absent; `main.protected=false`, repository rulesets empty |
| Merge authorization | not granted for PR #178 |

## 3. Quality-gate matrix

| Gate | Stato | Evidence / disposition |
|---|---|---|
| Scope and dependency order | Passed | F5-A follows integrated F5 architecture; F5-B/F5-C excluded |
| Architecture conformance | Passed | ARB R2 98/100; all R1 findings closed |
| Closed registry | Passed | closed enums and unknown rejection unchanged |
| Raw Human Decision contract | Passed | canonical F2 validator reused; F5A-UT-024 and F2 regression green |
| Source-set metadata contract | Passed | canonical directory/pattern equality; recomputed-digest probe rejected |
| F4 trust-chain reuse | Passed | canonical F4 validator invoked; internal drift probe rejected |
| Determinism and digests | Passed | stable evaluation identity and rebuild comparison verified |
| Known answer | Passed | 15/0/0/0 retained; no percentage or scientific promotion |
| Documentation and traceability | Passed | R1, remediation evidence, plan, backlog, bootstrap and navigation coherent |
| Build and tests | Passed | all eight exact-head workflows successful |
| Links and MkDocs | Passed | documentation and Developer Foundation workflows successful |
| Word build | Passed | workflow `34682979378` |
| Security and privacy | Passed | bounded raw inputs and sanitized public projection |
| Safety and authority | Passed | read-only/human-only; physical interlocks remain authoritative |
| Observability | Passed | deterministic IDs, digests, counts, reason codes and fail-closed errors |
| Migration and rollback | Passed | additive change; F5-A artifacts can be reverted without F1-F4 mutation |
| F5-B dynamic workflow | Not Executed | outside F5-A and explicitly retained |
| F5-B consumer/accessibility | Not Executed | outside F5-A and explicitly retained |
| Scientific effectiveness | Blocked | by evidence absence; non-promotional state is the required result, not a merge defect |
| Production readiness | Blocked | explicitly not granted; non-promotional state is the required result |
| Re-review publication-head CI | Pending | mandatory after adding R2 documents/navigation |
| Protected/authorized merge | Blocked | owner authorization and branch-protection disposition are separate gates |

## 4. Risk and waiver register

| ID | Risk / waiver | Stato R2 | Treatment |
|---|---|---|---|
| RQ-F5A-R01 | malformed F2 receipt admitted | **Closed** | canonical F2 validator plus negative and regression tests |
| RQ-F5A-R02 | source-set metadata drift accepted | **Closed** | equality to canonical directory/pattern plus negative test |
| RQ-F5A-R03 | F4 internal drift checked only indirectly | **Closed** | direct canonical F4 validator reuse plus negative test |
| RQ-F5A-R04 | green CI mistaken for complete conformance | Controlled | independent code inspection and reproduced probes supplement CI |
| RQ-F5A-R05 | F5-A mistaken for scientific/production acceptance | Controlled | `NOT_EVALUABLE`, `NOT_READY`, `KEEP_OPEN`, `aiModelImplemented=false` retained |
| RQ-F5A-R06 | material change after reviewed head | Open condition | any material descendant invalidates R2 and requires another review |
| W-BKL046-F5A-REREVIEW-001 | independent-human re-review replaced once by disclosed AI-assisted R2 | Authorized for R2; consumed on publication | exact reviewed head plus one non-material publication descendant only |
| Branch protection / merge | absent and not waived | Blocked | separate owner authorization and expected-head disposition required |

### 4.1 Re-review independence waiver

`W-BKL046-F5A-REREVIEW-001` è autorizzata dal repository owner il 12/09/2026. È distinta dalla precedente `W-BKL046-F5A-REVIEW-001`, già consumata.

Scope e compensating controls:

- pubblicazione delle sole ARB/RQ R2 AI-assistite per il reviewed head e un singolo descendant non materiale;
- disclosure evidente che non sono approvazioni umane indipendenti;
- reviewer role separato e nessun silent repair durante l'assessment;
- verifica dei blob GitHub, riesecuzione locale F5/F2, probe negativi e CI exact-head;
- decadenza in caso di modifica materiale, merge, chiusura o superamento della PR.

Explicit exclusions:

- nessun merge o bypass di branch protection/CI;
- nessuna autorizzazione F5-B/F5-C;
- nessuna closure BKL-046, scientific-effectiveness, AI-runtime o production-readiness claim;
- nessun model/provider, image transfer, automatic acceptance, PixInsight apply, device command o Safety Authority.

## 5. Validation commands and evidence

Comandi rieseguiti localmente sui blob coincidenti con GitHub:

```text
node --test .github/scripts/test-ai-post-processing-advisory-f5-evaluation.mjs
node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs
node --test .github/scripts/test-ai-post-processing-advisory-contract.mjs
```

Risultati: 25/25 F5-A, 17/17 F2, generator e verifier PASS. La copia locale di review non contiene gli script F3/F4/consumer non modificati; questi sono stati verificati nel job F5 GitHub `103524907284`, che registra exit success e nessuna failure.

Probe di re-review:

| Probe | Expected | Actual | Gate |
|---|---|---|---|
| F2-invalid receipt: stable ID/edit/rationale | reject | rejected | Passed |
| source-set directory/pattern drift con digest ricalcolato | reject | rejected | Passed |
| F4 internal decision-state drift con digest ricalcolati | reject | rejected | Passed |

## 6. Readiness recommendation

**CONDITIONALLY READY FOR MERGE.**

Non risultano difetti tecnici o documentali aperti che impediscano l'integrazione di F5-A. La recommendation diventa operativamente azionabile soltanto quando:

1. il publication head R2 ottiene tutti i workflow attesi verdi;
2. il repository owner autorizza separatamente il merge sull'exact publication head;
3. l'owner dispone esplicitamente la deroga/accettazione dell'assenza di branch protection;
4. la PR non riceve modifiche materiali dopo il reviewed head.

F5-A resta una foundation deterministica accettabile, non una prova di efficacia scientifica o production readiness. BKL-046 resta aperto con closure `KEEP_OPEN`; F5-B/F5-C restano non eseguiti.

## 7. Traceability

- [ARB F5-A R2](ARB-BKL-046-F5A-AI-Assisted-Implementation-ReReview-2026-09-12.md)
- [ARB F5-A R1](ARB-BKL-046-F5A-AI-Assisted-Implementation-Review-2026-09-12.md)
- [RQ F5-A R1](RQ-BKL-046-F5A-AI-Assisted-Release-Quality-Review-2026-09-12.md)
- [F5-A remediation evidence](../validation/BKL-046-F5A-Validation-Remediation-Evidence-2026-09-12.md)
- [F5 validation plan](../validation/BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
- [PR #178](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/178)
