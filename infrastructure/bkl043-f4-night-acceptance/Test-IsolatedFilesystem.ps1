# Local filesystem acceptance only. Collector top-level, credentials and network are never executed.
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'Start-BKL043-F4Pilot.ps1'
$tokens=$null;$errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'PARSE_FAILED'}
foreach($name in @('Save-Receipt','Get-QueueFiles','Test-QueueAllowsAdmission','Get-ProjectionHeartbeat','Normalize-ReceiptTaskArray','Send-Pending')){
 $fn=$ast.Find({param($n)$n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 if($null -eq $fn){throw "MISSING $name"};Invoke-Expression $fn.Extent.Text
}
$root=Join-Path ([IO.Path]::GetTempPath()) ('DSG-F4-Isolated-'+[guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($root)|Out-Null
$script:OutboxRoot=Join-Path $root 'outbox';$script:MaximumReceiptBytes=4096;$script:MaximumOutboxBytes=16MB;$script:FreshHeartbeatSeconds=60
$script:ProjectionPath=Join-Path $root 'metadata-only.json';$script:RetryState=@{};$script:ApprovedEnd=[DateTimeOffset]::Now.AddHours(1)
$script:ReceiverEndpoint='https://synthetic.invalid/v1/receipts'
function Get-IdentityToken {'SYNTHETIC_NO_CREDENTIAL'}
$script:mode='network';$script:postedId=$null
function Invoke-RestMethod {param($Method,$Uri,$TimeoutSec,$ContentType,$Headers,$Body)
 if($Uri -ne 'https://synthetic.invalid/v1/receipts'){throw 'UNEXPECTED_DESTINATION'}
 $record=$Body|ConvertFrom-Json;$script:postedId=$record.record_id
 if($script:mode -eq 'network'){throw [TimeoutException]::new('ISOLATED_TRANSPORT_FAULT')}
 [pscustomobject]@{ack='DURABLE_CREATED';record_id=$record.record_id}
}
function Check($ok,$label){if(-not $ok){throw "FAIL $label"};Write-Output "PASS $label"}
$now=[datetime]::UtcNow
$files=@(Get-QueueFiles);Check ($files.Count -eq 0) 'real_directory_empty'
$receipt=[ordered]@{record_id=[guid]::NewGuid().ToString('D');source_clock_quality='VALID';source_observed_at_utc=$now.AddHours(-24).ToString('o');signals=@{tasks=@(@{name='a'},@{name='b'},@{name='c'})}}
Save-Receipt $receipt
$files=@(Get-QueueFiles);$file=$files[0];$hash=(Get-FileHash -LiteralPath $file.FullName).Hash
Check ($files.Count -eq 1 -and @(Get-ChildItem -LiteralPath $script:OutboxRoot -Filter '*.pending').Count -eq 0) 'atomic_receipt_file_no_pending'
Check ((Test-QueueAllowsAdmission $files $now).Allowed) 'real_file_exact_24h_allowed'
Check ((Test-QueueAllowsAdmission $files $now.AddSeconds(1)).Reason -eq 'QUEUE_STALE') 'real_file_over_24h_paused'
$cap=Join-Path $script:OutboxRoot 'synthetic-cap.json';$stream=[IO.File]::Open($cap,[IO.FileMode]::CreateNew);try{$stream.SetLength(16MB)}finally{$stream.Dispose()}
Check ((Test-QueueAllowsAdmission @(Get-QueueFiles) $now).Reason -eq 'OUTBOX_FULL') 'real_file_byte_cap_paused'
Check (((Get-FileHash -LiteralPath $file.FullName).Hash -eq $hash) -and (Get-Item -LiteralPath $cap).Length -eq 16MB) 'cap_and_age_preserve_files'
Send-Pending @($file) $now | Out-Null
Check ((Test-Path -LiteralPath $file.FullName) -and (Get-FileHash -LiteralPath $file.FullName).Hash -eq $hash -and $script:postedId -eq $receipt.record_id) 'transport_fault_preserves_real_file_and_uuid'
$script:mode='created';Send-Pending @($file) $now.AddSeconds(3) | Out-Null
Check ((-not(Test-Path -LiteralPath $file.FullName)) -and $script:postedId -eq $receipt.record_id) 'same_uuid_removed_only_after_synthetic_ack'
[IO.File]::WriteAllText($script:ProjectionPath,'SYNTHETIC_METADATA_ONLY')
[IO.File]::SetLastWriteTimeUtc($script:ProjectionPath,$now.AddSeconds(-60))
Check ((Get-ProjectionHeartbeat $now $true).freshness -eq 'FRESH') 'real_metadata_60s_fresh'
Check ((Get-ProjectionHeartbeat $now.AddSeconds(1) $true).freshness -eq 'STALE') 'real_metadata_61s_stale'
$script:ProjectionPath=Join-Path $root 'absent.json'
Check ((Get-ProjectionHeartbeat $now $true).freshness -eq 'UNKNOWN') 'real_absent_metadata_unknown'
Write-Output '11 checks passed. Local synthetic filesystem only; transport simulated, no cloud/EAGLE acceptance implied.'
Write-Output "Preserved synthetic evidence: $root"
