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
Push-Location $repo
try {
    if ($CreateBranch) {
        $branch = "session/$SessionId"
        & git switch -c $branch
        if ($LASTEXITCODE -ne 0) { throw "Impossibile creare il branch $branch" }
    }
    & git add -- 'data/sessions' 'docs/session-reports'
    & git commit -m "Add session report $SessionId"
    if ($LASTEXITCODE -ne 0) { Write-Warning 'Nessuna modifica da registrare oppure commit non riuscito.' }
    if ($Push) {
        $current = (& git branch --show-current).Trim()
        & git push -u origin $current
        if ($LASTEXITCODE -ne 0) { throw 'Push Git non riuscito.' }
    }
} finally { Pop-Location }
