Set-StrictMode -Version 2.0
$ErrorActionPreference='Stop'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$script=Join-Path $repo 'scripts\telemetry\Export-EagleHealthPortalHistoryProjection.ps1'
$root=Join-Path ([IO.Path]::GetTempPath()) ('dsg-g7c-'+[guid]::NewGuid().ToString('N'))
$history=Join-Path $root 'history\2026\09'; New-Item -ItemType Directory -Path $history -Force|Out-Null
try {
  $segment=Join-Path $history 'eagle-health-2026-09.ndjson'
  $lines=@()
  1..5 | ForEach-Object {
    $i=$_; $signal=if($i -eq 5){'processes'}else{'cpu'}
    $r=[ordered]@{history_schema_version='1.0';record_id=('id'+$i);host='EAGLE30154';component='DSG.EagleHostHealthCollector';projection_schema_version='1.0';projection_correlation_id='c';projection_observed_at_utc=('2026-09-04T16:0'+$i+':00.000Z');signal_id=$signal;signal_state='OBSERVED';quality='CURRENT';observed_at_utc=('2026-09-04T16:0'+$i+':00.000Z');fresh_until_utc=('2026-09-04T16:0'+$i+':30.000Z');source='test';cadence_class='FAST';reason=$null;data=if($signal -eq 'cpu'){[ordered]@{load_pct=$i;window_avg_pct=$null;window_peak_pct=$null;temperature_c=$null}}else{[ordered]@{items=@([ordered]@{name='NINA';pid=1234})}};retention_deletion_enabled=$false;historical_records_deleted=0}
    $lines+=($r|ConvertTo-Json -Depth 10 -Compress)
  }
  [IO.File]::WriteAllLines($segment,$lines,(New-Object Text.UTF8Encoding($false)))
  $out=Join-Path $root 'public.json'; & $script -HistoryRoot (Join-Path $root 'history') -OutputPath $out -MaxRecords 3|Out-Null
  $p=Get-Content $out -Raw|ConvertFrom-Json
  if($p.component -ne 'DSG.EagleHealthPortalHistoryProjection' -or $p.bounded -ne $true){throw 'Invalid projection contract.'}
  if($p.records_returned -ne 3){throw 'MaxRecords not enforced.'}
  if(@($p.records|Where-Object{$_.signal_id -eq 'processes'}).Count -ne 0){throw 'Non-public signal leaked.'}
  if($p.records[0].record_id -ne 'id2' -or $p.records[2].record_id -ne 'id4'){throw 'Expected latest bounded records id2-id4.'}
  if($p.diagnostics.retention_deletion_enabled -ne $false -or $p.diagnostics.historical_records_deleted -ne 0){throw 'Retention invariant changed.'}
  Write-Host 'PASS: G7-C bounded EAGLE health history projection.'
}
finally{Remove-Item $root -Recurse -Force -ErrorAction SilentlyContinue}
