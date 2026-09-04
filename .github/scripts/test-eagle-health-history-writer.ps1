$ErrorActionPreference = 'Stop'
$root = Join-Path ([IO.Path]::GetTempPath()) ('dsg-g6b-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root -Force | Out-Null
try {
    $input = Join-Path $root 'eagle-health.json'
    $history = Join-Path $root 'history'
    $evidence = Join-Path $history 'evidence'
    $writer = Join-Path $PSScriptRoot '..\..\scripts\telemetry\Write-EagleHealthHistory.ps1'
    $projection = [ordered]@{
        schema_version='1.0'; component='DSG.EagleHostHealthCollector'; computer='EAGLE30154';
        observed_at_utc='2026-09-04T18:00:00.000Z'; fresh_until_utc='2026-09-04T18:02:00.000Z'; quality='CURRENT'; correlation_id='g6b-test';
        summary=[ordered]@{state='UNKNOWN';reasons=@()}; cadence_class='MIXED';
        signals=[ordered]@{
            cpu=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T18:00:00.000Z';fresh_until_utc='2026-09-04T18:02:00.000Z';source='Win32_Processor';cadence_class='FAST';reason=$null;data=[ordered]@{load_pct=12.0}}
            uptime=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T18:00:01.000Z';fresh_until_utc='2026-09-04T18:02:01.000Z';source='Win32_OperatingSystem';cadence_class='MEDIUM';reason=$null;data=[ordered]@{uptime_seconds=100}}
        };
        diagnostics=[ordered]@{collector_mode='READ_ONLY';safety_authority='OUTSIDE_SCOPE';automatic_remediation=$false}
    }
    [IO.File]::WriteAllText($input, ($projection|ConvertTo-Json -Depth 10), (New-Object Text.UTF8Encoding($false)))

    $segment = & $writer -InputPath $input -HistoryRoot $history -EvidenceRoot $evidence -LockName ('G6B.'+[guid]::NewGuid())
    if (-not (Test-Path -LiteralPath $segment)) { throw 'History segment not created.' }
    $lines1 = @([IO.File]::ReadAllLines($segment))
    if ($lines1.Count -ne 2) { throw "Expected 2 records, got $($lines1.Count)." }
    foreach($line in $lines1){ $r=$line|ConvertFrom-Json; if($r.history_schema_version -ne '1.0'){throw 'History schema mismatch.'}; if($r.historical_records_deleted -ne 0){throw 'Deletion invariant violated.'} }

    $null = & $writer -InputPath $input -HistoryRoot $history -EvidenceRoot $evidence -LockName ('G6B.'+[guid]::NewGuid())
    $lines2 = @([IO.File]::ReadAllLines($segment))
    if ($lines2.Count -ne 2) { throw 'Duplicate replay appended records.' }

    $checkpoint = Get-Content -LiteralPath (Join-Path $history 'checkpoints\latest.json') -Raw | ConvertFrom-Json
    if ($checkpoint.records_appended -ne 0 -or $checkpoint.records_duplicate_skipped -ne 2) { throw 'Checkpoint duplicate accounting mismatch.' }
    if ($checkpoint.retention_deletion_enabled -ne $false -or $checkpoint.historical_records_deleted -ne 0) { throw 'Checkpoint deletion invariant violated.' }

    $before = [IO.File]::ReadAllText($segment)
    [IO.File]::WriteAllText($input, '{bad-json', (New-Object Text.UTF8Encoding($false)))
    $failed=$false
    try { $null = & $writer -InputPath $input -HistoryRoot $history -EvidenceRoot $evidence -LockName ('G6B.'+[guid]::NewGuid()) } catch { $failed=$true }
    if (-not $failed) { throw 'Malformed input did not fail closed.' }
    $after = [IO.File]::ReadAllText($segment)
    if ($before -ne $after) { throw 'Malformed input modified valid history.' }

    $evidenceFiles=@(Get-ChildItem -LiteralPath $evidence -Filter '*.json')
    if($evidenceFiles.Count -lt 3){throw 'Expected cycle evidence files.'}
    foreach($f in $evidenceFiles){$ev=Get-Content -LiteralPath $f.FullName -Raw|ConvertFrom-Json;if($ev.historical_records_deleted -ne 0){throw 'Evidence deletion invariant violated.'}}

    Write-Host 'EAGLE health history writer tests passed.'
}
finally { Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue }
