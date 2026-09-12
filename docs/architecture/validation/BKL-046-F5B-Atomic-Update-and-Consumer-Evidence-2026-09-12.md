# BKL-046 F5-B — Atomic Update and Consumer Evidence

| Campo | Valore |
|---|---|
| Identificativo | BKL-046-F5B-EVD-001 |
| Stato | Implementation candidate; technical exact-head CI green; ARB/RQ pending |
| Data | 12/09/2026 |
| Base | `46b956f0a6ceb04442ffd80447f810ef6463b5a8` — F5-A accepted/post-merge verified |
| Technical candidate head | `f6555e80760f9c5d179df3dc0ee4e02c7e265a21` |
| Scope | `F5-EVAL-011`–`F5-EVAL-014` |
| Authority | read-only, human-only, action/execution none, local physical interlocks |

## 1. Outcome

F5-B integra come candidato il report F5 nel ciclo automatico first/retry e nel consumer browser. L'implementazione non modifica il risultato scientifico del report e non si auto-attesta: i gate persistiti `F5B_DYNAMIC_UPDATE` e `F5B_CONSUMER` restano `NOT_EXECUTED` fino alla decisione governata di review/acceptance.

Il known answer resta:

| Asse | Stato |
|---|---|
| Technical evaluation | `READY_FOR_F5_EVALUATION` |
| Scientific effectiveness | `NOT_EVALUABLE_CURRENT_EVIDENCE` |
| Human-decision evidence | `NOT_AVAILABLE` |
| Production readiness | `NOT_READY_FOR_PRODUCTION` |
| Capability closure | `KEEP_OPEN` |
| AI model implemented | `false` |

## 2. Implemented candidate

- `.github/workflows/analyze-session-automatic.yml` esegue generator `--write`, `--check` e verifier F5 dopo F4 sia nel first path sia nella funzione `regenerate()` successiva a `git reset --hard origin/main`;
- `docs/data/ai-post-processing-advisory-f5-evaluation.json` appartiene al medesimo `governed_paths` di catalogo e projection F4;
- il verifier F5 controlla presenza, cardinalità, ordine first/retry e atomic path membership;
- il browser scarica con `cache: no-store` catalogo, projection F4 e evaluation F5;
- il browser valida contratti chiusi, registry, authority, cohort, source-set digest, catalog digest, F4 projection digest, evaluation identity/digest, summary e correlazioni;
- qualsiasi failure rende il contenuto F5 indisponibile con `EVALUATION UNAVAILABLE · FAIL-CLOSED`;
- il pannello presenta quattro outcome separati, conteggi assoluti, closure, assenza di modello AI, gate non PASS e retained limitations senza controlli mutativi.

## 3. Test evidence locale

| Test ID | Evidenza | Risultato locale |
|---|---|---|
| `F5-EVAL-011` | first/retry generation, check e verifier dopo F4 | PASS |
| `F5-EVAL-012` | report nel governed path atomico; negative omission/order | PASS |
| `F5-EVAL-013` | full browser freshness; stale F4, tamper, authority e Web Crypto negative | PASS |
| `F5-EVAL-014` | stato testuale, live region, focus, responsive e assenza di apply/execute/accept | PASS |
| F5 evaluator/workflow suite | 28 test | 28 PASS / 0 FAIL |
| F4/F5 consumer suite | 16 test | 16 PASS / 0 FAIL |
| persisted generator/verifier | `--check` e deterministic reconstruction | PASS |

### 3.1 Exact technical-head CI

Sul technical head `f6555e80760f9c5d179df3dc0ee4e02c7e265a21` risultano 10/10 workflow `SUCCESS`:

| Workflow | Run |
|---|---:|
| BKL-046 F5 governance | `34685036134` |
| BKL-046 F4 governance | `34685036171` |
| BKL-041 F5 Governance | `34685036116` |
| BKL-041 F4 Governance | `34685036120` |
| BKL-039 F5 Governance | `34685036204` |
| Validate Session Comparison Projection | `34685036176` |
| Validate Analytics Center Consistency | `34685036201` |
| Validate documentation (no deploy) | `34685036142` |
| Developer Foundation | `34685036198` |
| Genera manuale Word | `34685036264` |

Comandi riproducibili:

```text
node --test .github/scripts/test-ai-post-processing-advisory-f5-evaluation.mjs
node --test .github/scripts/test-ai-post-processing-assistant-consumer.mjs
node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs
```

## 4. Failure evidence

I test negativi dimostrano che il candidato rifiuta:

- catalogo o snapshot F4 non allineati al report F5;
- alterazione del payload anche se strutturalmente plausibile;
- source-set digest non corrispondente;
- registry, stato scientifico o authority ampliati;
- assenza di Web Crypto SHA-256;
- omissione del report F5 dal commit atomico;
- generazione F5 antecedente alla projection F4 nel retry.

Non esiste fallback su una evaluation precedente: il rendering corrente avviene soltanto dopo la verifica completa.

## 5. Security, privacy and safety

Non sono introdotti endpoint, provider, rete esterna, token browser, upload, database, scheduler o processi residenti. Il report pubblico continua a rifiutare actor, rationale/edits umani, path locali, hostname, immagini, credential e secret. Nessun controllo accetta automaticamente Recommendation, applica parametri PixInsight, modifica immagini o comanda apparati. `LOCAL_PHYSICAL_INTERLOCKS` resta la Safety Authority.

## 6. Pending governance evidence

Prima di qualsiasi acceptance F5-B restano obbligatori:

1. publication-head CI dopo questo record documentale;
2. ARB implementation review e Release Quality review, dichiarando la modalità effettiva;
3. eventuale waiver nuovo, esplicito e limitato alla singola PR/head; nessuna deroga F5-A è riutilizzabile;
4. publication-head CI dopo eventuali review documentali;
5. merge separatamente autorizzato e post-merge workflow/Pages verification.

F5-C e la decisione finale di closure non fanno parte di questo candidato.
