# Digital StarGate Current Technical Baseline — 12/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 12/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Accepted main baseline | `46b956f0a6ceb04442ffd80447f810ef6463b5a8` |
| Current governed package | BKL-046 — AI Post-Processing Assistant for PixInsight |
| Current increment | BKL-046 F5-B — Atomic Update and Consumer candidate |
| Accepted predecessor | BKL-046 F5-A; F4; F3; F2; F1; BKL-041 closure; BKL-045; BKL-044; BKL-015 |

## 1. Accepted F5-A foundation

- canonical population: `docs/data/scientific-session-catalog.json`, 15 sessioni;
- accepted F4 projection: `docs/data/ai-post-processing-advisory-projection.json`;
- deterministic F5 policy: `BKL046-F5A-CLOSED-EVALUATION-1`;
- persisted evaluation: `docs/data/ai-post-processing-advisory-f5-evaluation.json`;
- closed cohort/gate/reason registry: `BKL046-F5A-CLOSED-REGISTRY-1`;
- authority: `READ_ONLY`, `HUMAN_ONLY`, action/execution `NONE`, Safety Authority locale.

## 2. Accepted identities and evidence

| Elemento | Valore |
|---|---|
| Authorized F5-A head | `74603bedad088dcf9f2cb33b9769658f4a9e639a` |
| Accepted merge | `46b956f0a6ceb04442ffd80447f810ef6463b5a8` |
| PR | #178 |
| ARB R2 | 98/100, approved with conditions |
| Release Quality | `CONDITIONALLY READY FOR MERGE` |
| Post-merge | 9/9 workflow `SUCCESS` |

Le review sono AI-assistite, owner-authorized e non equivalenti ad approvazioni umane indipendenti. La deroga `W-BKL046-F5A-MERGE-001` è consumata/scaduta.

## 3. Current observed dataset state

Il report F5-A `BKL046-F5A-F4FEB5E207DD3F7D3E4F6C87`, digest `174f8d75a27160b476c65d2670c50e4089811834dd1e5867418c77dfbac41f70`, contiene 15 sessioni canoniche, 0 provenance eligible, 0 Human Decision Receipt, 0 execution evidence e 2 source processing non correlate. L'efficacia scientifica resta `NOT_EVALUABLE_CURRENT_EVIDENCE`, la production readiness `NOT_READY_FOR_PRODUCTION` e la closure `KEEP_OPEN`.

## 4. F5-B candidate boundary

Il candidato estende il percorso automatico affinché F5 venga rigenerata e verificata dopo F4 sia al primo tentativo sia dopo il reset di retry. Il report F5 è incluso nel medesimo governed path set di catalogo/F4. Il consumer scarica i tre snapshot con `cache: no-store`, verifica contratti, authority, identity e digest, quindi mostra quattro outcome separati. Qualsiasi failure produce `EVALUATION UNAVAILABLE · FAIL-CLOSED`.

I gate persistiti `F5B_DYNAMIC_UPDATE` e `F5B_CONSUMER` restano `NOT_EXECUTED` finché F5-B non supera review e acceptance governata; il candidato non modifica retroattivamente il report F5-A.

## 5. Candidate validation state

Localmente sono verdi 28/28 test evaluator/workflow e 16/16 test consumer, oltre a generator `--check` e verifier. Sul technical head `f6555e80760f9c5d179df3dc0ee4e02c7e265a21` della PR #179 sono verdi 10/10 workflow. Publication-head CI, review ARB/RQ, merge e post-merge F5-B non sono ancora eseguiti.

## 6. Retained limitations

- processing history PixInsight reale incompleta o non correlabile resta unavailable;
- nessuna confidence scientifica, ground truth, calibrazione o production readiness;
- Recommendation, Human Decision Receipt ed execution evidence restano separate;
- nessun image upload/transfer, modello, provider, RAG/vector store o apply path;
- nessun comando apparato, remediation o modifica della Safety Authority.

## 7. Next governed action

Pubblicare il candidato F5-B su branch dedicato, ottenere exact-head CI e fermarsi per review ARB e Release Quality. Nessuna deroga o autorizzazione di F5-A si estende alla nuova PR.
