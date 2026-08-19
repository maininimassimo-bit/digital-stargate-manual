[CmdletBinding()]
param(
    [string]$Prefix = 'http://127.0.0.1:8765/',
    [string]$StoreRoot = 'C:\DigitalStarGate\TelemetryRelay',
    [string]$BearerToken = $env:DSG_TELEMETRY_INGEST_TOKEN,
    [string]$AllowedOrigin = '*',
    [ValidateRange(0, 86400)][int]$DurationSeconds = 0
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-JsonResponse {
    param(
        [Parameter(Mandatory = $true)]$Context,
        [Parameter(Mandatory = $true)][int]$StatusCode,
        [Parameter(Mandatory = $true)]$Body,
        [hashtable]$Headers = @{}
    )

    $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 10 -Compress }
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $Context.Response.StatusCode = $StatusCode
    $Context.Response.ContentType = 'application/json; charset=utf-8'
    $Context.Response.ContentEncoding = [System.Text.Encoding]::UTF8
    $Context.Response.ContentLength64 = $bytes.Length
    foreach ($key in $Headers.Keys) { $Context.Response.Headers[$key] = [string]$Headers[$key] }
    $Context.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    $Context.Response.OutputStream.Close()
}

function Test-BearerToken {
    param($Request)
    $authorization = [string]$Request.Headers['Authorization']
    if ([string]::IsNullOrWhiteSpace($authorization) -or -not $authorization.StartsWith('Bearer ')) { return $false }
    return ($authorization.Substring(7) -ceq $BearerToken)
}

