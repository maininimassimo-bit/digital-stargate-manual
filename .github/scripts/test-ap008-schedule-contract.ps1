[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Assert-Condition {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw "FAIL: $Message" }
}

function New-Schedule {
    param(
        [string]$ScheduleId,
        [string]$IdempotencyKey,
        [datetime]$StartUtc,
        [datetime]$EndUtc
    )

    Assert-Condition ($EndUtc -gt $StartUtc) "schedule interval must be positive"
    [pscustomobject]@{
        schedule_id = $ScheduleId
        idempotency_key = $IdempotencyKey
        start_utc = $StartUtc.ToUniversalTime()
        end_utc = $EndUtc.ToUniversalTime()
        state = 'PLANNED'
    }
}

function Add-Schedule {
    param([hashtable]$State, [object]$Schedule)

    if ($State.by_idempotency.ContainsKey($Schedule.idempotency_key)) {
        return $State.by_idempotency[$Schedule.idempotency_key]
    }

    Assert-Condition (-not $State.by_id.ContainsKey($Schedule.schedule_id)) "schedule id collision"
    $State.by_id[$Schedule.schedule_id] = $Schedule
    $State.by_idempotency[$Schedule.idempotency_key] = $Schedule.schedule_id
    $State.journal += [pscustomobject]@{ operation = 'ADD'; schedule = $Schedule }
    return $Schedule.schedule_id
}

function Cancel-Schedule {
    param([hashtable]$State, [string]$ScheduleId)

    Assert-Condition ($State.by_id.ContainsKey($ScheduleId)) "cancel target not found"
    $item = $State.by_id[$ScheduleId]
    if ($item.state -ne 'COMPLETED') { $item.state = 'CANCELLED' }
    $State.journal += [pscustomobject]@{ operation = 'CANCEL'; schedule_id = $ScheduleId }
}

function Restore-State {
    param([object[]]$Journal)

    $restored = @{ by_id = @{}; by_idempotency = @{}; journal = @() }

    foreach ($entry in $Journal) {
        if ($entry.operation -eq 'ADD') {
            $item = $entry.schedule
            $restored.by_id[$item.schedule_id] = $item
            $restored.by_idempotency[$item.idempotency_key] = $item.schedule_id
        }
        elseif ($entry.operation -eq 'CANCEL') {
            $restored.by_id[$entry.schedule_id].state = 'CANCELLED'
        }
    }

    return $restored
}

function New-State {
    return @{ by_id = @{}; by_idempotency = @{}; journal = @() }
}

$day = [datetime]::SpecifyKind([datetime]'2026-09-21T00:00:00', [System.DateTimeKind]::Utc)

foreach ($count in @(3, 10, 100, 1000)) {
    $state = New-State
    for ($index = 1; $index -le $count; $index++) {
        $start = $day.AddMinutes($index)
        $item = New-Schedule -ScheduleId ("S-{0:D4}" -f $index) -IdempotencyKey ("IDEMP-{0:D4}" -f $index) -StartUtc $start -EndUtc $start.AddMinutes(20)
        [void](Add-Schedule -State $state -Schedule $item)
    }
    Assert-Condition ($state.by_id.Count -eq $count) "count $count was not accepted"
    Write-Host ("PASS: {0} schedules in one UTC day" -f $count)
}

$state = New-State
$first = New-Schedule -ScheduleId 'S-DUP-1' -IdempotencyKey 'IDEMP-DUP' -StartUtc $day.AddHours(1) -EndUtc $day.AddHours(2)
$second = New-Schedule -ScheduleId 'S-DUP-2' -IdempotencyKey 'IDEMP-DUP' -StartUtc $day.AddHours(3) -EndUtc $day.AddHours(4)
[void](Add-Schedule -State $state -Schedule $first)
$duplicateResult = Add-Schedule -State $state -Schedule $second
Assert-Condition ($state.by_id.Count -eq 1) 'duplicate idempotency key created a second schedule'
Assert-Condition ($duplicateResult -eq 'S-DUP-1') 'duplicate did not resolve to original schedule'
Write-Host 'PASS: duplicate idempotency key is deduplicated'

$overlapA = New-Schedule -ScheduleId 'S-OVERLAP-A' -IdempotencyKey 'IDEMP-OVERLAP-A' -StartUtc $day.AddHours(5) -EndUtc $day.AddHours(7)
$overlapB = New-Schedule -ScheduleId 'S-OVERLAP-B' -IdempotencyKey 'IDEMP-OVERLAP-B' -StartUtc $day.AddHours(6) -EndUtc $day.AddHours(8)
[void](Add-Schedule -State $state -Schedule $overlapA)
[void](Add-Schedule -State $state -Schedule $overlapB)
Assert-Condition ($state.by_id.ContainsKey('S-OVERLAP-A') -and $state.by_id.ContainsKey('S-OVERLAP-B')) 'overlapping distinct schedules were merged or discarded'
Write-Host 'PASS: overlapping distinct schedules remain independently addressable'

Cancel-Schedule -State $state -ScheduleId 'S-OVERLAP-A'
Cancel-Schedule -State $state -ScheduleId 'S-OVERLAP-A'
Assert-Condition ($state.by_id['S-OVERLAP-A'].state -eq 'CANCELLED') 'cancellation is not idempotent'
Write-Host 'PASS: cancellation is idempotent'

$restored = Restore-State -Journal $state.journal
Assert-Condition ($restored.by_id.Count -eq $state.by_id.Count) 'restart lost schedules'
Assert-Condition ($restored.by_id['S-OVERLAP-A'].state -eq 'CANCELLED') 'restart resurrected cancelled schedule'
Assert-Condition ($restored.by_id['S-OVERLAP-B'].state -eq 'PLANNED') 'restart changed planned schedule state'
Write-Host 'PASS: restart restores journal state without resurrection'

Write-Host 'PASS: AP-008 schedule contract offline suite'
