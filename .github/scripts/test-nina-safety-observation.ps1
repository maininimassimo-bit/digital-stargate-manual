[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoryRoot,

    [string]$NinaProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\nina-observatory-status.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$adapter = Join-Path $RepositoryRoot 'scripts\telemetry\Export-NinaObservatoryStatus.ps1'
$publisher = Join-Path $RepositoryRoot 'scripts\telemetry\Publish-ObservatoryStatusTelemetry.ps1'
$schemaPath = Join-Path $RepositoryRoot 'contracts\telemetry\observatory-status-v1.schema.json'
$temp = Join-Path ([IO.Path]::GetTempPath()) ('dsg-nina-safety-test-' + [guid]::NewGuid().ToString('N'))

if (-not (Test-Path -LiteralPath $adapter -PathType Leaf)) { throw "Adapter non trovato: $adapter" }
if (-not (Test-Path -LiteralPath $publisher -PathType Leaf)) { throw "Publisher non trovato: $publisher" }
if (-not (Test-Path -LiteralPath $schemaPath -PathType Leaf)) { throw "Schema non trovato: $schemaPath" }

New-Item -ItemType Directory -Path $temp -Force | Out-Null

try {
    $schema = Get-Content $schemaPath -Raw | ConvertFrom-Json

    if (-not $schema.'$defs'.safetyObservation) {
        throw 'Schema safetyObservation mancante.'
    }

    if (-not $schema.properties.safety.properties.observation) {
        throw 'Schema safety.observation mancante.'
    }

    $currentOutput = Join-Path $temp 'current.json'

    & $adapter -NinaProjection $NinaProjection -OutputPath $currentOutput -FreshnessSeconds 300 -SourceInstance 'CI'

    $current = Get-Content $currentOutput -Raw | ConvertFrom-Json

    if ($current.safety.observed_state -ne 'UNKNOWN') { throw 'Overall safety deve restare UNKNOWN.' }
    if ($current.safety.authority -ne 'LOCAL_SAFETY_AUTHORITY') { throw 'Safety authority deve restare locale.' }
    if ($current.safety.observation.source -ne 'NINA_SAFETY_MONITOR') { throw 'Fonte NINA SafetyMonitor mancante.' }
    if ($current.safety.observation.no_hardware_commands -ne $true) { throw 'Command-path invariant fallito.' }

    $source = Get-Content $NinaProjection -Raw | ConvertFrom-Json
    $source.observedAtUtc = '2020-01-01T00:00:00Z'

    $staleProjection = Join-Path $temp 'stale-projection.json'
    $staleOutput = Join-Path $temp 'stale.json'

    $source | ConvertTo-Json -Depth 20 | Set-Content $staleProjection -Encoding UTF8

    & $adapter -NinaProjection $staleProjection -OutputPath $staleOutput -FreshnessSeconds 300 -SourceInstance 'CI-STALE'

    $stale = Get-Content $staleOutput -Raw | ConvertFrom-Json

    if ($stale.quality -ne 'STALE') { throw 'Projection stale non classificata STALE.' }
    if ($stale.safety.observed_state -ne 'UNKNOWN') { throw 'Safety stale deve essere UNKNOWN.' }
    if ($stale.safety.observation.state -ne 'UNKNOWN') { throw 'Observation stale deve essere UNKNOWN.' }

    $publisherText = Get-Content $publisher -Raw

    if ($publisherText -notmatch 'Pilot publication requires safety') {
        throw 'Guard fail-closed publisher mancante.'
    }

    Write-Output 'NINA SafetyMonitor observational integration tests: PASS'
}
finally {
    Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
}
