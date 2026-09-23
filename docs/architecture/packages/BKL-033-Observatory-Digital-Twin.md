# BKL-033 — Observatory Digital Twin

| Campo | Valore |
|---|---|
| Identificativo | `BKL-033` |
| Stato | CLOSED / ACCEPTED / POST-MERGE VERIFIED |
| Versione | 1.0 |
| Data | 23/09/2026 |
| Predecessore | AP-015 / CAP-40 semantic contract |
| Owner | Massimo Mainini |

## Scopo

Definire una rappresentazione bounded, descrittiva e read-only degli asset dell’osservatorio e delle loro dipendenze. Il Digital Twin è una projection navigabile: non è un digital control system, non calcola readiness e non autorizza azioni.

## Modello

- `TwinNode`: asset o projection identificata, source authority, lifecycle e stato osservato;
- `TwinDependency`: relazione direzionale tipizzata tra nodi, con evidence e freshness class;
- `ObservationRef`: riferimento a telemetry/catalog evidence, mai comando;
- `ProjectionBoundary`: authority `projection`, `commandAuthority=NONE`, `safetyAuthority=NONE`.

Il contract è `schemas/bkl033-digital-twin-contract.schema.json`; la fixture bounded è `docs/data/bkl033-digital-twin-fixture.json`.

## Invarianti

- source authority resta presso Catalog, EAGLE/telemetry, configuration baseline o GitHub;
- stato `observed`, `stale`, `unknown` e `unavailable` è esplicito;
- una dipendenza mancante non diventa healthy, ready o safe per inferenza;
- il modello non espone write path, command, remediation, scheduler o interlock override;
- nessun ranking, go/no-go o Safety Authority è derivato dal grafo.

## Acceptance

`.github/scripts/verify-bkl033-digital-twin.mjs` valida schema, fixture, riferimenti, freshness classification e boundary. Il package è chiuso a livello di contract/design; UI, ingestione runtime e materializzazione tecnologica sono successori separati.
