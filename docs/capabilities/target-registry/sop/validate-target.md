# SOP - Validate Target

| Campo | Valore |
|---|---|
| SOP | Validate Target |
| Capability | CAP-TGT-001 Target Registry |
| Stato | Approved for capability baseline |
| Owner | Science Owner / OPEN |

## Purpose

Definire la verifica target prima della pubblicazione per scheduling, session management and scientific traceability.

## Trigger

- Nuova registrazione.
- Cambio identity, catalogue reference or coordinates.
- Duplicate or unresolved identifier finding.
- Richiesta di pubblicazione target.

## Preconditions

- Target record esistente.
- Dati minimi disponibili: identity candidate, type and coordinates/ephemeris reference where applicable.

## Procedure

1. Verificare canonical identity candidate.
2. Verificare alias and catalogue references.
3. Cercare duplicati potenziali.
4. Verificare coordinates, epoch and coordinate system where applicable.
5. Verificare target type and scientific classification.
6. Verificare constraints and visibility profile if needed for scheduling.
7. Se duplicate risk exists, applicare `duplicate-target.md`.
8. Se identifier unresolved, applicare `unresolved-identifier.md`.
9. Se coordinates invalid, applicare `invalid-coordinates.md`.
10. Se verifica positiva, impostare state `Validated` or `Approved` secondo decisione owner.
11. Pubblicare solo dopo approvazione.

## Outputs

- Validation evidence.
- Updated lifecycle state.
- Recovery action if needed.

## Controls

- Target invalidi non sono pubblicati.
- Catalogue references non sostituiscono canonical identity.
- Moving targets richiedono metadata/ephemeris evidence sufficienti per uso previsto.

## Related Documents

- `../adr/TGT-ADR-002-canonical-target-identity.md`
- `../runbooks/duplicate-target.md`
- `../runbooks/unresolved-identifier.md`
- `../runbooks/invalid-coordinates.md`
