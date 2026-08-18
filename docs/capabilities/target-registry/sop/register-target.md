# SOP - Register Target

| Campo | Valore |
|---|---|
| SOP | Register Target |
| Capability | CAP-TGT-001 Target Registry |
| Stato | Approved for capability baseline |
| Owner | Science Owner / OPEN |

## Purpose

Definire la procedura per registrare un target candidato nel Target Registry.

## Trigger

- Nuovo target scientifico o operativo.
- Nuova Observation Request con target non ancora presente.
- Custom target da gestire internamente.

## Preconditions

- Nome, designazione or descrizione minima disponibile.
- Fonte iniziale documentabile.
- Owner iniziale identificato or marcato `OPEN`.

## Procedure

1. Creare Target record in stato `Proposed`.
2. Registrare proposed name and source.
3. Indicare target type presunto se noto.
4. Registrare catalogue reference se disponibile.
5. Registrare coordinates, epoch or ephemeris reference se disponibile.
6. Registrare metadata and notes.
7. Valutare potenziali duplicati.
8. Collegare Observation Request se applicabile.
9. Impostare identity status `Identity Pending` finche non validato.
10. Avviare SOP `validate-target.md` prima della pubblicazione.

## Outputs

- Proposed Target record.
- Initial metadata and reference evidence.
- Validation action pending.

## Controls

- Non pubblicare target durante la registrazione.
- Non usare catalogue reference come unico internal authority.
- Non introdurre dati sensibili non necessari.

## Related Documents

- `../data-model.md`
- `validate-target.md`
- `../adr/TGT-ADR-001-authoritative-target-model.md`
