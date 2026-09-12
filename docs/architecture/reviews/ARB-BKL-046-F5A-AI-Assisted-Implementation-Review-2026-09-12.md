# ARB BKL-046 F5-A — AI-Assisted Implementation Review

| Campo | Valore |
|---|---|
| Review ID | ARB-BKL-046-F5A-AI-ASSISTED-R1 |
| Package | BKL-046 F5-A — Evaluation Foundation |
| Review date | 12/09/2026 |
| Pull request | #178 |
| Reviewed technical head | `11ad8768a35e2c64865710eba9b5460a62d8d703` |
| Base | `main` @ `16e0f101fda50e375bff6d5e9c8ec90d2083bc12` |
| Review mode | AI-assisted governance assessment; not an independent human review |
| Owner authorization | Granted 12/09/2026 for PR #178 review publication only |
| Review-independence waiver | `W-BKL046-F5A-REVIEW-001` |
| Decision | **REWORK REQUIRED** |
| Score | **89/100** |

## 1. Review scope and independence disclosure

La review valuta l'implementazione F5-A della PR #178: schema, registry, raw source admission, exact correlation, evaluator, generator, projection, verifier, test, CI e traceability. F5-B dynamic workflow/consumer e F5-C acceptance/closure sono fuori scope e restano non eseguiti.

La valutazione è AI-assistita, autorizzata dal repository owner e **non equivale a un'approvazione umana indipendente**. Lo stesso ambiente AI ha assistito la preparazione del candidato; il passaggio al ruolo reviewer impedisce silent repair durante l'assessment ma non crea indipendenza umana o organizzativa.

La deroga `W-BKL046-F5A-REVIEW-001` consente una sola pubblicazione delle review ARB/RQ della PR #178 per il technical head indicato e per il solo commit non materiale che pubblica queste review. Non autorizza merge, non deroga alla CI, non risolve i finding e non è riutilizzabile.

## 2. Repository evidence verified

- PR #178 aperta, non draft, mergeable, 1 commit, 14 file, 2.346 addition e 32 deletion.
- Technical head e branch remota coincidono con `11ad8768a35e2c64865710eba9b5460a62d8d703`; `main` è ancora `16e0f101fda50e375bff6d5e9c8ec90d2083bc12`.
- Sei workflow pull-request sul technical head sono conclusi con successo: F5 governance `34681155102`, F4 governance `34681155058`, BKL-041 F4 Governance `34681155063`, Validate documentation `34681155039`, Developer Foundation `34681155068`, Word `34681155048`.
- La suite F5-A esegue 22 test con 22 PASS / 0 FAIL; generator `--check` e verifier sono verdi.
- Il report persistito `BKL046-F5A-F4FEB5E207DD3F7D3E4F6C87`, digest `174f8d75a27160b476c65d2670c50e4089811834dd1e5867418c77dfbac41f70`, registra 15 sessioni, 0 provenance eligible, 0 Human Decision Receipt, 0 execution evidence e 2 source BKL-045 non correlate.
- Gli esiti rimangono `READY_FOR_F5_EVALUATION`, `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION`, `KEEP_OPEN` e `aiModelImplemented=false`.
- `main.protected=false` e non esistono repository ruleset; nessuna deroga merge è stata autorizzata per PR #178.
- Nessuna review o review thread preesisteva sulla PR al momento dell'assessment.

