[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$CloudWatcherCsv = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    [string]$RuntimeRoot = 'C:\DigitalStarGate\TelemetryRuntime',
    [ValidateRange(5, 300)][int]$PollSeconds = 15,
    [ValidateRange(1, 3600)][int]$FreshnessSeconds = 60,
    [ValidateRange(0, 86400)][int]$DurationSeconds = 0
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$adapter = Join-Path $RepositoryRoot 'scripts\telemetry\Export-CloudWatcherObservatoryStatus.ps1'
if (-not (Test-Path -LiteralPath $adapter -PathType Leaf)) { throw "Adapter non trovato: $adapter" }
if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) { throw "CloudWatcher CSV non trovato: $CloudWatcherCsv" }

New-Item -ItemType Directory -Path $RuntimeRoot -Force | Out-Null
$projectionPath = Join-Path $RuntimeRoot 'observatory-status.json'
$tempPath = Join-Path $RuntimeRoot 'observatory-status.next.json'
$healthPath = Join-Path $RuntimeRoot 'producer-health.json'
$logPath = Join-Path $RuntimeRoot 'producer.log'

$startedAt = [datetime]::UtcNow
$deadline = if ($DurationSeconds -gt 0) { $startedAt.AddSeconds($DurationSeconds) } else { [datetime]::MaxValue }
$consecutiveFailures = 0
$lastSuccessUtc = $null
$lastError = $null

function Write-ProducerHealth {
    param([Parameter(Mandatory = $true)][string]$State)

    [ordered]@{
        schema_version = '1.0'
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
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $healthPath -Encoding UTF8
}

Write-ProducerHealth -State 'STARTING'
Add-Content -LiteralPath $logPath -Value ('{0} START computer={1} poll={2}s freshness={3}s' -f [datetime]::UtcNow.ToString('o'), $env:COMPUTERNAME, $PollSeconds, $FreshnessSeconds)

while ([datetime]::UtcNow -lt $deadline) {
    try {
        & $adapter -CloudWatcherCsv $CloudWatcherCsv -OutputPath $tempPath -FreshnessSeconds $FreshnessSeconds -SourceInstance $env:COMPUTERNAME | Out-Null
        $candidate = Get-Content -LiteralPath $tempPath -Raw | ConvertFrom-Json
        if ($candidate.schema_version -ne '1.1') { throw 'Projection schema inatteso.' }
        if ($candidate.safety.observed_state -ne 'UNKNOWN') { throw 'Safety invariant violata.' }

        Move-Item -LiteralPath $tempPath -Destination $projectionPath -Force
        $consecutiveFailures = 0
        $lastSuccessUtc = [datetime]::UtcNow.ToString('o')
        $lastError = $null
        Write-ProducerHealth -State 'RUNNING'
        Add-Content -LiteralPath $logPath -Value ('{0} OK observed={1} weather={2}/{3}' -f $lastSuccessUtc, $candidate.observed_at_utc, $candidate.systems.weather.state, $candidate.systems.weather.quality)
    }
    catch {
        $consecutiveFailures++
        $lastError = $_.Exception.Message
        if (Test-Path -LiteralPath $tempPath) { Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue }
        Write-ProducerHealth -State 'DEGRADED'
        Add-Content -LiteralPath $logPath -Value ('{0} ERROR failures={1} message={2}' -f [datetime]::UtcNow.ToString('o'), $consecutiveFailures, $lastError)
    }

    Start-Sleep -Seconds $PollSeconds
}

Write-ProducerHealth -State 'STOPPED'
Add-Content -LiteralPath $logPath -Value ('{0} STOP' -f [datetime]::UtcNow.ToString('o'))
