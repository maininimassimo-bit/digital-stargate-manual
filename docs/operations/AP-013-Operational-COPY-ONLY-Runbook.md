# AP-013 — Operational COPY_ONLY Promotion Runbook

| Campo | Valore |
|---|---|
| Runbook ID | `RB-AP013-COPYONLY-001` |
| Package | AP-013 — Scientific Image Repository Architecture |
| Modalità | `COPY_ONLY` |
| Stato | Pre-production / promotion controlled |
| Source cleanup | Prohibited |
| Overwrite | Prohibited |
| Data | 06/08/2026 |

## 1. Scopo

Definire il percorso controllato per passare dal pilot reale limitato alla produzione continuativa `COPY_ONLY`, senza introdurre cancellazioni della sorgente, overwrite o bypass dei controlli di integrità.

Questo runbook non costituisce da solo autorizzazione alla produzione. L'attivazione richiede la chiusura dei gate indicati nel Transfer Readiness Gate, la four-eyes review, l'OAT e una disposizione esplicita di Operational Acceptance.

## 2. Boundary operativi non negoziabili

La produzione deve mantenere:

- `mode = COPY_ONLY`;
- `sourceCleanupAuthorized = false`;
- `overwriteExisting = false`;
- `allowTransferMode = true`;
- `allowDestinationWrites = true`;
- `hashAlgorithm = SHA-256`;
- staging con estensione `.dsg-partial`;
- evidence bundle per ogni run;
- operating window governata;
- stop immediato al primo errore.

Non sono consentiti:

- cancellazione o spostamento dei file sorgente;
- overwrite silenzioso;
- esecuzione fuori finestra con `-IgnoreOperatingWindow` in esercizio ordinario;
- modifica manuale del manifest dopo la chiusura del run;
- esecuzione con destinazione o volume non verificati.

## 3. Prerequisiti per la promozione

Prima dell'attivazione devono risultare chiusi o formalmente accettati:

1. TR-17 — four-eyes review del pilot;
2. TR-01 — volume, spazio libero e root di destinazione verificati;
3. TR-02 — ACL e root containment verificati;
4. TR-09 — retry idempotente e ripresa controllata;
5. TR-10 — rollback del solo staging incompleto;
6. TR-13 — test negativo fuori finestra;
7. TR-14 — performance baseline su dataset rappresentativo;
8. OAT AP-013;
9. Operational Acceptance.

## 4. Preparazione della configurazione operativa

Partire da una copia locale del file:

```text
tools/dsdm/session-importer/session-transfer.sample.json
```

Creare sul PC principale:

```text
tools/dsdm/session-importer/session-transfer.production.json
```

Il file locale non deve contenere credenziali e non deve essere committato se include percorsi o dati specifici non destinati alla documentazione pubblica.

Il parametro `transfer.maxFilesPerRun` deve essere impostato al batch size approvato dall'OAT e dalla performance baseline. Non utilizzare un valore arbitrario e non rimuovere il limite senza una modifica testata dell'orchestratore.

Esempio strutturale:

```json
{
  "schemaVersion": "1.0",
  "mode": "COPY_ONLY",
  "source": {
    "sourceId": "SRC-EAGLE30154-NINA-001",
    "host": "EAGLE30154",
    "rootPath": "\\\\EAGLE30154\\NINA-Images"
  },
  "destination": {
    "storageVolumeId": "DSG-STORAGE-ACTIVE-F",
    "rootPath": "F:\\Astrofotografia",
    "expectedVolumeLabel": "Elements"
  },
  "evidence": {
    "outputRoot": "C:\\Users\\MassimoMainini\\DSG-Inventory\\SessionTransfer"
  },
  "window": {
    "notBeforeLocal": "07:30",
    "doNotStartAfterLocal": "08:05",
    "mustFinishBeforeLocal": "08:15"
  },
  "transfer": {
    "stabilityObservationDelaySeconds": 10,
    "maxFilesPerRun": "<OAT_APPROVED_POSITIVE_INTEGER>",
    "hashAlgorithm": "SHA-256",
    "stagingExtension": ".dsg-partial"
  },
  "safety": {
    "sourceCleanupAuthorized": false,
    "allowTransferMode": true,
    "allowDestinationWrites": true,
    "overwriteExisting": false
  }
}
```

La stringa placeholder deve essere sostituita con un intero positivo approvato prima dell'esecuzione.

## 5. Preflight giornaliero

Eseguire sul PC principale:

```powershell
$ConfigurationPath = 'C:\DigitalStarGate\digital-stargate-manual-ap013\tools\dsdm\session-importer\session-transfer.production.json'
$TransferPlanPath = '<PERCORSO_TRANSFER_PLAN_APPROVATO>'
$DestinationRoot = 'F:\Astrofotografia'
$EvidenceRoot = 'C:\Users\MassimoMainini\DSG-Inventory\SessionTransfer'

Test-Path -LiteralPath $ConfigurationPath -PathType Leaf
Test-Path -LiteralPath $TransferPlanPath -PathType Leaf
Test-Path -LiteralPath $DestinationRoot -PathType Container
Test-Path -LiteralPath $EvidenceRoot -PathType Container
Get-Volume -DriveLetter F | Select-Object DriveLetter, FileSystemLabel, HealthStatus, SizeRemaining, Size
```

Verificare inoltre che la configurazione mantenga i flag di sicurezza:

