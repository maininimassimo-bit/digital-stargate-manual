[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [string]$CloudWatcherCsv = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    [ValidateRange(4096, 1048576)][int]$TailBytes = 262144,
    [string]$AscomProgId,
    [switch]$ProbeAscomSkyQuality
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("sqm-source-inventory-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate SQM telemetry source inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)
Write-Output ('ASCOM probe requested: {0}' -f [bool]$ProbeAscomSkyQuality)

function Get-SafeRegistryChildren {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) { return @() }

    try {
        return @(Get-ChildItem -LiteralPath $Path -ErrorAction Stop | ForEach-Object {
            $item = Get-ItemProperty -LiteralPath $_.PSPath -ErrorAction SilentlyContinue
            [pscustomobject]@{
                registry_path = $_.PSPath
                key_name = $_.PSChildName
                description = if ($item -and $item.PSObject.Properties.Name -contains '') { [string]$item.'' } elseif ($item -and $item.PSObject.Properties.Name -contains 'Description') { [string]$item.Description } else { $null }
                driver_version = if ($item -and $item.PSObject.Properties.Name -contains 'DriverVersion') { [string]$item.DriverVersion } else { $null }
            }
        })
    }
    catch {
        return @([pscustomobject]@{
            registry_path = $Path
            key_name = $null
            description = $null
            driver_version = $null
            error = $_.Exception.Message
        })
    }
}

function Get-SafeCim {
    param([Parameter(Mandatory = $true)][string]$ClassName)
    try { return @(Get-CimInstance -ClassName $ClassName -ErrorAction Stop) } catch { return @() }
}

function Get-CsvFieldCount {
    param([Parameter(Mandatory = $true)][string]$Line)
    return ([regex]::Matches($Line, ',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)').Count + 1)
}

function Get-CloudWatcherSnapshot {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][int]$Bytes
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return [pscustomobject]@{
            exists = $false
            path = $Path
            header = $null
            fields = @()
            sqm_candidate_fields = @()
            latest_complete_row = $null
            latest_values = $null
            error = $null
        }
    }

    $stream = $null
    $reader = $null
    try {
        $stream = [System.IO.File]::Open($Path,[System.IO.FileMode]::Open,[System.IO.FileAccess]::Read,[System.IO.FileShare]::ReadWrite)
        $reader = New-Object System.IO.StreamReader($stream)
        $header = $reader.ReadLine()
        if ([string]::IsNullOrWhiteSpace($header)) { throw 'Header CloudWatcher assente.' }

        $length = $stream.Length
        $start = [math]::Max(0, $length - $Bytes)
        $stream.Seek($start, [System.IO.SeekOrigin]::Begin) | Out-Null
        $reader.DiscardBufferedData()
        if ($start -gt 0) { [void]$reader.ReadLine() }

        $lines = New-Object System.Collections.Generic.List[string]
        while (-not $reader.EndOfStream) {
            $line = $reader.ReadLine()
            if (-not [string]::IsNullOrWhiteSpace($line)) { $lines.Add($line) }
        }

        $headerCount = Get-CsvFieldCount -Line $header
        $row = $null
        $rowLine = $null
        for ($i = $lines.Count - 1; $i -ge 0; $i--) {
            if ((Get-CsvFieldCount -Line $lines[$i]) -ne $headerCount) { continue }
            try {
                $candidate = @($header, $lines[$i]) | ConvertFrom-Csv | Select-Object -First 1
                if ($candidate) {
                    $row = $candidate
                    $rowLine = $lines[$i]
                    break
                }
            }
            catch { }
        }

        $fieldNames = @()
        if ($row) { $fieldNames = @($row.PSObject.Properties | ForEach-Object { $_.Name }) }
        elseif ($header) {
            $fieldNames = @($header -split ',' | ForEach-Object { $_.Trim().Trim('"') })
        }

        $sqmCandidates = @($fieldNames | Where-Object {
            $_ -match '(?i)(^|[^a-z])(sqm|sky\s*quality|mpsas|mag.*arcsec|arcsec.*mag)([^a-z]|$)'
        })

        $latestValues = $null
        if ($row) {
            $latestValues = [ordered]@{}
            foreach ($property in $row.PSObject.Properties) {
                $latestValues[$property.Name] = $property.Value
            }
        }

        return [pscustomobject]@{
            exists = $true
            path = $Path
            last_write_time_utc = (Get-Item -LiteralPath $Path).LastWriteTimeUtc.ToString('o')
            size_bytes = (Get-Item -LiteralPath $Path).Length
            header = $header
            fields = $fieldNames
            sqm_candidate_fields = $sqmCandidates
            latest_complete_row = $rowLine
            latest_values = $latestValues
            error = $null
        }
    }
    catch {
        return [pscustomobject]@{
            exists = $true
            path = $Path
            header = $null
            fields = @()
            sqm_candidate_fields = @()
            latest_complete_row = $null
            latest_values = $null
            error = $_.Exception.Message
        }
    }
    finally {
        if ($reader) { $reader.Dispose() }
        elseif ($stream) { $stream.Dispose() }
    }
}

