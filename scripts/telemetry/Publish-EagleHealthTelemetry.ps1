[CmdletBinding()]
param(
    [string]$ProjectionPath = (Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\eagle-health-public.json'),
    [Parameter(Mandatory = $true)][string]$Endpoint,
    [string]$BearerToken = $env:DSG_TELEMETRY_INGEST_TOKEN,
    [ValidateRange(1,120)][int]$TimeoutSeconds = 10,
    [ValidateRange(0,5)][int]$MaxRetries = 2,
    [switch]$ValidateOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-Endpoint([uri]$Uri) {
    if ($Uri.Scheme -eq 'https') { return }
    if ($Uri.Scheme -eq 'http' -and @('localhost','127.0.0.1','::1') -contains $Uri.Host) { return }
    throw 'EAGLE health publication requires HTTPS; HTTP is allowed only for localhost integration testing.'
}

function Test-Projection($Payload) {
    if ([string]$Payload.schema_version -ne '1.0') { throw 'schema_version must be 1.0.' }
    if ([string]$Payload.component -ne 'DSG.EagleHealthPortalProjection') { throw 'Invalid component.' }
    if ([string]$Payload.host -ne $env:COMPUTERNAME) { throw 'Projection host must match local computer.' }
    if ([string]$Payload.source_component -ne 'DSG.EagleHostHealthCollector') { throw 'Invalid source_component.' }
    if ([string]$Payload.summary.state -ne 'UNKNOWN' -or [string]$Payload.summary.reason -ne 'POLICY_NOT_ACTIVATED') { throw 'Health policy must remain UNKNOWN/POLICY_NOT_ACTIVATED.' }
    if ([string]$Payload.diagnostics.projection_mode -ne 'READ_ONLY_PUBLIC') { throw 'Projection must be READ_ONLY_PUBLIC.' }
    if ([bool]$Payload.diagnostics.automatic_remediation) { throw 'Automatic remediation must remain false.' }
    if ([string]$Payload.diagnostics.safety_authority -ne 'OUTSIDE_SCOPE') { throw 'Safety Authority must remain outside scope.' }
    if ([string]::IsNullOrWhiteSpace([string]$Payload.source_correlation_id)) { throw 'source_correlation_id is required.' }

    $observed = [datetime]::Parse([string]$Payload.observed_at_utc, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
    $freshUntil = [datetime]::Parse([string]$Payload.fresh_until_utc, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
    if ($freshUntil -lt $observed) { throw 'fresh_until_utc precedes observed_at_utc.' }
    if ($freshUntil -lt [datetime]::UtcNow) { throw 'Projection is already stale; refusing publication.' }
}

if (-not (Test-Path -LiteralPath $ProjectionPath -PathType Leaf)) { throw "Projection not found: $ProjectionPath" }
$uri = [uri]$Endpoint
Test-Endpoint $uri
$raw = Get-Content -LiteralPath $ProjectionPath -Raw
$payload = $raw | ConvertFrom-Json
Test-Projection $payload

if ($ValidateOnly) {
    Write-Output ('VALIDATION RESULT: PASS component={0} host={1} observed={2} fresh_until={3} correlation_id={4}' -f $payload.component,$payload.host,$payload.observed_at_utc,$payload.fresh_until_utc,$payload.source_correlation_id)
    exit 0
}

if ([string]::IsNullOrWhiteSpace($BearerToken)) { throw 'DSG_TELEMETRY_INGEST_TOKEN/BearerToken is required for publication.' }
$headers = @{ Authorization="Bearer $BearerToken"; 'Idempotency-Key'=[string]$payload.source_correlation_id }

$attempt = 0
while ($true) {
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri $uri -Method Post -Headers $headers -ContentType 'application/json' -Body $raw -TimeoutSec $TimeoutSeconds -UseBasicParsing
        if ($response.StatusCode -lt 200 -or $response.StatusCode -ge 300) { throw "Unexpected HTTP status $($response.StatusCode)." }
        Write-Output ('PUBLISH RESULT: PASS status={0} attempt={1} observed={2} correlation_id={3}' -f $response.StatusCode,$attempt,$payload.observed_at_utc,$payload.source_correlation_id)
        break
    }
    catch {
        $status = $null
        if ($_.Exception.Response) { try { $status = [int]$_.Exception.Response.StatusCode } catch {} }
        $transient = ($null -eq $status) -or $status -eq 408 -or $status -eq 429 -or $status -ge 500
        if (-not $transient -or $attempt -gt ($MaxRetries + 1)) { throw }
        Start-Sleep -Seconds ([math]::Min(30,[math]::Pow(2,$attempt-1)))
    }
}
