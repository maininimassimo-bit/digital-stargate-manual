[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$RuntimeRoot = 'C:\DigitalStarGate\TelemetryRuntime',
    [string]$RelayRoot = 'C:\DigitalStarGate\TelemetryRelay',
    [string]$Endpoint = 'http://127.0.0.1:8765/v1/observatory-status',
    [string]$BearerToken = 'dsg-localhost-pilot-token'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$publisher = Join-Path $RepositoryRoot 'scripts\telemetry\Publish-ObservatoryStatusTelemetry.ps1'
$projection = Join-Path $RuntimeRoot 'observatory-status.json'
if (-not (Test-Path -LiteralPath $publisher -PathType Leaf)) { throw "Publisher not found: $publisher" }
if (-not (Test-Path -LiteralPath $projection -PathType Leaf)) { throw "Projection not found: $projection" }

Write-Output 'Digital StarGate Telemetry Relay E2E smoke test'

& $publisher -ProjectionPath $projection -Endpoint $Endpoint -BearerToken $BearerToken -MaxRetries 0

$received = Invoke-WebRequest -Uri $Endpoint -Method Get -UseBasicParsing -TimeoutSec 5
if ($received.StatusCode -ne 200) { throw "GET returned $($received.StatusCode)" }
$payload = $received.Content | ConvertFrom-Json
$source = Get-Content -LiteralPath $projection -Raw | ConvertFrom-Json

if ([string]$payload.correlation_id -ne [string]$source.correlation_id) { throw 'Relay correlation_id differs from local projection.' }
if ([string]$payload.observed_at_utc -ne [string]$source.observed_at_utc) { throw 'Relay observed_at_utc differs from local projection.' }
if ([string]$payload.safety.observed_state -ne 'UNKNOWN') { throw 'Relay changed the safety invariant.' }

$healthUri = ([uri]$Endpoint).GetLeftPart([System.UriPartial]::Authority) + '/health'
$healthResponse = Invoke-WebRequest -Uri $healthUri -Method Get -UseBasicParsing -TimeoutSec 5
$health = $healthResponse.Content | ConvertFrom-Json
if ([int]$health.accepted_requests -lt 1) { throw 'Relay health does not report an accepted request.' }

Write-Output ('E2E RESULT: PASS status={0} observed={1} correlation_id={2} accepted={3}' -f $received.StatusCode, $payload.observed_at_utc, $payload.correlation_id, $health.accepted_requests)
Write-Output ('Relay store: {0}' -f $RelayRoot)
