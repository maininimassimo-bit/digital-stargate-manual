[CmdletBinding()]
param(
    [string]$HistoryRoot = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\history\eagle-health'),
    [Parameter(Mandatory = $true)][string]$OutputPath,
    [ValidateRange(1,500)][int]$MaxRecords = 120
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$AllowedSignals = @('cpu','memory','storage','uptime','time_sync')

function Convert-ToPublicHistoryRecord([object]$Record) {
    if ([string]$Record.history_schema_version -ne '1.0') { throw 'Unsupported history_schema_version.' }
    if ([string]::IsNullOrWhiteSpace([string]$Record.record_id)) { throw 'History record_id missing.' }
    if ([string]::IsNullOrWhiteSpace([string]$Record.signal_id)) { throw 'History signal_id missing.' }
    if ([string]::IsNullOrWhiteSpace([string]$Record.observed_at_utc)) { throw 'History observed_at_utc missing.' }

    $signalId = [string]$Record.signal_id
    if ($AllowedSignals -notcontains $signalId) { return $null }

    $publicData = $null
    switch ($signalId) {
        'cpu' {
            $d = $Record.data
            $publicData = [ordered]@{ load_pct=$d.load_pct; window_avg_pct=$d.window_avg_pct; window_peak_pct=$d.window_peak_pct; temperature_c=$d.temperature_c }
        }
        'memory' {
            $d = $Record.data
            $publicData = [ordered]@{ available_physical_bytes=$d.available_physical_bytes; total_physical_bytes=$d.total_physical_bytes; available_ratio=$d.available_ratio; memory_pressure=$d.memory_pressure }
        }
        'storage' {
            $d = $Record.data
            $publicData = [ordered]@{
                logical_disks = @($d.logical_disks | ForEach-Object { [ordered]@{ device_id=$_.device_id; size_bytes=$_.size_bytes; free_bytes=$_.free_bytes; free_pct=$_.free_pct } })
                physical_disks = @($d.physical_disks | ForEach-Object { [ordered]@{ friendly_name=$_.friendly_name; health_status=$_.health_status; operational_status=@($_.operational_status) } })
            }
        }
        'uptime' {
            $d = $Record.data
            $publicData = [ordered]@{ uptime_seconds=$d.uptime_seconds; last_boot_at_utc=$d.last_boot_at_utc }
        }
        'time_sync' {
            $d = $Record.data
            $publicData = [ordered]@{ service_state=$d.service_state; time_source=$d.time_source; offset_ms=$d.offset_ms; last_successful_sync_utc=$d.last_successful_sync_utc }
        }
    }

    [ordered]@{
        history_schema_version = '1.0'
        record_id = [string]$Record.record_id
        host = [string]$Record.host
        signal_id = $signalId
        observed_at_utc = [string]$Record.observed_at_utc
        quality = [string]$Record.quality
        source = [string]$Record.source
        cadence_class = [string]$Record.cadence_class
        reason = $Record.reason
        data = $publicData
    }
}

$records = @()
if (Test-Path -LiteralPath $HistoryRoot -PathType Container) {
    $segments = @(Get-ChildItem -LiteralPath $HistoryRoot -Filter 'eagle-health-*.ndjson' -File -Recurse | Sort-Object FullName)
    foreach ($segment in $segments) {
        foreach ($line in [IO.File]::ReadAllLines($segment.FullName)) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            $item = $line | ConvertFrom-Json -ErrorAction Stop
            $public = Convert-ToPublicHistoryRecord $item
            if ($null -ne $public) { $records += [pscustomobject]$public }
        }
    }
}

$records = @($records | Sort-Object { [datetime]::Parse($_.observed_at_utc).ToUniversalTime() } -Descending | Select-Object -First $MaxRecords)
$records = @($records | Sort-Object { [datetime]::Parse($_.observed_at_utc).ToUniversalTime() })

$generated = [datetime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ')
$projection = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.EagleHealthPortalHistoryProjection'
    generated_at_utc = $generated
    max_records = $MaxRecords
    bounded = $true
    source_component = 'DSG.EagleHealthHistoryWriter'
    records_returned = $records.Count
    records = $records
    diagnostics = [ordered]@{
        projection_mode = 'READ_ONLY_PUBLIC_BOUNDED'
        safety_authority = 'OUTSIDE_SCOPE'
        automatic_remediation = $false
        retention_deletion_enabled = $false
        historical_records_deleted = 0
    }
}

$json = $projection | ConvertTo-Json -Depth 12
$parent = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$tmp = Join-Path $parent ('.' + [IO.Path]::GetFileName($OutputPath) + '.' + [guid]::NewGuid().ToString('N') + '.tmp')
$backup = Join-Path $parent ('.' + [IO.Path]::GetFileName($OutputPath) + '.' + [guid]::NewGuid().ToString('N') + '.bak')
try {
    [IO.File]::WriteAllText($tmp,$json,(New-Object Text.UTF8Encoding($false)))
    $check = Get-Content -LiteralPath $tmp -Raw | ConvertFrom-Json -ErrorAction Stop
    if ($check.component -ne 'DSG.EagleHealthPortalHistoryProjection' -or $check.bounded -ne $true) { throw 'Invalid bounded history projection.' }
    if ([int]$check.records_returned -gt $MaxRecords) { throw 'History projection exceeded MaxRecords.' }
    if (Test-Path -LiteralPath $OutputPath -PathType Leaf) { [IO.File]::Replace($tmp,$OutputPath,$backup,$true); if(Test-Path $backup){Remove-Item $backup -Force -ErrorAction SilentlyContinue} }
    else { Move-Item -LiteralPath $tmp -Destination $OutputPath }
}
finally {
    if(Test-Path $tmp){Remove-Item $tmp -Force -ErrorAction SilentlyContinue}
    if(Test-Path $backup){Remove-Item $backup -Force -ErrorAction SilentlyContinue}
}

Write-Output $OutputPath
