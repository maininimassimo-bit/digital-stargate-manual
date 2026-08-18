[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate TS Shelter switch configuration inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)

$paths = @(
    'HKLM:\Software\WOW6432Node\ASCOM\Dome Drivers\ASCOM.TS_Shelter.Dome',
    'HKLM:\Software\ASCOM\Dome Drivers\ASCOM.TS_Shelter.Dome',
    'HKCU:\Software\WOW6432Node\ASCOM\Dome Drivers\ASCOM.TS_Shelter.Dome',
    'HKCU:\Software\ASCOM\Dome Drivers\ASCOM.TS_Shelter.Dome'
)

Write-Output ''
Write-Output '=== TS SHELTER PROFILE ==='
foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Output ('--- {0} ---' -f $path)
        Get-ItemProperty -Path $path | Format-List * | Out-String | Write-Output
        Get-ChildItem -Path $path -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
            Write-Output ('[{0}]' -f $_.Name)
            try { Get-ItemProperty -Path $_.PSPath | Format-List * | Out-String | Write-Output } catch { }
        }
    }
}

Write-Output '=== ASCOM SWITCH DRIVERS ==='
$switchRoots = @(
    'HKLM:\Software\WOW6432Node\ASCOM\Switch Drivers',
    'HKLM:\Software\ASCOM\Switch Drivers',
    'HKCU:\Software\WOW6432Node\ASCOM\Switch Drivers',
    'HKCU:\Software\ASCOM\Switch Drivers'
)
foreach ($root in $switchRoots) {
    if (Test-Path $root) {
        Write-Output ('--- {0} ---' -f $root)
        Get-ChildItem -Path $root -ErrorAction SilentlyContinue | ForEach-Object {
            $props = $null
            try { $props = Get-ItemProperty -Path $_.PSPath -ErrorAction Stop } catch { }
            [pscustomobject]@{
                HivePath = $root
                KeyName = $_.PSChildName
                ProgID = if ($props -and $props.PSObject.Properties['ProgID']) { [string]$props.ProgID } else { $null }
                Description = if ($props -and $props.PSObject.Properties['Description']) { [string]$props.Description } else { $null }
                Default = if ($props -and $props.PSObject.Properties['(default)']) { [string]$props.'(default)' } else { $null }
            }
        } | Format-Table -AutoSize | Out-String -Width 220 | Write-Output
    }
}

Write-Output '=== RELATED REGISTRY KEYS ==='
$roots = @('HKLM:\Software\WOW6432Node\ASCOM','HKLM:\Software\ASCOM','HKCU:\Software\ASCOM')
foreach ($root in $roots) {
    if (-not (Test-Path $root)) { continue }
    Get-ChildItem -Path $root -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '(?i)(TS_Shelter|TS Shelter|Shelter|Switch)' } |
        Select-Object PSPath,PSChildName | Format-Table -AutoSize | Out-String -Width 220 | Write-Output
}

Write-Output 'No COM object was created. No device connection was opened. No command was sent.'
Write-Output 'TS SHELTER SWITCH CONFIG RESULT: PASS (configuration inventory only)'
