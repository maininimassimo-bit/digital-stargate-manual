# SOP - Retire Equipment

| Campo | Valore |
|---|---|
| SOP | Retire Equipment |
| Capability | CAP-003 Equipment Registry |
| Stato | Approved for capability baseline |
| Owner | Engineering Owner / Maintenance Owner / OPEN |

## Purpose

Definire il retirement governato di un asset, preservando storico, configurazioni, dipendenze e impatti operativi.

## Trigger

- Asset dismesso.
- Asset sostituito.
- Asset non piu sicuro o non piu compatibile.
- Decisione manutentiva o ingegneristica approvata.

## Preconditions

- Equipment record identificato.
- Assignment attivi verificati.
- Impatti su CAP-001, CAP-002, Safety and Maintenance valutati.

## Procedure

1. Identificare equipment record.
2. Verificare assignment attivi o futuri.
3. Informare capability consumatrici se necessario.
4. Registrare motivo retirement.
5. Registrare data e owner decisionale.
6. Aggiornare equipment state a `Retired`.
7. Aggiornare lifecycle state a `Retired`.
8. Rimuovere asset da disponibilita operativa.
9. Preservare configuration, firmware, driver, dependency and maintenance history.
10. Archiviare record storico.

## Outputs

- Retirement record.
- Archived historical evidence.
- Updated availability and dependency records.

## Controls

- Retirement non cancella storico.
- Asset retired non puo essere assegnato a schedule o sessione.
- Dipendenze verso altri asset devono essere valutate.

## Related Documents

- `../data-model.md`
- `../acceptance-criteria.md`
- `../traceability.md`
