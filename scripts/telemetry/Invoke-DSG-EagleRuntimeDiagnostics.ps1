[CmdletBinding()]
param(
    [string]$OutputPath = (Join-Path $env:TEMP 'dsg-eagle-runtime-diagnostics.json'),
    [string]$RepositoryRoot = '',
    [string]$TelemetryRoot = '',
    [string]$CloudWatcherCsv = '',
    [string]$NinaProjection = '',
    [string]$Phd2LogRoot = '',
    [string]$NinaLogRoot = '',
    [string]$ScheduledTaskName = 'Digital StarGate - Daily Session Upload'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# DSG-RTA-ADD-001: diagnostic-only collector.
# This script performs local read-only inspection. It does not:
# - call network endpoints or GitHub;
# - invoke NINA, PHD2, CloudWatcher, ASCOM, CPWI or hardware APIs;
# - start/stop processes or services;
# - create scheduled tasks;
# - change configuration, permissions, secrets or device state.
# It writes only the requested diagnostic report.

function Get-SafeString {
    param([AllowNull()][object]$Value)
    if ($null -eq $Value) { return $null }
    return ([string]$Value)
}

function Get-PathSnapshot {
    param([AllowNull()][string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return [ordered]@{
            supplied = $false
            path = $null
            exists = $false
            kind = $null
            last_write_time_utc = $null
            length_bytes = $null
            sha256 = $null
            error = $null
        }
    }

    try {
        $item = Get-Item -LiteralPath $Path -ErrorAction Stop
        $hash = $null
        if ($item.PSIsContainer -eq $false) {
            try { $hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256 -ErrorAction Stop).Hash } catch { $hash = $null }
        }
        return [ordered]@{
            supplied = $true
            path = $Path
            exists = $true
            kind = if ($item.PSIsContainer) { 'directory' } else { 'file' }
            last_write_time_utc = $item.LastWriteTimeUtc.ToString('o')
            length_bytes = if ($item.PSIsContainer) { $null } else { [int64]$item.Length }
            sha256 = $hash
            error = $null
        }
    }
    catch {
        return [ordered]@{
            supplied = $true
            path = $Path
            exists = $false
            kind = $null
            last_write_time_utc = $null
            length_bytes = $null
            sha256 = $null
            error = $_.Exception.Message
        }
    }
}

function Get-DirectorySnapshot {
    param([AllowNull()][string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return [ordered]@{
            supplied = $false
            path = $null
            exists = $false
            file_count = $null
            latest_files = @()
            error = $null
        }
    }

    try {
        $files = @(Get-ChildItem -LiteralPath $Path -File -ErrorAction Stop)
        $latest = @(
            $files |
                Sort-Object LastWriteTimeUtc -Descending |
                Select-Object -First 10 |
                ForEach-Object {
                    [ordered]@{
                        name = $_.Name
                        length_bytes = [int64]$_.Length
                        last_write_time_utc = $_.LastWriteTimeUtc.ToString('o')
                    }
                }
        )
        return [ordered]@{
            supplied = $true
            path = $Path
            exists = $true
            file_count = $files.Count
            latest_files = $latest
            error = $null
        }
    }
    catch {
        return [ordered]@{
            supplied = $true
            path = $Path
            exists = $false
            file_count = $null
            latest_files = @()
            error = $_.Exception.Message
        }
    }
}

function Get-ProcessSnapshot {
    param([Parameter(Mandatory = $true)][string[]]$Names)

    $items = @()
    foreach ($name in $Names) {
        $processes = @(Get-Process -Name $name -ErrorAction SilentlyContinue)
        $items += [ordered]@{
            name = $name
            running = ($processes.Count -gt 0)
            count = $processes.Count
            ids = @($processes | Select-Object -ExpandProperty Id)
            # Deliberately omit command lines, user names and environment data.
        }
    }
    return $items
}

function Get-ServiceSnapshot {
    param([Parameter(Mandatory = $true)][string[]]$Names)

    $items = @()
    foreach ($name in $Names) {
        $services = @(Get-Service -Name $name -ErrorAction SilentlyContinue)
        $items += [ordered]@{
            name = $name
            found = ($services.Count -gt 0)
            states = @($services | ForEach-Object { [string]$_.Status })
            start_types = @($services | ForEach-Object { [string]$_.StartType })
        }
    }
    return $items
}

function Get-ScheduledTaskSnapshot {
    param([Parameter(Mandatory = $true)][string]$Name)

    try {
        $task = Get-ScheduledTask -TaskName $Name -ErrorAction Stop
        $info = Get-ScheduledTaskInfo -TaskName $Name -ErrorAction Stop
        return [ordered]@{
            found = $true
            task_name = $task.TaskName
            task_path = $task.TaskPath
            state = [string]$task.State
            last_run_time = $info.LastRunTime.ToUniversalTime().ToString('o')
            last_task_result = [int64]$info.LastTaskResult
            next_run_time = $info.NextRunTime.ToUniversalTime().ToString('o')
            # Do not expose action arguments, principals or credential-related fields.
        }
    }
    catch {
        return [ordered]@{
            found = $false
            task_name = $Name
            task_path = $null
            state = $null
            last_run_time = $null
            last_task_result = $null
            next_run_time = $null
            error = $_.Exception.Message
        }
    }
}

function Get-JsonProjectionSnapshot {
    param([AllowNull()][string]$Path)

    $base = Get-PathSnapshot -Path $Path
    if (-not $base.exists -or $base.kind -ne 'file') {
        return [ordered]@{
            file = $base
            parseable = $false
            schema_version = $null
            observed_at_utc = $null
            fresh_until_utc = $null
            quality = $null
            state = $null
            error = $base.error
        }
    }

    try {
        $json = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop
        return [ordered]@{
            file = $base
            parseable = $true
            schema_version = Get-SafeString $json.schema_version
            observed_at_utc = Get-SafeString $json.observed_at_utc
            fresh_until_utc = Get-SafeString $json.fresh_until_utc
            quality = Get-SafeString $json.quality
            state = Get-SafeString $json.state
            error = $null
        }
    }
    catch {
        return [ordered]@{
            file = $base
            parseable = $false
            schema_version = $null
            observed_at_utc = $null
            fresh_until_utc = $null
            quality = $null
            state = $null
            error = $_.Exception.Message
        }
    }
}

$now = [datetime]::UtcNow
$os = Get-CimInstance -ClassName Win32_OperatingSystem
$computer = Get-CimInstance -ClassName Win32_ComputerSystem
$ps = $PSVersionTable

$report = [ordered]@{
    schema_version = '1.0'
    diagnostic_id = [guid]::NewGuid().ToString('D')
    generated_at_utc = $now.ToString('o')
    contract = [ordered]@{
        addendum = 'DSG-RTA-ADD-001'
        mode = 'READ_ONLY_DIAGNOSTICS'
        network_calls = $false
        hardware_commands = $false
        configuration_changes = $false
        secret_access = $false
        safety_authority = 'LOCAL_PHYSICAL_INTERLOCKS'
    }
    host = [ordered]@{
        computer_name = $env:COMPUTERNAME
        manufacturer = Get-SafeString $computer.Manufacturer
        model = Get-SafeString $computer.Model
        os_caption = Get-SafeString $os.Caption
        os_version = Get-SafeString $os.Version
        powershell_version = Get-SafeString $ps.PSVersion
        is_elevated = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    }
    processes = Get-ProcessSnapshot -Names @('NINA','phd2','AAG_CloudWatcher','ASCOM.TS.Shelter')
    services = Get-ServiceSnapshot -Names @('Spooler','Winmgmt')
    scheduled_task = Get-ScheduledTaskSnapshot -Name $ScheduledTaskName
    paths = [ordered]@{
        repository_root = Get-PathSnapshot -Path $RepositoryRoot
        telemetry_root = Get-PathSnapshot -Path $TelemetryRoot
        cloudwatcher_csv = Get-PathSnapshot -Path $CloudWatcherCsv
        nina_projection = Get-JsonProjectionSnapshot -Path $NinaProjection
        nina_logs = Get-DirectorySnapshot -Path $NinaLogRoot
        phd2_logs = Get-DirectorySnapshot -Path $Phd2LogRoot
    }
    runtime_files = [ordered]@{
        producer_health = Get-JsonProjectionSnapshot -Path (if ([string]::IsNullOrWhiteSpace($TelemetryRoot)) { $null } else { Join-Path $TelemetryRoot 'producer-health.json' })
        observatory_status = Get-JsonProjectionSnapshot -Path (if ([string]::IsNullOrWhiteSpace($TelemetryRoot)) { $null } else { Join-Path $TelemetryRoot 'observatory-status.json' })
    }
    limitations = @(
        'This report does not prove runtime compatibility or safety readiness.',
        'This report does not inspect secrets, tokens, passwords or credential stores.',
        'Unknown, missing or stale data must remain fail-closed.',
        'No runtime activation is performed by this script.'
    )
}

$parent = Split-Path -Parent $OutputPath
if (-not [string]::IsNullOrWhiteSpace($parent) -and -not (Test-Path -LiteralPath $parent -PathType Container)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
Write-Output ('DSG read-only diagnostics written: {0}' -f $OutputPath)
Write-Output ('Host: {0}; NINA/PHD2/CloudWatcher processes inspected; no network or hardware command executed.' -f $env:COMPUTERNAME)
