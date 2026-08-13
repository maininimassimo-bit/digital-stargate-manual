[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][datetime]$SessionStart,
    [Parameter(Mandatory = $true)][datetime]$SessionEnd,
    [string]$ConfigurationPath = "$env:USERPROFILE\DSG-Inventory\SessionPublisher\session-publisher.production.json",
    [switch]$NoPush
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($SessionEnd -le $SessionStart) { throw 'SessionEnd must be later than SessionStart.' }
if (-not (Test-Path -LiteralPath $ConfigurationPath -PathType Leaf)) { throw "Publisher configuration not found: $ConfigurationPath" }

$config = Get-Content -LiteralPath $ConfigurationPath -Raw | ConvertFrom-Json
$required = @('RepositoryRoot','NinaLogDirectory','Phd2LogDirectory','WeatherCsvPath','ObservatoryName','TimeZoneId')
foreach ($name in $required) {
    if ([string]::IsNullOrWhiteSpace([string]$config.$name)) { throw "Missing publisher configuration value: $name" }
}

$repo = [string]$config.RepositoryRoot
if (-not (Test-Path -LiteralPath (Join-Path $repo '.git') -PathType Container)) { throw "RepositoryRoot is not a Git repository: $repo" }
$common = Join-Path $repo 'scripts\reporting\Common.ps1'
$weatherExporter = Join-Path $repo 'scripts\reporting\Export-WeatherWindow.ps1'
if (-not (Test-Path -LiteralPath $common -PathType Leaf)) { throw "Reporting helper not found: $common" }
if (-not (Test-Path -LiteralPath $weatherExporter -PathType Leaf)) { throw "Weather exporter not found: $weatherExporter" }
. $common

$sessionId = Get-SessionId -SessionStart $SessionStart -SessionEnd $SessionEnd
$relativeSession = Join-Path $SessionStart.ToString('yyyy') (Join-Path $SessionStart.ToString('MM') $sessionId)
$destinationRoot = Join-Path (Join-Path $repo 'data\sessions') $relativeSession
$stagingRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('DSG-SessionPublisher-' + [guid]::NewGuid().ToString('N'))
$evidenceRoot = if (-not [string]::IsNullOrWhiteSpace([string]$config.EvidenceRoot)) { [string]$config.EvidenceRoot } else { "$env:USERPROFILE\DSG-Inventory\SessionPublisher" }
$runId = 'DSG-SESSION-PUBLISH-' + [guid]::NewGuid().ToString()
$runRoot = Join-Path $evidenceRoot $runId

function Copy-AdditiveFile {
    param([Parameter(Mandatory)][string]$Source, [Parameter(Mandatory)][string]$Destination)
    $parent = Split-Path -Parent $Destination
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    if (Test-Path -LiteralPath $Destination -PathType Leaf) {
        $sourceHash = (Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash
        $destinationHash = (Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash
        if ($sourceHash -ne $destinationHash) { throw "Session package conflict; existing file differs: $Destination" }
        return
    }
    Copy-Item -LiteralPath $Source -Destination $Destination
}

try {
    New-Item -ItemType Directory -Path $stagingRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
    foreach ($folder in @('raw\nina','raw\phd2','raw\weather','report')) { New-Item -ItemType Directory -Path (Join-Path $stagingRoot $folder) -Force | Out-Null }

    $nina = @(Copy-FilesInWindow -SourceDirectory ([string]$config.NinaLogDirectory) -DestinationDirectory (Join-Path $stagingRoot 'raw\nina') -SessionStart $SessionStart -SessionEnd $SessionEnd -Extensions @('.log'))
    $phd2 = @(Copy-FilesInWindow -SourceDirectory ([string]$config.Phd2LogDirectory) -DestinationDirectory (Join-Path $stagingRoot 'raw\phd2') -SessionStart $SessionStart -SessionEnd $SessionEnd -Extensions @('.txt','.log'))
    $weatherPath = Join-Path $stagingRoot ("raw\weather\CloudWatcher_{0}.csv" -f $sessionId)
    $weatherOk = $false
    try {
        & $weatherExporter -InputCsv ([string]$config.WeatherCsvPath) -OutputCsv $weatherPath -SessionStart $SessionStart -SessionEnd $SessionEnd | Out-Host
        $weatherOk = Test-Path -LiteralPath $weatherPath -PathType Leaf
    }
    catch {
        $weatherOk = $false
    }

    $complete = ($nina.Count -gt 0 -and $phd2.Count -gt 0 -and $weatherOk)
    $summary = [ordered]@{
        SchemaVersion = '1.0'
        RunId = $runId
        SessionId = $sessionId
        NinaFiles = $nina.Count
        Phd2Files = $phd2.Count
        WeatherAvailable = $weatherOk
        Status = if ($complete) { 'COMPLETE' } else { 'DEFERRED_INCOMPLETE_EVIDENCE' }
        Published = $false
        CompletedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    }

    if (-not $complete) {
        $summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runRoot 'publisher-evidence.json') -Encoding UTF8
        throw "Session evidence incomplete for $sessionId. No repository files were published."
    }

    Set-Content -LiteralPath (Join-Path $stagingRoot 'report\README.md') -Encoding UTF8 -Value "# Session report`n`nGenerated analytics reports are published downstream under docs/session-reports after the versioned session package is accepted.`n"
    $manifestConfig = @{ ObservatoryName = [string]$config.ObservatoryName; TimeZoneId = [string]$config.TimeZoneId }
    Update-SessionReadme -SessionRoot $stagingRoot -SessionId $sessionId -SessionStart $SessionStart -SessionEnd $SessionEnd
    Write-SessionManifest -SessionRoot $stagingRoot -SessionId $sessionId -SessionStart $SessionStart -SessionEnd $SessionEnd -Config $manifestConfig -Status 'COMPLETE' -Severity 'UNASSESSED'

    Push-Location $repo
    try {
        if (-not $NoPush) {
            & git pull --ff-only origin main
            if ($LASTEXITCODE -ne 0) { throw 'git pull --ff-only failed; publication aborted.' }
        }

        foreach ($source in Get-ChildItem -LiteralPath $stagingRoot -File -Recurse) {
            $relative = [System.IO.Path]::GetRelativePath($stagingRoot, $source.FullName)
            Copy-AdditiveFile -Source $source.FullName -Destination (Join-Path $destinationRoot $relative)
        }

        & git add -- (Join-Path 'data\sessions' $relativeSession)
        & git diff --cached --quiet
        if ($LASTEXITCODE -eq 0) {
            $summary.Status = 'NO_CHANGE'
            $summary.Published = $true
        }
        else {
            & git commit -m "feat(session): publish $sessionId"
            if ($LASTEXITCODE -ne 0) { throw 'Session package commit failed.' }
            if (-not $NoPush) {
                & git push origin HEAD:main
                if ($LASTEXITCODE -ne 0) { throw 'Session package push failed.' }
            }
            $summary.Status = 'PUBLISHED'
            $summary.Published = $true
        }
    }
    finally { Pop-Location }

    $summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runRoot 'publisher-evidence.json') -Encoding UTF8
    [pscustomobject]$summary | Format-List
}
finally {
    if (Test-Path -LiteralPath $stagingRoot) { Remove-Item -LiteralPath $stagingRoot -Recurse -Force }
}
