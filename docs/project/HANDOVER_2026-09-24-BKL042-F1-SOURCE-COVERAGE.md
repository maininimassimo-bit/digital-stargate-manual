# Handover — BKL-042 F1 source coverage (24/09/2026)

## Stato

BKL-042 resta **IN PROGRESS** e non viene chiuso. L'OAT owner-witnessed v2 ha
superato la query M 27; Massimo Mainini ha richiesto esplicitamente l'estensione
delle altre fonti F1 eleggibili prima della formal acceptance. L'incremento F7 è
stato integrato in `main` tramite PR #360, merge
`6e6cf43fdf7d29d67d4800541049a4acdf7f42ee`.

Il metodo di retrieval v3 aggiunge due fonti governate già pubblicate:

- BKL-037 session comparison, soltanto storica e descrittiva;
- BKL-041 scientific data quality, soltanto `EXPERIMENTAL_NOT_ACCEPTED`, senza
  score o decomposizioni sintetiche.

L'evidence di dettaglio è
`docs/architecture/validation/BKL-042-F7-F1-SOURCE-COVERAGE-EVIDENCE-2026-09-24.md`.
I test locali sono 12/12 PASS e i replay read-only sulle projection statiche
pubbliche hanno risolto entrambi i percorsi di retrieval. Final-head e tutti i
workflow post-merge applicabili sono PASS; i relativi run ID sono nel documento
evidence F7. Metodo v3 è ora sul relay esistente, revisione `00008-qat`, traffico
100%, massimo istanze 1. Rollback `00007-wrm`; l'evidence di deploy è
`docs/architecture/validation/BKL-042-F7-V3-DEPLOYMENT-EVIDENCE-2026-09-24.md`.
L'OAT autenticato owner-witnessed v3 è ancora da eseguire.

## Fonti residue e prossimo gate

Digital Twin, immagine/archive, PixInsight, Planner, Readiness e EAGLE non sono
aggiunti come fatti correnti perché le evidenze ispezionate sono fixture-only,
incomplete, scadute o `UNAVAILABLE`/`UNKNOWN`. Non reinterpretare questi stati come
healthy, ready, safe o completati; attendere projection eleggibile con freshness e
provenance risolte.

Le review AI-assisted ARB/RQ sull'implementation commit `8b89c048` sono registrate
nei rispettivi review record; non equivalgono ad approvazione umana indipendente.
Prossimo gate: Massimo esegue/witnessa l'OAT autenticato v3 dal portale, verificando
separatamente il recupero del confronto SQM BKL-037 e il contesto qualità BKL-041
`EXPERIMENTAL_NOT_ACCEPTED` senza punteggi sintetici; poi fornisce la formal
acceptance separata. Fino ad allora mantenere `command_authority=NONE`,
`execution_authority=NONE`, `safety_authority=NONE` e `acceptance_authority=HUMAN_ONLY`.
