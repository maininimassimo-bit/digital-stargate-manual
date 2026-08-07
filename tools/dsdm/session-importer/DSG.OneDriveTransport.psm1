Set-StrictMode -Version Latest

function Get-DSGTransportSha256 {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) {
        throw "File not found: $LiteralPath"
    }

    return (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Test-DSGTransportStableFile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$LiteralPath,
        [Parameter(Mandatory = $false)][int]$DelaySeconds = 10
    )

    $first = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
    $firstLength = [int64]$first.Length
    $firstWrite = $first.LastWriteTimeUtc

    Start-Sleep -Seconds $DelaySeconds

    $second = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
    return (
        $firstLength -eq [int64]$second.Length -and
        $firstWrite -eq $second.LastWriteTimeUtc
    )
}

function Export-DSGOneDriveTransportFile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$SourcePath,
        [Parameter(Mandatory = $true)][string]$TransportRoot,
        [Parameter(Mandatory = $false)][int]$StabilityDelaySeconds = 10
    )

    if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
        throw "Source file not found: $SourcePath"
    }
    if (-not (Test-Path -LiteralPath $TransportRoot -PathType Container)) {
        throw "Transport root not available: $TransportRoot"
    }
    if (-not (Test-DSGTransportStableFile -LiteralPath $SourcePath -DelaySeconds $StabilityDelaySeconds)) {
        return [pscustomobject][ordered]@{
            Status = 'DEFER_UNSTABLE'
            SourcePath = $SourcePath
            TransportPath = $null
            ManifestPath = $null
            SourceDeleted = $false
        }
    }

    $source = Get-Item -LiteralPath $SourcePath -ErrorAction Stop
    $transportPath = Join-Path $TransportRoot $source.Name
    $stagingPath = $transportPath + '.dsg-partial'
    $manifestPath = $transportPath + '.ready.json'
    $sourceHash = Get-DSGTransportSha256 -LiteralPath $SourcePath

    if (Test-Path -LiteralPath $transportPath -PathType Leaf) {
        $existing = Get-Item -LiteralPath $transportPath -ErrorAction Stop
        if ([int64]$existing.Length -ne [int64]$source.Length) {
            throw "Transport conflict: size differs for $transportPath"
        }
        $existingHash = Get-DSGTransportSha256 -LiteralPath $transportPath
        if ($existingHash -ne $sourceHash) {
            throw "Transport conflict: SHA-256 differs for $transportPath"
        }
    }
    else {
        Remove-Item -LiteralPath $stagingPath -Force -ErrorAction SilentlyContinue
        Copy-Item -LiteralPath $SourcePath -Destination $stagingPath -ErrorAction Stop

        $stage = Get-Item -LiteralPath $stagingPath -ErrorAction Stop
        $stageHash = Get-DSGTransportSha256 -LiteralPath $stagingPath
        if ([int64]$stage.Length -ne [int64]$source.Length -or $stageHash -ne $sourceHash) {
            Remove-Item -LiteralPath $stagingPath -Force -ErrorAction SilentlyContinue
            throw 'OneDrive transport staging verification failed.'
        }

        Move-Item -LiteralPath $stagingPath -Destination $transportPath -ErrorAction Stop
    }

    $manifest = [pscustomobject][ordered]@{
        SchemaVersion = '1.0'
        State = 'READY'
        FileName = $source.Name
        SizeBytes = [int64]$source.Length
        Sha256 = $sourceHash
        SourceHost = $env:COMPUTERNAME
        SourcePath = $source.FullName
        Transport = 'OneDrive'
        CreatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    }

    $manifest |
        ConvertTo-Json -Depth 5 |
        Set-Content -LiteralPath $manifestPath -Encoding UTF8

    return [pscustomobject][ordered]@{
        Status = 'READY'
        SourcePath = $source.FullName
        TransportPath = $transportPath
        ManifestPath = $manifestPath
        SizeBytes = [int64]$source.Length
        Sha256 = $sourceHash
        SourceDeleted = $false
    }
}

function Import-DSGOneDriveTransportFile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ManifestPath,
        [Parameter(Mandatory = $true)][string]$DestinationRoot,
        [Parameter(Mandatory = $true)][string]$DestinationPath
    )

    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        throw "READY manifest not found: $ManifestPath"
    }

    $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    if ([string]$manifest.State -ne 'READY') {
        throw "Manifest state must be READY. Observed: $($manifest.State)"
    }

    $transportPath = Join-Path (Split-Path -Parent $ManifestPath) ([string]$manifest.FileName)
    if (-not (Test-Path -LiteralPath $transportPath -PathType Leaf)) {
        throw "Transport file not found: $transportPath"
    }

    $transportItem = Get-Item -LiteralPath $transportPath -ErrorAction Stop
    if ([int64]$transportItem.Length -ne [int64]$manifest.SizeBytes) {
        throw 'Transport file size does not match READY manifest.'
    }

    $transportHash = Get-DSGTransportSha256 -LiteralPath $transportPath
    if ($transportHash -ne ([string]$manifest.Sha256).ToLowerInvariant()) {
        throw 'Transport file SHA-256 does not match READY manifest.'
    }

    $transferModule = Join-Path $PSScriptRoot 'DSG.SessionTransfer.psm1'
    Import-Module $transferModule -Force

    $result = Invoke-DSGCopyOnlyFile `
        -SourcePath $transportPath `
        -DestinationRoot $DestinationRoot `
        -DestinationPath $DestinationPath

    return [pscustomobject][ordered]@{
        Status = $result.Status
        ManifestPath = $ManifestPath
        TransportPath = $transportPath
        DestinationPath = $DestinationPath
        SourceSha256 = ([string]$manifest.Sha256).ToLowerInvariant()
        TransportSha256 = $transportHash
        DestinationSha256 = $result.DestinationSha256
        SourceDeleted = $false
        TransportDeleted = $false
        OverwritePerformed = $false
    }
}

Export-ModuleMember -Function @(
    'Get-DSGTransportSha256',
    'Test-DSGTransportStableFile',
    'Export-DSGOneDriveTransportFile',
    'Import-DSGOneDriveTransportFile'
)
