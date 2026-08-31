[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("eagle-health-source-discovery-{0}" -f $stamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Host 'Digital StarGate EAGLE Health source discovery - READ ONLY'
Write-Host ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Host ('Evidence bundle: {0}' -f $bundle)
Write-Host 'Mode: metadata/source capability inspection only; no producer; no device commands; no configuration changes'

function Invoke-SafeProbe {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][scriptblock]$Action
    )

    $started = [DateTime]::UtcNow
    try {
        $data = & $Action
        return [ordered]@{
            name = $Name
            status = 'AVAILABLE'
            error = $null
            elapsed_ms = [math]::Round(([DateTime]::UtcNow - $started).TotalMilliseconds, 1)
            data = @($data)
        }
    } catch {
        return [ordered]@{
            name = $Name
            status = 'UNAVAILABLE'
            error = $_.Exception.Message
            elapsed_ms = [math]::Round(([DateTime]::UtcNow - $started).TotalMilliseconds, 1)
            data = @()
        }
    }
}

function Test-Administrator {
    try {
        $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = [Security.Principal.WindowsPrincipal]::new($identity)
        return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch { return $false }
}

$identity = [ordered]@{
    computer = $env:COMPUTERNAME
    user = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    elevated = (Test-Administrator)
    powershell_version = $PSVersionTable.PSVersion.ToString()
    process_architecture = $env:PROCESSOR_ARCHITECTURE
    observed_at_utc = [DateTime]::UtcNow.ToString('o')
}

$probes = [System.Collections.Generic.List[object]]::new()

$probes.Add((Invoke-SafeProbe -Name 'operating_system' -Action {
    Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,OSArchitecture,LastBootUpTime,TotalVisibleMemorySize,FreePhysicalMemory
}))

$probes.Add((Invoke-SafeProbe -Name 'computer_system' -Action {
    Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,TotalPhysicalMemory,NumberOfLogicalProcessors
}))

$probes.Add((Invoke-SafeProbe -Name 'processor' -Action {
    Get-CimInstance Win32_Processor | Select-Object Name,Manufacturer,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed,LoadPercentage
}))

$probes.Add((Invoke-SafeProbe -Name 'logical_disks' -Action {
    Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | Select-Object DeviceID,VolumeName,FileSystem,Size,FreeSpace
}))

$probes.Add((Invoke-SafeProbe -Name 'physical_disks' -Action {
    Get-PhysicalDisk | Select-Object FriendlyName,SerialNumber,MediaType,BusType,HealthStatus,OperationalStatus,Size
}))

$probes.Add((Invoke-SafeProbe -Name 'storage_reliability_counters' -Action {
    $result = foreach ($disk in Get-PhysicalDisk) {
        try {
            $r = $disk | Get-StorageReliabilityCounter
            [pscustomobject]@{
                FriendlyName = $disk.FriendlyName
                Temperature = $r.Temperature
                TemperatureMax = $r.TemperatureMax
                Wear = $r.Wear
                ReadErrorsTotal = $r.ReadErrorsTotal
                WriteErrorsTotal = $r.WriteErrorsTotal
                PowerOnHours = $r.PowerOnHours
            }
        } catch {
            [pscustomobject]@{ FriendlyName=$disk.FriendlyName; Error=$_.Exception.Message }
        }
    }
    $result
}))

$probes.Add((Invoke-SafeProbe -Name 'windows_time_status' -Action {
    $exe = Join-Path $env:SystemRoot 'System32\w32tm.exe'
    if (-not (Test-Path -LiteralPath $exe)) { throw 'w32tm.exe not found' }
    & $exe /query /status 2>&1 | ForEach-Object { [string]$_ }
}))

$probes.Add((Invoke-SafeProbe -Name 'windows_time_configuration' -Action {
    $exe = Join-Path $env:SystemRoot 'System32\w32tm.exe'
    if (-not (Test-Path -LiteralPath $exe)) { throw 'w32tm.exe not found' }
    & $exe /query /configuration 2>&1 | ForEach-Object { [string]$_ }
}))

$probes.Add((Invoke-SafeProbe -Name 'dsg_scheduled_tasks' -Action {
    Get-ScheduledTask | Where-Object {
        $_.TaskName -match '(?i)(Digital StarGate|DSG)' -or $_.TaskPath -match '(?i)(DigitalStarGate|DSG)'
    } | ForEach-Object {
        $info = $_ | Get-ScheduledTaskInfo
        [pscustomobject]@{
            TaskName = $_.TaskName
            TaskPath = $_.TaskPath
            State = $_.State
            LastRunTime = $info.LastRunTime
            LastTaskResult = $info.LastTaskResult
            NextRunTime = $info.NextRunTime
        }
    }
}))

$probes.Add((Invoke-SafeProbe -Name 'relevant_processes' -Action {
    Get-Process -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -match '(?i)(NINA|PHD2|ASCOM|CloudWatcher|DigitalStarGate|DSG)'
    } | Select-Object ProcessName,Id,StartTime,Path,WorkingSet64,CPU
}))

