[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence',
    [string]$PortName,
    [ValidateRange(300, 115200)][int]$BaudRate = 9600,
    [ValidateRange(250, 5000)][int]$ReadTimeoutMs = 1500,
    [switch]$ExecuteProbe
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("cloudwatcher-sqm-protocol-probe-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate CloudWatcher SQM protocol probe'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)
Write-Output ('ExecuteProbe: {0}' -f [bool]$ExecuteProbe)

function Get-SerialCandidates {
    $results = @()
    try {
        $results = @(Get-CimInstance -ClassName Win32_SerialPort -ErrorAction Stop | ForEach-Object {
            [pscustomobject]@{
                device_id = $_.DeviceID
                name = $_.Name
                description = $_.Description
                pnp_device_id = $_.PNPDeviceID
                status = $_.Status
            }
        })
    }
    catch { }
    return $results
}

function Get-CloudWatcherProcesses {
    return @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -match '(?i)^AAG_CloudWatcher$|cloudwatcher|aagcw'
    } | Select-Object ProcessName, Id, Path)
}

function Read-Response {
    param(
        [Parameter(Mandatory = $true)][System.IO.Ports.SerialPort]$Port,
        [Parameter(Mandatory = $true)][int]$TimeoutMs
    )

    $deadline = [datetime]::UtcNow.AddMilliseconds($TimeoutMs)
    $buffer = New-Object System.Text.StringBuilder
    $lastData = [datetime]::UtcNow

    while ([datetime]::UtcNow -lt $deadline) {
        $available = $Port.BytesToRead
        if ($available -gt 0) {
            $chunk = $Port.ReadExisting()
            if (-not [string]::IsNullOrEmpty($chunk)) {
                [void]$buffer.Append($chunk)
                $lastData = [datetime]::UtcNow
            }
        }
        elseif ($buffer.Length -gt 0 -and ([datetime]::UtcNow - $lastData).TotalMilliseconds -ge 250) {
            break
        }
        Start-Sleep -Milliseconds 25
    }
    return $buffer.ToString()
}

function Invoke-ReadCommand {
    param(
        [Parameter(Mandatory = $true)][System.IO.Ports.SerialPort]$Port,
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(Mandatory = $true)][int]$TimeoutMs
    )

    $Port.DiscardInBuffer()
    $Port.DiscardOutBuffer()
    $sentAt = [datetime]::UtcNow
    $Port.Write($Command)
    $raw = Read-Response -Port $Port -TimeoutMs $TimeoutMs
    return [pscustomobject]@{
        command = $Command
        sent_at_utc = $sentAt.ToString('o')
        received_at_utc = [datetime]::UtcNow.ToString('o')
        raw_response = $raw
        response_length = $raw.Length
    }
}

function Get-ResponseBlocks {
    param([AllowEmptyString()][string]$Raw)

    if ([string]::IsNullOrEmpty($Raw)) { return @() }
    $blocks = @()
    for ($i = 0; $i -le ($Raw.Length - 15); $i++) {
        if ($Raw[$i] -ne '!') { continue }
        $candidate = $Raw.Substring($i, 15)
        $blocks += [pscustomobject]@{
            offset = $i
            raw = $candidate
            discriminator = if ($candidate.Length -ge 3) { $candidate.Substring(0,3) } else { $candidate }
            payload = if ($candidate.Length -gt 3) { $candidate.Substring(3) } else { '' }
        }
        $i += 14
    }
    return $blocks
}

$serialCandidates = @(Get-SerialCandidates)
$cloudWatcherProcesses = @(Get-CloudWatcherProcesses)
$preflight = [ordered]@{
    serial_candidates = $serialCandidates
    cloudwatcher_processes = $cloudWatcherProcesses
    requested_port = $PortName
    requested_baud_rate = $BaudRate
    execute_probe = [bool]$ExecuteProbe
    process_guard_clear = ($cloudWatcherProcesses.Count -eq 0)
    explicit_port_supplied = (-not [string]::IsNullOrWhiteSpace($PortName))
}

$responses = @()
$probeError = $null
$portOpened = $false
$portClosed = $false

if ($ExecuteProbe) {
    if ([string]::IsNullOrWhiteSpace($PortName)) {
        $probeError = 'ExecuteProbe requires an explicit -PortName. Automatic port selection is forbidden.'
    }
    elseif ($cloudWatcherProcesses.Count -gt 0) {
        $probeError = 'CloudWatcher-related process is running. Probe refused to avoid serial-port contention.'
    }
    elseif ($PortName -notmatch '^COM\d+$') {
        $probeError = 'PortName must be an explicit Windows COM port such as COM3.'
    }
    else {
        $port = $null
        try {
            $port = New-Object System.IO.Ports.SerialPort $PortName,$BaudRate,'None',8,'One'
            $port.ReadTimeout = $ReadTimeoutMs
            $port.WriteTimeout = $ReadTimeoutMs
            $port.DtrEnable = $false
            $port.RtsEnable = $false
            $port.Open()
            $portOpened = $true

            # Protocol v1.3 notes that a 2-second delay after opening is harmless for all hardware
            # and required by pocket CloudWatcher variants.
            Start-Sleep -Seconds 2

            foreach ($command in @('A!','B!','C!')) {
                $responses += Invoke-ReadCommand -Port $port -Command $command -TimeoutMs $ReadTimeoutMs
            }
        }
        catch {
            $probeError = $_.Exception.Message
        }
        finally {
            if ($port) {
                try {
                    if ($port.IsOpen) { $port.Close() }
                    $portClosed = $true
                }
                catch { }
                $port.Dispose()
            }
        }
    }
}

