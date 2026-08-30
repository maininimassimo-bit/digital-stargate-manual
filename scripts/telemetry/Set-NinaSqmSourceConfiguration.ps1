[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [string]$Endpoint = 'http://meteo.deeplab.space:8080/cgi-bin/cgiLastData',
    [ValidateRange(5,3600)] [int]$PollSeconds = 30,
    [ValidateRange(5,7200)] [int]$FreshnessSeconds = 120,
    [ValidateRange(1,30)] [int]$HttpTimeoutSeconds = 5,
    [switch]$RemoveConfiguration
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($FreshnessSeconds -lt $PollSeconds) {
    throw 'FreshnessSeconds must be greater than or equal to PollSeconds.'
}

$nina = @(Get-Process -Name NINA -ErrorAction SilentlyContinue)
if ($nina.Count -gt 0) {
    throw 'NINA is running. Close NINA before changing the SQM source configuration.'
}

$telemetryRoot = Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry'
$configPath = Join-Path $telemetryRoot 'sqm-source.json'
$backupRoot = Join-Path $telemetryRoot 'configuration-backups'
$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')

New-Item -ItemType Directory -Path $telemetryRoot -Force | Out-Null
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

if (Test-Path -LiteralPath $configPath -PathType Leaf) {
    $backup = Join-Path $backupRoot ("sqm-source.{0}.json" -f $stamp)
    Copy-Item -LiteralPath $configPath -Destination $backup -Force
    Write-Output ('Previous SQM configuration backed up to: {0}' -f $backup)
}

if ($RemoveConfiguration) {
    if ($PSCmdlet.ShouldProcess($configPath, 'Remove SQM source configuration and restore built-in defaults')) {
        Remove-Item -LiteralPath $configPath -Force -ErrorAction SilentlyContinue
    }
    Write-Output 'SQM source configuration removed. Built-in defaults will apply at next NINA start.'
    exit 0
}

$uri = $null
if (-not [Uri]::TryCreate($Endpoint, [UriKind]::Absolute, [ref]$uri) -or $uri.Scheme -notin @('http','https')) {
    throw 'Endpoint must be an absolute HTTP or HTTPS URI.'
}

$config = [ordered]@{
    endpoint = $uri.AbsoluteUri
    pollSeconds = $PollSeconds
    freshnessSeconds = $FreshnessSeconds
    httpTimeoutSeconds = $HttpTimeoutSeconds
}
$json = $config | ConvertTo-Json -Depth 3

if ($PSCmdlet.ShouldProcess($configPath, 'Write SQM source configuration')) {
    [System.IO.File]::WriteAllText($configPath, $json + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
}

Write-Output ('SQM source configuration: {0}' -f $configPath)
Write-Output ('Endpoint: {0}' -f $config.endpoint)
Write-Output ('Poll seconds: {0}' -f $config.pollSeconds)
Write-Output ('Freshness seconds: {0}' -f $config.freshnessSeconds)
Write-Output ('HTTP timeout seconds: {0}' -f $config.httpTimeoutSeconds)
Write-Output 'No NINA process was started. No equipment connection was opened. No device command was sent.'
