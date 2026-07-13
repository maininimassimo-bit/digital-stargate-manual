$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "1/4 - Verifica Git..."
git status --short

Write-Host "2/4 - Build sito MkDocs..."
& ".\.venv\Scripts\python.exe" -m mkdocs build --strict

if ($LASTEXITCODE -ne 0) {
    throw "La build MkDocs non è riuscita."
}

Write-Host "3/4 - Generazione Word..."
powershell -ExecutionPolicy Bypass -File ".\build.ps1"

if ($LASTEXITCODE -ne 0) {
    throw "La build Word non è riuscita."
}

Write-Host "4/4 - Verifica output..."

$word = ".\release\DSG-TM-001_Digital_StarGate_Master.docx"
$site = ".\site\index.html"

if (-not (Test-Path $word)) {
    throw "Documento Word non trovato."
}

if (-not (Test-Path $site)) {
    throw "Sito MkDocs non trovato."
}

Write-Host ""
Write-Host "Release generata correttamente."
Write-Host "Word: $root\release\DSG-TM-001_Digital_StarGate_Master.docx"
Write-Host "Web:  $root\site\index.html"