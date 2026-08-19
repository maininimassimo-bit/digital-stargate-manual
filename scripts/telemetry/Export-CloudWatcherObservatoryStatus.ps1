[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CloudWatcherCsv,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [ValidateRange(1, 3600)]
    [int]$FreshnessSeconds = 60,

    [ValidateRange(4096, 1048576)]
    [int]$TailBytes = 262144,

    [string]$SourceInstance = $env:COMPUTERNAME,

    [string]$NinaDomeProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\nina-dome.json"
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
    if ([string]::IsNullOrWhiteSpace($Value)) { return 'UNKNOWN' }
    switch ($Value.Trim().ToUpperInvariant()) {
        'SAFE' { return 'SAFE' }
        'UNSAFE' { return 'UNSAFE' }
        default { return 'UNKNOWN' }
    }
}

function Convert-ToNullableDouble {
    param([AllowNull()][object]$Value)
    if ($null -eq $Value) { return $null }
    $text = [string]$Value
    if ([string]::IsNullOrWhiteSpace($text)) { return $null }
    $number = 0.0
    if ([double]::TryParse($text.Trim(), [System.Globalization.NumberStyles]::Float, [System.Globalization.CultureInfo]::InvariantCulture, [ref]$number)) {
        return $number
    }
    return $null
}

function Get-RomeTimeZone {
    foreach ($id in @('W. Europe Standard Time', 'Europe/Rome')) {
        try { return [TimeZoneInfo]::FindSystemTimeZoneById($id) } catch { }
    }
    throw 'Timezone Europe/Rome non disponibile sul runtime corrente.'
}

function Get-CloudWatcherTimestampUtc {
    param(
        [Parameter(Mandatory = $true)][string]$Date,
        [Parameter(Mandatory = $true)][string]$Time
    )

    $local = [datetime]::ParseExact(
        ('{0} {1}' -f $Date.Trim(), $Time.Trim()),
        'yyyy-MM-dd HH:mm:ss',
        [System.Globalization.CultureInfo]::InvariantCulture)
    return [TimeZoneInfo]::ConvertTimeToUtc($local, (Get-RomeTimeZone))
}

function Get-CloudWatcherHeaderAndTailLines {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][int]$Bytes
    )

    $stream = $null
    $reader = $null
    try {
        $stream = [System.IO.File]::Open($Path,[System.IO.FileMode]::Open,[System.IO.FileAccess]::Read,[System.IO.FileShare]::ReadWrite)
        $reader = New-Object System.IO.StreamReader($stream)
        $header = $reader.ReadLine()
        $length = $stream.Length
        $start = [math]::Max(0, $length - $Bytes)
        $stream.Seek($start, [System.IO.SeekOrigin]::Begin) | Out-Null
        if ($start -gt 0) { [void]$reader.ReadLine() }
        $lines = New-Object System.Collections.Generic.List[string]
        while (-not $reader.EndOfStream) {
            $line = $reader.ReadLine()
            if (-not [string]::IsNullOrWhiteSpace($line)) { $lines.Add($line) }
        }
        return [pscustomobject]@{ Header = $header; Lines = @($lines) }
    }
    finally {
        if ($reader) { $reader.Dispose() }
        elseif ($stream) { $stream.Dispose() }
    }
}

function Get-CsvFieldCount {
    param([Parameter(Mandatory = $true)][string]$Line)
    return ([regex]::Matches($Line, ',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)').Count + 1)
}

function Get-LatestCompleteCloudWatcherRow {
    param(
        [Parameter(Mandatory = $true)][string]$Header,
        [Parameter(Mandatory = $true)][string[]]$Lines
    )

    $headerFieldCount = Get-CsvFieldCount -Line $Header
    for ($i = $Lines.Count - 1; $i -ge 0; $i--) {
        try {
            if ((Get-CsvFieldCount -Line $Lines[$i]) -ne $headerFieldCount) { continue }
            $row = @($Header, $Lines[$i]) | ConvertFrom-Csv | Select-Object -First 1
            if (-not $row) { continue }
            if ([string]::IsNullOrWhiteSpace([string]$row.Date) -or [string]::IsNullOrWhiteSpace([string]$row.Time)) { continue }
            [void](Get-CloudWatcherTimestampUtc -Date $row.Date -Time $row.Time)
            return $row
        }
        catch { continue }
    }
    throw 'Nessuna riga CloudWatcher strutturalmente completa e parseabile trovata nella coda del file.'
}

