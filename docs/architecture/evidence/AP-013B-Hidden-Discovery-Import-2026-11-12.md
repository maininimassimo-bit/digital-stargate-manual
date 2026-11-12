# AP-013B — Avvio nascosto discovery/import: verifica del 12 novembre 2026

| Campo | Valore |
|---|---|
| Tipo | Evidenza operativa locale e aggiornamento runbook |
| Attività Windows | `Digital StarGate - OneDrive Import` |
| Perimetro | Solo modalità di avvio sul PC principale |
| Esito | Avvio automatico osservato; discovery e controllo import/ACK conclusi senza errori |
| Limite | Nessuna nuova immagine disponibile: copia di nuovi file non esercitata |

## Problema e correzione applicata

L'attività avviava direttamente PowerShell con `-WindowStyle Hidden`, ma la
finestra CLI poteva comparire brevemente a ogni controllo. Il 12 novembre alle
18:53:51 Europe/Rome è stata sostituita soltanto l'azione dell'attività con
`wscript.exe //B //NoLogo` e il launcher locale
`Start-DSGOneDriveImportHidden.vbs`.

Il launcher usa `WScript.Shell.Run` con stile finestra `0` e attesa `True`,
quindi restituisce il codice del processo tramite `WScript.Quit`. Conserva
il comando PowerShell originale: `-NoProfile -NonInteractive -WindowStyle Hidden
-ExecutionPolicy Bypass`, script runtime
`tools\dsdm\session-importer\Start-DSGOneDriveImportScheduled.ps1` e
`-MaxFilesPerRun 30`. Un test sintetico separato con codice di uscita `37`
ha confermato la propagazione del risultato.

Il confronto XML prima/dopo conferma invariati trigger, principal e settings:
periodicità **5 minuti**, accesso Interactive/Limited, `IgnoreNew` e limite
di esecuzione di 30 minuti. La discovery prepara il piano; il wrapper esegue
poi l'import OneDrive verso `F:\Astrofotografia`. Non sono stati modificati
script di discovery/import, criteri READY/SHA-256 o dati scientifici.

## Verifica del successivo avvio automatico

Orari del 12 novembre 2026, fuso Europe/Rome (UTC+1).

| Evidenza | Risultato osservato |
|---|---|
| Avvio automatico | 18:58:49, `wscript.exe` PID 80324 → PowerShell PID 59776 |
| Osservazione finestre | 73 campioni tra 18:58:12 e 18:59:12; nessuna finestra CLI rilevata |
| Discovery completata | 18:58:54; 905 file, 905 riconosciuti, 0 errori, 0 `CopyNew` |
| Import completato | 19:16:01 (`2026-11-12T18:16:01.4546679Z`) |
| Risultato attività | `LastTaskResult = 0`, letto dopo la conclusione |
| Manifest READY osservati | 905 |
| File già importati | `AlreadyImportedSkipped = 905` |
| Ricevute esistenti verificate | `AckExistingVerified = 905` |
| Nuove copie/ricevute | `Requested = 0`, `CopiedVerified = 0`, `AckCreated = 0` |
| Errori | `Failed = 0`, `AckFailed = 0` |
| Cancellazioni/sovrascritture | `SourceFilesDeleted = 0`, `TransportFilesDeleted = 0`, `OverwritesPerformed = 0` |

Run discovery: `DSG-DISCOVERY-RUN-f58a6644-9523-4c2e-b901-56e386224525`.
Run import: `DSG-OD-IMPORT-8ab160e7-e7fb-4845-9adf-710ebdd3d51f`, schema `1.2`,
modalità `COPY_ONLY_ONEDRIVE_IMPORT_WITH_VERIFICATION_ACK`.

Il ciclo ha richiesto circa 17 minuti: il percorso esistente verifica gli
hash dei file e delle ricevute. I trigger intermedi non hanno avviato duplicati,
coerentemente con `IgnoreNew`. Un trigger rifiutato durante un ciclo attivo
non deve essere confuso con l'esito finale del ciclo realmente eseguito.

La prova conferma il percorso idempotente sui file e ACK esistenti; **non**
attesta 905 nuove copie, una nuova acquisizione EAGLE o una nuova pubblicazione
scientifica sul portale. L'assenza di finestra è una verifica campionata
dell'avvio, non una registrazione continua dell'intero ciclo.

## Conservazione e ripristino

Le evidenze complete restano locali in
`C:\Users\MassimoMainini\DSG-Inventory\HiddenLaunch-20261112`:

- `OneDriveImport-before.xml`, `OneDriveImport-after.xml`, `action-before.json`;
- `apply-result.json`, `automatic-run-verification.json`, `window-observation.json`;
- `Start-DSGOneDriveImportHidden.vbs`, `Apply-HiddenLaunch.ps1`,
  `Restore-PreviousLaunch.ps1` e `VERIFICA-AVVIO-AUTOMATICO.md`.

Il launcher è installato nella stessa directory locale, richiamata dall'azione
Windows: conservarla; non è una cartella temporanea eliminabile dopo la verifica.
I report originali si trovano nelle directory dei run sotto
`DSG-Inventory\SessionImporter` e `DSG-Inventory\OneDriveImport`.
Questo documento pubblica soltanto il riepilogo curato, non log grezzi,
inventari delle immagini, XML delle attività o configurazioni private.

Per ripristinare l'avvio precedente, ispezionare prima azione corrente e backup,
quindi eseguire localmente `Restore-PreviousLaunch.ps1` con i privilegi richiesti
da Windows. Lo script verifica che l'azione corrente richiami il launcher,
ripristina soltanto l'azione salvata e non arresta il lavoro già in corso.
Non cancellare file scientifici né riattivare il trasporto legacy SMB per questo
ripristino. Il ritorno all'azione originale può reintrodurre il lampeggio CLI.

Riferimenti: [runbook AP-013B](../validation/AP-013B-OneDrive-Transport-Operational-Acceptance.md)
e [handover](../../project/HANDOVER_2026-11-12-HIDDEN-DISCOVERY-IMPORT.md).
