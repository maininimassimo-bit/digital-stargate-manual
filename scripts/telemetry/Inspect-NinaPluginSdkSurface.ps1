[CmdletBinding()]
param(
    [string]$NinaExe = "C:\Program Files\N.I.N.A. - Nighttime Imaging 'N' Astronomy\NINA.exe"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Output 'Digital StarGate NINA plugin SDK surface inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('NINA exe: {0}' -f $NinaExe)

if (-not (Test-Path -LiteralPath $NinaExe)) {
    throw "NINA executable not found: $NinaExe"
}

$installRoot = Split-Path -Parent $NinaExe

Write-Output ''
Write-Output '=== NINA FILE VERSION ==='
$version = (Get-Item -LiteralPath $NinaExe).VersionInfo
[pscustomobject]@{
    FileVersion = $version.FileVersion
    ProductVersion = $version.ProductVersion
    ProductName = $version.ProductName
    CompanyName = $version.CompanyName
} | Format-List | Out-String | Write-Output

Write-Output '=== NINA PROCESS / MODULE SNAPSHOT ==='
$nina = @(Get-Process -Name NINA -ErrorAction SilentlyContinue)
if ($nina.Count -gt 0) {
    $nina | Select-Object Id,ProcessName,Path,StartTime |
        Format-Table -AutoSize | Out-String -Width 220 | Write-Output

    foreach ($proc in $nina) {
        Write-Output ('--- PID {0} modules ---' -f $proc.Id)
        try {
            $proc.Modules |
                Where-Object { $_.ModuleName -match '(?i)nina|plugin|device|dome|equipment' } |
                Select-Object ModuleName,FileName,FileVersionInfo |
                ForEach-Object {
                    [pscustomobject]@{
                        ModuleName = $_.ModuleName
                        FileName = $_.FileName
                        FileVersion = $_.FileVersionInfo.FileVersion
                        ProductVersion = $_.FileVersionInfo.ProductVersion
                    }
                } | Format-Table -AutoSize | Out-String -Width 260 | Write-Output
        } catch {
            Write-Output ('Module enumeration failed for PID {0}: {1}' -f $proc.Id,$_.Exception.Message)
        }
    }
} else {
    Write-Output '(NINA process not running)'
}

Write-Output '=== INSTALLED NINA ASSEMBLIES ==='
$assemblies = @(Get-ChildItem -LiteralPath $installRoot -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -eq '.dll' -and $_.Name -match '(?i)nina|plugin|device|equipment|dome' } |
    Sort-Object FullName -Unique)
if ($assemblies.Count -gt 0) {
    foreach ($file in $assemblies) {
        try {
            $fv = $file.VersionInfo
            [pscustomobject]@{
                Name = $file.Name
                FullName = $file.FullName
                FileVersion = $fv.FileVersion
                ProductVersion = $fv.ProductVersion
            }
        } catch {
            [pscustomobject]@{
                Name = $file.Name
                FullName = $file.FullName
                FileVersion = $null
                ProductVersion = $null
            }
        }
    } | Format-Table -AutoSize | Out-String -Width 280 | Write-Output
} else {
    Write-Output '(no matching assemblies found)'
}

Write-Output '=== REFLECTION CANDIDATES (METADATA ONLY) ==='
$candidateFiles = @($assemblies | Where-Object { $_.Name -match '(?i)NINA.*(Plugin|Core|Equipment|Device)|Plugin' } | Select-Object -First 40)
if ($candidateFiles.Count -eq 0) {
    Write-Output '(no candidate assemblies selected)'
} else {
    foreach ($file in $candidateFiles) {
        Write-Output ('--- {0} ---' -f $file.FullName)
        try {
            $asmName = [System.Reflection.AssemblyName]::GetAssemblyName($file.FullName)
            Write-Output ('AssemblyName: {0}' -f $asmName.FullName)
        } catch {
            Write-Output ('Assembly metadata read failed: {0}' -f $_.Exception.Message)
        }
    }
}

Write-Output '=== INSTALLED PLUGIN MANIFESTS / DLLS ==='
$pluginRoot = Join-Path $env:LOCALAPPDATA 'NINA\Plugins'
if (Test-Path -LiteralPath $pluginRoot) {
    Get-ChildItem -LiteralPath $pluginRoot -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -match '^\.(dll|json|manifest|xml|config)$' } |
        Select-Object FullName,Length,LastWriteTime |
        Sort-Object FullName |
        Format-Table -AutoSize | Out-String -Width 280 | Write-Output
} else {
    Write-Output '(plugin root not found)'
}

Write-Output 'No NINA plugin was loaded by this inspector. No device API was called. No ASCOM/COM object was created. No equipment connection was opened or changed.'
Write-Output 'NINA PLUGIN SDK SURFACE RESULT: PASS (metadata inventory only)'
