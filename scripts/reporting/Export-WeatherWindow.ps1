[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$InputCsv,
    [Parameter(Mandatory)][string]$OutputCsv,
    [Parameter(Mandatory)][datetime]$SessionStart,
    [Parameter(Mandatory)][datetime]$SessionEnd
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $InputCsv)) { throw "CSV meteo non trovato: $InputCsv" }

$rows = Import-Csv -LiteralPath $InputCsv
$invalidTimestampRows = 0
$filtered = foreach ($row in $rows) {
    $dateText = $row.Date
    $timeText = $row.Time
    if ([string]::IsNullOrWhiteSpace($dateText) -or [string]::IsNullOrWhiteSpace($timeText)) {
        $invalidTimestampRows++
        continue
    }

    $timestamp = [datetime]::MinValue
    $parsed = [datetime]::TryParseExact(
        "$dateText $timeText",
        'yyyy-MM-dd HH:mm:ss',
        [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::None,
        [ref]$timestamp)

    if (-not $parsed) {
        $invalidTimestampRows++
        continue
    }

    if ($timestamp -ge $SessionStart -and $timestamp -le $SessionEnd) { $row }
}
if (-not $filtered) { throw 'Nessuna riga meteo valida trovata nella finestra indicata.' }
$parent = Split-Path -Parent $OutputCsv
if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$filtered | Export-Csv -LiteralPath $OutputCsv -NoTypeInformation -Encoding UTF8
Write-Host "Estratte $(@($filtered).Count) righe meteo in $OutputCsv" -ForegroundColor Green
if ($invalidTimestampRows -gt 0) {
    Write-Warning "Ignorate $invalidTimestampRows righe CloudWatcher con timestamp mancante o non valido."
}
