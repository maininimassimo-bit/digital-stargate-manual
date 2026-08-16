[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$CloudWatcherCsv = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [ValidateRange(1, 3600)][int]$FreshnessSeconds = 30
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-SharedFileBytes {
    param([Parameter(Mandatory = $true)][string]$Path)

    $stream = $null
    try {
        $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
        $buffer = New-Object byte[] $stream.Length
        $read = 0
        while ($read -lt $buffer.Length) {
            $n = $stream.Read($buffer, $read, $buffer.Length - $read)
            if ($n -le 0) { break }
            $read += $n
        }
        if ($read -eq $buffer.Length) { return $buffer }
        $trimmed = New-Object byte[] $read
        [Array]::Copy($buffer, $trimmed, $read)
        return $trimmed
    }
    finally {
        if ($stream) { $stream.Dispose() }
    }
}

function Get-SharedFileHash {
    param([Parameter(Mandatory = $true)][string]$Path)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = Get-SharedFileBytes -Path $Path
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '')
    }
    finally {
        $sha.Dispose()
    }
}

function New-SharedSnapshot {
    param(
        [Parameter(Mandatory = $true)][string]$SourcePath,
        [Parameter(Mandatory = $true)][string]$DestinationPath
    )
    $bytes = Get-SharedFileBytes -Path $SourcePath
    [System.IO.File]::WriteAllBytes($DestinationPath, $bytes)
}

$adapter = Join-Path $RepositoryRoot 'scripts\telemetry\Export-CloudWatcherObservatoryStatus.ps1'
if (-not (Test-Path -LiteralPath $adapter -PathType Leaf)) { throw "Adapter non trovato: $adapter" }
if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) { throw "CloudWatcher CSV non trovato: $CloudWatcherCsv" }

$timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-pilot-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

$output = Join-Path $bundle 'observatory-status.json'
$transcript = Join-Path $bundle 'pilot-transcript.txt'
$manifestPath = Join-Path $bundle 'manifest.json'
$snapshot = Join-Path $bundle 'CloudWatcher.snapshot.csv'

Start-Transcript -LiteralPath $transcript -Force | Out-Null
try {
    Write-Output 'Digital StarGate CloudWatcher telemetry pilot - READ ONLY'
    Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
    Write-Output ('Repository: {0}' -f $RepositoryRoot)
    Write-Output ('CloudWatcher source: {0}' -f $CloudWatcherCsv)

    $sourceHashBefore = Get-SharedFileHash -Path $CloudWatcherCsv
    Write-Output ('Source SHA256 before: {0}' -f $sourceHashBefore)

    New-SharedSnapshot -SourcePath $CloudWatcherCsv -DestinationPath $snapshot
    Write-Output ('Shared snapshot: {0}' -f $snapshot)

    & $adapter -CloudWatcherCsv $snapshot -OutputPath $output -FreshnessSeconds $FreshnessSeconds -SourceInstance $env:COMPUTERNAME
    if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw "Adapter terminato con exit code $LASTEXITCODE" }

    $projection = Get-Content -LiteralPath $output -Raw | ConvertFrom-Json
    if ($projection.schema_version -ne '1.1') { throw 'Schema version inattesa.' }
    if ($projection.source_component -ne 'DSG.CloudWatcherCsvAdapter') { throw 'Source component inatteso.' }
    if ($projection.safety.observed_state -ne 'UNKNOWN') { throw 'Safety invariant violata: overall safety deve restare UNKNOWN.' }
    if ($projection.safety.authority -ne 'LOCAL_SAFETY_AUTHORITY') { throw 'Safety authority inattesa.' }
    if ($projection.systems.dome.state -ne 'UNKNOWN' -or $projection.systems.mount.state -ne 'UNKNOWN' -or $projection.systems.camera.state -ne 'UNKNOWN' -or $projection.systems.power.state -ne 'UNKNOWN' -or $projection.systems.network.state -ne 'UNKNOWN') {
        throw 'Isolation invariant violata: un producer non integrato non e UNKNOWN.'
    }

    $sourceHashAfter = Get-SharedFileHash -Path $CloudWatcherCsv
    Write-Output ('Source SHA256 after: {0}' -f $sourceHashAfter)

    $manifest = [ordered]@{
        schema_version = '1.0'
        pilot = 'DSG-OBS-RT-001'
        generated_at_local = (Get-Date).ToString('o')
        computer = $env:COMPUTERNAME
        repository_root = $RepositoryRoot
        repository_head = (& git -C $RepositoryRoot rev-parse HEAD 2>$null)
        cloudwatcher_source = $CloudWatcherCsv
        cloudwatcher_snapshot = $snapshot
        cloudwatcher_sha256_before = $sourceHashBefore
        cloudwatcher_sha256_after = $sourceHashAfter
        source_unchanged = ($sourceHashBefore -eq $sourceHashAfter)
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
            read_only_source_hash_unchanged = ($sourceHashBefore -eq $sourceHashAfter)
            overall_safety_unknown = $true
            non_integrated_systems_unknown = $true
        }
    }
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

    if ($sourceHashBefore -ne $sourceHashAfter) {
        Write-Warning 'CloudWatcher source changed while the pilot was reading it. This may be a normal append by CloudWatcher; source was never modified by the pilot.'
    }

    Write-Output ('Evidence bundle: {0}' -f $bundle)
    Write-Output 'PILOT RESULT: PASS'
}
finally {
    Stop-Transcript | Out-Null
}
