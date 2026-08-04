[CmdletBinding()]
param(
    [string]$ConfigurationPath = (Join-Path $PSScriptRoot 'session-importer.sample.json'),
    [string]$SourcePath,
    [string]$OutputRoot,
    [switch]$IgnoreOperatingWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-DSGSafePathSegment {
    param([Parameter(Mandatory = $true)][string]$Value)

    $builder = New-Object System.Text.StringBuilder
    $invalidCharacters = [System.IO.Path]::GetInvalidFileNameChars()

    foreach ($character in $Value.ToCharArray()) {
        if ($invalidCharacters -contains $character) {
            [void]$builder.Append('_')
        }
        else {
            [void]$builder.Append($character)
        }
    }

    $safeValue = $builder.ToString().Trim().TrimEnd('.')
    if ([string]::IsNullOrWhiteSpace($safeValue)) {
        return '_UNRESOLVED'
    }

    return $safeValue
}

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

function Get-DSGCount {
    param([object[]]$Items)
    return @($Items).Count
}

function Get-DSGInt64Sum {
    param(
        [object[]]$Items,
        [Parameter(Mandatory = $true)][string]$PropertyName
    )

    [int64]$sum = 0
    foreach ($item in @($Items)) {
        if ($null -ne $item -and $null -ne $item.$PropertyName) {
            $sum += [int64]$item.$PropertyName
        }
    }

    return $sum
}

function Get-DSGDoubleSum {
    param(
        [object[]]$Items,
        [Parameter(Mandatory = $true)][string]$PropertyName
    )

    [double]$sum = 0
    foreach ($item in @($Items)) {
        if ($null -ne $item -and $null -ne $item.$PropertyName) {
            $sum += [double]$item.$PropertyName
        }
    }

    return $sum
}

if (-not (Test-Path -LiteralPath $ConfigurationPath -PathType Leaf)) {
    throw "Configuration file not found: $ConfigurationPath"
}

$configuration = Get-Content -LiteralPath $ConfigurationPath -Raw | ConvertFrom-Json

if ($configuration.mode -ne 'DRY_RUN') {
    throw "Only DRY_RUN mode is supported. Observed: $($configuration.mode)"
}
if ($configuration.safety.allowTransferMode -ne $false) {
    throw 'Safety violation: allowTransferMode must be false.'
}
if ($configuration.safety.allowDestinationWrites -ne $false) {
    throw 'Safety violation: allowDestinationWrites must be false.'
}
if ($configuration.safety.sourceCleanupAuthorized -ne $false) {
    throw 'Safety violation: sourceCleanupAuthorized must be false.'
}

$effectiveSourcePath = if ($PSBoundParameters.ContainsKey('SourcePath')) {
    $SourcePath
}
else {
    [string]$configuration.source.rootPath
}

$effectiveOutputRoot = if ($PSBoundParameters.ContainsKey('OutputRoot')) {
    $OutputRoot
}
else {
    [string]$configuration.evidence.outputRoot
}

if (-not (Test-Path -LiteralPath $effectiveSourcePath -PathType Container)) {
    throw "Source path is unavailable: $effectiveSourcePath"
}

$windowResult = Test-DSGOperatingWindow -Window $configuration.window -LocalNow (Get-Date)
if (-not $IgnoreOperatingWindow -and -not $windowResult.IsAllowed) {
    throw 'Current local time is outside the configured discovery window.'
}

$modulePath = Join-Path $PSScriptRoot 'DSG.SessionImporter.psm1'
Import-Module $modulePath -Force

$sourceRootItem = Get-Item -LiteralPath $effectiveSourcePath -ErrorAction Stop
$sourceRootProviderPath = $sourceRootItem.FullName.TrimEnd('\')

$runId = New-DSGIdentifier -Entity 'DISCOVERY-RUN'
$runDirectory = Join-Path $effectiveOutputRoot $runId
New-Item -ItemType Directory -Path $runDirectory -Force | Out-Null

$startedAtUtc = (Get-Date).ToUniversalTime()
$allowedExtensions = @($configuration.source.allowedExtensions | ForEach-Object { ([string]$_).ToLowerInvariant() })
$minimumStableMinutes = [int]$configuration.source.minimumStableMinutes
$knownTelescopes = @($configuration.parser.knownTelescopes)
$useDateSubfolders = [bool]$configuration.destination.useDateSubfolders
$destinationRoot = [string]$configuration.destination.rootPath

$files = @(
    Get-ChildItem -LiteralPath $effectiveSourcePath -File -Recurse -ErrorAction Stop |
        Where-Object { $allowedExtensions -contains $_.Extension.ToLowerInvariant() } |
        Sort-Object FullName
)

$entries = @()

foreach ($file in $files) {
    $parsed = ConvertFrom-DSGNinaFileName -FileName $file.Name -KnownTelescopes $knownTelescopes

    $ageMinutes = ((Get-Date) - $file.LastWriteTime).TotalMinutes
    $stabilityStatus = if ($ageMinutes -ge $minimumStableMinutes) { 'STABLE_BY_AGE' } else { 'DEFER_UNSTABLE' }

    $observingDate = $null
    if ($parsed.DateTimeObserved -match '^(?<date>\d{4}-\d{2}-\d{2})_') {
        $observingDate = $Matches['date']
    }

    $targetName = if ($parsed.ParseStatus -eq 'PARSED') { [string]$parsed.Target } else { '_UNRESOLVED' }
    $safeTarget = ConvertTo-DSGSafePathSegment -Value $targetName

    $imageTypeDirectory = switch ($parsed.ImageType) {
        'LIGHT' { 'Light' }
        'DARK' { 'Dark' }
        'FLAT' { 'Flat' }
        'BIAS' { 'Bias' }
        'DARKFLAT' { 'DarkFlat' }
        default { '_Unclassified' }
    }

    $destinationDirectory = Join-Path (Join-Path $destinationRoot $safeTarget) $imageTypeDirectory
    if ($useDateSubfolders -and -not [string]::IsNullOrWhiteSpace($observingDate)) {
        $destinationDirectory = Join-Path $destinationDirectory $observingDate
    }

    $plannedDestination = Join-Path $destinationDirectory $file.Name

    $action = if ($stabilityStatus -ne 'STABLE_BY_AGE') {
        'DEFER_UNSTABLE'
    }
    elseif ($parsed.ParseStatus -eq 'FAILED') {
        'QUARANTINE'
    }
    elseif ($parsed.ParseStatus -eq 'AMBIGUOUS') {
        'REVIEW_PARSE_AMBIGUITY'
    }
    elseif (Test-Path -LiteralPath $plannedDestination -PathType Leaf) {
        'REVIEW_DESTINATION_COLLISION'
    }
    else {
        'COPY_NEW'
    }

    $relativePath = $file.Name
    if ($file.FullName.StartsWith($sourceRootProviderPath, [System.StringComparison]::OrdinalIgnoreCase)) {
        $relativePath = $file.FullName.Substring($sourceRootProviderPath.Length).TrimStart('\')
    }

    $entries += [pscustomobject][ordered]@{
        EntryId = New-DSGIdentifier -Entity 'DISCOVERY-ENTRY'
        SourceRelativePath = $relativePath
        SourceFullPath = $file.FullName
        FileName = $file.Name
        Extension = $file.Extension
        SizeBytes = [int64]$file.Length
        CreatedAtObserved = $file.CreationTimeUtc.ToString('o')
        ModifiedAtObserved = $file.LastWriteTimeUtc.ToString('o')
        AgeMinutes = [math]::Round($ageMinutes, 2)
        StabilityStatus = $stabilityStatus
        ParseStatus = $parsed.ParseStatus
        ImageType = $parsed.ImageType
        Target = $parsed.Target
        Telescope = $parsed.Telescope
        Filter = $parsed.Filter
        ExposureSeconds = $parsed.ExposureSeconds
        Gain = $parsed.Gain
        Offset = $parsed.Offset
        SensorTemperatureC = $parsed.SensorTemperatureC
        FrameNumber = $parsed.FrameNumber
        DateTimeObserved = $parsed.DateTimeObserved
        ObservingDate = $observingDate
        FwhmObserved = $parsed.FwhmObserved
        FocusPosition = $parsed.FocusPosition
        SessionKey = ('{0}|{1}|{2}' -f $targetName, $observingDate, $parsed.Telescope)
        PlannedDestination = $plannedDestination
        PlannedAction = $action
        ParseErrors = @($parsed.Errors)
        ParseWarnings = @($parsed.Warnings)
    }
}

$sessionGroups = @()
foreach ($group in @($entries | Group-Object -Property SessionKey)) {
    $groupEntries = @($group.Group)
    if ($groupEntries.Count -eq 0) {
        continue
    }

    $first = $groupEntries[0]
    $imageTypeSummary = [ordered]@{}
    $filterSummary = [ordered]@{}

    foreach ($imageTypeGroup in @($groupEntries | Group-Object ImageType)) {
        $key = if ([string]::IsNullOrWhiteSpace([string]$imageTypeGroup.Name)) { 'UNKNOWN' } else { [string]$imageTypeGroup.Name }
        $imageTypeSummary[$key] = $imageTypeGroup.Count
    }

    foreach ($filterGroup in @($groupEntries | Group-Object Filter)) {
        $key = if ([string]::IsNullOrWhiteSpace([string]$filterGroup.Name)) { 'UNKNOWN' } else { [string]$filterGroup.Name }
        $filterSummary[$key] = $filterGroup.Count
    }

    $lightEntries = @($groupEntries | Where-Object { $_.ImageType -eq 'LIGHT' })
    $blockingEntries = @($groupEntries | Where-Object {
        $_.PlannedAction -in @(
            'DEFER_UNSTABLE',
            'QUARANTINE',
            'REVIEW_PARSE_AMBIGUITY',
            'REVIEW_DESTINATION_COLLISION'
        )
    })

    $sessionGroups += [pscustomobject][ordered]@{
        SessionId = New-DSGIdentifier -Entity 'SESSION'
        SessionKey = $group.Name
        Target = $first.Target
        Telescope = $first.Telescope
        ObservingDate = $first.ObservingDate
        FileCount = $groupEntries.Count
        TotalBytes = Get-DSGInt64Sum -Items $groupEntries -PropertyName 'SizeBytes'
        TotalExposureSeconds = Get-DSGDoubleSum -Items $lightEntries -PropertyName 'ExposureSeconds'
        ImageTypeSummary = $imageTypeSummary
        FilterSummary = $filterSummary
        StableFileCount = Get-DSGCount -Items @($groupEntries | Where-Object { $_.StabilityStatus -eq 'STABLE_BY_AGE' })
        AmbiguousFileCount = Get-DSGCount -Items @($groupEntries | Where-Object { $_.ParseStatus -eq 'AMBIGUOUS' })
        FailedFileCount = Get-DSGCount -Items @($groupEntries | Where-Object { $_.ParseStatus -eq 'FAILED' })
        WarningFileCount = Get-DSGCount -Items @($groupEntries | Where-Object { $_.ParseWarnings.Count -gt 0 })
        PlannedCopyCount = Get-DSGCount -Items @($groupEntries | Where-Object { $_.PlannedAction -eq 'COPY_NEW' })
        BlockingFindingCount = $blockingEntries.Count
    }
}

$completedAtUtc = (Get-Date).ToUniversalTime()
$summary = [pscustomobject][ordered]@{
    SchemaVersion = '1.1'
    RunId = $runId
    Mode = 'DRY_RUN'
    SourcePath = $effectiveSourcePath
    SourceProviderPath = $sourceRootProviderPath
    DestinationRoot = $destinationRoot
    StartedAtUtc = $startedAtUtc.ToString('o')
    CompletedAtUtc = $completedAtUtc.ToString('o')
    OperatingWindow = $windowResult
    FileCount = $entries.Count
    TotalBytes = Get-DSGInt64Sum -Items $entries -PropertyName 'SizeBytes'
    SessionCount = $sessionGroups.Count
    ParsedCount = Get-DSGCount -Items @($entries | Where-Object { $_.ParseStatus -eq 'PARSED' })
    AmbiguousCount = Get-DSGCount -Items @($entries | Where-Object { $_.ParseStatus -eq 'AMBIGUOUS' })
    FailedCount = Get-DSGCount -Items @($entries | Where-Object { $_.ParseStatus -eq 'FAILED' })
    WarningCount = Get-DSGCount -Items @($entries | Where-Object { $_.ParseWarnings.Count -gt 0 })
    StableByAgeCount = Get-DSGCount -Items @($entries | Where-Object { $_.StabilityStatus -eq 'STABLE_BY_AGE' })
    DeferredUnstableCount = Get-DSGCount -Items @($entries | Where-Object { $_.StabilityStatus -eq 'DEFER_UNSTABLE' })
    CopyNewCount = Get-DSGCount -Items @($entries | Where-Object { $_.PlannedAction -eq 'COPY_NEW' })
    CollisionReviewCount = Get-DSGCount -Items @($entries | Where-Object { $_.PlannedAction -eq 'REVIEW_DESTINATION_COLLISION' })
    Safety = [ordered]@{
        SourceCleanupAuthorized = $false
        DestinationWritesPerformed = $false
        ScientificFilesCopied = 0
        ScientificFilesModified = 0
    }
    Limitations = @(
        'Stability is assessed from file age; repeated size observation is not yet implemented.',
        'Destination collision checks compare path existence only; size and hash comparison are not yet implemented.',
        'No session merge across midnight is performed.',
        'No scientific file is copied or modified.'
    )
}

$entriesJsonPath = Join-Path $runDirectory 'discovery-entries.json'
$entriesCsvPath = Join-Path $runDirectory 'transfer-plan.csv'
$sessionsJsonPath = Join-Path $runDirectory 'session-summary.json'
$summaryJsonPath = Join-Path $runDirectory 'discovery-run.json'

ConvertTo-Json -InputObject @($entries) -Depth 8 | Set-Content -LiteralPath $entriesJsonPath -Encoding UTF8
$entries | Select-Object SourceRelativePath, FileName, SizeBytes, StabilityStatus, ParseStatus, ImageType, Target, Telescope, Filter, ObservingDate, PlannedDestination, PlannedAction | Export-Csv -LiteralPath $entriesCsvPath -NoTypeInformation -Encoding UTF8
ConvertTo-Json -InputObject @($sessionGroups) -Depth 8 | Set-Content -LiteralPath $sessionsJsonPath -Encoding UTF8
ConvertTo-Json -InputObject $summary -Depth 8 | Set-Content -LiteralPath $summaryJsonPath -Encoding UTF8

$evidenceFiles = @($entriesJsonPath, $entriesCsvPath, $sessionsJsonPath, $summaryJsonPath)
$checksumPath = Join-Path $runDirectory 'evidence-checksums.txt'
$checksumLines = @()
foreach ($evidenceFile in $evidenceFiles) {
    $hash = Get-FileHash -LiteralPath $evidenceFile -Algorithm SHA256
    $checksumLines += ('{0}  {1}' -f $hash.Hash.ToLowerInvariant(), (Split-Path -Leaf $evidenceFile))
}
$checksumLines | Set-Content -LiteralPath $checksumPath -Encoding ASCII

Write-Host ''
Write-Host 'DSG SESSION DISCOVERY COMPLETED' -ForegroundColor Green
Write-Host "Run ID: $runId"
Write-Host "Source files: $($entries.Count)"
Write-Host "Sessions: $($sessionGroups.Count)"
Write-Host "Parsed: $($summary.ParsedCount)"
Write-Host "Ambiguous: $($summary.AmbiguousCount)"
Write-Host "Failed: $($summary.FailedCount)"
Write-Host "Warnings: $($summary.WarningCount)"
Write-Host "Planned COPY_NEW actions: $($summary.CopyNewCount)"
Write-Host "Evidence directory: $runDirectory"
Write-Host ''
Write-Host 'No scientific files were copied, moved, renamed, deleted or modified.' -ForegroundColor Cyan

[pscustomobject]@{
    RunId = $runId
    EvidenceDirectory = $runDirectory
    Summary = $summary
    Sessions = @($sessionGroups)
}
