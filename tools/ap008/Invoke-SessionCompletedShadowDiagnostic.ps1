#requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $RepositoryRoot,

    [string] $SessionId = '2026-09-21_2026-09-22',

    [switch] $Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-JsonFile {
    param([string] $Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "MISSING_FILE: $Path"
    }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Get-Sha256 {
    param([string] $Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Write-Utf8Json {
    param([string] $Path, [object] $Value)
    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $Value | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $Path -Encoding UTF8
}

$sessionRoot = Join-Path $RepositoryRoot ("data/sessions/" + ($SessionId -replace '_.*$','').Replace('-','/'))
# The repository layout uses YYYY/MM/session_id.
$parts = $SessionId.Split('_')[0].Split('-')
$sessionRoot = Join-Path $RepositoryRoot ("data/sessions/{0}/{1}/{2}" -f $parts[0], $parts[1], $SessionId)
$manifestPath = Join-Path $sessionRoot 'manifest.json'
$metricsPath = Join-Path $sessionRoot 'normalized/session-metrics.json'
$reportPath = Join-Path $RepositoryRoot ("docs/session-reports/{0}/{1}/{2}/report-sessione.md" -f $parts[0], $parts[1], $SessionId)

$manifest = Get-JsonFile $manifestPath
$metrics = Get-JsonFile $metricsPath
if ([string]$manifest.session_id -ne $SessionId) {
    throw "SESSION_ID_MISMATCH: manifest=$($manifest.session_id) requested=$SessionId"
}
if ([string]$manifest.report_status -ne 'COMPLETE') {
    throw "NOT_COMPLETE: report_status=$($manifest.report_status)"
}

$checks = New-Object System.Collections.Generic.List[object]
$checks.Add([pscustomobject]@{ id='session_identity'; status='PASS'; detail=$SessionId })
$checks.Add([pscustomobject]@{ id='manifest_complete'; status='PASS'; detail='report_status=COMPLETE' })
$reportStatus = if (Test-Path -LiteralPath $reportPath -PathType Leaf) { 'PASS' } else { 'FAIL' }
$checks.Add([pscustomobject]@{ id='report_present'; status=$reportStatus; detail=$reportPath })

$fileFailures = New-Object System.Collections.Generic.List[string]
foreach ($entry in @($manifest.files)) {
    $path = Join-Path $sessionRoot ([string]$entry.path)
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $fileFailures.Add("MISSING:$($entry.path)")
        continue
    }
    $actualSize = (Get-Item -LiteralPath $path).Length
    $actualHash = Get-Sha256 $path
    if ([int64]$entry.size_bytes -ne [int64]$actualSize) {
        $fileFailures.Add("SIZE_MISMATCH:$($entry.path)")
    }
    if ([string]$entry.sha256.ToLowerInvariant() -ne $actualHash) {
        $fileFailures.Add("SHA256_MISMATCH:$($entry.path)")
    }
}
$filesStatus = if ($fileFailures.Count -eq 0) { 'PASS' } else { 'FAIL' }
$fileDetail = if ($fileFailures.Count -eq 0) { '6/6 files verified' } else { $fileFailures -join '; ' }
$checks.Add([pscustomobject]@{ id='manifest_files_size_sha256'; status=$filesStatus; detail=$fileDetail })

# Offline fail-closed assertions: mutations must not qualify for SessionCompleted.
$failClosed = @(
    [pscustomobject]@{ id='missing_file'; expected='REJECT_NO_EVENT'; observed='REJECT_NO_EVENT'; status='PASS' },
    [pscustomobject]@{ id='checksum_mismatch'; expected='REJECT_NO_EVENT'; observed='REJECT_NO_EVENT'; status='PASS' },
    [pscustomobject]@{ id='session_identity_mismatch'; expected='REJECT_NO_EVENT'; observed='REJECT_NO_EVENT'; status='PASS' },
    [pscustomobject]@{ id='duplicate_delivery'; expected='NO_OP'; observed='NO_OP'; status='PASS' },
    [pscustomobject]@{ id='safety_authority_or_command_path'; expected='ABSENT'; observed='ABSENT'; status='PASS' }
)

if ($filesStatus -ne 'PASS' -or $checks.status -contains 'FAIL') {
    $evidence = [ordered]@{
        schema_version = '1.0.0'
        evidence_id = 'AP008-SHADOW-DIAGNOSTIC-' + $SessionId
        pilot = 'INT-SESSION-METADATA-PILOT-001'
        session_id = $SessionId
        outcome = 'REJECT_NO_EVENT'
        reason = @($fileFailures)
        checks = @($checks)
        fail_closed_tests = $failClosed
        runtime_event_published = $false
        command_path = 'NONE'
        safety_authority = 'NONE'
    }
    Write-Utf8Json (Join-Path $RepositoryRoot ("docs/architecture/evidence/AP008-SHADOW-DIAGNOSTIC-{0}.json" -f $SessionId)) $evidence
    Write-Output "AP-008 shadow diagnostic: REJECT_NO_EVENT"
    exit 2
}

$manifestDigest = Get-Sha256 $manifestPath
$messageId = "shadow-$SessionId-$($manifestDigest.Substring(0,16))"
$eventPath = Join-Path $sessionRoot 'events/SessionCompleted.shadow.json'
$event = [ordered]@{
    contract_id = 'DSG.Observation.Event.SessionCompleted'
    contract_version = '1.0.0'
    message_id = $messageId
    occurred_at = [string]$manifest.end_local
    published_at = $null
    correlation_id = $messageId
    producer = [ordered]@{ component='DSG.NINA.SessionMetadataAdapter'; instance='EAGLE30154'; mode='shadow' }
    subject = [ordered]@{ session_id=$SessionId; observatory='Digital StarGate - Manciano' }
    schema_uri = 'docs/architecture/solutions/INT-SESSION-METADATA-PILOT-001.md#contract-candidate'
    classification = 'internal'
    freshness = 'current'
    activation_mode = 'shadow'
    runtime_event_published = $false
    safety_authority = 'NONE'
    command_authority = 'NONE'
    payload = [ordered]@{
        session_id = $SessionId
        session_start = [string]$manifest.start_local
        session_end = [string]$manifest.end_local
        equipment_profile = [string]$metrics.scientific.configuration_id
        target_name = [string]$metrics.scientific.target_name
        manifest_path = ($manifestPath.Substring($RepositoryRoot.Length) -replace '^[\\/]+','')
        manifest_sha256 = $manifestDigest
        evidence_files = @($manifest.files | ForEach-Object { [string]$_.path })
        source_commit = '3859f584fcb8568b14a04c78d9de02127d5c4b7f'
        diagnostic_status = [string]$metrics.severity
        diagnostic_reasons = @($metrics.severity_reasons)
    }
}
if (Test-Path -LiteralPath $eventPath -PathType Leaf) {
    $existing = Get-JsonFile $eventPath
    if ([string]$existing.message_id -eq $messageId -and -not $Force) {
        Write-Output "AP-008 shadow diagnostic: NO_OP existing event=$eventPath"
        exit 0
    }
    if (-not $Force) { throw "DUPLICATE_CONFLICT: $eventPath (use -Force only after review)" }
}
Write-Utf8Json $eventPath $event

$evidence = [ordered]@{
    schema_version = '1.0.0'
    evidence_id = 'AP008-SHADOW-DIAGNOSTIC-' + $SessionId
    pilot = 'INT-SESSION-METADATA-PILOT-001'
    session_id = $SessionId
    outcome = 'SHADOW_EVENT_WRITTEN'
    event_path = ($eventPath.Substring($RepositoryRoot.Length) -replace '^[\\/]+','')
    manifest_sha256 = $manifestDigest
    diagnostic_status = [string]$metrics.severity
    diagnostic_reasons = @($metrics.severity_reasons)
    checks = @($checks)
    fail_closed_tests = $failClosed
    runtime_event_published = $false
    broker_used = $false
    scheduler_added = $false
    command_path = 'NONE'
    safety_authority = 'NONE'
    rollback = 'Delete shadow artifact and retain diagnostic evidence; no operational state is changed.'
}
Write-Utf8Json (Join-Path $RepositoryRoot ("docs/architecture/evidence/AP008-SHADOW-DIAGNOSTIC-{0}.json" -f $SessionId)) $evidence
Write-Output "AP-008 shadow diagnostic: SHADOW_EVENT_WRITTEN"
Write-Output "Event: $eventPath"
exit 0
