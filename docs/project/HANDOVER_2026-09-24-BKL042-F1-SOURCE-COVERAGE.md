# Handover — BKL-042 F1 source coverage (24/09/2026)

## Stato

BKL-042 resta **IN PROGRESS** e non viene chiuso. L'OAT owner-witnessed v2 ha
superato la query M 27; Massimo Mainini ha richiesto esplicitamente l'estensione
delle altre fonti F1 eleggibili prima della formal acceptance.

Il metodo di retrieval v3 aggiunge due fonti governate già pubblicate:

- BKL-037 session comparison, soltanto storica e descrittiva;
- BKL-041 scientific data quality, soltanto `EXPERIMENTAL_NOT_ACCEPTED`, senza
  score o decomposizioni sintetiche.

L'evidence di dettaglio è
`docs/architecture/validation/BKL-042-F7-F1-SOURCE-COVERAGE-EVIDENCE-2026-09-24.md`.
I test locali sono 12/12 PASS e i replay read-only sulle projection statiche
pubbliche hanno risolto entrambi i percorsi di retrieval. Il metodo v3 non è ancora
stato deployato né provato con l'OAT autenticato owner-witnessed.

## Fonti residue e prossimo gate

Digital Twin, immagine/archive, PixInsight, Planner, Readiness e EAGLE non sono
aggiunti come fatti correnti perché le evidenze ispezionate sono fixture-only,
incomplete, scadute o `UNAVAILABLE`/`UNKNOWN`. Non reinterpretare questi stati come
healthy, ready, safe o completati; attendere projection eleggibile con freshness e
provenance risolte.

Le review AI-assisted ARB/RQ sull'implementation commit `8b89c048` sono registrate
nei rispettivi review record; non equivalgono ad approvazione umana indipendente.
Prossimo gate: controlli sul final PR head, poi merge/post-merge. Il deploy del relay
esistente richiede evidenza di necessità; nessun nuovo servizio o
promozione. Dopo l'eventuale deploy, richiedere a Massimo l'OAT autenticato v3 e la
formal acceptance. Fino ad allora mantenere `command_authority=NONE`,
`execution_authority=NONE`, `safety_authority=NONE` e `acceptance_authority=HUMAN_ONLY`.
