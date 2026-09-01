[CmdletBinding()]
param(
    [Parameter(Mandatory)][datetime]$SessionStart,
    [Parameter(Mandatory)][datetime]$SessionEnd,
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\templates\reporting.config.psd1'),
    [switch]$CopyToRepository
)
. (Join-Path $PSScriptRoot 'Common.ps1')
$config = Get-ReportingConfig -ConfigPath $ConfigPath
if ($SessionEnd -le $SessionStart) { throw 'SessionEnd deve essere successivo a SessionStart.' }

$sessionId = Get-SessionId -SessionStart $SessionStart -SessionEnd $SessionEnd
$year = $SessionStart.ToString('yyyy')
$month = $SessionStart.ToString('MM')
$baseRoot = if ($CopyToRepository) { Join-Path $config.RepositoryRoot 'data\sessions' } else { $config.StagingRoot }
$sessionRoot = Join-Path $baseRoot (Join-Path $year (Join-Path $month $sessionId))

$ninaDest = Join-Path $sessionRoot 'raw\nina'
$phd2Dest = Join-Path $sessionRoot 'raw\phd2'
$weatherDest = Join-Path $sessionRoot 'raw\weather'
$sqmDest = Join-Path $sessionRoot 'raw\sqm'
$reportDest = Join-Path $sessionRoot 'report'
@($ninaDest, $phd2Dest, $weatherDest, $sqmDest, $reportDest) | ForEach-Object { Ensure-Directory $_ }

$nina = Copy-FilesInWindow -SourceDirectory $config.NinaLogDirectory -DestinationDirectory $ninaDest -SessionStart $SessionStart -SessionEnd $SessionEnd -Extensions @('.log')
$phd2 = Copy-FilesInWindow -SourceDirectory $config.Phd2LogDirectory -DestinationDirectory $phd2Dest -SessionStart $SessionStart -SessionEnd $SessionEnd -Extensions @('.txt', '.log')

$weatherOutput = Join-Path $weatherDest ("CloudWatcher_{0}.csv" -f $sessionId)
& (Join-Path $PSScriptRoot 'Export-WeatherWindow.ps1') -InputCsv $config.WeatherCsvPath -OutputCsv $weatherOutput -SessionStart $SessionStart -SessionEnd $SessionEnd

& (Join-Path $PSScriptRoot 'Export-SqmSessionHistory.ps1') -SessionStart $SessionStart -SessionEnd $SessionEnd -OutputDirectory $sqmDest
$sqmSummary = Join-Path $sqmDest 'sqm-summary.json'

$status = if ($nina.Count -gt 0 -and $phd2.Count -gt 0 -and (Test-Path $weatherOutput)) { 'COMPLETE' } else { 'PARTIAL' }
Update-SessionReadme -SessionRoot $sessionRoot -SessionId $sessionId -SessionStart $SessionStart -SessionEnd $SessionEnd
Write-SessionManifest -SessionRoot $sessionRoot -SessionId $sessionId -SessionStart $SessionStart -SessionEnd $SessionEnd -Config $config -Status $status

Write-Host "Sessione preparata: $sessionRoot" -ForegroundColor Green
Write-Host "N.I.N.A.: $($nina.Count) file; PHD2: $($phd2.Count) file; Meteo: $weatherOutput; SQM: $sqmSummary; Stato: $status"
