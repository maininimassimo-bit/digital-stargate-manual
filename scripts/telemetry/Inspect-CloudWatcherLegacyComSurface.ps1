[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [string]$ProgId = 'AAG_CloudWatcher.CloudWatcher'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-legacy-com-surface-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate CloudWatcher legacy COM surface inspector - READ ONLY / NO COM ACTIVATION'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('ProgID: {0}' -f $ProgId)
Write-Output ('Evidence bundle: {0}' -f $bundle)

function Get-RegistryDefaultValue {
    param([Parameter(Mandatory = $true)][string]$Path)
    try {
        $item = Get-Item -LiteralPath $Path -ErrorAction Stop
        return [string]$item.GetValue('')
    }
    catch { return $null }
}

function Get-RegistryNamedValues {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    try {
        $item = Get-Item -LiteralPath $Path -ErrorAction Stop
        $values = @()
        foreach ($name in $item.GetValueNames()) {
            if ($name -match '(?i)(password|secret|token|credential|community|key)') { continue }
            $values += [pscustomobject]@{
                name = if ([string]::IsNullOrEmpty($name)) { '(Default)' } else { $name }
                value = [string]$item.GetValue($name)
            }
        }
        return @($values)
    }
    catch { return @() }
}

$classesRoots = @(
    'Registry::HKEY_CLASSES_ROOT',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Classes',
    'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Classes'
)

$registrations = @()
foreach ($root in $classesRoots) {
    $progPath = Join-Path $root $ProgId
    if (-not (Test-Path -LiteralPath $progPath)) { continue }

    $clsidPath = Join-Path $progPath 'CLSID'
    $clsid = Get-RegistryDefaultValue -Path $clsidPath
    $registration = [ordered]@{
        root = $root
        prog_id_path = $progPath
        prog_id_description = Get-RegistryDefaultValue -Path $progPath
        clsid = $clsid
        clsid_path = $null
        inproc_server32 = $null
        local_server32 = $null
        threading_model = $null
        typelib = $null
        version = $null
        prog_id_values = Get-RegistryNamedValues -Path $progPath
    }

    if (-not [string]::IsNullOrWhiteSpace($clsid)) {
        $classPath = Join-Path $root ("CLSID\{0}" -f $clsid)
        $registration.clsid_path = $classPath
        $inprocPath = Join-Path $classPath 'InprocServer32'
        $localServerPath = Join-Path $classPath 'LocalServer32'
        $typeLibPath = Join-Path $classPath 'TypeLib'
        $versionPath = Join-Path $classPath 'Version'
        $registration.inproc_server32 = Get-RegistryDefaultValue -Path $inprocPath
        $registration.local_server32 = Get-RegistryDefaultValue -Path $localServerPath
        $registration.typelib = Get-RegistryDefaultValue -Path $typeLibPath
        $registration.version = Get-RegistryDefaultValue -Path $versionPath
        if (Test-Path -LiteralPath $inprocPath) {
            try {
                $item = Get-Item -LiteralPath $inprocPath -ErrorAction Stop
                $registration.threading_model = [string]$item.GetValue('ThreadingModel')
            }
            catch { }
        }
    }

    $registrations += [pscustomobject]$registration
}

$typeLibEvidence = @()
foreach ($registration in $registrations) {
    if ([string]::IsNullOrWhiteSpace([string]$registration.typelib)) { continue }
    foreach ($root in $classesRoots) {
        $typeLibRoot = Join-Path $root ("TypeLib\{0}" -f $registration.typelib)
        if (-not (Test-Path -LiteralPath $typeLibRoot)) { continue }
        try {
            Get-ChildItem -LiteralPath $typeLibRoot -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
                $default = Get-RegistryDefaultValue -Path $_.PSPath
                if ([string]::IsNullOrWhiteSpace($default)) { return }
                if ($default -match '(?i)(AAG|CloudWatcher|SQM|sky\s*quality|mpsas|light|dark|brightness|version|serial|firmware)') {
                    $typeLibEvidence += [pscustomobject]@{
                        registry_path = $_.PSPath
                        default_value = $default
                    }
                }
            }
        }
        catch { }
    }
}

