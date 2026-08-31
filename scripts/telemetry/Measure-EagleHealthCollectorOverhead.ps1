[CmdletBinding()]
param(
  [ValidateRange(30, 1800)]
  [int]$DurationSeconds = 180,

  [ValidateRange(5, 300)]
  [int]$PollSeconds = 15,

  [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("eagle-health-overhead-pilot-{0}" -f $stamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

$samplePath = Join-Path $bundle 'eagle-health-overhead-samples.ndjson'
$summaryPath = Join-Path $bundle 'eagle-health-overhead-summary.json'
$txtPath = Join-Path $bundle 'eagle-health-overhead-summary.txt'

Write-Host 'Digital StarGate EAGLE Health D3 overhead pilot - READ ONLY'
Write-Host ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Host ('Duration seconds: {0}' -f $DurationSeconds)
Write-Host ('Poll seconds: {0}' -f $PollSeconds)
Write-Host ('Evidence bundle: {0}' -f $bundle)
Write-Host 'Mode: temporary pilot only; no producer install; no task/service changes; no device commands'

function Get-HostSnapshot {
  $os = Get-CimInstance Win32_OperatingSystem
  $cpu = Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average

  $totalKb = [double]$os.TotalVisibleMemorySize
  $freeKb = [double]$os.FreePhysicalMemory
  $usedKb = $totalKb - $freeKb

  [pscustomobject]@{
    cpu_load_pct = if ($null -ne $cpu.Average) { [math]::Round([double]$cpu.Average, 2) } else { $null }
    memory_used_bytes = [int64]($usedKb * 1024.0)
    memory_free_bytes = [int64]($freeKb * 1024.0)
    memory_used_ratio = if ($totalKb -gt 0) { [math]::Round($usedKb / $totalKb, 6) } else { $null }
  }
}

function Invoke-ProbeSet {
  $started = [DateTime]::UtcNow
  $errors = [System.Collections.Generic.List[string]]::new()

  try {
    $null = Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' |
      Select-Object DeviceID,Size,FreeSpace
  } catch { $errors.Add(('logical_disks: {0}' -f $_.Exception.Message)) }

  try {
    $null = Get-CimInstance Win32_OperatingSystem |
      Select-Object LastBootUpTime,TotalVisibleMemorySize,FreePhysicalMemory
  } catch { $errors.Add(('operating_system: {0}' -f $_.Exception.Message)) }

  try {
    $null = Get-CimInstance Win32_Processor |
      Select-Object LoadPercentage
  } catch { $errors.Add(('processor: {0}' -f $_.Exception.Message)) }

  try {
    $null = Get-Process -ErrorAction SilentlyContinue | Where-Object {
      $_.ProcessName -match '(?i)(NINA|PHD2|ASCOM|CloudWatcher|DigitalStarGate|DSG|EagleManager)'
    } | Select-Object ProcessName,Id,WorkingSet64,CPU
  } catch { $errors.Add(('processes: {0}' -f $_.Exception.Message)) }

  try {
    $null = Get-ScheduledTask | Where-Object {
      $_.TaskName -match '(?i)(Digital StarGate|DSG)' -or $_.TaskPath -match '(?i)(DigitalStarGate|DSG)'
    } | ForEach-Object { $_ | Get-ScheduledTaskInfo }
  } catch { $errors.Add(('scheduled_tasks: {0}' -f $_.Exception.Message)) }

  try {
    $since = [DateTime]::Now.AddMinutes(-10)
    $null = Get-WinEvent -FilterHashtable @{ LogName='Application'; Level=@(1,2); StartTime=$since } -MaxEvents 50 -ErrorAction SilentlyContinue
  } catch { $errors.Add(('event_log: {0}' -f $_.Exception.Message)) }

  try {
    $null = Get-CimInstance Win32_PnPEntity -ErrorAction Stop | Where-Object {
      $_.PNPClass -eq 'Ports' -or $_.Name -match '(?i)\(COM\d+\)'
    } | Select-Object Name,Status,Manufacturer,DeviceID
  } catch { $errors.Add(('serial_inventory: {0}' -f $_.Exception.Message)) }

  try {
    $null = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
    $null = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
  } catch { $errors.Add(('pending_reboot: {0}' -f $_.Exception.Message)) }

  [pscustomobject]@{
    elapsed_ms = [math]::Round(([DateTime]::UtcNow - $started).TotalMilliseconds, 1)
    error_count = $errors.Count
    errors = @($errors)
  }
}

$pilotProcess = Get-Process -Id $PID
$startCpuSeconds = [double]$pilotProcess.CPU
$startWorkingSet = [int64]$pilotProcess.WorkingSet64
$startedAtUtc = [DateTime]::UtcNow
$deadline = $startedAtUtc.AddSeconds($DurationSeconds)
$nextSampleAtUtc = $startedAtUtc

$samples = [System.Collections.Generic.List[object]]::new()
$iteration = 0

while ($nextSampleAtUtc -lt $deadline) {
  $now = [DateTime]::UtcNow
  if ($now -lt $nextSampleAtUtc) {
    $waitMs = [int][math]::Round(($nextSampleAtUtc - $now).TotalMilliseconds)
    if ($waitMs -gt 0) { Start-Sleep -Milliseconds $waitMs }
  }

  if ([DateTime]::UtcNow -ge $deadline) { break }

  $iteration++
  $scheduledAtUtc = $nextSampleAtUtc
  $sampleStarted = [DateTime]::UtcNow
  $hostBefore = Get-HostSnapshot

  $procBefore = Get-Process -Id $PID
  $cpuBefore = [double]$procBefore.CPU
  $wsBefore = [int64]$procBefore.WorkingSet64

  $probe = Invoke-ProbeSet

  $procAfter = Get-Process -Id $PID
  $hostAfter = Get-HostSnapshot
  $cpuDelta = [math]::Round(([double]$procAfter.CPU - $cpuBefore), 6)

  $sample = [ordered]@{
    schema_version = '1.0'
    iteration = $iteration
    scheduled_at_utc = $scheduledAtUtc.ToString('o')
    observed_at_utc = [DateTime]::UtcNow.ToString('o')
    schedule_lag_ms = [math]::Round(($sampleStarted - $scheduledAtUtc).TotalMilliseconds, 1)
    wall_elapsed_ms = [math]::Round(([DateTime]::UtcNow - $sampleStarted).TotalMilliseconds, 1)
    probe_elapsed_ms = $probe.elapsed_ms
    probe_error_count = $probe.error_count
    probe_errors = @($probe.errors)
    collector_cpu_seconds_delta = $cpuDelta
    collector_working_set_before_bytes = $wsBefore
    collector_working_set_after_bytes = [int64]$procAfter.WorkingSet64
    collector_working_set_delta_bytes = [int64]$procAfter.WorkingSet64 - $wsBefore
    host_cpu_load_before_pct = $hostBefore.cpu_load_pct
    host_cpu_load_after_pct = $hostAfter.cpu_load_pct
    host_memory_used_ratio_before = $hostBefore.memory_used_ratio
    host_memory_used_ratio_after = $hostAfter.memory_used_ratio
    nina_running = [bool](Get-Process NINA -ErrorAction SilentlyContinue)
  }

  $obj = [pscustomobject]$sample
  $samples.Add($obj)
  ($obj | ConvertTo-Json -Depth 8 -Compress) | Add-Content -LiteralPath $samplePath -Encoding UTF8

  Write-Host ('Sample {0}: probe={1}ms cpu_delta={2}s ws={3}MB host_cpu={4}% lag={5}ms errors={6}' -f `
    $iteration,
    $probe.elapsed_ms,
    $cpuDelta,
    [math]::Round(([double]$procAfter.WorkingSet64 / 1MB), 1),
    $hostAfter.cpu_load_pct,
    $sample.schedule_lag_ms,
    $probe.error_count)

  $nextSampleAtUtc = $nextSampleAtUtc.AddSeconds($PollSeconds)
}

$remainingToDeadlineMs = [int][math]::Round(($deadline - [DateTime]::UtcNow).TotalMilliseconds)
if ($remainingToDeadlineMs -gt 0) {
  Start-Sleep -Milliseconds $remainingToDeadlineMs
}

$endedAtUtc = [DateTime]::UtcNow
$pilotProcess = Get-Process -Id $PID
$totalCpuSeconds = [math]::Round(([double]$pilotProcess.CPU - $startCpuSeconds), 6)
$totalWallSeconds = [math]::Round(($endedAtUtc - $startedAtUtc).TotalSeconds, 3)

$probeTimes = @($samples | ForEach-Object { [double]$_.probe_elapsed_ms })
$wallTimes = @($samples | ForEach-Object { [double]$_.wall_elapsed_ms })
$cpuDeltas = @($samples | ForEach-Object { [double]$_.collector_cpu_seconds_delta })
$wsAfter = @($samples | ForEach-Object { [double]$_.collector_working_set_after_bytes })
$hostCpu = @($samples | ForEach-Object { if ($null -ne $_.host_cpu_load_after_pct) { [double]$_.host_cpu_load_after_pct } })
$scheduleLag = @($samples | ForEach-Object { [double]$_.schedule_lag_ms })

function Get-Average([double[]]$Values) {
  if ($null -eq $Values -or $Values.Count -eq 0) { return $null }
  return [math]::Round((($Values | Measure-Object -Average).Average), 3)
}

function Get-Maximum([double[]]$Values) {
  if ($null -eq $Values -or $Values.Count -eq 0) { return $null }
  return [math]::Round((($Values | Measure-Object -Maximum).Maximum), 3)
}

$summary = [pscustomobject][ordered]@{
  schema_version = '1.1'
  component = 'DSG.EagleHealthOverheadPilot'
  computer = $env:COMPUTERNAME
  started_at_utc = $startedAtUtc.ToString('o')
  ended_at_utc = $endedAtUtc.ToString('o')
  requested_duration_seconds = $DurationSeconds
  actual_duration_seconds = $totalWallSeconds
  poll_seconds = $PollSeconds
  expected_sample_count = [int][math]::Ceiling($DurationSeconds / [double]$PollSeconds)
  sample_count = $samples.Count
  total_collector_cpu_seconds = $totalCpuSeconds
  collector_cpu_pct_of_one_logical_cpu = if ($totalWallSeconds -gt 0) { [math]::Round(($totalCpuSeconds / $totalWallSeconds) * 100.0, 4) } else { $null }
  collector_working_set_start_bytes = $startWorkingSet
  collector_working_set_end_bytes = [int64]$pilotProcess.WorkingSet64
  collector_working_set_avg_bytes = if ($wsAfter.Count -gt 0) { [int64](($wsAfter | Measure-Object -Average).Average) } else { $null }
  collector_working_set_max_bytes = if ($wsAfter.Count -gt 0) { [int64](($wsAfter | Measure-Object -Maximum).Maximum) } else { $null }
  probe_elapsed_ms_avg = Get-Average $probeTimes
  probe_elapsed_ms_max = Get-Maximum $probeTimes
  wall_elapsed_ms_avg = Get-Average $wallTimes
  wall_elapsed_ms_max = Get-Maximum $wallTimes
  schedule_lag_ms_avg = Get-Average $scheduleLag
  schedule_lag_ms_max = Get-Maximum $scheduleLag
  sample_cpu_seconds_delta_avg = Get-Average $cpuDeltas
  sample_cpu_seconds_delta_max = Get-Maximum $cpuDeltas
  host_cpu_load_after_pct_avg = Get-Average $hostCpu
  host_cpu_load_after_pct_max = Get-Maximum $hostCpu
  probe_error_count_total = [int](($samples | Measure-Object -Property probe_error_count -Sum).Sum)
  nina_observed_running = [bool](@($samples | Where-Object { $_.nina_running }).Count -gt 0)
  disposition = 'D3_OVERHEAD_PILOT_ONLY_NOT_BKL030_ACCEPTANCE'
}

$summary | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $summaryPath -Encoding UTF8

$lines = @(
  'Digital StarGate EAGLE Health D3 Overhead Pilot',
  ('Computer: {0}' -f $summary.computer),
  ('Samples: {0}/{1}' -f $summary.sample_count,$summary.expected_sample_count),
  ('Actual duration seconds: {0}' -f $summary.actual_duration_seconds),
  ('Total collector CPU seconds: {0}' -f $summary.total_collector_cpu_seconds),
  ('Collector CPU pct of one logical CPU: {0}' -f $summary.collector_cpu_pct_of_one_logical_cpu),
  ('Collector WS avg MB: {0}' -f [math]::Round(([double]$summary.collector_working_set_avg_bytes / 1MB), 2)),
  ('Collector WS max MB: {0}' -f [math]::Round(([double]$summary.collector_working_set_max_bytes / 1MB), 2)),
  ('Probe avg ms: {0}' -f $summary.probe_elapsed_ms_avg),
  ('Probe max ms: {0}' -f $summary.probe_elapsed_ms_max),
  ('Schedule lag avg ms: {0}' -f $summary.schedule_lag_ms_avg),
  ('Schedule lag max ms: {0}' -f $summary.schedule_lag_ms_max),
  ('Host CPU avg pct after probe: {0}' -f $summary.host_cpu_load_after_pct_avg),
  ('Host CPU max pct after probe: {0}' -f $summary.host_cpu_load_after_pct_max),
  ('Probe errors total: {0}' -f $summary.probe_error_count_total),
  ('NINA observed running: {0}' -f $summary.nina_observed_running),
  'DISPOSITION: D3_OVERHEAD_PILOT_ONLY_NOT_BKL030_ACCEPTANCE'
)
$lines | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Host ''
Write-Host '=== D3 OVERHEAD SUMMARY ==='
$summary | Select-Object sample_count,expected_sample_count,actual_duration_seconds,total_collector_cpu_seconds,collector_cpu_pct_of_one_logical_cpu,collector_working_set_avg_bytes,collector_working_set_max_bytes,probe_elapsed_ms_avg,probe_elapsed_ms_max,schedule_lag_ms_avg,schedule_lag_ms_max,host_cpu_load_after_pct_avg,host_cpu_load_after_pct_max,probe_error_count_total,nina_observed_running | Format-List
Write-Host ('Samples NDJSON: {0}' -f $samplePath)
Write-Host ('Summary JSON : {0}' -f $summaryPath)
Write-Host ('Summary TXT  : {0}' -f $txtPath)
Write-Host 'EAGLE HEALTH D3 OVERHEAD PILOT RESULT: PASS (measurements recorded; not BKL-030 acceptance)'
