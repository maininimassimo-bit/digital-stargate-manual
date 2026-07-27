# SOP - Verify Equipment

| Campo | Valore |
|---|---|
| SOP | Verify Equipment |
| Capability | CAP-003 Equipment Registry |
| Stato | Approved for capability baseline |
| Owner | Engineering Owner / Operations Owner / OPEN |

## Purpose

Definire la verifica equipment prima che un asset venga considerato disponibile per scheduling, session management o safety-dependent operations.

## Trigger

- Nuova registrazione.
- Aggiornamento configurazione, firmware or driver.
- Recovery da offline o mismatch.
- Verifica periodica o pre-sessione.

## Preconditions

- Equipment record esistente.
- Configuration record disponibile se necessario.
- Dipendenze note o esplicitamente `OPEN`.

## Procedure

1. Verificare identita equipment.
2. Verificare type, location and owner.
3. Verificare configuration, firmware and driver evidence.
4. Verificare dependencies and logical group membership.
5. Verificare health status.
6. Valutare criticality and safety relevance.
7. Se verifica positiva, impostare state `Verified` o `Available` secondo uso previsto.
8. Se verifica fallisce, impostare `Degraded`, `Offline` o `Maintenance` secondo evidenza.
9. Registrare verification evidence.
10. Informare CAP-001/CAP-002 se assignment o schedule sono impattati.

## Outputs

- Verification record.
- Updated equipment state.
- Recovery or maintenance action if needed.

## Controls

- Nessun asset operativo senza verifica.
- Mismatch deve essere registrato e non nascosto.
- State transition deve rispettare `EQR-ADR-002`.

## Related Documents

- `../adr/EQR-ADR-002-equipment-state-model.md`
- `../runbooks/equipment-offline.md`
- `../runbooks/configuration-mismatch.md`
