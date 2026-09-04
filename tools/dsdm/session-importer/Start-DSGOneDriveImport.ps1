[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$TransferPlanPath,
    [string]$TransportRoot = 'C:\Users\MassimoMainini\OneDrive - Massimo Mainini\Manciano\DigitalStarGate-Transport',
    [string]$DestinationRoot = 'F:\Astrofotografia',
    [int]$MaxFilesPerRun = 10,
    [string]$EvidenceRoot = "$env:USERPROFILE\DSG-Inventory\OneDriveImport"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Import-Module (Join-Path $PSScriptRoot 'DSG.OneDriveTransport.psm1') -Force
Import-Module (Join-Path $PSScriptRoot 'DSG.VerifiedTransportCleanup.psm1') -Force

if (-not (Test-Path -LiteralPath $TransferPlanPath -PathType Leaf)) { throw "Transfer plan not found: $TransferPlanPath" }
if (-not (Test-Path -LiteralPath $TransportRoot -PathType Container)) { throw "Transport root not found: $TransportRoot" }
if (-not (Test-Path -LiteralPath $DestinationRoot -PathType Container)) { throw "Destination root not found: $DestinationRoot" }
if ($MaxFilesPerRun -lt 1) { throw 'MaxFilesPerRun must be greater than zero.' }

function Write-DSGVerifiedImportAck {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ManifestPath,
        [Parameter(Mandatory = $true)][string]$DestinationPath,
        [Parameter(Mandatory = $true)][string]$CorrelationId
    )

    $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    $transportPath = Join-Path (Split-Path -Parent $ManifestPath) ([string]$manifest.FileName)
    $ackPath = $transportPath + '.imported.json'

    try {
        $ackResult = New-DSGDestinationVerificationAck `
            -ReadyManifestPath $ManifestPath `
            -DestinationPath $DestinationPath `
            -AckPath $ackPath `
            -CorrelationId $CorrelationId

        return [pscustomobject][ordered]@{
            Status = [string]$ackResult.Status
            ManifestPath = $ManifestPath
            DestinationPath = $DestinationPath
            AckPath = $ackPath
            Error = $null
        }
    }
    catch {
        return [pscustomobject][ordered]@{
            Status = 'ACK_FAILED'
            ManifestPath = $ManifestPath
            DestinationPath = $DestinationPath
            AckPath = $ackPath
            Error = $_.Exception.Message
        }
    }
}

$plan = Import-Csv -LiteralPath $TransferPlanPath
$planByName = @{}
foreach ($entry in $plan) {
    $name = if (-not [string]::IsNullOrWhiteSpace([string]$entry.FileName)) {
        [string]$entry.FileName
    }
    else {
        Split-Path -Leaf ([string]$entry.SourceRelativePath)
    }
    if (-not [string]::IsNullOrWhiteSpace($name)) {
        $planByName[$name] = $entry
    }
}

$runId = 'DSG-OD-IMPORT-' + [guid]::NewGuid().ToString()
$runDir = Join-Path $EvidenceRoot $runId
New-Item -ItemType Directory -Path $runDir -Force | Out-Null

$results = @()
$ackResults = @()
$alreadyImportedSkipped = 0
$deferredNoPlan = 0
$deferredPlanAction = 0
$deferredTransportNotReady = 0
$candidates = New-Object System.Collections.Generic.List[System.IO.FileInfo]
$allowedPlanActions = @(
    'COPY_NEW',
    'REVIEW_DESTINATION_COLLISION'
)

$manifestFiles = Get-ChildItem -LiteralPath $TransportRoot -Filter '*.ready.json' -File |
    Sort-Object LastWriteTime, Name

