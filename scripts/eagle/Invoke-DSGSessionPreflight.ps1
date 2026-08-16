[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoryPath,

    [Parameter(Mandatory = $true)]
    [string]$LauncherPath,

    [Parameter(Mandatory = $true)]
    [string]$ConfigPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-GitChecked {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed ($LASTEXITCODE): git $($Arguments -join ' ')"
    }
}

if (-not (Test-Path -LiteralPath $RepositoryPath -PathType Container)) {
    throw "Repository path not found: $RepositoryPath"
}

if (-not (Test-Path -LiteralPath $LauncherPath -PathType Leaf)) {
    throw "Launcher path not found: $LauncherPath"
}

if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
    throw "Reporting configuration not found: $ConfigPath"
}

Push-Location $RepositoryPath
try {
    $insideWorkTree = (& git rev-parse --is-inside-work-tree 2>$null)
    if ($LASTEXITCODE -ne 0 -or $insideWorkTree -ne 'true') {
        throw "Not a Git working tree: $RepositoryPath"
    }

    $changes = @(& git status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw 'Unable to inspect Git working tree status.'
    }
    if ($changes.Count -gt 0) {
        throw "Repository working tree is not clean. Refusing automatic session publication.`n$($changes -join [Environment]::NewLine)"
    }

    $branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') {
        throw "Repository must be on main before automatic synchronization. Current branch: $branch"
    }

    Invoke-GitChecked -Arguments @('fetch', 'origin', 'main')
    Invoke-GitChecked -Arguments @('pull', '--ff-only', 'origin', 'main')

    $localHead = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw 'Unable to resolve local HEAD after synchronization.'
    }

    $remoteHead = (& git rev-parse 'origin/main').Trim()
    if ($LASTEXITCODE -ne 0) {
        throw 'Unable to resolve origin/main after synchronization.'
    }

    if ($localHead -ne $remoteHead) {
        throw "Synchronization invariant failed: local HEAD=$localHead origin/main=$remoteHead"
    }

    Write-Host "DSG PRECHECK OK main-head=$localHead repository=$RepositoryPath"
}
finally {
    Pop-Location
}

& $LauncherPath -ConfigPath $ConfigPath
if ($LASTEXITCODE -ne 0) {
    throw "Automatic session launcher failed with exit code $LASTEXITCODE"
}
