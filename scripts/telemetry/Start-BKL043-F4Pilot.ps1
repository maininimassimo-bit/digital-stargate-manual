[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^https://[a-z0-9-]+-[a-z0-9-]+\.a\.run\.app$')]
    [string]$ReceiverUrl
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:OutboxRoot = 'D:\DigitalStarGate\Telemetry\Outbox'
$script:MaximumReceiptBytes = 4096
$script:MaximumOutboxBytes = 16MB
$script:MaximumQueueAge = [TimeSpan]::FromHours(24)
$script:SampleInterval = [TimeSpan]::FromSeconds(60)
$script:FreshHeartbeatSeconds = 60
$script:ExpectedHost = 'EAGLE30154'
$script:ExpectedTimezone = 'W. Europe Standard Time'
$script:ApprovedAccount = 'maininimassimo@gmail.com'
$script:InvokerServiceAccount = 'dsg-bkl043-f4-eagle-invoker@digital-stargate-telemetry.iam.gserviceaccount.com'
$script:ApprovedStart = [DateTimeOffset]::Parse('2026-09-29T10:00:00+02:00')
$script:ApprovedEnd = [DateTimeOffset]::Parse('2026-09-29T12:00:00+02:00')
$script:ReceiverUrl = $ReceiverUrl.TrimEnd('/')
$script:ReceiverEndpoint = $script:ReceiverUrl + '/v1/receipts'
$script:RetryState = @{}
$script:TaskNames = @(
    'Digital StarGate - Daily Session Upload',
    'Digital StarGate - OneDrive Export',
    'DigitalStarGate-EagleHealthTelemetry'
)
$script:ProjectionPath = Join-Path $env:LOCALAPPDATA 'DigitalStarGate\telemetry\nina-observatory-status.json'
$script:GCloud = Join-Path $env:LOCALAPPDATA 'Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd'

function Convert-LocalTimeToUtc([datetime]$Value, [TimeZoneInfo]$TimeZone) {
    $unspecified = [datetime]::SpecifyKind($Value, [DateTimeKind]::Unspecified)
    if ($TimeZone.IsInvalidTime($unspecified) -or $TimeZone.IsAmbiguousTime($unspecified)) {
        return $null
    }
    return [TimeZoneInfo]::ConvertTimeToUtc($unspecified, $TimeZone).ToString('yyyy-MM-ddTHH:mm:ssZ')
}

function Get-ClockQuality {
    $timeZone = Get-TimeZone
    if ($timeZone.Id -ne $script:ExpectedTimezone) {
        return [pscustomobject]@{ Valid = $false; TimeZone = $timeZone.Id; OffsetMinutes = [int][DateTimeOffset]::Now.Offset.TotalMinutes; LastSyncUtc = $null; RootDispersionSeconds = $null }
    }

    $statusLines = & "$env:windir\System32\w32tm.exe" /query /status 2>$null
    if ($LASTEXITCODE -ne 0) {
        return [pscustomobject]@{ Valid = $false; TimeZone = $timeZone.Id; OffsetMinutes = [int][DateTimeOffset]::Now.Offset.TotalMinutes; LastSyncUtc = $null; RootDispersionSeconds = $null }
    }
    $status = $statusLines -join "`n"
    $syncMatch = [regex]::Match($status, '(?im)^\s*(?:Last Successful Sync Time|Data e ora dell''ultima sincronizzazione riuscita)\s*:\s*(.+?)\s*$')
    $dispersionMatch = [regex]::Match($status, '(?im)^\s*(?:Root Dispersion|Dispersione radice)\s*:\s*([0-9]+(?:[.,][0-9]+)?)\s*s?\s*$')
    if (-not $syncMatch.Success -or -not $dispersionMatch.Success) {
        return [pscustomobject]@{ Valid = $false; TimeZone = $timeZone.Id; OffsetMinutes = [int][DateTimeOffset]::Now.Offset.TotalMinutes; LastSyncUtc = $null; RootDispersionSeconds = $null }
    }

    $syncLocal = [datetime]::MinValue
    $styles = [Globalization.DateTimeStyles]::AllowWhiteSpaces
    $parsed = [datetime]::TryParse($syncMatch.Groups[1].Value, [Globalization.CultureInfo]::CurrentCulture, $styles, [ref]$syncLocal)
    if (-not $parsed) {
        $parsed = [datetime]::TryParse($syncMatch.Groups[1].Value, [Globalization.CultureInfo]::InvariantCulture, $styles, [ref]$syncLocal)
    }
    if (-not $parsed) {
        return [pscustomobject]@{ Valid = $false; TimeZone = $timeZone.Id; OffsetMinutes = [int][DateTimeOffset]::Now.Offset.TotalMinutes; LastSyncUtc = $null; RootDispersionSeconds = $null }
    }

    $syncUtc = Convert-LocalTimeToUtc $syncLocal $timeZone
    $dispersion = [double]::Parse(($dispersionMatch.Groups[1].Value -replace ',', '.'), [Globalization.CultureInfo]::InvariantCulture)
    if ($null -eq $syncUtc) { return [pscustomobject]@{ Valid = $false; TimeZone = $timeZone.Id; OffsetMinutes = [int][DateTimeOffset]::Now.Offset.TotalMinutes; LastSyncUtc = $null; RootDispersionSeconds = $dispersion } }
    $ageHours = ([DateTimeOffset]::UtcNow - [DateTimeOffset]::Parse($syncUtc)).TotalHours
    $valid = ($null -ne $syncUtc -and $ageHours -ge 0 -and $ageHours -le 24 -and $dispersion -le 1)
    return [pscustomobject]@{
        Valid = $valid
        TimeZone = $timeZone.Id
        OffsetMinutes = [int][DateTimeOffset]::Now.Offset.TotalMinutes
        LastSyncUtc = $syncUtc
        RootDispersionSeconds = [math]::Round($dispersion, 6)
    }
}

function Get-RunningTaskProcessPresence([string]$TaskName) {
    $service = New-Object -ComObject 'Schedule.Service'
    $service.Connect()
    $task = $service.GetFolder('\').GetTask($TaskName)
    $instances = @($task.GetInstances(0))
    foreach ($instance in $instances) {
        $processId = [int]$instance.EnginePID
        if ($processId -gt 0) {
            $process = Get-CimInstance Win32_Process -Filter "ProcessId = $processId" -ErrorAction SilentlyContinue
            if ($null -ne $process) { return $true }
        }
    }
    return $false
}

function Get-TaskSignals([TimeZoneInfo]$TimeZone) {
    $items = @()
    foreach ($name in $script:TaskNames) {
        $task = Get-ScheduledTask -TaskPath '\' -TaskName $name
        $info = Get-ScheduledTaskInfo -InputObject $task
        $lastRunUtc = $null
        if ($info.LastRunTime -and $info.LastRunTime -ne [datetime]::MinValue) {
            $lastRunUtc = Convert-LocalTimeToUtc $info.LastRunTime $TimeZone
        }
        $result = [int]$info.LastTaskResult
        $resultHex = '0x{0:X8}' -f [uint32]$result
        $interpretation = if ($result -eq 0) { 'SUCCESS' } else { 'NONZERO_REVIEW' }
        $items += [pscustomobject][ordered]@{
            name = $name
            state = [string]$task.State
            last_task_result = $result
            result_hex = $resultHex
            outcome_interpretation = $interpretation
            last_run_utc = $lastRunUtc
            process_present = (Get-RunningTaskProcessPresence $name)
        }
    }
    return $items
}

function Get-ProjectionHeartbeat([datetime]$NowUtc, [bool]$ClockValid) {
    try {
        $item = Get-Item -LiteralPath $script:ProjectionPath -ErrorAction Stop
        $writeUtc = $item.LastWriteTimeUtc
        if (-not $ClockValid) { return [pscustomobject]@{ exists = $true; last_write_utc = $writeUtc.ToString('yyyy-MM-ddTHH:mm:ssZ'); age_seconds = $null; freshness = 'UNKNOWN' } }
        $age = [math]::Round(($NowUtc - $writeUtc).TotalSeconds, 1)
        if ($age -lt 0) {
            return [pscustomobject]@{ exists = $true; last_write_utc = $writeUtc.ToString('yyyy-MM-ddTHH:mm:ssZ'); age_seconds = $null; freshness = 'UNKNOWN' }
        }
        return [pscustomobject]@{
            exists = $true
            last_write_utc = $writeUtc.ToString('yyyy-MM-ddTHH:mm:ssZ')
            age_seconds = $age
            freshness = if ($age -le $script:FreshHeartbeatSeconds) { 'FRESH' } else { 'STALE' }
        }
    } catch {
        return [pscustomobject]@{ exists = $false; last_write_utc = $null; age_seconds = $null; freshness = 'UNKNOWN' }
    }
}

function New-Receipt([long]$SequenceId, [object]$Clock) {
    $os = Get-CimInstance Win32_OperatingSystem
    $bootUtc = ([datetime]$os.LastBootUpTime).ToUniversalTime()
    $uptime = [math]::Max(0, [int64]([datetime]::Now - [datetime]$os.LastBootUpTime).TotalSeconds)
    $disks = @(Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:' OR DeviceID='D:'" |
        Sort-Object DeviceID |
        ForEach-Object { [pscustomobject][ordered]@{ device_id = [string]$_.DeviceID; free_bytes = [int64]$_.FreeSpace } })
    if ($disks.Count -ne 2) { throw 'DISK_SOURCE_INCOMPLETE' }

    $nowUtc = [DateTime]::UtcNow
    $sourceTime = if ($Clock.Valid) { $nowUtc.ToString('yyyy-MM-ddTHH:mm:ssZ') } else { $null }
    $lastRunTimeZone = Get-TimeZone
    $tasks = @(Get-TaskSignals $lastRunTimeZone)
    if ($tasks.Count -ne 3) { throw 'TASK_SIGNAL_COUNT_INVALID' }
    $signals = [ordered]@{
        os = [ordered]@{
            caption = [string]$os.Caption
            version = [string]$os.Version
            build = [string]$os.BuildNumber
            architecture = [string]$os.OSArchitecture
        }
        uptime_seconds = $uptime
        disks = $disks
        tasks = $tasks
        nina_plugin_projection = (Get-ProjectionHeartbeat $nowUtc $Clock.Valid)
    }
    return [ordered]@{
        schema_version = 1
        record_id = [guid]::NewGuid().ToString('D')
        source_id = 'dsg-eagle-f4'
        host_identity = $script:ExpectedHost
        boot_epoch_id = $bootUtc.ToString('yyyy-MM-ddTHH:mm:ssZ')
        sequence_id = $SequenceId
        source_observed_at_utc = $sourceTime
        source_clock_quality = if ($Clock.Valid) { 'VALID' } else { 'UNKNOWN' }
        signals = $signals
    }
}

function Get-QueueFiles {
    if (-not (Test-Path -LiteralPath $script:OutboxRoot -PathType Container)) {
        New-Item -ItemType Directory -Path $script:OutboxRoot -Force | Out-Null
    }
    $temporary = @(Get-ChildItem -LiteralPath $script:OutboxRoot -File -Filter '*.pending')
    if ($temporary.Count -gt 0) { throw 'OUTBOX_UNRECOVERED_TEMP' }
    return @(Get-ChildItem -LiteralPath $script:OutboxRoot -File -Filter '*.json' | Sort-Object Name)
}

function Test-QueueAllowsAdmission([object[]]$Files, [datetime]$NowUtc) {
    $totalBytes = 0L
    foreach ($file in $Files) { $totalBytes += [int64]$file.Length }
if ($Files.Count -ge 1440 -or ($totalBytes + $script:MaximumReceiptBytes) -gt $script:MaximumOutboxBytes) {
        return [pscustomobject]@{ Allowed = $false; Reason = 'OUTBOX_FULL' }
    }
    if ($Files.Count -gt 0) {
        foreach ($file in $Files) {
            try {
                $queued = Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json
                if ($queued.source_clock_quality -ne 'VALID' -or -not $queued.source_observed_at_utc) {
                    return [pscustomobject]@{ Allowed = $false; Reason = 'QUEUE_AGE_UNKNOWN' }
                }
                $age = $NowUtc - [DateTime]::Parse($queued.source_observed_at_utc).ToUniversalTime()
                if ($age.TotalHours -gt 24) {
                    return [pscustomobject]@{ Allowed = $false; Reason = 'QUEUE_STALE' }
                }
            } catch {
                return [pscustomobject]@{ Allowed = $false; Reason = 'QUEUE_UNREADABLE' }
            }
        }
    }
    return [pscustomobject]@{ Allowed = $true; Reason = 'OK' }
}

function Save-Receipt([object]$Receipt) {
    $json = $Receipt | ConvertTo-Json -Depth 12 -Compress
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes($json)
    if ($bytes.Length -gt $script:MaximumReceiptBytes) { throw 'RECEIPT_SIZE_LIMIT' }
    $finalPath = Join-Path $script:OutboxRoot ($Receipt.record_id + '.json')
    $temporaryPath = Join-Path $script:OutboxRoot ([guid]::NewGuid().ToString('N') + '.pending')
    $stream = [IO.FileStream]::new($temporaryPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None, 4096, [IO.FileOptions]::WriteThrough)
    try {
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush($true)
    } finally {
        $stream.Dispose()
    }
    [IO.File]::Move($temporaryPath, $finalPath)
}

function Get-IdentityToken {
    if (-not (Test-Path -LiteralPath $script:GCloud -PathType Leaf)) { throw 'GCLOUD_NOT_FOUND' }
    $active = & $script:GCloud auth list --filter=status:ACTIVE --format='value(account)' 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]$active -ne $script:ApprovedAccount) { throw 'GCLOUD_ACTIVE_ACCOUNT_MISMATCH' }
    $token = & $script:GCloud auth print-identity-token "--impersonate-service-account=$($script:InvokerServiceAccount)" "--audiences=$($script:ReceiverUrl)" 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace([string]$token)) { throw 'IDENTITY_TOKEN_UNAVAILABLE' }
    return [string]$token
}

