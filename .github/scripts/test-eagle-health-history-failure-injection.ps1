$ErrorActionPreference = 'Stop'
$root = Join-Path ([IO.Path]::GetTempPath()) ('dsg-g6c-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root -Force | Out-Null

function New-Projection([string]$Path,[string]$Schema='1.0',[bool]$IncludeSecond=$true) {
    $signals=[ordered]@{
        cpu=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T19:00:00.000Z';fresh_until_utc='2026-09-04T19:02:00.000Z';source='Win32_Processor';cadence_class='FAST';reason=$null;data=[ordered]@{load_pct=14.0}}
    }
    if($IncludeSecond){$signals['uptime']=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T19:00:01.000Z';fresh_until_utc='2026-09-04T19:02:01.000Z';source='Win32_OperatingSystem';cadence_class='MEDIUM';reason=$null;data=[ordered]@{uptime_seconds=200}}}
    $p=[ordered]@{schema_version=$Schema;component='DSG.EagleHostHealthCollector';computer='EAGLE30154';observed_at_utc='2026-09-04T19:00:00.000Z';fresh_until_utc='2026-09-04T19:02:00.000Z';quality='CURRENT';correlation_id='g6c-test';summary=[ordered]@{state='UNKNOWN';reasons=@()};cadence_class='MIXED';signals=$signals;diagnostics=[ordered]@{collector_mode='READ_ONLY';safety_authority='OUTSIDE_SCOPE';automatic_remediation=$false}}
    [IO.File]::WriteAllText($Path,($p|ConvertTo-Json -Depth 10),(New-Object Text.UTF8Encoding($false)))
}

try {
    $writer=Join-Path $PSScriptRoot '..\..\scripts\telemetry\Write-EagleHealthHistory.ps1'
    $input=Join-Path $root 'eagle-health.json'
    $history=Join-Path $root 'history'
    $evidence=Join-Path $history 'evidence'

    # Nominal seed and immutable baseline.
    New-Projection $input
    $segment=& $writer -InputPath $input -HistoryRoot $history -EvidenceRoot $evidence -LockName ('G6C.'+[guid]::NewGuid())
    $baseline=[IO.File]::ReadAllText($segment)

    # Missing input must fail closed and preserve prior history.
    Remove-Item -LiteralPath $input -Force
    $failed=$false; try{$null=& $writer -InputPath $input -HistoryRoot $history -EvidenceRoot $evidence -LockName ('G6C.'+[guid]::NewGuid())}catch{$failed=$true}
    if(-not $failed){throw 'Missing input did not fail closed.'}
    if([IO.File]::ReadAllText($segment) -ne $baseline){throw 'Missing input changed prior history.'}

    # Unsupported schema must fail closed.
    New-Projection $input '2.0'
    $failed=$false; try{$null=& $writer -InputPath $input -HistoryRoot $history -EvidenceRoot $evidence -LockName ('G6C.'+[guid]::NewGuid())}catch{$failed=$true}
    if(-not $failed){throw 'Unsupported schema did not fail closed.'}
    if([IO.File]::ReadAllText($segment) -ne $baseline){throw 'Unsupported schema changed prior history.'}

    # Partial signals are valid evidence and must not synthesize absent signals.
    New-Projection $input '1.0' $false
    $partialRoot=Join-Path $root 'partial-history'
    $partialSegment=& $writer -InputPath $input -HistoryRoot $partialRoot -EvidenceRoot (Join-Path $partialRoot 'evidence') -LockName ('G6C.'+[guid]::NewGuid())
    $partial=@([IO.File]::ReadAllLines($partialSegment))
    if($partial.Count -ne 1){throw 'Partial signal projection synthesized or lost signals.'}
    if(($partial[0]|ConvertFrom-Json).signal_id -ne 'cpu'){throw 'Partial signal identity mismatch.'}

    # Corrupt existing segment simulates interrupted/partial prior write. Writer must refuse to replace it.
    New-Projection $input
    [IO.File]::WriteAllText($segment,($baseline + "`n" + '{partial'),(New-Object Text.UTF8Encoding($false)))
    $corruptBefore=[IO.File]::ReadAllText($segment)
    $failed=$false; try{$null=& $writer -InputPath $input -HistoryRoot $history -EvidenceRoot $evidence -LockName ('G6C.'+[guid]::NewGuid())}catch{$failed=$true}
    if(-not $failed){throw 'Corrupt existing segment was not rejected.'}
    if([IO.File]::ReadAllText($segment) -ne $corruptBefore){throw 'Corrupt segment was silently rewritten.'}
    [IO.File]::WriteAllText($segment,$baseline,(New-Object Text.UTF8Encoding($false)))

    # Write failure: use a file as HistoryRoot so directory creation cannot succeed. Existing good history remains untouched.
    $blocked=Join-Path $root 'blocked-root'
    [IO.File]::WriteAllText($blocked,'not-a-directory',(New-Object Text.UTF8Encoding($false)))
    $failed=$false; try{$null=& $writer -InputPath $input -HistoryRoot $blocked -EvidenceRoot $evidence -LockName ('G6C.'+[guid]::NewGuid())}catch{$failed=$true}
    if(-not $failed){throw 'Write failure injection did not fail.'}
    if([IO.File]::ReadAllText($segment) -ne $baseline){throw 'Write failure changed unrelated valid history.'}

    # Non-overlap: hold the named mutex and verify second cycle is skipped.
    $lockName='G6C.NonOverlap.'+[guid]::NewGuid().ToString('N')
    $mutex=New-Object System.Threading.Mutex($false,$lockName)
    $held=$mutex.WaitOne(0,$false)
    if(-not $held){throw 'Could not acquire test mutex.'}
    try{$skip=@(& $writer -InputPath $input -HistoryRoot (Join-Path $root 'overlap') -EvidenceRoot (Join-Path $root 'overlap\evidence') -LockName $lockName)}finally{$mutex.ReleaseMutex();$mutex.Dispose()}
    if(($skip -join '') -ne 'SKIPPED_NON_OVERLAP'){throw 'Concurrent writer was not skipped.'}

    # No test may authorize deletion.
    foreach($f in @(Get-ChildItem -LiteralPath $evidence -Filter '*.json' -ErrorAction SilentlyContinue)){
        $ev=Get-Content -LiteralPath $f.FullName -Raw|ConvertFrom-Json
        if($ev.historical_records_deleted -ne 0 -or $ev.retention_deletion_enabled -ne $false){throw 'Deletion invariant violated in failure evidence.'}
    }
    Write-Host 'EAGLE health history G6-C failure injection tests passed.'
}
finally { Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue }
