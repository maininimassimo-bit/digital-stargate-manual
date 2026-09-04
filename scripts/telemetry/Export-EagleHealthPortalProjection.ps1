[CmdletBinding()]
param(
    [string]$InputPath = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\eagle-health.json'),
    [Parameter(Mandatory = $true)][string]$OutputPath
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Convert-ToPublicSignal([string]$SignalId,[object]$Signal) {
    if ($null -eq $Signal) { return $null }

    $data = $null
    switch ($SignalId) {
        'cpu' {
            $d = $Signal.data
            $data = [ordered]@{
                model = $d.model
                physical_cores = $d.physical_cores
                logical_processors = $d.logical_processors
                load_pct = $d.load_pct
                window_avg_pct = $d.window_avg_pct
                window_peak_pct = $d.window_peak_pct
                temperature_c = $d.temperature_c
            }
        }
        'memory' {
            $d = $Signal.data
            $data = [ordered]@{
                total_physical_bytes = $d.total_physical_bytes
                available_physical_bytes = $d.available_physical_bytes
                available_ratio = $d.available_ratio
                memory_pressure = $d.memory_pressure
            }
        }
        'storage' {
            $d = $Signal.data
            $logical = @()
            foreach ($item in @($d.logical_disks)) {
                $logical += [ordered]@{
                    device_id = $item.device_id
                    volume_name = $item.volume_name
                    filesystem = $item.filesystem
                    size_bytes = $item.size_bytes
                    free_bytes = $item.free_bytes
                    free_ratio = $item.free_ratio
                    free_pct = $item.free_pct
                }
            }
            $physical = @()
            foreach ($item in @($d.physical_disks)) {
                $physical += [ordered]@{
                    friendly_name = $item.friendly_name
                    media_type = $item.media_type
                    bus_type = $item.bus_type
                    health_status = $item.health_status
                    operational_status = @($item.operational_status)
                    size_bytes = $item.size_bytes
                }
            }
            $data = [ordered]@{
                logical_disks = $logical
                physical_disks = $physical
                reliability = [ordered]@{
                    available = $d.reliability.available
                    temperature_c = $d.reliability.temperature_c
                    temperature_max_c = $d.reliability.temperature_max_c
                    wear_pct = $d.reliability.wear_pct
                    reason = $d.reliability.reason
                }
            }
        }
        'uptime' {
            $d = $Signal.data
            $data = [ordered]@{
                last_boot_at_utc = $d.last_boot_at_utc
                uptime_seconds = $d.uptime_seconds
                unexpected_reboot_observed = $d.unexpected_reboot_observed
            }
        }
        'time_sync' {
            $d = $Signal.data
            $data = [ordered]@{
                service_state = $d.service_state
                time_source = $d.time_source
                stratum = $d.stratum
                last_successful_sync_utc = $d.last_successful_sync_utc
                offset_ms = $d.offset_ms
            }
        }
        default { return $null }
    }

    return [ordered]@{
        state = [string]$Signal.state
        quality = [string]$Signal.quality
        observed_at_utc = [string]$Signal.observed_at_utc
        fresh_until_utc = [string]$Signal.fresh_until_utc
        source = [string]$Signal.source
        cadence_class = [string]$Signal.cadence_class
        reason = $Signal.reason
        data = $data
    }
}

function Assert-Input([object]$Projection) {
    if ($null -eq $Projection) { throw 'Projection is null.' }
    if ([string]$Projection.schema_version -ne '1.0') { throw 'Unsupported source schema_version.' }
    if ([string]$Projection.component -ne 'DSG.EagleHostHealthCollector') { throw 'Invalid source component.' }
    if ([string]$Projection.diagnostics.collector_mode -ne 'READ_ONLY') { throw 'Source collector_mode must be READ_ONLY.' }
    if ($null -eq $Projection.signals) { throw 'Source signals missing.' }
}

function Assert-Output([object]$Projection) {
    if ([string]$Projection.schema_version -ne '1.0') { throw 'Invalid portal schema_version.' }
    if ([string]$Projection.component -ne 'DSG.EagleHealthPortalProjection') { throw 'Invalid portal component.' }
    if ([string]$Projection.summary.state -ne 'UNKNOWN') { throw 'Portal summary state must remain UNKNOWN.' }
    if ([string]$Projection.summary.reason -ne 'POLICY_NOT_ACTIVATED') { throw 'Portal summary policy reason missing.' }
}

if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) { throw "Source projection not found: $InputPath" }
$source = Get-Content -LiteralPath $InputPath -Raw | ConvertFrom-Json -ErrorAction Stop
Assert-Input $source

$allowed = @('cpu','memory','storage','uptime','time_sync')
$signals = [ordered]@{}
$rejected = 0
foreach ($signalId in $allowed) {
    $property = $source.signals.PSObject.Properties[$signalId]
    if ($null -eq $property) { continue }
    $publicSignal = Convert-ToPublicSignal $signalId $property.Value
    if ($null -eq $publicSignal) { $rejected++; continue }
    $signals[$signalId] = $publicSignal
}

$reason = 'POLICY_NOT_ACTIVATED'
$projection = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.EagleHealthPortalProjection'
    host = [string]$source.computer
    observed_at_utc = [string]$source.observed_at_utc
    fresh_until_utc = [string]$source.fresh_until_utc
    quality = [string]$source.quality
    source_component = [string]$source.component
    source_schema_version = [string]$source.schema_version
    source_correlation_id = [string]$source.correlation_id
    summary = [ordered]@{
        state = 'UNKNOWN'
        reason = $reason
    }
    signals = $signals
    diagnostics = [ordered]@{
        projection_mode = 'READ_ONLY_PUBLIC'
        safety_authority = 'OUTSIDE_SCOPE'
        automatic_remediation = $false
        signals_seen = @($source.signals.PSObject.Properties).Count
        signals_published = $signals.Count
        signals_rejected = $rejected
    }
}

Assert-Output ([pscustomobject]$projection)
$json = $projection | ConvertTo-Json -Depth 12

$parent = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$tmp = Join-Path $parent ('.' + [IO.Path]::GetFileName($OutputPath) + '.' + [guid]::NewGuid().ToString('N') + '.tmp')
$backup = Join-Path $parent ('.' + [IO.Path]::GetFileName($OutputPath) + '.' + [guid]::NewGuid().ToString('N') + '.bak')
try {
    [IO.File]::WriteAllText($tmp, $json, (New-Object Text.UTF8Encoding($false)))
    $validated = Get-Content -LiteralPath $tmp -Raw | ConvertFrom-Json -ErrorAction Stop
    Assert-Output $validated
    if (Test-Path -LiteralPath $OutputPath -PathType Leaf) {
        [IO.File]::Replace($tmp, $OutputPath, $backup, $true)
        if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Force -ErrorAction SilentlyContinue }
    }
    else { Move-Item -LiteralPath $tmp -Destination $OutputPath }
}
finally {
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
    if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Force -ErrorAction SilentlyContinue }
}

Write-Output $OutputPath
