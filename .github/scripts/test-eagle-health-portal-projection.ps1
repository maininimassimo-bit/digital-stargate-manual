Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$script = Join-Path $repo 'scripts\telemetry\Export-EagleHealthPortalProjection.ps1'
$root = Join-Path ([IO.Path]::GetTempPath()) ('dsg-g7b-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root -Force | Out-Null
try {
    $input = Join-Path $root 'eagle-health.json'
    $output = Join-Path $root 'eagle-health-portal.json'
    $source = [ordered]@{
        schema_version='1.0'; component='DSG.EagleHostHealthCollector'; computer='EAGLE30154';
        observed_at_utc='2026-09-04T16:37:19.443Z'; fresh_until_utc='2026-09-04T16:39:19.443Z'; quality='CURRENT'; correlation_id='test-correlation';
        summary=[ordered]@{state='UNKNOWN';reasons=@([ordered]@{code='POLICY_NOT_ACTIVATED'})};
        signals=[ordered]@{
            cpu=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T16:37:19.443Z';fresh_until_utc='2026-09-04T16:39:19.443Z';source='Win32_Processor';cadence_class='FAST';reason=$null;data=[ordered]@{model='CPU';physical_cores=4;logical_processors=8;load_pct=12;window_avg_pct=$null;window_peak_pct=$null;temperature_c=$null}}
            memory=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T16:37:19.443Z';fresh_until_utc='2026-09-04T16:39:19.443Z';source='Win32_OperatingSystem';cadence_class='FAST';reason=$null;data=[ordered]@{total_physical_bytes=1000;available_physical_bytes=400;available_ratio=0.4;memory_pressure=$null}}
            storage=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T16:37:19.443Z';fresh_until_utc='2026-09-04T16:39:19.443Z';source='Win32_LogicalDisk/Get-PhysicalDisk';cadence_class='MEDIUM';reason=$null;data=[ordered]@{logical_disks=@([ordered]@{device_id='C:';volume_name='OS';filesystem='NTFS';size_bytes=1000;free_bytes=300;free_ratio=0.3;free_pct=30});physical_disks=@([ordered]@{friendly_name='Disk';media_type='SSD';bus_type='SATA';health_status='Healthy';operational_status=@('OK');size_bytes=1000});reliability=[ordered]@{available=$false;temperature_c=$null;temperature_max_c=$null;wear_pct=$null;reason='UNAVAILABLE_UNLESS_SEPARATELY_VERIFIED'}}}
            uptime=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T16:37:19.443Z';fresh_until_utc='2026-09-04T16:39:19.443Z';source='Win32_OperatingSystem';cadence_class='MEDIUM';reason=$null;data=[ordered]@{last_boot_at_utc='2026-09-01T00:00:00.000Z';uptime_seconds=100;unexpected_reboot_observed=$null}}
            time_sync=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T16:37:19.443Z';fresh_until_utc='2026-09-04T16:39:19.443Z';source='W32Time service state';cadence_class='MEDIUM';reason=$null;data=[ordered]@{service_state='Running';time_source=$null;stratum=$null;last_successful_sync_utc=$null;offset_ms=$null}}
            processes=[ordered]@{state='OBSERVED';quality='CURRENT';observed_at_utc='2026-09-04T16:37:19.443Z';fresh_until_utc='2026-09-04T16:39:19.443Z';source='Windows process table';cadence_class='FAST';reason=$null;data=[ordered]@{items=@([ordered]@{name='NINA';pid=1234})}}
        };
        diagnostics=[ordered]@{collector_mode='READ_ONLY';safety_authority='OUTSIDE_SCOPE';automatic_remediation=$false}
    }
    $source | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $input -Encoding UTF8
    & $script -InputPath $input -OutputPath $output | Out-Null
    $p = Get-Content -LiteralPath $output -Raw | ConvertFrom-Json
    if ($p.component -ne 'DSG.EagleHealthPortalProjection') { throw 'Wrong component.' }
    if ($p.summary.state -ne 'UNAVAILABLE' -or $p.summary.reason -ne 'REQUIRED_SIGNAL_NOT_CURRENT') { throw 'Fail-closed summary changed.' }
    if ($p.host -ne 'EAGLE30154') { throw 'Host provenance lost.' }
    if ($null -eq $p.signals.cpu -or $null -eq $p.signals.storage) { throw 'Required signals missing.' }
    if ($null -ne $p.signals.PSObject.Properties['processes']) { throw 'Process details leaked to public projection.' }
    if ($p.signals.storage.data.logical_disks[0].free_pct -ne 30) { throw 'Logical capacity not preserved.' }
    if ($p.signals.storage.data.physical_disks[0].health_status -ne 'Healthy') { throw 'Physical health not preserved.' }
    if ($p.diagnostics.projection_mode -ne 'READ_ONLY_PUBLIC' -or $p.diagnostics.automatic_remediation -ne $false) { throw 'Read-only boundary changed.' }

    $bad = Join-Path $root 'bad.json'
    $source.component = 'WRONG'
    $source | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $bad -Encoding UTF8
    $failed = $false
    try { & $script -InputPath $bad -OutputPath (Join-Path $root 'bad-out.json') | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Invalid source component was accepted.' }

    Write-Host 'PASS: G7-B EAGLE health portal projection contract.'
}
finally { Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue }
