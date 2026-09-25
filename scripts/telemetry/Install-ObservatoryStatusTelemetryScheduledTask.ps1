[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$TaskName = 'DigitalStarGate-ObservatoryStatusTelemetry',
    [string]$SecretPath = 'C:\DigitalStarGate\TelemetryRuntime\secrets\ingest-token.dpapi',
    [string]$PublishEndpoint = 'https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app/v1/observatory-status',
    [bool]$RuntimeEnabled = $false
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $RuntimeEnabled) {
    Write-Host 'Runtime disabled by contract: no task installed or started.'
    exit 0
}

$runtime = Join-Path $RepositoryRoot 'scripts\telemetry\Start-ObservatoryStatusTelemetryRuntime.ps1'
if (-not (Test-Path -LiteralPath $runtime -PathType Leaf)) { throw "Runtime launcher non trovato: $runtime" }
if (-not (Test-Path -LiteralPath $SecretPath -PathType Leaf)) { throw "Secret DPAPI non trovato: $SecretPath" }

$arguments = '-NoLogo -NoProfile -ExecutionPolicy Bypass -File "{0}" -RepositoryRoot "{1}" -SecretPath "{2}" -PublishEndpoint "{3}" -RuntimeEnabled $true' -f $runtime, $RepositoryRoot, $SecretPath, $PublishEndpoint
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $arguments
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName $TaskName
Write-Host "Scheduled task installed and started: $TaskName"
