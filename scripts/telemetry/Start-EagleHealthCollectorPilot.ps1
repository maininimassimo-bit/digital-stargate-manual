[CmdletBinding()]
param(
  [ValidateRange(30, 3600)]
  [int]$DurationSeconds = 300,

  [ValidateRange(5, 300)]
  [int]$FastSeconds = 30,

  [ValidateRange(30, 1800)]
  [int]$MediumSeconds = 120,

  [ValidateRange(60, 3600)]
  [int]$SlowSeconds = 600,

  [ValidateRange(15, 3600)]
  [int]$ProjectionFreshnessSeconds = 120,

  [string]$OutputPath = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\eagle-health.json",

  [string]$NinaProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\nina-observatory-status.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($MediumSeconds -lt $FastSeconds) { throw 'MediumSeconds must be >= FastSeconds.' }
if ($SlowSeconds -lt $MediumSeconds) { throw 'SlowSeconds must be >= MediumSeconds.' }

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
  New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

Write-Host 'Digital StarGate EAGLE Health Collector - NON-COMMISSIONED PILOT'
Write-Host ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Host ('Duration: {0}s; fast={1}s medium={2}s slow={3}s' -f $DurationSeconds,$FastSeconds,$MediumSeconds,$SlowSeconds)
Write-Host ('Projection: {0}' -f $OutputPath)
Write-Host 'Mode: read-only pilot; no task/service install; no remediation; no device commands; summary policy disabled'

function New-SignalEnvelope {
  param(
    [Parameter(Mandatory)][string]$State,
    [Parameter(Mandatory)][string]$Quality,
    [Parameter(Mandatory)][datetime]$ObservedAtUtc,
    [Parameter(Mandatory)][datetime]$FreshUntilUtc,
    [Parameter(Mandatory)][string]$Source,
    [object]$Data = $null,
    [string]$Reason = $null
  )

  [ordered]@{
    state = $State
    quality = $Quality
    observed_at_utc = $ObservedAtUtc.ToString('o')
    fresh_until_utc = $FreshUntilUtc.ToString('o')
    source = $Source
    reason = $Reason
    data = $Data
  }
}

function Invoke-SafeSignal {
  param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][int]$FreshnessSeconds,
    [Parameter(Mandatory)][scriptblock]$Action
  )

  $observed = [datetime]::UtcNow
  try {
    $data = & $Action
    New-SignalEnvelope -State 'OBSERVED' -Quality 'CURRENT' -ObservedAtUtc $observed -FreshUntilUtc $observed.AddSeconds($FreshnessSeconds) -Source $Source -Data $data
  } catch {
    New-SignalEnvelope -State 'UNAVAILABLE' -Quality 'UNKNOWN' -ObservedAtUtc $observed -FreshUntilUtc $observed -Source $Source -Data $null -Reason $_.Exception.Message
  }
}

