[CmdletBinding()]
param(
    [string]$CloudWatcherCsv = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [ValidateRange(60, 3600)][int]$DurationSeconds = 300,
    [ValidateRange(1, 60)][int]$PollSeconds = 5
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Open-SharedReadStream {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::Open($Path,[System.IO.FileMode]::Open,[System.IO.FileAccess]::Read,[System.IO.FileShare]::ReadWrite)
}

function Get-CloudWatcherHeaderAndLastLineShared {
    param([Parameter(Mandatory = $true)][string]$Path)

    $stream = $null
    $reader = $null
    try {
        $stream = Open-SharedReadStream -Path $Path
        $reader = New-Object System.IO.StreamReader($stream)
        $header = $reader.ReadLine()
        $last = $null
        while (-not $reader.EndOfStream) {
            $line = $reader.ReadLine()
            if (-not [string]::IsNullOrWhiteSpace($line)) { $last = $line }
        }
        return [pscustomobject]@{ Header = $header; LastLine = $last }
    }
    finally {
        if ($reader) { $reader.Dispose() }
        elseif ($stream) { $stream.Dispose() }
    }
}

function Parse-CloudWatcherTimestampUtc {
    param(
        [Parameter(Mandatory = $true)][string]$HeaderLine,
        [Parameter(Mandatory = $true)][string]$CsvLine
    )

    $row = @($HeaderLine, $CsvLine) | ConvertFrom-Csv | Select-Object -First 1
    if (-not $row) { throw 'Impossibile interpretare la riga CloudWatcher.' }
    if ([string]::IsNullOrWhiteSpace($row.Date) -or [string]::IsNullOrWhiteSpace($row.Time)) {
        throw 'La riga CloudWatcher non contiene Date/Time validi.'
    }

    $local = [datetime]::ParseExact(
        ('{0} {1}' -f $row.Date.Trim(), $row.Time.Trim()),
        'yyyy-MM-dd HH:mm:ss',
        [System.Globalization.CultureInfo]::InvariantCulture)

    $zone = $null
    foreach ($id in @('W. Europe Standard Time','Europe/Rome')) {
        try { $zone = [TimeZoneInfo]::FindSystemTimeZoneById($id); break } catch { }
    }
    if (-not $zone) { throw 'Timezone Europe/Rome non disponibile.' }
    return [TimeZoneInfo]::ConvertTimeToUtc($local, $zone)
}

if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) {
    throw "CloudWatcher CSV non trovato: $CloudWatcherCsv"
}

$timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-cadence-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null
$csvOut = Join-Path $bundle 'cadence-samples.csv'
$jsonOut = Join-Path $bundle 'cadence-summary.json'
$transcript = Join-Path $bundle 'cadence-transcript.txt'

Start-Transcript -LiteralPath $transcript -Force | Out-Null
try {
    Write-Output 'Digital StarGate CloudWatcher cadence pilot - READ ONLY'
    Write-Output ('Source: {0}' -f $CloudWatcherCsv)
    Write-Output ('Duration: {0}s; Poll: {1}s' -f $DurationSeconds, $PollSeconds)

    $deadline = [datetime]::UtcNow.AddSeconds($DurationSeconds)
    $samples = New-Object System.Collections.Generic.List[object]
    $observedChanges = New-Object System.Collections.Generic.List[datetime]
    $lastFileLength = -1L
    $lastObservedUtc = $null

    while ([datetime]::UtcNow -lt $deadline) {
        $now = [datetime]::UtcNow
        $info = Get-Item -LiteralPath $CloudWatcherCsv
        $tail = Get-CloudWatcherHeaderAndLastLineShared -Path $CloudWatcherCsv
        $observedUtc = if ($tail.LastLine) { Parse-CloudWatcherTimestampUtc -HeaderLine $tail.Header -CsvLine $tail.LastLine } else { $null }

        $changed = ($info.Length -ne $lastFileLength) -or ($lastObservedUtc -and $observedUtc -and $observedUtc -ne $lastObservedUtc)
        if ($observedUtc -and (($null -eq $lastObservedUtc) -or ($observedUtc -ne $lastObservedUtc))) {
            $observedChanges.Add($observedUtc)
        }

        $samples.Add([pscustomobject]@{
            sampled_at_utc = $now.ToString('o')
            file_length = $info.Length
            observed_at_utc = if ($observedUtc) { $observedUtc.ToString('o') } else { $null }
            age_seconds = if ($observedUtc) { [math]::Round(($now - $observedUtc).TotalSeconds, 3) } else { $null }
            changed = [bool]$changed
        })

        $lastFileLength = $info.Length
        $lastObservedUtc = $observedUtc
        Start-Sleep -Seconds $PollSeconds
    }

    $intervals = New-Object System.Collections.Generic.List[double]
    for ($i = 1; $i -lt $observedChanges.Count; $i++) {
        $intervals.Add(($observedChanges[$i] - $observedChanges[$i-1]).TotalSeconds)
    }

    $samples | Export-Csv -LiteralPath $csvOut -NoTypeInformation -Encoding UTF8

    $sorted = @($intervals | Sort-Object)
    $maxInterval = if ($sorted.Count -gt 0) { [double]$sorted[-1] } else { $null }
    $avgInterval = if ($sorted.Count -gt 0) { [math]::Round((($sorted | Measure-Object -Average).Average),3) } else { $null }
    $p95 = if ($sorted.Count -gt 0) {
        $idx = [math]::Ceiling($sorted.Count * 0.95) - 1
        [double]$sorted[[math]::Max(0,$idx)]
    } else { $null }

    $recommendedFreshness = if ($maxInterval) { [int][math]::Ceiling([math]::Max($maxInterval * 2, $p95 * 2)) } else { $null }

    $summary = [ordered]@{
        schema_version = '1.0'
        pilot = 'DSG-OBS-RT-001-CADENCE'
        generated_at_utc = [datetime]::UtcNow.ToString('o')
        computer = $env:COMPUTERNAME
        source = $CloudWatcherCsv
        duration_seconds = $DurationSeconds
        poll_seconds = $PollSeconds
        sample_count = $samples.Count
        observed_change_count = $observedChanges.Count
        interval_count = $intervals.Count
        average_interval_seconds = $avgInterval
        p95_interval_seconds = $p95
        max_interval_seconds = $maxInterval
        recommended_freshness_seconds = $recommendedFreshness
        note = 'Recommendation is evidence-derived from this pilot only and must be reviewed before becoming a governed operational threshold.'
    }
    $summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $jsonOut -Encoding UTF8

    Write-Output ('Observed changes: {0}' -f $observedChanges.Count)
    Write-Output ('Average interval: {0}s' -f $avgInterval)
    Write-Output ('P95 interval: {0}s' -f $p95)
    Write-Output ('Max interval: {0}s' -f $maxInterval)
    Write-Output ('Recommended freshness candidate: {0}s' -f $recommendedFreshness)
    Write-Output ('Evidence bundle: {0}' -f $bundle)
    Write-Output 'CADENCE PILOT RESULT: PASS'
}
finally {
    Stop-Transcript | Out-Null
}
