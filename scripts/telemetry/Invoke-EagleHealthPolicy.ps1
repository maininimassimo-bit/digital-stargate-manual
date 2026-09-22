Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-EagleHealthPolicy {
param(
    [Parameter(Mandatory = $true)][object]$Projection,
    [string]$PolicyPath = (Join-Path $PSScriptRoot '..\..\docs\data\bkl-036-f5-eagle-health-policy-v1.json')
)

function Test-Fresh([object]$Signal, [datetime]$Now) {
    if ($null -eq $Signal) { return $false }
    try {
        $until = [datetime]::Parse([string]$Signal.fresh_until_utc, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
        return $until -ge $Now
    } catch { return $false }
}

function Test-Number([object]$Value) {
    if ($null -eq $Value) { return $false }
    $parsed = 0.0
    return [double]::TryParse([string]$Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$parsed) -and -not [double]::IsNaN($parsed) -and -not [double]::IsInfinity($parsed)
}

$policy = Get-Content -LiteralPath $PolicyPath -Raw | ConvertFrom-Json
$now = [datetime]::UtcNow
$signals = $Projection.signals
$required = @('cpu','memory','storage','uptime','time_sync')

foreach ($name in $required) {
    $property = $signals.PSObject.Properties[$name]
    if ($null -eq $property -or -not (Test-Fresh $property.Value $now)) {
        return [pscustomobject]@{ state = 'UNAVAILABLE'; score = $null; reason = 'REQUIRED_SIGNAL_NOT_CURRENT'; reasons = @('REQUIRED_SIGNAL_NOT_CURRENT') }
    }
}

$cpu = $signals.cpu.data
$memory = $signals.memory.data
$cpuSamplesProperty = $cpu.PSObject.Properties['samples']
$memorySamplesProperty = $memory.PSObject.Properties['available_pct_samples']
$cpuSamples = @()
$memorySamples = @()
if ($null -ne $cpuSamplesProperty) { $cpuSamples = @($cpuSamplesProperty.Value) }
if ($null -ne $memorySamplesProperty) { $memorySamples = @($memorySamplesProperty.Value) }
$minimumSamples = [int]$policy.thresholds.evaluation_window.minimum_samples
if ($cpuSamples.Count -lt $minimumSamples -or $memorySamples.Count -lt $minimumSamples) {
    return [pscustomobject]@{ state = 'UNAVAILABLE'; score = $null; reason = 'WINDOW_NOT_COMPUTABLE'; reasons = @('WINDOW_NOT_COMPUTABLE') }
}
if (@($cpuSamples | Where-Object { -not (Test-Number $_) }).Count -gt 0 -or @($memorySamples | Where-Object { -not (Test-Number $_) }).Count -gt 0) {
    return [pscustomobject]@{ state = 'UNAVAILABLE'; score = $null; reason = 'WINDOW_NOT_COMPUTABLE'; reasons = @('WINDOW_NOT_COMPUTABLE') }
}

$volumes = @{}
foreach ($disk in @($signals.storage.data.logical_disks)) {
    $id = [string]$disk.device_id
    if ($id -in @('C:','D:')) { $volumes[$id] = $disk }
}
foreach ($id in @('C:','D:')) {
    if (-not $volumes.ContainsKey($id) -or -not (Test-Number $volumes[$id].free_pct)) {
        return [pscustomobject]@{ state = 'UNAVAILABLE'; score = $null; reason = 'STORAGE_C_OR_D_NOT_COMPUTABLE'; reasons = @('STORAGE_C_OR_D_NOT_COMPUTABLE') }
    }
}

try { $sync = [datetime]::Parse([string]$signals.time_sync.data.last_successful_sync_utc, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime() } catch { $sync = $null }
if ($null -eq $sync -or $sync -gt $now) {
    return [pscustomobject]@{ state = 'UNAVAILABLE'; score = $null; reason = 'TIME_SYNC_NOT_CURRENT'; reasons = @('TIME_SYNC_NOT_CURRENT') }
}

$cpuDegraded = @($cpuSamples | Where-Object { [double]$_ -le [double]$policy.thresholds.cpu.percent }).Count -eq 0
$memoryDegraded = @($memorySamples | Where-Object { [double]$_ -ge [double]$policy.thresholds.memory_available.percent }).Count -eq 0
$storageDegraded = ([double]$volumes['C:'].free_pct -lt [double]$policy.thresholds.storage_free.percent) -or ([double]$volumes['D:'].free_pct -lt [double]$policy.thresholds.storage_free.percent)
if ($cpuDegraded -or $memoryDegraded -or $storageDegraded) {
    return [pscustomobject]@{ state = 'DEGRADED'; score = 50; reason = 'THRESHOLD_EXCEEDED'; reasons = @('THRESHOLD_EXCEEDED') }
}
return [pscustomobject]@{ state = 'HEALTHY'; score = 100; reason = 'ALL_REQUIRED_SIGNALS_HEALTHY'; reasons = @('ALL_REQUIRED_SIGNALS_HEALTHY') }
}
