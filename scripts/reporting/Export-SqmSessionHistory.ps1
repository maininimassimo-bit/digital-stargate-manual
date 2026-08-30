[CmdletBinding()]
param(
    [Parameter(Mandatory)][datetime]$SessionStart,
    [Parameter(Mandatory)][datetime]$SessionEnd,
    [Parameter(Mandatory)][string]$OutputDirectory,
    [string]$HistoryPath = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\sqm-history.ndjson'),
    [int]$ExpectedCadenceSeconds = 30
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($SessionEnd -le $SessionStart) { throw 'SessionEnd deve essere successivo a SessionStart.' }
if ($ExpectedCadenceSeconds -le 0) { throw 'ExpectedCadenceSeconds deve essere maggiore di zero.' }

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$rawOutput = Join-Path $OutputDirectory 'sqm-history.ndjson'
$summaryOutput = Join-Path $OutputDirectory 'sqm-summary.json'
$startUtc = $SessionStart.ToUniversalTime()
$endUtc = $SessionEnd.ToUniversalTime()
$valid = New-Object System.Collections.Generic.List[object]

if (Test-Path -LiteralPath $HistoryPath) {
    foreach ($line in Get-Content -LiteralPath $HistoryPath) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $sample = $line | ConvertFrom-Json } catch { continue }
        $observed = [datetime]::MinValue
        if (-not [datetime]::TryParse([string]$sample.observedAtUtc, [ref]$observed)) { continue }
        $observed = $observed.ToUniversalTime()
        if ($observed -lt $startUtc -or $observed -gt $endUtc) { continue }
        if ([string]$sample.quality -ne 'CURRENT') { continue }
        $value = 0.0
        if (-not [double]::TryParse([string]$sample.sqmMagArcsec2, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$value)) { continue }
        if ($value -le 0) { continue }
        $valid.Add([pscustomobject]@{ observedAtUtc=$observed; sqmMagArcsec2=$value; source=[string]$sample.source; serial=[string]$sample.serial; firmware=[string]$sample.firmware; quality='CURRENT'; raw=$line })
    }
}

$ordered = @($valid | Sort-Object observedAtUtc -Unique)
Set-Content -LiteralPath $rawOutput -Value @($ordered | ForEach-Object { $_.raw }) -Encoding UTF8
$durationSeconds = [math]::Max(0.0, ($endUtc - $startUtc).TotalSeconds)
$expectedSamples = if ($durationSeconds -eq 0) { 0 } else { [math]::Max(1, [math]::Floor($durationSeconds / $ExpectedCadenceSeconds) + 1) }
$coverage = if ($expectedSamples -gt 0) { [math]::Min(1.0, $ordered.Count / [double]$expectedSamples) } else { 0.0 }

if ($ordered.Count -gt 0) {
    $values = @($ordered | ForEach-Object { $_.sqmMagArcsec2 } | Sort-Object)
    $middle = [math]::Floor($values.Count / 2)
    $median = if (($values.Count % 2) -eq 1) { $values[$middle] } else { ($values[$middle - 1] + $values[$middle]) / 2.0 }
    $summary = [ordered]@{
        schema_version = '1.0'
        start = $ordered[0].observedAtUtc.ToString('o')
        end = $ordered[-1].observedAtUtc.ToString('o')
        min = [math]::Round(($values | Measure-Object -Minimum).Minimum, 4)
        max = [math]::Round(($values | Measure-Object -Maximum).Maximum, 4)
        mean = [math]::Round(($values | Measure-Object -Average).Average, 4)
        median = [math]::Round($median, 4)
        valid_samples = $ordered.Count
        temporal_coverage = [math]::Round($coverage, 4)
        expected_cadence_seconds = $ExpectedCadenceSeconds
        source = (($ordered | Select-Object -ExpandProperty source -Unique) -join '; ')
        serial = (($ordered | Select-Object -ExpandProperty serial -Unique) -join '; ')
        firmware = (($ordered | Select-Object -ExpandProperty firmware -Unique) -join '; ')
        quality = 'AVAILABLE'
    }
} else {
    $summary = [ordered]@{
        schema_version = '1.0'; start = $null; end = $null; min = $null; max = $null; mean = $null; median = $null
        valid_samples = 0; temporal_coverage = 0.0; expected_cadence_seconds = $ExpectedCadenceSeconds
        source = 'AAG CloudWatcher SOLO HTTP / lightmpsas'; serial = $null; firmware = $null; quality = 'UNKNOWN'
    }
}

$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryOutput -Encoding UTF8
Write-Host "SQM session history: $($ordered.Count) valid samples; coverage=$($summary.temporal_coverage); quality=$($summary.quality)"
Write-Host "SQM raw: $rawOutput"
Write-Host "SQM summary: $summaryOutput"
