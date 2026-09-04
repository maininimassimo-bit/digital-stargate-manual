[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$TransportRoot,
    [string]$EvidenceRoot = (Join-Path $env:USERPROFILE 'DSG-Inventory\VerifiedTransportCleanup')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Import-Module (Join-Path $PSScriptRoot 'DSG.VerifiedTransportCleanup.psm1') -Force

if (-not (Test-Path -LiteralPath $TransportRoot -PathType Container)) {
    throw "Transport root not found: $TransportRoot"
}

$runId = [guid]::NewGuid().ToString()
$startedAt = (Get-Date).ToUniversalTime()
$runRoot = Join-Path $EvidenceRoot ($startedAt.ToString('yyyyMMddTHHmmssZ') + '-' + $runId)
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null

# Metadata-only discovery: enumerate names/paths, never read or hash bulk XISF payloads.
$allFiles = @(Get-ChildItem -LiteralPath $TransportRoot -File -Recurse -ErrorAction Stop)
$transportFiles = @($allFiles | Where-Object { $_.Name -like '*.xisf' -and $_.Name -notlike '*.dsg-partial*' })
$readyFiles = @($allFiles | Where-Object { $_.Name -like '*.xisf.ready.json' })
$ackFiles = @($allFiles | Where-Object { $_.Name -like '*.xisf.imported.json' })

$assetPaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($file in $transportFiles) { [void]$assetPaths.Add($file.FullName) }
foreach ($file in $readyFiles) { [void]$assetPaths.Add($file.FullName.Substring(0, $file.FullName.Length - '.ready.json'.Length)) }
foreach ($file in $ackFiles) { [void]$assetPaths.Add($file.FullName.Substring(0, $file.FullName.Length - '.imported.json'.Length)) }

$results = @()
foreach ($transportPath in @($assetPaths | Sort-Object)) {
    $readyPath = $transportPath + '.ready.json'
    $ackPath = $transportPath + '.imported.json'

    if (-not (Test-Path -LiteralPath $readyPath -PathType Leaf)) {
        $results += [pscustomobject][ordered]@{
            FileName = [System.IO.Path]::GetFileName($transportPath)
            State = 'BLOCKED'
            TechnicalCandidate = $false
            CleanupEligible = $false
            CleanupAuthorized = $false
            ReasonCode = $(if (Test-Path -LiteralPath $ackPath -PathType Leaf) { 'ORPHAN_ACK_READY_MISSING' } else { 'READY_MISSING' })
            PolicyReasonCode = 'RETENTION_NOT_APPROVED'
            TransportPath = $transportPath
            ReadyManifestPath = $readyPath
            AckPath = $ackPath
            Deleted = 0
        }
        continue
    }

    $results += Test-DSGCleanupEvidence -ReadyManifestPath $readyPath -AckPath $ackPath -TransportPath $transportPath
}

$technicalCandidates = @($results | Where-Object { $_.TechnicalCandidate }).Count
$authorized = @($results | Where-Object { $_.CleanupAuthorized }).Count
$blocked = @($results | Where-Object { -not $_.TechnicalCandidate }).Count

$summary = [pscustomobject][ordered]@{
    SchemaVersion = '1.1'
    Component = 'DSG.VerifiedTransportCleanupDryRun'
    Mode = 'DRY_RUN_NO_DELETE'
    RunId = $runId
    StartedAtUtc = $startedAt.ToString('o')
    CompletedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    Computer = $env:COMPUTERNAME
    TransportRoot = $TransportRoot
    AssetsObserved = $assetPaths.Count
    XisfObserved = $transportFiles.Count
    ReadyObserved = $readyFiles.Count
    AckObserved = $ackFiles.Count
    TechnicalCandidates = $technicalCandidates
    CleanupAuthorized = $authorized
    CleanupEligible = 0
    Blocked = $blocked
    Deleted = 0
}

$csvPath = Join-Path $runRoot 'cleanup-evaluation.csv'
$jsonPath = Join-Path $runRoot 'cleanup-evaluation.json'
$summaryPath = Join-Path $runRoot 'cleanup-summary.json'

$results | Export-Csv -LiteralPath $csvPath -NoTypeInformation -Encoding UTF8
$results | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $jsonPath -Encoding UTF8
$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $summaryPath -Encoding UTF8

[pscustomobject]@{
    Summary = $summary
    Results = $results
    EvidenceRoot = $runRoot
    Deleted = 0
}
