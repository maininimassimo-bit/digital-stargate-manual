param(
    [string]$CsvPath = ".\reports\registro-validazioni.csv"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $CsvPath)) {
    throw "Registro non trovato: $CsvPath"
}

$data = Import-Csv $CsvPath
$allowedStatus = @("Aperto","In verifica","Validato","Non applicabile","Rinviato")
$errors = @()

foreach ($row in $data) {
    if ($row.Stato -notin $allowedStatus) {
        $errors += "$($row.ID): stato non valido '$($row.Stato)'"
    }

    if ($row.Stato -eq "Validato") {
        if ([string]::IsNullOrWhiteSpace($row.ValoreConfermato)) { $errors += "$($row.ID): ValoreConfermato mancante" }
        if ([string]::IsNullOrWhiteSpace($row.Fonte)) { $errors += "$($row.ID): Fonte mancante" }
        if ([string]::IsNullOrWhiteSpace($row.ValidatoDa)) { $errors += "$($row.ID): ValidatoDa mancante" }
        if ([string]::IsNullOrWhiteSpace($row.DataValidazione)) { $errors += "$($row.ID): DataValidazione mancante" }
    }
}

if ($errors.Count -gt 0) {
    Write-Host "Il registro contiene errori:"
    $errors | ForEach-Object { Write-Host " - $_" }
    exit 1
}

$data | Group-Object Stato | Sort-Object Name | ForEach-Object {
    Write-Host "$($_.Name): $($_.Count)"
}
