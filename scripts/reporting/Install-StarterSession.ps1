[CmdletBinding()]
param(
    [string]$PackageRoot = (Split-Path $PSScriptRoot -Parent),
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\templates\reporting.config.psd1')
)
. (Join-Path $PSScriptRoot 'Common.ps1')
$config = Get-ReportingConfig -ConfigPath $ConfigPath
$source = Join-Path $PackageRoot 'starter-session\2026\07\2026-07-14_2026-07-15'
if (-not (Test-Path $source)) { throw "Sessione iniziale non presente nel pacchetto: $source" }

$nina = Get-ChildItem (Join-Path $source 'raw\nina') -File | Select-Object -First 1
$phd2 = Get-ChildItem (Join-Path $source 'raw\phd2') -File | Select-Object -First 1
$weather = Get-ChildItem (Join-Path $source 'raw\weather') -File | Select-Object -First 1
$report = Get-ChildItem (Join-Path $source 'report') -File -Filter '*.pdf' | Select-Object -First 1

& (Join-Path $PSScriptRoot 'Import-ExistingSession.ps1') `
    -SessionStart ([datetime]'2026-07-14T19:00:00') `
    -SessionEnd ([datetime]'2026-07-15T05:00:00') `
    -NinaLog $nina.FullName -Phd2GuideLog $phd2.FullName `
    -WeatherCsv $weather.FullName -ReportPdf $report.FullName `
    -ConfigPath $ConfigPath
