$ErrorActionPreference='Stop'
$script=Join-Path $PSScriptRoot '..\..\scripts\telemetry\Export-EagleHostHealth.ps1'
if(-not (Test-Path $script)){ throw 'Exporter missing' }
$text=Get-Content -Raw $script

$required=@(
  'DSG.EagleHostHealthCollector','eagle-health.json','POLICY_NOT_ACTIVATED',
  'free_bytes','free_pct','health_status','operational_status',
  'automatic_remediation=$false','PROBE_TIMEOUT','SLOW_ON_CHANGE',
  'System.Threading.Mutex','Assert-Projection','[IO.File]::Replace'
)
foreach($token in $required){
  if(-not $text.Contains($token)){ throw "Missing contract token: $token" }
}

$forbidden=@('Restart-Computer','Stop-Process','Restart-Service','Start-Service','Set-Service','Disable-PnpDevice','Enable-PnpDevice','Set-ItemProperty','Remove-ItemProperty','Register-ScheduledTask','Set-NetAdapter','shutdown.exe')
foreach($token in $forbidden){ if($text -match [regex]::Escape($token)){ throw "Forbidden remediation/control command found: $token" } }

$tokens=$null;$errors=$null
[void][System.Management.Automation.Language.Parser]::ParseFile($script,[ref]$tokens,[ref]$errors)
if($errors.Count -gt 0){ throw ('PowerShell parse errors: '+(($errors | ForEach-Object {$_.Message}) -join '; ')) }

$root=Join-Path ([IO.Path]::GetTempPath()) ('dsg-eagle-health-ci-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root -Force | Out-Null
try {
  $out=Join-Path $root 'eagle-health.json'
  $overrides=@{
    cpu={ [ordered]@{ model='CI'; physical_cores=2; logical_processors=2; max_clock_mhz=1; load_pct=1; window_avg_pct=$null; window_peak_pct=$null; temperature_c=$null } }
    memory={ throw 'SIMULATED_MEMORY_FAILURE' }
    processes={ Start-Sleep -Seconds 3; [ordered]@{items=@()} }
    plugin_heartbeat={ [ordered]@{projection_path='ci';exists=$true;last_write_at_utc=$null;plugin_version=$null} }
  }
  & $script -OutputPath $out -CadenceClass fast -FreshnessSeconds 30 -ProbeTimeoutSeconds 1 -LockName ('DSG.CI.'+[guid]::NewGuid()) -ProbeOverrides $overrides | Out-Null
  if(-not (Test-Path $out)){ throw 'Projection not produced' }
  $j=Get-Content -Raw $out | ConvertFrom-Json
  if($j.component -ne 'DSG.EagleHostHealthCollector'){ throw 'Component mismatch' }
  if($j.signals.cpu.state -ne 'OBSERVED'){ throw 'Successful probe was not preserved' }
  if($j.signals.cpu.cadence_class -ne 'FAST'){ throw 'Per-signal cadence missing' }
  if($j.signals.memory.state -ne 'UNAVAILABLE' -or $j.signals.memory.quality -ne 'UNKNOWN'){ throw 'Probe exception was not isolated' }
  if($j.signals.processes.reason -ne 'PROBE_TIMEOUT'){ throw 'Probe timeout was not isolated' }
  if($j.signals.plugin_heartbeat.state -ne 'OBSERVED'){ throw 'Partial success was not preserved' }

  $sentinel='{"sentinel":"previous-valid-projection"}'
  [IO.File]::WriteAllText($out,$sentinel,(New-Object Text.UTF8Encoding($false)))
  $badPath=Join-Path $out 'child.json'
  $failed=$false
  try { & $script -OutputPath $badPath -CadenceClass fast -ProbeTimeoutSeconds 1 -LockName ('DSG.CI.'+[guid]::NewGuid()) -ProbeOverrides $overrides | Out-Null } catch { $failed=$true }
  if(-not $failed){ throw 'Expected invalid projection path failure' }
  if((Get-Content -Raw $out) -ne $sentinel){ throw 'Previous projection was not preserved after publication failure' }

  # Non-overlap must be tested from a second process. A named Mutex is re-entrant
  # for its owning thread, so invoking the collector in this same PowerShell
  # process would not represent two concurrent collector instances.
  $mutexName='DSG.CI.Overlap.'+[guid]::NewGuid()
  $m=New-Object System.Threading.Mutex($false,$mutexName)
  $held=$m.WaitOne(0,$false)
  if(-not $held){ throw 'Unable to acquire parent mutex for non-overlap test' }
  try {
    $overlapOut=Join-Path $root 'overlap.json'
    $childScript=Join-Path $root 'invoke-overlap.ps1'
    $childStdout=Join-Path $root 'overlap.stdout.txt'
    $childStderr=Join-Path $root 'overlap.stderr.txt'
    $escapedScript=$script.Replace("'","''")
    $escapedOut=$overlapOut.Replace("'","''")
    $escapedMutex=$mutexName.Replace("'","''")
    @"
`$ErrorActionPreference='Stop'
& '$escapedScript' -OutputPath '$escapedOut' -CadenceClass fast -ProbeTimeoutSeconds 1 -LockName '$escapedMutex'
"@ | Set-Content -LiteralPath $childScript -Encoding UTF8

    $pwshPath=(Get-Process -Id $PID).Path
    $p=Start-Process -FilePath $pwshPath -ArgumentList @('-NoLogo','-NoProfile','-File',$childScript) -PassThru -RedirectStandardOutput $childStdout -RedirectStandardError $childStderr
    $p.WaitForExit()
    if($p.ExitCode -ne 0){ throw ('Non-overlap child process failed: '+(Get-Content -Raw $childStderr -ErrorAction SilentlyContinue)) }
    $skip=(Get-Content -Raw $childStdout).Trim()
    if($skip -ne 'SKIPPED_NON_OVERLAP'){ throw "Non-overlap invocation was not skipped; output=$skip" }
    if(Test-Path $overlapOut){ throw 'Skipped overlapping invocation unexpectedly wrote a projection' }
  }
  finally {
    $m.ReleaseMutex()
    $m.Dispose()
  }

  Write-Host 'EAGLE host health collector executable failure tests: PASS'
}
finally {
  Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
