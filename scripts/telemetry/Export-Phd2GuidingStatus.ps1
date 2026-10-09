[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$OutputPath,
    [Parameter(Mandatory = $true)][string]$Phd2LogRoot,
    [string]$GuideLogPath = '',
    [ValidateRange(1, 86400)][int]$FreshnessSeconds = 300,
    [string]$SourceInstance = $env:COMPUTERNAME
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function New-ProfileAccumulator {
    param([Parameter(Mandatory = $true)][string]$Name)
    return [ordered]@{
        profile = $Name
        pixel_scale_arcsec_per_px = $null
        valid_samples = 0
        drop_samples = 0
        star_lost_events = 0
        ra_square_sum = 0.0
        dec_square_sum = 0.0
        guiding_segments = 0
    }
}

function Get-Number {
    param([AllowNull()][object]$Value)
    $n = 0.0
    if ($null -ne $Value -and [double]::TryParse(
        ([string]$Value).Trim(),
        [System.Globalization.NumberStyles]::Float,
        [System.Globalization.CultureInfo]::InvariantCulture,
        [ref]$n)) {
        return $n
    }
    return $null
}

if (-not (Test-Path -LiteralPath $Phd2LogRoot -PathType Container)) {
    throw "PHD2 log root non trovato: $Phd2LogRoot"
}

if (-not [string]::IsNullOrWhiteSpace($GuideLogPath)) {
    if (-not (Test-Path -LiteralPath $GuideLogPath -PathType Leaf)) {
        throw "PHD2 GuideLog non trovato: $GuideLogPath"
    }
    $files = @(Get-Item -LiteralPath $GuideLogPath -ErrorAction Stop)
}
else {
    $files = @(Get-ChildItem -LiteralPath $Phd2LogRoot -Recurse -File -ErrorAction Stop |
        Where-Object { $_.Name -like 'PHD2_GuideLog_*.txt' } |
        Sort-Object LastWriteTimeUtc -Descending)
}

if ($files.Count -eq 0) {
    throw "Nessun PHD2 GuideLog trovato: $Phd2LogRoot"
}

$file = $files[0]
$lines = @(Get-Content -LiteralPath $file.FullName -ErrorAction Stop)
$profiles = @{}
$currentProfile = 'UNKNOWN'
$currentScale = $null
$currentHeader = $null
$currentGuiding = $false
$state = 'NOT_GUIDING'
$lastObserved = $file.LastWriteTimeUtc

foreach ($line in $lines) {
    if ($line -match '^Equipment Profile\s*=\s*(.+)$') {
        $currentProfile = $Matches[1].Trim()
        if (-not $profiles.Contains($currentProfile)) { $profiles[$currentProfile] = New-ProfileAccumulator -Name $currentProfile }
        continue
    }

    if ($line -match '^Pixel scale\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*arc-sec/px') {
        $currentScale = Get-Number $Matches[1]
        if (-not $profiles.Contains($currentProfile)) { $profiles[$currentProfile] = New-ProfileAccumulator -Name $currentProfile }
        $profiles[$currentProfile].pixel_scale_arcsec_per_px = $currentScale
        continue
    }

    if ($line -match '^Guiding Begins at ') {
        $currentGuiding = $true
        $state = 'GUIDING'
        if (-not $profiles.Contains($currentProfile)) { $profiles[$currentProfile] = New-ProfileAccumulator -Name $currentProfile }
        $profiles[$currentProfile].guiding_segments++
        continue
    }

    if ($line -match '^Guiding Ends at ') {
        $currentGuiding = $false
        if ($state -eq 'GUIDING') { $state = 'NOT_GUIDING' }
        continue
    }

    if ($line -match 'STAR LOST') {
        if (-not $profiles.Contains($currentProfile)) { $profiles[$currentProfile] = New-ProfileAccumulator -Name $currentProfile }
        $profiles[$currentProfile].star_lost_events++
        continue
    }

    if ($line -match '^Frame,') {
        $currentHeader = $line
        continue
    }

    if ($null -eq $currentHeader -or $line -notmatch '^\d+,') { continue }

    try {
        $row = @($currentHeader, $line) | ConvertFrom-Csv | Select-Object -First 1
        if (-not $row) { continue }
        if (-not $profiles.Contains($currentProfile)) { $profiles[$currentProfile] = New-ProfileAccumulator -Name $currentProfile }
        $p = $profiles[$currentProfile]

        if ([string]$row.mount -eq 'DROP') {
            $p.drop_samples++
            continue
        }

        $errorCode = Get-Number $row.ErrorCode
        if ($null -ne $errorCode -and $errorCode -notin @(0, 1)) {
            $p.drop_samples++
            continue
        }

        $ra = Get-Number $row.RARawDistance
        $dec = Get-Number $row.DECRawDistance
        if ($null -eq $ra -or $null -eq $dec) { continue }

        $p.valid_samples++
        $p.ra_square_sum += ($ra * $ra)
        $p.dec_square_sum += ($dec * $dec)
    }
    catch {
        # A malformed row is evidence loss, not a synthetic sample.
        continue
    }
}

$now = [datetime]::UtcNow
$observedAt = $lastObserved.ToUniversalTime()
$freshUntil = $observedAt.AddSeconds($FreshnessSeconds)
$quality = if ($freshUntil -ge $now) { 'CURRENT' } else { 'STALE' }

$profileOutput = @(
    foreach ($p in $profiles.Values) {
        if ($p.profile -eq 'UNKNOWN' -and $p.valid_samples -eq 0 -and $p.drop_samples -eq 0 -and $p.star_lost_events -eq 0) {
            continue
        }

        $scale = $p.pixel_scale_arcsec_per_px
        $raRms = $null
        $decRms = $null
        $totalRms = $null
        if ($p.valid_samples -gt 0 -and $null -ne $scale) {
            $raRms = [math]::Sqrt($p.ra_square_sum / $p.valid_samples) * $scale
            $decRms = [math]::Sqrt($p.dec_square_sum / $p.valid_samples) * $scale
            $totalRms = [math]::Sqrt(($raRms * $raRms) + ($decRms * $decRms))
        }

        [ordered]@{
            profile = $p.profile
            pixel_scale_arcsec_per_px = $scale
            valid_samples = $p.valid_samples
            drop_samples = $p.drop_samples
            star_lost_events = $p.star_lost_events
            guiding_segments = $p.guiding_segments
            rms_ra_arcsec = $raRms
            rms_dec_arcsec = $decRms
            rms_total_arcsec = $totalRms
        }
    }
)

$payload = [ordered]@{
    schema_version = '1.0'
    source_component = 'DSG.Phd2GuideLogAdapter'
    source_instance = $SourceInstance
    observed_at_utc = $observedAt.ToString('o')
    fresh_until_utc = $freshUntil.ToString('o')
    quality = $quality
    state = if ($quality -eq 'CURRENT') { $state } else { 'UNKNOWN' }
    latest_log = $file.FullName
    profiles = $profileOutput
    diagnostics = [ordered]@{
        log_version = '2.5'
        parser_mode = 'DYNAMIC_GUIDELOG_HEADER'
        no_hardware_commands = $true
        safety_authority = 'LOCAL_PHYSICAL_INTERLOCKS'
    }
}

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$temp = "$OutputPath.tmp"
$payload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $temp -Encoding UTF8
Move-Item -LiteralPath $temp -Destination $OutputPath -Force

Write-Output ('PHD2 guiding projection written: {0}' -f $OutputPath)
Write-Output ('Latest log: {0}; quality={1}; state={2}; profiles={3}' -f $file.FullName, $payload.quality, $payload.state, $profileOutput.Count)
