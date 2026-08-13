[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$SessionId,
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\templates\reporting.config.psd1'),
    [switch]$CreateBranch,
    [switch]$Push
)
. (Join-Path $PSScriptRoot 'Common.ps1')
$config = Get-ReportingConfig -ConfigPath $ConfigPath
$repo = $config.RepositoryRoot
if (-not (Test-Path (Join-Path $repo '.git'))) { throw "La cartella non è un repository Git: $repo" }

$sessionRoot = Get-ChildItem -LiteralPath (Join-Path $repo 'data\sessions') -Directory -Recurse |
    Where-Object { $_.Name -eq $SessionId } |
    Select-Object -First 1
if ($null -eq $sessionRoot) { throw "Session package non trovato: $SessionId" }

$manifestPath = Join-Path $sessionRoot.FullName 'manifest.json'
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { throw "Manifest non trovato: $manifestPath" }
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ([string]$manifest.session_id -ne $SessionId) { throw "SessionId manifest non coerente: $($manifest.session_id)" }
if ([string]$manifest.report_status -ne 'COMPLETE') { throw "Session package non pubblicabile: report_status=$($manifest.report_status)" }
foreach ($required in @('raw\nina','raw\phd2','raw\weather')) {
    $requiredPath = Join-Path $sessionRoot.FullName $required
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Container)) { throw "Evidence directory mancante: $required" }
    if (-not (Get-ChildItem -LiteralPath $requiredPath -File -Recurse | Select-Object -First 1)) { throw "Evidence file mancante: $required" }
}

Push-Location $repo
try {
    & git fetch origin main
    if ($LASTEXITCODE -ne 0) { throw 'Git fetch origin/main non riuscito.' }

    $current = (& git branch --show-current).Trim()
    if ($CreateBranch) {
        $branch = "session/$SessionId"
        & git switch -c $branch
        if ($LASTEXITCODE -ne 0) { throw "Impossibile creare il branch $branch" }
        $current = $branch
    }

    $relativeSession = [System.IO.Path]::GetRelativePath($repo, $sessionRoot.FullName).Replace('\','/')
    & git add -- $relativeSession
    $docsSession = Join-Path $repo ("docs\session-reports\{0}\{1}\{2}" -f $manifest.start_local.Substring(0,4), $manifest.start_local.Substring(5,2), $SessionId)
    if (Test-Path -LiteralPath $docsSession) {
        $relativeDocs = [System.IO.Path]::GetRelativePath($repo, $docsSession).Replace('\','/')
        & git add -- $relativeDocs
    }

    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Session package già versionato e invariato: $SessionId" -ForegroundColor Green
        return
    }

    & git commit -m "feat(session): publish $SessionId"
    if ($LASTEXITCODE -ne 0) { throw 'Commit session package non riuscito.' }

    if ($Push) {
        & git pull --rebase origin $current
        if ($LASTEXITCODE -ne 0) { throw 'Rebase prima del push non riuscito.' }
        & git push origin $current
        if ($LASTEXITCODE -ne 0) { throw 'Push Git non riuscito.' }
    }
} finally { Pop-Location }
