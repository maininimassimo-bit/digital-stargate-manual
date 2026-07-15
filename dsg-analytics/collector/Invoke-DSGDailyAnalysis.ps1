[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SessionId,

    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual',

    [string]$PythonExe = 'python'
)

$ErrorActionPreference = 'Stop'
$sessionPath = Join-Path $RepositoryRoot ("data\sessions\{0}\{1}\{2}" -f $SessionId.Substring(0,4), $SessionId.Substring(5,2), $SessionId)
$analyticsRoot = Join-Path $RepositoryRoot 'dsg-analytics'
$metricsPath = Join-Path $sessionPath 'normalized\session-metrics.json'
$reportPath = Join-Path $RepositoryRoot ("docs\session-reports\{0}\{1}\{2}\report-sessione.md" -f $SessionId.Substring(0,4), $SessionId.Substring(5,2), $SessionId)

if (-not (Test-Path -LiteralPath $sessionPath)) {
    throw "Sessione non trovata: $sessionPath"
}

& $PythonExe (Join-Path $analyticsRoot 'analyzer\analyze_session.py') --session $sessionPath --output $metricsPath
if ($LASTEXITCODE -ne 0) { throw 'Analisi sessione fallita.' }

& $PythonExe (Join-Path $analyticsRoot 'reporter\generate_markdown_report.py') --metrics $metricsPath --output $reportPath
if ($LASTEXITCODE -ne 0) { throw 'Generazione report Markdown fallita.' }

Write-Host "Analisi completata: $reportPath" -ForegroundColor Green
