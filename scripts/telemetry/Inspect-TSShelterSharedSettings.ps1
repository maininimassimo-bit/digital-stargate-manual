[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate TS Shelter shared settings inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)

$paths = @(
    'HKLM:\Software\WOW6432Node\ASCOM\Hub Application Drivers\TS_Shelter_Settings',
    'HKLM:\Software\ASCOM\Hub Application Drivers\TS_Shelter_Settings',
    'HKCU:\Software\WOW6432Node\ASCOM\Hub Application Drivers\TS_Shelter_Settings',
    'HKCU:\Software\ASCOM\Hub Application Drivers\TS_Shelter_Settings',
    'HKLM:\Software\WOW6432Node\ASCOM\Switch Drivers\ASCOM.TS_Shelter.Switch',
    'HKLM:\Software\ASCOM\Switch Drivers\ASCOM.TS_Shelter.Switch',
    'HKCU:\Software\WOW6432Node\ASCOM\Switch Drivers\ASCOM.TS_Shelter.Switch',
    'HKCU:\Software\ASCOM\Switch Drivers\ASCOM.TS_Shelter.Switch',
    'HKLM:\Software\WOW6432Node\ASCOM\SafetyMonitor Drivers\ASCOM.TS_Shelter.SafetyMonitor',
    'HKLM:\Software\ASCOM\SafetyMonitor Drivers\ASCOM.TS_Shelter.SafetyMonitor',
    'HKCU:\Software\WOW6432Node\ASCOM\SafetyMonitor Drivers\ASCOM.TS_Shelter.SafetyMonitor',
    'HKCU:\Software\ASCOM\SafetyMonitor Drivers\ASCOM.TS_Shelter.SafetyMonitor'
)

function Show-RegistryTree {
    param([Parameter(Mandatory=$true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) { return }

    Write-Output ('--- {0} ---' -f $Path)
    try {
        Get-ItemProperty -LiteralPath $Path -ErrorAction Stop |
            Format-List * | Out-String -Width 260 | Write-Output
    } catch {
        Write-Output ('Unable to read properties: {0}' -f $_.Exception.Message)
    }

    Get-ChildItem -LiteralPath $Path -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Output ('[{0}]' -f $_.Name)
        try {
            Get-ItemProperty -LiteralPath $_.PSPath -ErrorAction Stop |
                Format-List * | Out-String -Width 260 | Write-Output
        } catch {
            Write-Output ('Unable to read child properties: {0}' -f $_.Exception.Message)
        }
    }
}

Write-Output ''
Write-Output '=== TS SHELTER SHARED SETTINGS / SWITCH / SAFETYMONITOR ==='
$found = 0
foreach ($path in $paths) {
    if (Test-Path -LiteralPath $path) {
        $found++
        Show-RegistryTree -Path $path
    }
}

Write-Output ''
Write-Output ('Registry profiles found: {0}' -f $found)
Write-Output 'No COM object was created. No device connection was opened. No command was sent.'
Write-Output 'TS SHELTER SHARED SETTINGS RESULT: PASS (configuration inventory only)'
