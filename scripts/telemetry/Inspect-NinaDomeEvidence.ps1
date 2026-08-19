[CmdletBinding()]
param(
    [string]$NinaRoot = "$env:LOCALAPPDATA\NINA",
    [int]$MaxFiles = 50,
    [int]$TailLines = 4000
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate NINA dome evidence inspector - READ ONLY'
Write-Output ('NINA root: {0}' -f $NinaRoot)

if (-not (Test-Path -LiteralPath $NinaRoot)) {
    throw "NINA root non trovato: $NinaRoot"
}

$patterns = @('TS_Shelter','TS Shelter','Dome','ShutterStatus','AtPark','AtHome','Connected')

$files = @(Get-ChildItem -LiteralPath $NinaRoot -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -match '^\.(json|xml|config|txt|log)$' } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First $MaxFiles)

Write-Output ''
Write-Output '=== MATCHES ==='
$found = 0
foreach ($file in $files) {
    try {
        $lines = @(Get-Content -LiteralPath $file.FullName -Tail $TailLines -ErrorAction Stop)
        $matches = @($lines | Select-String -Pattern $patterns -SimpleMatch -CaseSensitive:$false)
        if ($matches.Count -gt 0) {
            $found++
            Write-Output ('--- {0} | {1:o} ---' -f $file.FullName, $file.LastWriteTime)
            $matches | Select-Object -Last 80 | ForEach-Object { Write-Output $_.Line }
        }
    }
    catch { }
}

if ($found -eq 0) {
    Write-Output '(no relevant matches found)'
}

Write-Output ''
Write-Output 'NINA DOME EVIDENCE RESULT: PASS (read-only search only)'
