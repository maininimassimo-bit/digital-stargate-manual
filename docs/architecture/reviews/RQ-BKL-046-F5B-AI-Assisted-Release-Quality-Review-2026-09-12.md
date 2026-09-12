# RQ BKL-046 F5-B — AI-Assisted Release Quality Review

| Campo | Valore |
|---|---|
| Review ID | RQ-BKL-046-F5B-AI-ASSISTED-R1 |
| Package | BKL-046 F5-B — Atomic Update and Consumer |
| Pull request | #179 |
| Reviewed head | `5c0999b715e9a238df119cbc36fdbac2bdef78bf` |
| Technical head | `f6555e80760f9c5d179df3dc0ee4e02c7e265a21` |
| Base | `main` @ `46b956f0a6ceb04442ffd80447f810ef6463b5a8` |
| Review date | 12/09/2026 |
| Review mode | AI-assisted release-quality review; not an independent human approval |
| Owner authorization | Granted 12/09/2026 for PR #179 ARB/RQ publication only |
| Review-independence exception | `W-BKL046-F5B-REVIEW-001` |
| ARB decision | **APPROVED WITH CONDITIONS — 98/100** |
| Recommendation | **CONDITIONALLY READY FOR MERGE** |

## 1. Release impact report

F5-B modifica il comportamento di pubblicazione e presentazione read-only: il workflow post-import include ora l'evaluation F5 nello stesso commit di catalogo/F4, mentre il portale mostra gli outcome F5 solo dopo la verifica crittografica dell'intera catena. Non vengono modificati schema F5, evaluator, known-answer o authority.

L'incremento non introduce servizi, database, scheduler aggiuntivi, endpoint, provider, image transfer, PixInsight apply o command path. Non è assegnato un semantic version bump o una release note applicativa distinta dal package F5; la closure e l'eventuale release disposition restano F5-C.

## 2. Verified evidence

| Evidence | Result |
|---|---|
| PR state | open, non-draft, mergeable |
| PR scope | 3 commit; 18 file; 656 additions; 99 deletions |
| Reviewed head | `5c0999b715e9a238df119cbc36fdbac2bdef78bf` |
| Merge base | `46b956f0a6ceb04442ffd80447f810ef6463b5a8`; `main` invariata |
| Local aggregate | PASS — 85/85 |
| F5 evaluator/workflow suite | PASS — 28/28 |
| F4/F5 consumer suite | PASS — 16/16 |
| Generator/check/verifier | PASS — F4 e F5 |
| F5 governance | SUCCESS — `34685550353` |
| F4 governance | SUCCESS — `34685550289` |
| Cross-capability regressions | SUCCESS — 5 workflow |
| Validate documentation | SUCCESS — `34685550285` |
| Developer Foundation | SUCCESS — `34685550305` |
| Word build | SUCCESS — `34685550251` |
| ARB F5-B | APPROVED WITH CONDITIONS — 98/100 |
| Branch protection | absent; `main.protected=false`, repository rulesets empty |
| Merge authorization | not granted for PR #179 |

## 3. Quality-gate matrix

| Gate | Stato | Evidence / disposition |
|---|---|---|
| Scope and dependency order | Passed | F5-A accepted predecessor; F5-B bounded; F5-C excluded |
| Architecture conformance | Passed | ARB 98/100; no Blocker/Major/Minor |
| First/retry generation order | Passed | structural verifier plus positive/negative tests |
| Atomic publication | Passed | F5 report nel medesimo `governed_paths` di catalogo/F4 |
| Browser freshness | Passed | catalog/F4/F5 identity and digest chain; no-store; no permissive fallback |
| Failure behavior | Passed | stale/tamper/authority/Web Crypto render unavailable fail-closed |
| Known answer and scientific boundary | Passed | 15/0/0/0; `NOT_EVALUABLE`, `NOT_READY`, `KEEP_OPEN`, no AI model |
| Documentation and traceability | Passed | architecture, plan, evidence, bootstrap, backlog, handover, index e nav coerenti |
| Build, tests and formatting | Passed | 85 tests e exact-head Developer Foundation green |
| Links, MkDocs and Mermaid | Passed | documentation workflow `34685550285` e Developer Foundation green |
| Word build | Passed | workflow `34685550251` |
| Security and privacy | Passed | closed fields/path, no raw/private/browser token or external endpoint |
| Safety and authority | Passed | read-only/human-only; no apply/command; physical interlocks unchanged |
| Accessibility | Passed | text status, live region, focus, responsive and non-mutative controls |
| Observability | Passed | deterministic identity, digest, counts, reason codes and diagnostic failure |
| Migration | Not Applicable | additive repository/browser projection; no persistent migration |
| Rollback | Passed | revert workflow/consumer additions without changing F1–F5-A contracts |
| Live post-import execution | Not Executed | required post-merge; cannot be inferred from structural tests |
| Live Pages verification | Not Executed | required post-merge before F5-C |
| Scientific effectiveness | Blocked | evidence absent; required non-promotional result, not a merge defect |
| Production readiness | Blocked | explicitly not granted; not a merge defect |
| Review-publication head CI | Pending | required after adding ARB/RQ and navigation |
| Protected/authorized merge | Blocked | separate owner authorization and branch-protection disposition required |

