Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$tokens=$null; $errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot 'Invoke-BKL043-F4Window.ps1'),[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'PARSE_FAILED'}
$fn=$ast.Find({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Invoke-BoundedPilotJob'},$true)
Invoke-Expression $fn.Extent.Text
$result=@(Invoke-BoundedPilotJob -MaximumSeconds 10 -Arguments @() -Body { 'SYNTHETIC_COMPLETED' })
if($result -notcontains 'SYNTHETIC_COMPLETED' -or $result -contains 'BKL043_F4_SUPERVISOR_DEADLINE_STOP'){throw 'NORMAL_COMPLETION_FAILED'}
Write-Output 'PASS normal completion'
$result=@(Invoke-BoundedPilotJob -MaximumSeconds 10 -Arguments @('path with spaces','https://synthetic.invalid') -Body {param($a,$b) "$a|$b"})
if($result -notcontains 'path with spaces|https://synthetic.invalid'){throw 'ARGUMENT_TRANSPORT_FAILED'}
Write-Output 'PASS arguments preserved without shell interpolation'
$watch=[Diagnostics.Stopwatch]::StartNew()
$result=@(Invoke-BoundedPilotJob -MaximumSeconds 3 -Arguments @() -Body { Start-Sleep -Seconds 60 })
if($result -notcontains 'BKL043_F4_SUPERVISOR_DEADLINE_STOP' -or $watch.Elapsed.TotalSeconds -gt 8){throw 'DEADLINE_FAILED'}
Write-Output 'PASS blocked PowerShell operation stopped'
$watch.Restart()
$result=@(Invoke-BoundedPilotJob -MaximumSeconds 4 -Arguments @() -Body { & "$env:windir\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -Command '$PID; Start-Sleep -Seconds 60' })
if($result -notcontains 'BKL043_F4_SUPERVISOR_DEADLINE_STOP' -or $watch.Elapsed.TotalSeconds -gt 9){throw 'NATIVE_DEADLINE_FAILED'}
Write-Output 'PASS blocked native operation supervisor returned'
$nativeId=@($result | Where-Object { [string]$_ -match '^\d+$' })
if($nativeId.Count -ne 1){throw 'NATIVE_PID_NOT_OBSERVED'}
if(Get-Process -Id ([int]$nativeId[0]) -ErrorAction SilentlyContinue){throw 'NATIVE_CHILD_LEAK'}
Write-Output 'PASS native child no longer running'
$caught=$false
try { Invoke-BoundedPilotJob -MaximumSeconds 0 -Arguments @() -Body {throw 'MUST_NOT_RUN'} } catch { $caught=$_.Exception.Message -eq 'WINDOW_EXPIRED' }
if(-not $caught){throw 'EXPIRED_WINDOW_FAILED'}
Write-Output 'PASS expired duration rejected'
if(@(Get-Job).Count -ne 0){throw 'JOB_LEAK'}
Write-Output 'PASS no job remains in test session'
Write-Output 'No collector top-level, cloud credentials, network or real outbox used.'
