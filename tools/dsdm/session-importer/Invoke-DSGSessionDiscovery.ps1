[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$ConfigurationPath = (Join-Path $PSScriptRoot 'session-importer.sample.json'),

    [Parameter(Mandatory = $false)]
    [string]$SourcePath,

    [Parameter(Mandatory = $false)]
    [string]$OutputRoot,

    [Parameter(Mandatory = $false)]
    [switch]$IgnoreOperatingWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-DSGSafePathSegment {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $invalidCharacters = [System.IO.Path]::GetInvalidFileNameChars()
    $builder = [System.Text.StringBuilder]::new()

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
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

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
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        $Window,

        [Parameter(Mandatory = $true)]
        [datetime]$LocalNow
    )

    $notBefore = ConvertTo-DSGTimeSpanToday -Value $Window.notBeforeLocal
    $doNotStartAfter = ConvertTo-DSGTimeSpanToday -Value $Window.doNotStartAfterLocal
    $current = $LocalNow.TimeOfDay

    [pscustomobject]@{
        IsAllowed = ($current -ge $notBefore -and $current -le $doNotStartAfter)
        LocalNow = $LocalNow.ToString('o')
        NotBeforeLocal = $Window.notBeforeLocal
        DoNotStartAfterLocal = $Window.doNotStartAfterLocal
        MustFinishBeforeLocal = $Window.mustFinishBeforeLocal
    }
}

function New-DSGIdentifier {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Entity
    )

    return 'DSG-{0}-{1}' -f $Entity.ToUpperInvariant(), ([guid]::NewGuid().ToString())
}

if (-not (Test-Path -LiteralPath $ConfigurationPath -PathType Leaf)) {
    throw "Configuration file not found: $ConfigurationPath"
}

$configuration = Get-Content -LiteralPath $ConfigurationPath -Raw | ConvertFrom-Json

if ($configuration.mode -ne 'DRY_RUN') {
    throw "Only DRY_RUN mode is supported by this implementation. Observed: $($configuration.mode)"
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
    throw "Current local time is outside the configured discovery window. Use -IgnoreOperatingWindow only for an explicitly controlled test."
}

$modulePath = Join-Path $PSScriptRoot 'DSG.SessionImporter.psm1'
Import-Module $modulePath -Force

$runId = New-DSGIdentifier -Entity 'DISCOVERY-RUN'
$runDirectory = Join-Path $effectiveOutputRoot $runId
New-Item -ItemType Directory -Path $runDirectory -Force | Out-Null

$startedAtUtc = (Get-Date).ToUniversalTime()
$allowedExtensions = @($configuration.source.allowedExtensions | ForEach-Object { $_.ToLowerInvariant() })
$minimumStableMinutes = [int]$configuration.source.minimumStableMinutes
$knownTelescopes = @($configuration.parser.knownTelescopes)
$useDateSubfolders = [bool]$configuration.destination.useDateSubfolders
$destinationRoot = [string]$configuration.destination.rootPath

$files = @(
    Get-ChildItem -LiteralPath $effectiveSourcePath -File -Recurse -ErrorAction Stop |
        Where-Object { $allowedExtensions -contains $_.Extension.ToLowerInvariant() } |
        Sort-Object FullName
)

$entries = [System.Collections.Generic.List[object]]::new()

