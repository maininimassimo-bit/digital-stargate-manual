[CmdletBinding()]
param(
  [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("eagle-health-gap-reconciliation-{0}" -f $stamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Host 'Digital StarGate EAGLE Health gap reconciliation - READ ONLY'
Write-Host ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Host ('Evidence bundle: {0}' -f $bundle)
Write-Host 'Mode: source reconciliation only; no producer; no device commands; no configuration changes'

function Invoke-SafeProbe {
  param(
    [Parameter(Mandatory)][string]$Name,
    [Parameter(Mandatory)][scriptblock]$Action
  )

  $started = [DateTime]::UtcNow
  try {
    $data = & $Action
    [ordered]@{
      name = $Name
      status = 'AVAILABLE'
      error = $null
      elapsed_ms = [math]::Round(([DateTime]::UtcNow - $started).TotalMilliseconds, 1)
      data = @($data)
    }
  } catch {
    [ordered]@{
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
  } catch {
    return $false
  }
}

$identity = [ordered]@{
  computer = $env:COMPUTERNAME
  user = [Security.Principal.WindowsIdentity]::GetCurrent().Name
  elevated = (Test-Administrator)
  observed_at_utc = [DateTime]::UtcNow.ToString('o')
}

$probes = [System.Collections.Generic.List[object]]::new()

$probes.Add((Invoke-SafeProbe -Name 'hardware_temperature_candidates' -Action {
  $rows = [System.Collections.Generic.List[object]]::new()

  try {
    Get-CimInstance -Namespace 'root/wmi' -ClassName MSAcpi_ThermalZoneTemperature -ErrorAction Stop |
      ForEach-Object {
        $celsius = if ($null -ne $_.CurrentTemperature) {
          [math]::Round((([double]$_.CurrentTemperature / 10.0) - 273.15), 2)
        } else { $null }
        $rows.Add([pscustomobject]@{
          Source = 'root/wmi:MSAcpi_ThermalZoneTemperature'
          InstanceName = $_.InstanceName
          CurrentTemperatureC = $celsius
          CriticalTripPointRaw = $_.CriticalTripPoint
        })
      }
  } catch {
    $rows.Add([pscustomobject]@{
      Source = 'root/wmi:MSAcpi_ThermalZoneTemperature'
      Error = $_.Exception.Message
    })
  }

  try {
    Get-CimInstance -Namespace 'root/cimv2' -ClassName Win32_TemperatureProbe -ErrorAction Stop |
      ForEach-Object {
        $rows.Add([pscustomobject]@{
          Source = 'root/cimv2:Win32_TemperatureProbe'
          Name = $_.Name
          Status = $_.Status
          CurrentReading = $_.CurrentReading
          NominalReading = $_.NominalReading
        })
      }
  } catch {
    $rows.Add([pscustomobject]@{
      Source = 'root/cimv2:Win32_TemperatureProbe'
      Error = $_.Exception.Message
    })
  }

  $rows
}))

$probes.Add((Invoke-SafeProbe -Name 'windows_time_service_and_registry' -Action {
  $svc = Get-CimInstance Win32_Service -Filter "Name='W32Time'" -ErrorAction Stop
  [pscustomobject]@{
    Source = 'Win32_Service:W32Time'
    State = $svc.State
    StartMode = $svc.StartMode
    StartName = $svc.StartName
    ProcessId = $svc.ProcessId
  }

  $parametersPath = 'HKLM:\SYSTEM\CurrentControlSet\Services\W32Time\Parameters'
  if (Test-Path -LiteralPath $parametersPath) {
    $p = Get-ItemProperty -LiteralPath $parametersPath -ErrorAction Stop
    [pscustomobject]@{
      Source = 'registry:W32Time.Parameters'
      Type = $p.Type
      NtpServer = $p.NtpServer
    }
  }

  $clientPath = 'HKLM:\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpClient'
  if (Test-Path -LiteralPath $clientPath) {
    $c = Get-ItemProperty -LiteralPath $clientPath -ErrorAction Stop
    [pscustomobject]@{
      Source = 'registry:W32Time.NtpClient'
      Enabled = $c.Enabled
      SpecialPollInterval = $c.SpecialPollInterval
    }
  }
}))

$probes.Add((Invoke-SafeProbe -Name 'clock_sync_event_evidence' -Action {
  $since = [DateTime]::Now.AddDays(-30)
  $providerCandidates = @('Microsoft-Windows-Time-Service','Time-Service')
  foreach ($provider in $providerCandidates) {
    try {
      Get-WinEvent -FilterHashtable @{ LogName='System'; ProviderName=$provider; StartTime=$since } -MaxEvents 50 -ErrorAction Stop |
        Select-Object TimeCreated,Id,LevelDisplayName,ProviderName,Message
    } catch {
      [pscustomobject]@{ Provider=$provider; Error=$_.Exception.Message }
    }
  }
}))

$probes.Add((Invoke-SafeProbe -Name 'dsg_scheduled_task_contracts' -Action {
  Get-ScheduledTask | Where-Object {
    $_.TaskName -match '(?i)(Digital StarGate|DSG)' -or $_.TaskPath -match '(?i)(DigitalStarGate|DSG)'
  } | ForEach-Object {
    $task = $_
    $info = $task | Get-ScheduledTaskInfo
    [pscustomobject]@{
      TaskName = $task.TaskName
      TaskPath = $task.TaskPath
      State = $task.State
      LastRunTime = $info.LastRunTime
      LastTaskResult = $info.LastTaskResult
      LastTaskResultHex = ('0x{0:X8}' -f ([uint32]$info.LastTaskResult))
      NextRunTime = $info.NextRunTime
      PrincipalUserId = $task.Principal.UserId
      PrincipalLogonType = $task.Principal.LogonType
      PrincipalRunLevel = $task.Principal.RunLevel
      Actions = @($task.Actions | ForEach-Object {
        [pscustomobject]@{ Execute=$_.Execute; Arguments=$_.Arguments; WorkingDirectory=$_.WorkingDirectory }
      })
      Triggers = @($task.Triggers | ForEach-Object {
        [pscustomobject]@{ Enabled=$_.Enabled; StartBoundary=$_.StartBoundary; EndBoundary=$_.EndBoundary }
      })
    }
  }
}))

$probes.Add((Invoke-SafeProbe -Name 'serial_port_reconciliation' -Action {
  [pscustomobject]@{
    Source = 'Win32_SerialPort'
    Items = @(Get-CimInstance Win32_SerialPort -ErrorAction SilentlyContinue |
      Select-Object DeviceID,Name,Description,Status,PNPDeviceID)
  }

  [pscustomobject]@{
    Source = 'Win32_PnPEntity PortsClass'
    Items = @(Get-CimInstance Win32_PnPEntity -ErrorAction Stop |
      Where-Object {
        $_.PNPClass -eq 'Ports' -or $_.Name -match '(?i)\(COM\d+\)' -or $_.DeviceID -match '(?i)(VID_0403|VID_067B|FTDI|PROLIFIC)'
      } |
      Select-Object Name,PNPClass,Status,Manufacturer,DeviceID)
  }

  $serialComm = 'HKLM:\HARDWARE\DEVICEMAP\SERIALCOMM'
  $registryItems = @()
  if (Test-Path -LiteralPath $serialComm) {
    $item = Get-ItemProperty -LiteralPath $serialComm -ErrorAction Stop
    $registryItems = @($item.PSObject.Properties |
      Where-Object { $_.Name -notmatch '^PS' } |
      ForEach-Object { [pscustomobject]@{ Device=$_.Name; ComPort=[string]$_.Value } })
  }
  [pscustomobject]@{
    Source = 'registry:SERIALCOMM'
    Items = $registryItems
  }
}))

$probes.Add((Invoke-SafeProbe -Name 'pending_reboot_reconciliation' -Action {
  $cbs = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
  $wu = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
  $sessionManager = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager'

  $pendingRename = @()
  if (Test-Path -LiteralPath $sessionManager) {
    try {
      $pendingRename = @((Get-ItemProperty -LiteralPath $sessionManager -Name PendingFileRenameOperations -ErrorAction Stop).PendingFileRenameOperations)
    } catch { }
  }

  [pscustomobject]@{
    CbsRebootPending = (Test-Path -LiteralPath $cbs)
    WindowsUpdateRebootRequired = (Test-Path -LiteralPath $wu)
    PendingFileRenamePresent = ($pendingRename.Count -gt 0)
    PendingFileRenameCount = $pendingRename.Count
    PendingFileRenameOperations = $pendingRename
    DerivedRebootRequired = $null
    PolicyNote = 'Raw evidence only; no reboot classification is made by discovery.'
  }
}))

$probes.Add((Invoke-SafeProbe -Name 'reliability_event_fingerprints' -Action {
  $since = [DateTime]::Now.AddDays(-30)
  $events = foreach ($logName in @('Application','System')) {
    Get-WinEvent -FilterHashtable @{ LogName=$logName; Level=@(1,2); StartTime=$since } -MaxEvents 500 -ErrorAction Stop |
      Where-Object {
        $_.ProviderName -match '(?i)(Application Error|\.NET Runtime|Service Control Manager|Disk|Ntfs|storahci|WHEA|Kernel-Power|Time-Service)' -or
        $_.Message -match '(?i)(EagleManager|NINA|PHD2|ASCOM|CloudWatcher|DigitalStarGate)'
      } |
      Select-Object @{n='LogName';e={$logName}},TimeCreated,Id,LevelDisplayName,ProviderName,Message
  }

  $events | Group-Object LogName,ProviderName,Id | ForEach-Object {
    $latest = $_.Group | Sort-Object TimeCreated -Descending | Select-Object -First 1
    [pscustomobject]@{
      LogName = $latest.LogName
      ProviderName = $latest.ProviderName
      EventId = $latest.Id
      Count30Days = $_.Count
      LastObserved = $latest.TimeCreated
      ExampleContainsEagleManager = [bool]($latest.Message -match '(?i)EagleManager')
      ExampleContainsNina = [bool]($latest.Message -match '(?i)NINA')
      ExampleContainsPhd2 = [bool]($latest.Message -match '(?i)PHD2')
      ExampleContainsAscom = [bool]($latest.Message -match '(?i)ASCOM')
      ExampleContainsCloudWatcher = [bool]($latest.Message -match '(?i)CloudWatcher')
    }
  } | Sort-Object Count30Days -Descending
}))

$probes.Add((Invoke-SafeProbe -Name 'storage_capacity_raw' -Action {
  Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ForEach-Object {
    $size = [double]$_.Size
    $free = [double]$_.FreeSpace
    [pscustomobject]@{
      DeviceID = $_.DeviceID
      VolumeName = $_.VolumeName
      FileSystem = $_.FileSystem
      SizeBytes = [int64]$_.Size
      FreeBytes = [int64]$_.FreeSpace
      FreeRatio = if ($size -gt 0) { [math]::Round($free / $size, 6) } else { $null }
      FreePercent = if ($size -gt 0) { [math]::Round(($free / $size) * 100.0, 3) } else { $null }
      Severity = $null
      PolicyNote = 'Descriptive evidence only; no threshold applied.'
    }
  }
}))

$payload = [ordered]@{
  schema_version = '1.0'
  component = 'DSG.EagleHealthGapReconciliation'
  mode = 'READ_ONLY_DISCOVERY'
  identity = $identity
  probes = @($probes)
  disposition = 'DISCOVERY_ONLY_NOT_BKL030_ACCEPTANCE'
}

$jsonPath = Join-Path $bundle 'eagle-health-gap-reconciliation.json'
$txtPath = Join-Path $bundle 'eagle-health-gap-reconciliation.txt'

$payload | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add('Digital StarGate EAGLE Health Gap Reconciliation')
$lines.Add(('Computer: {0}' -f $identity.computer))
$lines.Add(('User: {0}' -f $identity.user))
$lines.Add(('Elevated: {0}' -f $identity.elevated))
$lines.Add('')
foreach ($probe in $probes) {
  $lines.Add(('=== {0} ===' -f $probe.name))
  $lines.Add(('Status: {0}' -f $probe.status))
  $lines.Add(('Elapsed ms: {0}' -f $probe.elapsed_ms))
  if ($probe.error) { $lines.Add(('Error: {0}' -f $probe.error)) }
  foreach ($row in @($probe.data)) { $lines.Add(($row | Out-String -Width 240).TrimEnd()) }
  $lines.Add('')
}
$lines.Add('DISPOSITION: DISCOVERY_ONLY_NOT_BKL030_ACCEPTANCE')
$lines | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Host ''
Write-Host '=== GAP RECONCILIATION SUMMARY ==='
$probes | Select-Object name,status,elapsed_ms,error | Format-Table -AutoSize
Write-Host ('Evidence JSON: {0}' -f $jsonPath)
Write-Host ('Evidence TXT : {0}' -f $txtPath)
Write-Host 'EAGLE HEALTH GAP RECONCILIATION RESULT: PASS (evidence recorded; not BKL-030 acceptance)'