$probes.Add((Invoke-SafeProbe -Name 'event_log_recent_errors' -Action {
    $since = [DateTime]::Now.AddDays(-7)
    foreach ($logName in @('System','Application')) {
        Get-WinEvent -FilterHashtable @{ LogName=$logName; Level=@(1,2); StartTime=$since } -MaxEvents 100 -ErrorAction Stop |
            Select-Object @{n='LogName';e={$logName}},TimeCreated,Id,LevelDisplayName,ProviderName,Message
    }
}))

$probes.Add((Invoke-SafeProbe -Name 'usb_pnp_inventory' -Action {
    Get-CimInstance Win32_PnPEntity | Where-Object {
        $_.PNPClass -eq 'USB' -or $_.DeviceID -match '^USB'
    } | Select-Object Name,PNPClass,Status,Manufacturer,DeviceID
}))

$probes.Add((Invoke-SafeProbe -Name 'serial_ports' -Action {
    Get-CimInstance Win32_SerialPort | Select-Object DeviceID,Name,Description,ProviderType,Status,PNPDeviceID
}))

$probes.Add((Invoke-SafeProbe -Name 'pending_reboot_registry' -Action {
    $paths = @(
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending',
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired',
        'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager'
    )
    foreach ($path in $paths) {
        $exists = Test-Path -LiteralPath $path
        $pendingRename = $null
        if ($path -like '*Session Manager' -and $exists) {
            try { $pendingRename = (Get-ItemProperty -LiteralPath $path -Name PendingFileRenameOperations -ErrorAction Stop).PendingFileRenameOperations } catch { }
        }
        [pscustomobject]@{ Path=$path; Exists=$exists; PendingFileRenameOperations=@($pendingRename) }
    }
}))

$probes.Add((Invoke-SafeProbe -Name 'windows_update_service' -Action {
    Get-Service -Name wuauserv -ErrorAction Stop | Select-Object Name,Status,StartType
}))

$probes.Add((Invoke-SafeProbe -Name 'dsg_paths' -Action {
    $paths = @(
        'C:\DigitalStarGate',
        'C:\DigitalStarGate\TelemetryRuntime',
        'C:\DigitalStarGate\SessionReports',
        (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry'),
        (Join-Path $env:LOCALAPPDATA 'NINA\Plugins\3.0.0\Digital StarGate Dome Telemetry Exporter'),
        'C:\Users\PrimaLuceLab\Documents\CloudWatcher'
    )
    foreach ($path in $paths) {
        $item = Get-Item -LiteralPath $path -ErrorAction SilentlyContinue
        [pscustomobject]@{
            Path = $path
            Exists = ($null -ne $item)
            LastWriteTimeUtc = if ($item) { $item.LastWriteTimeUtc } else { $null }
        }
    }
}))

$probes.Add((Invoke-SafeProbe -Name 'known_log_files' -Action {
    $roots = @(
        'C:\Users\PrimaLuceLab\Documents\CloudWatcher',
        'C:\Users\PrimaLuceLab\Documents\ASCOM',
        'C:\DigitalStarGate\TelemetryRuntime'
    )
    foreach ($root in $roots) {
        if (-not (Test-Path -LiteralPath $root)) { continue }
        Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '(?i)(log|csv|json|txt|dat)$' } |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 25 FullName,Length,LastWriteTimeUtc
    }
}))

$payload = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.EagleHealthSourceDiscovery'
    mode = 'READ_ONLY_DISCOVERY'
    identity = $identity
    probes = @($probes)
    disposition = 'DISCOVERY_ONLY_NOT_BKL030_ACCEPTANCE'
}

$jsonPath = Join-Path $bundle 'eagle-health-source-discovery.json'
$txtPath = Join-Path $bundle 'eagle-health-source-discovery.txt'

$payload | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add('Digital StarGate EAGLE Health Source Discovery')
$lines.Add(('Computer: {0}' -f $identity.computer))
$lines.Add(('User: {0}' -f $identity.user))
$lines.Add(('Elevated: {0}' -f $identity.elevated))
$lines.Add('')
foreach ($probe in $probes) {
    $lines.Add(('=== {0} ===' -f $probe.name))
    $lines.Add(('Status: {0}' -f $probe.status))
    $lines.Add(('Elapsed ms: {0}' -f $probe.elapsed_ms))
    if ($probe.error) { $lines.Add(('Error: {0}' -f $probe.error)) }
    foreach ($row in @($probe.data)) { $lines.Add(($row | Out-String).TrimEnd()) }
    $lines.Add('')
}
$lines.Add('DISPOSITION: DISCOVERY_ONLY_NOT_BKL030_ACCEPTANCE')
$lines | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Host ''
Write-Host '=== DISCOVERY SUMMARY ==='
$probes | Select-Object name,status,elapsed_ms,error | Format-Table -AutoSize
Write-Host ('Evidence JSON: {0}' -f $jsonPath)
Write-Host ('Evidence TXT : {0}' -f $txtPath)
Write-Host 'EAGLE HEALTH SOURCE DISCOVERY RESULT: PASS (inventory status recorded; not BKL-030 acceptance)'
