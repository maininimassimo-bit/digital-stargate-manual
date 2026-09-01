Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ReportingConfig {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$ConfigPath)
    if (-not (Test-Path -LiteralPath $ConfigPath)) {
        throw "File di configurazione non trovato: $ConfigPath"
    }
    return Import-PowerShellDataFile -LiteralPath $ConfigPath
}

function Get-SessionId {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][datetime]$SessionStart,
        [Parameter(Mandatory)][datetime]$SessionEnd
    )
    return ('{0:yyyy-MM-dd}_{1:yyyy-MM-dd}' -f $SessionStart, $SessionEnd)
}

function Ensure-Directory {
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Get-RelativePathSafe {
    param(
        [Parameter(Mandatory)][string]$BasePath,
        [Parameter(Mandatory)][string]$TargetPath
    )

    $baseFull = [System.IO.Path]::GetFullPath($BasePath).TrimEnd([char[]]@('\', '/'))
    $targetFull = [System.IO.Path]::GetFullPath($TargetPath)
    $basePrefix = $baseFull + [System.IO.Path]::DirectorySeparatorChar

    if ($targetFull.StartsWith($basePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $targetFull.Substring($basePrefix.Length)
    }

    $baseUri = New-Object System.Uri(($basePrefix -replace '\', '/'))
    $targetUri = New-Object System.Uri(($targetFull -replace '\', '/'))
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

function Get-Sha256 {
    param([Parameter(Mandatory)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Copy-FilesInWindow {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$SourceDirectory,
        [Parameter(Mandatory)][string]$DestinationDirectory,
        [Parameter(Mandatory)][datetime]$SessionStart,
        [Parameter(Mandatory)][datetime]$SessionEnd,
        [string[]]$Extensions = @('.log', '.txt', '.csv'),
        [int]$BoundaryHours = 12
    )
    Ensure-Directory $DestinationDirectory
    if (-not (Test-Path -LiteralPath $SourceDirectory)) { return @() }

    $windowStart = $SessionStart.AddHours(-$BoundaryHours)
    $windowEnd = $SessionEnd.AddHours($BoundaryHours)
    $files = Get-ChildItem -LiteralPath $SourceDirectory -File -Recurse |
        Where-Object {
            $Extensions -contains $_.Extension.ToLowerInvariant() -and
            $_.LastWriteTime -ge $windowStart -and $_.LastWriteTime -le $windowEnd
        }

    $copied = @()
    foreach ($file in $files) {
        $destination = Join-Path $DestinationDirectory $file.Name
        Copy-Item -LiteralPath $file.FullName -Destination $destination -Force
        $copied += Get-Item -LiteralPath $destination
    }
    return $copied
}

function Write-SessionManifest {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$SessionRoot,
        [Parameter(Mandatory)][string]$SessionId,
        [Parameter(Mandatory)][datetime]$SessionStart,
        [Parameter(Mandatory)][datetime]$SessionEnd,
        [Parameter(Mandatory)][hashtable]$Config,
        [string]$Status = 'COMPLETE',
        [string]$Severity = 'UNASSESSED',
        [int]$DiagnosticLevel = 1
    )
    $files = Get-ChildItem -LiteralPath $SessionRoot -File -Recurse | ForEach-Object {
        [ordered]@{
            path = Get-RelativePathSafe -BasePath $SessionRoot -TargetPath $_.FullName
            size_bytes = $_.Length
            sha256 = Get-Sha256 -Path $_.FullName
            modified_local = $_.LastWriteTime.ToString('o')
        }
    }
    $manifest = [ordered]@{
        schema_version = '1.0'
        session_id = $SessionId
        observatory = $Config.ObservatoryName
        start_local = $SessionStart.ToString('o')
        end_local = $SessionEnd.ToString('o')
        timezone_id = $Config.TimeZoneId
        report_status = $Status
        severity = $Severity
        diagnostic_level = $DiagnosticLevel
        generated_at_local = (Get-Date).ToString('o')
        files = @($files)
    }
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $SessionRoot 'manifest.json') -Encoding UTF8
}

function Update-SessionReadme {
    param(
        [Parameter(Mandatory)][string]$SessionRoot,
        [Parameter(Mandatory)][string]$SessionId,
        [Parameter(Mandatory)][datetime]$SessionStart,
        [Parameter(Mandatory)][datetime]$SessionEnd
    )
    $content = @"
# Sessione $SessionId

- **Inizio:** $($SessionStart.ToString('dd/MM/yyyy HH:mm'))
- **Fine:** $($SessionEnd.ToString('dd/MM/yyyy HH:mm'))
- **Livello diagnostico:** 1 - report ordinario

## Contenuto

- `raw/nina`: log N.I.N.A.
- `raw/phd2`: PHD2 GuideLog
- `raw/weather`: estratto meteo CloudWatcher
- `report`: report PDF e, quando disponibile, Markdown
- `manifest.json`: inventario e hash SHA-256

## Note operative

Questa cartella deve contenere esclusivamente i dati riferiti alla sessione indicata.
"@
    Set-Content -LiteralPath (Join-Path $SessionRoot 'README.md') -Value $content -Encoding UTF8
}
