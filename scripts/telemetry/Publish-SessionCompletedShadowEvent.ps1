[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$EventPath,
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
    throw 'SessionCompleted publication requires HTTPS; HTTP is allowed only for localhost integration testing.'
}

function Test-SessionCompletedShadow($Event) {
    if ([string]$Event.contract_id -ne 'DSG.Observation.Event.SessionCompleted') { throw 'Invalid contract_id.' }
    if ([string]$Event.contract_version -ne '1.0.0') { throw 'Unsupported contract_version.' }
    if ([string]$Event.producer.instance -ne $env:COMPUTERNAME) { throw 'Producer instance must match local computer.' }
    if ([string]$Event.producer.mode -ne 'shadow') { throw 'Only shadow transport is enabled.' }
    if ([string]$Event.activation_mode -ne 'shadow') { throw 'activation_mode must remain shadow.' }
    if ([bool]$Event.runtime_event_published) { throw 'runtime_event_published must remain false.' }
    if ([string]$Event.safety_authority -ne 'NONE') { throw 'safety_authority must remain NONE.' }
    if ([string]$Event.command_authority -ne 'NONE') { throw 'command_authority must remain NONE.' }
    if ([string]::IsNullOrWhiteSpace([string]$Event.message_id)) { throw 'message_id is required.' }
    if ([string]$Event.subject.session_id -ne [string]$Event.payload.session_id) { throw 'subject/payload session_id mismatch.' }
    if ([string]$Event.payload.manifest_sha256 -notmatch '^[0-9a-fA-F]{64}$') { throw 'manifest_sha256 must be a SHA-256 digest.' }
    if (-not $Event.payload.evidence_files -or @($Event.payload.evidence_files).Count -eq 0) { throw 'evidence_files must be non-empty.' }
    if (@('GREEN','YELLOW','RED','UNKNOWN') -notcontains [string]$Event.payload.diagnostic_status) { throw 'Invalid diagnostic_status.' }
}

if (-not (Test-Path -LiteralPath $EventPath -PathType Leaf)) { throw "Event not found: $EventPath" }
$uri = [uri]$Endpoint
Test-Endpoint $uri
$raw = Get-Content -LiteralPath $EventPath -Raw
$event = $raw | ConvertFrom-Json
Test-SessionCompletedShadow $event

if ($ValidateOnly) {
    Write-Output ('VALIDATION RESULT: PASS contract={0} session={1} message_id={2}' -f $event.contract_id,$event.subject.session_id,$event.message_id)
    exit 0
}

if ([string]::IsNullOrWhiteSpace($BearerToken)) { throw 'DSG_TELEMETRY_INGEST_TOKEN/BearerToken is required.' }
$headers = @{ Authorization = "Bearer $BearerToken"; 'Idempotency-Key' = [string]$event.message_id }

$attempt = 0
while ($true) {
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri $uri -Method Post -Headers $headers -ContentType 'application/json' -Body $raw -TimeoutSec $TimeoutSeconds -UseBasicParsing
        if ($response.StatusCode -lt 200 -or $response.StatusCode -ge 300) { throw "Unexpected HTTP status $($response.StatusCode)." }
        Write-Output ('PUBLISH RESULT: PASS status={0} attempt={1} session={2} message_id={3}' -f $response.StatusCode,$attempt,$event.subject.session_id,$event.message_id)
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
