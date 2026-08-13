[CmdletBinding()]
param(
    [string]$ConfigurationPath = "$env:USERPROFILE\DSG-Inventory\SessionPublisher\session-publisher.production.json",
    [int]$SessionStartHour = 18,
    [int]$SessionEndHour = 8,
    [switch]$NoPush
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($SessionStartHour -lt 0 -or $SessionStartHour -gt 23) { throw 'SessionStartHour must be between 0 and 23.' }
if ($SessionEndHour -lt 0 -or $SessionEndHour -gt 23) { throw 'SessionEndHour must be between 0 and 23.' }

$today = (Get-Date).Date
$sessionStart = $today.AddDays(-1).AddHours($SessionStartHour)
$sessionEnd = $today.AddHours($SessionEndHour)
$publisher = Join-Path $PSScriptRoot 'Publish-DSGSessionPackage.ps1'
if (-not (Test-Path -LiteralPath $publisher -PathType Leaf)) { throw "Publisher not found: $publisher" }

$params = @{
    SessionStart = $sessionStart
    SessionEnd = $sessionEnd
    ConfigurationPath = $ConfigurationPath
}
if ($NoPush) { $params.NoPush = $true }
& $publisher @params
