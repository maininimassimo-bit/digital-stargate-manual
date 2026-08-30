[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-ascom-surface-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate CloudWatcher ASCOM surface inspector - READ ONLY / NO ASCOM ACTIVATION'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)

function Get-RegistryEntries {
    param([Parameter(Mandatory = $true)][string[]]$Roots)

    $entries = @()
    foreach ($root in $Roots) {
        if (-not (Test-Path -LiteralPath $root)) { continue }
        try {
            Get-ChildItem -LiteralPath $root -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
                $item = $_
                $props = @{}
                try {
                    foreach ($name in $item.GetValueNames()) {
                        $value = [string]$item.GetValue($name)
                        if (-not [string]::IsNullOrWhiteSpace($value)) {
                            $props[$name] = $value
                        }
                    }
                }
                catch { }
                $rendered = ($props.GetEnumerator() | ForEach-Object { "{0}={1}" -f $_.Key,$_.Value }) -join '; '
                if ($item.Name -match '(?i)(CloudWatcher|ObservingConditions|CWAscom|Lunatico|AAG)' -or $rendered -match '(?i)(CloudWatcher|ObservingConditions|CWAscom|Lunatico|AAG)') {
                    $entries += [pscustomobject]@{
                        path = $item.Name
                        values = $rendered
                    }
                }
            }
        }
        catch { }
    }
    return @($entries | Sort-Object path -Unique)
}

$registryRoots = @(
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\ASCOM',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\ASCOM',
    'Registry::HKEY_CURRENT_USER\Software\ASCOM',
    'Registry::HKEY_CLASSES_ROOT'
)

$entries = @(Get-RegistryEntries -Roots $registryRoots)
$processes = @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -match '(?i)(CloudWatcher|CWAscom)'
} | Select-Object ProcessName,Id,Path)

$installFiles = @()
foreach ($root in @('C:\Program Files (x86)\CWAscom','C:\Program Files\CWAscom')) {
    if (Test-Path -LiteralPath $root) {
        $installFiles += @(Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction SilentlyContinue | Select-Object FullName,Length,LastWriteTimeUtc,@{n='FileVersion';e={$_.VersionInfo.FileVersion}},@{n='ProductVersion';e={$_.VersionInfo.ProductVersion}})
    }
}

$progIdCandidates = @($entries | Where-Object {
    $_.path -match '(?i)(ObservingConditions|CloudWatcher|CWAscom)' -or $_.values -match '(?i)(ObservingConditions|CloudWatcher|CWAscom)'
})

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.CloudWatcherAscomSurfaceInspector'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = 'READ_ONLY_REGISTRY_AND_FILE_METADATA_NO_ASCOM_ACTIVATION'
    running_processes = $processes
    registry_entries = $entries
    install_files = $installFiles
    conclusions = [ordered]@{
        candidate_entries = $progIdCandidates.Count
        ascom_object_activated = $false
        device_connection_opened = $false
        serial_port_opened = $false
        disposition = if ($progIdCandidates.Count -gt 0) { 'ASCOM_CLOUDWATCHER_SURFACE_FOUND_REQUIRES_SEMANTIC_REVIEW' } else { 'NO_ASCOM_CLOUDWATCHER_REGISTRATION_FOUND'
        }
    }
}

$jsonPath = Join-Path $bundle 'cloudwatcher-ascom-surface.json'
$txtPath = Join-Path $bundle 'cloudwatcher-ascom-surface.txt'
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== RUNNING PROCESSES ===',
    ($processes | Format-Table -AutoSize | Out-String),
    '=== ASCOM / CLOUDWATCHER REGISTRY CANDIDATES ===',
    ($progIdCandidates | Format-Table -Wrap -AutoSize | Out-String),
    '=== CWASCOM INSTALL FILES ===',
    ($installFiles | Format-Table -AutoSize | Out-String),
    '=== CONCLUSIONS ===',
    ($report.conclusions | Format-List | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== RUNNING PROCESSES ==='
if ($processes.Count -gt 0) { $processes | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none)' }
Write-Output '=== ASCOM / CLOUDWATCHER REGISTRY CANDIDATES ==='
if ($progIdCandidates.Count -gt 0) { $progIdCandidates | Format-Table -Wrap -AutoSize | Out-String | Write-Output } else { Write-Output '(none)' }
Write-Output '=== CWASCOM INSTALL FILES ==='
if ($installFiles.Count -gt 0) { $installFiles | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none)' }
Write-Output '=== DISPOSITION ==='
Write-Output $report.conclusions.disposition
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'CLOUDWATCHER ASCOM SURFACE INSPECTION RESULT: PASS (no ASCOM activation)'
