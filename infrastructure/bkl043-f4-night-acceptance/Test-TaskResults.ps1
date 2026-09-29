Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'Start-BKL043-F4Pilot.ps1'
$tokens=$null;$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
foreach($name in @('Get-TaskSignals','Convert-LocalTimeToUtc')){
 $fn=$ast.Find({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 Invoke-Expression $fn.Extent.Text
}
$script:TaskNames=@('synthetic-a','synthetic-b','synthetic-c')
function Get-ScheduledTask {param($TaskPath,$TaskName) [pscustomobject]@{State='Ready';Name=$TaskName}}
function Get-ScheduledTaskInfo {param($InputObject) [pscustomobject]@{LastRunTime=[datetime]::MinValue;LastTaskResult=$script:caseCode}}
function Get-RunningTaskProcessPresence {param($TaskName) $false}
$failures=0
$hexValues=@('0x00000000','0x00000001','0x00041301','0x80070001','0xFFFFFFFF','0x80070001')
$caseIndex=0
foreach($code in @(0L,1L,267009L,2147942401L,4294967295L,-2147024895L)){
 $script:caseCode=$code
 try{
  $signals=@(Get-TaskSignals ([TimeZoneInfo]::Utc))
  $expected=if($code -eq 0){'SUCCESS'}else{'NONZERO_REVIEW'}
  if($signals.Count -ne 3 -or @($signals | Where-Object {$_.outcome_interpretation -ne $expected -or $_.last_task_result -ne $code}).Count){throw 'SEMANTICS_MISMATCH'}
  if(@($signals | Where-Object {$_.result_hex -ne $hexValues[$caseIndex]}).Count){throw 'HEX_MISMATCH'}
  Write-Output "PASS synthetic task result $code"
 }catch{
  $failures++
  Write-Output "FAIL synthetic task result $code : $($_.Exception.GetType().Name)"
 }
 $caseIndex++
}
Write-Output 'No real tasks, cloud, devices or collector top-level accessed.'
if($failures){exit 1}
