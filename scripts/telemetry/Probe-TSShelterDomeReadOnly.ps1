[CmdletBinding()]
param(
    [string]$ProgId = 'ASCOM.TS_Shelter.Dome'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate TS Shelter dome probe - READ ONLY / NO CONNECT'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('ProgID: {0}' -f $ProgId)

$dome = $null
try {
    $dome = New-Object -ComObject $ProgId

    $connected = $false
    try {
        $connected = [bool]$dome.Connected
    }
    catch {
        Write-Output ('Connected read failed: {0}' -f $_.Exception.Message)
        Write-Output 'PROBE RESULT: INCONCLUSIVE'
        return
    }

    Write-Output ('Connected: {0}' -f $connected)

    $name = $null
    $description = $null
    $driverVersion = $null
    foreach ($item in @(
        @{ Label = 'Name'; Property = 'Name' },
        @{ Label = 'Description'; Property = 'Description' },
        @{ Label = 'DriverVersion'; Property = 'DriverVersion' }
    )) {
        try {
            $value = $dome.($item.Property)
            Write-Output ('{0}: {1}' -f $item.Label, $value)
        }
        catch {
            Write-Output ('{0}: <unavailable>' -f $item.Label)
        }
    }

    if (-not $connected) {
        Write-Output 'Driver object is not connected in this client context.'
        Write-Output 'No connection was opened and no device command was sent.'
        Write-Output 'PROBE RESULT: PASS (safe no-connect; live shutter status unavailable)'
        return
    }

    try {
        $status = $dome.ShutterStatus
        $statusInt = [int]$status
        $statusName = switch ($statusInt) {
            0 { 'ShutterOpen' }
            1 { 'ShutterClosed' }
            2 { 'ShutterOpening' }
            3 { 'ShutterClosing' }
            4 { 'ShutterError' }
            default { 'UnknownEnumValue' }
        }
        Write-Output ('ShutterStatusRaw: {0}' -f $statusInt)
        Write-Output ('ShutterStatus: {0}' -f $statusName)
        Write-Output 'No connection state was changed and no motion command was sent.'
        Write-Output 'PROBE RESULT: PASS'
    }
    catch {
        Write-Output ('ShutterStatus read failed: {0}' -f $_.Exception.Message)
        Write-Output 'PROBE RESULT: INCONCLUSIVE'
    }
}
finally {
    if ($null -ne $dome) {
        try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($dome) } catch { }
    }
}
