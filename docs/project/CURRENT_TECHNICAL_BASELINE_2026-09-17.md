# Digital StarGate — Current Technical Baseline 17/09/2026

| Campo | Valore |
|---|---|
| Stato | Current governed baseline |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| BKL-031 closure merge | `4a509d574a004fe7fb72bc6c678c9e7f71fe821f` |
| Closure record | `docs/project/BKL-031-CLOSURE-2026-09-18.md` |
| BKL-032 closure | PR #304; merge `7e38453b2e499fe577efa0231aeb7bb06329016e` |
| Current package | BKL-036 |
| Current next gate | BKL-036 follow-on source mapping and policy gate |

## Observation Planner baseline

BKL-031 F3–F9 è Closed / Accepted / Post-Merge Verified. F9 chiude la pipeline repeatable: forecast MeteoHub corrente di Manciano, geometria astronomica della notte, suitability esplicita setup-target e ranking/finestre advisory nel portale. Il metodo resta `EVALUATION/NONE/READ_ONLY` e non è un readiness/safety engine.

## Authority baseline

- Site Authority: protected GitHub-governed record; coordinate esatte non pubblicabili.
- Setup Authority: approved GitHub-governed assignment/baseline.
- Ephemeris/lunar method: ADR-010 accepted repository authority.
- Forecast source/run lineage: ADR-011 accepted repository authority.
- F9 operating model: ADR-012, EUR 0, nessun limite giornaliero imposto dal workflow, fail-closed e GRIB effimeri.
- Session Readiness / Go-No-Go: **BKL-032 Session Readiness / Go-No-Go Decision Support**, closed as deterministic read-only decision support; live source/transport remains separately gated.
- Safety Authority: local physical interlocks.
- S10 production runtime: `UNAVAILABLE`.

## Closure evidence

PR #301 merged with governance, documentation validation, Word generation and GitHub Pages deployment SUCCESS. La verifica web diretta ha confermato il planner pubblico di Manciano con forecast corrente, 16 campioni notturni, setup/filtri/ranking e correzione percentuali. Predecessor F8 reconciliation: reviewed head `bca410dcde804483052beded16c29a9f58f43872`, merge `84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4`, 19/19 applicable post-merge workflows SUCCESS.

## Maintained limits

Il Planner resta advisory/read-only: nessun readiness/go-no-go, scheduler, selezione automatica, device command o Safety Authority. Nessun GRIB o coordinata protetta è pubblicato. Missing, stale, incompleto o incoerente evidence fallisce chiuso.

BKL-032 closure evidence is recorded in `docs/project/BKL-032-CLOSURE-2026-09-18.md`. Its evaluator does not authorize live apparatus operation or replace local interlocks.

## BKL-036 closure state

BKL-036 source-discovery gate è **Closed / Accepted / Post-Merge Verified** tramite PR #306 e merge `b0d3a8b1a10ce71610e4592d5c876e9fd0c8d7c5`; la capability BKL-036 resta corrente per follow-on separatamente governati. Non introduce score numerico, soglie, pesi, RAG, Safety Score, remediation, runtime transport o comandi. Source mapping, comparabilità e qualunque futuro score restano gate separati.