function Get-NinaDomeSignal {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][int]$Freshness
    )

    $unknown = New-UnknownSignal -Source 'NINA dome exporter'
    if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $unknown
    }

    try {
        $projection = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop | ConvertFrom-Json
        if ($projection.schemaVersion -ne 1) { return $unknown }
        if ([string]$projection.source -ne 'nina-dome-exporter') { return $unknown }

        $observedAt = [datetime]::Parse(
            [string]$projection.observedAtUtc,
            [System.Globalization.CultureInfo]::InvariantCulture,
            [System.Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
        $freshUntil = $observedAt.AddSeconds($Freshness)
        $now = [datetime]::UtcNow

        $state = ([string]$projection.state).Trim().ToUpperInvariant()
        if ($state -notin @('OPEN','CLOSED','MOVING','FAULT','UNKNOWN')) { return $unknown }

        $isConnected = [bool]$projection.connected
        $quality = if ($isConnected -and $freshUntil -ge $now) { 'CURRENT' } else { if ($observedAt -le $now) { 'STALE' } else { 'UNKNOWN' } }

        return [ordered]@{
            state = if ($quality -eq 'CURRENT') { $state } else { 'UNKNOWN' }
            observed_at_utc = $observedAt.ToString('o')
            fresh_until_utc = $freshUntil.ToString('o')
            quality = $quality
            source = 'NINA dome exporter'
        }
    }
    catch {
        return $unknown
    }
}

if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) {
    throw "CloudWatcher CSV non trovato: $CloudWatcherCsv"
}

$tail = Get-CloudWatcherHeaderAndTailLines -Path $CloudWatcherCsv -Bytes $TailBytes
if ([string]::IsNullOrWhiteSpace($tail.Header)) { throw 'Header CloudWatcher assente.' }
$row = Get-LatestCompleteCloudWatcherRow -Header $tail.Header -Lines $tail.Lines

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
$weather.temperature_c = Convert-ToNullableDouble -Value $row.'Ambient Temperature'
$weather.humidity_pct = Convert-ToNullableDouble -Value $row.'Relative Humidity'
$weather.dew_point_c = Convert-ToNullableDouble -Value $row.'Dew Point'
$weather.wind_speed_kmh = $null
$weather.wind_gust_kmh = $null
$weather.rain_rate_mm_h = $null
$weather.pressure_hpa = Convert-ToNullableDouble -Value $row.'Absolute Pressure'
$weather.sqm_mag_arcsec2 = $null
$weather.sky_temperature_c = $null

$dome = Get-NinaDomeSignal -Path $NinaDomeProjection -Freshness $FreshnessSeconds

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
        dome = $dome
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
        wind_value_raw = Convert-ToNullableDouble -Value $row.'Wind Value'
        rain_value_raw = Convert-ToNullableDouble -Value $row.'Rain Value'
        brightness_value_raw = Convert-ToNullableDouble -Value $row.'Brightness Value'
        raw_ir_temperature = Convert-ToNullableDouble -Value $row.'Raw IR Temperature'
        relative_pressure_raw = Convert-ToNullableDouble -Value $row.'Relative Pressure'
        switch_status = $row.'Switch Status'
        cloudwatcher_safe_status = $row.'Safe Status'
        nina_dome_projection = if (Test-Path -LiteralPath $NinaDomeProjection -PathType Leaf) { $NinaDomeProjection } else { $null }
    }
}

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$tempPath = "$OutputPath.tmp"
$payload | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $tempPath -Encoding UTF8
Move-Item -LiteralPath $tempPath -Destination $OutputPath -Force

Write-Output ('CloudWatcher projection written: {0}' -f $OutputPath)
Write-Output ('Observed UTC: {0}' -f $payload.observed_at_utc)
Write-Output ('Dome: {0} / {1}' -f $dome.state, $dome.quality)
Write-Output ('Weather: {0} / {1}' -f $weather.state, $weather.quality)
Write-Output ('Weather metrics: temp={0}C humidity={1}% dew={2}C pressure={3}hPa' -f $weather.temperature_c, $weather.humidity_pct, $weather.dew_point_c, $weather.pressure_hpa)
Write-Output ('Overall quality: {0}; overall safety: UNKNOWN' -f $payload.quality)