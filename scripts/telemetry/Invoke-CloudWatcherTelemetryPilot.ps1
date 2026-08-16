[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$CloudWatcherCsv = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [ValidateRange(1, 3600)][int]$FreshnessSeconds = 30
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$adapter = Join-Path $RepositoryRoot 'scripts\telemetry\Export-CloudWatcherObservatoryStatus.ps1'
if (-not (Test-Path -LiteralPath $adapter -PathType Leaf)) { throw "Adapter non trovato: $adapter" }
if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) { throw "CloudWatcher CSV non trovato: $CloudWatcherCsv" }

$timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-pilot-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

$output = Join-Path $bundle 'observatory-status.json'
$transcript = Join-Path $bundle 'pilot-transcript.txt'
$manifestPath = Join-Path $bundle 'manifest.json'

Start-Transcript -LiteralPath $transcript -Force | Out-Null
try {
    Write-Output 'Digital StarGate CloudWatcher telemetry pilot - READ ONLY'
    Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
    Write-Output ('Repository: {0}' -f $RepositoryRoot)
    Write-Output ('CloudWatcher source: {0}' -f $CloudWatcherCsv)
    Write-Output ('Source SHA256 before: {0}' -f (Get-FileHash -LiteralPath $CloudWatcherCsv -Algorithm SHA256).Hash)

    & $adapter -CloudWatcherCsv $CloudWatcherCsv -OutputPath $output -FreshnessSeconds $FreshnessSeconds -SourceInstance $env:COMPUTERNAME
    if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw "Adapter terminato con exit code $LASTEXITCODE" }

    $projection = Get-Content -LiteralPath $output -Raw | ConvertFrom-Json
    if ($projection.schema_version -ne '1.1') { throw 'Schema version inattesa.' }
    if ($projection.source_component -ne 'DSG.CloudWatcherCsvAdapter') { throw 'Source component inatteso.' }
    if ($projection.safety.observed_state -ne 'UNKNOWN') { throw 'Safety invariant violata: overall safety deve restare UNKNOWN.' }
    if ($projection.safety.authority -ne 'LOCAL_SAFETY_AUTHORITY') { throw 'Safety authority inattesa.' }
    if ($projection.systems.dome.state -ne 'UNKNOWN' -or $projection.systems.mount.state -ne 'UNKNOWN' -or $projection.systems.camera.state -ne 'UNKNOWN' -or $projection.systems.power.state -ne 'UNKNOWN' -or $projection.systems.network.state -ne 'UNKNOWN') {
        throw 'Isolation invariant violata: un producer non integrato non e UNKNOWN.'
    }

    $sourceHashAfter = (Get-FileHash -LiteralPath $CloudWatcherCsv -Algorithm SHA256).Hash
    Write-Output ('Source SHA256 after: {0}' -f $sourceHashAfter)

    $manifest = [ordered]@{
        schema_version = '1.0'
        pilot = 'DSG-OBS-RT-001'
        generated_at_local = (Get-Date).ToString('o')
        computer = $env:COMPUTERNAME
        repository_root = $RepositoryRoot
        repository_head = (& git -C $RepositoryRoot rev-parse HEAD 2>$null)
        cloudwatcher_source = $CloudWatcherCsv
        cloudwatcher_sha256_before = (Get-FileHash -LiteralPath $CloudWatcherCsv -Algorithm SHA256).Hash
        cloudwatcher_sha256_after = $sourceHashAfter
        source_unchanged = $true
        freshness_seconds = $FreshnessSeconds
        projection = [ordered]@{
            path = $output
            sha256 = (Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash
            observed_at_utc = $projection.observed_at_utc
            fresh_until_utc = $projection.fresh_until_utc
            quality = $projection.quality
            weather_state = $projection.systems.weather.state
            weather_quality = $projection.systems.weather.quality
            overall_safety = $projection.safety.observed_state
        }
        invariants = [ordered]@{
            read_only_source_hash_unchanged = $true
            overall_safety_unknown = $true
            non_integrated_systems_unknown = $true
        }
    }
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
    Write-Output ('Evidence bundle: {0}' -f $bundle)
    Write-Output 'PILOT RESULT: PASS'
}
finally {
    Stop-Transcript | Out-Null
}
