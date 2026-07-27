# CAP-003 - Acceptance Criteria

## Purpose

Gli acceptance criteria definiscono condizioni misurabili per considerare Equipment Registry pronto per futura implementazione capability-by-capability.

## Criteria

| ID | Criterion | Measurement | Status |
|---|---|---|---|
| `EQR-AC-001` | Ogni equipment operativo puo avere identificatore, tipo, owner, location, state and lifecycle state. | Campi presenti nel modello concettuale. | Defined |
| `EQR-AC-002` | Il registro copre categorie fisiche, logiche, firmware, drivers and logical equipment groups. | Coverage esplicita in `index.md` e `architecture-mapping.md`. | Defined |
| `EQR-AC-003` | Asset non verificato non e disponibile per scheduling o session management. | State model e ADR lo impediscono. | Defined |
| `EQR-AC-004` | CAP-002 puo consumare availability and resource assignment constraints. | Mapping architetturale presente. | Defined |
| `EQR-AC-005` | CAP-001 puo consumare readiness, configuration and health evidence. | Mapping architetturale presente. | Defined |
| `EQR-AC-006` | Configuration mismatch blocca l'uso operativo finche non risolto o accettato con evidenza. | Runbook dedicato e SOP update presenti. | Defined |
| `EQR-AC-007` | Equipment offline rimuove disponibilita operativa e attiva recovery. | Runbook dedicato presente. | Defined |
| `EQR-AC-008` | Equipment missing produce investigazione e registry correction. | Runbook dedicato presente. | Defined |
| `EQR-AC-009` | Ogni update preserva storico minimo. | SOP `update-equipment.md` presente. | Defined |
| `EQR-AC-010` | Retirement non cancella storico, configurazioni o dipendenze. | SOP `retire-equipment.md` presente. | Defined |
| `EQR-AC-011` | Ogni requisito CAP-003 ha identificatore unico. | 32 requisiti con prefisso `EQR`. | Defined |
| `EQR-AC-012` | ADR specifiche chiariscono registry authority e state model. | 2 ADR presenti. | Defined |
| `EQR-AC-013` | SOP e runbook coprono operazioni e failure mode richiesti. | 4 SOP e 4 runbook presenti. | Defined |
| `EQR-AC-014` | CAP-000 registra status `Documented`, readiness `Implementation Ready`, version `0.1`. | CAP-000 aggiornato. | Pending update |
| `EQR-AC-015` | REL-000 contiene riferimento minimo alla capability. | REL-000 aggiornato. | Pending update |
| `EQR-AC-016` | MkDocs rende raggiungibili tutti i documenti CAP-003. | Navigazione aggiornata. | Pending update |
| `EQR-AC-017` | Validation non segnala duplicati o link interni mancanti nel package. | Static validation o MkDocs strict. | Pending validation |

## Acceptance Notes

- `Defined` indica criterio documentato, non implementazione completata.
- I criteri `Pending update` saranno chiusi con aggiornamento di CAP-000, REL-000 e MkDocs.
- Futura operativita richiedera evidenza di implementazione e rilascio secondo REL-000.
