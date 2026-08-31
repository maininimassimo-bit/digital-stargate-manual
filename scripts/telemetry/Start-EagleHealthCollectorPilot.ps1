[CmdletBinding()]
param(
  [ValidateRange(30,3600)][int]$DurationSeconds = 300,
  [ValidateRange(5,300)][int]$FastSeconds = 30,
  [ValidateRange(30,1800)][int]$MediumSeconds = 120,
  [ValidateRange(60,3600)][int]$SlowSeconds = 600,
  [ValidateRange(15,3600)][int]$ProjectionFreshnessSeconds = 120,
  [string]$OutputPath = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\eagle-health-pilot.json",
  [string]$NinaProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\nina-observatory-status.json"
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($MediumSeconds -lt $FastSeconds) { throw 'MediumSeconds must be >= FastSeconds.' }
if ($SlowSeconds -lt $MediumSeconds) { throw 'SlowSeconds must be >= MediumSeconds.' }
$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
Write-Host 'Digital StarGate EAGLE Health Collector - NON-COMMISSIONED PILOT'
Write-Host ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Host ('Duration: {0}s; fast={1}s medium={2}s slow={3}s' -f $DurationSeconds,$FastSeconds,$MediumSeconds,$SlowSeconds)
Write-Host ('Projection: {0}' -f $OutputPath)
Write-Host 'Mode: read-only pilot; no task/service install; no remediation; no device commands; summary policy disabled'

function New-SignalEnvelope {
  param([string]$State,[string]$Quality,[datetime]$ObservedAtUtc,[datetime]$FreshUntilUtc,[string]$Source,[object]$Data=$null,[string]$Reason=$null)
  [ordered]@{ state=$State; quality=$Quality; observed_at_utc=$ObservedAtUtc.ToString('o'); fresh_until_utc=$FreshUntilUtc.ToString('o'); source=$Source; reason=$Reason; data=$Data }
}
function Invoke-SafeSignal {
  param([string]$Source,[int]$FreshnessSeconds,[scriptblock]$Action)
  $observed=[datetime]::UtcNow
  try { $data=& $Action; New-SignalEnvelope 'OBSERVED' 'CURRENT' $observed $observed.AddSeconds($FreshnessSeconds) $Source $data }
  catch { New-SignalEnvelope 'UNAVAILABLE' 'UNKNOWN' $observed $observed $Source $null $_.Exception.Message }
}
function Get-ProcessStartUtc { param([System.Diagnostics.Process]$Process) try { $Process.StartTime.ToUniversalTime().ToString('o') } catch { $null } }
function Get-ProcessExecutablePath { param([System.Diagnostics.Process]$Process) try { $Process.Path } catch { $null } }

function Get-FastSignals {
  $os=Get-CimInstance Win32_OperatingSystem
  $cpu=Get-CimInstance Win32_Processor | Select-Object -First 1
  $total=[int64]$os.TotalVisibleMemorySize*1024; $free=[int64]$os.FreePhysicalMemory*1024
  $processes=@(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match '(?i)(NINA|PHD2|ASCOM|CloudWatcher|EagleManager|DigitalStarGate|DSG)' } | ForEach-Object {
    $p=$_; [ordered]@{ name=$p.ProcessName; pid=$p.Id; running=$true; started_at_utc=(Get-ProcessStartUtc $p); working_set_bytes=$p.WorkingSet64; cpu_total_seconds=$p.CPU; executable_path=(Get-ProcessExecutablePath $p) }
  })
  $plugin=[ordered]@{ projection_path=$NinaProjection; exists=(Test-Path -LiteralPath $NinaProjection -PathType Leaf); observed_at_utc=$null; fresh_until_utc=$null; quality='UNKNOWN'; plugin_version=$null }
  if ($plugin.exists) {
    try {
      $n=Get-Content -LiteralPath $NinaProjection -Raw | ConvertFrom-Json
      $plugin.observed_at_utc=[string]$n.observedAtUtc
      if ($n.services -and ($n.services.PSObject.Properties.Name -contains 'sqm') -and $n.services.sqm -and $n.services.sqm.details) { $plugin.fresh_until_utc=[string]$n.services.sqm.details.freshUntilUtc }
      if ($plugin.observed_at_utc) {
        $t=[datetime]::Parse([string]$plugin.observed_at_utc,[Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
        $plugin.quality=if (([datetime]::UtcNow-$t).TotalSeconds -le $ProjectionFreshnessSeconds) {'CURRENT'} else {'STALE'}
      }
    } catch { $plugin.quality='UNKNOWN' }
  }
  [ordered]@{
    cpu=[ordered]@{ model=$cpu.Name; physical_cores=$cpu.NumberOfCores; logical_processors=$cpu.NumberOfLogicalProcessors; max_clock_mhz=$cpu.MaxClockSpeed; load_pct=$cpu.LoadPercentage; window_avg_pct=$null; window_peak_pct=$null; temperature_c=$null }
    memory=[ordered]@{ total_physical_bytes=$total; available_physical_bytes=$free; used_physical_bytes=($total-$free); available_ratio=if($total -gt 0){[math]::Round($free/[double]$total,6)}else{$null}; memory_pressure=$null }
    uptime=[ordered]@{ last_boot_at_utc=$os.LastBootUpTime.ToUniversalTime().ToString('o'); uptime_seconds=[math]::Round(([datetime]::UtcNow-$os.LastBootUpTime.ToUniversalTime()).TotalSeconds,0); unexpected_reboot_observed=$null }
    processes=[ordered]@{items=$processes}; plugin_heartbeat=$plugin
  }
}
function Get-MediumSignals {
  $disks=@(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ForEach-Object { [ordered]@{device_id=$_.DeviceID;volume_name=$_.VolumeName;filesystem=$_.FileSystem;size_bytes=[int64]$_.Size;free_bytes=[int64]$_.FreeSpace;free_ratio=if([double]$_.Size -gt 0){[math]::Round([double]$_.FreeSpace/[double]$_.Size,6)}else{$null}} })
  $tasks=@(Get-ScheduledTask | Where-Object {$_.TaskName -match '(?i)(Digital StarGate|DSG)' -or $_.TaskPath -match '(?i)(DigitalStarGate|DSG)'} | ForEach-Object { $i=$_|Get-ScheduledTaskInfo; [ordered]@{task_name=$_.TaskName;task_path=$_.TaskPath;state=[string]$_.State;last_run_at_utc=if($i.LastRunTime -and $i.LastRunTime.Year -gt 1900){$i.LastRunTime.ToUniversalTime().ToString('o')}else{$null};last_task_result=$i.LastTaskResult;next_run_at_utc=if($i.NextRunTime -and $i.NextRunTime.Year -gt 1900){$i.NextRunTime.ToUniversalTime().ToString('o')}else{$null};result_classification=$null} })
  $logs=@(foreach($path in @('C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv','C:\DigitalStarGate\TelemetryRuntime\producer.log',$NinaProjection)){ $i=Get-Item -LiteralPath $path -ErrorAction SilentlyContinue; [ordered]@{path=$path;exists=($null-ne $i);length_bytes=if($i){$i.Length}else{$null};last_write_at_utc=if($i){$i.LastWriteTimeUtc.ToString('o')}else{$null}} })
  [ordered]@{storage=[ordered]@{logical_disks=$disks;physical_disks=@();reliability=[ordered]@{available=$false;temperature_c=$null;temperature_max_c=$null;wear_pct=$null;read_errors_total=$null;write_errors_total=$null;power_on_hours=$null;reason='UNAVAILABLE_NON_ELEVATED'}};scheduled_tasks=[ordered]@{items=$tasks};log_sources=[ordered]@{items=$logs}}
}
function Get-SlowSignals {
  $since=[datetime]::Now.AddDays(-7)
  $events=@(foreach($log in @('Application','System')){ Get-WinEvent -FilterHashtable @{LogName=$log;Level=@(1,2);StartTime=$since} -MaxEvents 100 -ErrorAction SilentlyContinue | Where-Object {$_.ProviderName -match '(?i)(Application Error|\.NET Runtime|Service Control Manager|Disk|Ntfs|storahci|WHEA|Kernel-Power|Time-Service)' -or $_.Message -match '(?i)(EagleManager|NINA|PHD2|ASCOM|CloudWatcher|DigitalStarGate)'} | ForEach-Object {[ordered]@{log_name=$log;time_created_utc=$_.TimeCreated.ToUniversalTime().ToString('o');event_id=$_.Id;level=$_.LevelDisplayName;provider=$_.ProviderName;eagle_manager=[bool]($_.Message-match'(?i)EagleManager');nina=[bool]($_.Message-match'(?i)NINA');phd2=[bool]($_.Message-match'(?i)PHD2');ascom=[bool]($_.Message-match'(?i)ASCOM');cloudwatcher=[bool]($_.Message-match'(?i)CloudWatcher')}} })
  $ports=@(Get-CimInstance Win32_PnPEntity | Where-Object {$_.PNPClass -eq 'Ports' -or $_.Name -match '(?i)\(COM\d+\)'} | ForEach-Object {[ordered]@{name=$_.Name;status=$_.Status;manufacturer=$_.Manufacturer;device_id=$_.DeviceID}})
  $map=@(); $reg='HKLM:\HARDWARE\DEVICEMAP\SERIALCOMM'; if(Test-Path $reg){$r=Get-ItemProperty $reg;$map=@($r.PSObject.Properties|Where-Object{$_.Name-notmatch'^PS'}|ForEach-Object{[ordered]@{device=$_.Name;com_port=[string]$_.Value}})}
  $cbs=Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'; $wu=Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'; $rename=@(); try{$rename=@((Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name PendingFileRenameOperations -ErrorAction Stop).PendingFileRenameOperations)}catch{}
  $w32=Get-CimInstance Win32_Service -Filter "Name='W32Time'" -ErrorAction SilentlyContinue
  $te=@(Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Time-Service';StartTime=[datetime]::Now.AddDays(-30)} -MaxEvents 20 -ErrorAction SilentlyContinue|Where-Object{$_.Id-in@(35,37)}|Sort-Object TimeCreated -Descending);$ls=$te|Select-Object -First 1
  [ordered]@{
    event_log=[ordered]@{window_start_utc=$since.ToUniversalTime().ToString('o');window_end_utc=[datetime]::UtcNow.ToString('o');events=$events}
    usb_com=[ordered]@{usb_devices=$ports;serial_mappings=$map;source_reconciliation='PNP_AND_SERIALCOMM'}
    pending_reboot=[ordered]@{cbs_reboot_pending=$cbs;windows_update_reboot_required=$wu;pending_file_rename_present=($rename.Count-gt 0);pending_file_rename_count=$rename.Count;reboot_required=$null;policy='RAW_EVIDENCE_ONLY'}
    time_sync=[ordered]@{service_state=if($w32){[string]$w32.State}else{'UNKNOWN'};start_mode=if($w32){[string]$w32.StartMode}else{$null};last_successful_sync_utc=if($ls){$ls.TimeCreated.ToUniversalTime().ToString('o')}else{$null};offset_ms=$null;command_available=(Test-Path (Join-Path $env:SystemRoot 'System32\w32tm.exe'))}
    configuration_drift=[ordered]@{baseline_id=$null;baseline_version=$null;observed_items=@();drift_items=@();status='UNKNOWN'}
  }
}
$cache=[ordered]@{fast=$null;medium=$null;slow=$null};$last=[ordered]@{fast=[datetime]::MinValue;medium=[datetime]::MinValue;slow=[datetime]::MinValue};$deadline=[datetime]::UtcNow.AddSeconds($DurationSeconds);$cycle=0
while([datetime]::UtcNow -lt $deadline){
  $cycle++;$start=[datetime]::UtcNow
  if(($start-$last.fast).TotalSeconds-ge$FastSeconds){$cache.fast=Invoke-SafeSignal 'Windows host fast sources' ($FastSeconds*3) {Get-FastSignals};$last.fast=$start}
  if(($start-$last.medium).TotalSeconds-ge$MediumSeconds){$cache.medium=Invoke-SafeSignal 'Windows host medium sources' ($MediumSeconds*3) {Get-MediumSignals};$last.medium=$start}
  if(($start-$last.slow).TotalSeconds-ge$SlowSeconds){$cache.slow=Invoke-SafeSignal 'Windows host slow sources' ($SlowSeconds*3) {Get-SlowSignals};$last.slow=$start}
  $now=[datetime]::UtcNow;$signals=[ordered]@{}
  foreach($g in @('fast','medium','slow')){$x=$cache[$g];if($x -and $x.data){foreach($p in $x.data.GetEnumerator()){$signals[$p.Key]=[ordered]@{state=$x.state;quality=$x.quality;observed_at_utc=$x.observed_at_utc;fresh_until_utc=$x.fresh_until_utc;source=$x.source;reason=$x.reason;data=$p.Value}}}}
  $payload=[ordered]@{schema_version='1.0';component='DSG.EagleHostHealthCollector';computer=$env:COMPUTERNAME;observed_at_utc=$now.ToString('o');fresh_until_utc=$now.AddSeconds($ProjectionFreshnessSeconds).ToString('o');quality='CURRENT';correlation_id=[guid]::NewGuid().ToString('D');summary=[ordered]@{state='UNKNOWN';reasons=@([ordered]@{code='POLICY_NOT_ACTIVATED';signal=$null;severity=$null;evidence=$null})};signals=$signals;diagnostics=[ordered]@{mode='NON_COMMISSIONED_PILOT';cycle=$cycle;cadence_seconds=[ordered]@{fast=$FastSeconds;medium=$MediumSeconds;slow=$SlowSeconds};policy_enabled=$false;safety_authority='OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS'}}
  $tmp="$OutputPath.tmp";$payload|ConvertTo-Json -Depth 14|Set-Content -LiteralPath $tmp -Encoding UTF8;Move-Item -LiteralPath $tmp -Destination $OutputPath -Force
  Write-Host ('Cycle {0}: signals={1} summary=UNKNOWN' -f $cycle,$signals.Count)
  $sleep=$FastSeconds-([datetime]::UtcNow-$start).TotalSeconds;if($sleep-gt 0 -and [datetime]::UtcNow.AddSeconds($sleep)-lt$deadline){Start-Sleep -Milliseconds ([int][math]::Round($sleep*1000))}else{break}
}
Write-Host ('EAGLE HEALTH COLLECTOR PILOT RESULT: STOPPED normally; projection={0}; not BKL-030 acceptance' -f $OutputPath)
