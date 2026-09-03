[CmdletBinding()]
param(
    [int]$Iterations = 3,
    [int]$IntervalSeconds = 15,
    [string]$RepositoryPath = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($Iterations -lt 1 -or $Iterations -gt 10) { throw 'Iterations must be between 1 and 10.' }
if ($IntervalSeconds -lt 0 -or $IntervalSeconds -gt 300) { throw 'IntervalSeconds must be between 0 and 300.' }

$discoveryScript = Join-Path $RepositoryPath 'scripts\telemetry\Inspect-EagleHealthSources.ps1'
if (-not (Test-Path -LiteralPath $discoveryScript)) { throw "Discovery script not found: $discoveryScript" }

$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("eagle-health-overhead-pilot-{0}" -f $stamp)
$childEvidenceRoot = Join-Path $bundle 'discovery-runs'
New-Item -ItemType Directory -Path $childEvidenceRoot -Force | Out-Null

Write-Host 'Digital StarGate BKL-030 D3 overhead pilot - READ ONLY'
Write-Host ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Host ('Iterations: {0}' -f $Iterations)
Write-Host ('Interval seconds: {0}' -f $IntervalSeconds)
Write-Host ('Evidence bundle: {0}' -f $bundle)
Write-Host 'Mode: bounded measurement of discovery process; no producer install; no task/service/registry/device changes'

$identity = [pscustomobject]@{
    computer = $env:COMPUTERNAME
    user = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    powershell_version = $PSVersionTable.PSVersion.ToString()
    process_architecture = $env:PROCESSOR_ARCHITECTURE
    observed_at_utc = [DateTime]::UtcNow.ToString('o')
}

$contextProcesses = Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -match '(?i)(NINA|PHD2|ASCOM|CloudWatcher|DigitalStarGate|DSG)'
} | Select-Object ProcessName,Id,WorkingSet64,CPU

$runs = [System.Collections.Generic.List[object]]::new()
$powerShellExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'

for ($i = 1; $i -le $Iterations; $i++) {
    Write-Host ''
    Write-Host ('=== D3 RUN {0}/{1} ===' -f $i,$Iterations)

    $stdout = Join-Path $bundle ("run-{0:00}.stdout.txt" -f $i)
    $stderr = Join-Path $bundle ("run-{0:00}.stderr.txt" -f $i)
    $args = @(
        '-NoLogo','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass',
        '-File',('"{0}"' -f $discoveryScript),
        '-EvidenceRoot',('"{0}"' -f $childEvidenceRoot)
    )

    $started = [DateTime]::UtcNow
    $p = Start-Process -FilePath $powerShellExe -ArgumentList ($args -join ' ') -PassThru -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr

    $peakWorkingSet = 0L
    $samples = 0
    while (-not $p.HasExited) {
        try {
            $p.Refresh()
            if ($p.WorkingSet64 -gt $peakWorkingSet) { $peakWorkingSet = $p.WorkingSet64 }
            $samples++
        } catch { }
        Start-Sleep -Milliseconds 200
    }

    # PowerShell 5.1 can expose a blank/unstable ExitCode on a redirected child process
    # until WaitForExit() has completed. Call it explicitly before reading process metrics.
    $p.WaitForExit()
    $p.Refresh()
    if ($p.WorkingSet64 -gt $peakWorkingSet) { $peakWorkingSet = $p.WorkingSet64 }

    $ended = [DateTime]::UtcNow
    $exitCode = [int]$p.ExitCode
    $cpuSeconds = $null
    try { $cpuSeconds = [math]::Round($p.TotalProcessorTime.TotalSeconds,3) } catch { }
    $stderrLength = if (Test-Path -LiteralPath $stderr) { (Get-Item -LiteralPath $stderr).Length } else { 0 }

    $runs.Add([pscustomobject]@{
        iteration = $i
        started_at_utc = $started.ToString('o')
        ended_at_utc = $ended.ToString('o')
        elapsed_ms = [math]::Round(($ended-$started).TotalMilliseconds,1)
        exit_code = $exitCode
        cpu_seconds = $cpuSeconds
        peak_working_set_bytes = $peakWorkingSet
        monitor_samples = $samples
        stderr_bytes = $stderrLength
        stdout_path = $stdout
        stderr_path = $stderr
    })

    Write-Host ('elapsed_ms={0} exit_code={1} cpu_seconds={2} peak_working_set_bytes={3} stderr_bytes={4}' -f $runs[$runs.Count-1].elapsed_ms,$exitCode,$cpuSeconds,$peakWorkingSet,$stderrLength)
    if ($i -lt $Iterations -and $IntervalSeconds -gt 0) { Start-Sleep -Seconds $IntervalSeconds }
}

$childFiles = @(Get-ChildItem -LiteralPath $childEvidenceRoot -File -Recurse -ErrorAction SilentlyContinue)
$childBytes = ($childFiles | Measure-Object -Property Length -Sum).Sum
if ($null -eq $childBytes) { $childBytes = 0 }

$elapsedValues = @($runs | ForEach-Object { [double]$_.elapsed_ms })
$cpuValues = @($runs | Where-Object { $null -ne $_.cpu_seconds } | ForEach-Object { [double]$_.cpu_seconds })
$wsValues = @($runs | ForEach-Object { [double]$_.peak_working_set_bytes })
$failedRuns = @($runs | Where-Object { [int]$_.exit_code -ne 0 -or [int64]$_.stderr_bytes -gt 0 })

$summary = [pscustomobject]@{
    iterations = $Iterations
    failures = $failedRuns.Count
    elapsed_ms_avg = [math]::Round(($elapsedValues | Measure-Object -Average).Average,1)
    elapsed_ms_max = [math]::Round(($elapsedValues | Measure-Object -Maximum).Maximum,1)
    cpu_seconds_avg = if ($cpuValues.Count -gt 0) { [math]::Round(($cpuValues | Measure-Object -Average).Average,3) } else { $null }
    cpu_seconds_max = if ($cpuValues.Count -gt 0) { [math]::Round(($cpuValues | Measure-Object -Maximum).Maximum,3) } else { $null }
    peak_working_set_bytes_max = [int64](($wsValues | Measure-Object -Maximum).Maximum)
    discovery_evidence_files = $childFiles.Count
    discovery_evidence_bytes = [int64]$childBytes
    nina_running_at_start = [bool](@($contextProcesses | Where-Object ProcessName -match '(?i)^NINA$').Count)
    phd2_running_at_start = [bool](@($contextProcesses | Where-Object ProcessName -match '(?i)^PHD2').Count)
}

$payload = [pscustomobject]@{
    schema_version = '1.0'
    component = 'DSG.EagleHealthOverheadPilot'
    mode = 'READ_ONLY_BOUNDED_PILOT'
    identity = $identity
    parameters = [pscustomobject]@{ iterations=$Iterations; interval_seconds=$IntervalSeconds; discovery_script=$discoveryScript }
    operational_context = @($contextProcesses)
    runs = @($runs)
    summary = $summary
    disposition = 'MEASUREMENT_ONLY_NOT_BKL030_ACCEPTANCE'
}

$jsonPath = Join-Path $bundle 'eagle-health-overhead-pilot.json'
$payload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

Write-Host ''
Write-Host '=== D3 OVERHEAD SUMMARY ==='
$summary | Format-List *
Write-Host ('Evidence JSON: {0}' -f $jsonPath)
Write-Host 'BKL-030 D3 PILOT RESULT: MEASURED (descriptive evidence only; no thresholds or acceptance inferred)'