function Invoke-AscomSkyQualityProbe {
    param([Parameter(Mandatory = $true)][string]$ProgId)

    $result = [ordered]@{
        requested = $true
        prog_id = $ProgId
        connected = $false
        sky_quality_read = $false
        sky_quality_mag_arcsec2 = $null
        sensor_description = $null
        driver_info = $null
        driver_version = $null
        interface_version = $null
        error = $null
        disconnected = $false
    }

    $driver = $null
    try {
        $type = [type]::GetTypeFromProgID($ProgId)
        if (-not $type) { throw "ProgID ASCOM non registrato: $ProgId" }
        $driver = [Activator]::CreateInstance($type)

        if ($driver.PSObject.Properties.Name -contains 'DriverInfo') { $result.driver_info = [string]$driver.DriverInfo }
        if ($driver.PSObject.Properties.Name -contains 'DriverVersion') { $result.driver_version = [string]$driver.DriverVersion }
        if ($driver.PSObject.Properties.Name -contains 'InterfaceVersion') { $result.interface_version = [string]$driver.InterfaceVersion }

        if (-not ($driver.PSObject.Properties.Name -contains 'Connected')) {
            throw 'Il driver non espone la property Connected attesa dal contratto ASCOM.'
        }

        $driver.Connected = $true
        $result.connected = [bool]$driver.Connected
        if (-not $result.connected) { throw 'Connessione ASCOM non confermata.' }

        try {
            $value = [double]$driver.SkyQuality
            if ([double]::IsNaN($value) -or [double]::IsInfinity($value)) { throw 'SkyQuality non numerico.' }
            $result.sky_quality_mag_arcsec2 = $value
            $result.sky_quality_read = $true
        }
        catch {
            throw "SkyQuality non leggibile: $($_.Exception.Message)"
        }

        try {
            if ($driver.PSObject.Methods.Name -contains 'SensorDescription') {
                $result.sensor_description = [string]$driver.SensorDescription('SkyQuality')
            }
        }
        catch { }
    }
    catch {
        $result.error = $_.Exception.Message
    }
    finally {
        if ($driver) {
            try {
                if ($driver.PSObject.Properties.Name -contains 'Connected') { $driver.Connected = $false }
                $result.disconnected = $true
            }
            catch { }
            try { [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($driver) } catch { }
        }
    }

    return [pscustomobject]$result
}

$ascomRegistryRoots = @(
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\ASCOM\ObservingConditions',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\ASCOM\ObservingConditions',
    'Registry::HKEY_CURRENT_USER\SOFTWARE\ASCOM\ObservingConditions'
)

$ascomDrivers = @()
foreach ($root in $ascomRegistryRoots) {
    $ascomDrivers += @(Get-SafeRegistryChildren -Path $root)
}
$ascomDrivers = @($ascomDrivers | Sort-Object registry_path -Unique)

$cloudWatcher = Get-CloudWatcherSnapshot -Path $CloudWatcherCsv -Bytes $TailBytes

$installedSoftware = @(
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'Registry::HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
) | ForEach-Object {
    Get-ItemProperty -Path $_ -ErrorAction SilentlyContinue
} | Where-Object {
    $displayNameProperty = $_.PSObject.Properties['DisplayName']
    if ($null -eq $displayNameProperty) { return $false }
    $displayName = [string]$displayNameProperty.Value
    -not [string]::IsNullOrWhiteSpace($displayName) -and $displayName -match '(?i)ASCOM|CloudWatcher|Lunatico|Unihedron|Sky Quality|SQM'
} | Select-Object DisplayName, DisplayVersion, Publisher, InstallLocation, PSPath

$relevantProcesses = @(Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -match '(?i)cloudwatch|lunatico|ascom|sqm|unihedron' } |
    Select-Object ProcessName, Id, Path)

$relevantServices = @(Get-Service -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '(?i)cloudwatch|lunatico|ascom|sqm|unihedron' -or $_.DisplayName -match '(?i)cloudwatch|lunatico|ascom|sqm|unihedron' } |
    Select-Object Name, DisplayName, Status, StartType)

$pnpCandidates = @(Get-SafeCim -ClassName 'Win32_PnPEntity' |
    Where-Object { $_.Name -match '(?i)cloudwatch|lunatico|sqm|unihedron|sky quality' -or $_.Description -match '(?i)cloudwatch|lunatico|sqm|unihedron|sky quality' } |
    Select-Object Name, Description, PNPDeviceID, Status, Manufacturer)

$serialPorts = @(Get-SafeCim -ClassName 'Win32_SerialPort' |
    Select-Object DeviceID, Name, Description, PNPDeviceID, Status)

