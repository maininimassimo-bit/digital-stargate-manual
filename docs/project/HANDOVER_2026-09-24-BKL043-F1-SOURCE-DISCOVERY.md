# Handover — BKL-043 F1 source discovery (24/09/2026)

## 1. Stato e obiettivo raggiunto

BKL-042 è ACCEPTED entro il perimetro bounded read-only dopo OAT owner-witnessed e
formal acceptance di Massimo Mainini. BKL-043 è la milestone corrente; completata la
prima ricognizione repository-only delle fonti per l'affidabilità. Non è disponibile
una baseline operativa eleggibile per availability, fault frequency, MTBF, MTTR,
completion rate o failure budget; non è stato definito alcun SLI/SLO numerico.

## 2. Repository e stato Git

- Repository autorevole: `maininimassimo-bit/digital-stargate-manual`.
- Branch di integrazione: `main`.
- Head post-merge verificato: `a483410c33e825419a969508df7d0ed4db7161ff`.
- Incremento: PR #364, merge commit `a483410c33e825419a969508df7d0ed4db7161ff`.

## 3. Owner e responsabilità

Owner/accountable: Massimo Mainini. Acceptance e ogni decisione su soglie,
strumentazione live o semantica operativa restano `HUMAN_ONLY`.

## 4. Perimetro completato

- Registrata closure di BKL-042 e spostata la roadmap su BKL-043.
- Inventariate le fonti repository senza trasformare dati storici, fixture sintetiche,
  stati `UNKNOWN` o incidenti CI in misure operative dell'osservatorio.
- Evidenza: `docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md`.
- Limiti OAT BKL-042: `docs/project/BKL-042-F7-BOUNDED-ACCEPTANCE-2026-09-24.md`.

## 5. Modifiche principali

Closure BKL-042, evidenza F1 BKL-043, roadmap e proiezioni rigenerate, backlog,
baseline tecnica, handover e verificatori di coerenza legacy aggiornati. Nessuna ADR
nuova; AP-004/AP-007 e OPSC-ALM-001 restano i riferimenti applicabili.

## 6. Validazione locale

Superati `python -m mkdocs build --strict`, generazione/check roadmap e Scientific
Platform, `verify-roadmap-consistency.mjs`, tutti i verificatori
`verify-observation-planner-*.mjs` e `git diff --check`.

## 7. Workflow exact-head e post-merge

PR #364, head `0b736176b91688d2c6f5b5d4bb15da8e394fc5ef`: tutti i 14 check esatti
sono `SUCCESS`. Sul merge SHA `a483410c33e825419a969508df7d0ed4db7161ff`, tutti i 15
workflow sono `SUCCESS`, compresi Developer Foundation (`35991908692`), Validate
documentation (`35991908978`), Deploy MkDocs artifact to GitHub Pages
(`35991909029`), Governed Projection Sync (`35991909137`), Scientific Platform
Governance (`35991908842`) e Genera manuale Word (`35991908841`).

## 8. Limiti e rischi residui

Nessuna misura di uptime, incident rate, MTBF, MTTR, session-success population,
freshness rate o failure budget è affermata. SLI/SLO numerici richiedono baseline
misurata e deliberazione AP-007. Non modificati runtime Cloud Run, hardware, live
writer, alert routing, command path o policy di sicurezza. Autorità mantenute:
`command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE`.

## 9. Prossimo gate

Continuare BKL-043 con definizione repository-only di popolazioni, eventi e qualità
delle fonti. Fermarsi prima di soglie numeriche, raccolta live, alert routing o
interpretazioni di safety/readiness per la review/decisione applicabile. BKL-050
resta l'ultima milestone approvata, dopo i package precedenti ancora aperti.
