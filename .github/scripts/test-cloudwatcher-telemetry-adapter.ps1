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

    # Fixture aligned with the physical EAGLE CloudWatcher schema validated on 2026-08-18.
    $header = '"Date","Time","Cloud Condition","Rain Condition","Brightness Condition","Cloud Value","Cloud Sensor Temperature","Rain Value","Brightness Value","Ambient Temperature","Rain Heating Percentage","Rain Sensor Temperature","Heating Status","Switch Status","Read Cycle","Timeout Errors","Safe Status","Wind Condition","Wind Value","Relative Humidity","Dew Point","Raw IR Temperature","Absolute Pressure","Relative Pressure",'

    function New-CloudWatcherRow {
        param(
            [Parameter(Mandatory = $true)][string]$Date,
            [Parameter(Mandatory = $true)][string]$Time,
            [Parameter(Mandatory = $true)][string]$SafeStatus
        )

        return '"{0}","{1}","Clear","Dry","Dark","5.0","10.0","3328","2","12.5","10%","15.0","","Opened","7.440","0","{2}","Calm","6.8","40","-0.2","-5.0","993.4","1004.5",' -f $Date, $Time, $SafeStatus
    }

    foreach ($case in @(
        @{ Name = 'safe'; Status = 'Safe'; Expected = 'SAFE' },
        @{ Name = 'unsafe'; Status = 'Unsafe'; Expected = 'UNSAFE' },
        @{ Name = 'unknown'; Status = 'Unexpected'; Expected = 'UNKNOWN' }
    )) {
        $csv = Join-Path $temp ($case.Name + '.csv')
        $json = Join-Path $temp ($case.Name + '.json')
        @($header, (New-CloudWatcherRow -Date $date -Time $time -SafeStatus $case.Status)) | Set-Content -LiteralPath $csv -Encoding UTF8

        & $adapter -CloudWatcherCsv $csv -OutputPath $json -FreshnessSeconds 300 -SourceInstance 'CI'
        $p = Get-Content -LiteralPath $json -Raw | ConvertFrom-Json

        if ($p.systems.weather.state -ne $case.Expected) { throw "Case $($case.Name): weather state $($p.systems.weather.state), expected $($case.Expected)" }
        if ($p.systems.weather.quality -ne 'CURRENT') { throw "Case $($case.Name): expected CURRENT" }
        if ($p.quality -ne 'DEGRADED') { throw "Case $($case.Name): expected DEGRADED payload" }
        if ($p.safety.observed_state -ne 'UNKNOWN') { throw "Case $($case.Name): overall safety must remain UNKNOWN" }

        if ([double]$p.systems.weather.temperature_c -ne 12.5) { throw "Case $($case.Name): temperature mapping failed" }
        if ([double]$p.systems.weather.humidity_pct -ne 40.0) { throw "Case $($case.Name): humidity mapping failed" }
        if ([double]$p.systems.weather.dew_point_c -ne -0.2) { throw "Case $($case.Name): dew point mapping failed" }
        if ([double]$p.systems.weather.pressure_hpa -ne 993.4) { throw "Case $($case.Name): pressure mapping failed" }
    }

    $staleCsv = Join-Path $temp 'stale.csv'
    $staleJson = Join-Path $temp 'stale.json'
    @($header, (New-CloudWatcherRow -Date '2020-01-01' -Time '00:00:00' -SafeStatus 'Safe')) | Set-Content -LiteralPath $staleCsv -Encoding UTF8
    & $adapter -CloudWatcherCsv $staleCsv -OutputPath $staleJson -FreshnessSeconds 30 -SourceInstance 'CI'
    $stale = Get-Content -LiteralPath $staleJson -Raw | ConvertFrom-Json
    if ($stale.systems.weather.state -ne 'UNKNOWN' -or $stale.systems.weather.quality -ne 'STALE' -or $stale.quality -ne 'STALE') { throw 'Stale case did not fail closed.' }

    Write-Output 'CloudWatcher telemetry adapter tests: PASS'
}
finally {
    Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
}
