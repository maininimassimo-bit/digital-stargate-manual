$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$inputFiles = @(
    ".\docs\index.md"
)

$inputFiles += Get-ChildItem ".\docs\chapters\*.md" |
    Sort-Object Name |
    ForEach-Object { $_.FullName }

$inputFiles += Get-ChildItem ".\docs\appendices\*.md" |
    Sort-Object Name |
    ForEach-Object { $_.FullName }

New-Item -ItemType Directory -Force -Path ".\build" | Out-Null
New-Item -ItemType Directory -Force -Path ".\release" | Out-Null

$outputFile = ".\build\DSG-TM-001_Digital_StarGate_Master.docx"

$pandocArgs = @(
    "--from=markdown",
    "--to=docx",
    "--standalone",
    "--toc",
    "--toc-depth=3",
    "--number-sections",
    "--resource-path=$root\docs;$root\docs\assets\images;$root\docs\assets\diagrams",
    "--metadata=title:Digital StarGate - Manuale Tecnico",
    "--metadata=author:Massimo Mainini",
    "--output=$outputFile"
)

$referenceDoc = ".\templates\DSG-reference.docx"

if (Test-Path $referenceDoc) {
    $pandocArgs += "--reference-doc=$referenceDoc"
}

Write-Host "Generazione del documento Word..."

$pandocOutput = & pandoc @inputFiles @pandocArgs 2>&1
$exitCode = $LASTEXITCODE

$pandocOutput | ForEach-Object {
    Write-Host $_
}

if ($exitCode -ne 0) {
    throw "Pandoc ha restituito il codice di errore $exitCode."
}

Copy-Item $outputFile ".\release\DSG-TM-001_Digital_StarGate_Master.docx" -Force

Write-Host ""
Write-Host "Build completata:"
Write-Host "$root\release\DSG-TM-001_Digital_StarGate_Master.docx"