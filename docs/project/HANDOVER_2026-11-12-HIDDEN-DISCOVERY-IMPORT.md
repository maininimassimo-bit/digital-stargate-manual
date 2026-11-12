# Handover — Discovery/import con avvio nascosto, 12 novembre 2026

## Stato operativo

La finestra CLI segnalata dall'Owner riguarda l'attività locale
`Digital StarGate - OneDrive Import`, che esegue discovery e importazione
OneDrive. Modificata soltanto l'azione Windows: launcher `wscript.exe`
senza console, avvio nascosto del comando PowerShell originale e propagazione
del codice di uscita. Periodicità reale **5 minuti**, `IgnoreNew`, account,
privilegi, timeout e batch massimo 30 conservati.

Successivo ciclo **automatico**, 12 novembre 18:58:49–19:16:01 Europe/Rome:
73 campioni dell'avvio senza finestre CLI rilevate, discovery 905 file/0 errori,
import concluso con codice 0, 905 file già importati e 905 ricevute verificate.
Zero nuove copie, errori, cancellazioni o sovrascritture. Non erano disponibili
nuove immagini: il trasferimento di nuovi file non è stato esercitato.

## Riferimenti e continuità

- [Evidenza operativa, configurazione e rollback](../architecture/evidence/AP-013B-Hidden-Discovery-Import-2026-11-12.md).
- [Runbook AP-013B aggiornato](../architecture/validation/AP-013B-OneDrive-Transport-Operational-Acceptance.md#710-avvio-nascosto-del-wrapper-discoveryimport-12-novembre-2026).

Launcher e backup sono conservati nella directory locale
`DSG-Inventory\HiddenLaunch-20261112`, che deve restare disponibile perché
l'attività la richiama. Il ripristino riguarda soltanto l'azione Windows.
Non reinstallare o rieseguire importazioni per aggiornare questa documentazione.
La modifica locale non cambia il contratto del pacchetto di reporting EAGLE,
la pubblicazione delle sessioni GitHub/Pages o la Safety Authority.
Non costituisce una nuova acceptance globale AP-013 o un collaudo di capacità.

Questo handover è circoscritto al launcher locale: conserva gli altri handover,
le baseline scientifiche e gli stati dei package non coinvolti.
