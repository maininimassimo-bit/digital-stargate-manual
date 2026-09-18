# Digital StarGate — Current Technical Baseline 17/09/2026

| Campo | Valore |
|---|---|
| Stato | Current governed baseline |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| BKL-031 closure merge | `dee6f117c964db92f152e3b7d924d7fedb66e093` |
| Closure record | `docs/project/BKL-031-CLOSURE-2026-09-18.md` |
| Current package | BKL-032 |
| Current next gate | BKL-032 Session Readiness / Go-No-Go Decision Support |

## Observation Planner baseline

BKL-031 F3–F9 è Closed / Accepted / Post-Merge Verified. F9 chiude la pipeline repeatable: forecast MeteoHub corrente di Manciano, geometria astronomica della notte, suitability esplicita setup-target e ranking/finestre advisory nel portale. Il metodo resta `EVALUATION/NONE/READ_ONLY` e non è un readiness/safety engine.

## Authority baseline

- Site Authority: protected GitHub-governed record; coordinate esatte non pubblicabili.
- Setup Authority: approved GitHub-governed assignment/baseline.
- Ephemeris/lunar method: ADR-010 accepted repository authority.
- Forecast source/run lineage: ADR-011 accepted repository authority.
- F9 operating model: ADR-012, EUR 0, massimo due acquisizioni UTC/giorno, fail-closed e GRIB effimeri.
- Session Readiness / Go-No-Go: BKL-032, non BKL-031.
- Safety Authority: local physical interlocks.
- S10 production runtime: `UNAVAILABLE`.

## Closure evidence

PR #300 merged with governance, documentation validation, Word generation and GitHub Pages deployment SUCCESS. La verifica web diretta ha confermato il planner pubblico di Manciano con forecast corrente, 16 campioni notturni, setup/filtri/ranking e correzione percentuali.

## Maintained limits

Il Planner resta advisory/read-only: nessun readiness/go-no-go, scheduler, selezione automatica, device command o Safety Authority. Nessun GRIB o coordinata protetta è pubblicato. Missing, stale, incompleto o incoerente evidence fallisce chiuso.