$parsedResponses = @($responses | ForEach-Object {
    [pscustomobject]@{
        command = $_.command
        sent_at_utc = $_.sent_at_utc
        received_at_utc = $_.received_at_utc
        raw_response = $_.raw_response
        response_length = $_.response_length
        blocks = @(Get-ResponseBlocks -Raw $_.raw_response)
    }
})

$cResponse = @($parsedResponses | Where-Object { $_.command -eq 'C!' } | Select-Object -First 1)
$block8 = @()
$block4 = @()
if ($cResponse.Count -gt 0) {
    $block8 = @($cResponse[0].blocks | Where-Object { $_.discriminator -eq '!8 ' -or $_.discriminator -match '^!8' })
    $block4 = @($cResponse[0].blocks | Where-Object { $_.discriminator -eq '!4 ' -or $_.discriminator -match '^!4' })
}

$disposition = if (-not $ExecuteProbe) {
    'PREFLIGHT_ONLY_NO_SERIAL_ACCESS'
}
elseif (-not [string]::IsNullOrWhiteSpace($probeError)) {
    'PROBE_REFUSED_OR_FAILED'
}
elseif ($block8.Count -gt 0) {
    'SKY_QUALITY_SENSOR_RAW_BLOCK_8_OBSERVED'
}
else {
    'PROBE_COMPLETED_NO_BLOCK_8_OBSERVED'
}

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.CloudWatcherSqmProtocolProbe'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = if ($ExecuteProbe) { 'EXPLICIT_READ_ONLY_SERIAL_PROTOCOL_PROBE' } else { 'PREFLIGHT_ONLY_NO_SERIAL_ACCESS' }
    protocol_basis = [ordered]@{
        read_commands = @('A!','B!','C!')
        a_command_semantics = 'Get internal name'
        b_command_semantics = 'Get firmware version'
        c_command_semantics = 'Get values'
        sqm_raw_block = '!8'
        legacy_ldr_block = '!4'
        sqm_conversion_performed = $false
        reason = 'Raw !8 presence verifies candidate sky-quality sensor data. Conversion to MPSAS is forbidden until the actual SQReference configuration is verified.'
    }
    preflight = $preflight
    execution = [ordered]@{
        port_opened = $portOpened
        port_closed = $portClosed
        error = $probeError
        responses = $parsedResponses
    }
    conclusions = [ordered]@{
        block_8_observed = [bool]($block8.Count -gt 0)
        block_4_observed = [bool]($block4.Count -gt 0)
        sqm_source_verified = $false
        sqm_value_published = $false
        device_setting_changed = $false
        firmware_changed = $false
        relay_command_sent = $false
        pwm_command_sent = $false
        disposition = $disposition
        note = 'A!, B! and C! are read requests. This probe never sends G!, H!, Pxxxx!, reset, firmware-update or configuration-write commands. !4 is never treated as SQM.'
    }
}

$jsonPath = Join-Path $bundle 'cloudwatcher-sqm-protocol-probe.json'
$txtPath = Join-Path $bundle 'cloudwatcher-sqm-protocol-probe.txt'
$report | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== PREFLIGHT ===',
    ($preflight | Format-List | Out-String),
    '=== SERIAL CANDIDATES ===',
    ($serialCandidates | Format-Table -AutoSize | Out-String),
    '=== CLOUDWATCHER PROCESSES ===',
    ($cloudWatcherProcesses | Format-Table -AutoSize | Out-String),
    '=== RESPONSES ===',
    ($parsedResponses | Format-List command,sent_at_utc,received_at_utc,response_length,raw_response | Out-String),
    '=== CONCLUSIONS ===',
    ($report.conclusions | Format-List | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== SERIAL CANDIDATES ==='
if ($serialCandidates.Count -gt 0) { $serialCandidates | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none enumerated via Win32_SerialPort)' }
Write-Output '=== CLOUDWATCHER PROCESSES ==='
if ($cloudWatcherProcesses.Count -gt 0) { $cloudWatcherProcesses | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none running)' }
Write-Output '=== EXECUTION ==='
Write-Output ('Port opened: {0}' -f $portOpened)
if ($probeError) { Write-Output ('Error: {0}' -f $probeError) }
if ($parsedResponses.Count -gt 0) {
    $parsedResponses | Select-Object command,response_length,raw_response | Format-List | Out-String | Write-Output
}
Write-Output '=== SQM EVIDENCE ==='
Write-Output ('Block !8 observed: {0}' -f [bool]($block8.Count -gt 0))
Write-Output ('Block !4 observed: {0}' -f [bool]($block4.Count -gt 0))
Write-Output 'MPSAS conversion performed: False'
Write-Output '=== DISPOSITION ==='
Write-Output $disposition
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'CLOUDWATCHER SQM PROTOCOL PROBE RESULT: evidence recorded; not BKL-029 acceptance'
