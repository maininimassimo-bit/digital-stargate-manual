# ADR-005 - EAGLE Operational Authority

| Campo | Valore |
|---|---|
| Stato | Proposed |
| Data | 2026-07-28 |
| Decisione | L'EAGLE mantiene l'autorità operativa dell'osservatorio |

## Contesto

Digital StarGate evolve verso una piattaforma software più ampia. È necessario evitare che monitoraggio, AI e workflow vengano interpretati come sostituti dei sistemi locali di controllo.

## Decisione

EAGLE, NINA, PHD2, CPWI, ASCOM e i controlli locali mantengono la responsabilità primaria per acquisizione, automazione e sicurezza. Digital StarGate raccoglie dati, ricostruisce stato, analizza, cataloga e supporta l'utente.

## Conseguenze

- il collector deve essere non invasivo;
- l'indisponibilità di Digital StarGate non blocca la sessione;
- nessun comando safety-critical viene introdotto senza nuovo ADR;
- Mission Control rappresenta lo stato, non sostituisce i controlli locali.
