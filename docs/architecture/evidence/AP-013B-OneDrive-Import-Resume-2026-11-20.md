# AP-013B — Riattivazione OneDrive Import, 20 novembre 2026

## Perimetro e stato operativo

Riattivata su richiesta Owner soltanto l'attività Windows `Digital StarGate - OneDrive Import`, precedentemente sospesa per il surriscaldamento dello storage e la sua rimozione sicura. La ventola è stata ripristinata. **Morning Transfer resta disabilitato; le elaborazioni scientifiche restano sospese.** Nessuna lettura o scrittura dei payload H: e K: effettuata dalla verifica.

Il confronto XML prima/dopo conferma la sola modifica di `Settings/Enabled`. Conservati launcher nascosto WScript, comando PowerShell originale, trigger ogni 5 minuti, `MaxFilesPerRun 30`, `IgnoreNew`, principal e timeout 30 minuti. Nessuna modifica al runtime, al trasporto EAGLE o alla Safety Authority.

## Ciclo automatico verificato

Orari Europe/Rome, 20 novembre 2026:

- avvio automatico del processo: **18:43:49**;
- discovery: **18:43:50–18:43:54**;
- completamento import: **18:55:02**;
- attività tornata Ready, `LastTaskResult = 0`;
- rapporto conclusivo: **18:56:38**.

Discovery: `DSG-DISCOVERY-RUN-3c018bca-a341-4c73-802a-e72473950994`.
Import: `DSG-OD-IMPORT-4717b4cd-6b4c-40e5-bbb2-597256bd6419`.

| Riscontro | Esito |
|---|---:|
| File discovery / parsed | 905 / 905 |
| Parsing fallito / ambiguo | 0 / 0 |
| Manifest READY osservati | 905 |
| File già importati verificati | 905 |
| ACK esistenti verificati | 905 |
| Nuovi file richiesti / copiati | 0 / 0 |
| Errori import / ACK | 0 / 0 |
| Cancellazioni sorgente / transport | 0 / 0 |
| Overwrite | 0 |

Tutte le 905 righe delle ricevute riportano `ACK_EXISTS_VERIFIED`, senza errori, con destinazione sotto `F:\Astrofotografia`. Verificate dimensioni e SHA-256 dei file esistenti. I 124 avvisi discovery riguardano esclusivamente FWHM non disponibile nel nome NINA (`NaN`): non sono errori di trasferimento.

**Nessuna nuova immagine disponibile:** il ciclo prova discovery, verifica dei file esistenti e idempotenza; non esercita una nuova copia e non misura la capacità o la velocità di trasferimento. Non costituisce una nuova acceptance globale AP-013 o una chiusura scientifica.

I trigger intermedi durante il ciclo sono gestiti da `IgnoreNew`: non avviano import paralleli. Il risultato del processo concluso va distinto dai trigger rifiutati durante la sua esecuzione.

## Storage e limiti del controllo

F: osservato a 50–51 °C, ultimo campione 50 °C alle 18:56:33. Nessun nuovo avviso/errore System dei provider storage, NVMe, Plug and Play, UMDF e WHEA controllati nella finestra 18:43:49–18:55:38. Riscontro limitato alla finestra osservata, non garanzia sui cicli futuri. Monitoraggio temporaneo terminato; nessuna nuova attività di monitoraggio permanente.

## Tracciabilità delle prove

Ricevute complete conservate localmente in `DSG-Inventory\Import-Resume-20261120` e nella directory del run Import. Pubblicati soltanto riepilogo, identificativi e impronte degli artefatti; CSV, XML amministrativi e percorsi personali completi restano locali.

| Artefatto | SHA-256 |
|---|---|
| import-manifest.json | `d0191227ff46fbdab59cecd151019438c114d7cb575158deccfdc642a3fd9893` |
| import-results.csv | `f1945cd6c19e56b3c1c78943ef5ec18116907a4ca1efc40a57d48ab1db7adfc5` |
| ack-results.csv | `81e0dad4c835eaa5d32060338d12dcdb51b8d68d3802c22b7ede61ae1bea426c` |

## Continuità e ripristino

In caso di nuovo problema, sospendere il solo Import e conservare file e ricevute; non riattivare automaticamente Morning Transfer e non riprendere le elaborazioni. Il rollback generale del trasporto resta quello del runbook, distinto dalla sospensione locale. Al primo ciclo con immagini nuove verificare `CopiedVerified`, SHA-256, ACK e assenza di errori/delete/overwrite.

[Runbook AP-013B](../validation/AP-013B-OneDrive-Transport-Operational-Acceptance.md) ·
[Handover operativo](../../project/HANDOVER_2026-11-20-ONEDRIVE-IMPORT-RESUME.md).
