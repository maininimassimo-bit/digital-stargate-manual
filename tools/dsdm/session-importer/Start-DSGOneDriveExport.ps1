[CmdletBinding()]
param(
    [string]$SourceRoot = 'D:\Images NINA\Target',
    [string]$TransportRoot = 'C:\Users\PrimaLuceLab\OneDrive - Massimo Mainini\Manciano\DigitalStarGate-Transport',
    [int]$MaxFilesPerRun = 10,
    [int]$StabilityDelaySeconds = 10,
    [string]$EvidenceRoot = "$env:USERPROFILE\DSG-Inventory\OneDriveExport"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Import-Module (Join-Path $PSScriptRoot 'DSG.OneDriveTransport.psm1') -Force

if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) { throw "Source root not found: $SourceRoot" }
if (-not (Test-Path -LiteralPath $TransportRoot -PathType Container)) { throw "Transport root not found: $TransportRoot" }
if ($MaxFilesPerRun -lt 1) { throw 'MaxFilesPerRun must be greater than zero.' }

$runId = 'DSG-OD-EXPORT-' + [guid]::NewGuid().ToString()
$runDir = Join-Path $EvidenceRoot $runId
New-Item -ItemType Directory -Path $runDir -Force | Out-Null

$results = @()
$alreadyReady = 0
$candidates = New-Object System.Collections.Generic.List[System.IO.FileInfo]

$sourceFiles = Get-ChildItem -LiteralPath $SourceRoot -Filter '*.xisf' -File |
    Sort-Object LastWriteTime, Name

foreach ($file in $sourceFiles) {
    if ($candidates.Count -ge $MaxFilesPerRun) { break }

    $transportPath = Join-Path $TransportRoot $file.Name
    $manifestPath = $transportPath + '.ready.json'
    $isCompleted = $false

    if (
        (Test-Path -LiteralPath $transportPath -PathType Leaf) -and
        (Test-Path -LiteralPath $manifestPath -PathType Leaf)
    ) {
        try {
            $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
            $transportItem = Get-Item -LiteralPath $transportPath -ErrorAction Stop

            $isCompleted = (
                [string]$manifest.State -eq 'READY' -and
                [string]$manifest.FileName -eq $file.Name -and
                [int64]$manifest.SizeBytes -eq [int64]$file.Length -and
                [int64]$transportItem.Length -eq [int64]$file.Length -and
                -not [string]::IsNullOrWhiteSpace([string]$manifest.Sha256)
            )
        }
        catch {
            $isCompleted = $false
        }
    }

    if ($isCompleted) {
        $alreadyReady++
        continue
    }

    $candidates.Add($file)
}

$files = @($candidates)

foreach ($file in $files) {
    try {
        $result = Export-DSGOneDriveTransportFile `
            -SourcePath $file.FullName `
            -TransportRoot $TransportRoot `
            -StabilityDelaySeconds $StabilityDelaySeconds
        $results += $result
    }
    catch {
        $results += [pscustomobject][ordered]@{
            Status = 'FAILED'
            SourcePath = $file.FullName
            TransportPath = $null
            ManifestPath = $null
            Error = $_.Exception.Message
            SourceDeleted = $false
        }
    }
}

$resultsPath = Join-Path $runDir 'export-results.csv'
$results | Export-Csv -LiteralPath $resultsPath -NoTypeInformation -Encoding UTF8

$summary = [pscustomobject][ordered]@{
    SchemaVersion = '1.0'
    RunId = $runId
    Mode = 'COPY_ONLY_ONEDRIVE_EXPORT'
    SourceRoot = $SourceRoot
    TransportRoot = $TransportRoot
    SourceFilesObserved = @($sourceFiles).Count
    AlreadyReadySkipped = $alreadyReady
    Requested = @($files).Count
    Ready = @($results | Where-Object { $_.Status -eq 'READY' }).Count
    Deferred = @($results | Where-Object { $_.Status -eq 'DEFER_UNSTABLE' }).Count
    Failed = @($results | Where-Object { $_.Status -eq 'FAILED' }).Count
    SourceFilesDeleted = 0
    CompletedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
}

$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runDir 'export-manifest.json') -Encoding UTF8
$summary | Format-List
