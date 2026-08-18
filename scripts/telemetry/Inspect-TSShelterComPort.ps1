[CmdletBinding()]
param(
    [string]$PortName = 'COM47'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate TS Shelter COM port inspector - READ ONLY / NO PORT OPEN'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Target port: {0}' -f $PortName)

Write-Output ''
Write-Output '=== WIN32 SERIAL PORT ==='
$serial = Get-CimInstance Win32_SerialPort -ErrorAction SilentlyContinue |
    Where-Object { $_.DeviceID -eq $PortName }
if ($serial) {
    $serial | Select-Object DeviceID,Name,Description,Manufacturer,PNPDeviceID,ProviderType,Status |
        Format-List | Out-String | Write-Output
}
else {
    Write-Output '(not returned by Win32_SerialPort)'
}

Write-Output '=== PNP DEVICES MATCHING PORT ==='
$pnp = Get-CimInstance Win32_PnPEntity -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match ('\(' + [regex]::Escape($PortName) + '\)') }
if ($pnp) {
    $pnp | Select-Object Name,Description,Manufacturer,PNPDeviceID,Service,Status,ClassGuid |
        Format-List | Out-String | Write-Output
}
else {
    Write-Output '(none found)'
}

Write-Output '=== SIGNED DRIVER ==='
$driverMatches = @()
foreach ($device in @($pnp)) {
    if ($device.PNPDeviceID) {
        $escapedId = [regex]::Escape([string]$device.PNPDeviceID)
        $driverMatches += Get-CimInstance Win32_PnPSignedDriver -ErrorAction SilentlyContinue |
            Where-Object { $_.DeviceID -match ('^' + $escapedId + '$') }
    }
}
$driverMatches = @($driverMatches | Sort-Object DeviceID -Unique)
if ($driverMatches.Count -gt 0) {
    $driverMatches | Select-Object DeviceName,Manufacturer,DriverProviderName,DriverVersion,DriverDate,InfName,DeviceID |
        Format-List | Out-String | Write-Output
}
else {
    Write-Output '(no exact signed-driver match found)'
}

Write-Output '=== PRESENT PORT DEVICES (PNP CLASS Ports) ==='
try {
    $ports = Get-PnpDevice -Class Ports -PresentOnly -ErrorAction Stop |
        Select-Object Status,Class,FriendlyName,InstanceId
    if ($ports) {
        $ports | Format-Table -AutoSize | Out-String | Write-Output
    }
    else {
        Write-Output '(none found)'
    }
}
catch {
    Write-Output ('Get-PnpDevice unavailable/failed: {0}' -f $_.Exception.Message)
}

Write-Output 'No serial port was opened. No COM/ASCOM object was created. No device command was sent.'
Write-Output 'TS SHELTER COM PORT INVENTORY RESULT: PASS (inventory only)'
