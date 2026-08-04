[CmdletBinding()]
param(
    [switch]$IgnoreOperatingWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ImporterRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $ImporterRoot 'session-transfer.local.json'
$TransferScript = Join-Path $ImporterRoot 'Invoke-DSGSessionTransfer.ps1'

$DiscoveryRoot = Join-Path `
    $env:USERPROFILE `
    'DSG-Inventory\SessionImporter'

$CredentialPath = Join-Path `
    $env:USERPROFILE `
    'DSG-Inventory\Credentials\EAGLE30154-DSGReadOnly.credential.xml'

$EvidenceLogRoot = Join-Path `
    $env:USERPROFILE `
    'DSG-Inventory\SessionTransfer-Launcher'

$SourceShare = '\\192.168.1.144\NINA-Images'
$DestinationRoot = 'F:\Astrofotografia'

New-Item `
    -ItemType Directory `
    -Path $EvidenceLogRoot `
    -Force |
    Out-Null

$LogPath = Join-Path `
    $EvidenceLogRoot `
    ('launcher-{0}.log' -f (Get-Date -Format 'yyyyMMdd-HHmmss'))

Start-Transcript `
    -LiteralPath $LogPath `
    -Force |
    Out-Null

try {
    Write-Host "Launcher started: $(Get-Date -Format 'o')"

    if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
        throw "Configuration file not found: $ConfigPath"
    }

    if (-not (Test-Path -LiteralPath $TransferScript -PathType Leaf)) {
        throw "Transfer script not found: $TransferScript"
    }

    if (-not (Test-Path -LiteralPath $CredentialPath -PathType Leaf)) {
        throw "Credential file not found: $CredentialPath"
    }

    if (-not (Test-Path -LiteralPath $DestinationRoot -PathType Container)) {
        throw "Destination unavailable: $DestinationRoot"
    }

    Remove-PSDrive `
        -Name DSGNINA `
        -Force `
        -ErrorAction SilentlyContinue

    $Credential = Import-Clixml `
        -LiteralPath $CredentialPath

    New-PSDrive `
        -Name DSGNINA `
        -PSProvider FileSystem `
        -Root $SourceShare `
        -Credential $Credential `
        -Scope Global `
        -ErrorAction Stop |
        Out-Null

    if (-not (Test-Path -LiteralPath 'DSGNINA:\')) {
        throw 'The EAGLE source share is not available.'
    }

    $LatestRun = Get-ChildItem `
        -LiteralPath $DiscoveryRoot `
        -Directory `
        -ErrorAction Stop |
        Where-Object {
            Test-Path `
                -LiteralPath (Join-Path $_.FullName 'transfer-plan.csv') `
                -PathType Leaf
        } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($null -eq $LatestRun) {
        throw 'No discovery transfer plan was found.'
    }

    $TransferPlanPath = Join-Path `
        $LatestRun.FullName `
        'transfer-plan.csv'

    $TransferParameters = @{
        ConfigurationPath = $ConfigPath
        TransferPlanPath  = $TransferPlanPath
    }

    if ($IgnoreOperatingWindow) {
        $TransferParameters.IgnoreOperatingWindow = $true
    }

    & $TransferScript @TransferParameters

    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
        throw "Transfer script returned exit code $LASTEXITCODE."
    }

    Write-Host "Launcher completed: $(Get-Date -Format 'o')"
}
catch {
    Write-Error $_
    exit 1
}
finally {
    Remove-PSDrive `
        -Name DSGNINA `
        -Force `
        -ErrorAction SilentlyContinue

    Stop-Transcript `
        -ErrorAction SilentlyContinue
}
