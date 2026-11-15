# Avvii locali — Riscontro operativo del 15 novembre 2026

## Perimetro e data

Controllo in sola lettura del **15 novembre 2026, ore 19:36:10 Europe/Rome**
(`18:36:10 UTC`). Verifica la persistenza delle correzioni documentate nelle
PR #623 e #626 e le successive ricevute operative. Non modifica script,
configurazioni o dati e non avvia, interrompe o ripete elaborazioni.

Le prove visive del 12 novembre restano riferite ai propri intervalli.
Il presente riscontro legge configurazione, hash, processi e ricevute:
non è una nuova osservazione campionata delle finestre.

## Discovery e importazione OneDrive

L'attività `Digital StarGate - OneDrive Import` richiama ancora il launcher
`wscript.exe //B //NoLogo` con il comando PowerShell originale nascosto.
La policy `IgnoreNew` e il limite di 30 minuti sono conservati.

| Riscontro | Esito osservato |
|---|---|
| Cicli conclusi nelle 24 ore precedenti il controllo | 80 manifest di import completati |
| Errori nei cicli conclusi | `Failed = 0`, `AckFailed = 0`, nessun ciclo con errori |
| Nuove richieste e copie nei cicli conclusi | `Requested = 0`, `CopiedVerified = 0` |
| Cancellazioni e sovrascritture nei cicli conclusi | Tutti i contatori a 0 |
| Ultimo import concluso | 15 novembre, 19:21:26.6193419 Europe/Rome |
| File già importati e ACK verificati nell'ultimo ciclo | 905 file, 905 ricevute |
| Discovery più recente | Conclusa alle 19:24:00.5897596; 905 file, 0 errori, 0 `CopyNew` |
| Avvisi discovery | 124, tutti per FWHM non disponibile (`NaN`) nel nome N.I.N.A. |
| Ciclo corrente allo snapshot | Processo attivo; cartella di run senza manifest conclusivo |

Riferimenti dei run: import concluso
`DSG-OD-IMPORT-e132f067-875e-45d2-bdc8-d30eab55c293`, discovery
`DSG-DISCOVERY-RUN-36e1501c-11f9-4dac-bad6-12ffd840b87c`.
Il run ancora in corso è
`DSG-OD-IMPORT-a947adda-0c22-400f-84ea-fb99d02fe75e`: non è incluso
negli 80 cicli conclusi e non gli viene attribuito un esito finale.

I contatori I/O del processo corrente sono cresciuti tra le letture.
Il campo dell'ultimo trigger Windows riportava `2147946720 / 0x800710E0`
mentre la stessa istanza avviata alle 19:23 era ancora attiva e i trigger
successivi incontravano `IgnoreNew`. Distinguere il risultato del trigger
sovrapposto dal risultato finale del ciclo: per quest'ultimo attendere
il manifest conclusivo e verificare l'esito effettivo dell'attività.

Il riscontro prova il percorso idempotente sui file e sulle ricevute esistenti.
Non essendoci nuove richieste, non attesta una nuova copia, una nuova
acquisizione EAGLE o la pubblicazione di nuove sessioni sul portale.
I 124 avvisi descrivono metadati mancanti; non sono errori del launcher.

## SpatialLag e ricevute successive al lotto 40

L'adapter installato conserva lo SHA-256
`78c5ac18f7b79697b2543f889a49f3589e03d9437f2c5371d698083caccf4cfb`.
Il binario `SpatialLag.dll` conserva lo SHA-256
`6fc539a880e4170ea2f9c03761195e46eb1e1977dbb6d0bdd09b5a2cf07570b3`.
Entrambi coincidono con quelli della correzione e della verifica del lotto 40.

I protocolli dei lotti 40, 41, 42, della coda recuperata del lotto 43 e dei
lotti 44 e 45 riportano l'adapter corretto. Il vecchio arresto del lotto 43
è conservato; le ricevute successive documentano il recupero e la prosecuzione
fino al lotto 45. Il recupero è un fatto operativo distinto dalla correzione
della console; questo riscontro non ne attribuisce la causa al flag di avvio.

| Evidenza successiva letta il 15 novembre | Stato registrato |
|---|---|
| `strata-14-23-native-queue-g-v1/terminal.json` nella campagna | `PASS_FINAL_TEN_SPATIAL_STRATA_ARCHIVED_AND_CLASSIFIED`, 4.794 blocchi complessivi; report del 13 novembre, 03:20:20 Europe/Rome |
| `strata-14-23-resume-after-session43-h-v1/terminal.json` nella campagna | `PASS_H_RESUMPTION_COMPLETE_FROZEN_FINAL_TEN_STRATA` |
| `spatial-source-epoch-complete-campaign-audit-h-v1/verification.json` nel workspace | `PASS_ALL4794_SOURCE_EPOCH_BINDINGS_WITH_EXPLICIT_FIRST21_CACHE_REUSE`, 4.794 blocchi; report del 13 novembre, 03:24:15 Europe/Rome |
| `post-campaign-complete-source-epoch-audit-after-session43-h-v2/terminal.json` nel workspace | `PASS_COMPLETE4794_SOURCE_EPOCH_AUDIT` |

I vecchi `stop.json` delle code precedenti restano evidenze storiche e non
sostituiscono le ricevute dei successori esplicitamente identificati.
Il presente controllo legge gli esiti registrati: non riesegue indipendentemente
la decodifica, i calcoli o tutte le verifiche d'archivio.
L'audit conserva `scientificClosures = 0` e `completeStudy = false`:
il completamento tecnico di questa sequenza non chiude lo studio complessivo
e non costituisce una nuova acceptance scientifica o una validazione d'immagine.
La nota di provenienza della transizione del lotto 39 resta applicabile.

## Conservazione e riferimenti

Il riepilogo locale del controllo è
`local-script-health-20261115-evidence.json` nel workspace di manutenzione.
I manifest originali restano in `DSG-Inventory`; i report scientifici restano
nel workspace PixInsight. Si pubblica questo riepilogo curato, non log grezzi,
inventari delle finestre o risultati scientifici privati.

- [Runbook degli avvii locali e ripristino](../../developer/local-background-launch.md).
- [Correzione e prova iniziale OneDrive](AP-013B-Hidden-Discovery-Import-2026-11-12.md).
- [Correzione SpatialLag, transizione del lotto 39 e prova del lotto 40](PIAI-SpatialLag-Hidden-Launch-2026-11-12.md).

Questa pubblicazione è solo documentale. Il suo rollback è il revert della PR;
non richiede modifiche agli script, riavvii o ripetizioni del calcolo.