function Get-FastSignals {
  $os = Get-CimInstance Win32_OperatingSystem
  $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
  $totalBytes = [int64]$os.TotalVisibleMemorySize * 1024
  $freeBytes = [int64]$os.FreePhysicalMemory * 1024
  $usedBytes = $totalBytes - $freeBytes

  $processes = @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -match '(?i)(NINA|PHD2|ASCOM|CloudWatcher|EagleManager|DigitalStarGate|DSG)'
  } | ForEach-Object {
    [ordered]@{
      name = $_.ProcessName
      pid = $_.Id
      running = $true
      started_at_utc = try { $_.StartTime.ToUniversalTime().ToString('o') } catch { $null }
      working_set_bytes = $_.WorkingSet64
      cpu_total_seconds = $_.CPU
      executable_path = try { $_.Path } catch { $null }
    }
  })

  $pluginData = [ordered]@{
    projection_path = $NinaProjection
    exists = (Test-Path -LiteralPath $NinaProjection -PathType Leaf)
    observed_at_utc = $null
    fresh_until_utc = $null
    quality = 'UNKNOWN'
    plugin_version = $null
  }
  if ($pluginData.exists) {
    try {
      $nina = Get-Content -LiteralPath $NinaProjection -Raw | ConvertFrom-Json
      $pluginData.observed_at_utc = [string]$nina.observedAtUtc
      $pluginData.fresh_until_utc = if ($nina.services.sqm -and $nina.services.sqm.details) { [string]$nina.services.sqm.details.freshUntilUtc } else { $null }
      if ($pluginData.observed_at_utc) {
        $age = ([datetime]::UtcNow - ([datetime]$pluginData.observed_at_utc).ToUniversalTime()).TotalSeconds
        $pluginData.quality = if ($age -le $ProjectionFreshnessSeconds) { 'CURRENT' } else { 'STALE' }
      }
    } catch {
      $pluginData.quality = 'UNKNOWN'
    }
  }

  [ordered]@{
    cpu = [ordered]@{
      model = $cpu.Name
      physical_cores = $cpu.NumberOfCores
      logical_processors = $cpu.NumberOfLogicalProcessors
      max_clock_mhz = $cpu.MaxClockSpeed
      load_pct = $cpu.LoadPercentage
      window_avg_pct = $null
      window_peak_pct = $null
      temperature_c = $null
    }
    memory = [ordered]@{
      total_physical_bytes = $totalBytes
      available_physical_bytes = $freeBytes
      used_physical_bytes = $usedBytes
      available_ratio = if ($totalBytes -gt 0) { [math]::Round($freeBytes / [double]$totalBytes,6) } else { $null }
      memory_pressure = $null
    }
    uptime = [ordered]@{
      last_boot_at_utc = $os.LastBootUpTime.ToUniversalTime().ToString('o')
      uptime_seconds = [math]::Round(([datetime]::UtcNow - $os.LastBootUpTime.ToUniversalTime()).TotalSeconds,0)
      unexpected_reboot_observed = $null
    }
    processes = [ordered]@{ items = $processes }
    plugin_heartbeat = $pluginData
  }
}

function Get-MediumSignals {
  $disks = @(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ForEach-Object {
    [ordered]@{
      device_id = $_.DeviceID
      volume_name = $_.VolumeName
      filesystem = $_.FileSystem
      size_bytes = [int64]$_.Size
      free_bytes = [int64]$_.FreeSpace
      free_ratio = if ([double]$_.Size -gt 0) { [math]::Round(([double]$_.FreeSpace / [double]$_.Size),6) } else { $null }
    }
  })

  $tasks = @(Get-ScheduledTask | Where-Object {
    $_.TaskName -match '(?i)(Digital StarGate|DSG)' -or $_.TaskPath -match '(?i)(DigitalStarGate|DSG)'
  } | ForEach-Object {
    $info = $_ | Get-ScheduledTaskInfo
    [ordered]@{
      task_name = $_.TaskName
      task_path = $_.TaskPath
      state = [string]$_.State
      last_run_at_utc = if ($info.LastRunTime -and $info.LastRunTime.Year -gt 1900) { $info.LastRunTime.ToUniversalTime().ToString('o') } else { $null }
      last_task_result = $info.LastTaskResult
      next_run_at_utc = if ($info.NextRunTime -and $info.NextRunTime.Year -gt 1900) { $info.NextRunTime.ToUniversalTime().ToString('o') } else { $null }
      result_classification = $null
    }
  })

  $logCandidates = @(
    'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    'C:\DigitalStarGate\TelemetryRuntime\producer.log',
    $NinaProjection
  )
  $logs = @(foreach ($path in $logCandidates) {
    $item = Get-Item -LiteralPath $path -ErrorAction SilentlyContinue
    [ordered]@{
      path = $path
      exists = ($null -ne $item)
      length_bytes = if ($item) { $item.Length } else { $null }
      last_write_at_utc = if ($item) { $item.LastWriteTimeUtc.ToString('o') } else { $null }
    }
  })

  [ordered]@{
    storage = [ordered]@{
      logical_disks = $disks
      physical_disks = @()
      reliability = [ordered]@{
        available = $false
        temperature_c = $null
        temperature_max_c = $null
        wear_pct = $null
        read_errors_total = $null
        write_errors_total = $null
        power_on_hours = $null
        reason = 'UNAVAILABLE_NON_ELEVATED'
      }
    }
    scheduled_tasks = [ordered]@{ items = $tasks }
    log_sources = [ordered]@{ items = $logs }
  }
}

