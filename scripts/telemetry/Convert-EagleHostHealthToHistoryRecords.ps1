[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$InputPath,
    [string]$OutputPath
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Get-Sha256Hex([string]$Text) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Text)
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally { $sha.Dispose() }
}

function Assert-Projection([object]$Projection) {
    if ($null -eq $Projection) { throw 'Projection is null.' }
    if ([string]$Projection.schema_version -ne '1.0') { throw 'Unsupported projection schema_version.' }
    if ([string]$Projection.component -ne 'DSG.EagleHostHealthCollector') { throw 'Invalid projection component.' }
    if ([string]$Projection.diagnostics.collector_mode -ne 'READ_ONLY') { throw 'Projection collector_mode must be READ_ONLY.' }
    if ($null -eq $Projection.signals) { throw 'Projection signals missing.' }
    if ([string]::IsNullOrWhiteSpace([string]$Projection.computer)) { throw 'Projection computer missing.' }
}

if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) { throw "Input projection not found: $InputPath" }

$projection = Get-Content -LiteralPath $InputPath -Raw | ConvertFrom-Json -ErrorAction Stop
Assert-Projection $projection

$records = @()
foreach ($property in $projection.signals.PSObject.Properties | Sort-Object Name) {
    $signalId = [string]$property.Name
    $signal = $property.Value
    if ($null -eq $signal) { throw "Signal '$signalId' is null." }

    $observedAt = [string]$signal.observed_at_utc
    $source = [string]$signal.source
    if ([string]::IsNullOrWhiteSpace($observedAt)) { throw "Signal '$signalId' observed_at_utc missing." }
    if ([string]::IsNullOrWhiteSpace($source)) { throw "Signal '$signalId' source missing." }

    $identityMaterial = ([string]$projection.computer) + '|' + $signalId + '|' + $observedAt + '|' + $source
    $recordId = Get-Sha256Hex $identityMaterial

    $records += [pscustomobject][ordered]@{
        history_schema_version = '1.0'
        record_id = $recordId
        host = [string]$projection.computer
        component = [string]$projection.component
        projection_schema_version = [string]$projection.schema_version
        projection_correlation_id = [string]$projection.correlation_id
        projection_observed_at_utc = [string]$projection.observed_at_utc
        signal_id = $signalId
        signal_state = [string]$signal.state
        quality = [string]$signal.quality
        observed_at_utc = $observedAt
        fresh_until_utc = [string]$signal.fresh_until_utc
        source = $source
        cadence_class = [string]$signal.cadence_class
        reason = $signal.reason
        data = $signal.data
        retention_deletion_enabled = $false
        historical_records_deleted = 0
    }
}

if (-not [string]::IsNullOrWhiteSpace($OutputPath)) {
    $parent = Split-Path -Parent $OutputPath
    if (-not [string]::IsNullOrWhiteSpace($parent) -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $lines = @($records | ForEach-Object { $_ | ConvertTo-Json -Depth 12 -Compress })
    [IO.File]::WriteAllLines($OutputPath, $lines, (New-Object Text.UTF8Encoding($false)))
}

$records
