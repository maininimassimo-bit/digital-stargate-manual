$ErrorActionPreference = 'Stop'
$validator = Join-Path $PSScriptRoot 'validate-session-promotion.ps1'
$sessionId = '2099-01-01_2099-01-02'

function New-TestPackage {
    param([string]$Status = 'COMPLETE')
    $base = Join-Path ([System.IO.Path]::GetTempPath()) ("dsg-promotion-" + [guid]::NewGuid().ToString('N'))
    $root = Join-Path $base "data/sessions/2099/01/$sessionId"
    foreach ($dir in @('raw/nina','raw/phd2','raw/weather')) {
        New-Item -ItemType Directory -Path (Join-Path $root $dir) -Force | Out-Null
    }
    Set-Content -Path (Join-Path $root 'raw/nina/nina.log') -Value 'nina' -NoNewline
    Set-Content -Path (Join-Path $root 'raw/phd2/phd2.log') -Value 'phd2' -NoNewline
    Set-Content -Path (Join-Path $root 'raw/weather/weather.csv') -Value 'weather' -NoNewline
    $files = foreach ($relative in @('raw/nina/nina.log','raw/phd2/phd2.log','raw/weather/weather.csv')) {
        $path = Join-Path $root $relative
        [ordered]@{
            path = $relative
            size_bytes = (Get-Item $path).Length
            sha256 = (Get-FileHash $path -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }
    [ordered]@{ session_id = $sessionId; report_status = $Status; files = @($files) } |
        ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $root 'manifest.json')
    [pscustomobject]@{ Base = $base; Root = $root }
}

function Assert-Pass {
    param([scriptblock]$Action, [string]$Name)
    try { & $Action | Out-Null; Write-Host "PASS $Name" }
    catch { throw "Expected PASS for $Name but got: $($_.Exception.Message)" }
}

function Assert-Reject {
    param([scriptblock]$Action, [string]$Pattern, [string]$Name)
    try { & $Action | Out-Null; throw "Expected rejection for $Name" }
    catch {
        if ($_.Exception.Message -like "Expected rejection*") { throw }
        if ($_.Exception.Message -notmatch $Pattern) { throw "Wrong rejection for $Name`: $($_.Exception.Message)" }
        Write-Host "PASS rejection $Name -> $($_.Exception.Message)"
    }
}

$packages = @()
try {
    $p = New-TestPackage; $packages += $p.Base
    Assert-Pass { & $validator -SessionId $sessionId -Root $p.Root -SkipAncestry -SkipScope } 'nominal COMPLETE/hash contract'

    $p = New-TestPackage -Status 'PARTIAL'; $packages += $p.Base
    Assert-Reject { & $validator -SessionId $sessionId -Root $p.Root -SkipAncestry -SkipScope } 'not COMPLETE' 'PARTIAL'

    $p = New-TestPackage; $packages += $p.Base
    $manifestPath = Join-Path $p.Root 'manifest.json'
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    $manifest.files[0].size_bytes = [int64]$manifest.files[0].size_bytes + 1
    $manifest | ConvertTo-Json -Depth 5 | Set-Content $manifestPath
    Assert-Reject { & $validator -SessionId $sessionId -Root $p.Root -SkipAncestry -SkipScope } 'size mismatch' 'manifest size mismatch'

    $p = New-TestPackage; $packages += $p.Base
    $manifestPath = Join-Path $p.Root 'manifest.json'
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    $manifest.files[0].sha256 = ('0' * 64)
    $manifest | ConvertTo-Json -Depth 5 | Set-Content $manifestPath
    Assert-Reject { & $validator -SessionId $sessionId -Root $p.Root -SkipAncestry -SkipScope } 'SHA-256 mismatch' 'manifest SHA-256 mismatch'

    $p = New-TestPackage; $packages += $p.Base
    Assert-Reject { & $validator -SessionId $sessionId -Root $p.Root -SkipAncestry -ChangedPaths @("data/sessions/2099/01/$sessionId/manifest.json", 'README.md') } 'Unexpected path' 'extraneous scope'

    $p = New-TestPackage; $packages += $p.Base
    $gitRoot = Join-Path $p.Base 'git-fixture'
    New-Item -ItemType Directory -Path $gitRoot -Force | Out-Null
    Push-Location $gitRoot
    try {
        git init -q
        git config user.email 'ci@digital-stargate.invalid'
        git config user.name 'Digital StarGate CI'
        Set-Content baseline.txt 'baseline'
        git add .; git commit -q -m baseline
        git branch main
        git checkout -q -b session-test
        Set-Content session.txt 'session'; git add .; git commit -q -m session
        git checkout -q --orphan unrelated
        git rm -rf -q .
        Set-Content unrelated.txt 'unrelated'; git add .; git commit -q -m unrelated
        Assert-Reject { & $validator -SessionId $sessionId -Root $p.Root -BaseRef main -SkipScope } 'not a fast-forward descendant' 'non-descendant ancestry'
    } finally { Pop-Location }
} finally {
    foreach ($path in $packages) { Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue }
}

Write-Host 'Session promotion contract tests PASS.'
