[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [string]$NinaProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\nina-observatory-status.json",

    [ValidateRange(1, 3600)]
    [int]$FreshnessSeconds = 60,

    [string]$SourceInstance = $env:COMPUTERNAME
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ServiceSignal {
    param(
        [Parameter(Mandatory = $true)][object]$Service,
        [Parameter(Mandatory = $true)][datetime]$ObservedAt,
        [Parameter(Mandatory = $true)][datetime]$FreshUntil,
        [Parameter(Mandatory = $true)][string]$Source
    )

    $quality = if ($FreshUntil -ge [datetime]::UtcNow) { 'CURRENT' } else { 'STALE' }
    $state = if ($quality -eq 'CURRENT') { ([string]$Service.state).Trim().ToUpperInvariant() } else { 'UNKNOWN' }

    return [ordered]@{
        state = if ([string]::IsNullOrWhiteSpace($state)) { 'UNKNOWN' } else { $state }
        observed_at_utc = $ObservedAt.ToString('o')
        fresh_until_utc = $FreshUntil.ToString('o')
        quality = $quality
        source = $Source
    }
}

function Get-UnverifiedServiceSignal {
    param([Parameter(Mandatory = $true)][string]$Source)
    return [ordered]@{
        state = 'UNKNOWN'
        observed_at_utc = $null
        fresh_until_utc = $null
        quality = 'UNKNOWN'
        source = $Source
    }
}

if (-not (Test-Path -LiteralPath $NinaProjection -PathType Leaf)) {
    throw "Projection NINA non trovata: $NinaProjection"
}

$projection = Get-Content -LiteralPath $NinaProjection -Raw -ErrorAction Stop | ConvertFrom-Json
if ($projection.schemaVersion -ne 2) { throw 'Schema NINA observatory telemetry inatteso.' }
if ([string]$projection.source -ne 'nina-observatory-telemetry-exporter') { throw 'Source NINA observatory telemetry inattesa.' }
if (-not $projection.services) { throw 'Servizi NINA observatory telemetry assenti.' }

$observedAt = [datetime]::Parse(
    [string]$projection.observedAtUtc,
    [System.Globalization.CultureInfo]::InvariantCulture,
    [System.Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
$freshUntil = $observedAt.AddSeconds($FreshnessSeconds)
$overallQuality = if ($freshUntil -ge [datetime]::UtcNow) { 'CURRENT' } else { 'STALE' }
$source = 'NINA Observatory Telemetry Exporter'
$networkSource = 'NINA Observatory Telemetry Exporter / Passive Network Adapter'

$dome = Get-ServiceSignal -Service $projection.services.dome -ObservedAt $observedAt -FreshUntil $freshUntil -Source $source
$mount = Get-ServiceSignal -Service $projection.services.mount -ObservedAt $observedAt -FreshUntil $freshUntil -Source $source
$camera = Get-ServiceSignal -Service $projection.services.camera -ObservedAt $observedAt -FreshUntil $freshUntil -Source $source
$power = Get-UnverifiedServiceSignal -Source $source
$network = Get-ServiceSignal -Service $projection.services.network -ObservedAt $observedAt -FreshUntil $freshUntil -Source $networkSource
$weatherSignal = Get-ServiceSignal -Service $projection.services.weather -ObservedAt $observedAt -FreshUntil $freshUntil -Source $source
$safetySignal = Get-ServiceSignal -Service $projection.services.safety -ObservedAt $observedAt -FreshUntil $freshUntil -Source $source

# Management-only semantics stay unresolved unless an approved direct source exists.
$network.active_link = $projection.services.network.details.activeLink
$network.vpn = $projection.services.network.details.vpn
$network.lte_failover = $projection.services.network.details.lteFailover

$weather = $weatherSignal
$weather.temperature_c = $projection.services.weather.details.temperatureC
$weather.humidity_pct = $projection.services.weather.details.humidityPct
$weather.dew_point_c = $projection.services.weather.details.dewPointC
$weather.wind_speed_m_s = $projection.services.weather.details.windSpeed
$weather.wind_gust_m_s = $projection.services.weather.details.windGust
$weather.wind_speed_kmh = if ($null -ne $projection.services.weather.details.windSpeed) { [math]::Round(([double]$projection.services.weather.details.windSpeed * 3.6), 3) } else { $null }
$weather.wind_gust_kmh = if ($null -ne $projection.services.weather.details.windGust) { [math]::Round(([double]$projection.services.weather.details.windGust * 3.6), 3) } else { $null }
$weather.rain_rate_mm_h = $projection.services.weather.details.rainRate
$weather.pressure_hpa = $projection.services.weather.details.pressure
$weather.cloud_cover_pct = $projection.services.weather.details.cloudCoverPct
$weather.sky_temperature_c = $projection.services.weather.details.skyTemperatureC
$weather.sqm_mag_arcsec2 = $null

$observedSafety = if ($overallQuality -eq 'CURRENT') { $safetySignal.state } else { 'UNKNOWN' }
$reason = if ($observedSafety -eq 'UNKNOWN') {
    'NINA SafetyMonitor state unavailable or stale; local physical interlocks remain authoritative'
} else {
    'Observed through NINA SafetyMonitor; local physical interlocks remain authoritative'
}

$payload = [ordered]@{
    schema_version = '1.1'
    observatory = [ordered]@{
        name = 'Digital StarGate'
        location = 'Manciano (GR)'
    }
    observed_at_utc = $observedAt.ToString('o')
    fresh_until_utc = $freshUntil.ToString('o')
    source_component = 'DSG.NinaObservatoryTelemetryAdapter'
    source_instance = $SourceInstance
    quality = $overallQuality
    correlation_id = [guid]::NewGuid().ToString('D')
    systems = [ordered]@{
        dome = $dome
        mount = $mount
        camera = $camera
        power = $power
        network = $network
        weather = $weather
    }
    safety = [ordered]@{
        observed_state = $observedSafety
        authority = 'NINA_SAFETY_MONITOR_OBSERVATION'
        reasons = @($reason)
    }
    diagnostics = [ordered]@{
        telemetry_author = $projection.author
        nina_projection = $NinaProjection
        dome_raw_shutter_status = $projection.services.dome.details.rawShutterStatus
        mount_at_park = $projection.services.mount.details.atPark
        mount_at_home = $projection.services.mount.details.atHome
        mount_tracking = $projection.services.mount.details.tracking
        mount_side_of_pier = $projection.services.mount.details.sideOfPier
        camera_temperature_c = $projection.services.camera.details.temperatureC
        camera_cooler_on = $projection.services.camera.details.coolerOn
        camera_cooler_power_pct = $projection.services.camera.details.coolerPowerPct
        camera_exposing = $projection.services.camera.details.exposing
        safety_monitor_is_safe = $projection.services.safety.details.isSafe
        network_interface = $projection.services.network.details.interface
        network_gateway = $projection.services.network.details.gateway
        network_gateway_reachable = $projection.services.network.details.gatewayReachable
        network_gateway_latency_ms = $projection.services.network.details.gatewayLatencyMs
        network_internet_target = $projection.services.network.details.internetTarget
        network_internet_reachable = $projection.services.network.details.internetReachable
        network_internet_latency_ms = $projection.services.network.details.internetLatencyMs
        network_dns_name = $projection.services.network.details.dnsName
        network_dns_resolved = $projection.services.network.details.dnsResolved
        network_dns_latency_ms = $projection.services.network.details.dnsLatencyMs
        network_dns_address_count = $projection.services.network.details.dnsAddressCount
    }
}

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$tempPath = "$OutputPath.tmp"
$payload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $tempPath -Encoding UTF8
Move-Item -LiteralPath $tempPath -Destination $OutputPath -Force

Write-Output ('NINA Observatory Status projection written: {0}' -f $OutputPath)
Write-Output ('Observed UTC: {0}' -f $payload.observed_at_utc)
Write-Output ('Dome: {0}/{1}; Mount: {2}/{3}; Camera: {4}/{5}' -f $dome.state,$dome.quality,$mount.state,$mount.quality,$camera.state,$camera.quality)
Write-Output ('Weather: {0}/{1}; Safety observed: {2}' -f $weather.state,$weather.quality,$payload.safety.observed_state)
Write-Output ('Power: {0}/{1}; Network: {2}/{3}' -f $power.state,$power.quality,$network.state,$network.quality)
