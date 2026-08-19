[CmdletBinding()]
param(
    [string]$NinaRoot = "$env:LOCALAPPDATA\NINA"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate NINA local telemetry interface inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('NINA root: {0}' -f $NinaRoot)

Write-Output ''
Write-Output '=== NINA PROCESSES ==='
$ninaProcesses = @(Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -match '(?i)^NINA$|NINA' } |
    Select-Object ProcessName,Id,Path,StartTime)
if ($ninaProcesses.Count -gt 0) {
    $ninaProcesses | Format-Table -AutoSize | Out-String -Width 220 | Write-Output
} else {
    Write-Output '(NINA process not running)'
}

Write-Output '=== TCP LISTENERS OWNED BY NINA ==='
$listeners = @()
try {
    $connections = @(Get-NetTCPConnection -State Listen -ErrorAction Stop)
    foreach ($proc in $ninaProcesses) {
        $listeners += $connections |
            Where-Object { $_.OwningProcess -eq $proc.Id } |
            Select-Object @{n='ProcessName';e={$proc.ProcessName}},OwningProcess,LocalAddress,LocalPort,State
    }
} catch {
    Write-Output ('Get-NetTCPConnection unavailable/failed: {0}' -f $_.Exception.Message)
}
if ($listeners.Count -gt 0) {
    $listeners | Sort-Object LocalPort | Format-Table -AutoSize | Out-String -Width 220 | Write-Output
} else {
    Write-Output '(no NINA-owned listening TCP ports found)'
}

Write-Output '=== NINA PLUGIN / EXTENSION DIRECTORIES ==='
$candidateDirs = @(
    (Join-Path $NinaRoot 'Plugins'),
    (Join-Path $NinaRoot 'Plugin'),
    (Join-Path $NinaRoot 'Extensions'),
    (Join-Path $NinaRoot 'Plugins3'),
    (Join-Path $NinaRoot 'Profiles')
)
foreach ($dir in $candidateDirs) {
    if (Test-Path -LiteralPath $dir) {
        Write-Output ('--- {0} ---' -f $dir)
        Get-ChildItem -LiteralPath $dir -Force -ErrorAction SilentlyContinue |
            Select-Object Name,FullName,PSIsContainer,LastWriteTime |
            Format-Table -AutoSize | Out-String -Width 260 | Write-Output
    }
}

Write-Output '=== API / SERVER CONFIG REFERENCES ==='
$patterns = @('api','rest','http','https','websocket','socket','server','port','advanced sequencer','remote')
$configFiles = @()
if (Test-Path -LiteralPath $NinaRoot) {
    $configFiles = @(Get-ChildItem -LiteralPath $NinaRoot -File -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -match '^\.(config|json|xml|ini|txt)$' } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 120)
}

$found = 0
foreach ($file in $configFiles) {
    try {
        $hits = @(Get-Content -LiteralPath $file.FullName -Tail 2500 -ErrorAction Stop |
            Select-String -Pattern $patterns -SimpleMatch -CaseSensitive:$false)
        if ($hits.Count -gt 0) {
            $found++
            Write-Output ('--- {0} | {1:o} ---' -f $file.FullName,$file.LastWriteTime)
            foreach ($hit in ($hits | Select-Object -Last 80)) {
                $line = [string]$hit.Line
                if ($line -match '(?i)(token|secret|password|apikey|api_key|authorization|bearer)') {
                    Write-Output '[redacted sensitive-looking line]'
                } else {
                    Write-Output $line
                }
            }
        }
    } catch { }
}
if ($found -eq 0) {
    Write-Output '(no API/server references found in inspected config files)'
}

Write-Output 'No network request was sent. No HTTP endpoint was called. No ASCOM/COM object was created. No device connection was opened.'
Write-Output 'NINA LOCAL TELEMETRY INTERFACE RESULT: PASS (inventory only)'
