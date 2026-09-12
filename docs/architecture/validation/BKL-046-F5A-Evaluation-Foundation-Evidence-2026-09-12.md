# BKL-046 F5-A — Evaluation Foundation Evidence

| Campo | Valore |
|---|---|
| Evidence ID | BKL-046-F5A-EVIDENCE-001 |
| Data | 12/09/2026 |
| Stato | Local implementation evidence complete; exact-head CI and governance review pending |
| Baseline | F5 architecture merge `16e0f101fda50e375bff6d5e9c8ec90d2083bc12` |
| Branch | `feature/bkl-046-f5a-evaluation-foundation` |
| Scope | F5-A contract, registry, source allowlist/correlation, evaluator, generator, projection, verifier, tests and CI definition |
| Explicitly excluded | F5-B workflow/consumer; F5-C acceptance/closure; AI model; scientific effectiveness; production/apply authority |

## 1. Outcome

F5-A rende eseguibile la foundation di valutazione approvata dal design F5. Chiude le condizioni architetturali `ARB-F5-C01` e `ARB-F5-C02` nel candidato di implementazione, ma non le dichiara accettate prima della review F5-A.

Il risultato è `F5A_EVALUATION_FOUNDATION_READY` con closure recommendation `KEEP_OPEN`. Non costituisce acceptance della capability, prova di efficacia scientifica, implementazione di un modello AI o autorizzazione produttiva.

## 2. Delivered controls

| Control | Evidence |
|---|---|
| Closed machine-readable contract | schema F5-A con proprietà chiuse, registry enumerata e raw source definition |
| `ARB-F5-C01` candidate closure | directory e filename allowlisted; raw authority/digest validation; exact session/recommendation/correlation/receipt/BKL-045 linkage; ordering e duplicate rejection |
| `ARB-F5-C02` candidate closure | registry machine-readable per cohort, selection rule, technical gate, outcome, evidence state e reason code; unknown value rejection |
| Deterministic evaluation | canonical JSON SHA-256 identity/digest, stable evaluation ID e rebuild comparison |
| Missingness semantics | empty cohort `NOT_EVALUABLE`/`NOT_AVAILABLE`; nessuna percentuale o successo implicito |
| Authority | read-only, human-only, action/execution authority `NONE`, physical interlock authority invariata |
| Public projection boundary | raw actor/rationale/edits non persistiti; forbidden sensitive fields rejected |
| Regression gate | workflow F5 definito con F2, F3, F4 projection e F4 consumer regressions |

## 3. Commands and local results

| Command | Result |
|---|---|
| `node --test .github/scripts/test-ai-post-processing-advisory-f5-evaluation.mjs` | PASS — 22/22, 0 failed |
| `node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --write` | PASS — report generated |
| `node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check` | PASS — persisted report aligned |
| `node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs` | PASS — registry, source contracts and deterministic reconstruction verified |

Il workflow `.github/workflows/bkl-046-f5-governance.yml` deve ancora fornire exact-head evidence per questi comandi e per tutte le regressioni F2-F4. Nessuna run ID è anticipata in questo record.

## 4. Persisted known answer

| Field | Observed value |
|---|---|
| Evaluation ID | `BKL046-F5A-F4FEB5E207DD3F7D3E4F6C87` |
| Evaluation digest | `174f8d75a27160b476c65d2670c50e4089811834dd1e5867418c77dfbac41f70` |
| Canonical sessions | 15 |
| Exact provenance eligible | 0 |
| Human Decision receipts | 0 |
| Execution evidence | 0 |
| Uncorrelated BKL-045 sources | 2 |
| Technical state | `READY_FOR_F5_EVALUATION` |
| Scientific state | `NOT_EVALUABLE_CURRENT_EVIDENCE` |
| Human-decision state | `NOT_AVAILABLE` |
| Production state | `NOT_READY_FOR_PRODUCTION` |
| Closure recommendation | `KEEP_OPEN` |
| AI model implemented | `false` |

Questi valori descrivono la evidence disponibile. Non misurano accuracy, quality uplift, recommendation correctness, rappresentatività o beneficio scientifico.

## 5. Test coverage summary

La suite verifica:

- closed report shape, full population e known answer;
- empty-cohort semantics senza percentuali permissive;
- path allowlist, traversal e directory-content rejection;
- identity/digest deterministici e anti-tampering;
- catalog/F4 population drift;
- Human Decision authority, orphan, duplicate e exact correlation;
- execution evidence authority, decision link, temporal ordering e BKL-045 reference;
- separation fra decision, execution e scientific outcome;
- unknown outcome/reason-code rejection;
- report field, authority e closure escalation rejection;
- directory sorgenti assenti come empty set esplicito.

## 6. Retained limitations and stop conditions

- F5-B dynamic first/retry generation, atomic publication, consumer freshness e accessibility sono `NOT_EXECUTED`.
- Nessuna ground-truth method è approvata; scientific effectiveness resta non valutabile.
- Nessun Human Decision Receipt o execution evidence reale è presente nella baseline.
- Exact-head CI, implementation ARB/RQ, merge authorization e post-merge verification non sono ancora disponibili.
- F5-C non può proporre closure finché i gate F5-B e F5-C non sono completati.
- `aiModelImplemented=false`; nessun model/provider, image transfer, apply, command, remediation o Safety Authority è introdotto.

## 7. Traceability

- [F5 architecture](../scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md)
- [F5 validation plan](BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
- [F5 architecture review](../reviews/ARB-BKL-046-F5-AI-Assisted-Architecture-Review-2026-09-12.md)
- [F5 architecture release-quality review](../reviews/RQ-BKL-046-F5-AI-Assisted-Release-Quality-Review-2026-09-12.md)
- [F4 acceptance](../../project/BKL-046-F4-ACCEPTANCE-2026-09-12.md)
