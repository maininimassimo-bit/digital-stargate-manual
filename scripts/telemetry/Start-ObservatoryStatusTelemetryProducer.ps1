[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$NinaProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\nina-observatory-status.json",
    [string]$CloudWatcherCsv = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    [string]$Phd2LogRoot = 'C:\Users\PrimaLuceLab\Documents\PHD2',
    [string]$RuntimeRoot = 'C:\DigitalStarGate\TelemetryRuntime',
    [ValidateRange(5, 300)][int]$PollSeconds = 15,
    [ValidateRange(1, 3600)][int]$FreshnessSeconds = 60,
    [ValidateRange(0, 86400)][int]$DurationSeconds = 0,
    [string]$PublishEndpoint = '',
    [ValidateRange(1, 120)][int]$PublishTimeoutSeconds = 10,
    [ValidateRange(0, 5)][int]$PublishMaxRetries = 2,
    [bool]$RuntimeEnabled = $false
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $RuntimeEnabled) {
    throw 'Runtime disabled by contract: pass -RuntimeEnabled $true only after the governed activation gate.'
}

$ninaAdapter = Join-Path $RepositoryRoot 'scripts\telemetry\Export-NinaObservatoryStatus.ps1'
$fallbackAdapter = Join-Path $RepositoryRoot 'scripts\telemetry\Export-CloudWatcherObservatoryStatus.ps1'
$publisher = Join-Path $RepositoryRoot 'scripts\telemetry\Publish-ObservatoryStatusTelemetry.ps1'
$phd2Adapter = Join-Path $RepositoryRoot 'scripts\telemetry\Export-Phd2GuidingStatus.ps1'
if (-not (Test-Path -LiteralPath $ninaAdapter -PathType Leaf)) { throw "Adapter NINA non trovato: $ninaAdapter" }
if (-not (Test-Path -LiteralPath $fallbackAdapter -PathType Leaf)) { throw "Adapter fallback CloudWatcher non trovato: $fallbackAdapter" }
if ($PublishEndpoint -and -not (Test-Path -LiteralPath $publisher -PathType Leaf)) { throw "Publisher non trovato: $publisher" }
if (-not (Test-Path -LiteralPath $phd2Adapter -PathType Leaf)) { throw "Adapter PHD2 non trovato: $phd2Adapter" }

New-Item -ItemType Directory -Path $RuntimeRoot -Force | Out-Null
$projectionPath = Join-Path $RuntimeRoot 'observatory-status.json'
$tempPath = Join-Path $RuntimeRoot 'observatory-status.next.json'
$healthPath = Join-Path $RuntimeRoot 'producer-health.json'
$logPath = Join-Path $RuntimeRoot 'producer.log'
$lockPath = Join-Path $RuntimeRoot 'producer.lock'
$lockHandle = $null

