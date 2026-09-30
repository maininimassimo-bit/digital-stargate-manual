# Candidate for independent review; do not execute before exact package approval.
[CmdletBinding()]
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-BoundedPilotJob {
    param([scriptblock]$Body, [object[]]$Arguments, [double]$MaximumSeconds)
    if ($MaximumSeconds -le 0) { throw 'WINDOW_EXPIRED' }
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $job = $null
    $ownedProcess = $null
    try {
        $job = Start-Job -ArgumentList @($Body.ToString(),$Arguments) -ScriptBlock {
            param($bodyText,$bodyArgs)
            $process = [Diagnostics.Process]::GetCurrentProcess()
            [pscustomobject]@{dsg_supervisor_pid=$PID; start_ticks=$process.StartTime.ToUniversalTime().Ticks}
            & ([scriptblock]::Create($bodyText)) @bodyArgs
        }
        while ($job.State -in @('Running','NotStarted')) {
            foreach ($item in @(Receive-Job -Job $job)) {
                if ($null -ne $item -and $item.PSObject.Properties['dsg_supervisor_pid']) { $ownedProcess=$item }
                else { Write-Output $item }
            }
            if ($timer.Elapsed.TotalSeconds -ge $MaximumSeconds) {
                if ($null -ne $ownedProcess) {
                    $child = Get-Process -Id $ownedProcess.dsg_supervisor_pid -ErrorAction SilentlyContinue
                    if ($null -ne $child) {
                        if ($child.StartTime.ToUniversalTime().Ticks -ne $ownedProcess.start_ticks) { throw 'CHILD_IDENTITY_CHANGED' }
                        # Terminate only our identified job process tree, including a blocked native gcloud child.
                        & "$env:windir\System32\taskkill.exe" /PID ([string]$ownedProcess.dsg_supervisor_pid) /T /F | Out-Null
                        if ($LASTEXITCODE -ne 0) { throw 'CHILD_TERMINATION_FAILED' }
                    }
                }
                Stop-Job -Job $job
                Write-Output 'BKL043_F4_SUPERVISOR_DEADLINE_STOP'
                return
            }
            Start-Sleep -Milliseconds 100
        }
        foreach ($item in @(Receive-Job -Job $job)) {
            if ($null -ne $item -and $item.PSObject.Properties['dsg_supervisor_pid']) { $ownedProcess=$item }
            else { Write-Output $item }
        }
        if ($job.State -ne 'Completed') { throw 'COLLECTOR_JOB_FAILED' }
    } finally {
        if ($null -ne $job) {
            if ($job.State -in @('Running','NotStarted')) {
                if ($null -ne $ownedProcess) {
                    $child = Get-Process -Id $ownedProcess.dsg_supervisor_pid -ErrorAction SilentlyContinue
                    if ($null -ne $child -and $child.StartTime.ToUniversalTime().Ticks -eq $ownedProcess.start_ticks) {
                        & "$env:windir\System32\taskkill.exe" /PID ([string]$ownedProcess.dsg_supervisor_pid) /T /F | Out-Null
                    }
                }
                Stop-Job -Job $job
            }
            Remove-Job -Job $job
        }
        $timer.Stop()
    }
}

$start = [DateTimeOffset]::Parse('2026-09-30T12:09:21+02:00')
$end = [DateTimeOffset]::Parse('2026-09-30T14:09:21+02:00')
if ($env:COMPUTERNAME -ne 'EAGLE30154') { throw 'HOST_IDENTITY_MISMATCH' }
if ((Get-TimeZone).Id -ne 'W. Europe Standard Time') { throw 'TIMEZONE_MISMATCH' }
if ([DateTimeOffset]::Now -lt $start -or [DateTimeOffset]::Now -ge $end.AddSeconds(-30)) { throw 'OUTSIDE_APPROVED_WINDOW' }
$collector = Join-Path $PSScriptRoot 'Start-BKL043-F4Pilot.ps1'
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw | ConvertFrom-Json
if ((Get-FileHash -LiteralPath $collector -Algorithm SHA256).Hash -ne $manifest.collector_sha256) { throw 'COLLECTOR_HASH_MISMATCH' }
$receiver = 'https://dsg-bkl043-f4-receiver-cfjug35c6q-oc.a.run.app'
# Monotonic deadline: a backwards wall-clock adjustment cannot extend the run.
# Five seconds reserved for cleanup; only this launcher's own job is stopped.
$seconds = ($end.AddSeconds(-5) - [DateTimeOffset]::Now).TotalSeconds
Invoke-BoundedPilotJob -MaximumSeconds $seconds -Arguments @($collector,$receiver) -Body {
    param($path,$url)
    & $path -ReceiverUrl $url
}