function Get-SlowSignals {
  $since = [datetime]::Now.AddDays(-7)
  $events = @(foreach ($logName in @('Application','System')) {
    Get-WinEvent -FilterHashtable @{ LogName=$logName; Level=@(1,2); StartTime=$since } -MaxEvents 100 -ErrorAction SilentlyContinue |
      Where-Object {
        $_.ProviderName -match '(?i)(Application Error|\.NET Runtime|Service Control Manager|Disk|Ntfs|storahci|WHEA|Kernel-Power|Time-Service)' -or
        $_.Message -match '(?i)(EagleManager|NINA|PHD2|ASCOM|CloudWatcher|DigitalStarGate)'
      } | ForEach-Object {
        [ordered]@{
          log_name = $logName
          time_created_utc = $_.TimeCreated.ToUniversalTime().ToString('o')
          event_id = $_.Id
          level = $_.LevelDisplayName
          provider = $_.ProviderName
          eagle_manager = [bool]($_.Message -match '(?i)EagleManager')
          nina = [bool]($_.Message -match '(?i)NINA')
          phd2 = [bool]($_.Message -match '(?i)PHD2')
          ascom = [bool]($_.Message -match '(?i)ASCOM')
          cloudwatcher = [bool]($_.Message -match '(?i)CloudWatcher')
        }
      }
  })

  $ports = @(Get-CimInstance Win32_PnPEntity -ErrorAction Stop | Where-Object {
    $_.PNPClass -eq 'Ports' -or $_.Name -match '(?i)\(COM\d+\)'
  } | ForEach-Object {
    [ordered]@{ name=$_.Name; status=$_.Status; manufacturer=$_.Manufacturer; device_id=$_.DeviceID }
  })

  $serialCommPath = 'HKLM:\HARDWARE\DEVICEMAP\SERIALCOMM'
  $mappings = @()
  if (Test-Path -LiteralPath $serialCommPath) {
    $item = Get-ItemProperty -LiteralPath $serialCommPath
    $mappings = @($item.PSObject.Properties | Where-Object { $_.Name -notmatch '^PS' } | ForEach-Object {
      [ordered]@{ device=$_.Name; com_port=[string]$_.Value }
    })
  }

  $cbs = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
  $wu = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
  $rename = @()
  try {
    $rename = @((Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name PendingFileRenameOperations -ErrorAction Stop).PendingFileRenameOperations)
  } catch { }

  $w32 = Get-CimInstance Win32_Service -Filter "Name='W32Time'" -ErrorAction SilentlyContinue
  $timeEvents = @(Get-WinEvent -FilterHashtable @{ LogName='System'; ProviderName='Microsoft-Windows-Time-Service'; StartTime=[datetime]::Now.AddDays(-30) } -MaxEvents 20 -ErrorAction SilentlyContinue |
    Where-Object { $_.Id -in @(35,37) } |
    Sort-Object TimeCreated -Descending)
  $lastSync = $timeEvents | Select-Object -First 1

  [ordered]@{
    event_log = [ordered]@{
      window_start_utc = $since.ToUniversalTime().ToString('o')
      window_end_utc = [datetime]::UtcNow.ToString('o')
      events = $events
    }
    usb_com = [ordered]@{
      usb_devices = $ports
      serial_mappings = $mappings
      source_reconciliation = 'PNP_AND_SERIALCOMM'
    }
    pending_reboot = [ordered]@{
      cbs_reboot_pending = $cbs
      windows_update_reboot_required = $wu
      pending_file_rename_present = ($rename.Count -gt 0)
      pending_file_rename_count = $rename.Count
      reboot_required = if ($cbs -or $wu) { $true } else { $false }
    }
    time_sync = [ordered]@{
      service_state = if ($w32) { [string]$w32.State } else { 'UNKNOWN' }
      start_mode = if ($w32) { [string]$w32.StartMode } else { $null }
      last_successful_sync_utc = if ($lastSync) { $lastSync.TimeCreated.ToUniversalTime().ToString('o') } else { $null }
      offset_ms = $null
      command_available = (Test-Path (Join-Path $env:SystemRoot 'System32\w32tm.exe'))
    }
    configuration_drift = [ordered]@{
      baseline_id = $null
      baseline_version = $null
      observed_items = @()
      drift_items = @()
      status = 'UNKNOWN'
    }
  }
}

