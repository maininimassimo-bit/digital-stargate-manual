param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = ".\reports"
)

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path $RepoRoot).Path
$docs = Join-Path $repo "docs"

if (-not (Test-Path $docs)) {
    throw "Cartella docs non trovata in: $repo"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$output = (Resolve-Path $OutputDir).Path

$patterns = @("DA VALIDARE","DA CONFERMARE","DA VERIFICARE","TBD","TODO")
$results = @()

$files = Get-ChildItem $docs -Recurse -File -Include *.md,*.yml,*.yaml,*.json,*.csv

foreach ($file in $files) {
    $lineNumber = 0
    foreach ($line in Get-Content $file.FullName) {
        $lineNumber++
        foreach ($pattern in $patterns) {
            if ($line -match [regex]::Escape($pattern)) {
                $relative = $file.FullName.Substring($repo.Length).TrimStart('\','/')
                $category = "Altro"
                if ($relative -match "chapters\\0[1-5]-") { $category = "Generalita-Infrastruttura" }
                elseif ($relative -match "chapters\\0[6-9]-|chapters\\10-") { $category = "Hardware-Astronomico" }
                elseif ($relative -match "chapters\\1[1-5]-") { $category = "Software-Automazione" }
                elseif ($relative -match "chapters\\1[6-9]-") { $category = "Operations-Recovery-Manutenzione" }
                elseif ($relative -match "chapters\\2[0-9]-") { $category = "Governance-Dati-Sicurezza" }
                elseif ($relative -match "chapters\\3[0-9]-") { $category = "Affidabilita-Engineering" }
                elseif ($relative -match "chapters\\4[0-4]-") { $category = "Validazione-Release" }

                $results += [pscustomobject]@{
                    ID = ""
                    Stato = "Aperto"
                    Priorita = ""
                    Categoria = $category
                    File = $relative
                    Riga = $lineNumber
                    Marcatore = $pattern
                    Testo = $line.Trim()
                    ValoreConfermato = ""
                    Fonte = ""
                    Evidenza = ""
                    ValidatoDa = ""
                    DataValidazione = ""
                    Note = ""
                }
                break
            }
        }
    }
}

$counter = 1
foreach ($item in $results) {
    $item.ID = "VAL-{0:D4}" -f $counter
    $counter++
}

$csvPath = Join-Path $output "registro-validazioni.csv"
$results | Export-Csv $csvPath -NoTypeInformation -Encoding UTF8

$mdPath = Join-Path $output "registro-validazioni.md"
$lines = @(
    "# Registro delle validazioni",
    "",
    "Generato: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "",
    "| ID | Stato | Priorita | Categoria | File | Riga | Testo | Valore confermato | Fonte | Validato da | Data |",
    "|---|---|---|---|---|---:|---|---|---|---|---|"
)
foreach ($item in $results) {
    $safeText = $item.Testo.Replace("|","\|")
    $lines += "| $($item.ID) | $($item.Stato) | $($item.Priorita) | $($item.Categoria) | $($item.File) | $($item.Riga) | $safeText |  |  |  |  |"
}
$lines | Set-Content $mdPath -Encoding UTF8

$summaryPath = Join-Path $output "riepilogo-validazioni.txt"
$groups = $results | Group-Object Categoria | Sort-Object Name
@("Totale campi trovati: $($results.Count)","") + ($groups | ForEach-Object { "$($_.Name): $($_.Count)" }) |
    Set-Content $summaryPath -Encoding UTF8

Write-Host ""
Write-Host "Analisi completata."
Write-Host "CSV: $csvPath"
Write-Host "Markdown: $mdPath"
Write-Host "Riepilogo: $summaryPath"
Write-Host "Totale campi trovati: $($results.Count)"
