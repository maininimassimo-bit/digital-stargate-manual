[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [string]$ProgId = 'ASCOM.CloudWatcher.ObservingConditions',
    [switch]$ExecuteProbe
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-ascom-skyquality-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate CloudWatcher ASCOM SkyQuality probe'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('ProgID: {0}' -f $ProgId)
Write-Output ('ExecuteProbe: {0}' -f [bool]$ExecuteProbe)
Write-Output ('Evidence bundle: {0}' -f $bundle)

function Get-RegistrationEvidence {
    param([Parameter(Mandatory = $true)][string]$DriverProgId)

    $paths = @(
        "Registry::HKEY_CLASSES_ROOT\$DriverProgId",
        "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\ASCOM\ObservingConditions Drivers\$DriverProgId",
        "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\ASCOM\ObservingConditions Drivers\$DriverProgId"
    )

    $entries = @()
    foreach ($path in $paths) {
        if (-not (Test-Path -LiteralPath $path)) { continue }
        try {
            $item = Get-Item -LiteralPath $path -ErrorAction Stop
            $values = @()
            foreach ($name in $item.GetValueNames()) {
                $value = [string]$item.GetValue($name)
                if ($name -match '(?i)(password|secret|token|credential|community|key)') { continue }
                $values += [pscustomobject]@{
                    name = if ([string]::IsNullOrWhiteSpace($name)) { '(Default)' } else { $name }
                    value = $value
                }
            }
            $entries += [pscustomobject]@{ path = $path; values = $values }
        }
        catch { }
    }
    return @($entries)
}

$registration = @(Get-RegistrationEvidence -DriverProgId $ProgId)
$processes = @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -match '(?i)(CloudWatcher|CWAscom)'
} | Select-Object ProcessName,Id,Path)

$probe = [ordered]@{
    attempted = $false
    object_created = $false
    connected_before = $null
    connected_after = $null
    connected_set_true = $false
    connected_set_false = $false
    name = $null
    description = $null
    driver_info = $null
    driver_version = $null
    interface_version = $null
    sky_quality_read = $false
    sky_quality_mag_arcsec2 = $null
    sky_quality_sensor_description = $null
    sky_quality_time_since_last_update_seconds = $null
    error = $null
}

$driver = $null
if ($ExecuteProbe) {
    $probe.attempted = $true
    try {
        $type = [type]::GetTypeFromProgID($ProgId)
        if (-not $type) { throw "ProgID non registrato: $ProgId" }
        $driver = [Activator]::CreateInstance($type)
        $probe.object_created = $true

        foreach ($propertyName in @('Name','Description','DriverInfo','DriverVersion','InterfaceVersion')) {
            try {
                if ($driver.PSObject.Properties.Name -contains $propertyName) {
                    $probe[$propertyName.ToLowerInvariant()] = [string]$driver.$propertyName
                }
            }
            catch { }
        }

        if (-not ($driver.PSObject.Properties.Name -contains 'Connected')) {
            throw 'Driver ASCOM privo della property Connected attesa.'
        }

        try { $probe.connected_before = [bool]$driver.Connected } catch { }
        if (-not $probe.connected_before) {
            $driver.Connected = $true
            $probe.connected_set_true = $true
        }
        $probe.connected_after = [bool]$driver.Connected
        if (-not $probe.connected_after) { throw 'Connessione ASCOM non confermata.' }

        try {
            $value = [double]$driver.SkyQuality
            if ([double]::IsNaN($value) -or [double]::IsInfinity($value)) { throw 'SkyQuality non numerico.' }
            $probe.sky_quality_mag_arcsec2 = $value
            $probe.sky_quality_read = $true
        }
        catch {
            throw "SkyQuality non leggibile: $($_.Exception.Message)"
        }

        try {
            if ($driver.PSObject.Methods.Name -contains 'SensorDescription') {
                $probe.sky_quality_sensor_description = [string]$driver.SensorDescription('SkyQuality')
            }
        }
        catch { }

        try {
            if ($driver.PSObject.Methods.Name -contains 'TimeSinceLastUpdate') {
                $probe.sky_quality_time_since_last_update_seconds = [double]$driver.TimeSinceLastUpdate('SkyQuality')
            }
        }
        catch { }
    }
    catch {
        $probe.error = $_.Exception.Message
    }
    finally {
        if ($driver) {
            try {
                if ($probe.connected_set_true -and ($driver.PSObject.Properties.Name -contains 'Connected')) {
                    $driver.Connected = $false
                    $probe.connected_set_false = $true
                }
            }
            catch { }
            try { [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($driver) } catch { }
        }
    }
}

$disposition = if (-not $ExecuteProbe) {
    'PREFLIGHT_ONLY_NO_ASCOM_ACTIVATION'
}
elseif ($probe.sky_quality_read) {
    'ASCOM_SKYQUALITY_READ_SUCCEEDED_REQUIRES_PLAUSIBILITY_AND_FRESHNESS_REVIEW'
}
elseif ($probe.object_created) {
    'ASCOM_OBJECT_CREATED_SKYQUALITY_NOT_READABLE'
}
else {
    'ASCOM_PROBE_FAILED_BEFORE_OBJECT_CREATION'
}

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.CloudWatcherAscomSkyQualityProbe'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = if ($ExecuteProbe) { 'EXPLICIT_READ_ONLY_ASCOM_OBSERVINGCONDITIONS_PROBE' } else { 'PREFLIGHT_ONLY_NO_ASCOM_ACTIVATION' }
    prog_id = $ProgId
    registration = $registration
    running_processes = $processes
    probe = $probe
    conclusions = [ordered]@{
        sqm_candidate_verified = [bool]$probe.sky_quality_read
        sqm_value_published = $false
        serial_port_opened_directly = $false
        configuration_changed = $false
        safety_command_sent = $false
        disposition = $disposition
        note = 'Probe reads only ASCOM ObservingConditions metadata and SkyQuality. No direct serial access and no SafetyMonitor interaction. A numeric value is not promoted to production until plausibility, provenance and freshness are validated.'
    }
}

$jsonPath = Join-Path $bundle 'cloudwatcher-ascom-skyquality.json'
$txtPath = Join-Path $bundle 'cloudwatcher-ascom-skyquality.txt'
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== REGISTRATION ===',
    ($registration | Format-List | Out-String),
    '=== RUNNING PROCESSES ===',
    ($processes | Format-Table -AutoSize | Out-String),
    '=== PROBE ===',
    ($probe | Format-List | Out-String),
    '=== CONCLUSIONS ===',
    ($report.conclusions | Format-List | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== REGISTRATION ==='
if ($registration.Count -gt 0) { $registration | Format-List | Out-String | Write-Output } else { Write-Output '(registration not found)' }
Write-Output '=== RUNNING PROCESSES ==='
if ($processes.Count -gt 0) { $processes | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none)' }
Write-Output '=== PROBE ==='
$probe | Format-List | Out-String | Write-Output
Write-Output '=== DISPOSITION ==='
Write-Output $disposition
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'CLOUDWATCHER ASCOM SKYQUALITY PROBE RESULT: evidence recorded; not BKL-029 acceptance'
