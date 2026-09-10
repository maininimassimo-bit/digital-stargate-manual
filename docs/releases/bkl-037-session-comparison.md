# BKL-037 — Session Comparison & Benchmarking — Release Note

| Campo | Valore |
|---|---|
| Identificativo | DSG-REL-BKL-037 |
| Data | 10/09/2026 |
| Stato | Release candidate — pending transition merge |
| Capability | BKL-037 — Session Comparison & Benchmarking |
| Successor | BKL-041 — Scientific Data Quality Score |

## Outcome

BKL-037 introduce una comparison projection multi-sessione deterministica e read-only, alimentata dal catalogo scientifico governato.

Alla closure:

- 15 sessioni catalogate;
- 8 sessioni SQM-comparabili;
- 7 exclusions fail-closed;
- statistiche descrittive: sample size, minimum, maximum, mean, median e range;
- portal consumer senza analytics autonoma.

## Compatibility

La modifica è additive e repository/Pages-only. Nessun contratto operativo o device command cambia. Le sessioni prive di evidence compatibile restano escluse esplicitamente.

## Authority and safety

BKL-037 non introduce quality score, ranking, threshold, automatic acceptance, recommendation, remediation o Safety Authority. Gli interlock locali restano indipendenti.

## Migration and rollback

Nessuna migrazione runtime. Rollback mediante revert del transition package e delle projection generate.

## Next

BKL-041 F1 definirà il semantic contract dello Scientific Data Quality Score prima di qualunque algoritmo o consumer.
