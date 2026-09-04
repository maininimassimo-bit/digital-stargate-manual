BeforeAll {
    $script:modulePath = Join-Path $PSScriptRoot '..\DSG.VerifiedTransportCleanup.psm1'
    $script:dryRunPath = Join-Path $PSScriptRoot '..\Invoke-DSGVerifiedTransportCleanupDryRun.ps1'
    Import-Module $script:modulePath -Force
}

Describe 'AP-013C failure injection: EAGLE 445/445 vs PC 426/426' {
    BeforeEach {
        $root = Join-Path $TestDrive ([guid]::NewGuid().ToString('N'))
        $transportRoot = Join-Path $root 'transport'
        $destinationRoot = Join-Path $root 'destination'
        $evidenceRoot = Join-Path $root 'evidence'
        New-Item -ItemType Directory -Path $transportRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null

        $script:readyPaths = @()
        $script:destinationPaths = @()

        1..445 | ForEach-Object {
            $name = ('frame-{0:D4}.xisf' -f $_)
            $destinationPath = Join-Path $destinationRoot $name
            [System.IO.File]::WriteAllText($destinationPath, ('synthetic-frame-' + $_))
            $hash = (Get-FileHash -LiteralPath $destinationPath -Algorithm SHA256).Hash
            $readyPath = (Join-Path $transportRoot $name) + '.ready.json'
            [pscustomobject][ordered]@{
                SchemaVersion = '1.0'
                State = 'READY'
                FileName = $name
                SizeBytes = (Get-Item -LiteralPath $destinationPath).Length
                Sha256 = $hash
                SourceHost = 'TEST-EAGLE'
                SourcePath = ('D:\Images NINA\Target\' + $name)
                Transport = 'OneDrive'
                CreatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
            } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $readyPath -Encoding UTF8
            $script:readyPaths += $readyPath
            $script:destinationPaths += $destinationPath
        }

        0..425 | ForEach-Object {
            $readyPath = $script:readyPaths[$_]
            $ready = Get-Content -LiteralPath $readyPath -Raw | ConvertFrom-Json
            $ackPath = (Join-Path $transportRoot ([string]$ready.FileName)) + '.imported.json'
            New-DSGDestinationVerificationAck -ReadyManifestPath $readyPath -DestinationPath $script:destinationPaths[$_] -AckPath $ackPath -VerifiedByHost 'TEST-PC' | Out-Null
        }
    }

    It 'keeps the 19 non-converged assets blocked and deletes nothing' {
        $run = & $script:dryRunPath -TransportRoot $transportRoot -EvidenceRoot $evidenceRoot

        $run.Summary.ReadyObserved | Should -Be 445
        $run.Summary.CleanupEligible | Should -Be 426
        $run.Summary.Blocked | Should -Be 19
        $run.Summary.Deleted | Should -Be 0
        @($run.Results | Where-Object { $_.ReasonCode -eq 'ACK_MISSING' }).Count | Should -Be 19
        @($run.Results | Where-Object { $_.CleanupEligible }).Count | Should -Be 426
    }

    It 'reaches 445 eligible only after the missing 19 ACKs converge and still deletes nothing' {
        426..444 | ForEach-Object {
            $readyPath = $script:readyPaths[$_]
            $ready = Get-Content -LiteralPath $readyPath -Raw | ConvertFrom-Json
            $ackPath = (Join-Path $transportRoot ([string]$ready.FileName)) + '.imported.json'
            New-DSGDestinationVerificationAck -ReadyManifestPath $readyPath -DestinationPath $script:destinationPaths[$_] -AckPath $ackPath -VerifiedByHost 'TEST-PC' | Out-Null
        }

        $run = & $script:dryRunPath -TransportRoot $transportRoot -EvidenceRoot $evidenceRoot

        $run.Summary.ReadyObserved | Should -Be 445
        $run.Summary.CleanupEligible | Should -Be 445
        $run.Summary.Blocked | Should -Be 0
        $run.Summary.Deleted | Should -Be 0
        @($run.Results | Where-Object { -not $_.CleanupEligible }).Count | Should -Be 0
    }
}
