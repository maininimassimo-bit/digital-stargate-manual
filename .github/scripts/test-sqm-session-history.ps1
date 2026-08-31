[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$scriptPath = Join-Path $repoRoot 'scripts\reporting\Export-SqmSessionHistory.ps1'
if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) { throw "Aggregator not found: $scriptPath" }

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("dsg-sqm-regression-{0}" -f [guid]::NewGuid().ToString('N'))
$historyPath = Join-Path $tempRoot 'sqm-history.ndjson'
$outputDir = Join-Path $tempRoot 'out'
New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null

try {
    $rows = @(
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:00:00Z","sqmMagArcsec2":18.40,"source":"AAG CloudWatcher SOLO HTTP / lightmpsas","serial":"2382","firmware":"5.88","quality":"CURRENT"}',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:00:30Z","sqmMagArcsec2":18.50,"source":"AAG CloudWatcher SOLO HTTP / lightmpsas","serial":"2382","firmware":"5.88","quality":"CURRENT"}',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:01:00Z","sqmMagArcsec2":18.60,"source":"AAG CloudWatcher SOLO HTTP / lightmpsas","serial":"2382","firmware":"5.88","quality":"CURRENT"}',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:01:30Z","sqmMagArcsec2":18.70,"source":"AAG CloudWatcher SOLO HTTP / lightmpsas","serial":"2382","firmware":"5.88","quality":"CURRENT"}',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:02:00Z","sqmMagArcsec2":18.80,"source":"AAG CloudWatcher SOLO HTTP / lightmpsas","serial":"2382","firmware":"5.88","quality":"CURRENT"}',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:01:00Z","sqmMagArcsec2":99.00,"source":"duplicate","serial":"x","firmware":"x","quality":"CURRENT"}',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:02:30Z","sqmMagArcsec2":18.90,"source":"AAG CloudWatcher SOLO HTTP / lightmpsas","serial":"2382","firmware":"5.88","quality":"STALE"}',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T22:03:00Z","sqmMagArcsec2":0,"source":"AAG CloudWatcher SOLO HTTP / lightmpsas","serial":"2382","firmware":"5.88","quality":"CURRENT"}',
        'not-json',
        '{"schemaVersion":1,"observedAtUtc":"2026-08-30T21:59:30Z","sqmMagArcsec2":17.00,"source":"outside","serial":"2382","firmware":"5.88","quality":"CURRENT"}'
    )
    [System.IO.File]::WriteAllLines($historyPath, $rows, [System.Text.UTF8Encoding]::new($false))

    & $scriptPath `
        -SessionStart ([datetime]'2026-08-30T22:00:00Z') `
        -SessionEnd ([datetime]'2026-08-30T22:02:00Z') `
        -OutputDirectory $outputDir `
        -HistoryPath $historyPath `
        -ExpectedCadenceSeconds 30

    $summaryPath = Join-Path $outputDir 'sqm-summary.json'
    $rawPath = Join-Path $outputDir 'sqm-history.ndjson'
    if (-not (Test-Path -LiteralPath $summaryPath)) { throw 'sqm-summary.json was not generated.' }
    if (-not (Test-Path -LiteralPath $rawPath)) { throw 'sqm-history.ndjson was not generated.' }

    $summary = Get-Content -LiteralPath $summaryPath -Raw | ConvertFrom-Json
    $raw = @(Get-Content -LiteralPath $rawPath | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })

    function Assert-Equal([object]$Actual, [object]$Expected, [string]$Name) {
        if ($Actual -ne $Expected) { throw "$Name expected '$Expected' but got '$Actual'." }
    }

    Assert-Equal $summary.valid_samples 5 'valid_samples'
    Assert-Equal ([double]$summary.min) 18.4 'min'
    Assert-Equal ([double]$summary.max) 18.8 'max'
    Assert-Equal ([double]$summary.mean) 18.6 'mean'
    Assert-Equal ([double]$summary.median) 18.6 'median'
    Assert-Equal ([double]$summary.temporal_coverage) 1.0 'temporal_coverage'
    Assert-Equal $summary.expected_cadence_seconds 30 'expected_cadence_seconds'
    Assert-Equal $summary.source 'AAG CloudWatcher SOLO HTTP / lightmpsas' 'source'
    Assert-Equal $summary.serial '2382' 'serial'
    Assert-Equal $summary.firmware '5.88' 'firmware'
    Assert-Equal $summary.quality 'AVAILABLE' 'quality'
    Assert-Equal $raw.Count 5 'raw sample count'

    $emptyDir = Join-Path $tempRoot 'empty-out'
    & $scriptPath `
        -SessionStart ([datetime]'2026-08-31T00:00:00Z') `
        -SessionEnd ([datetime]'2026-08-31T00:01:00Z') `
        -OutputDirectory $emptyDir `
        -HistoryPath $historyPath `
        -ExpectedCadenceSeconds 30

    $emptySummary = Get-Content -LiteralPath (Join-Path $emptyDir 'sqm-summary.json') -Raw | ConvertFrom-Json
    Assert-Equal $emptySummary.valid_samples 0 'empty.valid_samples'
    Assert-Equal ([double]$emptySummary.temporal_coverage) 0.0 'empty.temporal_coverage'
    Assert-Equal $emptySummary.quality 'UNKNOWN' 'empty.quality'
    if ($null -ne $emptySummary.min -or $null -ne $emptySummary.mean -or $null -ne $emptySummary.median) {
        throw 'Empty-window statistics must remain null.'
    }

    Write-Host 'SQM SESSION HISTORY REGRESSION RESULT: PASS'
} finally {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}
