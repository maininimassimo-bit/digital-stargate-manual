[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\templates\reporting.config.psd1')
)
. (Join-Path $PSScriptRoot 'Common.ps1')
$config = Get-ReportingConfig -ConfigPath $ConfigPath
$root = $config.RepositoryRoot

$directories = @(
    'data\sessions',
    'data\diagnostics',
    'docs\session-reports',
    'docs\diagnostics',
    'docs\operations',
    'scripts\reporting',
    'templates\reporting',
    '.github\workflows'
)
foreach ($relative in $directories) {
    $path = Join-Path $root $relative
    if ($PSCmdlet.ShouldProcess($path, 'Creazione cartella')) { Ensure-Directory $path }
}

$sessionIndex = Join-Path $root 'docs\session-reports\index.md'
if (-not (Test-Path $sessionIndex)) {
    @"
# Report delle sessioni

| Sessione | Stato | Severità | Report |
|---|---|---|---|
"@ | Set-Content -LiteralPath $sessionIndex -Encoding UTF8
}

$diagIndex = Join-Path $root 'docs\diagnostics\index.md'
if (-not (Test-Path $diagIndex)) {
    @"
# Diagnostica di secondo livello

| Incidente | Sessione | Stato | Report |
|---|---|---|---|
"@ | Set-Content -LiteralPath $diagIndex -Encoding UTF8
}

Write-Host "Struttura inizializzata in: $root" -ForegroundColor Green
