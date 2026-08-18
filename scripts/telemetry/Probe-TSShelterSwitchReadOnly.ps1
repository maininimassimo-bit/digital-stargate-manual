[CmdletBinding()]
param(
    [string]$ProgId = 'ASCOM.TS_Shelter.Switch'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate TS Shelter switch probe - READ ONLY / NO CONNECT'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('ProgID: {0}' -f $ProgId)

$switch = $null
try {
    $switch = New-Object -ComObject $ProgId

    $connected = $false
    try {
        $connected = [bool]$switch.Connected
    }
    catch {
        Write-Output ('Connected read failed: {0}' -f $_.Exception.Message)
        Write-Output 'PROBE RESULT: INCONCLUSIVE'
        return
    }

    Write-Output ('Connected: {0}' -f $connected)

    foreach ($property in @('Name','Description','DriverVersion','InterfaceVersion')) {
        try {
            $value = $switch.$property
            Write-Output ('{0}: {1}' -f $property, $value)
        }
        catch {
            Write-Output ('{0}: <unavailable>' -f $property)
        }
    }

    if (-not $connected) {
        Write-Output 'Driver object is not connected in this client context.'
        Write-Output 'No connection was opened and no switch getter beyond metadata was called.'
        Write-Output 'PROBE RESULT: PASS (safe no-connect; live switch values unavailable)'
        return
    }

    $max = 0
    try {
        $max = [int]$switch.MaxSwitch
        Write-Output ('MaxSwitch: {0}' -f $max)
    }
    catch {
        Write-Output ('MaxSwitch read failed: {0}' -f $_.Exception.Message)
        Write-Output 'PROBE RESULT: INCONCLUSIVE'
        return
    }

    Write-Output '=== SWITCHES ==='
    for ($id = 0; $id -lt $max; $id++) {
        $name = $null
        $description = $null
        $canWrite = $null
        $state = $null
        $value = $null

        try { $name = [string]$switch.GetSwitchName($id) } catch { }
        try { $description = [string]$switch.GetSwitchDescription($id) } catch { }
        try { $canWrite = [bool]$switch.CanWrite($id) } catch { }
        try { $state = [bool]$switch.GetSwitch($id) } catch { }
        try { $value = [double]$switch.GetSwitchValue($id) } catch { }

        [pscustomobject]@{
            Id = $id
            Name = $name
            Description = $description
            CanWrite = $canWrite
            State = $state
            Value = $value
        } | Format-List | Out-String | Write-Output
    }

    Write-Output 'No connection state was changed. No SetSwitch/SetSwitchValue call was made.'
    Write-Output 'PROBE RESULT: PASS'
}
finally {
    if ($null -ne $switch) {
        try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($switch) } catch { }
    }
}
