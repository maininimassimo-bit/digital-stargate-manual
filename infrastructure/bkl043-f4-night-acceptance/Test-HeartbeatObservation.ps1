Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$tokens=$null;$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot 'Start-BKL043-F4Pilot.ps1'),[ref]$tokens,[ref]$errors)
$fn=$ast.Find({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Get-ProjectionHeartbeat'},$true)
Invoke-Expression $fn.Extent.Text
$script:ProjectionPath='SYNTHETIC_ONLY';$script:FreshHeartbeatSeconds=60
$script:mode='current'
function Get-Item {
 param($LiteralPath,$ErrorAction)
 if($LiteralPath -ne 'SYNTHETIC_ONLY'){throw 'UNEXPECTED_SOURCE'}
 if($script:mode -eq 'denied'){throw [UnauthorizedAccessException]::new('synthetic')}
 $timestamp=[datetime]::UtcNow
 if($script:mode -eq 'future'){$timestamp=$timestamp.AddMinutes(5)}
 [pscustomobject]@{LastWriteTimeUtc=$timestamp}
}
$staleObservation=[datetime]::UtcNow.AddSeconds(-2)
if((Get-ProjectionHeartbeat $staleObservation $true).freshness -ne 'UNKNOWN'){throw 'REGRESSION_NOT_REPRODUCED'}
Write-Output 'PASS old sampling timestamp reproduces concurrent-update UNKNOWN'
if((Get-ProjectionHeartbeat -ClockValid $true).freshness -ne 'FRESH'){throw 'OBSERVATION_TIME_FAILED'}
Write-Output 'PASS current metadata measured at observation remains FRESH'
$script:mode='future'
if((Get-ProjectionHeartbeat -ClockValid $true).freshness -ne 'UNKNOWN'){throw 'FUTURE_TIMESTAMP_TRUSTED'}
Write-Output 'PASS genuinely future metadata remains UNKNOWN'
$script:mode='denied'
if((Get-ProjectionHeartbeat -ClockValid $true).freshness -ne 'UNKNOWN'){throw 'UNREADABLE_NOT_UNKNOWN'}
Write-Output 'PASS unreadable metadata remains UNKNOWN'
Write-Output 'No real projection or collector top-level accessed.'