try {
    try {
        $lockHandle = [System.IO.File]::Open(
            $lockPath,
            [System.IO.FileMode]::OpenOrCreate,
            [System.IO.FileAccess]::ReadWrite,
            [System.IO.FileShare]::None)
    }
    catch [System.IO.IOException] {
        throw "Un altro producer Observatory Status sta gia usando RuntimeRoot '$RuntimeRoot'. Single-writer invariant: usa un RuntimeRoot separato per canary/dry-run oppure arresta prima l'istanza attiva."
    }

    $startedAt = [datetime]::UtcNow
    $deadline = if ($DurationSeconds -gt 0) { $startedAt.AddSeconds($DurationSeconds) } else { [datetime]::MaxValue }
    $consecutiveFailures = 0
    $lastSuccessUtc = $null
    $lastError = $null
    $activeSource = $null
    $fallbackCount = 0
    $publishEnabled = -not [string]::IsNullOrWhiteSpace($PublishEndpoint)
    $publishConsecutiveFailures = 0
    $lastPublishAttemptUtc = $null
    $lastPublishSuccessUtc = $null
    $lastPublishError = $null
    $lastPublishedCorrelationId = $null

    function Write-ProducerHealth {
        param([Parameter(Mandatory = $true)][string]$State)

        [ordered]@{
            schema_version = '1.1'
            component = 'DSG.ObservatoryStatusTelemetryProducer'
            computer = $env:COMPUTERNAME
            state = $State
            started_at_utc = $startedAt.ToString('o')
            updated_at_utc = [datetime]::UtcNow.ToString('o')
            last_success_utc = $script:lastSuccessUtc
            consecutive_failures = $script:consecutiveFailures
            last_error = $script:lastError
            projection_path = $projectionPath
            poll_seconds = $PollSeconds
            freshness_seconds = $FreshnessSeconds
            source = [ordered]@{
                primary = 'NINA_OBSERVATORY_TELEMETRY'
                fallback = 'CLOUDWATCHER_CSV'
                active = $script:activeSource
                fallback_count = $script:fallbackCount
            }
            transport = [ordered]@{
                enabled = $script:publishEnabled
                endpoint = if ($script:publishEnabled) { $PublishEndpoint } else { $null }
                last_attempt_utc = $script:lastPublishAttemptUtc
                last_success_utc = $script:lastPublishSuccessUtc
                consecutive_failures = $script:publishConsecutiveFailures
                last_error = $script:lastPublishError
                last_correlation_id = $script:lastPublishedCorrelationId
            }
        } | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $healthPath -Encoding UTF8
    }

    Write-ProducerHealth -State 'STARTING'
    Add-Content -LiteralPath $logPath -Value ('{0} START computer={1} poll={2}s freshness={3}s primary=NINA fallback=CLOUDWATCHER publish={4} single_writer=True' -f [datetime]::UtcNow.ToString('o'), $env:COMPUTERNAME, $PollSeconds, $FreshnessSeconds, $publishEnabled)

    while ([datetime]::UtcNow -lt $deadline) {
        $cycleState = 'RUNNING'
        try {
            $primaryError = $null
            try {
                & $ninaAdapter -NinaProjection $NinaProjection -OutputPath $tempPath -FreshnessSeconds $FreshnessSeconds -SourceInstance $env:COMPUTERNAME | Out-Null
                $candidate = Get-Content -LiteralPath $tempPath -Raw | ConvertFrom-Json
                if ($candidate.schema_version -ne '1.1') { throw 'Projection NINA schema inatteso.' }
                if ($candidate.quality -ne 'CURRENT') { throw "Projection NINA non corrente: $($candidate.quality)" }
                $activeSource = 'NINA_OBSERVATORY_TELEMETRY'
            }
            catch {
                $primaryError = $_.Exception.Message
                if (Test-Path -LiteralPath $tempPath) { Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue }
                if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) {
                    throw "NINA primary failed: $primaryError; CloudWatcher fallback unavailable: $CloudWatcherCsv"
                }
                & $fallbackAdapter -CloudWatcherCsv $CloudWatcherCsv -OutputPath $tempPath -FreshnessSeconds $FreshnessSeconds -SourceInstance $env:COMPUTERNAME | Out-Null
                $candidate = Get-Content -LiteralPath $tempPath -Raw | ConvertFrom-Json
                if ($candidate.schema_version -ne '1.1') { throw 'Projection fallback schema inatteso.' }
                $activeSource = 'CLOUDWATCHER_CSV'
                $fallbackCount++
                $cycleState = 'DEGRADED'
                Add-Content -LiteralPath $logPath -Value ('{0} FALLBACK primary_error={1}' -f [datetime]::UtcNow.ToString('o'), $primaryError)
            }

            $phd2ProjectionPath = Join-Path $RuntimeRoot 'phd2-guiding-status.next.json'
            try {
                & $phd2Adapter -Phd2LogRoot $Phd2LogRoot -OutputPath $phd2ProjectionPath -FreshnessSeconds $FreshnessSeconds -SourceInstance $env:COMPUTERNAME | Out-Null
                $guiding = Get-Content -LiteralPath $phd2ProjectionPath -Raw | ConvertFrom-Json
                Add-Member -InputObject $candidate.systems -MemberType NoteProperty -Name guiding -Value $guiding -Force
                if ($guiding.quality -ne 'CURRENT' -or $guiding.state -eq 'UNKNOWN') {
                    $cycleState = 'DEGRADED'
                }
            }
            catch {
                $guiding = [ordered]@{
                    schema_version = '1.0'
                    source_component = 'DSG.Phd2GuideLogAdapter'
                    source_instance = $env:COMPUTERNAME
                    observed_at_utc = $null
                    fresh_until_utc = $null
                    quality = 'UNKNOWN'
                    state = 'UNKNOWN'
                    profiles = @()
                    diagnostics = [ordered]@{
                        reason = $_.Exception.Message
                        no_hardware_commands = $true
                        safety_authority = 'LOCAL_PHYSICAL_INTERLOCKS'
                    }
                }
                Add-Member -InputObject $candidate.systems -MemberType NoteProperty -Name guiding -Value $guiding -Force
                $cycleState = 'DEGRADED'
                Add-Content -LiteralPath $logPath -Value ('{0} PHD2_ERROR message={1}' -f [datetime]::UtcNow.ToString('o'), $_.Exception.Message)
            }

            Move-Item -LiteralPath $tempPath -Destination $projectionPath -Force
            $consecutiveFailures = 0
            $lastSuccessUtc = [datetime]::UtcNow.ToString('o')
            $lastError = $primaryError
            Add-Content -LiteralPath $logPath -Value ('{0} OK source={1} observed={2} weather={3}/{4} safety={5} guiding={6}/{7}' -f $lastSuccessUtc, $activeSource, $candidate.observed_at_utc, $candidate.systems.weather.state, $candidate.systems.weather.quality, $candidate.safety.observed_state, $candidate.systems.guiding.state, $candidate.systems.guiding.quality)

            if ($publishEnabled) {
                $lastPublishAttemptUtc = [datetime]::UtcNow.ToString('o')
                try {
                    $publishOutput = & $publisher -ProjectionPath $projectionPath -Endpoint $PublishEndpoint -TimeoutSeconds $PublishTimeoutSeconds -MaxRetries $PublishMaxRetries -RuntimeEnabled $RuntimeEnabled
                    $publishConsecutiveFailures = 0
                    $lastPublishSuccessUtc = [datetime]::UtcNow.ToString('o')
                    $lastPublishError = $null
                    $lastPublishedCorrelationId = [string]$candidate.correlation_id
                    Add-Content -LiteralPath $logPath -Value ('{0} PUBLISH_OK correlation_id={1} result={2}' -f $lastPublishSuccessUtc, $lastPublishedCorrelationId, (($publishOutput -join ' ') -replace '[\r\n]+',' '))
                }
                catch {
                    $publishConsecutiveFailures++
                    $lastPublishError = $_.Exception.Message
                    $cycleState = 'DEGRADED'
                    Add-Content -LiteralPath $logPath -Value ('{0} PUBLISH_ERROR failures={1} message={2}' -f [datetime]::UtcNow.ToString('o'), $publishConsecutiveFailures, $lastPublishError)
                }
            }
        }
        catch {
            $consecutiveFailures++
            $lastError = $_.Exception.Message
            $cycleState = 'DEGRADED'
            if (Test-Path -LiteralPath $tempPath) { Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue }
            Add-Content -LiteralPath $logPath -Value ('{0} ERROR failures={1} message={2}' -f [datetime]::UtcNow.ToString('o'), $consecutiveFailures, $lastError)
        }

        Write-ProducerHealth -State $cycleState
        Start-Sleep -Seconds $PollSeconds
    }

    Write-ProducerHealth -State 'STOPPED'
    Add-Content -LiteralPath $logPath -Value ('{0} STOP' -f [datetime]::UtcNow.ToString('o'))
}
finally {
    if ($lockHandle) {
        $lockHandle.Dispose()
    }
}
