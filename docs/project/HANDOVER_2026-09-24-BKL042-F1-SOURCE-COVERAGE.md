# Handover — BKL-042 F1 source coverage (24/09/2026)

## Stato

BKL-042 F7 è **ACCEPTED / BOUNDED GATE / OWNER-WITNESSED**. L'OAT owner-witnessed v2
aveva superato la query M 27; dopo l'estensione F1 e l'OAT v3, Massimo Mainini ha
formalmente accettato F7 nel perimetro bounded read-only, inclusi i limiti
documentati. L'incremento F7 è
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
L'OAT v3 è PASS con limiti accettati: il confronto SQM è aggregato e non contiene
misure per singola sessione; i record M 27 BKL-041 restano sperimentali, sintetici
e non calibrati. I correlation ID e l'acceptance owner sono in
`docs/project/BKL-042-F7-BOUNDED-ACCEPTANCE-2026-09-24.md`.

## Fonti residue e prossimo gate

Digital Twin, immagine/archive, PixInsight, Planner, Readiness e EAGLE non sono
aggiunti come fatti correnti perché le evidenze ispezionate sono fixture-only,
incomplete, scadute o `UNAVAILABLE`/`UNKNOWN`. Non reinterpretare questi stati come
healthy, ready, safe o completati; attendere projection eleggibile con freshness e
provenance risolte.

Le review AI-assisted ARB/RQ sull'implementation commit `8b89c048` sono registrate
nei rispettivi review record; non equivalgono ad approvazione umana indipendente.
Nessun gate runtime ulteriore è autorizzato o necessario per l'acceptance F7.
Eventuali future estensioni alle classi escluse richiederanno nuove projection e
una decisione separata. Mantenere `command_authority=NONE`,
`execution_authority=NONE`, `safety_authority=NONE` e `acceptance_authority=HUMAN_ONLY`.
