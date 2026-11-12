# Avvio nascosto dei processi locali

## Perimetro e diagnosi

Questo runbook descrive le correzioni locali verificate il 12 novembre 2026.
Non installa servizi e non avvia elaborazioni. La pubblicazione della
documentazione non distribuisce modifiche al runtime scientifico.

| Sintomo | Origine identificata | Correzione verificata |
|---|---|---|
| Console al controllo discovery/import | Attività Windows `Digital StarGate - OneDrive Import`, ogni 5 minuti | Launcher WScript, comando PowerShell originale nascosto e codice d'uscita propagato |
| Finestra intitolata `dotnet`, segnalata circa ogni minuto | Chiamate ripetute a `SpatialLag.dll` dal controller Python della campagna PixInsight | `CREATE_NO_WINDOW` nel lancio del sottoprocesso .NET |

La frequenza segnalata della finestra `dotnet` non identifica una schedulazione
fissa ogni minuto. Le chiamate derivano dai passi del calcolo scientifico.
Prima di modificare un avvio, correlare eseguibile, comando, processo padre,
orario e lotto; il solo nome `dotnet.exe` non identifica l'applicazione.

## Correzione SpatialLag

Il controller `continue_spatial_sessions38_45_h_v1.py` è eseguito con
`pythonw.exe`, ma il suo adapter `spatial_lag_stdin_adapter_g_v1.py` avviava
`dotnet.exe exec --fx-version 10.0.10 …/SpatialLag.dll` senza impedire la
creazione della console. Nascondere il padre non risolve questo avvio figlio.

L'unica modifica al `subprocess.run` dell'adapter è:

```python
creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
```

Restano invariati comando, ambiente, input binario via stdin, cattura di
stdout/stderr, codice d'uscita e controlli del risultato. Il binario .NET,
le formule e gli input scientifici non sono stati modificati.
Cinque fixture conservate hanno prodotto gli stessi risultati numerici;
due flussi malformati sono rimasti respinti.

## Attivazione durante un'elaborazione

Un modulo Python già importato resta in memoria: l'aggiornamento su disco
si applica ai successivi processi avviati naturalmente. Non arrestare o
duplicare un lotto per rendere immediata una modifica di presentazione.

Conservare i byte precedenti, gli hash prima/dopo e l'orario del nuovo avvio.
Se un protocollo registra l'hash del file su disco durante una transizione,
non usarlo da solo come prova della versione già caricata in memoria.
Registrare una nota di provenienza senza riscrivere il protocollo originale.
Questo caso è documentato esplicitamente per il lotto 39.

Il lotto 40 è il primo successivo avvio naturale verificato con il sorgente
corretto: avvio alle 22:10:43 Europe/Rome, 2.106 campioni senza finestre `dotnet`
rilevate, primi tre blocchi controllati e sette completati al riscontro delle
22:20:39, con processo attivo e log errori vuoto. Sono snapshot del 12 novembre,
non indicatori live né acceptance dell'intero lotto.

## Verifica e ripristino

Per verificare un successore, controllare la nuova identità del processo,
il suo orario rispetto alla correzione, l'hash dell'adapter nel protocollo,
le ricevute dei blocchi, il log errori e un intervallo dichiarato di osservazione
delle finestre. Non equiparare l'assenza di finestre alla validità scientifica.

Il bundle locale `work/dotnet-hidden-launch-h-v1`, relativo al workspace
scientifico PixInsight, conserva `adapter-before.py`, `adapter-candidate.py`,
le verifiche e la nota di transizione. Prima del rollback verificare che il
sorgente corrente corrisponda ancora all'hash della correzione; ripristinare
atomicamente soltanto l'adapter precedente. Se è cambiato, ispezionare il
successore e non sovrascriverlo. Anche il rollback riguarda i futuri import:
non riavviare la campagna né alterare ricevute o dati per applicarlo.

Riferimenti: [evidenza SpatialLag e limiti](../architecture/evidence/PIAI-SpatialLag-Hidden-Launch-2026-11-12.md),
[handover lotto 40](../project/HANDOVER_2026-11-12-DOTNET-HIDDEN-LOT40.md) e
[avvio discovery/import OneDrive](../architecture/evidence/AP-013B-Hidden-Discovery-Import-2026-11-12.md).