foreach ($manifestFile in $manifestFiles) {
    if ($candidates.Count -ge $MaxFilesPerRun) { break }

    try {
        $manifest = Get-Content -LiteralPath $manifestFile.FullName -Raw | ConvertFrom-Json
        $fileName = [string]$manifest.FileName

        if ([string]$manifest.State -ne 'READY' -or [string]::IsNullOrWhiteSpace($fileName)) {
            $results += [pscustomobject][ordered]@{
                Status = 'FAILED'
                ManifestPath = $manifestFile.FullName
                FileName = $fileName
                DestinationPath = $null
                Error = 'Manifest is not a valid READY manifest.'
                SourceDeleted = $false
                TransportDeleted = $false
                OverwritePerformed = $false
            }
            continue
        }

        if (-not $planByName.ContainsKey($fileName)) {
            $deferredNoPlan++
            continue
        }

        $entry = $planByName[$fileName]
        $plannedAction = [string]$entry.PlannedAction
        if ($plannedAction -notin $allowedPlanActions) {
            $deferredPlanAction++
            continue
        }

        $destinationPath = [string]$entry.PlannedDestination
        if ([string]::IsNullOrWhiteSpace($destinationPath)) {
            $results += [pscustomobject][ordered]@{
                Status = 'FAILED'
                ManifestPath = $manifestFile.FullName
                FileName = $fileName
                DestinationPath = $null
                Error = 'Transfer-plan destination is empty.'
                SourceDeleted = $false
                TransportDeleted = $false
                OverwritePerformed = $false
            }
            continue
        }

        $transportPath = Join-Path $TransportRoot $fileName
        if (-not (Test-Path -LiteralPath $transportPath -PathType Leaf)) {
            $deferredTransportNotReady++
            continue
        }

        if (Test-Path -LiteralPath $destinationPath -PathType Leaf) {
            $destinationItem = Get-Item -LiteralPath $destinationPath -ErrorAction Stop
            if ([int64]$destinationItem.Length -eq [int64]$manifest.SizeBytes) {
                $destinationHash = Get-DSGTransportSha256 -LiteralPath $destinationPath
                if ($destinationHash -eq ([string]$manifest.Sha256).ToLowerInvariant()) {
                    $alreadyImportedSkipped++
                    $ackResults += Write-DSGVerifiedImportAck `
                        -ManifestPath $manifestFile.FullName `
                        -DestinationPath $destinationPath `
                        -CorrelationId $runId
                    continue
                }
            }
        }

        $candidates.Add($manifestFile)
    }
    catch {
        $results += [pscustomobject][ordered]@{
            Status = 'FAILED'
            ManifestPath = $manifestFile.FullName
            FileName = $manifestFile.Name
            DestinationPath = $null
            Error = $_.Exception.Message
            SourceDeleted = $false
            TransportDeleted = $false
            OverwritePerformed = $false
        }
    }
}

$manifests = @($candidates)

foreach ($manifestFile in $manifests) {
    try {
        $manifest = Get-Content -LiteralPath $manifestFile.FullName -Raw | ConvertFrom-Json
        $fileName = [string]$manifest.FileName
        $entry = $planByName[$fileName]
        $destinationPath = [string]$entry.PlannedDestination

        $result = Import-DSGOneDriveTransportFile `
            -ManifestPath $manifestFile.FullName `
            -DestinationRoot $DestinationRoot `
            -DestinationPath $destinationPath

        $results += $result

        if ($result.Status -in @('COPIED_VERIFIED', 'SKIP_IDENTICAL')) {
            $ackResults += Write-DSGVerifiedImportAck `
                -ManifestPath $manifestFile.FullName `
                -DestinationPath $destinationPath `
                -CorrelationId $runId
        }
    }
    catch {
        $results += [pscustomobject][ordered]@{
            Status = 'FAILED'
            ManifestPath = $manifestFile.FullName
            FileName = $manifestFile.Name
            DestinationPath = $null
            Error = $_.Exception.Message
            SourceDeleted = $false
            TransportDeleted = $false
            OverwritePerformed = $false
        }
    }
}

$resultsPath = Join-Path $runDir 'import-results.csv'
$ackResultsPath = Join-Path $runDir 'ack-results.csv'
$results | Export-Csv -LiteralPath $resultsPath -NoTypeInformation -Encoding UTF8
$ackResults | Export-Csv -LiteralPath $ackResultsPath -NoTypeInformation -Encoding UTF8

$summary = [pscustomobject][ordered]@{
    SchemaVersion = '1.2'
    RunId = $runId
    Mode = 'COPY_ONLY_ONEDRIVE_IMPORT_WITH_VERIFICATION_ACK'
    TransferPlanPath = $TransferPlanPath
    TransportRoot = $TransportRoot
    DestinationRoot = $DestinationRoot
    ReadyManifestsObserved = @($manifestFiles).Count
    AlreadyImportedSkipped = $alreadyImportedSkipped
    DeferredNoPlan = $deferredNoPlan
    DeferredPlanAction = $deferredPlanAction
    DeferredTransportNotReady = $deferredTransportNotReady
    Requested = @($manifests).Count
    CopiedVerified = @($results | Where-Object { $_.Status -eq 'COPIED_VERIFIED' }).Count
    SkippedIdentical = @($results | Where-Object { $_.Status -eq 'SKIP_IDENTICAL' }).Count
    Failed = @($results | Where-Object { $_.Status -eq 'FAILED' }).Count
    AckCreated = @($ackResults | Where-Object { $_.Status -eq 'ACK_CREATED' }).Count
    AckExistingVerified = @($ackResults | Where-Object { $_.Status -eq 'ACK_EXISTS_VERIFIED' }).Count
    AckFailed = @($ackResults | Where-Object { $_.Status -eq 'ACK_FAILED' }).Count
    SourceFilesDeleted = 0
    TransportFilesDeleted = 0
    OverwritesPerformed = 0
    CompletedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
}

$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runDir 'import-manifest.json') -Encoding UTF8
$summary | Format-List
