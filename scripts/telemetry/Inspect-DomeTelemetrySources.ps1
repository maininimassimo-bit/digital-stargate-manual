[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("dome-source-inventory-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

function Safe-GetChildItem {
    param([string]$Path)
    try {
        if (Test-Path -LiteralPath $Path) {
            return @(Get-ChildItem -LiteralPath $Path -ErrorAction Stop | Select-Object Name, PSPath, Property)
        }
    }
    catch { }
    return @()
}

function Safe-GetRegistryChildren {
    param([string]$Path)
    $items = @()
    try {
        if (Test-Path $Path) {
            foreach ($key in Get-ChildItem $Path -ErrorAction Stop) {
                $props = $null
                try { $props = Get-ItemProperty -Path $key.PSPath -ErrorAction Stop } catch { }
                $items += [pscustomobject]@{
                    hive_path = $Path
                    key_name = $key.PSChildName
                    prog_id = if ($props -and $props.PSObject.Properties['ProgID']) { [string]$props.ProgID } else { $null }
                    description = if ($props -and $props.PSObject.Properties['Description']) { [string]$props.Description } else { $null }
                }
            }
        }
    }
    catch { }
    return $items
}

Write-Output 'Digital StarGate dome telemetry source inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)

$processes = @(Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -match '(?i)nina|ascom|alpaca|dome|roof|relay|eagle' } |
    Select-Object ProcessName, Id, Path)

$services = @(Get-Service -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '(?i)nina|ascom|alpaca|dome|roof|relay|eagle' -or $_.DisplayName -match '(?i)nina|ascom|alpaca|dome|roof|relay|eagle' } |
    Select-Object Name, DisplayName, Status, StartType)

$registryPaths = @(
    'HKCU:\Software\ASCOM\Dome Drivers',
    'HKLM:\Software\ASCOM\Dome Drivers',
    'HKLM:\Software\WOW6432Node\ASCOM\Dome Drivers',
    'HKCU:\Software\WOW6432Node\ASCOM\Dome Drivers'
)
$ascomDomeDrivers = @()
foreach ($path in $registryPaths) {
    $ascomDomeDrivers += Safe-GetRegistryChildren -Path $path
}

$candidatePaths = @(
    (Join-Path $env:LOCALAPPDATA 'NINA'),
    (Join-Path $env:APPDATA 'NINA'),
    'C:\Program Files\ASCOM',
    'C:\Program Files (x86)\ASCOM',
    'C:\ProgramData\ASCOM',
    'C:\DigitalStarGate'
)

$pathStatus = foreach ($path in $candidatePaths) {
    [pscustomobject]@{
        path = $path
        exists = [bool](Test-Path -LiteralPath $path)
    }
}

$serialPorts = @()
try {
    $serialPorts = @(Get-CimInstance Win32_SerialPort -ErrorAction Stop |
        Select-Object DeviceID, Name, Description, PNPDeviceID)
}
catch { }

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.DomeTelemetrySourceInspector'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = 'READ_ONLY_NO_DEVICE_CONNECTIONS'
    processes = $processes
    services = $services
    ascom_dome_drivers = $ascomDomeDrivers
    candidate_paths = @($pathStatus)
    serial_ports = $serialPorts
    conclusions = [ordered]@{
        operational_interface_verified = $false
        commands_sent = $false
        device_connections_opened = $false
        note = 'Inventory only. A runtime dome adapter must not be enabled until the actual source, semantics, polarity and freshness are validated on EAGLE30154.'
    }
}

$jsonPath = Join-Path $bundle 'dome-source-inventory.json'
$txtPath = Join-Path $bundle 'dome-source-inventory.txt'

$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== PROCESSES ===',
    ($processes | Format-Table -AutoSize | Out-String),
    '=== SERVICES ===',
    ($services | Format-Table -AutoSize | Out-String),
    '=== ASCOM DOME DRIVERS ===',
    ($ascomDomeDrivers | Format-Table -AutoSize | Out-String),
    '=== CANDIDATE PATHS ===',
    ($pathStatus | Format-Table -AutoSize | Out-String),
    '=== SERIAL PORTS ===',
    ($serialPorts | Format-Table -AutoSize | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== ASCOM DOME DRIVERS ==='
if ($ascomDomeDrivers.Count -gt 0) { $ascomDomeDrivers | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== RELEVANT PROCESSES ==='
if ($processes.Count -gt 0) { $processes | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== RELEVANT SERVICES ==='
if ($services.Count -gt 0) { $services | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== CANDIDATE PATHS ==='
$pathStatus | Format-Table -AutoSize | Out-String | Write-Output
Write-Output '=== SERIAL PORTS ==='
if ($serialPorts.Count -gt 0) { $serialPorts | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output ('Evidence: {0}' -f $jsonPath)
Write-Output 'DOME SOURCE INVENTORY RESULT: PASS (inventory only)'
