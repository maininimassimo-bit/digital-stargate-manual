[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [int]$MaxDepth = 5,
    [int]$MaxFiles = 200
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("ts-shelter-passive-sources-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate TS Shelter passive state source inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)

$roots = @(
    'C:\Program Files (x86)\Common Files\ASCOM\LocalServer',
    'C:\Program Files\Common Files\ASCOM\LocalServer',
    (Join-Path $env:LOCALAPPDATA 'NINA'),
    (Join-Path $env:LOCALAPPDATA 'ASCOM'),
    (Join-Path $env:APPDATA 'ASCOM'),
    (Join-Path $env:PROGRAMDATA 'ASCOM'),
    'C:\DigitalStarGate'
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }

$interestingNames = '(?i)(ts.?shelter|shelter|dome|roof|shutter|ascom)'
$interestingExt = '^\.(log|txt|json|xml|config|ini|csv|dat|db|sqlite|sqlite3)$'

$candidates = New-Object System.Collections.Generic.List[object]
foreach ($root in $roots) {
    try {
        Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match $interestingNames -or $_.Extension -match $interestingExt } |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First $MaxFiles |
            ForEach-Object {
                $candidates.Add([pscustomobject]@{
                    root = $root
                    full_name = $_.FullName
                    name = $_.Name
                    extension = $_.Extension
                    length = $_.Length
                    last_write_time = $_.LastWriteTime
                    last_write_time_utc = $_.LastWriteTimeUtc
                })
            }
    }
    catch { }
}

$unique = @($candidates | Sort-Object full_name -Unique | Sort-Object last_write_time_utc -Descending)

Write-Output ''
Write-Output '=== PASSIVE FILE CANDIDATES ==='
if ($unique.Count -gt 0) {
    $unique | Select-Object -First 100 full_name,length,last_write_time | Format-Table -AutoSize | Out-String -Width 260 | Write-Output
} else {
    Write-Output '(none found)'
}

$pattern = '(?i)(Shutter(Open|Closed|Opening|Closing|Error)|ShutterStatus|OpenDomeShutter|CloseDomeShutter|Shelter Dome|ASCOM\.TS_Shelter\.Dome)'
$matches = New-Object System.Collections.Generic.List[object]
foreach ($file in ($unique | Select-Object -First 100)) {
    if ($file.extension -notmatch '^\.(log|txt|json|xml|config|ini|csv|dat)$') { continue }
    try {
        $lines = @(Get-Content -LiteralPath $file.full_name -Tail 3000 -ErrorAction Stop)
        foreach ($m in ($lines | Select-String -Pattern $pattern)) {
            $matches.Add([pscustomobject]@{
                file = $file.full_name
                file_last_write_utc = $file.last_write_time_utc
                line = $m.Line
            })
        }
    }
    catch { }
}

Write-Output '=== STATE-TEXT MATCHES ==='
if ($matches.Count -gt 0) {
    $matches | Select-Object -Last 120 | ForEach-Object {
        Write-Output ('[{0:o}] {1}' -f $_.file_last_write_utc, $_.file)
        Write-Output $_.line
    }
} else {
    Write-Output '(no state-text matches found)'
}

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.TSShelterPassiveStateSourceInspector'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = 'READ_ONLY_NO_DEVICE_CONNECTIONS'
    roots = @($roots)
    candidates = @($unique)
    state_text_matches = @($matches)
    conclusions = [ordered]@{
        commands_sent = $false
        device_connections_opened = $false
        passive_runtime_source_verified = $false
        note = 'Use a candidate as live telemetry only after proving it updates independently with bounded freshness while the dome state changes.'
    }
}

$jsonPath = Join-Path $bundle 'ts-shelter-passive-sources.json'
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

Write-Output ('Evidence: {0}' -f $jsonPath)
Write-Output 'PASSIVE SOURCE INVENTORY RESULT: PASS (inventory only)'
