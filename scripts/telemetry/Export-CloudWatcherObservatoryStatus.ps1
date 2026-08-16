[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CloudWatcherCsv,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [ValidateRange(1, 3600)]
    [int]$FreshnessSeconds = 30,

    [string]$SourceInstance = $env:COMPUTERNAME
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function New-UnknownSignal {
    param([Parameter(Mandatory = $true)][string]$Source)
    return [ordered]@{
        state = 'UNKNOWN'
        observed_at_utc = $null
        fresh_until_utc = $null
        quality = 'UNKNOWN'
        source = $Source
    }
}

function Convert-CloudWatcherSafeStatus {
    param([AllowNull()][string]$Value)
    switch (($Value | ForEach-Object { $_.Trim().ToUpperInvariant() })) {
        'SAFE' { return 'SAFE' }
        'UNSAFE' { return 'UNSAFE' }
        default { return 'UNKNOWN' }
    }
}

function Get-CloudWatcherTimestampUtc {
    param(
        [Parameter(Mandatory = $true)][string]$Date,
        [Parameter(Mandatory = $true)][string]$Time
    )

    $local = [datetime]::ParseExact(
        ('{0} {1}' -f $Date.Trim(), $Time.Trim()),
        'yyyy-MM-dd HH:mm:ss',
        [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::Unspecified)

    $zone = [TimeZoneInfo]::FindSystemTimeZoneById('W. Europe Standard Time')
    return [TimeZoneInfo]::ConvertTimeToUtc($local, $zone)
}

if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) {
    throw "CloudWatcher CSV non trovato: $CloudWatcherCsv"
}

$rows = @(Import-Csv -LiteralPath $CloudWatcherCsv)
if ($rows.Count -eq 0) {
    throw "CloudWatcher CSV privo di righe dati: $CloudWatcherCsv"
}

$requiredHeaders = @('Date', 'Time', 'Safe Status')
$headers = @($rows[0].PSObject.Properties.Name)
foreach ($header in $requiredHeaders) {
    if ($headers -notcontains $header) {
        throw "Header CloudWatcher richiesto non trovato: $header"
    }
}

$row = $rows[$rows.Count - 1]
$observedAt = Get-CloudWatcherTimestampUtc -Date $row.Date -Time $row.Time
$freshUntil = $observedAt.AddSeconds($FreshnessSeconds)
$weatherState = Convert-CloudWatcherSafeStatus -Value $row.'Safe Status'
$now = [datetime]::UtcNow
$weatherQuality = if ($freshUntil -ge $now) { 'CURRENT' } else { 'STALE' }

$weather = New-UnknownSignal -Source 'CloudWatcher CSV'
$weather.state = if ($weatherQuality -eq 'CURRENT') { $weatherState } else { 'UNKNOWN' }
$weather.observed_at_utc = $observedAt.ToString('o')
$weather.fresh_until_utc = $freshUntil.ToString('o')
$weather.quality = $weatherQuality
$weather.temperature_c = $null
$weather.humidity_pct = $null
$weather.dew_point_c = $null
$weather.wind_speed_kmh = $null
$weather.wind_gust_kmh = $null
$weather.rain_rate_mm_h = $null
$weather.pressure_hpa = $null
$weather.sqm_mag_arcsec2 = $null
$weather.sky_temperature_c = $null

$payload = [ordered]@{
    schema_version = '1.1'
    observatory = [ordered]@{
        name = 'Digital StarGate'
        location = 'Manciano (GR)'
    }
    observed_at_utc = $observedAt.ToString('o')
    fresh_until_utc = $freshUntil.ToString('o')
    source_component = 'DSG.CloudWatcherCsvAdapter'
    source_instance = $SourceInstance
    quality = if ($weatherQuality -eq 'CURRENT') { 'DEGRADED' } else { 'STALE' }
    correlation_id = [guid]::NewGuid().ToString('D')
    systems = [ordered]@{
        dome = New-UnknownSignal -Source 'not-integrated'
        mount = New-UnknownSignal -Source 'not-integrated'
        camera = New-UnknownSignal -Source 'not-integrated'
        power = New-UnknownSignal -Source 'not-integrated'
        network = New-UnknownSignal -Source 'not-integrated'
        weather = $weather
    }
    safety = [ordered]@{
        observed_state = 'UNKNOWN'
        authority = 'LOCAL_SAFETY_AUTHORITY'
        reasons = @('Overall safety authority not integrated; CloudWatcher Safe Status is weather evidence only')
    }
    diagnostics = [ordered]@{
        cloud_condition = $row.'Cloud Condition'
        rain_condition = $row.'Rain Condition'
        brightness_condition = $row.'Brightness Condition'
        wind_condition = $row.'Wind Condition'
        switch_status = $row.'Switch Status'
        cloudwatcher_safe_status = $row.'Safe Status'
    }
}

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding UTF8

Write-Output ('CloudWatcher projection written: {0}' -f $OutputPath)
Write-Output ('Observed UTC: {0}' -f $payload.observed_at_utc)
Write-Output ('Weather: {0} / {1}' -f $weather.state, $weather.quality)
Write-Output ('Overall quality: {0}; overall safety: UNKNOWN' -f $payload.quality)
