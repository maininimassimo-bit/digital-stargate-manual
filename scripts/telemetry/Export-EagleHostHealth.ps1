[CmdletBinding()]
param(
    [string]$OutputPath = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\eagle-health.json'),
    [ValidateSet('fast','medium','slow','all')]
    [string]$CadenceClass = 'all',
    [int]$FreshnessSeconds = 120
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Convert-ToUtcIso([datetime]$Value) { $Value.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ') }
function New-Envelope([string]$Source, [object]$Data, [string]$State = 'OBSERVED', [string]$Quality = 'CURRENT', [string]$Reason = $null) {
    $now = [datetime]::UtcNow
    [ordered]@{ state=$State; quality=$Quality; observed_at_utc=(Convert-ToUtcIso $now); fresh_until_utc=(Convert-ToUtcIso $now.AddSeconds($FreshnessSeconds)); source=$Source; reason=$Reason; data=$Data }
}
function Invoke-Probe([string]$Name, [string]$Source, [scriptblock]$Body) {
    try { New-Envelope $Source (& $Body) }
    catch { New-Envelope $Source $null 'UNAVAILABLE' 'UNKNOWN' (($_.Exception.Message -replace '[\r\n]+',' ') | Select-Object -First 1) }
}

$signals = [ordered]@{}

if ($CadenceClass -in @('fast','all')) {
    $signals.cpu = Invoke-Probe 'cpu' 'Win32_Processor' {
        $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
        [ordered]@{ model=$cpu.Name; physical_cores=[int]$cpu.NumberOfCores; logical_processors=[int]$cpu.NumberOfLogicalProcessors; max_clock_mhz=[int]$cpu.MaxClockSpeed; load_pct=if($null -eq $cpu.LoadPercentage){$null}else{[double]$cpu.LoadPercentage}; window_avg_pct=$null; window_peak_pct=$null; temperature_c=$null }
    }
    $signals.memory = Invoke-Probe 'memory' 'Win32_OperatingSystem' {
        $os = Get-CimInstance Win32_OperatingSystem
        $total = [int64]$os.TotalVisibleMemorySize * 1024
        $free = [int64]$os.FreePhysicalMemory * 1024
        [ordered]@{ total_physical_bytes=$total; available_physical_bytes=$free; available_ratio=if($total -gt 0){[math]::Round($free/[double]$total,6)}else{$null}; commit_used_bytes=$null; commit_limit_bytes=$null; memory_pressure=$null }
    }
    $signals.processes = Invoke-Probe 'processes' 'Windows process table' {
        $names = @('NINA','phd2','AAG_CloudWatcher','ASCOM.TS_Shelter')
        $items = foreach($n in $names){ $p = @(Get-Process -Name $n -ErrorAction SilentlyContinue); [ordered]@{ name=$n; running=($p.Count -gt 0); pid=if($p.Count){$p[0].Id}else{$null}; started_at_utc=$null; working_set_bytes=if($p.Count){[int64]$p[0].WorkingSet64}else{$null}; cpu_total_seconds=if($p.Count -and $null -ne $p[0].CPU){[double]$p[0].CPU}else{$null} } }
        [ordered]@{ items=@($items) }
    }
    $signals.plugin_heartbeat = Invoke-Probe 'plugin_heartbeat' 'NINA telemetry projection metadata' {
        $p = Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\nina-observatory-status.json'
        $f = Get-Item -LiteralPath $p -ErrorAction SilentlyContinue
        [ordered]@{ projection_path=$p; exists=($null -ne $f); last_write_at_utc=if($f){Convert-ToUtcIso $f.LastWriteTimeUtc}else{$null}; plugin_version=$null }
    }
}

if ($CadenceClass -in @('medium','all')) {
    $signals.storage = Invoke-Probe 'storage' 'Win32_LogicalDisk/Get-PhysicalDisk' {
        $logical = @(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ForEach-Object { $size=[int64]$_.Size; $free=[int64]$_.FreeSpace; [ordered]@{ device_id=$_.DeviceID; volume_name=$_.VolumeName; filesystem=$_.FileSystem; size_bytes=$size; free_bytes=$free; free_ratio=if($size -gt 0){[math]::Round($free/[double]$size,6)}else{$null}; free_pct=if($size -gt 0){[math]::Round(100*$free/[double]$size,3)}else{$null} } })
        $physical = @()
        if(Get-Command Get-PhysicalDisk -ErrorAction SilentlyContinue){ $physical=@(Get-PhysicalDisk | ForEach-Object { [ordered]@{ friendly_name=$_.FriendlyName; media_type=[string]$_.MediaType; bus_type=[string]$_.BusType; health_status=[string]$_.HealthStatus; operational_status=@($_.OperationalStatus | ForEach-Object {[string]$_}); size_bytes=[int64]$_.Size } }) }
        [ordered]@{ logical_disks=$logical; physical_disks=$physical; reliability=[ordered]@{ available=$false; temperature_c=$null; temperature_max_c=$null; wear_pct=$null; read_errors_total=$null; write_errors_total=$null; power_on_hours=$null; reason='UNAVAILABLE_UNLESS_SEPARATELY_VERIFIED' } }
    }
    $signals.uptime = Invoke-Probe 'uptime' 'Win32_OperatingSystem' { $os=Get-CimInstance Win32_OperatingSystem; $boot=[datetime]$os.LastBootUpTime; [ordered]@{ last_boot_at_utc=(Convert-ToUtcIso $boot); uptime_seconds=[int64]([datetime]::UtcNow-$boot.ToUniversalTime()).TotalSeconds; unexpected_reboot_observed=$null } }
    $signals.time_sync = Invoke-Probe 'time_sync' 'W32Time service state' { $s=Get-Service W32Time -ErrorAction SilentlyContinue; [ordered]@{ service_state=if($s){[string]$s.Status}else{'UNKNOWN'}; time_source=$null; stratum=$null; last_successful_sync_utc=$null; offset_ms=$null; command_available=($null -ne (Get-Command w32tm.exe -ErrorAction SilentlyContinue)) } }
    $signals.usb_com = Invoke-Probe 'usb_com' 'Win32_PnPEntity' { $ports=@(Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match '\(COM\d+\)' } | ForEach-Object { [ordered]@{ name=$_.Name; status=$_.Status; manufacturer=$_.Manufacturer; device_id=$_.PNPDeviceID } }); [ordered]@{ serial_ports=$ports; source_reconciliation='PNP_PRIMARY' } }
    $signals.log_sources = Invoke-Probe 'log_sources' 'filesystem metadata' { $items=@(); [ordered]@{ items=$items } }
}

if ($CadenceClass -in @('slow','all')) {
    $signals.scheduled_tasks = Invoke-Probe 'scheduled_tasks' 'Task Scheduler read API' { $items=@(); if(Get-Command Get-ScheduledTask -ErrorAction SilentlyContinue){ foreach($t in @(Get-ScheduledTask | Where-Object {$_.TaskName -like 'Digital StarGate*'})){ $i=$t | Get-ScheduledTaskInfo; $items += [ordered]@{ task_name=$t.TaskName; task_path=$t.TaskPath; state=[string]$t.State; last_run_at_utc=if($i.LastRunTime.Year -gt 1900){Convert-ToUtcIso $i.LastRunTime}else{$null}; last_task_result=[int64]$i.LastTaskResult; next_run_at_utc=if($i.NextRunTime.Year -gt 1900){Convert-ToUtcIso $i.NextRunTime}else{$null}; result_classification=$null } } }; [ordered]@{items=@($items)} }
    $signals.pending_reboot = Invoke-Probe 'pending_reboot' 'bounded registry evidence' { $cbs=Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'; $wu=Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'; $pfr=$null -ne (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name PendingFileRenameOperations -ErrorAction SilentlyContinue); [ordered]@{ cbs_reboot_pending=$cbs; windows_update_reboot_required=$wu; pending_file_rename_present=$pfr; pending_file_rename_count=$null; reboot_required=$null } }
    $signals.windows_update = Invoke-Probe 'windows_update' 'wuauserv service state' { $s=Get-Service wuauserv -ErrorAction SilentlyContinue; [ordered]@{ service_name='wuauserv'; service_state=if($s){[string]$s.Status}else{'UNKNOWN'}; start_type=$null; pending_update_count=$null; last_scan_at_utc=$null } }
    $signals.event_log = Invoke-Probe 'event_log' 'Windows Event Log bounded query' { $end=[datetime]::Now; $start=$end.AddHours(-1); $events=@(Get-WinEvent -FilterHashtable @{LogName=@('System','Application'); StartTime=$start; Level=@(1,2)} -ErrorAction SilentlyContinue | Select-Object -First 50 | ForEach-Object { [ordered]@{ log_name=$_.LogName; time_created_utc=(Convert-ToUtcIso $_.TimeCreated); event_id=[int]$_.Id; level=$_.LevelDisplayName; provider=$_.ProviderName } }); [ordered]@{ window_start_utc=(Convert-ToUtcIso $start); window_end_utc=(Convert-ToUtcIso $end); events=$events } }
    $signals.configuration_drift = New-Envelope 'governed baseline manifest' ([ordered]@{baseline_id=$null;baseline_version=$null;observed_items=@();drift_items=@();status='UNKNOWN'}) 'UNKNOWN' 'UNKNOWN' 'BASELINE_NOT_APPROVED'
}

$now=[datetime]::UtcNow
$projection=[ordered]@{ schema_version='1.0'; component='DSG.EagleHostHealthCollector'; computer=$env:COMPUTERNAME; observed_at_utc=(Convert-ToUtcIso $now); fresh_until_utc=(Convert-ToUtcIso $now.AddSeconds($FreshnessSeconds)); quality='CURRENT'; correlation_id=[guid]::NewGuid().ToString(); summary=[ordered]@{state='UNKNOWN';reasons=@([ordered]@{code='POLICY_NOT_ACTIVATED';signal=$null;severity=$null;evidence=$null})}; cadence_class=$CadenceClass; signals=$signals; diagnostics=[ordered]@{collector_mode='READ_ONLY';safety_authority='OUTSIDE_SCOPE';automatic_remediation=$false} }

$dir=Split-Path -Parent $OutputPath
if(-not (Test-Path -LiteralPath $dir)){ New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$tmp=Join-Path $dir ('.'+[IO.Path]::GetFileName($OutputPath)+'.'+[guid]::NewGuid().ToString('N')+'.tmp')
try {
    $json=$projection | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText($tmp,$json,(New-Object Text.UTF8Encoding($false)))
    Move-Item -LiteralPath $tmp -Destination $OutputPath -Force
} finally { if(Test-Path -LiteralPath $tmp){ Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue } }
Write-Output $OutputPath
