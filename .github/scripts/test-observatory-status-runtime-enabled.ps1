[CmdletBinding()]
param(
    [string]$RepositoryRoot = (Join-Path $PSScriptRoot '..\..')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$files = @(
    'scripts\telemetry\Start-ObservatoryStatusTelemetryRuntime.ps1',
    'scripts\telemetry\Start-ObservatoryStatusTelemetryProducer.ps1',
    'scripts\telemetry\Publish-ObservatoryStatusTelemetry.ps1',
    'scripts\telemetry\Install-ObservatoryStatusTelemetryScheduledTask.ps1',
    'scripts\telemetry\Invoke-DSG-EagleRuntimeDiagnostics.ps1',
    'scripts\telemetry\Export-Phd2GuidingStatus.ps1'
)

foreach ($relative in $files) {
    $path = Join-Path $RepositoryRoot $relative
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Runtime guard file missing: $path"
    }

    $tokens = $null
    $errors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$errors) | Out-Null
    if ($errors.Count -gt 0) {
        throw "PowerShell parse errors in $path"
    }

    $content = Get-Content -LiteralPath $path -Raw
    if ($content -notmatch '\[bool\]\$RuntimeEnabled\s*=\s*\$false') {
        throw "Fail-closed RuntimeEnabled default missing: $path"
    }
    if ($content -notmatch 'Runtime disabled by contract|no task installed or started') {
        throw "RuntimeEnabled guard message missing: $path"
    }
}

$phd2 = Get-Content -LiteralPath (Join-Path $RepositoryRoot 'scripts\telemetry\Export-Phd2GuidingStatus.ps1') -Raw
if ($phd2 -notmatch 'C8_QHY695A|SW4P_EVO' -or $phd2 -notmatch 'RARawDistance|DECRawDistance') { throw 'Profile-aware PHD2 adapter contract missing.' }

$diagnostic = Get-Content -LiteralPath (Join-Path $RepositoryRoot 'scripts\telemetry\Invoke-DSG-EagleRuntimeDiagnostics.ps1') -Raw
if ($diagnostic -notmatch "schemaVersion.*2" -or $diagnostic -notmatch 'Unsupported projection schema') { throw 'Diagnostic must recognize NINA schemaVersion=2.' }

$publisher = Get-Content -LiteralPath (Join-Path $RepositoryRoot 'scripts\telemetry\Publish-ObservatoryStatusTelemetry.ps1') -Raw
if ($publisher -notmatch 'RuntimeEnabled') { throw 'Publisher guard missing.' }

$installer = Get-Content -LiteralPath (Join-Path $RepositoryRoot 'scripts\telemetry\Install-ObservatoryStatusTelemetryScheduledTask.ps1') -Raw
if ($installer -notmatch 'RuntimeEnabled \$true') { throw 'Installer must propagate explicit enable flag.' }

Write-Host 'PASS: runtimeEnabled=false fail-closed guards and PowerShell syntax.'
