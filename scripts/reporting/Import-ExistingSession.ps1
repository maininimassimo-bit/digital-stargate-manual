[CmdletBinding()]
param(
    [Parameter(Mandatory)][datetime]$SessionStart,
    [Parameter(Mandatory)][datetime]$SessionEnd,
    [Parameter(Mandatory)][string]$NinaLog,
    [Parameter(Mandatory)][string]$Phd2GuideLog,
    [Parameter(Mandatory)][string]$WeatherCsv,
    [Parameter(Mandatory)][string]$ReportPdf,
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\templates\reporting.config.psd1')
)
. (Join-Path $PSScriptRoot 'Common.ps1')
$config = Get-ReportingConfig -ConfigPath $ConfigPath
foreach ($p in @($NinaLog,$Phd2GuideLog,$WeatherCsv,$ReportPdf)) {
    if (-not (Test-Path -LiteralPath $p)) { throw "File non trovato: $p" }
}

$sessionId = Get-SessionId -SessionStart $SessionStart -SessionEnd $SessionEnd
$sessionRoot = Join-Path $config.RepositoryRoot ("data\sessions\{0:yyyy}\{0:MM}\{1}" -f $SessionStart, $sessionId)
$docsRoot = Join-Path $config.RepositoryRoot ("docs\session-reports\{0:yyyy}\{0:MM}\{1}" -f $SessionStart, $sessionId)

$destinations = @{
    Nina = Join-Path $sessionRoot 'raw\nina'
    Phd2 = Join-Path $sessionRoot 'raw\phd2'
    Weather = Join-Path $sessionRoot 'raw\weather'
    Report = Join-Path $sessionRoot 'report'
    Docs = $docsRoot
}
$destinations.Values | ForEach-Object { Ensure-Directory $_ }

Copy-Item -LiteralPath $NinaLog -Destination (Join-Path $destinations.Nina ("NINA_{0}.log" -f $sessionId)) -Force
Copy-Item -LiteralPath $Phd2GuideLog -Destination (Join-Path $destinations.Phd2 ("PHD2_GuideLog_{0}.txt" -f $sessionId)) -Force
Copy-Item -LiteralPath $WeatherCsv -Destination (Join-Path $destinations.Weather ("CloudWatcher_{0}.csv" -f $sessionId)) -Force
$reportName = "Report_Sessione_{0}.pdf" -f $sessionId
Copy-Item -LiteralPath $ReportPdf -Destination (Join-Path $destinations.Report $reportName) -Force
Copy-Item -LiteralPath $ReportPdf -Destination (Join-Path $destinations.Docs $reportName) -Force

Write-SessionManifest -SessionRoot $sessionRoot -SessionId $sessionId -SessionStart $SessionStart -SessionEnd $SessionEnd -Config $config -Status 'COMPLETE' -Severity 'UNASSESSED'
Update-SessionReadme -SessionRoot $sessionRoot -SessionId $sessionId -SessionStart $SessionStart -SessionEnd $SessionEnd

$reportIndex = Join-Path $config.RepositoryRoot 'docs\session-reports\index.md'
if (-not (Test-Path $reportIndex)) { Ensure-Directory (Split-Path $reportIndex); "# Report delle sessioni`n" | Set-Content $reportIndex }
$relativeReport = "{0:yyyy}/{0:MM}/{1}/{2}" -f $SessionStart, $sessionId, $reportName
$row = "| $sessionId | COMPLETE | Da valutare | [PDF]($relativeReport) |"
if (-not (Select-String -LiteralPath $reportIndex -SimpleMatch $sessionId -Quiet)) { Add-Content -LiteralPath $reportIndex -Value $row -Encoding UTF8 }

Write-Host "Importazione completata: $sessionRoot" -ForegroundColor Green
