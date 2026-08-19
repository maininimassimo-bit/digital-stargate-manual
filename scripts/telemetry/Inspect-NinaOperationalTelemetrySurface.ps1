[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate NINA operational telemetry surface inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)

$targets = @(Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -match '(?i)nina|ts_shelter|ascom\.ts_shelter' } |
    Select-Object ProcessName,Id,Path,StartTime)

Write-Output ''
Write-Output '=== TARGET PROCESSES ==='
if ($targets.Count -gt 0) {
    $targets | Format-Table -AutoSize | Out-String -Width 240 | Write-Output
} else {
    Write-Output '(no NINA/TS Shelter process found)'
}

Write-Output '=== TCP LISTENERS OWNED BY TARGETS ==='
$listeners = @()
try {
    $allListeners = @(Get-NetTCPConnection -State Listen -ErrorAction Stop)
    foreach ($proc in $targets) {
        $listeners += $allListeners |
            Where-Object { $_.OwningProcess -eq $proc.Id } |
            Select-Object @{n='ProcessName';e={$proc.ProcessName}},OwningProcess,LocalAddress,LocalPort,State
    }
} catch {
    Write-Output ('Get-NetTCPConnection failed: {0}' -f $_.Exception.Message)
}
if ($listeners.Count -gt 0) {
    $listeners | Sort-Object LocalPort | Format-Table -AutoSize | Out-String -Width 220 | Write-Output
} else {
    Write-Output '(none)'
}

Write-Output '=== ESTABLISHED TCP CONNECTIONS OWNED BY TARGETS ==='
$established = @()
try {
    $allEstablished = @(Get-NetTCPConnection -State Established -ErrorAction Stop)
    foreach ($proc in $targets) {
        $established += $allEstablished |
            Where-Object { $_.OwningProcess -eq $proc.Id } |
            Select-Object @{n='ProcessName';e={$proc.ProcessName}},OwningProcess,LocalAddress,LocalPort,RemoteAddress,RemotePort,State
    }
} catch {
    Write-Output ('Get-NetTCPConnection established scan failed: {0}' -f $_.Exception.Message)
}
if ($established.Count -gt 0) {
    $established | Sort-Object ProcessName,LocalPort | Format-Table -AutoSize | Out-String -Width 260 | Write-Output
} else {
    Write-Output '(none)'
}

Write-Output '=== NAMED PIPE CANDIDATES ==='
$pipeNames = @()
try {
    $pipeNames = @(Get-ChildItem -LiteralPath '\\.\pipe\' -ErrorAction Stop |
        Select-Object -ExpandProperty Name |
        Where-Object { $_ -match '(?i)nina|shelter|ascom|dome' } |
        Sort-Object -Unique)
} catch {
    Write-Output ('Named pipe inventory failed: {0}' -f $_.Exception.Message)
}
if ($pipeNames.Count -gt 0) {
    $pipeNames | ForEach-Object { Write-Output $_ }
} else {
    Write-Output '(none matched)'
}

Write-Output '=== TS SHELTER LOCALSERVER PROCESS DETAILS ==='
$ts = @($targets | Where-Object { $_.ProcessName -match '(?i)TS_Shelter' })
if ($ts.Count -gt 0) {
    foreach ($proc in $ts) {
        try {
            Get-CimInstance Win32_Process -Filter ("ProcessId={0}" -f $proc.Id) -ErrorAction Stop |
                Select-Object ProcessId,Name,ExecutablePath,CommandLine,ParentProcessId |
                Format-List | Out-String -Width 260 | Write-Output
        } catch {
            Write-Output ('Unable to read process details for PID {0}: {1}' -f $proc.Id,$_.Exception.Message)
        }
    }
} else {
    Write-Output '(TS Shelter LocalServer not running)'
}

Write-Output 'No socket connection was opened. No endpoint was called. No named pipe was opened. No ASCOM/COM object was created. No device connection was changed.'
Write-Output 'NINA OPERATIONAL TELEMETRY SURFACE RESULT: PASS (inventory only)'
