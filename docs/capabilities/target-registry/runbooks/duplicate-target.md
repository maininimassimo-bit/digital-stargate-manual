# Runbook - Duplicate Target

| Campo | Valore |
|---|---|
| Runbook | Duplicate Target |
| Capability | CAP-TGT-001 Target Registry |
| Severity | Data Quality / Operational |
| Owner | Science Owner / Knowledge Owner / OPEN |

## Trigger

- Nuovo target sembra gia presente nel registry.
- Alias or catalogue reference punta a target esistente.
- Observation history mostra duplicazione di target identity.

## Immediate Assessment

1. Identificare target candidati duplicati.
2. Confrontare canonical name, aliases, catalogue references and coordinates.
3. Verificare observation history and scheduling references.
4. Determinare quale record e canonical candidate.
5. Bloccare pubblicazione finche non risolto.

## Recovery Steps

1. Applicare `TGT-ADR-002` per mantenere una canonical target identity.
2. Se duplicato confermato, collegare alias/catalogue reference al record canonico.
3. Preservare record storico o redirect documentale senza cancellare evidenza.
4. Aggiornare CAP-SCH-001 or CAP-OSM-001 references se impattati.
5. Registrare decisione, owner and rationale.
6. Ri-validare target canonico prima della pubblicazione.

## Escalation

Escalare se:

- duplicato impatta schedule pubblicate;
- duplicato impatta observation history;
- canonical identity non e determinabile;
- serve decisione scientifica.

## Exit Criteria

- Esiste un solo target canonico pubblicabile.
- Alias e catalogue references sono preservati.
- Impatti su scheduling/session/data sono aggiornati or documentati open.

## Related Documents

- `../adr/TGT-ADR-002-canonical-target-identity.md`
- `../sop/validate-target.md`
- `../sop/update-target.md`
