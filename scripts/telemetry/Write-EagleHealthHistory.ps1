[CmdletBinding()]
param(
    [string]$InputPath = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\eagle-health.json'),
    [string]$HistoryRoot = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\history\eagle-health'),
    [string]$EvidenceRoot = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\history\eagle-health\evidence'),
    [string]$LockName = 'DigitalStarGate.EagleHealthHistoryWriter'
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function New-Utf8NoBom { New-Object Text.UTF8Encoding($false) }
function Convert-ToUtcIso([datetime]$Value) { $Value.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ') }
function Write-AtomicText([string]$Path,[string[]]$Lines) {
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $name = [IO.Path]::GetFileName($Path)
    $tmp = Join-Path $dir ('.' + $name + '.' + [guid]::NewGuid().ToString('N') + '.tmp')
    $bak = Join-Path $dir ('.' + $name + '.' + [guid]::NewGuid().ToString('N') + '.bak')
    try {
        [IO.File]::WriteAllLines($tmp, $Lines, (New-Utf8NoBom))
        foreach ($line in [IO.File]::ReadAllLines($tmp)) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            $null = $line | ConvertFrom-Json -ErrorAction Stop
        }
        if (Test-Path -LiteralPath $Path -PathType Leaf) {
            [IO.File]::Replace($tmp, $Path, $bak, $true)
            if (Test-Path -LiteralPath $bak) { Remove-Item -LiteralPath $bak -Force -ErrorAction SilentlyContinue }
        }
        else { Move-Item -LiteralPath $tmp -Destination $Path }
    }
    finally {
        if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
        if (Test-Path -LiteralPath $bak) { Remove-Item -LiteralPath $bak -Force -ErrorAction SilentlyContinue }
    }
}

$mutex = New-Object System.Threading.Mutex($false, $LockName)
$lockAcquired = $false
$started = [datetime]::UtcNow
$runId = 'DSG-EAGLE-HISTORY-' + [guid]::NewGuid().ToString()
$result = 'FAILED'
$lastError = $null
$recordsSeen = 0
$recordsAppended = 0
$recordsDuplicateSkipped = 0
$recordsRejected = 0
$writeFailures = 0
$inputObserved = $null
$segmentPath = $null

try {
    try { $lockAcquired = $mutex.WaitOne(0, $false) }
    catch [System.Threading.AbandonedMutexException] { $lockAcquired = $true }
    if (-not $lockAcquired) {
        Write-Output 'SKIPPED_NON_OVERLAP'
        return
    }

    if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) { throw "Input projection not found: $InputPath" }
    $projection = Get-Content -LiteralPath $InputPath -Raw | ConvertFrom-Json -ErrorAction Stop
    $inputObserved = [string]$projection.observed_at_utc
    if ([string]::IsNullOrWhiteSpace($inputObserved)) { throw 'Projection observed_at_utc missing.' }

    $serializer = Join-Path $PSScriptRoot 'Convert-EagleHostHealthToHistoryRecords.ps1'
    if (-not (Test-Path -LiteralPath $serializer -PathType Leaf)) { throw 'History serializer missing.' }
    $records = @(& $serializer -InputPath $InputPath)
    $recordsSeen = $records.Count

    $observedUtc = [datetime]::Parse($inputObserved).ToUniversalTime()
    $segmentDir = Join-Path (Join-Path $HistoryRoot $observedUtc.ToString('yyyy')) $observedUtc.ToString('MM')
    $segmentPath = Join-Path $segmentDir ('eagle-health-' + $observedUtc.ToString('yyyy-MM') + '.ndjson')

    $existingLines = @()
    $existingIds = @{}
    if (Test-Path -LiteralPath $segmentPath -PathType Leaf) {
        $existingLines = @([IO.File]::ReadAllLines($segmentPath))
        foreach ($line in $existingLines) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            $item = $line | ConvertFrom-Json -ErrorAction Stop
            if ([string]::IsNullOrWhiteSpace([string]$item.record_id)) { throw 'Existing history record_id missing.' }
            $existingIds[[string]$item.record_id] = $true
        }
    }

    $newLines = @()
    foreach ($record in $records) {
        if ([string]::IsNullOrWhiteSpace([string]$record.record_id)) {
            $recordsRejected++
            continue
        }
        if ($existingIds.ContainsKey([string]$record.record_id)) {
            $recordsDuplicateSkipped++
            continue
        }
        $newLines += ($record | ConvertTo-Json -Depth 12 -Compress)
        $existingIds[[string]$record.record_id] = $true
        $recordsAppended++
    }

    if ($newLines.Count -gt 0) {
        try { Write-AtomicText -Path $segmentPath -Lines @($existingLines + $newLines) }
        catch { $writeFailures++; throw }
    }

    $checkpointDir = Join-Path $HistoryRoot 'checkpoints'
    $checkpointPath = Join-Path $checkpointDir 'latest.json'
    $checkpoint = [ordered]@{
        schema_version = '1.0'
        component = 'DSG.EagleHealthHistoryWriter'
        host = [string]$projection.computer
        input_projection_observed_at_utc = $inputObserved
        segment_path = $segmentPath
        records_seen = $recordsSeen
        records_appended = $recordsAppended
        records_duplicate_skipped = $recordsDuplicateSkipped
        historical_records_deleted = 0
        retention_deletion_enabled = $false
        updated_at_utc = Convert-ToUtcIso ([datetime]::UtcNow)
    }
    Write-AtomicText -Path $checkpointPath -Lines @(($checkpoint | ConvertTo-Json -Depth 8 -Compress))
    $result = 'PASS'
}
catch {
    $lastError = ($_.Exception.Message -replace '[\r\n]+',' ').Trim()
    throw
}
finally {
    $completed = [datetime]::UtcNow
    try {
        if (-not (Test-Path -LiteralPath $EvidenceRoot)) { New-Item -ItemType Directory -Path $EvidenceRoot -Force | Out-Null }
        $evidencePath = Join-Path $EvidenceRoot ($started.ToString('yyyyMMddTHHmmssZ') + '-' + $runId + '.json')
        $evidence = [ordered]@{
            schema_version = '1.0'
            component = 'DSG.EagleHealthHistoryWriter'
            run_id = $runId
            started_at_utc = Convert-ToUtcIso $started
            completed_at_utc = Convert-ToUtcIso $completed
            host = $env:COMPUTERNAME
            input_projection_observed_at_utc = $inputObserved
            segment_path = $segmentPath
            records_seen = $recordsSeen
            records_appended = $recordsAppended
            records_duplicate_skipped = $recordsDuplicateSkipped
            records_rejected = $recordsRejected
            write_failures = $writeFailures
            historical_records_deleted = 0
            retention_deletion_enabled = $false
            result = $result
            last_error = $lastError
        }
        Write-AtomicText -Path $evidencePath -Lines @(($evidence | ConvertTo-Json -Depth 8 -Compress))
    }
    catch { }
    if ($lockAcquired) { try { $mutex.ReleaseMutex() } catch { } }
    $mutex.Dispose()
}

Write-Output $segmentPath