## 4. Risk and waiver register

| ID | Risk / waiver | Stato | Treatment |
|---|---|---|---|
| RQ-F5B-R01 | F5 stale rispetto a catalogo/F4 | Controlled | first/retry generation, atomic set and browser digest chain |
| RQ-F5B-R02 | workflow cambia ordine o omette il report | Controlled | structural verifier and negative mutation tests |
| RQ-F5B-R03 | tampering o authority escalation nel browser | Controlled | closed validation and fail-closed rendering |
| RQ-F5B-R04 | candidate UI letta come efficacia AI | Controlled | four distinct outcomes, limitations, `aiModelImplemented=false` |
| RQ-F5B-R05 | structural test scambiato per runtime proof | Open condition | live post-import/Pages evidence required after merge |
| RQ-F5B-R06 | material change after reviewed head | Open condition | invalidates review and requires re-review |
| `W-BKL046-F5B-REVIEW-001` | independent-human review replaced once by disclosed AI-assisted ARB/RQ | Authorized; consumed on publication | exact reviewed head plus one non-material review/navigation descendant |
| Branch protection / merge | absent and not waived | Blocked | separate owner authorization and exact-head waiver required |

### 4.1 Review-independence exception

`W-BKL046-F5B-REVIEW-001` deriva dall'autorizzazione owner del 12/09/2026. Consente esclusivamente la pubblicazione di ARB/RQ AI-assistite, con disclosure che non sono approvazioni umane indipendenti.

Sono esclusi: merge, bypass di CI/branch protection, F5-C, closure BKL-046, scientific-effectiveness claim, AI runtime, production readiness, model/provider, image transfer, automatic acceptance, PixInsight apply, device command e Safety Authority.

## 5. Validation commands and evidence

Comandi rieseguiti sul reviewed head con blob parity GitHub/local verificata:

```text
node --test .github/scripts/test-ai-post-processing-advisory-contract.mjs .github/scripts/test-ai-post-processing-advisory-demonstrator.mjs .github/scripts/test-ai-post-processing-advisory-projection.mjs .github/scripts/test-ai-post-processing-advisory-f5-evaluation.mjs .github/scripts/test-ai-post-processing-assistant-consumer.mjs
node .github/scripts/generate-ai-post-processing-advisory-projection.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-projection.mjs
node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs
```

Risultato: 85/85 test PASS; generator e verifier F4/F5 PASS. Il workflow documentale e Developer Foundation confermano MkDocs, link, roadmap consistency, build e test repository-wide sul medesimo head.

## 6. Readiness recommendation

**CONDITIONALLY READY FOR MERGE.**

La recommendation diventa operativamente azionabile soltanto quando:

1. il publication head contenente soltanto ARB/RQ e navigazione ottiene tutti i workflow attesi verdi;
2. la PR non riceve modifiche materiali dopo il reviewed head;
3. il repository owner autorizza separatamente il merge sull'exact publication head;
4. l'owner dispone esplicitamente una nuova deroga una tantum per l'assenza di branch protection;
5. dopo il merge vengono verificati workflow e Pages live prima di iniziare F5-C.

F5-B resta una capability deterministica read-only; non prova efficacia scientifica o production readiness. BKL-046 resta aperto con closure `KEEP_OPEN`.

## 7. Traceability

- [ARB F5-B](ARB-BKL-046-F5B-AI-Assisted-Implementation-Review-2026-09-12.md)
- [F5-B evidence](../validation/BKL-046-F5B-Atomic-Update-and-Consumer-Evidence-2026-09-12.md)
- [F5 validation plan](../validation/BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
- [F5 architecture](../scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md)
- [PR #179](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/179)
