# SOP - Update Equipment

| Campo | Valore |
|---|---|
| SOP | Update Equipment |
| Capability | CAP-003 Equipment Registry |
| Stato | Approved for capability baseline |
| Owner | Engineering Owner / OPEN |

## Purpose

Definire come aggiornare un equipment record mantenendo storico, tracciabilita e impatto operativo.

## Trigger

- Cambio configurazione.
- Aggiornamento firmware o driver.
- Cambio location, owner, dependency or logical group.
- Cambio stato operativo o health status.
- Correzione di un record errato.

## Preconditions

- Equipment record identificato.
- Motivo dell'update noto.
- Impatto su CAP-001, CAP-002, Safety or Maintenance valutabile.

## Procedure

1. Identificare equipment record.
2. Registrare motivo e owner dell'update.
3. Conservare valore precedente o riferimento storico.
4. Aggiornare configuration, firmware, driver, location, dependency or state.
5. Valutare impatto su assignment attivi.
6. Se impatta availability, aggiornare equipment state.
7. Se impatta safety, informare Observatory Safety.
8. Se impatta scheduling o sessione, aggiornare riferimenti CAP-002/CAP-001.
9. Richiedere verification se il cambio modifica configurazione operativa.
10. Registrare storico minimo: chi, quando, cosa, perche, impatto.

## Outputs

- Updated equipment record.
- Historical change evidence.
- Verification or recovery action if required.

## Controls

- Nessun cambio operativo senza storico.
- Asset con configurazione non verificata non resta `Available`.
- Safety-critical update richiede evidenza di impatto.

## Related Documents

- `verify-equipment.md`
- `../runbooks/configuration-mismatch.md`
- `../traceability.md`
