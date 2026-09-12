# RQ BKL-046 F5-A — AI-Assisted Release Quality Review

| Campo | Valore |
|---|---|
| Review ID | RQ-BKL-046-F5A-AI-ASSISTED-R1 |
| Package | BKL-046 F5-A — Evaluation Foundation |
| Pull request | #178 |
| Reviewed technical head | `11ad8768a35e2c64865710eba9b5460a62d8d703` |
| Base | `main` @ `16e0f101fda50e375bff6d5e9c8ec90d2083bc12` |
| Review date | 12/09/2026 |
| Review mode | AI-assisted quality assessment; not an independent human approval |
| Owner authorization | Granted 12/09/2026 for PR #178 review publication only |
| Review-independence waiver | `W-BKL046-F5A-REVIEW-001` |
| Recommendation | **NOT READY FOR MERGE — REWORK REQUIRED** |

## 1. Release impact report

La PR #178 introduce la foundation F5-A: contratto e registry F5, source admission, evaluator/generator/verifier, projection known-answer, test e CI. Non modifica il consumer, il workflow automatico first/retry, PixInsight, apparati o servizi residenti. Non è richiesto un semantic version bump né una release note applicativa in questa slice.

L'implementazione conserva correttamente gli esiti non promozionali, ma la conformance fra schema e validator runtime non è sufficiente per l'exit gate. La release recommendation è quindi negativa fino alla remediation e alla re-review.

## 2. Verified evidence

| Evidence | Result |
|---|---|
| PR scope | 1 commit; 14 files; 2.346 additions; 32 deletions |
| Reviewed head | `11ad8768a35e2c64865710eba9b5460a62d8d703` |
| Merge base | `16e0f101fda50e375bff6d5e9c8ec90d2083bc12`; branch 0 behind |
| Mergeability | mergeable at review time |
| F5-A tests | PASS — 22/22 |
| F5 persisted check/verifier | PASS |
| F5 governance | SUCCESS — run `34681155102` |
| F4 governance | SUCCESS — run `34681155058` |
| BKL-041 F4 Governance | SUCCESS — run `34681155063` |
| Validate documentation | SUCCESS — run `34681155039` |
| Developer Foundation | SUCCESS — run `34681155068` |
| Word publication build | SUCCESS — run `34681155048` |
| ARB result | REWORK REQUIRED; 2 Major, 1 Minor |
| Branch protection | absent; `main.protected=false`, repository rulesets empty |
| Merge authorization | not granted for PR #178 |

## 3. Quality-gate matrix

| Gate | Stato | Evidence / disposition |
|---|---|---|
| Scope and dependency order | Passed | F5-A follows integrated F5 architecture; F5-B/F5-C excluded |
| Architecture conformance | Failed | `ARB-F5-C01` not closed because runtime raw validation is weaker than F2/F5 schema |
| Closed registry | Passed | cohort/gate/outcome/reason-code registry and unknown rejection implemented |
| Raw Human Decision contract | Failed | nonconforming F2 receipt accepted by exported validator; `ARB-F5A-M01` |
| Source-set metadata contract | Failed | wrong directory and wildcard pattern accepted after digest recomputation; `ARB-F5A-M02` |
| F4 trust-chain reuse | Conditionally Passed | CI regression green; direct F5 validation remains partial and duplicated |
| Determinism and digests | Passed | stable identity and deterministic rebuild verified for governed baseline |
| Known answer | Passed | 15/0/0/0/2 preserved; no success percentage |
| Documentation and traceability | Passed | architecture, validation, evidence, backlog, bootstrap and navigation present |
| Build, tests and formatting | Passed | Developer Foundation `34681155068` |
| Links and MkDocs | Passed | Validate documentation `34681155039` and Developer Foundation MkDocs step |
| Word build | Passed | `34681155048` |
| Security and privacy | Conditionally Passed | public projection sanitization verified; raw input bounds incomplete |
| Safety and authority | Passed | read-only, human-only, no apply/command; physical interlocks preserved |
| Observability | Passed | counts, reason codes, identities and digests emitted without raw sensitive data |
| Migration and rollback | Passed | additive artifacts; F1-F4 removable independently |
| F5-B dynamic workflow | Not Executed | intentionally outside F5-A |
| F5-B consumer/accessibility | Not Executed | intentionally outside F5-A |
| Scientific effectiveness | Blocked | no exact eligible provenance and no approved ground truth |
| Production readiness | Blocked | explicitly `NOT_READY_FOR_PRODUCTION` |
| Review-publication head CI | Pending | required after these review documents are committed |
| Protected/authorized merge | Blocked | no server protection and no PR #178 merge authorization/waiver |