$ascomProbe = [pscustomobject]@{
    requested = [bool]$ProbeAscomSkyQuality
    prog_id = $AscomProgId
    connected = $false
    sky_quality_read = $false
    sky_quality_mag_arcsec2 = $null
    sensor_description = $null
    driver_info = $null
    driver_version = $null
    interface_version = $null
    error = if ($ProbeAscomSkyQuality -and [string]::IsNullOrWhiteSpace($AscomProgId)) { 'Probe richiesto senza -AscomProgId.' } else { $null }
    disconnected = $false
}

if ($ProbeAscomSkyQuality -and -not [string]::IsNullOrWhiteSpace($AscomProgId)) {
    $ascomProbe = Invoke-AscomSkyQualityProbe -ProgId $AscomProgId
}

$cloudWatcherHasSqmField = @($cloudWatcher.sqm_candidate_fields).Count -gt 0
$ascomInventoryHasCandidates = @($ascomDrivers | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_.key_name) }).Count -gt 0
$ascomVerified = [bool]($ascomProbe.sky_quality_read -and $null -ne $ascomProbe.sky_quality_mag_arcsec2)

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.SqmTelemetrySourceInspector'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = if ($ProbeAscomSkyQuality) { 'READ_ONLY_INVENTORY_PLUS_EXPLICIT_ASCOM_READ_PROBE' } else { 'READ_ONLY_PASSIVE_INVENTORY_NO_DEVICE_CONNECTIONS' }
    ascom = [ordered]@{
        registry_roots = $ascomRegistryRoots
        observing_conditions_drivers = $ascomDrivers
        probe = $ascomProbe
    }
    cloudwatcher = $cloudWatcher
    host = [ordered]@{
        installed_software = @($installedSoftware)
        relevant_processes = $relevantProcesses
        relevant_services = $relevantServices
        pnp_candidates = $pnpCandidates
        serial_ports = $serialPorts
    }
    conclusions = [ordered]@{
        cloudwatcher_sqm_candidate_field_found = $cloudWatcherHasSqmField
        ascom_observing_conditions_candidate_found = $ascomInventoryHasCandidates
        ascom_sky_quality_verified = $ascomVerified
        sqm_source_verified = $ascomVerified
        source_disposition = if ($ascomVerified) { 'VERIFIED_ASCOM_SKYQUALITY' } elseif ($cloudWatcherHasSqmField) { 'CANDIDATE_CLOUDWATCHER_FIELD_REQUIRES_SEMANTIC_VERIFICATION' } elseif ($ascomInventoryHasCandidates) { 'CANDIDATE_ASCOM_DRIVER_REQUIRES_EXPLICIT_PROBE' } else { 'NO_VERIFIED_SOURCE_FOUND' }
        configuration_changed = $false
        device_command_sent = $false
        note = 'Inventory never infers SQM from brightness/cloud/sky temperature. Explicit ASCOM probe only connects the selected ObservingConditions driver, reads SkyQuality metadata/value, then disconnects.'
    }
}

$jsonPath = Join-Path $bundle 'sqm-source-inventory.json'
$txtPath = Join-Path $bundle 'sqm-source-inventory.txt'
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== ASCOM OBSERVING CONDITIONS REGISTRY ===',
    ($ascomDrivers | Format-Table -AutoSize | Out-String),
    '=== ASCOM SKYQUALITY PROBE ===',
    ($ascomProbe | Format-List | Out-String),
    '=== CLOUDWATCHER CSV ===',
    ($cloudWatcher | Format-List exists,path,last_write_time_utc,size_bytes,header,sqm_candidate_fields,error | Out-String),
    '=== INSTALLED SOFTWARE ===',
    ($installedSoftware | Format-Table -AutoSize | Out-String),
    '=== RELEVANT PROCESSES ===',
    ($relevantProcesses | Format-Table -AutoSize | Out-String),
    '=== RELEVANT SERVICES ===',
    ($relevantServices | Format-Table -AutoSize | Out-String),
    '=== PNP CANDIDATES ===',
    ($pnpCandidates | Format-Table -AutoSize | Out-String),
    '=== SERIAL PORTS ===',
    ($serialPorts | Format-Table -AutoSize | Out-String),
    '=== CONCLUSIONS ===',
    ($report.conclusions | Format-List | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== ASCOM OBSERVING CONDITIONS CANDIDATES ==='
if ($ascomDrivers.Count -gt 0) { $ascomDrivers | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== CLOUDWATCHER SQM CANDIDATE FIELDS ==='
if (@($cloudWatcher.sqm_candidate_fields).Count -gt 0) { @($cloudWatcher.sqm_candidate_fields) | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== PNP / SERIAL CANDIDATES ==='
if ($pnpCandidates.Count -gt 0) { $pnpCandidates | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(no named SQM candidates found via PnP)' }
$serialPorts | Format-Table -AutoSize | Out-String | Write-Output
Write-Output '=== SOURCE DISPOSITION ==='
Write-Output $report.conclusions.source_disposition
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'SQM SOURCE INVENTORY RESULT: PASS (inventory/probe status recorded; not BKL-029 acceptance)'
