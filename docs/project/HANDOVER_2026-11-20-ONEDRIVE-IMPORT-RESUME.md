# Handover — OneDrive Import riattivato, 20 novembre 2026

## Stato verificato

- **OneDrive Import attivo**, con launcher nascosto, periodicità 5 minuti, batch massimo 30 e `IgnoreNew` invariati.
- **Morning Transfer disabilitato**, conservato esclusivamente come rollback legacy.
- **Elaborazioni scientifiche sospese**; nessun riavvio autorizzato da questa nota.
- H: e K: esclusi dalle letture/scritture dei payload della verifica.

La sospensione dell'Import era legata al surriscaldamento dello storage e alla necessità di rimozione sicura. Dopo il ripristino della ventola è stato riabilitato soltanto `Enabled` dell'attività, su richiesta Owner.

## Esito del ciclo

Avvio automatico **20/11/2026 18:43:49**, conclusione **18:55:02 Europe/Rome**, `LastTaskResult = 0`. Discovery 905 file senza errori di parsing; import su `F:\Astrofotografia`: 905 file già presenti verificati, 905 ACK esistenti verificati, zero errori, cancellazioni e overwrite.

**Zero nuove immagini, zero nuove copie:** verificati discovery e idempotenza, non il trasferimento di un nuovo file. Gli avvisi FWHM `NaN` del nome NINA non rappresentano errori di importazione.

## Continuità

Conservare launcher/backup locali e ricevute; verificare il primo ciclo con immagini nuove senza riavviare le elaborazioni. In caso di anomalia sospendere il solo Import, conservare le prove e non attivare automaticamente Morning Transfer.

Questa nota operativa non modifica promotion, gate storici, stato scientifico delle milestone o altri handover.

- [Evidenze, impronte e limiti](../architecture/evidence/AP-013B-OneDrive-Import-Resume-2026-11-20.md)
- [Runbook AP-013B](../architecture/validation/AP-013B-OneDrive-Transport-Operational-Acceptance.md)
- [Launcher nascosto](HANDOVER_2026-11-12-HIDDEN-DISCOVERY-IMPORT.md)
