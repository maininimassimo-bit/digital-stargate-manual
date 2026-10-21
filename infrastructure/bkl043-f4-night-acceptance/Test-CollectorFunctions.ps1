# Only selected functions are imported through AST; collector top-level is never run.
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'Start-BKL043-F4Pilot.ps1'
$tokens=$null;$errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'PARSE_FAILED'}
foreach($name in @('Get-ProjectionHeartbeat','Test-QueueAllowsAdmission','Normalize-ReceiptTaskArray','Send-Pending')) {
 $fn=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 if($null -eq $fn){throw "MISSING $name"}
 Invoke-Expression $fn.Extent.Text
}
$script:ProjectionPath='SYNTHETIC_ONLY';$script:FreshHeartbeatSeconds=60
$script:MaximumReceiptBytes=4096;$script:MaximumOutboxBytes=16MB
$script:ReceiverEndpoint='https://synthetic.invalid/v1/receipts'
$script:ApprovedEnd=[DateTimeOffset]::Now.AddHours(1)
$script:RetryState=@{};$script:Removed=0;$script:Posted=0
$script:now=[DateTimeOffset]::Parse('2026-09-29T14:00:00Z').UtcDateTime;$script:age=60;$script:missing=$false
$script:payload='';$script:mode='created';$script:ackId='synthetic-record'
function Get-Item {param($LiteralPath,$ErrorAction) if($LiteralPath -ne 'SYNTHETIC_ONLY'){throw 'UNEXPECTED_PATH'};if($script:missing){throw 'SYNTHETIC_MISSING'};[pscustomobject]@{LastWriteTimeUtc=$script:now.AddSeconds(-$script:age)}}
function Get-Content {param($LiteralPath,[switch]$Raw) if($LiteralPath -ne 'SYNTHETIC_ONLY'){throw 'UNEXPECTED_PATH'};$script:payload}
function Remove-Item {param($LiteralPath,[switch]$Force) if($LiteralPath -ne 'SYNTHETIC_ONLY'){throw 'UNEXPECTED_PATH'};$script:Removed++}
function Get-IdentityToken {'SYNTHETIC_NO_CREDENTIAL'}
function Invoke-RestMethod {
 param($Method,$Uri,$TimeoutSec,$ContentType,$Headers,$Body)
 if($Uri -ne 'https://synthetic.invalid/v1/receipts'){throw 'UNEXPECTED_DESTINATION'}
 $script:Posted++
 if($script:mode -eq 'network'){throw [TimeoutException]::new('SYNTHETIC_TIMEOUT')}
 [pscustomobject]@{ack=$(if($script:mode -eq 'bad'){'INVALID'}elseif($script:mode -eq 'duplicate'){'DURABLE_DUPLICATE'}else{'DURABLE_CREATED'});record_id=$script:ackId}
}
function Assert-Check($condition,$name){if(-not $condition){throw "FAIL $name"};Write-Output "PASS $name"}
Assert-Check ((Get-ProjectionHeartbeat $script:now $true).freshness -eq 'FRESH') 'heartbeat_60s_fresh'
$script:age=61
Assert-Check ((Get-ProjectionHeartbeat $script:now $true).freshness -eq 'STALE') 'heartbeat_61s_stale'
Assert-Check ((Get-ProjectionHeartbeat $script:now $false).freshness -eq 'UNKNOWN') 'heartbeat_invalid_clock_unknown'
$script:missing=$true
Assert-Check ((Get-ProjectionHeartbeat $script:now $true).freshness -eq 'UNKNOWN') 'heartbeat_missing_unknown'
Assert-Check ((Test-QueueAllowsAdmission @() $script:now).Allowed) 'empty_queue_allowed'
$f=[pscustomobject]@{Name='synthetic.json';BaseName='synthetic';FullName='SYNTHETIC_ONLY';Length=1024}
$script:payload='{"source_clock_quality":"VALID","source_observed_at_utc":"2026-09-28T14:00:00Z"}'
Assert-Check ((Test-QueueAllowsAdmission @($f) $script:now).Allowed) 'queue_age_exact_24h_allowed'
Assert-Check ((Test-QueueAllowsAdmission @($f) $script:now.AddSeconds(1)).Reason -eq 'QUEUE_STALE') 'queue_over_24h_paused'
$script:payload='{"source_clock_quality":"UNKNOWN","source_observed_at_utc":null}'
Assert-Check ((Test-QueueAllowsAdmission @($f) $script:now).Reason -eq 'QUEUE_AGE_UNKNOWN') 'queue_unknown_age_paused'
$script:payload='{not-json'
Assert-Check ((Test-QueueAllowsAdmission @($f) $script:now).Reason -eq 'QUEUE_UNREADABLE') 'queue_unreadable_paused'
$f.Length=16MB
Assert-Check ((Test-QueueAllowsAdmission @($f) $script:now).Reason -eq 'OUTBOX_FULL') 'queue_byte_cap_paused'
$f.Length=1024
Assert-Check ((Test-QueueAllowsAdmission (@($f)*1440) $script:now).Reason -eq 'OUTBOX_FULL') 'queue_count_cap_paused'
$script:payload='{"record_id":"synthetic-record","signals":{"tasks":[{"name":"a"},{"name":"b"},{"name":"c"}]}}'
foreach($mode in @('network','bad','created','duplicate')) {
 $script:mode=$mode;$script:Removed=0;$script:Posted=0;$script:RetryState=@{}
 Send-Pending @($f) $script:now | Out-Null
 $expected=if($mode -in @('created','duplicate')){1}else{0}
 Assert-Check ($script:Removed -eq $expected -and $script:Posted -eq 1) "dequeue_$mode"
}
$script:mode='network';$script:RetryState=@{};$script:Removed=0
for($i=0;$i -lt 12;$i++){Send-Pending @($f) $script:now.AddMinutes(10*$i) | Out-Null}
$delay=($script:RetryState[$f.Name].NextUtc-$script:now.AddMinutes(110)).TotalSeconds
Assert-Check ($delay -eq 300 -and $script:Removed -eq 0) 'retry_capped_300s_and_preserved'
$script:ApprovedEnd=[DateTimeOffset]::Now.AddSeconds(20);$script:Posted=0;$script:Removed=0;$script:RetryState=@{}
Send-Pending @($f) $script:now | Out-Null
Assert-Check ($script:Posted -eq 0 -and $script:Removed -eq 0) 'final_30s_no_send_no_delete'
Write-Output '17 checks passed; no live sources, tokens, network or outbox writes; top-level collector never executed.'