## 4. Risk and waiver register

| ID | Risk / waiver | Stato | Treatment |
|---|---|---|---|
| RQ-F5A-R01 | malformed F2 receipt admitted as governed source | Open Major | remediate `ARB-F5A-M01`; add schema/runtime negative tests |
| RQ-F5A-R02 | source-set metadata drift accepted by standalone validator | Open Major | remediate `ARB-F5A-M02`; pin canonical directory/pattern |
| RQ-F5A-R03 | F4 internal drift checked only through separate regression | Open Minor | reuse canonical validator or prove equivalent trust-chain checks |
| RQ-F5A-R04 | green CI interpreted as complete contract conformance | Controlled | review records explicit probes and retains `NOT READY` |
| RQ-F5A-R05 | F5-A mistaken for scientific or production acceptance | Controlled | four outcomes separated; `KEEP_OPEN`, `aiModelImplemented=false` |
| W-BKL046-F5A-REVIEW-001 | independent-human-review requirement replaced once by disclosed AI-assisted ARB/RQ publication | Authorized; consumed by first publication | PR #178 technical head plus single non-material review publication only |
| Branch protection / merge | absent and not waived | Blocked | separate owner authorization and expected-head disposition required only after re-review |

### 4.1 One-time review-independence waiver

`W-BKL046-F5A-REVIEW-001` è stato esplicitamente autorizzato dal repository owner il 12/09/2026.

Scope:

- consente la pubblicazione e l'uso di governance delle review ARB/RQ F5-A per PR #178 come valutazioni AI-assistite;
- si applica al technical head `11ad8768a35e2c64865710eba9b5460a62d8d703` e al singolo commit non materiale che pubblica review e navigation;
- è consumato dalla prima pubblicazione e scade definitivamente al merge, chiusura o superamento della PR.

Compensating controls:

- disclosure evidente che le review non sono approvazioni umane indipendenti;
- separazione del reviewer role e divieto di silent repair durante l'assessment;
- probe riproducibili oltre alla suite proposta;
- finding Major bloccanti non convertiti in condizioni post-merge;
- nuova review obbligatoria dopo remediation.

Explicit exclusions:

- nessuna autorizzazione o deroga al merge;
- nessun bypass di branch protection o CI;
- nessuna acceptance F5-A/F5-B/F5-C;
- nessuna closure, scientific-effectiveness, AI-runtime o production-readiness claim;
- nessun model/provider, image transfer, automatic acceptance, apply, remediation, command o Safety authority.

Le deroghe della PR #177 sono consumate/scadute e non sono riutilizzate.

## 5. Validation commands and evidence

Il technical head ha eseguito con successo:

```text
node --test .github/scripts/test-ai-post-processing-advisory-f5-evaluation.mjs
node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs
node --test .github/scripts/test-ai-post-processing-advisory-contract.mjs
node --test .github/scripts/test-ai-post-processing-advisory-demonstrator.mjs
node --test .github/scripts/test-ai-post-processing-advisory-projection.mjs
node .github/scripts/generate-ai-post-processing-advisory-projection.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-projection.mjs
node --test .github/scripts/test-ai-post-processing-assistant-consumer.mjs
```

Probe review aggiuntivi osservati:

| Probe | Expected | Actual | Gate |
|---|---|---|---|
| receipt con stable ID, edits e rationale non conformi a F2 | reject | accepted | Failed |
| report con source directory/pattern non canonici e digest ricalcolato | reject | accepted | Failed |

Una validazione Draft 2020-12 effettiva dello schema e dei raw payload non è eseguita dal workflow: il passo corrente effettua soltanto `JSON.parse` dello schema.

## 6. Readiness recommendation

**NOT READY FOR MERGE — REWORK REQUIRED.**

Prima di una nuova recommendation servono:

1. correzione dei due Major ARB;
2. negative test che falliscano sul technical head attuale e passino sul remediation head;
3. disposition del finding F4 trust-chain;
4. 6/6 workflow verdi sul nuovo exact head;
5. nuova review ARB/RQ, senza riuso della deroga consumata;
6. solo dopo esito favorevole, autorizzazione al merge e branch-protection disposition separate.

F5-A resta un implementation candidate. F5-B/F5-C non possono iniziare; BKL-046 resta aperto.

## 7. Traceability

- [F5-A ARB implementation review](ARB-BKL-046-F5A-AI-Assisted-Implementation-Review-2026-09-12.md)
- [F5 architecture](../scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md)
- [F5 validation plan](../validation/BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
- [F5-A implementation evidence](../validation/BKL-046-F5A-Evaluation-Foundation-Evidence-2026-09-12.md)
- [PR #178](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/178)

