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

if (-not (Test-Path -LiteralPath $TransferPlanPath -PathType Leaf)) { throw "Transfer plan not found: $TransferPlanPath" }
if (-not (Test-Path -LiteralPath $TransportRoot -PathType Container)) { throw "Transport root not found: $TransportRoot" }
if (-not (Test-Path -LiteralPath $DestinationRoot -PathType Container)) { throw "Destination root not found: $DestinationRoot" }

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
$manifests = Get-ChildItem -LiteralPath $TransportRoot -Filter '*.ready.json' -File |
    Sort-Object LastWriteTime |
    Select-Object -First $MaxFilesPerRun

foreach ($manifestFile in $manifests) {
    try {
        $manifest = Get-Content -LiteralPath $manifestFile.FullName -Raw | ConvertFrom-Json
        $fileName = [string]$manifest.FileName
        if (-not $planByName.ContainsKey($fileName)) {
            $results += [pscustomobject][ordered]@{
                Status = 'DEFER_NO_PLAN'
                ManifestPath = $manifestFile.FullName
                FileName = $fileName
                DestinationPath = $null
                Error = 'No matching transfer-plan entry.'
                SourceDeleted = $false
                TransportDeleted = $false
                OverwritePerformed = $false
            }
            continue
        }

        $entry = $planByName[$fileName]
        $destinationPath = [string]$entry.PlannedDestination
        if ([string]::IsNullOrWhiteSpace($destinationPath)) {
            throw "Transfer-plan destination is empty for $fileName"
        }

        $result = Import-DSGOneDriveTransportFile `
            -ManifestPath $manifestFile.FullName `
            -DestinationRoot $DestinationRoot `
            -DestinationPath $destinationPath

        $results += $result
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
$results | Export-Csv -LiteralPath $resultsPath -NoTypeInformation -Encoding UTF8

$summary = [pscustomobject][ordered]@{
    SchemaVersion = '1.0'
    RunId = $runId
    Mode = 'COPY_ONLY_ONEDRIVE_IMPORT'
    TransferPlanPath = $TransferPlanPath
    TransportRoot = $TransportRoot
    DestinationRoot = $DestinationRoot
    Requested = @($manifests).Count
    CopiedVerified = @($results | Where-Object { $_.Status -eq 'COPIED_VERIFIED' }).Count
    SkippedIdentical = @($results | Where-Object { $_.Status -eq 'SKIP_IDENTICAL' }).Count
    DeferredNoPlan = @($results | Where-Object { $_.Status -eq 'DEFER_NO_PLAN' }).Count
    Failed = @($results | Where-Object { $_.Status -eq 'FAILED' }).Count
    SourceFilesDeleted = 0
    TransportFilesDeleted = 0
    OverwritesPerformed = 0
    CompletedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
}

$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runDir 'import-manifest.json') -Encoding UTF8
$summary | Format-List
