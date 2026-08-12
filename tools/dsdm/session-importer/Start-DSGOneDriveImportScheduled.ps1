[CmdletBinding()]
param(
    [string]$DiscoveryRoot = "$env:USERPROFILE\DSG-Inventory\SessionImporter",
    [string]$DiscoveryConfigurationPath = "$env:USERPROFILE\DSG-Inventory\SessionImporter\session-importer.production.json",
    [string]$TransportRoot = 'C:\Users\MassimoMainini\OneDrive - Massimo Mainini\Manciano\DigitalStarGate-Transport',
    [string]$DestinationRoot = 'F:\Astrofotografia',
    [int]$MaxFilesPerRun = 10,
    [string]$EvidenceRoot = "$env:USERPROFILE\DSG-Inventory\OneDriveImport"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$importer = Join-Path $PSScriptRoot 'Start-DSGOneDriveImport.ps1'
$discovery = Join-Path $PSScriptRoot 'Invoke-DSGSessionDiscovery.ps1'

if (-not (Test-Path -LiteralPath $importer -PathType Leaf)) {
    throw "Importer not found: $importer"
}
if (-not (Test-Path -LiteralPath $discovery -PathType Leaf)) {
    throw "Discovery script not found: $discovery"
}
if (-not (Test-Path -LiteralPath $DiscoveryConfigurationPath -PathType Leaf)) {
    throw "Discovery configuration not found: $DiscoveryConfigurationPath"
}
if (-not (Test-Path -LiteralPath $TransportRoot -PathType Container)) {
    throw "Transport root not found: $TransportRoot"
}

New-Item -ItemType Directory -Path $DiscoveryRoot -Force | Out-Null

# Fail-safe rule: every scheduled import run must refresh discovery from the
# locally synchronized transport. A stale plan is never reused if discovery
# cannot complete successfully.
& $discovery `
    -ConfigurationPath $DiscoveryConfigurationPath `
    -SourcePath $TransportRoot `
    -OutputRoot $DiscoveryRoot `
    -IgnoreOperatingWindow |
    Out-Host

$latestDiscovery = Get-ChildItem -LiteralPath $DiscoveryRoot -Directory |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'transfer-plan.csv') -PathType Leaf } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $latestDiscovery) {
    throw "No transfer-plan.csv found after discovery under: $DiscoveryRoot"
}

$transferPlanPath = Join-Path $latestDiscovery.FullName 'transfer-plan.csv'

& $importer `
    -TransferPlanPath $transferPlanPath `
    -TransportRoot $TransportRoot `
    -DestinationRoot $DestinationRoot `
    -MaxFilesPerRun $MaxFilesPerRun `
    -EvidenceRoot $EvidenceRoot
