Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$adapter = Join-Path $repo 'scripts\telemetry\Export-CloudWatcherObservatoryStatus.ps1'
$temp = Join-Path ([IO.Path]::GetTempPath()) ('dsg-cloudwatcher-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temp | Out-Null

try {
    $nowRome = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::UtcNow, 'Europe/Rome')
    $date = $nowRome.ToString('yyyy-MM-dd')
    $time = $nowRome.ToString('HH:mm:ss')
    $header = '"Date","Time","Cloud Condition","Rain Condition","Brightness Condition","Wind Condition","Switch Status","Safe Status"'

    foreach ($case in @(
        @{ Name = 'safe'; Status = 'Safe'; Expected = 'SAFE' },
        @{ Name = 'unsafe'; Status = 'Unsafe'; Expected = 'UNSAFE' },
        @{ Name = 'unknown'; Status = 'Unexpected'; Expected = 'UNKNOWN' }
    )) {
        $csv = Join-Path $temp ($case.Name + '.csv')
        $json = Join-Path $temp ($case.Name + '.json')
        @($header, ('"{0}","{1}","Clear","Dry","Dark","Calm","Opened","{2}"' -f $date, $time, $case.Status)) | Set-Content -LiteralPath $csv -Encoding UTF8
        & $adapter -CloudWatcherCsv $csv -OutputPath $json -FreshnessSeconds 300 -SourceInstance 'CI'
        $p = Get-Content -LiteralPath $json -Raw | ConvertFrom-Json
        if ($p.systems.weather.state -ne $case.Expected) { throw "Case $($case.Name): weather state $($p.systems.weather.state), expected $($case.Expected)" }
        if ($p.systems.weather.quality -ne 'CURRENT') { throw "Case $($case.Name): expected CURRENT" }
        if ($p.quality -ne 'DEGRADED') { throw "Case $($case.Name): expected DEGRADED payload" }
        if ($p.safety.observed_state -ne 'UNKNOWN') { throw "Case $($case.Name): overall safety must remain UNKNOWN" }
    }

    $staleCsv = Join-Path $temp 'stale.csv'
    $staleJson = Join-Path $temp 'stale.json'
    @($header, '"2020-01-01","00:00:00","Clear","Dry","Dark","Calm","Opened","Safe"') | Set-Content -LiteralPath $staleCsv -Encoding UTF8
    & $adapter -CloudWatcherCsv $staleCsv -OutputPath $staleJson -FreshnessSeconds 30 -SourceInstance 'CI'
    $stale = Get-Content -LiteralPath $staleJson -Raw | ConvertFrom-Json
    if ($stale.systems.weather.state -ne 'UNKNOWN' -or $stale.systems.weather.quality -ne 'STALE' -or $stale.quality -ne 'STALE') { throw 'Stale case did not fail closed.' }

    Write-Output 'CloudWatcher telemetry adapter tests: PASS'
}
finally {
    Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
}
