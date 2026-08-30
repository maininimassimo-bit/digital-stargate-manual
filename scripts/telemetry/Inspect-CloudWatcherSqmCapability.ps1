[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [string]$CloudWatcherRoot = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-sqm-capability-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate CloudWatcher SQM capability inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)

function Get-SafePropertyValue {
    param(
        [Parameter(Mandatory = $true)][object]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) { return $null }
    return $property.Value
}

function Find-RelevantFiles {
    param([Parameter(Mandatory = $true)][string[]]$Roots)

    $results = New-Object System.Collections.Generic.List[object]
    foreach ($root in $Roots) {
        if ([string]::IsNullOrWhiteSpace($root) -or -not (Test-Path -LiteralPath $root)) { continue }
        try {
            Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction SilentlyContinue |
                Where-Object {
                    $_.Name -match '(?i)^(aag(_dat|_json)?|cloudwatcher|aagcw).*\.(json|dat|txt|csv|ini|cfg|config|xml)$' -or
                    $_.Name -match '(?i)(cloudwatcher|aag).*\.(exe|dll)$'
                } |
                Select-Object -First 200 |
                ForEach-Object {
                    $version = $null
                    if ($_.Extension -match '(?i)^\.(exe|dll)$') {
                        try { $version = $_.VersionInfo.FileVersion } catch { }
                    }
                    $results.Add([pscustomobject]@{
                        path = $_.FullName
                        extension = $_.Extension
                        size_bytes = $_.Length
                        last_write_time_utc = $_.LastWriteTimeUtc.ToString('o')
                        file_version = $version
                    })
                }
        }
        catch { }
    }
    return @($results)
}

function Inspect-StructuredFile {
    param([Parameter(Mandatory = $true)][string]$Path)

    $result = [ordered]@{
        path = $Path
        exists = [bool](Test-Path -LiteralPath $Path -PathType Leaf)
        sqm_candidate_fields = @()
        firmware_candidate_fields = @()
        metadata_candidate_fields = @()
        error = $null
    }
    if (-not $result.exists) { return [pscustomobject]$result }

    try {
        $raw = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop
        $sqmMatches = [regex]::Matches($raw, '(?im)\b(sqm|sky\s*quality|mpsas|mag(?:nitudes?)?\s*(?:per|/)\s*(?:square\s*)?arcsec(?:ond)?s?)\b') |
            ForEach-Object { $_.Value } | Sort-Object -Unique
        $firmwareMatches = [regex]::Matches($raw, '(?im)\b(firmware|fw\s*version|device\s*version|serial\s*number|hardware\s*version)\b') |
            ForEach-Object { $_.Value } | Sort-Object -Unique
        $metadataMatches = [regex]::Matches($raw, '(?im)\b(model|device|version|serial|sensor|light|darkness|reference)\b') |
            ForEach-Object { $_.Value } | Sort-Object -Unique
        $result.sqm_candidate_fields = @($sqmMatches)
        $result.firmware_candidate_fields = @($firmwareMatches)
        $result.metadata_candidate_fields = @($metadataMatches)
    }
    catch {
        $result.error = $_.Exception.Message
    }
    return [pscustomobject]$result
}

$registryRoot = 'Registry::HKEY_CURRENT_USER\Software\VB and VBA Program Settings\AAG_CloudWatcher'
$registryEvidence = @()
if (Test-Path -LiteralPath $registryRoot) {
    try {
        $registryEvidence = @(Get-ChildItem -LiteralPath $registryRoot -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
            $item = Get-ItemProperty -LiteralPath $_.PSPath -ErrorAction SilentlyContinue
            if (-not $item) { return }
            $pairs = @()
            foreach ($property in $item.PSObject.Properties) {
                if ($property.Name -match '^PS(Path|ParentPath|ChildName|Drive|Provider)$') { continue }
                if ($property.Name -match '(?i)(password|secret|token|credential|community|key)') { continue }
                if ($property.Name -notmatch '(?i)(port|com|mode|path|file|json|version|firmware|serial|device|sensor|light|dark|reference|sqm|quality)') { continue }
                $pairs += [pscustomobject]@{ name = $property.Name; value = [string]$property.Value }
            }
            if ($pairs.Count -gt 0) {
                [pscustomobject]@{ registry_path = $_.PSPath; values = $pairs }
            }
        })
    }
    catch { }
}

$uninstallRoots = @(
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'Registry::HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
)

$installedSoftware = @($uninstallRoots | ForEach-Object {
    Get-ItemProperty -Path $_ -ErrorAction SilentlyContinue
} | Where-Object {
    $name = Get-SafePropertyValue -Object $_ -Name 'DisplayName'
    $name -and ([string]$name -match '(?i)CloudWatcher|AAG|Lunatico')
} | ForEach-Object {
    [pscustomobject]@{
        display_name = [string](Get-SafePropertyValue -Object $_ -Name 'DisplayName')
        display_version = [string](Get-SafePropertyValue -Object $_ -Name 'DisplayVersion')
        publisher = [string](Get-SafePropertyValue -Object $_ -Name 'Publisher')
        install_location = [string](Get-SafePropertyValue -Object $_ -Name 'InstallLocation')
    }
})

