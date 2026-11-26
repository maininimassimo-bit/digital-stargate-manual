param(
    [Parameter(Mandatory)][string]$RootK,
    [Parameter(Mandatory)][string]$RootH,
    [Parameter(Mandatory)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
$repo = 'maininimassimo-bit/digital-stargate-manual'
$source = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'fonti.json') -Raw | ConvertFrom-Json -AsHashtable

function Read-GitHubFile($path, $commit) {
    $url = 'repos/{0}/contents/{1}?ref={2}' -f $repo, $path, $commit
    $response = gh api $url | ConvertFrom-Json -AsHashtable
    if ($LASTEXITCODE -ne 0 -or $response.encoding -ne 'base64') { throw "GitHub readback failed for $path" }
    $bytes = [Convert]::FromBase64String($response.content)
    [ordered]@{
        gitBlob = $response.sha
        sha256 = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    }
}

$baseline = Read-GitHubFile $source.baseline.path $source.baseline.commit
$ledgerPath = Join-Path $RootK 'BKL046-requisiti-residui-v65\rendiconto-VM-v65.json'
if ((Get-FileHash -LiteralPath $ledgerPath).Hash -ine $source.ledger) { throw 'Changed residual ledger' }
$ledger = Get-Content -LiteralPath $ledgerPath -Raw | ConvertFrom-Json -AsHashtable
$records = [ordered]@{}
$evidence = @{}
foreach ($study in $source.studies) {
    $directory = Join-Path $RootK $study.dir
    $archiveName = $study.dir + '.zip'
    $archives = @(
        (Join-Path $directory $archiveName)
        (Join-Path (Join-Path $RootH $study.h) $archiveName)
    )
    foreach ($archive in $archives) {
        if ((Get-FileHash -LiteralPath $archive).Hash -ine $study.archive) { throw "Changed archive $archive" }
    }
    $zip = [IO.Compression.ZipFile]::OpenRead($archives[0])
    try {
        $verified = [ordered]@{}
        foreach ($filename in $study.files.Keys) {
            $hash = $study.files[$filename]
            $local = Join-Path $directory $filename
            if ((Get-FileHash -LiteralPath $local).Hash -ine $hash) { throw "Changed local receipt $local" }
            $entries = @($zip.Entries | Where-Object FullName -CEQ $filename)
            if ($entries.Count -ne 1) { throw "Unexpected archive members for $filename" }
            $stream = $entries[0].Open()
            try {
                $memberHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($stream))
                if ($memberHash -ine $hash) { throw "Changed archive member $filename" }
            } finally {
                $stream.Dispose()
            }
            $path = "$($study.git)/$filename"
            $readback = Read-GitHubFile $path $study.commit
            if ($readback.sha256 -cne $hash) { throw "Changed GitHub receipt $path" }
            $verified[$filename] = [ordered]@{ path = $path; gitBlob = $readback.gitBlob; sha256 = $hash }
            $payload = Get-Content -LiteralPath $local -Raw | ConvertFrom-Json -AsHashtable
            if ($payload.scientificClosures -ne 0 -or $payload.nativeExecutions -ne 0) { throw "Unexpected evidence class $filename" }
            $evidence["$($study.dir)/$filename"] = $payload
        }
    } finally {
        $zip.Dispose()
    }
    $axes = [ordered]@{}
    foreach ($axis in $study.axes) {
        if ($ledger.axes[$axis].open -ne $true) { throw "Expected open axis $axis" }
        $axes[$axis] = $ledger.axes[$axis].title
    }
    $records[$study.dir] = [ordered]@{
        axes = $axes
        archiveSha256 = $study.archive
        archiveCopiesVerified = 2
        commit = $study.commit
        files = $verified
    }
}
$m8 = $evidence['BKL046-M8-M20-rumore-pari-raggio-incertezza-v1/riscontro.json']
$ic = $evidence['BKL046-IC1805-rumore-pari-raggio-incertezza-v1/riscontro.json']
$join = $evidence['BKL046-IC1805-rumore-pari-raggio-incertezza-v1/trasferimento.json']
$reg = $evidence['BKL046-M51-registrazione-tre-pose-v1/riscontro.json']
$variance = $evidence['BKL046-M8-M20-varianza-segnale-v1/riscontro.json']
if ($join.ic1805Sha256 -cne $source.studies[3].files['riscontro.json'] -or
    $join.m8m20Sha256 -cne $source.studies[2].files['riscontro.json']) { throw 'Join refers to different receipts' }

$p90 = @(foreach ($method in $reg.results.Values) {
    foreach ($weight in $method.Values) {
        foreach ($pair in '0-1', '0-2', '1-2') { $weight[$pair].p90Px }
    }
})
$report = [ordered]@{
    schema = 'BKL046_KNOWLEDGE_NOISE_REGISTRATION_ADDENDUM_V1'
    baseline = [ordered]@{ commit = $source.baseline.commit; path = $source.baseline.path; sha256 = $baseline.sha256 }
    residualLedgerSha256 = $source.ledger
    evidence = $records
    findings = [ordered]@{
        rawGainCalibrated = $variance.gainCalibrated
        m8m20StableBilinearCases = @($m8.rows | Where-Object direction -CEQ 'bilinearLower').Count
        ic1805StableBilinearCases = @($ic.rows | Where-Object direction -CEQ 'bilinearLower').Count
        comparedEndpointsPerReconstructedField = $m8.rows.Count
        g1EndpointsReplicated = $join.replicated
        g1EndpointsTested = $join.results.Count
        m51CommonHeldOutStars = $reg.commonHoldout
        m51BestDirectP90Px = ($p90 | Measure-Object -Minimum).Minimum
        registrationDiagnosticThresholdPx = 0.30
    }
    remaining = @(
        'Native matched-scale and matched-response measurements under the approved coordinator'
        'Independent calibrated Bayer acquisition with acceptable registration and appropriate repeats'
        'Absolute noise/flux calibration across read-noise, mixed and signal-dominated regimes'
        'Verified complete knowledge delivery and remote corpus reconstruction'
    )
    scientificClosures = 0
    finalKnowledge = $false
    fullGitHubTransfer = $false
}
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($report | ConvertTo-Json -Depth 15) + [char]10)
$stream = [IO.File]::Open($OutputPath, 'CreateNew', 'Write', 'None')
try {
    $stream.Write($bytes, 0, $bytes.Length)
} finally {
    $stream.Dispose()
}
