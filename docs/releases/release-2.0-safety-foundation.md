# Release 2.0 – Safety Foundation

## Stato

Proposta architetturale. Nessuna capability runtime è dichiarata implementata.

## Obiettivo

Introdurre una fondazione fail-safe per la futura automazione dell'osservatorio, mantenendo separati il modello di sicurezza, l'orchestrazione applicativa e gli adattatori verso sensori, N.I.N.A., ASCOM e controller della cupola.

## Ambito iniziale

- [ADR-005 – Weather Safety Interlock fail-safe](../architecture/ADR-005-Weather-Safety-Interlock.md);
- [Capability 002 – Weather Safety Interlock](../developer/capability-002-weather-safety-interlock.md);
- sequenza incrementale in shadow mode, blocco apertura e successiva chiusura automatica;
- osservabilità, audit, allarmi e runbook;
- test con simulatori prima dell'attivazione hardware.

## Dipendenze

- inventario verificato dei sensori e dei protocolli;
- soglie ambientali validate;
- disponibilità di un comando idempotente di chiusura;
- conferma attendibile dello stato `CLOSED`;
- interlock locali indipendenti dall'Application;
- procedura di rollback verso la gestione manuale.

## Non incluso

- soglie numeriche non ancora validate;
- riapertura automatica;
- bypass della pioggia confermata;
- sostituzione degli interlock fisici;
- dichiarazioni di integrazione con hardware non verificato.

## Piano di delivery

| Incremento | Contenuto | Evidenza richiesta |
|---|---|---|
| 2.0-A | Contratti, modello e simulatori | test unitari e architetturali |
| 2.0-B | Shadow mode | confronto decisioni/operatore |
| 2.0-C | Blocco apertura | nessun falso `SAFE` nei test |
| 2.0-D | Chiusura automatica | test idempotenza, `CLOSED`, rollback |
| Futuro | Riapertura automatica | nuova decisione architetturale |

## Acceptance Criteria di release

- [ ] Domain indipendente da Infrastructure e SDK esterni.
- [ ] `UNKNOWN` blocca l'apertura.
- [ ] Tutte le decisioni sono auditabili con `CorrelationId`.
- [ ] Il comando di chiusura è idempotente.
- [ ] Il mancato `CLOSED` genera un allarme.
- [ ] MkDocs e riferimenti sono validati.
- [ ] Test fisici eseguiti prima dell'attivazione operativa.

## Rischi aperti

- sensori e soglie ancora da validare;
- comportamento degradato dell'EAGLE e della rete;
- coerenza tra stato applicativo e stato fisico;
- gestione operativa degli override;
- tempi reali di chiusura in condizioni severe.
