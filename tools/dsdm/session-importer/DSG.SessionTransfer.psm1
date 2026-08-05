Set-StrictMode -Version Latest

function Test-DSGPathUnderRoot {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$RootPath,
        [Parameter(Mandatory = $true)][string]$CandidatePath
    )

    $root = [System.IO.Path]::GetFullPath($RootPath).TrimEnd('\') + '\'
    $candidate = [System.IO.Path]::GetFullPath($CandidatePath)

    return $candidate.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)
}

function Get-DSGFileSha256 {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) {
        throw "File not found: $LiteralPath"
    }

    return (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-DSGCollisionState {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$SourcePath,
        [Parameter(Mandatory = $true)][string]$DestinationPath
    )

    if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
        throw "Source file not found: $SourcePath"
    }

    if (-not (Test-Path -LiteralPath $DestinationPath -PathType Leaf)) {
        return [pscustomobject][ordered]@{
            State = 'NEW'
            SourceSize = [int64](Get-Item -LiteralPath $SourcePath).Length
            DestinationSize = $null
            SourceSha256 = $null
            DestinationSha256 = $null
        }
    }

    $sourceSize = [int64](Get-Item -LiteralPath $SourcePath).Length
    $destinationSize = [int64](Get-Item -LiteralPath $DestinationPath).Length

    if ($sourceSize -ne $destinationSize) {
        return [pscustomobject][ordered]@{
            State = 'CONFLICT'
            SourceSize = $sourceSize
            DestinationSize = $destinationSize
            SourceSha256 = $null
            DestinationSha256 = $null
        }
    }

    $sourceHash = Get-DSGFileSha256 -LiteralPath $SourcePath
    $destinationHash = Get-DSGFileSha256 -LiteralPath $DestinationPath

    $state = if ($sourceHash -eq $destinationHash) { 'IDENTICAL' } else { 'CONFLICT' }

    return [pscustomobject][ordered]@{
        State = $state
        SourceSize = $sourceSize
        DestinationSize = $destinationSize
        SourceSha256 = $sourceHash
        DestinationSha256 = $destinationHash
    }
}

function Test-DSGStableObservation {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]$FirstObservation,
        [Parameter(Mandatory = $true)]$SecondObservation
    )

    return (
        [int64]$FirstObservation.SizeBytes -eq [int64]$SecondObservation.SizeBytes -and
        [string]$FirstObservation.LastWriteTimeUtc -eq [string]$SecondObservation.LastWriteTimeUtc
    )
}

function New-DSGFileObservation {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    $item = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
    return [pscustomobject][ordered]@{
        Path = $item.FullName
        SizeBytes = [int64]$item.Length
        LastWriteTimeUtc = $item.LastWriteTimeUtc.ToString('o')
        ObservedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    }
}

function Invoke-DSGCopyOnlyFile {
    [CmdletBinding(SupportsShouldProcess = $true)]
    param(
        [Parameter(Mandatory = $true)][string]$SourcePath,
        [Parameter(Mandatory = $true)][string]$DestinationRoot,
        [Parameter(Mandatory = $true)][string]$DestinationPath,
        [Parameter(Mandatory = $false)][string]$StagingExtension = '.dsg-partial'
    )

    if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
        throw "Source file not found: $SourcePath"
    }

    if (-not (Test-DSGPathUnderRoot -RootPath $DestinationRoot -CandidatePath $DestinationPath)) {
        throw 'Destination path escapes the authorized root.'
    }

    $collision = Get-DSGCollisionState -SourcePath $SourcePath -DestinationPath $DestinationPath
    if ($collision.State -eq 'IDENTICAL') {
        return [pscustomobject][ordered]@{
            Status = 'SKIP_IDENTICAL'
            SourcePath = $SourcePath
            DestinationPath = $DestinationPath
            SourceSha256 = $collision.SourceSha256
            DestinationSha256 = $collision.DestinationSha256
            SourceDeleted = $false
        }
    }

    if ($collision.State -eq 'CONFLICT') {
        throw 'Destination conflict detected. Overwrite is prohibited.'
    }

    $destinationDirectory = Split-Path -Parent $DestinationPath
    $stagingPath = $DestinationPath + $StagingExtension

    if (-not (Test-DSGPathUnderRoot -RootPath $DestinationRoot -CandidatePath $stagingPath)) {
        throw 'Staging path escapes the authorized root.'
    }

    if (Test-Path -LiteralPath $stagingPath) {
        Remove-Item -LiteralPath $stagingPath -Force -ErrorAction Stop
    }

    $sourceHash = Get-DSGFileSha256 -LiteralPath $SourcePath
    $sourceSize = [int64](Get-Item -LiteralPath $SourcePath).Length

    if ($PSCmdlet.ShouldProcess($DestinationPath, 'Copy scientific file using staging and SHA-256 verification')) {
        New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null
        Copy-Item -LiteralPath $SourcePath -Destination $stagingPath -Force -ErrorAction Stop

        $stagingSize = [int64](Get-Item -LiteralPath $stagingPath).Length
        $stagingHash = Get-DSGFileSha256 -LiteralPath $stagingPath

        if ($sourceSize -ne $stagingSize -or $sourceHash -ne $stagingHash) {
            Remove-Item -LiteralPath $stagingPath -Force -ErrorAction SilentlyContinue
            throw 'Post-copy verification failed. Staging file removed.'
        }

        Move-Item -LiteralPath $stagingPath -Destination $DestinationPath -ErrorAction Stop
        $destinationHash = Get-DSGFileSha256 -LiteralPath $DestinationPath

        if ($destinationHash -ne $sourceHash) {
            throw 'Final destination hash verification failed.'
        }

        return [pscustomobject][ordered]@{
            Status = 'COPIED_VERIFIED'
            SourcePath = $SourcePath
            DestinationPath = $DestinationPath
            SizeBytes = $sourceSize
            SourceSha256 = $sourceHash
            DestinationSha256 = $destinationHash
            SourceDeleted = $false
        }
    }
}

Export-ModuleMember -Function @(
    'Test-DSGPathUnderRoot',
    'Get-DSGFileSha256',
    'Get-DSGCollisionState',
    'Test-DSGStableObservation',
    'New-DSGFileObservation',
    'Invoke-DSGCopyOnlyFile'
)