$searchRoots = @(
    $CloudWatcherRoot,
    'C:\Program Files',
    'C:\Program Files (x86)',
    (Join-Path $env:APPDATA 'Lunatico'),
    (Join-Path $env:LOCALAPPDATA 'Lunatico'),
    (Join-Path $env:APPDATA 'AAG_CloudWatcher'),
    (Join-Path $env:LOCALAPPDATA 'AAG_CloudWatcher')
)

$files = @(Find-RelevantFiles -Roots $searchRoots)
$structuredCandidates = @($files | Where-Object { $_.extension -match '(?i)^\.(json|dat|txt|csv|ini|cfg|config|xml)$' })
$structuredEvidence = @()
foreach ($candidate in $structuredCandidates) {
    $structuredEvidence += Inspect-StructuredFile -Path $candidate.path
}

$comRegistration = @()
foreach ($progId in @('AAG_CloudWatcher.CloudWatcher','ASCOM.AAGCloudWatcher.ObservingConditions','ASCOM.Lunatico.ObservingConditions')) {
    try {
        $type = [type]::GetTypeFromProgID($progId)
        $comRegistration += [pscustomobject]@{ prog_id = $progId; registered = [bool]$type }
    }
    catch {
        $comRegistration += [pscustomobject]@{ prog_id = $progId; registered = $false }
    }
}

$sqmFiles = @($structuredEvidence | Where-Object { @($_.sqm_candidate_fields).Count -gt 0 })
$firmwareFiles = @($structuredEvidence | Where-Object { @($_.firmware_candidate_fields).Count -gt 0 })

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.CloudWatcherSqmCapabilityInspector'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = 'READ_ONLY_PASSIVE_NO_DEVICE_CONNECTION_NO_CONFIGURATION_CHANGE'
    registry = [ordered]@{
        root = $registryRoot
        present = [bool](Test-Path -LiteralPath $registryRoot)
        relevant_values = $registryEvidence
    }
    installed_software = $installedSoftware
    com_registration = $comRegistration
    relevant_files = $files
    structured_file_evidence = $structuredEvidence
    conclusions = [ordered]@{
        sqm_evidence_file_count = $sqmFiles.Count
        firmware_metadata_file_count = $firmwareFiles.Count
        cloudwatcher_legacy_com_registered = [bool](@($comRegistration | Where-Object { $_.prog_id -eq 'AAG_CloudWatcher.CloudWatcher' -and $_.registered }).Count -gt 0)
        sqm_capability_verified = $false
        disposition = if ($sqmFiles.Count -gt 0) { 'SQM_METADATA_OR_FIELD_FOUND_REQUIRES_CONTENT_REVIEW' } elseif ($firmwareFiles.Count -gt 0) { 'FIRMWARE_METADATA_FOUND_REQUIRES_CONTENT_REVIEW' } else { 'NO_PASSIVE_SQM_OR_FIRMWARE_METADATA_FOUND' }
        configuration_changed = $false
        device_connection_opened = $false
        device_command_sent = $false
        note = 'Passive inspection only. No SQM value is inferred from brightness/LDR. Firmware/hardware capability remains unverified until explicit evidence is reviewed.'
    }
}

$jsonPath = Join-Path $bundle 'cloudwatcher-sqm-capability.json'
$txtPath = Join-Path $bundle 'cloudwatcher-sqm-capability.txt'
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== INSTALLED SOFTWARE ===',
    ($installedSoftware | Format-Table -AutoSize | Out-String),
    '=== COM REGISTRATION ===',
    ($comRegistration | Format-Table -AutoSize | Out-String),
    '=== CLOUDWATCHER REGISTRY SETTINGS (FILTERED) ===',
    ($registryEvidence | Format-List | Out-String),
    '=== RELEVANT FILES ===',
    ($files | Format-Table -AutoSize | Out-String),
    '=== STRUCTURED FILES WITH SQM TERMS ===',
    ($sqmFiles | Format-List | Out-String),
    '=== STRUCTURED FILES WITH FIRMWARE TERMS ===',
    ($firmwareFiles | Format-List | Out-String),
    '=== CONCLUSIONS ===',
    ($report.conclusions | Format-List | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== INSTALLED CLOUDWATCHER/LUNATICO SOFTWARE ==='
if ($installedSoftware.Count -gt 0) { $installedSoftware | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found in uninstall registry)' }
Write-Output '=== COM REGISTRATION ==='
$comRegistration | Format-Table -AutoSize | Out-String | Write-Output
Write-Output '=== PASSIVE SQM / FIRMWARE EVIDENCE ==='
Write-Output ('SQM evidence files: {0}' -f $sqmFiles.Count)
Write-Output ('Firmware metadata files: {0}' -f $firmwareFiles.Count)
if ($sqmFiles.Count -gt 0) { $sqmFiles | Select-Object path,sqm_candidate_fields | Format-List | Out-String | Write-Output }
if ($firmwareFiles.Count -gt 0) { $firmwareFiles | Select-Object path,firmware_candidate_fields | Format-List | Out-String | Write-Output }
Write-Output '=== DISPOSITION ==='
Write-Output $report.conclusions.disposition
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'CLOUDWATCHER SQM CAPABILITY INSPECTION RESULT: PASS (passive evidence only; capability not yet verified)'
