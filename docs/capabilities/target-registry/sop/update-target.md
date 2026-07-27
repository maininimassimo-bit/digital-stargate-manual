# SOP - Update Target

| Campo | Valore |
|---|---|
| SOP | Update Target |
| Capability | CAP-TGT-001 Target Registry |
| Stato | Approved for capability baseline |
| Owner | Science Owner / Knowledge Owner / OPEN |

## Purpose

Definire come aggiornare un target preservando identita, alias, coordinate, classificazione, vincoli e storico decisionale.

## Trigger

- Nuovo alias or catalogue reference.
- Correzione coordinate or epoch.
- Aggiornamento scientific classification.
- Cambio observation constraints, priority or visibility profile.
- Correzione metadata.

## Preconditions

- Target record identificato.
- Motivo dell'update noto.
- Impatto su CAP-SCH-001 or CAP-OSM-001 valutabile.

## Procedure

1. Identificare target record.
2. Registrare motivo e owner dell'update.
3. Conservare valore precedente or riferimento storico.
4. Aggiornare identity, catalogue reference, coordinates, classification, constraints or metadata.
5. Verificare se l'update crea duplicati potenziali.
6. Verificare se l'update invalida schedules or sessions future.
7. Se coordinate or identity cambiano, eseguire `validate-target.md`.
8. Se il target era `Published`, valutare ritorno a `Approved`, `Validated` or `Suspended`.
9. Informare CAP-SCH-001/CAP-OSM-001 se impattati.
10. Registrare storico minimo: chi, quando, cosa, perche, impatto.

## Outputs

- Updated Target record.
- Historical change evidence.
- Validation or recovery action if required.

## Controls

- Nessun cambio identity senza storico.
- Target con coordinate non verificate non resta schedulabile.
- Merge or override richiede evidenza auditabile.

## Related Documents

- `validate-target.md`
- `../runbooks/duplicate-target.md`
- `../runbooks/invalid-coordinates.md`
