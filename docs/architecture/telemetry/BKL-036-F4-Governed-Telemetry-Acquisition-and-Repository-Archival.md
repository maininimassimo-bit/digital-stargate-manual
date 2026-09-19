# BKL-036-F4 — Governed Telemetry Acquisition and Repository Archival

| Campo | Valore |
|---|---|
| Identifier | BKL-036-F4 |
| Status | Implementation candidate |
| Version | 0.1 |
| Parent | BKL-036 — Observatory Health Score |
| Upstream | F1 source mapping, F2 evidence envelope, F3 archived score |
| Authority | Repository evidence only |
| Runtime impact | None in this increment |
| Safety Authority | No change |

## Purpose

F4 definisce il primo passaggio controllato per rendere archiviabile una snapshot telemetry proveniente dalla cupola, preservando la separazione tra acquisizione, evidence repository e runtime.

## Processing contract

Il comando .github/scripts/archive-bkl-036-f4-telemetry.mjs:

1. legge un file JSON già disponibile nel workspace;
2. valida il contratto F4;
3. forza la classificazione dell'output a repository_archived_snapshot;
4. scrive un archivio deterministico;
5. non effettua richieste di rete e non interagisce con EAGLE, CloudWatcher, dome, mount, camera o power.

L'input reale della cupola potrà essere collegato solo da un successivo runtime gate con source authority, retention, autenticazione e failure handling approvati.

## Evidence states

PRESENT richiede timestamp di osservazione e freshness. MISSING, STALE, UNAVAILABLE, PARTIAL e CONFLICTING restano fail-closed e non comparabili. F4 non assegna punteggi e non modifica soglie.

## Data boundary

Il payload è limitato a dati osservativi e metadati di provenienza. Sono esclusi password, token, chiavi, dati personali, comandi, remediation, decisioni readiness e Safety Authority.

## Validation

- schema: contracts/telemetry/bkl-036-f4-archived-telemetry-v1.schema.json;
- validator: .github/scripts/verify-bkl-036-f4-archived-telemetry.mjs;
- archive command: .github/scripts/archive-bkl-036-f4-telemetry.mjs;
- bounded tests: .github/scripts/test-bkl-036-f4-archived-telemetry.mjs.

## Non-goals

F4 non implementa consumer live, relay, scheduling, comandi, remediation, interlock software, score operativo o integrazione automatica con EAGLE/CloudWatcher.
