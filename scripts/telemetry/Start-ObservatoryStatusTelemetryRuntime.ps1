[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$SecretPath = 'C:\DigitalStarGate\TelemetryRuntime\secrets\ingest-token.dpapi',
    [string]$PublishEndpoint = 'https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app/v1/observatory-status',
    [string]$NinaProjection = 'C:\Users\PrimaLuceLab\AppData\Local\DigitalStarGate\telemetry\nina-observatory-status.json',
    [ValidateRange(5,300)][int]$PollSeconds = 15,
    [ValidateRange(1,3600)][int]$FreshnessSeconds = 60
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Security

$producer = Join-Path $RepositoryRoot 'scripts\telemetry\Start-ObservatoryStatusTelemetryProducer.ps1'
if (-not (Test-Path -LiteralPath $producer -PathType Leaf)) { throw "Producer non trovato: $producer" }
if (-not (Test-Path -LiteralPath $SecretPath -PathType Leaf)) { throw "Secret DPAPI non trovato: $SecretPath" }
if (-not (Test-Path -LiteralPath $NinaProjection -PathType Leaf)) { throw "Projection NINA non trovata: $NinaProjection" }

$protected = [System.IO.File]::ReadAllBytes($SecretPath)
$plainBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
    $protected,
    $null,
    [System.Security.Cryptography.DataProtectionScope]::LocalMachine)

try {
    $env:DSG_TELEMETRY_INGEST_TOKEN = [System.Text.Encoding]::UTF8.GetString($plainBytes)
    if ([string]::IsNullOrWhiteSpace($env:DSG_TELEMETRY_INGEST_TOKEN)) { throw 'Token ingest decrittato vuoto.' }

    & $producer `
        -RepositoryRoot $RepositoryRoot `
        -NinaProjection $NinaProjection `
        -PollSeconds $PollSeconds `
        -FreshnessSeconds $FreshnessSeconds `
        -PublishEndpoint $PublishEndpoint
}
finally {
    if ($plainBytes) { [Array]::Clear($plainBytes, 0, $plainBytes.Length) }
    Remove-Item Env:\DSG_TELEMETRY_INGEST_TOKEN -ErrorAction SilentlyContinue
}