$serverFiles = @($registrations | ForEach-Object {
    @($_.inproc_server32, $_.local_server32)
} | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } | Sort-Object -Unique | ForEach-Object {
    $path = ([string]$_).Trim('"')
    $exists = Test-Path -LiteralPath $path -PathType Leaf
    $fileVersion = $null
    $productVersion = $null
    if ($exists) {
        try {
            $info = (Get-Item -LiteralPath $path -ErrorAction Stop).VersionInfo
            $fileVersion = $info.FileVersion
            $productVersion = $info.ProductVersion
        }
        catch { }
    }
    [pscustomobject]@{
        path = $path
        exists = [bool]$exists
        file_version = $fileVersion
        product_version = $productVersion
    }
})

$sqmRegistryEvidence = @($typeLibEvidence | Where-Object { $_.default_value -match '(?i)(SQM|sky\s*quality|mpsas)' })

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.CloudWatcherLegacyComSurfaceInspector'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = 'READ_ONLY_REGISTRY_AND_FILE_METADATA_NO_COM_ACTIVATION'
    prog_id = $ProgId
    registrations = $registrations
    typelib_evidence = $typeLibEvidence
    server_files = $serverFiles
    conclusions = [ordered]@{
        registration_found = [bool]($registrations.Count -gt 0)
        sqm_registry_or_typelib_term_found = [bool]($sqmRegistryEvidence.Count -gt 0)
        com_object_activated = $false
        device_connection_opened = $false
        device_command_sent = $false
        configuration_changed = $false
        disposition = if ($sqmRegistryEvidence.Count -gt 0) { 'SQM_TERM_FOUND_IN_REGISTERED_COM_METADATA_REQUIRES_SEMANTIC_REVIEW' } elseif ($registrations.Count -gt 0) { 'LEGACY_COM_REGISTERED_NO_SQM_TERM_FOUND_IN_PASSIVE_METADATA' } else { 'LEGACY_COM_REGISTRATION_NOT_FOUND' }
        note = 'This inspector never activates the COM class. Absence of SQM terms in registry/type-library metadata does not prove that the device firmware lacks SQM; it only constrains the registered software surface visible without activation.'
    }
}

$jsonPath = Join-Path $bundle 'cloudwatcher-legacy-com-surface.json'
$txtPath = Join-Path $bundle 'cloudwatcher-legacy-com-surface.txt'
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== REGISTRATIONS ===',
    ($registrations | Format-List | Out-String),
    '=== TYPELIB EVIDENCE ===',
    ($typeLibEvidence | Format-Table -AutoSize | Out-String),
    '=== SERVER FILES ===',
    ($serverFiles | Format-Table -AutoSize | Out-String),
    '=== CONCLUSIONS ===',
    ($report.conclusions | Format-List | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== LEGACY COM REGISTRATION ==='
if ($registrations.Count -gt 0) { $registrations | Select-Object root,prog_id_description,clsid,inproc_server32,local_server32,typelib,version | Format-List | Out-String | Write-Output } else { Write-Output '(registration not found)' }
Write-Output '=== SERVER FILE METADATA ==='
if ($serverFiles.Count -gt 0) { $serverFiles | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(no registered server file resolved)' }
Write-Output '=== PASSIVE TYPELIB / SQM EVIDENCE ==='
Write-Output ('TypeLib evidence entries: {0}' -f $typeLibEvidence.Count)
Write-Output ('SQM-related entries: {0}' -f $sqmRegistryEvidence.Count)
if ($sqmRegistryEvidence.Count -gt 0) { $sqmRegistryEvidence | Format-Table -AutoSize | Out-String | Write-Output }
Write-Output '=== DISPOSITION ==='
Write-Output $report.conclusions.disposition
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'CLOUDWATCHER LEGACY COM SURFACE INSPECTION RESULT: PASS (no COM activation)'
