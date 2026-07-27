# SOP - Retire Target

| Campo | Valore |
|---|---|
| SOP | Retire Target |
| Capability | CAP-TGT-001 Target Registry |
| Stato | Approved for capability baseline |
| Owner | Science Owner / Data Owner / OPEN |

## Purpose

Definire il retirement governato di un target, preservando identita, alias, riferimenti catalogo and observation history.

## Trigger

- Target non piu osservabile or non piu rilevante per il programma.
- Target duplicato consolidato in altra identita canonica.
- Target custom non piu valido.
- Decisione scientifica o operativa approvata.

## Preconditions

- Target record identificato.
- Schedules future e sessioni correlate verificate.
- Observation history references valutate.

## Procedure

1. Identificare target record.
2. Verificare schedules future in CAP-SCH-001.
3. Verificare session history in CAP-OSM-001/Data Platform.
4. Registrare motivo retirement.
5. Registrare owner decisionale.
6. Aggiornare lifecycle state a `Retired`.
7. Rimuovere target da nuove pubblicazioni/scheduling.
8. Preservare canonical identity, aliases, catalogue references and observation history.
9. Se il target e duplicato, collegare target canonico sostitutivo quando approvato.
10. Archiviare retirement evidence.

## Outputs

- Retirement record.
- Archived target evidence.
- Updated scheduling availability.

## Controls

- Retirement non cancella observation history.
- Target retired non puo essere usato per nuove schedule.
- Merge/duplicate retirement richiede evidenza auditabile.

## Related Documents

- `../data-model.md`
- `../acceptance-criteria.md`
- `../traceability.md`
