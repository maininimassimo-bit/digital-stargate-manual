# RQ BKL-046 F4 — AI-Assisted Release Quality Review

| Campo | Valore |
|---|---|
| Review ID | RQ-BKL-046-F4-AI-ASSISTED-R1 |
| Package | BKL-046 F4 — Session/Provenance-Driven Read-Only Consumer |
| Pull request | #172 |
| Reviewed proposal head | `1ccb6970ee2789663d32e01d188e8f974393ffbf` |
| Base | `main` @ `ec4eb991bd9e20bcd34b00e111400a5ac07fd750` |
| Review date | 11/09/2026 |
| Review mode | AI-assisted quality assessment; not an independent human approval |
| Owner authorization | Required before governance adoption or merge |
| Recommendation | CONDITIONALLY READY FOR ARCHITECTURE PROPOSAL MERGE |
| Implementation readiness | NOT READY — implementation artifacts and runtime evidence do not yet exist |
| Waiver | None |

## 1. Release impact report

La PR #172 introduce esclusivamente il progetto architetturale F4 e la sua discoverability. Non modifica schema runtime, generator, projection, workflow di import, JavaScript consumer, session data o apparati.

L'impatto di release è quindi documentale e additivo. La proposta definisce gli obblighi per l'implementazione futura, ma non deve essere interpretata come disponibilità del consumer o come completamento del requisito di aggiornamento automatico.

## 2. Verified evidence

| Evidence | Result |
|---|---|
| PR scope | 3 files, 338 additions, 0 deletions |
| Reviewed head | `1ccb6970ee2789663d32e01d188e8f974393ffbf` |
| BKL-041 F4 Governance | SUCCESS — run `34649750149` |
| Genera manuale Word | SUCCESS — run `34649750186` |
| Validate documentation | SUCCESS — run `34649750118` |
| Mergeability | mergeable on reviewed snapshot |
| F3 predecessor | Accepted and post-merge verified |

## 3. Quality-gate matrix

| Gate | Stato | Evidence / disposition |
|---|---|---|
| Scope and dependency order | Passed | F4 follows F3; F5 remains gated by F4 acceptance |
| Architecture completeness | Passed | current/target, components, data flow, slices, risks and criteria present |
| ADR consistency | Passed | ADR-008 applied; no conflicting decision introduced |
| Documentation navigation | Passed | unique project-index and MkDocs entries |
| MkDocs / links | Passed | repository Validate documentation run `34649750118` |
| Word publication build | Passed | run `34649750186` |
| Mermaid | Passed | documentation CI completed on exact reviewed head |
| Security/privacy design | Conditionally Passed | ARB-F4-C01/C02 mandatory before implementation acceptance |
| Safety/authority design | Passed | read-only, human-only, action/execution NONE, local interlocks preserved |
| Observability design | Passed | proposed counters, reason codes and workflow failure evidence defined |
| Migration/rollback design | Passed | additive slices and repository revert path defined |
| Implementation build/tests | Not Applicable | architecture-proposal PR; no F4 implementation exists |
| Dynamic post-import execution | Not Executed | mandatory F4-B evidence; documentation is not runtime proof |
| Consumer freshness/tamper execution | Not Executed | mandatory F4-C evidence |
| Hardware/OAT | Not Applicable | F4 is repository/portal-side and must not modify observatory runtime |
| Protected merge / post-merge Pages | Blocked | requires owner authorization and proposal merge |

## 4. Risk and waiver register

| ID | Risk | State | Treatment |
|---|---|---|---|
| RQ-F4-R01 | source glob admits non-sidecar JSON | Open condition | close ARB-F4-C01 in F4-A |
| RQ-F4-R02 | raw provenance metadata exposed or duplicated client-side | Open condition | close ARB-F4-C02 before F4-C exit |
| RQ-F4-R03 | zero matched provenance misread as implementation failure | Accepted limitation | publish explicit `PROVENANCE_UNAVAILABLE`, no inference |
| RQ-F4-R04 | proposal mistaken for implemented automatic refresh | Controlled | status remains Proposed; implementation gates Not Executed |
| RQ-F4-R05 | first and retry generation paths diverge | Open implementation risk | verifier and tests required in F4-B |

Nessuna waiver è richiesta o concessa. Le condizioni aperte non possono essere declassate mediante documentazione o wording.

## 5. Validation commands and future evidence

La proposal CI ha già eseguito i gate documentali applicabili. L'implementazione dovrà aggiungere ed eseguire almeno:

```text
node .github/scripts/verify-ai-post-processing-advisory-projection.mjs
node .github/scripts/generate-ai-post-processing-advisory-projection.mjs --check
node --test .github/scripts/test-ai-post-processing-advisory-contract.mjs
node --test .github/scripts/test-ai-post-processing-advisory-demonstrator.mjs
node --test .github/scripts/test-ai-post-processing-advisory-projection.mjs
node --test .github/scripts/test-ai-post-processing-assistant-consumer.mjs
```

Il gate dovrà inoltre verificare staticamente le due invocazioni nel workflow, l'inclusione del persisted output in `governed_paths` e il regeneration path successivo a `git reset --hard origin/main`.

## 6. Readiness recommendation

**CONDITIONALLY READY FOR ARCHITECTURE PROPOSAL MERGE.**

Condizioni per il merge della proposta:

1. il repository owner autorizza esplicitamente le review ARB/RQ come AI-assistite e non come approvazioni umane indipendenti;
2. l'exact-head CI successivo alla pubblicazione delle review rimane verde;
3. il merge usa l'head atteso e viene seguito da verifica dei workflow `main` e Pages.

Questa recommendation non autorizza implementation acceptance, F5, model/provider, image transfer, automatic acceptance, PixInsight apply, remediation, device command o Safety Authority.

## 7. Next quality gate

Dopo il merge della proposta, l'unico passo dependency-ordered è F4-A — source and projection contract. F4-A deve chiudere `ARB-F4-C01`; la strategia scelta per `ARB-F4-C02` deve essere definita entro F4-A e completata prima dell'exit gate F4-C.
