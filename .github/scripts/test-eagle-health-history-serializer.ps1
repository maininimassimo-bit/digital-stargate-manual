$ErrorActionPreference='Stop'
$serializer=Join-Path $PSScriptRoot '..\..\scripts\telemetry\Convert-EagleHostHealthToHistoryRecords.ps1'
if(-not(Test-Path -LiteralPath $serializer)){throw 'G6-A serializer missing'}

$tokens=$null;$errors=$null
[void][System.Management.Automation.Language.Parser]::ParseFile($serializer,[ref]$tokens,[ref]$errors)
if($errors.Count -gt 0){throw ('PowerShell parse errors: '+(($errors|ForEach-Object{$_.Message}) -join '; '))}

$text=Get-Content -LiteralPath $serializer -Raw
$required=@('history_schema_version','record_id','retention_deletion_enabled','historical_records_deleted','DSG.EagleHostHealthCollector','READ_ONLY','SHA256')
foreach($token in $required){if(-not $text.Contains($token)){throw "Missing G6-A contract token: $token"}}
$forbidden=@('Remove-Item','Restart-Computer','Stop-Process','Restart-Service','Set-Service','Register-ScheduledTask')
foreach($token in $forbidden){if($text -match [regex]::Escape($token)){throw "Forbidden control/delete command found: $token"}}

$root=Join-Path ([IO.Path]::GetTempPath()) ('dsg-g6a-'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory -Path $root -Force|Out-Null
try {
  $input=Join-Path $root 'eagle-health.json';$out=Join-Path $root 'records.ndjson'
  $projection=[ordered]@{
    schema_version='1.0';component='DSG.EagleHostHealthCollector';computer='EAGLE30154';observed_at_utc='2026-09-04T16:00:00.000Z';correlation_id='ci-correlation';
    summary=[ordered]@{state='UNKNOWN'};diagnostics=[ordered]@{collector_mode='READ_ONLY';automatic_remediation=$false};
    signals=[ordered]@{
      cpu=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T16:00:00.001Z';fresh_until_utc='2026-09-04T16:02:00.001Z';source='Win32_Processor';cadence_class='FAST';reason=$null;data=[ordered]@{load_pct=12}}
      memory=[ordered]@{state='UNAVAILABLE';quality='UNKNOWN';observed_at_utc='2026-09-04T16:00:00.002Z';fresh_until_utc='2026-09-04T16:02:00.002Z';source='Win32_OperatingSystem';cadence_class='FAST';reason='SIMULATED';data=$null}
    }
  }
  $projection|ConvertTo-Json -Depth 12|Set-Content -LiteralPath $input -Encoding UTF8
  $a=@(& $serializer -InputPath $input -OutputPath $out)
  $b=@(& $serializer -InputPath $input)
  if($a.Count -ne 2 -or $b.Count -ne 2){throw 'Expected two historical signal records'}
  if($a[0].history_schema_version -ne '1.0'){throw 'History schema mismatch'}
  if($a[0].host -ne 'EAGLE30154'){throw 'Host provenance mismatch'}
  if($a[0].retention_deletion_enabled -ne $false -or $a[0].historical_records_deleted -ne 0){throw 'Deletion invariant violated'}
  if(($a.record_id -join '|') -ne ($b.record_id -join '|')){throw 'Deterministic identity/idempotency failure'}
  if(@(Get-Content -LiteralPath $out).Count -ne 2){throw 'NDJSON output line count mismatch'}

  $bad=Join-Path $root 'bad.json'
  '{"schema_version":"2.0","component":"DSG.EagleHostHealthCollector","computer":"EAGLE30154","diagnostics":{"collector_mode":"READ_ONLY"},"signals":{}}'|Set-Content -LiteralPath $bad -Encoding UTF8
  $failed=$false;try{& $serializer -InputPath $bad|Out-Null}catch{$failed=$true}
  if(-not $failed){throw 'Unsupported projection schema must fail closed'}

  $badSignal=Join-Path $root 'bad-signal.json'
  $projection.signals.cpu.observed_at_utc=$null
  $projection|ConvertTo-Json -Depth 12|Set-Content -LiteralPath $badSignal -Encoding UTF8
  $failed=$false;try{& $serializer -InputPath $badSignal|Out-Null}catch{$failed=$true}
  if(-not $failed){throw 'Malformed signal must fail closed'}

  Write-Host 'EAGLE health history G6-A serializer tests: PASS'
}
finally{Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue}
