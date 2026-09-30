Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$tokens=$null; $errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot 'Start-BKL043-F4Pilot.ps1'),[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'PARSE_FAILED'}
foreach($name in @('Get-TaskSignals','Convert-LocalTimeToUtc')){
 $fn=$ast.Find({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 Invoke-Expression $fn.Extent.Text
}
$script:TaskNames=@('synthetic-task')
function Get-ScheduledTask {param($TaskPath,$TaskName) [pscustomobject]@{State='Ready'}}
function Get-ScheduledTaskInfo {param($InputObject) [pscustomobject]@{LastRunTime=$script:last;LastTaskResult=2147942401L}}
function Get-RunningTaskProcessPresence {param($TaskName) $false}
$origin=[datetime]::new(2026,9,30,8,55,26,[DateTimeKind]::Utc)
$cases=@(
 @{Name='reproduced_future';Delta=29;End=0.05;Unknown=$true},
 @{Name='past';Delta=-24;End=0.05;Unknown=$false},
 @{Name='during_read';Delta=0.02;End=0.05;Unknown=$false},
 @{Name='exact_end';Delta=0.05;End=0.05;Unknown=$false},
 @{Name='subsecond_future';Delta=0.06;End=0.05;Unknown=$true},
 @{Name='clock_backwards';Delta=-24;End=-1;Unknown=$true}
)
foreach($case in $cases){
 $script:last=$origin.AddSeconds($case.Delta)
 $script:clockIndex=0
 $script:clockTimes=@($origin,$origin.AddSeconds($case.End))
 $clock={ $v=$script:clockTimes[$script:clockIndex];$script:clockIndex++;return $v }
 $captured=@(Get-TaskSignals ([TimeZoneInfo]::Utc) $clock 3>&1)
 $warnings=@($captured | Where-Object {$_ -is [Management.Automation.WarningRecord]})
 $row=@($captured | Where-Object {$_ -isnot [Management.Automation.WarningRecord]})[0]
 if(($null -eq $row.last_run_utc) -ne $case.Unknown){throw "FAIL $($case.Name)"}
 if($case.Unknown -and $warnings.Count -ne 1){throw 'MISSING_DIAGNOSTIC'}
 if(-not $case.Unknown -and $warnings.Count -ne 0){throw 'UNEXPECTED_DIAGNOSTIC'}
 if($row.last_task_result -ne 2147942401L -or $row.result_hex -ne '0x80070001' -or $row.outcome_interpretation -ne 'NONZERO_REVIEW'){throw 'OTHER_SIGNALS_CHANGED'}
 Write-Output "PASS $($case.Name)"
}
Write-Output 'Synthetic function tests only; no real tasks, collector top-level or network.'
