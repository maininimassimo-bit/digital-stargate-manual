[CmdletBinding()]
param(
    [string]$ProjectionPath = 'C:\DigitalStarGate\TelemetryRuntime\observatory-status.json',
    [Parameter(Mandatory = $true)][string]$Endpoint,
    [string]$BearerToken = $env:DSG_TELEMETRY_INGEST_TOKEN,
    [ValidateRange(1, 120)][int]$TimeoutSeconds = 10,
    [ValidateRange(0, 5)][int]$MaxRetries = 2,
    [switch]$ValidateOnly,
    [bool]$RuntimeEnabled = $false
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $RuntimeEnabled) {
    throw 'Runtime disabled by contract: publication is blocked unless -RuntimeEnabled $true is explicitly supplied after the governed activation gate.'
}

function Test-Projection {
    param([Parameter(Mandatory = $true)]$Payload)

    if ([string]$Payload.schema_version -ne '1.1') { throw 'Projection schema_version must be 1.1.' }

    $safetyState = ([string]$Payload.safety.observed_state).Trim().ToUpperInvariant()
if ($safetyState -ne 'UNKNOWN') {
    throw 'Pilot publication requires safety.observed_state=UNKNOWN.'
}

    $safetyAuthority = ([string]$Payload.safety.authority).Trim().ToUpperInvariant()
    if ([string]::IsNullOrWhiteSpace($safetyAuthority)) { throw 'safety.authority is required.' }
if ($safetyAuthority -ne 'LOCAL_SAFETY_AUTHORITY') {
    throw 'Pilot publication requires safety.authority=LOCAL_SAFETY_AUTHORITY.'
}

    if ([string]::IsNullOrWhiteSpace([string]$Payload.correlation_id)) { throw 'correlation_id is required.' }

    $observed = [datetime]::Parse([string]$Payload.observed_at_utc, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
    $freshUntil = [datetime]::Parse([string]$Payload.fresh_until_utc, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
    if ($freshUntil -lt $observed) { throw 'fresh_until_utc precedes observed_at_utc.' }
    if ($freshUntil -lt [datetime]::UtcNow) { throw 'Projection is already stale; refusing publication.' }

    $guid = [guid]::Empty
    if (-not [guid]::TryParse([string]$Payload.correlation_id, [ref]$guid)) { throw 'correlation_id must be a UUID.' }
}

function Test-Endpoint {
    param([Parameter(Mandatory = $true)][uri]$Uri)
    if ($Uri.Scheme -eq 'https') { return }
    if ($Uri.Scheme -eq 'http' -and @('localhost','127.0.0.1','::1') -contains $Uri.Host) { return }
    throw 'Telemetry publication requires HTTPS; HTTP is allowed only for localhost integration testing.'
}

if (-not (Test-Path -LiteralPath $ProjectionPath -PathType Leaf)) { throw "Projection not found: $ProjectionPath" }
$uri = [uri]$Endpoint
Test-Endpoint -Uri $uri

$raw = Get-Content -LiteralPath $ProjectionPath -Raw
$payload = $raw | ConvertFrom-Json
Test-Projection -Payload $payload

if ($ValidateOnly) {
    Write-Output ('VALIDATION RESULT: PASS schema={0} safety={1}/{2} observed={3} fresh_until={4} correlation_id={5}' -f $payload.schema_version, $payload.safety.observed_state, $payload.safety.authority, $payload.observed_at_utc, $payload.fresh_until_utc, $payload.correlation_id)
    exit 0
}

if ([string]::IsNullOrWhiteSpace($BearerToken)) { throw 'DSG_TELEMETRY_INGEST_TOKEN/BearerToken is required for publication.' }

$headers = @{
    Authorization = "Bearer $BearerToken"
    'Idempotency-Key' = [string]$payload.correlation_id
}

$attempt = 0
while ($true) {
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri $uri -Method Post -Headers $headers -ContentType 'application/json' -Body $raw -TimeoutSec $TimeoutSeconds -UseBasicParsing
        if ($response.StatusCode -lt 200 -or $response.StatusCode -ge 300) { throw "Unexpected HTTP status $($response.StatusCode)." }
        Write-Output ('PUBLISH RESULT: PASS status={0} attempt={1} observed={2} correlation_id={3}' -f $response.StatusCode, $attempt, $payload.observed_at_utc, $payload.correlation_id)
        break
    }
    catch {
        $status = $null
        if ($_.Exception.Response) {
            try { $status = [int]$_.Exception.Response.StatusCode } catch { }
        }
        $transient = ($null -eq $status) -or $status -eq 408 -or $status -eq 429 -or $status -ge 500
        if (-not $transient -or $attempt -gt ($MaxRetries + 1)) { throw }
        $delay = [math]::Min(30, [math]::Pow(2, $attempt - 1))
        Start-Sleep -Seconds $delay
    }
}