function Test-Payload {
    param([Parameter(Mandatory = $true)]$Payload)

    if ([string]$Payload.schema_version -ne '1.1') { throw 'schema_version must be 1.1' }
    if ([string]$Payload.source_instance -ne 'EAGLE30154') { throw 'source_instance not authorized for localhost pilot' }
    if ([string]$Payload.safety.observed_state -ne 'UNKNOWN') { throw 'overall safety must remain UNKNOWN in pilot' }
    if ([string]$Payload.safety.authority -ne 'LOCAL_SAFETY_AUTHORITY') { throw 'safety authority mismatch' }
    if ([string]::IsNullOrWhiteSpace([string]$Payload.correlation_id)) { throw 'correlation_id required' }

    $id = [guid]::Empty
    if (-not [guid]::TryParse([string]$Payload.correlation_id, [ref]$id)) { throw 'correlation_id must be UUID' }

    $observed = [datetime]::Parse([string]$Payload.observed_at_utc, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
    $freshUntil = [datetime]::Parse([string]$Payload.fresh_until_utc, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
    if ($freshUntil -lt $observed) { throw 'fresh_until_utc precedes observed_at_utc' }
    if ($freshUntil -lt [datetime]::UtcNow) { throw 'snapshot already stale' }
}

if ([string]::IsNullOrWhiteSpace($BearerToken)) { throw 'DSG_TELEMETRY_INGEST_TOKEN/BearerToken is required.' }

$uri = [uri]$Prefix
if ($uri.Scheme -ne 'http' -or @('127.0.0.1','localhost','::1') -notcontains $uri.Host) {
    throw 'Reference relay is localhost-only and accepts HTTP only on loopback.'
}

New-Item -ItemType Directory -Path $StoreRoot -Force | Out-Null
$latestPath = Join-Path $StoreRoot 'observatory-status.json'
$healthPath = Join-Path $StoreRoot 'relay-health.json'
$logPath = Join-Path $StoreRoot 'relay.log'

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($Prefix)
$startedAt = [datetime]::UtcNow
$deadline = if ($DurationSeconds -gt 0) { $startedAt.AddSeconds($DurationSeconds) } else { [datetime]::MaxValue }
$accepted = 0
$rejected = 0
$lastAcceptedUtc = $null
$lastCorrelationId = $null

function Write-RelayHealth {
    [ordered]@{
        schema_version = '1.0'
        component = 'DSG.ObservatoryStatusTelemetryRelay.Reference'
        state = if ($listener.IsListening) { 'RUNNING' } else { 'STOPPED' }
        prefix = $Prefix
        started_at_utc = $startedAt.ToString('o')
        updated_at_utc = [datetime]::UtcNow.ToString('o')
        accepted_requests = $script:accepted
        rejected_requests = $script:rejected
        last_accepted_utc = $script:lastAcceptedUtc
        last_correlation_id = $script:lastCorrelationId
        latest_path = $latestPath
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $healthPath -Encoding UTF8
}

try {
    $listener.Start()
    Write-RelayHealth
    Add-Content -LiteralPath $logPath -Value ('{0} START prefix={1}' -f [datetime]::UtcNow.ToString('o'), $Prefix)
    Write-Output ('Digital StarGate Telemetry Relay reference - listening on {0}' -f $Prefix)
    Write-Output ('Store: {0}' -f $StoreRoot)

    while ([datetime]::UtcNow -lt $deadline) {
        $async = $listener.BeginGetContext($null, $null)
        while (-not $async.AsyncWaitHandle.WaitOne(500)) {
            if ([datetime]::UtcNow -ge $deadline) { break }
        }
        if (-not $async.IsCompleted) { break }
        $context = $listener.EndGetContext($async)
        $request = $context.Request
        $path = $request.Url.AbsolutePath.TrimEnd('/')
        if ([string]::IsNullOrEmpty($path)) { $path = '/' }

        $cors = @{ 'Access-Control-Allow-Origin' = $AllowedOrigin; 'Cache-Control' = 'no-store' }

        try {
            if ($request.HttpMethod -eq 'OPTIONS') {
                $context.Response.StatusCode = 204
                $context.Response.Headers['Access-Control-Allow-Origin'] = $AllowedOrigin
                $context.Response.Headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
                $context.Response.Headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, Idempotency-Key'
                $context.Response.OutputStream.Close()
                continue
            }

            if ($path -eq '/health' -and $request.HttpMethod -eq 'GET') {
                Write-RelayHealth
                $health = Get-Content -LiteralPath $healthPath -Raw
                Write-JsonResponse -Context $context -StatusCode 200 -Body $health -Headers $cors
                continue
            }

            if ($path -eq '/v1/observatory-status' -and $request.HttpMethod -eq 'GET') {
                if (-not (Test-Path -LiteralPath $latestPath -PathType Leaf)) {
                    Write-JsonResponse -Context $context -StatusCode 404 -Body @{ error = 'snapshot_not_found' } -Headers $cors
                    continue
                }
                $body = Get-Content -LiteralPath $latestPath -Raw
                Write-JsonResponse -Context $context -StatusCode 200 -Body $body -Headers $cors
                continue
            }

            if ($path -eq '/v1/observatory-status' -and $request.HttpMethod -eq 'POST') {
                if (-not (Test-BearerToken -Request $request)) {
                    $rejected++
                    Write-RelayHealth
                    Add-Content -LiteralPath $logPath -Value ('{0} REJECT status=401 remote={1}' -f [datetime]::UtcNow.ToString('o'), $request.RemoteEndPoint)
                    Write-JsonResponse -Context $context -StatusCode 401 -Body @{ error = 'unauthorized' } -Headers $cors
                    continue
                }

                $reader = New-Object System.IO.StreamReader($request.InputStream, $request.ContentEncoding)
                try { $raw = $reader.ReadToEnd() } finally { $reader.Dispose() }
                $payload = $raw | ConvertFrom-Json
                Test-Payload -Payload $payload

                $idempotencyKey = [string]$request.Headers['Idempotency-Key']
                if ($idempotencyKey -ne [string]$payload.correlation_id) { throw 'Idempotency-Key must equal correlation_id' }

                $temp = "$latestPath.tmp"
                Set-Content -LiteralPath $temp -Value $raw -Encoding UTF8
                Move-Item -LiteralPath $temp -Destination $latestPath -Force

                $accepted++
                $lastAcceptedUtc = [datetime]::UtcNow.ToString('o')
                $lastCorrelationId = [string]$payload.correlation_id
                Write-RelayHealth
                Add-Content -LiteralPath $logPath -Value ('{0} ACCEPT observed={1} correlation_id={2}' -f $lastAcceptedUtc, $payload.observed_at_utc, $lastCorrelationId)
                Write-JsonResponse -Context $context -StatusCode 202 -Body @{ result = 'accepted'; correlation_id = $lastCorrelationId } -Headers $cors
                continue
            }

            Write-JsonResponse -Context $context -StatusCode 404 -Body @{ error = 'not_found' } -Headers $cors
        }
        catch {
            $rejected++
            Write-RelayHealth
            $message = $_.Exception.Message
            Add-Content -LiteralPath $logPath -Value ('{0} REJECT status=422 message={1}' -f [datetime]::UtcNow.ToString('o'), $message)
            Write-JsonResponse -Context $context -StatusCode 422 -Body @{ error = 'validation_failed'; message = $message } -Headers $cors
        }
    }
}
finally {
    if ($listener.IsListening) { $listener.Stop() }
    $listener.Close()
    Write-RelayHealth
    Add-Content -LiteralPath $logPath -Value ('{0} STOP' -f [datetime]::UtcNow.ToString('o'))
    Write-Output 'Telemetry Relay reference stopped.'
}
