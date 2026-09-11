# BKL-046 F1 — Acceptance Record

| Campo | Valore |
|---|---|
| Increment | BKL-046 F1 — Source Discovery and Advisory Semantic Contract |
| Stato | CLOSED / ACCEPTED / POST-MERGE PAGES VERIFIED |
| Data | 11/09/2026 |
| Pull request | #165 |
| Accepted merge | `3f2e3edae93b009f5800a58a4ac5afc4f04e9bb7` |
| Exact reviewed head | `4540a1f96d28d46f31bf152a5df44ce4c931d17b` |
| Successor | BKL-046 F2 — Machine-Readable Recommendation and Human Decision Contracts |

## 1. Acceptance decision

BKL-046 F1 è accettato come baseline architetturale dell'AI Post-Processing Assistant per PixInsight. L'incremento definisce source eligibility, Recommendation, rationale, confidence, human decision, execution-evidence separation, missingness, authority, privacy, safety e roadmap F2–F5.

L'acceptance è esclusivamente documentale e architetturale. Non dichiara implementati un modello, provider, runtime AI, RAG/vector store, recommendation engine, image upload, PixInsight apply path o capability produttiva.

## 2. Verified evidence

- exact-head CI della PR: 7/7 workflow successful;
- Architecture Review Board: `APPROVED`, 99/100, nessun Blocker/Major/Minor;
- Release Quality: `READY FOR MERGE`, nessun waiver;
- protected merge PR #165: `3f2e3edae93b009f5800a58a4ac5afc4f04e9bb7`;
- pagina F1 e report Release Quality pubblicati e leggibili sul portale dopo il merge;
- ricerca live verificata con query `BKL-046`, inclusa la pagina di assessment F1.

La verifica live dimostra la pubblicazione del contenuto integrato. Gli identificativi dei run `push` post-merge non sono esposti dal connettore disponibile e non vengono inventati.

## 3. Accepted boundaries

- Recommendation resta advisory e non è Evidence, osservazione, decisione umana o esecuzione;
- `OBSERVED`, `DECLARED` e `SUGGESTED` restano distinti;
- provenance `UNAVAILABLE/PARTIAL` non viene ricostruita;
- BKL-041 resta contesto sperimentale, mai ground truth o production signal;
- user approval non prova execution;
- AP-013/AP-014 e BKL-044/BKL-045 mantengono la propria authority;
- nessun device command, automatic acceptance, remediation non presidiata o Safety Authority.

## 4. Dynamic update boundary

La canonical roadmap resta `.github/roadmap/roadmap-source.json`. Le proiezioni del portale `docs/data/roadmap.json` e `docs/data/scientific-platform-status.json` sono state rigenerate dal workflow governato sulla feature branch. La pipeline di import delle sessioni scientifiche e i consumer esistenti non vengono modificati da F1.

F2 dovrà mantenere la stessa separazione authority/projection e introdurre soltanto contratti machine-readable e fixture bounded. Eventuali consumer dinamici successivi dovranno essere collegati alla pipeline automatica di import prima dell'acceptance.

## 5. Retained limitations

- complete PixInsight process history remains unavailable nella real evidence BKL-045;
- nessun metodo di recommendation quality o confidence calibration è accettato;
- provider/runtime placement, privacy threat model ed evaluation dataset restano open issues;
- `ASSISTED APPLY` resta fuori scope e richiede nuova architecture/security review.

## 6. Transition

F2 è dependency-ready per definire:

1. closed versioned Recommendation envelope;
2. separate Human Decision Receipt;
3. bounded synthetic fixtures;
4. deterministic validator e negative tests;
5. producer/method/version, provenance, limitation e authority invariants.

F2 non seleziona un modello/provider e non autorizza l'esecuzione PixInsight.
