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

$results = @()
$readyFiles = @(Get-ChildItem -LiteralPath $TransportRoot -Filter '*.ready.json' -File -Recurse -ErrorAction Stop)

foreach ($readyFile in $readyFiles) {
    $transportPath = $readyFile.FullName.Substring(0, $readyFile.FullName.Length - '.ready.json'.Length)
    $ackPath = $transportPath + '.imported.json'
    $results += Test-DSGCleanupEvidence -ReadyManifestPath $readyFile.FullName -AckPath $ackPath
}

$eligible = @($results | Where-Object { $_.CleanupEligible }).Count
$blocked = @($results | Where-Object { -not $_.CleanupEligible }).Count

$summary = [pscustomobject][ordered]@{
    SchemaVersion = '1.0'
    Component = 'DSG.VerifiedTransportCleanupDryRun'
    Mode = 'DRY_RUN_NO_DELETE'
    RunId = $runId
    StartedAtUtc = $startedAt.ToString('o')
    CompletedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    Computer = $env:COMPUTERNAME
    TransportRoot = $TransportRoot
    ReadyObserved = $readyFiles.Count
    CleanupEligible = $eligible
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
