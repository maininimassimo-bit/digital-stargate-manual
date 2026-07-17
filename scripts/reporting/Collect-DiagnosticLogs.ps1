[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$IncidentId,
    [Parameter(Mandatory)][datetime]$SessionStart,
    [Parameter(Mandatory)][datetime]$SessionEnd,
    [string[]]$Sources = @('Cpwi','Ascom','Eagle','Dome','Network'),
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\templates\reporting.config.psd1')
)
. (Join-Path $PSScriptRoot 'Common.ps1')
$config = Get-ReportingConfig -ConfigPath $ConfigPath
$caseRoot = Join-Path $config.RepositoryRoot "data\diagnostics\$IncidentId"
if (-not (Test-Path $caseRoot)) { throw "Caso diagnostico non trovato: $IncidentId" }

foreach ($sourceName in $Sources) {
    if (-not $config.DiagnosticSources.ContainsKey($sourceName)) {
        Write-Warning "Sorgente non configurata: $sourceName"; continue
    }
    $sourcePath = $config.DiagnosticSources[$sourceName]
    $destination = Join-Path $caseRoot $sourceName.ToLowerInvariant()
    $copied = Copy-FilesInWindow -SourceDirectory $sourcePath -DestinationDirectory $destination -SessionStart $SessionStart -SessionEnd $SessionEnd -Extensions @('.log','.txt','.csv','.json','.evtx') -BoundaryHours 2
    Write-Host "$sourceName: $($copied.Count) file copiati"
}
