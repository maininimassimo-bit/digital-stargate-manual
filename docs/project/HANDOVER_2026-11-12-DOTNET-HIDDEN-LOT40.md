# Handover — Finestra dotnet e verifica del lotto 40

## Stato osservato il 12 novembre 2026

La console `dotnet` residua proveniva dalle chiamate SpatialLag della campagna
PixInsight, distinta dall'attività discovery/import OneDrive già corretta.
Installato `CREATE_NO_WINDOW` nel solo lancio del figlio .NET dell'adapter
`spatial_lag_stdin_adapter_g_v1.py`. Cinque fixture con risultati numerici
identici, due input malformati respinti, binario e input scientifici invariati.

Nessun processo arrestato o riavviato. Il lotto 39 era già caricato e ha una
nota esplicita di transizione della provenienza: l'hash registrato dal suo
protocollo descriveva il file su disco, non provava l'aggiornamento in memoria.
Protocollo originale e sorgenti precedenti conservati.

Il lotto 39 ha completato 128 blocchi. Il lotto 40 è partito naturalmente alle
**22:10:43 Europe/Rome**, PID 32112, con l'hash dell'adapter corretto.
**2.106 campioni** tra le 22:11:49 e le 22:17:24 senza finestre `dotnet`
rilevate. Primi tre blocchi controllati; alle **22:20:39**, sette completati,
controller attivo e log errori vuoto.

## Continuità e limiti

- [Runbook degli avvii locali e rollback](../developer/local-background-launch.md).
- [Evidenza, hash, transizione del lotto 39 e limiti](../architecture/evidence/PIAI-SpatialLag-Hidden-Launch-2026-11-12.md).
- [Precedente launcher discovery/import](HANDOVER_2026-11-12-HIDDEN-DISCOVERY-IMPORT.md).

Conservare il bundle locale `work/dotnet-hidden-launch-h-v1` del workspace
scientifico. Il riepilogo descrive lo snapshot osservato, non lo stato live:
non attestare completamento dell'intero lotto 40, nuova validazione scientifica
o promozione della conoscenza. Campionamento finestre distinto da registrazione
continua; nessun singolo processo figlio catturato dal tentativo separato.

Per questa pubblicazione documentale non avviare, interrompere o duplicare
il calcolo. Gli altri handover, le authority e gli stati dei package restano
invariati; nessuna nuova operazione cloud o modifica della Safety Authority.
