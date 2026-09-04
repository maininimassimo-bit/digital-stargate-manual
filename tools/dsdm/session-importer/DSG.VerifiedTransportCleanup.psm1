Set-StrictMode -Version Latest

$script:AckSchemaVersion = '1.0'
$script:AckState = 'DESTINATION_VERIFIED'

function Get-DSGCleanupSha256 {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$LiteralPath)

    if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) {
        throw "File not found: $LiteralPath"
    }

    return (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash.ToUpperInvariant()
}

function Read-DSGJsonFile {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$LiteralPath)

    if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) {
        throw "JSON file not found: $LiteralPath"
    }

    return (Get-Content -LiteralPath $LiteralPath -Raw | ConvertFrom-Json)
}

function Test-DSGReadyManifest {
    [CmdletBinding()]
    param([Parameter(Mandatory)][object]$Manifest)

    if ([string]$Manifest.State -ne 'READY') { return $false }
    if ([string]::IsNullOrWhiteSpace([string]$Manifest.FileName)) { return $false }
    if ([long]$Manifest.SizeBytes -lt 0) { return $false }
    if ([string]::IsNullOrWhiteSpace([string]$Manifest.Sha256)) { return $false }
    return $true
}

function New-DSGDestinationVerificationAck {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$ReadyManifestPath,
        [Parameter(Mandatory)][string]$DestinationPath,
        [Parameter(Mandatory)][string]$AckPath,
        [string]$CorrelationId = ([guid]::NewGuid().ToString()),
        [string]$VerifiedByHost = $env:COMPUTERNAME
    )

    $ready = Read-DSGJsonFile -LiteralPath $ReadyManifestPath
    if (-not (Test-DSGReadyManifest -Manifest $ready)) {
        throw 'READY manifest is invalid.'
    }
    if (-not (Test-Path -LiteralPath $DestinationPath -PathType Leaf)) {
        throw "Destination not found: $DestinationPath"
    }

    $destination = Get-Item -LiteralPath $DestinationPath
    if ([long]$destination.Length -ne [long]$ready.SizeBytes) {
        throw 'Destination size does not match READY manifest.'
    }

    $destinationHash = Get-DSGCleanupSha256 -LiteralPath $DestinationPath
    $expectedHash = ([string]$ready.Sha256).ToUpperInvariant()
    if ($destinationHash -ne $expectedHash) {
        throw 'Destination SHA-256 does not match READY manifest.'
    }

    $ack = [pscustomobject][ordered]@{
        SchemaVersion = $script:AckSchemaVersion
        State = $script:AckState
        FileName = [string]$ready.FileName
        SizeBytes = [long]$ready.SizeBytes
        Sha256 = $expectedHash
        ReadyManifestSha256 = Get-DSGCleanupSha256 -LiteralPath $ReadyManifestPath
        DestinationPath = $DestinationPath
        DestinationSha256 = $destinationHash
        VerifiedByHost = $VerifiedByHost
        VerifiedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
        CorrelationId = $CorrelationId
    }

    $parent = Split-Path -Parent $AckPath
    if (-not [string]::IsNullOrWhiteSpace($parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if (Test-Path -LiteralPath $AckPath -PathType Leaf) {
        $existing = Read-DSGJsonFile -LiteralPath $AckPath
        $same = (
            [string]$existing.SchemaVersion -eq $script:AckSchemaVersion -and
            [string]$existing.State -eq $script:AckState -and
            [string]$existing.FileName -eq [string]$ack.FileName -and
            [long]$existing.SizeBytes -eq [long]$ack.SizeBytes -and
            ([string]$existing.Sha256).ToUpperInvariant() -eq $ack.Sha256 -and
            ([string]$existing.ReadyManifestSha256).ToUpperInvariant() -eq $ack.ReadyManifestSha256 -and
            ([string]$existing.DestinationSha256).ToUpperInvariant() -eq $ack.DestinationSha256
        )
        if (-not $same) {
            throw "ACK conflict detected: $AckPath"
        }
        return [pscustomobject]@{ Status = 'ACK_EXISTS_VERIFIED'; AckPath = $AckPath; Ack = $existing }
    }

    $tempPath = $AckPath + '.dsg-partial-' + [guid]::NewGuid().ToString('N')
    try {
        $ack | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $tempPath -Encoding UTF8
        Move-Item -LiteralPath $tempPath -Destination $AckPath
    }
    finally {
        if (Test-Path -LiteralPath $tempPath -PathType Leaf) {
            Remove-Item -LiteralPath $tempPath -Force
        }
    }

    return [pscustomobject]@{ Status = 'ACK_CREATED'; AckPath = $AckPath; Ack = $ack }
}

function Test-DSGCleanupEvidence {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$ReadyManifestPath,
        [Parameter(Mandatory)][string]$AckPath,
        [string]$TransportPath
    )

    if ([string]::IsNullOrWhiteSpace($TransportPath)) {
        $TransportPath = $ReadyManifestPath.Substring(0, $ReadyManifestPath.Length - '.ready.json'.Length)
    }

    $result = [ordered]@{
        FileName = $null
        State = 'BLOCKED'
        TechnicalCandidate = $false
        CleanupEligible = $false
        CleanupAuthorized = $false
        ReasonCode = 'UNKNOWN'
        PolicyReasonCode = 'RETENTION_NOT_APPROVED'
        TransportPath = $TransportPath
        ReadyManifestPath = $ReadyManifestPath
        AckPath = $AckPath
        Deleted = 0
    }

    if (-not (Test-Path -LiteralPath $ReadyManifestPath -PathType Leaf)) {
        $result.ReasonCode = 'READY_MISSING'
        return [pscustomobject]$result
    }

    try { $ready = Read-DSGJsonFile -LiteralPath $ReadyManifestPath } catch {
        $result.ReasonCode = 'READY_INVALID'; return [pscustomobject]$result
    }
    if (-not (Test-DSGReadyManifest -Manifest $ready)) {
        $result.ReasonCode = 'READY_INVALID'; return [pscustomobject]$result
    }
    $result.FileName = [string]$ready.FileName

    if (-not (Test-Path -LiteralPath $TransportPath -PathType Leaf)) {
        $result.ReasonCode = 'TRANSPORT_PAYLOAD_MISSING'
        return [pscustomobject]$result
    }

    if (-not (Test-Path -LiteralPath $AckPath -PathType Leaf)) {
        $result.ReasonCode = 'ACK_MISSING'
        return [pscustomobject]$result
    }

    try { $ack = Read-DSGJsonFile -LiteralPath $AckPath } catch {
        $result.ReasonCode = 'ACK_INVALID'; return [pscustomobject]$result
    }

    if ([string]$ack.SchemaVersion -ne $script:AckSchemaVersion -or [string]$ack.State -ne $script:AckState) {
        $result.ReasonCode = 'ACK_INVALID'; return [pscustomobject]$result
    }
    if ([string]$ack.FileName -ne [string]$ready.FileName -or [long]$ack.SizeBytes -ne [long]$ready.SizeBytes) {
        $result.ReasonCode = 'ACK_INVALID'; return [pscustomobject]$result
    }

    $expectedHash = ([string]$ready.Sha256).ToUpperInvariant()
    if (([string]$ack.Sha256).ToUpperInvariant() -ne $expectedHash -or ([string]$ack.DestinationSha256).ToUpperInvariant() -ne $expectedHash) {
        $result.ReasonCode = 'DESTINATION_HASH_MISMATCH'; return [pscustomobject]$result
    }

    $readyHash = Get-DSGCleanupSha256 -LiteralPath $ReadyManifestPath
    if (([string]$ack.ReadyManifestSha256).ToUpperInvariant() -ne $readyHash) {
        $result.ReasonCode = 'ACK_READY_HASH_MISMATCH'; return [pscustomobject]$result
    }

    $result.State = 'TECHNICAL_CANDIDATE_DRY_RUN'
    $result.TechnicalCandidate = $true
    $result.CleanupEligible = $false
    $result.CleanupAuthorized = $false
    $result.ReasonCode = 'TECHNICAL_CANDIDATE_POLICY_BLOCKED'
    return [pscustomobject]$result
}

Export-ModuleMember -Function Get-DSGCleanupSha256, New-DSGDestinationVerificationAck, Test-DSGCleanupEvidence