foreach ($file in $files) {
    $parsed = ConvertFrom-DSGNinaFileName `
        -FileName $file.Name `
        -KnownTelescopes $knownTelescopes

    $ageMinutes = ((Get-Date) - $file.LastWriteTime).TotalMinutes
    $stabilityStatus = if ($ageMinutes -ge $minimumStableMinutes) {
        'STABLE_BY_AGE'
    }
    else {
        'DEFER_UNSTABLE'
    }

    $observingDate = $null
    if ($parsed.DateTimeObserved -match '^(?<date>\d{4}-\d{2}-\d{2})_') {
        $observingDate = $Matches['date']
    }

    $targetName = if ($parsed.ParseStatus -eq 'PARSED') {
        [string]$parsed.Target
    }
    else {
        '_UNRESOLVED'
    }

    $safeTarget = ConvertTo-DSGSafePathSegment -Value $targetName
    $imageTypeDirectory = switch ($parsed.ImageType) {
        'LIGHT' { 'Light' }
        'DARK' { 'Dark' }
        'FLAT' { 'Flat' }
        'BIAS' { 'Bias' }
        'DARKFLAT' { 'DarkFlat' }
        default { '_Unclassified' }
    }

    $destinationDirectory = Join-Path $destinationRoot $safeTarget
    $destinationDirectory = Join-Path $destinationDirectory $imageTypeDirectory

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

    $relativePath = $file.FullName.Substring($effectiveSourcePath.TrimEnd('\').Length).TrimStart('\')

    $entries.Add([pscustomobject][ordered]@{
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
        SessionKey = '{0}|{1}|{2}' -f $targetName, $observingDate, $parsed.Telescope
        PlannedDestination = $plannedDestination
        PlannedAction = $action
        ParseErrors = @($parsed.Errors)
    })
}

$sessionGroups = @(
    $entries |
        Group-Object -Property SessionKey |
        ForEach-Object {
            $groupEntries = @($_.Group)
            $first = $groupEntries[0]
            $imageTypeSummary = [ordered]@{}
            $filterSummary = [ordered]@{}

            foreach ($imageTypeGroup in @($groupEntries | Group-Object ImageType)) {
                $key = if ([string]::IsNullOrWhiteSpace([string]$imageTypeGroup.Name)) { 'UNKNOWN' } else { $imageTypeGroup.Name }
                $imageTypeSummary[$key] = $imageTypeGroup.Count
            }

            foreach ($filterGroup in @($groupEntries | Group-Object Filter)) {
                $key = if ([string]::IsNullOrWhiteSpace([string]$filterGroup.Name)) { 'UNKNOWN' } else { $filterGroup.Name }
                $filterSummary[$key] = $filterGroup.Count
            }

            [pscustomobject][ordered]@{
                SessionId = New-DSGIdentifier -Entity 'SESSION'
                SessionKey = $_.Name
                Target = $first.Target
                Telescope = $first.Telescope
                ObservingDate = $first.ObservingDate
                FileCount = $groupEntries.Count
                TotalBytes = [int64](($groupEntries | Measure-Object -Property SizeBytes -Sum).Sum)
                TotalExposureSeconds = [double](($groupEntries | Where-Object { $_.ImageType -eq 'LIGHT' } | Measure-Object -Property ExposureSeconds -Sum).Sum)
                ImageTypeSummary = $imageTypeSummary
                FilterSummary = $filterSummary
                StableFileCount = @($groupEntries | Where-Object { $_.StabilityStatus -eq 'STABLE_BY_AGE' }).Count
                AmbiguousFileCount = @($groupEntries | Where-Object { $_.ParseStatus -eq 'AMBIGUOUS' }).Count
                FailedFileCount = @($groupEntries | Where-Object { $_.ParseStatus -eq 'FAILED' }).Count
                PlannedCopyCount = @($groupEntries | Where-Object { $_.PlannedAction -eq 'COPY_NEW' }).Count
                BlockingFindingCount = @($groupEntries | Where-Object {
                    $_.PlannedAction -in @(
                        'DEFER_UNSTABLE',
                        'QUARANTINE',
                        'REVIEW_PARSE_AMBIGUITY',
                        'REVIEW_DESTINATION_COLLISION'
                    )
                }).Count
            }
        }
)

$completedAtUtc = (Get-Date).ToUniversalTime()

$summary = [pscustomobject][ordered]@{
    SchemaVersion = '1.0'
    RunId = $runId
    Mode = 'DRY_RUN'
    SourcePath = $effectiveSourcePath
    DestinationRoot = $destinationRoot
    StartedAtUtc = $startedAtUtc.ToString('o')
    CompletedAtUtc = $completedAtUtc.ToString('o')
    OperatingWindow = $windowResult
    FileCount = $entries.Count
    TotalBytes = [int64](($entries | Measure-Object -Property SizeBytes -Sum).Sum)
    SessionCount = $sessionGroups.Count
    ParsedCount = @($entries | Where-Object { $_.ParseStatus -eq 'PARSED' }).Count
    AmbiguousCount = @($entries | Where-Object { $_.ParseStatus -eq 'AMBIGUOUS' }).Count
    FailedCount = @($entries | Where-Object { $_.ParseStatus -eq 'FAILED' }).Count
    StableByAgeCount = @($entries | Where-Object { $_.StabilityStatus -eq 'STABLE_BY_AGE' }).Count
    DeferredUnstableCount = @($entries | Where-Object { $_.StabilityStatus -eq 'DEFER_UNSTABLE' }).Count
    CopyNewCount = @($entries | Where-Object { $_.PlannedAction -eq 'COPY_NEW' }).Count
    CollisionReviewCount = @($entries | Where-Object { $_.PlannedAction -eq 'REVIEW_DESTINATION_COLLISION' }).Count
    Safety = [ordered]@{
        SourceCleanupAuthorized = $false
        DestinationWritesPerformed = $false
        ScientificFilesCopied = 0
        ScientificFilesModified = 0
    }
    Limitations = @(
        'Stability is assessed from file age in this version; repeated size observation is not yet implemented.',
        'Destination collision checks compare path existence only; size and hash comparison are not yet implemented.',
        'No session merge across midnight is performed in this version.',
        'No scientific file is copied or modified.'
    )
}

$entriesJsonPath = Join-Path $runDirectory 'discovery-entries.json'
$entriesCsvPath = Join-Path $runDirectory 'transfer-plan.csv'
$sessionsJsonPath = Join-Path $runDirectory 'session-summary.json'
$summaryJsonPath = Join-Path $runDirectory 'discovery-run.json'

$entries | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $entriesJsonPath -Encoding UTF8
$entries | Select-Object `
    SourceRelativePath,
    FileName,
    SizeBytes,
    StabilityStatus,
    ParseStatus,
    ImageType,
    Target,
    Telescope,
    Filter,
    ObservingDate,
    PlannedDestination,
    PlannedAction |
    Export-Csv -LiteralPath $entriesCsvPath -NoTypeInformation -Encoding UTF8
$sessionGroups | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $sessionsJsonPath -Encoding UTF8
$summary | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $summaryJsonPath -Encoding UTF8

$evidenceFiles = @(
    $entriesJsonPath,
    $entriesCsvPath,
    $sessionsJsonPath,
    $summaryJsonPath
)

$checksumPath = Join-Path $runDirectory 'evidence-checksums.txt'
$checksumLines = foreach ($evidenceFile in $evidenceFiles) {
    $hash = Get-FileHash -LiteralPath $evidenceFile -Algorithm SHA256
    '{0}  {1}' -f $hash.Hash.ToLowerInvariant(), (Split-Path -Leaf $evidenceFile)
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
Write-Host "Planned COPY_NEW actions: $($summary.CopyNewCount)"
Write-Host "Evidence directory: $runDirectory"
Write-Host ''
Write-Host 'No scientific files were copied, moved, renamed, deleted or modified.' -ForegroundColor Cyan

[pscustomobject]@{
    RunId = $runId
    EvidenceDirectory = $runDirectory
    Summary = $summary
    Sessions = $sessionGroups
}