$cache = [ordered]@{ fast=$null; medium=$null; slow=$null }
$last = [ordered]@{ fast=[datetime]::MinValue; medium=[datetime]::MinValue; slow=[datetime]::MinValue }
$startedAt = [datetime]::UtcNow
$deadline = $startedAt.AddSeconds($DurationSeconds)
$cycle = 0

while ([datetime]::UtcNow -lt $deadline) {
  $cycle++
  $cycleStarted = [datetime]::UtcNow

  if (($cycleStarted - $last.fast).TotalSeconds -ge $FastSeconds) {
    $cache.fast = Invoke-SafeSignal -Source 'Windows host fast sources' -FreshnessSeconds ($FastSeconds * 3) -Action { Get-FastSignals }
    $last.fast = $cycleStarted
  }
  if (($cycleStarted - $last.medium).TotalSeconds -ge $MediumSeconds) {
    $cache.medium = Invoke-SafeSignal -Source 'Windows host medium sources' -FreshnessSeconds ($MediumSeconds * 3) -Action { Get-MediumSignals }
    $last.medium = $cycleStarted
  }
  if (($cycleStarted - $last.slow).TotalSeconds -ge $SlowSeconds) {
    $cache.slow = Invoke-SafeSignal -Source 'Windows host slow sources' -FreshnessSeconds ($SlowSeconds * 3) -Action { Get-SlowSignals }
    $last.slow = $cycleStarted
  }

  $observed = [datetime]::UtcNow
  $signals = [ordered]@{}
  foreach ($groupName in @('fast','medium','slow')) {
    $group = $cache[$groupName]
    if (-not $group) { continue }
    if ($group.data) {
      foreach ($property in $group.data.GetEnumerator()) {
        $signals[$property.Key] = [ordered]@{
          state = $group.state
          quality = $group.quality
          observed_at_utc = $group.observed_at_utc
          fresh_until_utc = $group.fresh_until_utc
          source = $group.source
          reason = $group.reason
          data = $property.Value
        }
      }
    }
  }

  $payload = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.EagleHostHealthCollector'
    computer = $env:COMPUTERNAME
    observed_at_utc = $observed.ToString('o')
    fresh_until_utc = $observed.AddSeconds($ProjectionFreshnessSeconds).ToString('o')
    quality = 'CURRENT'
    correlation_id = [guid]::NewGuid().ToString('D')
    summary = [ordered]@{
      state = 'UNKNOWN'
      reasons = @([ordered]@{ code='POLICY_NOT_ACTIVATED'; signal=$null; severity=$null; evidence=$null })
    }
    signals = $signals
    diagnostics = [ordered]@{
      mode = 'NON_COMMISSIONED_PILOT'
      cycle = $cycle
      cadence_seconds = [ordered]@{ fast=$FastSeconds; medium=$MediumSeconds; slow=$SlowSeconds }
      policy_enabled = $false
      safety_authority = 'OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS'
    }
  }

  $tempPath = "$OutputPath.tmp"
  $payload | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $tempPath -Encoding UTF8
  Move-Item -LiteralPath $tempPath -Destination $OutputPath -Force

  Write-Host ('Cycle {0}: signals={1} fast={2} medium={3} slow={4} summary=UNKNOWN' -f $cycle,$signals.Count,$last.fast.ToString('HH:mm:ss'),$last.medium.ToString('HH:mm:ss'),$last.slow.ToString('HH:mm:ss'))

  $sleepSeconds = $FastSeconds - ([datetime]::UtcNow - $cycleStarted).TotalSeconds
  if ($sleepSeconds -gt 0 -and [datetime]::UtcNow.AddSeconds($sleepSeconds) -lt $deadline) {
    Start-Sleep -Milliseconds ([int][math]::Round($sleepSeconds * 1000.0))
  } else {
    break
  }
}

Write-Host ('EAGLE HEALTH COLLECTOR PILOT RESULT: STOPPED normally; projection={0}; not BKL-030 acceptance' -f $OutputPath)
