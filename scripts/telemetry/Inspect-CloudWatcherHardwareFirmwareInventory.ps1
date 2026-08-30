[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [string]$InstallRoot = 'C:\Program Files (x86)\AAG_CloudWatcher',
    [string]$CloudWatcherDataRoot = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher',
    [ValidateRange(16384, 1048576)][int]$MaxTextBytesPerFile = 262144
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-hardware-firmware-inventory-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate CloudWatcher hardware/firmware metadata inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)
Write-Output 'Mode: local files/registry metadata only; NO COM activation; NO serial access'

function Get-SafeRegistryValueSet {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    try {
        $item = Get-Item -LiteralPath $Path -ErrorAction Stop
        $values = @()
        foreach ($name in $item.GetValueNames()) {
            if ($name -match '(?i)(password|secret|token|credential|community|key)') { continue }
            $value = [string]$item.GetValue($name)
            if ([string]::IsNullOrWhiteSpace($value)) { continue }
            if ($name -notmatch '(?i)(firmware|version|serial|model|device|hardware|revision|rev|port|com|sensor|light|sqm|quality|path|file)') { continue }
            $values += [pscustomobject]@{
                registry_path = $Path
                name = if ([string]::IsNullOrWhiteSpace($name)) { '(Default)' } else { $name }
                value = $value
            }
        }
        return @($values)
    }
    catch { return @() }
}

function Get-RegistryEvidence {
    param([Parameter(Mandatory = $true)][string[]]$Roots)

    $evidence = @()
    foreach ($root in $Roots) {
        if (-not (Test-Path -LiteralPath $root)) { continue }
        $evidence += @(Get-SafeRegistryValueSet -Path $root)
        try {
            Get-ChildItem -LiteralPath $root -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
                $evidence += @(Get-SafeRegistryValueSet -Path $_.PSPath)
            }
        }
        catch { }
    }
    return @($evidence)
}

function Get-FileMetadata {
    param([Parameter(Mandatory = $true)][string[]]$Roots)

    $files = @()
    foreach ($root in $Roots) {
        if ([string]::IsNullOrWhiteSpace($root) -or -not (Test-Path -LiteralPath $root)) { continue }
        try {
            Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 500 | ForEach-Object {
                $fileVersion = $null
                $productVersion = $null
                if ($_.Extension -match '(?i)^\.(exe|dll|ocx)$') {
                    try {
                        $fileVersion = $_.VersionInfo.FileVersion
                        $productVersion = $_.VersionInfo.ProductVersion
                    }
                    catch { }
                }
                $files += [pscustomobject]@{
                    path = $_.FullName
                    extension = $_.Extension
                    size_bytes = $_.Length
                    last_write_time_utc = $_.LastWriteTimeUtc.ToString('o')
                    file_version = $fileVersion
                    product_version = $productVersion
                }
            }
        }
        catch { }
    }
    return @($files | Sort-Object path -Unique)
}

function Get-TextEvidence {
    param(
        [Parameter(Mandatory = $true)][object[]]$Files,
        [Parameter(Mandatory = $true)][int]$MaxBytes
    )

    $allowedExtensions = '(?i)^\.(ini|cfg|config|xml|json|dat|txt|log|csv)$'
    $pattern = '(?i)(firmware|fw\s*version|hardware\s*(version|revision|rev)|device\s*(version|model|id)|model|serial\s*(number|no|id)|sky\s*quality|sqm|mpsas|mag(?:nitudes?)?\s*(?:per|/)\s*(?:square\s*)?arcsec|!8|!4)'
    $evidence = @()

    foreach ($file in @($Files | Where-Object { $_.extension -match $allowedExtensions })) {
        if ($file.size_bytes -gt $MaxBytes) { continue }
        try {
            $lineNumber = 0
            Get-Content -LiteralPath $file.path -ErrorAction Stop | ForEach-Object {
                $lineNumber++
                $line = [string]$_
                if ($line -notmatch $pattern) { return }
                if ($line -match '(?i)(password|secret|token|credential|community|api[_ -]?key)') { return }
                $trimmed = $line.Trim()
                if ($trimmed.Length -gt 300) { $trimmed = $trimmed.Substring(0,300) + '...' }
                $evidence += [pscustomobject]@{
                    path = $file.path
                    line = $lineNumber
                    text = $trimmed
                }
            }
        }
        catch { }
    }
    return @($evidence)
}

$registryRoots = @(
    'Registry::HKEY_CURRENT_USER\Software\VB and VBA Program Settings\AAG_CloudWatcher',
    'Registry::HKEY_CURRENT_USER\Software\VB and VBA Program Settings\AAG_WeatherCenter',
    'Registry::HKEY_CURRENT_USER\Software\Lunatico',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Lunatico',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\AAG_CloudWatcher'
)

