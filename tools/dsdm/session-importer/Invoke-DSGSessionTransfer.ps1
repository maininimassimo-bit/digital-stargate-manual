[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)][string]$ConfigurationPath,
    [Parameter(Mandatory = $true)][string]$TransferPlanPath,
    [switch]$IgnoreOperatingWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-DSGTimeSpanToday {
    param([Parameter(Mandatory = $true)][string]$Value)

    $parsed = [TimeSpan]::Zero
    if (-not [TimeSpan]::TryParseExact(
        $Value,
        'hh\:mm',
        [System.Globalization.CultureInfo]::InvariantCulture,
        [ref]$parsed
    )) {
        throw "Time value '$Value' must use HH:mm."
    }

    return $parsed
}

function Test-DSGOperatingWindow {
    param(
        [Parameter(Mandatory = $true)]$Window,
        [Parameter(Mandatory = $true)][datetime]$LocalNow
    )

    $notBefore = ConvertTo-DSGTimeSpanToday -Value $Window.notBeforeLocal
    $doNotStartAfter = ConvertTo-DSGTimeSpanToday -Value $Window.doNotStartAfterLocal
    $current = $LocalNow.TimeOfDay

    return [pscustomobject]@{
        IsAllowed = ($current -ge $notBefore -and $current -le $doNotStartAfter)
        LocalNow = $LocalNow.ToString('o')
        NotBeforeLocal = $Window.notBeforeLocal
        DoNotStartAfterLocal = $Window.doNotStartAfterLocal
        MustFinishBeforeLocal = $Window.mustFinishBeforeLocal
    }
}

function New-DSGIdentifier {
    param([Parameter(Mandatory = $true)][string]$Entity)
    return ('DSG-{0}-{1}' -f $Entity.ToUpperInvariant(), ([guid]::NewGuid().ToString()))
}

if (-not (Test-Path -LiteralPath $ConfigurationPath -PathType Leaf)) {
    throw "Configuration file not found: $ConfigurationPath"
}
if (-not (Test-Path -LiteralPath $TransferPlanPath -PathType Leaf)) {
    throw "Transfer plan not found: $TransferPlanPath"
}

$configuration = Get-Content -LiteralPath $ConfigurationPath -Raw | ConvertFrom-Json

if ($configuration.mode -ne 'COPY_ONLY') {
    throw "Configuration mode must be COPY_ONLY. Observed: $($configuration.mode)"
}
if ($configuration.safety.allowTransferMode -ne $true) {
    throw 'Safety violation: allowTransferMode must be true.'
}
if ($configuration.safety.allowDestinationWrites -ne $true) {
    throw 'Safety violation: allowDestinationWrites must be true.'
}
if ($configuration.safety.sourceCleanupAuthorized -ne $false) {
    throw 'Safety violation: sourceCleanupAuthorized must remain false.'
}
if ($configuration.safety.overwriteExisting -ne $false) {
    throw 'Safety violation: overwriteExisting must remain false.'
}

$windowResult = Test-DSGOperatingWindow -Window $configuration.window -LocalNow (Get-Date)
if (-not $IgnoreOperatingWindow -and -not $windowResult.IsAllowed) {
    throw 'Current local time is outside the configured transfer window.'
}

$destinationRoot = [string]$configuration.destination.rootPath
$evidenceRoot = [string]$configuration.evidence.outputRoot
$stabilityDelaySeconds = [int]$configuration.transfer.stabilityObservationDelaySeconds
$maxFiles = [int]$configuration.transfer.maxFilesPerRun

if (-not (Test-Path -LiteralPath $destinationRoot -PathType Container)) {
    throw "Destination root is unavailable: $destinationRoot"
}

$destinationItem = Get-Item -LiteralPath $destinationRoot -ErrorAction Stop
if (-not [string]::IsNullOrWhiteSpace([string]$configuration.destination.expectedVolumeLabel)) {
    $drive = Get-PSDrive -Name $destinationItem.PSDrive.Name -ErrorAction Stop
    $volume = Get-Volume -DriveLetter $drive.Name -ErrorAction Stop
    if ([string]$volume.FileSystemLabel -ne [string]$configuration.destination.expectedVolumeLabel) {
        throw "Destination volume label mismatch. Expected '$($configuration.destination.expectedVolumeLabel)', observed '$($volume.FileSystemLabel)'."
    }
}

$modulePath = Join-Path $PSScriptRoot 'DSG.SessionTransfer.psm1'
Import-Module $modulePath -Force

$planEntries = @(Import-Csv -LiteralPath $TransferPlanPath)
$eligibleEntries = @(
    $planEntries |
        Where-Object { $_.PlannedAction -eq 'COPY_NEW' } |
        Select-Object -First $maxFiles
)

if ($eligibleEntries.Count -eq 0) {
    throw 'Transfer plan contains no eligible COPY_NEW entries.'
}

$runId = New-DSGIdentifier -Entity 'TRANSFER-RUN'
$runDirectory = Join-Path $evidenceRoot $runId

# Evidence is intentionally produced even for -WhatIf runs.
# WhatIf applies only to scientific destination writes.
New-Item -ItemType Directory -Path $runDirectory -Force -WhatIf:$false | Out-Null

$startedAtUtc = (Get-Date).ToUniversalTime()
$results = @()
$runStatus = 'COMPLETED'

