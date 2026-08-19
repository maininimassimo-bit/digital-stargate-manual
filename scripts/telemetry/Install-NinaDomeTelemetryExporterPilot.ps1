[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$ArtifactDll,

    [string]$ExpectedSha256 = '6c59ab0decb975bd96ea03581ddb674cf1ea08abb9bf77597be5af2dc031bdee',

    [string]$NinaPluginVersionDirectory = '3.0.0'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate NINA Observatory Telemetry Exporter - PILOT INSTALLER'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)

$nina = @(Get-Process -Name NINA -ErrorAction SilentlyContinue)
if ($nina.Count -gt 0) {
    throw 'NINA is running. Close NINA before installing or replacing the pilot plugin.'
}

if (-not (Test-Path -LiteralPath $ArtifactDll -PathType Leaf)) {
    throw "Artifact DLL not found: $ArtifactDll"
}

$actualHash = (Get-FileHash -LiteralPath $ArtifactDll -Algorithm SHA256).Hash.ToLowerInvariant()
$expectedHash = $ExpectedSha256.ToLowerInvariant()
Write-Output ('Artifact SHA256: {0}' -f $actualHash)
if ($actualHash -ne $expectedHash) {
    throw "Artifact SHA256 mismatch. Expected $expectedHash"
}

$pluginRoot = Join-Path $env:LOCALAPPDATA 'NINA\Plugins'
$versionedRoot = Join-Path $pluginRoot $NinaPluginVersionDirectory
$pluginDir = Join-Path $versionedRoot 'Digital StarGate Dome Telemetry Exporter'
$targetDll = Join-Path $pluginDir 'DigitalStarGate.Nina.DomeTelemetryExporter.dll'
$legacyPluginDir = Join-Path $pluginRoot 'Digital StarGate Dome Telemetry Exporter'
$legacyDll = Join-Path $legacyPluginDir 'DigitalStarGate.Nina.DomeTelemetryExporter.dll'
$backupRoot = Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\plugin-backups'
$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')

New-Item -ItemType Directory -Path $pluginDir -Force | Out-Null
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

if (Test-Path -LiteralPath $targetDll -PathType Leaf) {
    $backup = Join-Path $backupRoot ("DigitalStarGate.Nina.DomeTelemetryExporter.versioned.{0}.dll" -f $stamp)
    Copy-Item -LiteralPath $targetDll -Destination $backup -Force
    Write-Output ('Previous versioned plugin backed up to: {0}' -f $backup)
}

if (Test-Path -LiteralPath $legacyDll -PathType Leaf) {
    $legacyBackup = Join-Path $backupRoot ("DigitalStarGate.Nina.DomeTelemetryExporter.legacy-root.{0}.dll" -f $stamp)
    Copy-Item -LiteralPath $legacyDll -Destination $legacyBackup -Force
    Write-Output ('Legacy root plugin backed up to: {0}' -f $legacyBackup)
    Remove-Item -LiteralPath $legacyDll -Force
    try {
        if ((Get-ChildItem -LiteralPath $legacyPluginDir -Force -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) {
            Remove-Item -LiteralPath $legacyPluginDir -Force
        }
    } catch { }
}

Copy-Item -LiteralPath $ArtifactDll -Destination $targetDll -Force
try { Unblock-File -LiteralPath $targetDll -ErrorAction SilentlyContinue } catch { }

$installedHash = (Get-FileHash -LiteralPath $targetDll -Algorithm SHA256).Hash.ToLowerInvariant()
if ($installedHash -ne $expectedHash) {
    throw 'Installed DLL hash does not match expected commissioning artifact.'
}

Write-Output ('NINA plugin version directory: {0}' -f $NinaPluginVersionDirectory)
Write-Output ('Installed: {0}' -f $targetDll)
Write-Output ('Installed SHA256: {0}' -f $installedHash)
Write-Output 'No NINA process was started. No equipment connection was opened. No device command was sent.'
Write-Output 'PILOT INSTALL RESULT: PASS'
