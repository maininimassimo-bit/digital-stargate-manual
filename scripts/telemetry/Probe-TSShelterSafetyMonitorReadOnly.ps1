[CmdletBinding()]
param(
    [string]$ProgId = 'ASCOM.TS_Shelter.SafetyMonitor'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate TS Shelter SafetyMonitor probe - READ ONLY / NO CONNECT'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('ProgID: {0}' -f $ProgId)

$monitor = $null
try {
    $monitor = New-Object -ComObject $ProgId

    $connected = $false
    try {
        $connected = [bool]$monitor.Connected
    }
    catch {
        Write-Output ('Connected read failed: {0}' -f $_.Exception.Message)
        Write-Output 'PROBE RESULT: INCONCLUSIVE'
        return
    }

    Write-Output ('Connected: {0}' -f $connected)

    foreach ($property in @('Name','Description','DriverVersion','InterfaceVersion')) {
        try {
            $value = $monitor.$property
            Write-Output ('{0}: {1}' -f $property, $value)
        }
        catch {
            Write-Output ('{0}: <unavailable>' -f $property)
        }
    }

    if (-not $connected) {
        Write-Output 'Driver object is not connected in this client context.'
        Write-Output 'No connection was opened and IsSafe was not read.'
        Write-Output 'PROBE RESULT: PASS (safe no-connect; live safety value unavailable)'
        return
    }

    try {
        $isSafe = [bool]$monitor.IsSafe
        Write-Output ('IsSafe: {0}' -f $isSafe)
        Write-Output 'No connection state was changed and no command method was invoked.'
        Write-Output 'PROBE RESULT: PASS'
    }
    catch {
        Write-Output ('IsSafe read failed: {0}' -f $_.Exception.Message)
        Write-Output 'PROBE RESULT: INCONCLUSIVE'
    }
}
finally {
    if ($null -ne $monitor) {
        try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($monitor) } catch { }
    }
}
