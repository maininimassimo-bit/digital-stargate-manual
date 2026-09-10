# Digital StarGate Current Technical Baseline — 10/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 10/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Main baseline di partenza | `42fe320f2c1e6b54edd2808b15d12bf2d3e94ae4` |
| Current governed package | BKL-037 — Session Comparison & Benchmarking |
| Next governed package | BKL-041 — Scientific Data Quality Score |

## 1. Accepted foundation

BKL-029, BKL-035 e BKL-045, dipendenze dichiarate di BKL-037, risultano accepted nel backlog/canonical roadmap. BKL-038 e BKL-039 sono anch'essi chiusi/accettati. BKL-045 closure è `docs/project/BKL-045-CLOSURE-2026-09-10.md`, PR #140 merge `a08aed981e5ffa4af6b68fea521ada25a4b2b338`.

## 2. BKL-037 comparison contract

BKL-037 è una capability di confronto read-only. I candidate comparison devono conservare dimensione, valore, unità, source, tempo/interval, quality, completeness, provenance e comparability classification. Il default deve restare fail-closed quando la comparabilità non è dimostrata.

Statistiche/benchmark sono descrittivi e non costituiscono acceptance threshold, ranking, quality score, SLA/SLO, raccomandazione o Safety Authority.

FWHM storico source-native non può essere reinterpretato automaticamente come arcsec senza provenance dell'unità/calibrazione. Missing evidence resta missing; provenance PixInsight `UNAVAILABLE`/`PARTIAL` non equivale ad assenza di processing.

## 3. Analytics baseline

La baseline include le correzioni integrate fino alla PR #151:

- Analytics Center dinamico e session-driven;
- configuration metadata propagation governata e fail-closed;
- Executive Dashboard coerente con history consolidata;
- weather full-window analytics dove disponibile;
- severity GREEN/YELLOW/RED governata per la vista analytics;
- consistency/idempotency gates.

Le dashboard sono projection/read model e non possono comandare apparati o assumere Safety Authority.

## 4. Authority / projection

- repository GitHub: source of truth;
- `docs/project/BACKLOG.md`: stato/priorità/dipendenze live;
- `.github/roadmap/roadmap-source.json`: canonical roadmap source;
- `docs/data/roadmap.json`: generated projection;
- closure/review/evidence/workflow: supporto delle acceptance claim sui rispettivi exact SHA.

## 5. Runtime e safety

Nessuna modifica EAGLE è richiesta per BKL-037. AP-013 resta authority per scientific asset identity/checksum/lifecycle; AP-014 resta boundary di catalogo/sincronizzazione dove applicabile. Local physical interlocks e Safety Authority restano indipendenti.

## 6. Entry condition per BKL-041

BKL-041 non deve diventare current finché BKL-037 non è formalmente CLOSED / ACCEPTED, con canonical backlog/roadmap transition integrata e quality gates/post-merge verification verificati sul repository.
