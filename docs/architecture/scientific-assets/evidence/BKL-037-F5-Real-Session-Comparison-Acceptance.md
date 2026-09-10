# BKL-037 F5 — Real Session Comparison Acceptance Evidence

| Campo | Valore |
|---|---|
| Evidence ID | BKL-037-F5-E01 |
| Data | 10/09/2026 |
| Baseline F4 | `2e58d440b78e2c5c6d2f2c5978ccdf738c8674c3` |
| Dimensione | SQM median |
| Unità | `mag/arcsec2` |
| Authority | Evidence only / READ_ONLY |

## Evidenza sorgente

La prova usa esclusivamente sessioni reali già governate nel repository:

1. `2026-09-05_2026-09-06` — `sqm.median_mag_arcsec2 = 20.57`, quality `AVAILABLE`, 1301 campioni validi, coverage `0.9849`, source `AAG CloudWatcher SOLO HTTP / lightmpsas`;
2. `2026-09-07_2026-09-08` — `sqm.median_mag_arcsec2 = 20.89`, quality `AVAILABLE`, 1283 campioni validi, coverage `0.9712`, stessa source e stessa unità.

I locator autoritativi sono i rispettivi `normalized/session-metrics.json`, che referenziano a loro volta `raw/sqm/sqm-summary.json`.

## Risultato F2/F3

Le due osservazioni sono una cohort comparabile per la stessa dimensione `SQM_MEDIAN`, stessa unità e stessa source semantics. La projection persistita `docs/data/session-comparison-projection.json` espone:

- sample size `2`;
- minimum `20.57`;
- maximum `20.89`;
- mean `20.73`;
- median `20.73`;
- range `0.32`.

Le statistiche sono esclusivamente descrittive e non costituiscono ranking, score, target o soglia di accettazione.

## Verifica consumer F4

Il consumer F4 legge esclusivamente `/data/session-comparison-projection.json` e verifica prima del rendering:

- `projectionType = SESSION_COMPARISON_PROJECTION`;
- `consumerMode = READ_ONLY`;
- `acceptanceAuthority = false`;
- `actionAuthority = NONE`.

La projection F5 soddisfa questi vincoli e mantiene `includedSessions`, `exclusions`, `limitations` e provenance refs. Il browser non calcola nuove statistiche e non modifica il payload.

## Limiti della prova

Questa evidence dimostra il percorso repository-side `real session metrics -> governed comparison projection -> read-only portal contract`. La build MkDocs/Pages costituisce la verifica di integrazione statica del consumer; non viene dichiarata una prova manuale del rendering su browser o hardware.

La prova non autorizza comandi runtime, non modifica AP-013/AP-014 e non ha alcun ruolo nella Safety Authority.

## Esito

**PASS — repository-side end-to-end acceptance evidence**, subordinato ai gate CI exact-head e post-merge della PR F5.
