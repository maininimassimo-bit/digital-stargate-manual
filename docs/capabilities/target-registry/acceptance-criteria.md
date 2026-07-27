# CAP-TGT-001 - Acceptance Criteria

## Purpose

Gli acceptance criteria definiscono condizioni misurabili per considerare Target Registry pronto per futura implementazione capability-by-capability.

## Criteria

| ID | Criterion | Measurement | Status |
|---|---|---|---|
| `TGT-AC-001` | Ogni target pubblicato ha identita canonica, type, lifecycle state and metadata. | Campi presenti nel modello concettuale. | Defined |
| `TGT-AC-002` | Il registry copre i cataloghi e tipi target richiesti senza dipendere da provider specifico. | Coverage esplicita in `index.md`. | Defined |
| `TGT-AC-003` | Target non validato non e disponibile per scheduling. | Processo, SOP and state model lo impediscono. | Defined |
| `TGT-AC-004` | Coordinate invalide bloccano pubblicazione. | Runbook dedicato presente. | Defined |
| `TGT-AC-005` | Unknown catalogue identifier blocca approvazione fino a risoluzione o decisione documentata. | Runbook dedicato presente. | Defined |
| `TGT-AC-006` | Duplicati potenziali sono risolti prima della pubblicazione. | `duplicate-target.md` e ADR identity presenti. | Defined |
| `TGT-AC-007` | CAP-SCH-001 puo consumare target, constraints, priority and visibility profile. | Mapping architetturale presente. | Defined |
| `TGT-AC-008` | CAP-OSM-001 puo consumare published target and coordinate evidence. | Mapping architetturale presente. | Defined |
| `TGT-AC-009` | CAP-EQR-001 resta owner della compatibilita equipment, non della target identity. | Governance boundary documentato. | Defined |
| `TGT-AC-010` | Ogni update preserva storico minimo. | SOP `update-target.md` presente. | Defined |
| `TGT-AC-011` | Retirement non cancella observation history references. | SOP `retire-target.md` presente. | Defined |
| `TGT-AC-012` | Ogni requisito CAP-TGT-001 ha identificatore unico. | 32 requisiti con prefisso `TGT`. | Defined |
| `TGT-AC-013` | ADR specifiche chiariscono target authority and canonical identity. | 2 ADR presenti. | Defined |
| `TGT-AC-014` | SOP e runbook coprono operazioni e failure mode richiesti. | 4 SOP e 4 runbook presenti. | Defined |
| `TGT-AC-015` | CAP-000 registra status `Documented`, maturity `Documented`, readiness `Implementation Ready`, version `0.1`. | CAP-000 aggiornato. | Pending update |
| `TGT-AC-016` | REL-000 contiene riferimento minimo alla capability. | REL-000 aggiornato. | Pending update |
| `TGT-AC-017` | MkDocs rende raggiungibili tutti i documenti CAP-TGT-001. | Navigazione aggiornata. | Pending update |
| `TGT-AC-018` | Validation non segnala duplicati o link interni mancanti nel package. | Static validation or MkDocs strict. | Pending validation |

## Acceptance Notes

- `Defined` indica criterio documentato, non implementazione completata.
- Futura operativita richiedera evidenza di implementazione e rilascio secondo REL-000.