## 3. Architecture scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Program and dependency alignment | 100 | F5-A segue il design F5 integrato e mantiene F5-B/F5-C fuori scope |
| Domain and layer integrity | 92 | policy, generator, projection e verifier sono separati; la validazione F4 è duplicata solo parzialmente |
| Source authority and provenance | 82 | allowlist e correlazione nominale sono presenti, ma il raw validator non applica integralmente il contratto F2 |
| Contract and schema/runtime congruence | 72 | schema chiuso disponibile; CI lo esegue solo con `JSON.parse` e il validatore runtime accetta shape vietate dallo schema |
| Determinism and identity | 97 | canonical JSON SHA-256, stable evaluation ID e rebuild comparison verificati |
| Scientific evidence integrity | 100 | empty cohort e ground truth assente non sono promosse a efficacia |
| Security and privacy | 90 | projection sanitizzata e authority chiusa; raw input non rispetta ancora tutti i bound F2 |
| Safety and authority | 100 | nessun apply, command o produzione; interlock fisici locali invariati |
| Operability and observability | 94 | failure esplicita, reason code e digest disponibili; F5-B resta correttamente non eseguita |
| Migration and rollback | 97 | incremento additivo senza mutation di F1-F4 |
| Traceability and documentation | 99 | bootstrap, backlog, architecture, validation, evidence e navigation coerenti |
| Test and CI evidence | 86 | 22 test e 6 workflow verdi, ma mancano i negative test che espongono la divergenza schema/runtime |

## 4. Findings

### Blocker

Nessuno.

### Major

**ARB-F5A-M01 — Il raw Human Decision validator non applica il contratto F2 completo**

`validateRawHumanDecisionSource()` verifica exact keys, authority, timestamp, disposition e digest, ma non applica integralmente `$defs/humanDecisionReceipt` di F2. Un probe riproducibile sul reviewed head è stato accettato con:

- `receiptId` contenente spazi, vietato da `stableId`;
- `actorRef` di un solo carattere, sotto il minimo F2;
- `decisionEdits` con item arbitrario non conforme a `decisionEdit`;
- `decisionRationale` di 5.000 caratteri, oltre il massimo 4.096.

Risultato osservato: `validateRawHumanDecisionSource(...) === true`.

Il workflow F5 esegue `JSON.parse` sullo schema, non una validazione Draft 2020-12 del report e delle raw source con risoluzione del riferimento F2. La sanitizzazione impedisce che actor, edits e rationale entrino nella projection pubblica, ma non chiude il contratto di ammissione richiesto da `ARB-F5-C01`.

Remediation obbligatoria:

1. validare le raw Human Decision source contro il contratto F2 completo mediante validator machine-readable con local reference resolution, oppure riusare un validator F2 canonico equivalente;
2. applicare pattern/bound per stable ID, `decisionEdits`, `decisionRationale` e ogni proprietà del receipt;
3. aggiungere negative test per ciascuna shape sopra indicata;
4. eseguire la conformance schema/runtime in CI, non soltanto il parse JSON;
5. ripetere ARB/RQ sull'exact remediation head.

**ARB-F5A-M02 — I metadata canonici del source-set non sono chiusi dal validator runtime**

`validateSourceSet()` richiede soltanto che `directory` e `pathPattern` siano stringhe non vuote. Un secondo probe sul report baseline, dopo sostituzione di:

- `humanDecisionSourceSet.directory = "wrong-directory"`;
- `humanDecisionSourceSet.pathPattern = ".*"`;
- ricalcolo coerente di `evaluationDigest`;

ha prodotto `validateRealEvidenceEvaluation(report) === true`.

Il verifier persistito ricostruisce il report e intercetterebbe questo drift nel percorso repository corrente, ma il validator esportato non rispetta autonomamente i `const` e pattern dichiarati dallo schema. La contract boundary rimane quindi permissiva fuori dal rebuild path.

Remediation obbligatoria:

1. parametrizzare `validateSourceSet()` con directory e regex canoniche attese;
2. richiedere equality esatta per `directory` e `pathPattern`;
3. aggiungere negative test con digest ricalcolato;
4. dimostrare con CI che schema e validator rifiutano lo stesso drift.

### Minor

**ARB-F5A-C01 — La validazione F4 è parziale e duplicata**

Il design F5 prevede il riuso del validator e rule set F4. L'evaluator F5 verifica top-level `projectionDigest`, authority e population set, mentre la coerenza interna F4 è demandata alle regressioni CI. Una projection modificata con digest top-level ricalcolato può essere accettata dal solo evaluator F5 senza verifica diretta di source-set digest, record digest e summary.

