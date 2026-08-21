param(
    [Parameter(Mandatory = $true)]
    [string]$SessionId,

    [Parameter(Mandatory = $true)]
    [string]$Root,

    [string]$BaseRef = 'origin/main',

    [string[]]$ChangedPaths,

    [switch]$SkipAncestry,

    [switch]$SkipScope
)

$ErrorActionPreference = 'Stop'

if ($SessionId -notmatch '^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$') {
    throw "Invalid session ID: $SessionId"
}

$manifestPath = Join-Path $Root 'manifest.json'
if (-not (Test-Path $manifestPath -PathType Leaf)) {
    throw "Manifest missing: $manifestPath"
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
if ([string]$manifest.session_id -ne $SessionId) {
    throw "Manifest session ID mismatch: $($manifest.session_id)"
}
if ([string]$manifest.report_status -ne 'COMPLETE') {
    throw "Session package is not COMPLETE: $SessionId"
}

foreach ($required in @('raw/nina', 'raw/phd2', 'raw/weather')) {
    $requiredPath = Join-Path $Root $required
    if (-not (Test-Path $requiredPath -PathType Container)) {
        throw "Missing required evidence directory: $required"
    }
    if (-not (Get-ChildItem $requiredPath -File -Recurse | Select-Object -First 1)) {
        throw "Missing evidence files: $required"
    }
}

foreach ($entry in @($manifest.files)) {
    $relative = ([string]$entry.path).Replace('\', '/')
    $path = Join-Path $Root $relative
    if (-not (Test-Path $path -PathType Leaf)) {
        throw "Manifest file missing: $relative"
    }

    $actualSize = (Get-Item $path).Length
    if ($null -ne $entry.size_bytes -and [int64]$entry.size_bytes -ne $actualSize) {
        throw "Manifest size mismatch: $relative"
    }

    if (-not [string]::IsNullOrWhiteSpace([string]$entry.sha256)) {
        $actualHash = (Get-FileHash $path -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualHash -ne ([string]$entry.sha256).ToLowerInvariant()) {
            throw "Manifest SHA-256 mismatch: $relative"
        }
    }
}

if (-not $SkipAncestry) {
    & git merge-base --is-ancestor $BaseRef HEAD
    if ($LASTEXITCODE -ne 0) {
        throw 'Session branch is not a fast-forward descendant of current main.'
    }
}

if (-not $SkipScope) {
    $year = $SessionId.Substring(0, 4)
    $month = $SessionId.Substring(5, 2)
    $allowedSession = "data/sessions/$year/$month/$SessionId/"
    $allowedReport = "docs/session-reports/$year/$month/$SessionId/"

    $paths = @($ChangedPaths)
    if ($paths.Count -eq 0) {
        $paths = @(& git diff --name-only "$BaseRef...HEAD")
        if ($LASTEXITCODE -ne 0) {
            throw "Unable to calculate changed paths against $BaseRef"
        }
    }

    foreach ($path in $paths) {
        if ([string]::IsNullOrWhiteSpace($path)) { continue }
        $normalized = ([string]$path).Replace('\', '/')
        if (-not ($normalized.StartsWith($allowedSession) -or $normalized.StartsWith($allowedReport))) {
            throw "Unexpected path in session branch: $normalized"
        }
    }
}

[pscustomobject]@{
    SessionId = $SessionId
    Status = 'PASS'
    Manifest = $manifestPath
    BaseRef = $BaseRef
}