```powershell
$Configuration = Get-Content -LiteralPath $ConfigurationPath -Raw | ConvertFrom-Json

[pscustomobject]@{
    Mode                    = $Configuration.mode
    SourceCleanupAuthorized = $Configuration.safety.sourceCleanupAuthorized
    OverwriteExisting       = $Configuration.safety.overwriteExisting
    HashAlgorithm           = $Configuration.transfer.hashAlgorithm
    MaxFilesPerRun          = $Configuration.transfer.maxFilesPerRun
}
```

## 6. Dry run obbligatorio dopo ogni modifica

Dopo qualunque modifica a configurazione, script o piano:

```powershell
& .\tools\dsdm\session-importer\Invoke-DSGSessionTransfer.ps1 `
  -ConfigurationPath $ConfigurationPath `
  -TransferPlanPath $TransferPlanPath `
  -WhatIf
```

Il dry run deve produrre evidence, non deve copiare file e deve riportare:

- `Status = COMPLETED`;
- `WhatIfCount > 0`;
- `SourceFilesDeleted = 0`;
- `FailedCount = 0`.

## 7. Esecuzione operativa

Solo dopo preflight e dry run positivi:

```powershell
& .\tools\dsdm\session-importer\Invoke-DSGSessionTransfer.ps1 `
  -ConfigurationPath $ConfigurationPath `
  -TransferPlanPath $TransferPlanPath
```

Non usare `-IgnoreOperatingWindow` nell'esercizio ordinario.

## 8. Verifica post-run

Individuare l'ultima cartella evidence:

```powershell
$Run = Get-ChildItem -LiteralPath $EvidenceRoot -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

$Manifest = Get-Content -LiteralPath (Join-Path $Run.FullName 'transfer-manifest.json') -Raw | ConvertFrom-Json
$Manifest | ConvertTo-Json -Depth 20
```

Il run è accettabile solo se:

```powershell
$Checks = [ordered]@{
    ModeCopyOnly           = $Manifest.Mode -eq 'COPY_ONLY'
    StatusCompleted        = $Manifest.Status -eq 'COMPLETED'
    NoFailures             = $Manifest.FailedCount -eq 0
    NotWhatIf              = $Manifest.WhatIfCount -eq 0
    NoSourceDeletion       = $Manifest.SourceFilesDeleted -eq 0
    CleanupNotAuthorized   = -not $Manifest.Safety.SourceCleanupAuthorized
    OverwriteNotAuthorized = -not $Manifest.Safety.OverwriteExisting
}

$Checks.GetEnumerator() | ForEach-Object {
    [pscustomobject]@{ Check = $_.Key; Passed = $_.Value }
} | Format-Table -AutoSize

if ($Checks.Values -notcontains $false) {
    'OPERATIONAL COPY_ONLY RUN: PASSED'
} else {
    'OPERATIONAL COPY_ONLY RUN: FAILED OR INCOMPLETE'
}
```

## 9. Evidence bundle integrity

Verificare i checksum:

```powershell
Push-Location $Run.FullName
Get-Content .\evidence-checksums.txt
Get-FileHash .\transfer-manifest.json -Algorithm SHA256
Get-FileHash .\transfer-results.csv -Algorithm SHA256
Pop-Location
```

Gli hash ricalcolati devono coincidere con `evidence-checksums.txt`.

## 10. Stop conditions

Interrompere la produzione e non rilanciare automaticamente se si verifica uno dei seguenti eventi:

- `Status = FAILED`;
- `FailedCount > 0`;
- mismatch SHA-256;
- volume label inattesa;
- spazio insufficiente;
- destinazione non disponibile;
- `CONFLICT` su un file esistente;
- file `.dsg-partial` residuo;
- sorgente instabile;
- manifest o evidence bundle incompleti;
- modifica inattesa dei flag di sicurezza.

## 11. Rollback operativo

Il rollback non cancella mai la sorgente e non rimuove file destinazione verificati.

Azioni consentite:

1. fermare l'esecuzione o disabilitare la schedulazione;
2. ripristinare la configurazione precedentemente accettata;
3. rimuovere esclusivamente file `.dsg-partial` dopo verifica manuale;
4. conservare integralmente l'evidence bundle del run fallito;
5. rigenerare il transfer plan;
6. eseguire nuovamente un dry run;
7. rilanciare solo dopo disposizione dell'operatore responsabile.

## 12. Schedulazione Windows

La schedulazione automatica deve essere creata solo dopo Operational Acceptance.

La task deve:

- eseguire PowerShell sul PC principale;
- usare percorsi assoluti per script, configurazione e transfer plan;
- non utilizzare `-IgnoreOperatingWindow`;
- essere eseguita con un account autorizzato soltanto alla lettura della sorgente e alla scrittura nella root governata;
- registrare exit code e output;
- non avviare una seconda istanza se la precedente è ancora in esecuzione;
- essere disabilitabile immediatamente come rollback.

## 13. Four-eyes review

Il revisore indipendente deve verificare:

- configurazione e flag di sicurezza;
- transfer plan approvato;
- manifest finale;
- risultati CSV;
- checksum del bundle;
- almeno un confronto SHA-256 sorgente/destinazione;
- `SourceFilesDeleted = 0`;
- assenza di overwrite;
- assenza di staging residuo.

La review deve essere registrata in un documento versionato con nome, data, decisione e condizioni.

## 14. Disposizione corrente

**Pilot reale limitato: PASSED.**

**Runbook di promozione: AVAILABLE.**

**Produzione continuativa COPY_ONLY: NOT YET AUTHORIZED.**

**Source cleanup: PROHIBITED.**