Prima dell'acceptance F5-A occorre riusare il validator F4 canonico oppure documentare e testare un controllo equivalente della trust chain interna. La regressione F4 nel workflow resta un controllo compensativo valido ma non sostituisce la congruenza del boundary F5.

### Observations

**ARB-F5A-O01 — Esiti correttamente non promozionali**  
Il report non dichiara efficacia scientifica, produzione, AI runtime o closure.

**ARB-F5A-O02 — C01/C02 del design non sono entrambe chiuse**  
Il registro chiuso richiesto da `ARB-F5-C02` è implementato e coperto da unknown rejection. `ARB-F5-C01` resta aperta per i finding M01/M02.

**ARB-F5A-O03 — F5-B correttamente separata**  
Dynamic update, atomic workflow integration, consumer freshness e accessibility rimangono `NOT_EXECUTED` e non sono rappresentati come failure F5-A né come evidence disponibile.

## 5. Domain, dependency and contract assessment

La direzione generale delle dipendenze è corretta: catalogo e projection F4 alimentano una policy deterministica, quindi generator, projection e verifier. Non emerge una dipendenza UI-to-domain o una mutation path.

La debolezza è nel punto di ingresso delle source future: lo schema dichiara un boundary più stretto del codice che effettivamente ammette i payload. Poiché la condizione architetturale richiede sia schema sia authority ammessi, la presenza dello schema senza execution validation non è sufficiente.

## 6. Security, privacy, safety and operations

La projection pubblica è sanitizzata e vieta actor, rationale, edits, hostname, path locali, image data, credential e secret. Nessun file immagine o endpoint esterno è introdotto. L'authority resta read-only/human-only e `LOCAL_PHYSICAL_INTERLOCKS` rimane l'unica Safety Authority.

Il raw validator permissivo resta tuttavia un rischio di input-governance e resource bounding. Non costituisce una escalation di Safety Authority, ma deve essere corretto prima che future receipt siano considerate governate.

## 7. Decision

**REWORK REQUIRED.**

La PR #178 non deve essere merged né F5-A dichiarata accepted sul reviewed head. I sei workflow verdi dimostrano che l'implementazione soddisfa i test correnti; non annullano i probe negativi non coperti.

La decisione non modifica gli esiti scientifici o produttivi: scientific effectiveness resta `NOT_EVALUABLE_CURRENT_EVIDENCE`, production readiness resta `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false` e closure `KEEP_OPEN`.

## 8. Re-review criteria

La re-review richiede:

1. remediation di `ARB-F5A-M01` e `ARB-F5A-M02` con negative test;
2. disposition documentata di `ARB-F5A-C01`;
3. F5 governance e regressioni F2-F4 verdi sul nuovo exact head;
4. nessuna modifica materiale a cohort, authority, ownership, decision table o Safety boundary senza estendere il review scope;
5. nuova ARB/RQ sul remediation head;
6. autorizzazione al merge e disposizione branch-protection separate dopo esito favorevole.

## 9. Reproducible probes

I probe usano soltanto gli export del reviewed head:

```text
validateRawHumanDecisionSource(validAllowlistedPath, f2NonConformingReceipt) -> true
validateRealEvidenceEvaluation(reportWithWrongDirectoryAndWildcardPatternAndRecomputedDigest) -> true
```

Le shape concrete e i risultati sono descritti nei finding M01/M02. Nessun dato operativo o sensibile è stato utilizzato.

## 10. Traceability

- [F5 architecture](../scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md)
- [F5 validation plan](../validation/BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
- [F5-A implementation evidence](../validation/BKL-046-F5A-Evaluation-Foundation-Evidence-2026-09-12.md)
- [F5 architecture ARB](ARB-BKL-046-F5-AI-Assisted-Architecture-Review-2026-09-12.md)
- [PR #178](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/178)

