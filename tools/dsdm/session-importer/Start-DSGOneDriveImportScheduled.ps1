[CmdletBinding()]
param(
    [string]$DiscoveryRoot = "$env:USERPROFILE\DSG-Inventory\SessionImporter",
    [string]$TransportRoot = 'C:\Users\MassimoMainini\OneDrive - Massimo Mainini\Manciano\DigitalStarGate-Transport',
    [string]$DestinationRoot = 'F:\Astrofotografia',
    [int]$MaxFilesPerRun = 10,
    [string]$EvidenceRoot = "$env:USERPROFILE\DSG-Inventory\OneDriveImport"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$importer = Join-Path $PSScriptRoot 'Start-DSGOneDriveImport.ps1'
if (-not (Test-Path -LiteralPath $importer -PathType Leaf)) {
    throw "Importer not found: $importer"
}
if (-not (Test-Path -LiteralPath $DiscoveryRoot -PathType Container)) {
    throw "Discovery root not found: $DiscoveryRoot"
}

$latestDiscovery = Get-ChildItem -LiteralPath $DiscoveryRoot -Directory |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'transfer-plan.csv') -PathType Leaf } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $latestDiscovery) {
    throw "No transfer-plan.csv found under discovery root: $DiscoveryRoot"
}

$transferPlanPath = Join-Path $latestDiscovery.FullName 'transfer-plan.csv'

& $importer `
    -TransferPlanPath $transferPlanPath `
    -TransportRoot $TransportRoot `
    -DestinationRoot $DestinationRoot `
    -MaxFilesPerRun $MaxFilesPerRun `
    -EvidenceRoot $EvidenceRoot
