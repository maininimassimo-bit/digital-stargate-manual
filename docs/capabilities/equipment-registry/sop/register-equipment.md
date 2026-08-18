# SOP - Register Equipment

| Campo | Valore |
|---|---|
| SOP | Register Equipment |
| Capability | CAP-003 Equipment Registry |
| Stato | Approved for capability baseline |
| Owner | Engineering Owner / OPEN |

## Purpose

Definire la procedura per registrare un asset fisico o logico nel registry autorevole.

## Trigger

- Nuovo equipment installato o previsto.
- Nuovo firmware, driver or logical equipment group da censire.
- Asset esistente non ancora registrato.

## Preconditions

- Identita minima disponibile.
- Tipo equipment noto o classificabile.
- Owner iniziale identificato o marcato `OPEN`.

## Procedure

1. Assegnare o registrare identificatore equipment.
2. Definire equipment type.
3. Registrare owner e location.
4. Registrare configuration baseline se disponibile.
5. Collegare firmware, driver e dependencies se applicabili.
6. Indicare criticality e safety relevance.
7. Impostare lifecycle state `Registered`.
8. Impostare equipment state `Registered` o `Unknown` se verifica non completata.
9. Registrare note e fonte documentale.
10. Pianificare verification prima dell'uso operativo.

## Outputs

- Equipment record.
- Initial configuration reference.
- Verification action pending when needed.

## Controls

- Non marcare asset `Available` durante la registrazione.
- Non registrare segreti o credenziali.
- Non usare vendor-specific implementation assumptions.

## Related Documents

- `../data-model.md`
- `verify-equipment.md`
- `../adr/EQR-ADR-001-authoritative-registry.md`
