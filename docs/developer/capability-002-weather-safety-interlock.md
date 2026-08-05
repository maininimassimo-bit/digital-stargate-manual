# Capability 002 – Weather Safety Interlock

**Status:** Proposed  
**Release target:** 2.0  
**Related ADR:** [ADR-005 – Weather Safety Interlock fail-safe](../architecture/ADR-005-Weather-Safety-Interlock.md)

## Scopo

Definire il vertical slice che valuta i segnali meteo e di sicurezza, impedisce aperture non sicure, richiede la chiusura quando necessario e registra ogni decisione senza dipendere direttamente da N.I.N.A., ASCOM o dai driver dei sensori.

## Ambito

La capability comprende:

- acquisizione normalizzata delle osservazioni ambientali;
- valutazione deterministica degli stati `SAFE`, `WARNING`, `UNSAFE` e `UNKNOWN`;
- controllo della freschezza e coerenza dei dati;
- isteresi e finestra di stabilità;
- blocco apertura;
- richiesta idempotente di chiusura;
- audit con `CorrelationId`;
- notifica dell'operatore;
- override manuale controllato entro i limiti dell'ADR-005.

Non comprende, fino a validazione dell'hardware reale:

- soglie numeriche definitive;
- riapertura automatica;
- bypass della pioggia confermata;
- sostituzione degli interlock locali della cupola;
- dipendenze dirette del Domain da SDK ASCOM, N.I.N.A. o sensori.

## Modello applicativo

```text
Weather observations
  -> EvaluateWeatherSafety
  -> SafetyDecision
  -> AuditSafetyDecision
  -> BlockOpening | RequestDomeClosure | NoAction
  -> NotifyOperator
```

## Porte applicative

- `IWeatherObservationSource`
- `ISafetyDecisionAudit`
- `IDomeSafetyCommandPort`
- `IOperatorNotificationPort`
- `IClock`

Le interfacce appartengono all'Application; gli adattatori appartengono a Infrastructure.

## Regole

1. Dati mancanti, obsoleti o incoerenti producono `UNKNOWN`.
2. `UNKNOWN` blocca l'apertura ed equivale a `UNSAFE` per l'automazione.
3. La pioggia confermata produce immediatamente `UNSAFE`.
4. La decisione include cause, timestamp, qualità del dato e `CorrelationId`.
5. La chiusura può essere richiesta più volte senza effetti collaterali aggiuntivi.
6. La transizione verso `SAFE` richiede una finestra stabile configurata.
7. Gli interlock fisici locali restano autoritativi per la protezione della cupola.

## Osservabilità

La capability deve produrre:

- log strutturati delle osservazioni e della decisione;
- metriche per stato corrente, transizioni, dati obsoleti, chiusure richieste e fallite;
- health check separati per sorgenti meteo, audit e comando cupola;
- `CorrelationId` propagato dall'acquisizione alla conferma di chiusura;
- allarmi per stato `UNKNOWN` persistente, comando fallito e mancata conferma `CLOSED`;
- riferimenti al runbook operativo.

## Sicurezza e safety

- safety prevale sulla disponibilità;
- i segreti degli adattatori non attraversano Domain o Contracts pubblici;
- ogni override richiede identità, motivazione, durata e audit;
- nessun override consente apertura con pioggia confermata;
- la perdita di rete deve degradare verso chiusura o blocco apertura secondo gli interlock disponibili.

## Migrazione

| Fase | Modalità | Criterio di uscita |
|---|---|---|
| 1 | Inventario e simulatori | sensori e attuatori verificati |
| 2 | Shadow mode | decisioni confrontate con operatore |
| 3 | Blocco apertura | nessun falso `SAFE` nei test |
| 4 | Chiusura automatica | conferma `CLOSED` e rollback collaudati |
| 5 | Evoluzione | riapertura automatica valutata separatamente |

## Acceptance Criteria

- [ ] `UNKNOWN` non autorizza mai l'apertura automatica.
- [ ] Il Domain non referenzia framework, ORM, SDK ASCOM o client esterni.
- [ ] Ogni decisione è auditabile e correlata.
- [ ] Il comando di chiusura è idempotente.
- [ ] Il mancato `CLOSED` genera allarme operativo.
- [ ] Sono coperti dati assenti, obsoleti, incoerenti e transizioni oscillanti.
- [ ] È disponibile una procedura di rollback verso la gestione manuale.

## Open Issues

- sensori meteo effettivamente installati e protocolli disponibili;
- soglie operative validate per vento, umidità e margine di rugiada;
- controller che fornisce la conferma `CLOSED`;
- comportamento locale in assenza di EAGLE o rete;
- canale e priorità delle notifiche;
- durata della finestra stabile prima del ritorno a `SAFE`.

## Traceability

- [ADR-005](../architecture/ADR-005-Weather-Safety-Interlock.md)
- [Monitoraggio meteo e sicurezza ambientale](../chapters/26-monitoraggio-meteo-sicurezza-ambientale.md)
- [Chiusura dell'osservatorio](../chapters/25-chiusura-osservatorio.md)
- [Roadmap evolutiva](../chapters/33-roadmap-evolutiva.md)
