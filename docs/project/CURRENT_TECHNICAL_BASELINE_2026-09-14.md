# Digital StarGate — Current Technical Baseline 14/09/2026

| Campo | Valore |
|---|---|
| Stato | Active |
| Repository baseline osservata | `e674cdb601fd15582a2d5ce0c39dc8f009e5b9cc` |
| Current governed package | BKL-031 F2 — handoff only |
| Accepted predecessor | BKL-031 F1 |
| F2 implementation | **NOT AUTHORIZED** |
| Runtime impact | None |

## 1. Accepted foundation

BKL-015, BKL-044, BKL-035, BKL-040, BKL-038, BKL-039, BKL-045, BKL-037, BKL-041 e BKL-046 restano accepted nei rispettivi boundary documentati.

BKL-031 F1 è ACCEPTED / POST-MERGE VERIFIED tramite PR #183 e merge `b14d9cdd991b5eef74dd9b972958e74c5903a32d`.

## 2. Current BKL-031 boundary

F2 è promosso come prossimo incremento governato per un futuro contratto machine-readable source/context con fixture bounded e validazione fail-closed. Lo stato current non autorizza l'implementazione.

S07–S11 restano unavailable/unknown sulla baseline corrente. Nessuna source storica o projection può essere presentata come sito corrente, setup attivo, ephemeris/lunar, forecast o stato realtime.

## 3. Preserved invariants

- repository e contratti governati restano authority;
- projection non diventa authority;
- Citation, Provenance, identity, freshness, missingness e conflict sono preservati;
- BKL-031 advisory resta separato da BKL-032 readiness;
- local physical interlocks restano l'unica Safety Authority;
- workload pesante e chiamate esterne restano fuori da EAGLE.

## 4. Explicit exclusions

Nessun schema, fixture, validator, algoritmo, peso, score, soglia, ranking, scheduler, go/no-go, provider, device command o runtime change F2 è autorizzato da questa baseline.

## 5. Operational baseline

La sessione `2026-09-13_2026-09-14` è presente e rielaborata con RMS PHD2 canonico totale `1.414 arcsec` nel commit analytics `e674cdb601fd15582a2d5ce0c39dc8f009e5b9cc`. L'evidenza operativa resta separata dalla transizione documentale BKL-031.

## 6. Next gate

Nuova autorizzazione owner per preparare F2. La futura delivery dovrà fermarsi prima di review e merge, che restano gate separati.