foreach ($entry in $eligibleEntries) {
    $sourcePath = [string]$entry.SourceFullPath
    if ([string]::IsNullOrWhiteSpace($sourcePath)) {
        $sourcePath = Join-Path ([string]$configuration.source.rootPath) ([string]$entry.SourceRelativePath)
    }

    $destinationPath = [string]$entry.PlannedDestination

    try {
        if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
            throw "Source file not found: $sourcePath"
        }

        $firstObservation = New-DSGFileObservation -LiteralPath $sourcePath
        Start-Sleep -Seconds $stabilityDelaySeconds
        $secondObservation = New-DSGFileObservation -LiteralPath $sourcePath

        if (-not (Test-DSGStableObservation -FirstObservation $firstObservation -SecondObservation $secondObservation)) {
            $results += [pscustomobject][ordered]@{
                SourcePath = $sourcePath
                DestinationPath = $destinationPath
                Status = 'DEFER_UNSTABLE'
                Error = $null
                SourceDeleted = $false
            }
            continue
        }

        $copyResult = Invoke-DSGCopyOnlyFile `
            -SourcePath $sourcePath `
            -DestinationRoot $destinationRoot `
            -DestinationPath $destinationPath `
            -WhatIf:$WhatIfPreference

        if ($WhatIfPreference) {
            $results += [pscustomobject][ordered]@{
                SourcePath = $sourcePath
                DestinationPath = $destinationPath
                Status = 'WHATIF'
                Error = $null
                SourceDeleted = $false
            }
        }
        else {
            $results += $copyResult
        }
    }
    catch {
        $runStatus = 'FAILED'
        $results += [pscustomobject][ordered]@{
            SourcePath = $sourcePath
            DestinationPath = $destinationPath
            Status = 'FAILED'
            Error = $_.Exception.Message
            SourceDeleted = $false
        }
        break
    }
}

$completedAtUtc = (Get-Date).ToUniversalTime()
$manifest = [pscustomobject][ordered]@{
    SchemaVersion = '1.0'
    RunId = $runId
    Mode = 'COPY_ONLY'
    Status = $runStatus
    StartedAtUtc = $startedAtUtc.ToString('o')
    CompletedAtUtc = $completedAtUtc.ToString('o')
    OperatingWindow = $windowResult
    ConfigurationPath = (Resolve-Path -LiteralPath $ConfigurationPath).Path
    TransferPlanPath = (Resolve-Path -LiteralPath $TransferPlanPath).Path
    DestinationRoot = $destinationRoot
    RequestedFileCount = $eligibleEntries.Count
    ResultCount = $results.Count
    CopiedVerifiedCount = @($results | Where-Object { $_.Status -eq 'COPIED_VERIFIED' }).Count
    SkippedIdenticalCount = @($results | Where-Object { $_.Status -eq 'SKIP_IDENTICAL' }).Count
    DeferredUnstableCount = @($results | Where-Object { $_.Status -eq 'DEFER_UNSTABLE' }).Count
    FailedCount = @($results | Where-Object { $_.Status -eq 'FAILED' }).Count
    WhatIfCount = @($results | Where-Object { $_.Status -eq 'WHATIF' }).Count
    SourceFilesDeleted = 0
    Safety = [ordered]@{
        SourceCleanupAuthorized = $false
        OverwriteExisting = $false
        HashAlgorithm = 'SHA-256'
        CopyOnly = $true
    }
    Results = @($results)
}

$manifestPath = Join-Path $runDirectory 'transfer-manifest.json'
$manifestCsvPath = Join-Path $runDirectory 'transfer-results.csv'
$checksumPath = Join-Path $runDirectory 'evidence-checksums.txt'

$manifest |
    ConvertTo-Json -Depth 8 |
    Set-Content -LiteralPath $manifestPath -Encoding UTF8 -WhatIf:$false

$results |
    Export-Csv -LiteralPath $manifestCsvPath -NoTypeInformation -Encoding UTF8 -WhatIf:$false

$checksumLines = @()
foreach ($evidenceFile in @($manifestPath, $manifestCsvPath)) {
    $hash = Get-FileHash -LiteralPath $evidenceFile -Algorithm SHA256
    $checksumLines += ('{0}  {1}' -f $hash.Hash.ToLowerInvariant(), (Split-Path -Leaf $evidenceFile))
}
$checksumLines | Set-Content -LiteralPath $checksumPath -Encoding ASCII -WhatIf:$false

Write-Host ''
Write-Host 'DSG COPY-ONLY TRANSFER RUN COMPLETED' -ForegroundColor Green
Write-Host "Run ID: $runId"
Write-Host "Status: $runStatus"
Write-Host "Requested files: $($eligibleEntries.Count)"
Write-Host "Copied and verified: $($manifest.CopiedVerifiedCount)"
Write-Host "Skipped identical: $($manifest.SkippedIdenticalCount)"
Write-Host "Deferred unstable: $($manifest.DeferredUnstableCount)"
Write-Host "Failed: $($manifest.FailedCount)"
Write-Host "WhatIf: $($manifest.WhatIfCount)"
Write-Host "Source files deleted: 0"
Write-Host "Evidence directory: $runDirectory"

if ($runStatus -ne 'COMPLETED') {
    throw "Transfer run failed. Evidence directory: $runDirectory"
}

$manifest