function Send-Pending([object[]]$Files, [datetime]$NowUtc) {
    foreach ($file in $Files) {
        if ([DateTimeOffset]::Now -ge $script:ApprovedEnd.AddSeconds(-30)) { break }
        $key = $file.Name
        if ($script:RetryState.ContainsKey($key) -and $NowUtc -lt $script:RetryState[$key].NextUtc) { continue }
        try {
            $payload = Get-Content -LiteralPath $file.FullName -Raw
            $record = $payload | ConvertFrom-Json
            $token = Get-IdentityToken
            if ([DateTimeOffset]::Now -ge $script:ApprovedEnd.AddSeconds(-30)) { break }
            $response = Invoke-RestMethod -Method Post -Uri $script:ReceiverEndpoint -TimeoutSec 30 -ContentType 'application/json' -Headers @{ Authorization = "Bearer $token" } -Body $payload
            if ($response.ack -notin @('DURABLE_CREATED', 'DURABLE_DUPLICATE') -or $response.record_id -ne $record.record_id) {
                throw 'INVALID_DURABLE_ACK'
            }
            Remove-Item -LiteralPath $file.FullName -Force
            $script:RetryState.Remove($key)
            Write-Output ('DURABLE_ACK ' + $record.record_id + ' ' + $response.ack)
        } catch {
            $attempt = 1
            if ($script:RetryState.ContainsKey($key)) { $attempt = [int]$script:RetryState[$key].Attempt + 1 }
$delay = [math]::Min(300, [math]::Pow(2, [math]::Min($attempt, 9)))
            $script:RetryState[$key] = [pscustomobject]@{ Attempt = $attempt; NextUtc = $NowUtc.AddSeconds($delay) }
            Write-Output ('RETRY_PENDING ' + $file.BaseName + ' delay_seconds=' + $delay)
        }
    }
}

