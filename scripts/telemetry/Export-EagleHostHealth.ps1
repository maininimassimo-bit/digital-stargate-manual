[CmdletBinding()]
param(
    [string]$OutputPath = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\eagle-health.json'),
    [ValidateSet('fast','medium','slow','all')]
    [string]$CadenceClass = 'all',
    [int]$FreshnessSeconds = 120,
    [ValidateRange(1,60)]
    [int]$ProbeTimeoutSeconds = 10,
    [string]$LockName = 'DigitalStarGate.EagleHostHealthCollector',
    [hashtable]$ProbeOverrides
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Convert-ToUtcIso([datetime]$Value) { $Value.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ') }
function Get-GovernedCadence([string]$Cadence) {
    switch ($Cadence) { 'fast' {'FAST'} 'medium' {'MEDIUM'} 'slow' {'SLOW_ON_CHANGE'} default {'MIXED'} }
}
function New-Envelope([string]$Source,[string]$SignalCadence,[object]$Data,[string]$State='OBSERVED',[string]$Quality='CURRENT',[string]$Reason=$null) {
    $now=[datetime]::UtcNow
    [ordered]@{ state=$State; quality=$Quality; observed_at_utc=Convert-ToUtcIso $now; fresh_until_utc=Convert-ToUtcIso $now.AddSeconds($FreshnessSeconds); source=$Source; cadence_class=$SignalCadence; reason=$Reason; data=$Data }
}
function Invoke-BoundedProbe([string]$Name,[string]$Source,[string]$SignalCadence,[scriptblock]$Body) {
    if($null -ne $ProbeOverrides -and $ProbeOverrides.ContainsKey($Name)){ $Body=[scriptblock]$ProbeOverrides[$Name]; $Source='TEST_OVERRIDE' }
    $ps=[powershell]::Create(); $async=$null
    try {
        [void]$ps.AddScript($Body.ToString()); $async=$ps.BeginInvoke()
        if(-not $async.AsyncWaitHandle.WaitOne([timespan]::FromSeconds($ProbeTimeoutSeconds))){ try{$ps.Stop()}catch{}; return New-Envelope $Source $SignalCadence $null 'UNAVAILABLE' 'UNKNOWN' 'PROBE_TIMEOUT' }
        try {
            $result=@($ps.EndInvoke($async))
            if($ps.HadErrors){ $message=(($ps.Streams.Error|ForEach-Object{$_.Exception.Message}) -join '; '); if([string]::IsNullOrWhiteSpace($message)){$message='PROBE_ERROR'}; return New-Envelope $Source $SignalCadence $null 'UNAVAILABLE' 'UNKNOWN' (($message -replace '[\r\n]+',' ').Trim()) }
            $data=if($result.Count -eq 1){$result[0]}else{@($result)}
            return New-Envelope $Source $SignalCadence $data
        } catch { return New-Envelope $Source $SignalCadence $null 'UNAVAILABLE' 'UNKNOWN' (($_.Exception.Message -replace '[\r\n]+',' ').Trim()) }
    } catch { return New-Envelope $Source $SignalCadence $null 'UNAVAILABLE' 'UNKNOWN' (($_.Exception.Message -replace '[\r\n]+',' ').Trim()) }
    finally { if($null -ne $async -and $null -ne $async.AsyncWaitHandle){$async.AsyncWaitHandle.Close()}; $ps.Dispose() }
}
function Assert-Projection([string]$JsonText) {
    $parsed=$JsonText|ConvertFrom-Json -ErrorAction Stop
    if([string]$parsed.schema_version -ne '1.0'){throw 'Invalid schema_version.'}
    if([string]$parsed.component -ne 'DSG.EagleHostHealthCollector'){throw 'Invalid component.'}
    if($null -eq $parsed.signals){throw 'Projection signals missing.'}
    if($null -eq $parsed.summary){throw 'Projection summary missing.'}
    if([string]$parsed.diagnostics.collector_mode -ne 'READ_ONLY'){throw 'Invalid collector mode.'}
}

$mutex=New-Object System.Threading.Mutex($false,$LockName); $lockAcquired=$false
try {
    try{$lockAcquired=$mutex.WaitOne(0,$false)}catch [System.Threading.AbandonedMutexException]{$lockAcquired=$true}
    if(-not $lockAcquired){Write-Output 'SKIPPED_NON_OVERLAP'; exit 0}
    $signals=[ordered]@{}

    if($CadenceClass -in @('fast','all')){
        $signals.cpu=Invoke-BoundedProbe 'cpu' 'Win32_Processor' 'FAST' { $cpu=Get-CimInstance Win32_Processor|Select-Object -First 1; [ordered]@{model=$cpu.Name;physical_cores=[int]$cpu.NumberOfCores;logical_processors=[int]$cpu.NumberOfLogicalProcessors;max_clock_mhz=[int]$cpu.MaxClockSpeed;load_pct=if($null -eq $cpu.LoadPercentage){$null}else{[double]$cpu.LoadPercentage};window_avg_pct=$null;window_peak_pct=$null;temperature_c=$null} }
        $signals.memory=Invoke-BoundedProbe 'memory' 'Win32_OperatingSystem' 'FAST' { $os=Get-CimInstance Win32_OperatingSystem; $total=[int64]$os.TotalVisibleMemorySize*1024; $free=[int64]$os.FreePhysicalMemory*1024; [ordered]@{total_physical_bytes=$total;available_physical_bytes=$free;available_ratio=if($total -gt 0){[math]::Round($free/[double]$total,6)}else{$null};commit_used_bytes=$null;commit_limit_bytes=$null;memory_pressure=$null} }
        $signals.processes=Invoke-BoundedProbe 'processes' 'Windows process table' 'FAST' { $names=@('NINA','phd2','AAG_CloudWatcher','ASCOM.TS_Shelter'); $items=foreach($n in $names){$p=@(Get-Process -Name $n -ErrorAction SilentlyContinue);[ordered]@{name=$n;running=($p.Count -gt 0);pid=if($p.Count){$p[0].Id}else{$null};started_at_utc=$null;working_set_bytes=if($p.Count){[int64]$p[0].WorkingSet64}else{$null};cpu_total_seconds=if($p.Count -and $null -ne $p[0].CPU){[double]$p[0].CPU}else{$null}}}; [ordered]@{items=@($items)} }
        $signals.plugin_heartbeat=Invoke-BoundedProbe 'plugin_heartbeat' 'NINA telemetry projection metadata' 'FAST' { $p=Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\nina-observatory-status.json'; $f=Get-Item -LiteralPath $p -ErrorAction SilentlyContinue; [ordered]@{projection_path=$p;exists=($null -ne $f);last_write_at_utc=if($f){$f.LastWriteTimeUtc.ToString('yyyy-MM-ddTHH:mm:ss.fffZ')}else{$null};plugin_version=$null} }
    }

    if($CadenceClass -in @('medium','all')){
        $signals.storage=Invoke-BoundedProbe 'storage' 'Win32_LogicalDisk/Get-PhysicalDisk' 'MEDIUM' { $logical=@(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3'|ForEach-Object{$size=[int64]$_.Size;$free=[int64]$_.FreeSpace;[ordered]@{device_id=$_.DeviceID;volume_name=$_.VolumeName;filesystem=$_.FileSystem;size_bytes=$size;free_bytes=$free;free_ratio=if($size -gt 0){[math]::Round($free/[double]$size,6)}else{$null};free_pct=if($size -gt 0){[math]::Round(100*$free/[double]$size,3)}else{$null}}}); $physical=@(); if(Get-Command Get-PhysicalDisk -ErrorAction SilentlyContinue){$physical=@(Get-PhysicalDisk|ForEach-Object{[ordered]@{friendly_name=$_.FriendlyName;media_type=[string]$_.MediaType;bus_type=[string]$_.BusType;health_status=[string]$_.HealthStatus;operational_status=@($_.OperationalStatus|ForEach-Object{[string]$_});size_bytes=[int64]$_.Size}})}; [ordered]@{logical_disks=$logical;physical_disks=$physical;reliability=[ordered]@{available=$false;temperature_c=$null;temperature_max_c=$null;wear_pct=$null;read_errors_total=$null;write_errors_total=$null;power_on_hours=$null;reason='UNAVAILABLE_UNLESS_SEPARATELY_VERIFIED'}} }
        $signals.uptime=Invoke-BoundedProbe 'uptime' 'Win32_OperatingSystem' 'MEDIUM' { $os=Get-CimInstance Win32_OperatingSystem;$boot=[datetime]$os.LastBootUpTime;[ordered]@{last_boot_at_utc=$boot.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ');uptime_seconds=[int64]([datetime]::UtcNow-$boot.ToUniversalTime()).TotalSeconds;unexpected_reboot_observed=$null} }
        $signals.time_sync=Invoke-BoundedProbe 'time_sync' 'W32Time service state' 'MEDIUM' { $s=Get-Service W32Time -ErrorAction SilentlyContinue;[ordered]@{service_state=if($s){[string]$s.Status}else{'UNKNOWN'};time_source=$null;stratum=$null;last_successful_sync_utc=$null;offset_ms=$null;command_available=($null -ne (Get-Command w32tm.exe -ErrorAction SilentlyContinue))} }
        $signals.usb_com=Invoke-BoundedProbe 'usb_com' 'Win32_PnPEntity' 'MEDIUM' { $ports=@(Get-CimInstance Win32_PnPEntity|Where-Object{$_.Name -match '\(COM\d+\)'}|ForEach-Object{[ordered]@{name=$_.Name;status=$_.Status;manufacturer=$_.Manufacturer;device_id=$_.PNPDeviceID}});[ordered]@{serial_ports=$ports;source_reconciliation='PNP_PRIMARY'} }
        $signals.log_sources=Invoke-BoundedProbe 'log_sources' 'filesystem metadata' 'MEDIUM' { [ordered]@{items=@()} }
    }

    if($CadenceClass -in @('slow','all')){
        $signals.scheduled_tasks=Invoke-BoundedProbe 'scheduled_tasks' 'Task Scheduler read API' 'SLOW_ON_CHANGE' { $items=@();if(Get-Command Get-ScheduledTask -ErrorAction SilentlyContinue){foreach($t in @(Get-ScheduledTask|Where-Object{$_.TaskName -like 'Digital StarGate*'})){$i=$t|Get-ScheduledTaskInfo;$items += [ordered]@{task_name=$t.TaskName;task_path=$t.TaskPath;state=[string]$t.State;last_run_at_utc=if($i.LastRunTime.Year -gt 1900){$i.LastRunTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ')}else{$null};last_task_result=[int64]$i.LastTaskResult;next_run_at_utc=if($i.NextRunTime.Year -gt 1900){$i.NextRunTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ')}else{$null};result_classification=$null}}};[ordered]@{items=@($items)} }
        $signals.pending_reboot=Invoke-BoundedProbe 'pending_reboot' 'bounded registry evidence' 'SLOW_ON_CHANGE' { $cbs=Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending';$wu=Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired';$pfr=$null -ne (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name PendingFileRenameOperations -ErrorAction SilentlyContinue);[ordered]@{cbs_reboot_pending=$cbs;windows_update_reboot_required=$wu;pending_file_rename_present=$pfr;pending_file_rename_count=$null;reboot_required=$null} }
        $signals.windows_update=Invoke-BoundedProbe 'windows_update' 'wuauserv service state' 'SLOW_ON_CHANGE' { $s=Get-Service wuauserv -ErrorAction SilentlyContinue;[ordered]@{service_name='wuauserv';service_state=if($s){[string]$s.Status}else{'UNKNOWN'};start_type=$null;pending_update_count=$null;last_scan_at_utc=$null} }
        $signals.event_log=Invoke-BoundedProbe 'event_log' 'Windows Event Log bounded query' 'SLOW_ON_CHANGE' {
            $end=[datetime]::Now; $start=$end.AddHours(-1); $events=@()
            try {
                $events=@(Get-WinEvent -FilterHashtable @{LogName=@('System','Application');StartTime=$start;Level=@(1,2)} -ErrorAction Stop|Select-Object -First 50|ForEach-Object{[ordered]@{log_name=$_.LogName;time_created_utc=$_.TimeCreated.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ');event_id=[int]$_.Id;level=$_.LevelDisplayName;provider=$_.ProviderName}})
            } catch {
                if($_.FullyQualifiedErrorId -notlike 'NoMatchingEventsFound*'){ throw }
                $events=@()
            }
            [ordered]@{window_start_utc=$start.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ');window_end_utc=$end.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ');events=@($events)}
        }
        $signals.configuration_drift=New-Envelope 'governed baseline manifest' 'SLOW_ON_CHANGE' ([ordered]@{baseline_id=$null;baseline_version=$null;observed_items=@();drift_items=@();status='UNKNOWN'}) 'UNKNOWN' 'UNKNOWN' 'BASELINE_NOT_APPROVED'
    }

    $now=[datetime]::UtcNow
    $projection=[ordered]@{schema_version='1.0';component='DSG.EagleHostHealthCollector';computer=$env:COMPUTERNAME;observed_at_utc=(Convert-ToUtcIso $now);fresh_until_utc=(Convert-ToUtcIso $now.AddSeconds($FreshnessSeconds));quality='CURRENT';correlation_id=[guid]::NewGuid().ToString();summary=[ordered]@{state='UNKNOWN';reasons=@([ordered]@{code='POLICY_NOT_ACTIVATED';signal=$null;severity=$null;evidence=$null})};cadence_class=(Get-GovernedCadence $CadenceClass);signals=$signals;diagnostics=[ordered]@{collector_mode='READ_ONLY';safety_authority='OUTSIDE_SCOPE';automatic_remediation=$false;probe_timeout_seconds=$ProbeTimeoutSeconds;non_overlap='MUTEX_SKIP'}}
    $dir=Split-Path -Parent $OutputPath;if(-not(Test-Path -LiteralPath $dir)){New-Item -ItemType Directory -Path $dir -Force|Out-Null}
    $tmp=Join-Path $dir ('.'+[IO.Path]::GetFileName($OutputPath)+'.'+[guid]::NewGuid().ToString('N')+'.tmp');$backup=Join-Path $dir ('.'+[IO.Path]::GetFileName($OutputPath)+'.'+[guid]::NewGuid().ToString('N')+'.bak')
    try { $json=$projection|ConvertTo-Json -Depth 12;Assert-Projection $json;[IO.File]::WriteAllText($tmp,$json,(New-Object Text.UTF8Encoding($false)));Assert-Projection([IO.File]::ReadAllText($tmp));if(Test-Path -LiteralPath $OutputPath -PathType Leaf){[IO.File]::Replace($tmp,$OutputPath,$backup,$true);if(Test-Path -LiteralPath $backup){Remove-Item -LiteralPath $backup -Force -ErrorAction SilentlyContinue}}else{Move-Item -LiteralPath $tmp -Destination $OutputPath} }
    finally {if(Test-Path -LiteralPath $tmp){Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue};if(Test-Path -LiteralPath $backup){Remove-Item -LiteralPath $backup -Force -ErrorAction SilentlyContinue}}
    Write-Output $OutputPath
}
finally {if($lockAcquired){try{$mutex.ReleaseMutex()}catch{}};$mutex.Dispose()}
