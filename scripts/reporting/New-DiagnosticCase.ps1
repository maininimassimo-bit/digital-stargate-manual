[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$SessionId,
    [Parameter(Mandatory)][ValidateSet('ORANGE','RED')][string]$Severity,
    [Parameter(Mandatory)][string]$Title,
    [string]$IncidentId,
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\templates\reporting.config.psd1')
)
. (Join-Path $PSScriptRoot 'Common.ps1')
$config = Get-ReportingConfig -ConfigPath $ConfigPath
if (-not $IncidentId) {
    $year = (Get-Date).Year
    $existing = Get-ChildItem -LiteralPath (Join-Path $config.RepositoryRoot 'data\diagnostics') -Directory -ErrorAction SilentlyContinue |
        Where-Object Name -Match "^INC-$year-\d{3}$" |
        ForEach-Object { [int]($_.Name.Split('-')[-1]) }
    $next = if ($existing) { (($existing | Measure-Object -Maximum).Maximum + 1) } else { 1 }
    $IncidentId = 'INC-{0}-{1:000}' -f $year, $next
}

$dataRoot = Join-Path $config.RepositoryRoot "data\diagnostics\$IncidentId"
$docsRoot = Join-Path $config.RepositoryRoot "docs\diagnostics\$((Get-Date).Year)\$IncidentId"
@($dataRoot,$docsRoot) | ForEach-Object { Ensure-Directory $_ }
@('nina','phd2','cpwi','ascom','eagle','dome','weather','network','windows-events') |
    ForEach-Object { Ensure-Directory (Join-Path $dataRoot $_) }

$case = [ordered]@{
    incident_id = $IncidentId
    session_id = $SessionId
    severity = $Severity
    title = $Title
    status = 'OPEN'
    opened_at = (Get-Date).ToString('o')
    hypotheses = @()
    resolution = $null
}
$case | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $dataRoot 'case.json') -Encoding UTF8

@"
# $IncidentId - $Title

- **Sessione:** $SessionId
- **Severità:** $Severity
- **Stato:** OPEN

## Sintomo

Da compilare.

## Log richiesti

- N.I.N.A. e PHD2 della sessione
- CPWI / ASCOM Telescope se coinvolta la montatura
- Safety Monitor / cupola se coinvolta la sicurezza
- EAGLE / Windows Event Log se presenti blocchi o riavvii
- Teltonika / VPN / Starlink se presente perdita di connettività

## Analisi causa radice

Da compilare nel report diagnostico.
"@ | Set-Content -LiteralPath (Join-Path $docsRoot 'index.md') -Encoding UTF8

Write-Host "Creato caso diagnostico: $IncidentId" -ForegroundColor Green
Write-Host "Dati: $dataRoot"
Write-Host "Documentazione: $docsRoot"