$fileRoots = @(
    $InstallRoot,
    $CloudWatcherDataRoot,
    (Join-Path $env:APPDATA 'AAG_CloudWatcher'),
    (Join-Path $env:LOCALAPPDATA 'AAG_CloudWatcher'),
    (Join-Path $env:APPDATA 'AAG_WeatherCenter'),
    (Join-Path $env:LOCALAPPDATA 'AAG_WeatherCenter'),
    (Join-Path $env:APPDATA 'Lunatico'),
    (Join-Path $env:LOCALAPPDATA 'Lunatico')
)

$registryEvidence = @(Get-RegistryEvidence -Roots $registryRoots)
$files = @(Get-FileMetadata -Roots $fileRoots)
$textEvidence = @(Get-TextEvidence -Files $files -MaxBytes $MaxTextBytesPerFile)

$binaryMetadata = @($files | Where-Object {
    $_.extension -match '(?i)^\.(exe|dll|ocx)$' -and
    (-not [string]::IsNullOrWhiteSpace([string]$_.file_version) -or -not [string]::IsNullOrWhiteSpace([string]$_.product_version))
})

$firmwareEvidence = @($textEvidence | Where-Object { $_.text -match '(?i)(firmware|fw\s*version|hardware\s*(version|revision|rev)|device\s*(version|model)|model|serial\s*(number|no|id))' })
$sqmEvidence = @($textEvidence | Where-Object { $_.text -match '(?i)(sky\s*quality|sqm|mpsas|mag(?:nitudes?)?\s*(?:per|/)\s*(?:square\s*)?arcsec|!8)' })

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.CloudWatcherHardwareFirmwareInventory'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = 'READ_ONLY_LOCAL_METADATA_NO_COM_ACTIVATION_NO_SERIAL_ACCESS'
    registry_roots = $registryRoots
    file_roots = $fileRoots
    registry_evidence = $registryEvidence
    binary_metadata = $binaryMetadata
    text_evidence = $textEvidence
    conclusions = [ordered]@{
        firmware_or_hardware_metadata_entries = $firmwareEvidence.Count
        sqm_metadata_entries = $sqmEvidence.Count
        device_connection_opened = $false
        com_object_activated = $false
        serial_port_opened = $false
        device_command_sent = $false
        configuration_changed = $false
        disposition = if ($sqmEvidence.Count -gt 0) { 'LOCAL_SQM_METADATA_FOUND_REQUIRES_SEMANTIC_REVIEW' } elseif ($firmwareEvidence.Count -gt 0) { 'LOCAL_HARDWARE_OR_FIRMWARE_METADATA_FOUND_REQUIRES_REVIEW' } else { 'NO_LOCAL_HARDWARE_FIRMWARE_OR_SQM_METADATA_FOUND' }
        note = 'Local metadata only. !4/LDR/brightness is never accepted as SQM. A !8 reference is only a capability clue until tied to the real installed hardware and a verified instrumental reading.'
    }
}

$jsonPath = Join-Path $bundle 'cloudwatcher-hardware-firmware-inventory.json'
$txtPath = Join-Path $bundle 'cloudwatcher-hardware-firmware-inventory.txt'
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== REGISTRY EVIDENCE ===',
    ($registryEvidence | Format-Table -AutoSize | Out-String),
    '=== BINARY VERSION METADATA ===',
    ($binaryMetadata | Format-Table -AutoSize | Out-String),
    '=== HARDWARE / FIRMWARE TEXT EVIDENCE ===',
    ($firmwareEvidence | Format-Table -Wrap -AutoSize | Out-String),
    '=== SQM TEXT EVIDENCE ===',
    ($sqmEvidence | Format-Table -Wrap -AutoSize | Out-String),
    '=== CONCLUSIONS ===',
    ($report.conclusions | Format-List | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== BINARY VERSION METADATA ==='
if ($binaryMetadata.Count -gt 0) { $binaryMetadata | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== HARDWARE / FIRMWARE METADATA ==='
Write-Output ('Entries: {0}' -f $firmwareEvidence.Count)
if ($firmwareEvidence.Count -gt 0) { $firmwareEvidence | Format-Table -Wrap -AutoSize | Out-String | Write-Output }
Write-Output '=== SQM METADATA ==='
Write-Output ('Entries: {0}' -f $sqmEvidence.Count)
if ($sqmEvidence.Count -gt 0) { $sqmEvidence | Format-Table -Wrap -AutoSize | Out-String | Write-Output }
Write-Output '=== DISPOSITION ==='
Write-Output $report.conclusions.disposition
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'CLOUDWATCHER HARDWARE/FIRMWARE INVENTORY RESULT: PASS (local metadata only; no device access)'