function Assert-PilotWindow {
    $now = [DateTimeOffset]::Now
    if ($env:COMPUTERNAME -ne $script:ExpectedHost) { throw 'HOST_IDENTITY_MISMATCH' }
    $zone = Get-TimeZone
    if ($zone.Id -ne $script:ExpectedTimezone) { throw 'TIMEZONE_MISMATCH' }
    if ($now -lt $script:ApprovedStart -or $now -ge $script:ApprovedEnd) { throw 'OUTSIDE_APPROVED_WINDOW' }
}

try {
    Assert-PilotWindow
    if (-not ($ReceiverUrl -match '^https://[a-z0-9-]+-[a-z0-9-]+\.a\.run\.app$')) { throw 'RECEIVER_URL_INVALID' }
    Write-Output 'BKL043_F4_PILOT_START'
    $sample = 0
    while ([DateTimeOffset]::Now -lt $script:ApprovedEnd) {
        $nowUtc = [DateTime]::UtcNow
        $clock = Get-ClockQuality
        $files = @(Get-QueueFiles)

        if ($clock.Valid) {
            $admission = Test-QueueAllowsAdmission $files $nowUtc
            if ($admission.Allowed) {
                $receipt = New-Receipt $sample $clock
                Save-Receipt $receipt
                Write-Output ('RECEIPT_QUEUED sequence=' + $sample)
                $files = @(Get-QueueFiles)
            } else {
                Write-Output ('ADMISSION_PAUSED reason=' + $admission.Reason)
            }
        } else {
            Write-Output 'ADMISSION_PAUSED reason=CLOCK_QUALITY_UNKNOWN'
        }

        Send-Pending $files $nowUtc
        $sample++
        $remaining = ($script:SampleInterval - [TimeSpan]::FromSeconds(([DateTime]::UtcNow - $nowUtc).TotalSeconds)).TotalSeconds
        if ($remaining -gt 0) { Start-Sleep -Seconds ([int][math]::Ceiling($remaining)) }
    }
    Write-Output 'BKL043_F4_PILOT_STOPPED_WINDOW_END'
} catch {
    Write-Output 'BKL043_F4_PILOT_STOPPED reason=SEE_OPERATOR_LOCAL_ERROR'
    exit 1
}
