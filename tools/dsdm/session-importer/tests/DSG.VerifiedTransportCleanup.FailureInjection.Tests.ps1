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
        $script:transportPaths = @()
        $script:destinationPaths = @()

        1..445 | ForEach-Object {
            $name = ('frame-{0:D4}.xisf' -f $_)
            $transportPath = Join-Path $transportRoot $name
            $destinationPath = Join-Path $destinationRoot $name
            [System.IO.File]::WriteAllText($transportPath, ('synthetic-frame-' + $_))
            Copy-Item -LiteralPath $transportPath -Destination $destinationPath
            $hash = (Get-FileHash -LiteralPath $destinationPath -Algorithm SHA256).Hash
            $readyPath = $transportPath + '.ready.json'
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
            $script:transportPaths += $transportPath
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

    It 'keeps the 19 non-converged assets blocked and authorizes no cleanup' {
        $run = & $script:dryRunPath -TransportRoot $transportRoot -EvidenceRoot $evidenceRoot

        $run.Summary.XisfObserved | Should -Be 445
        $run.Summary.ReadyObserved | Should -Be 445
        $run.Summary.AckObserved | Should -Be 426
        $run.Summary.TechnicalCandidates | Should -Be 426
        $run.Summary.CleanupAuthorized | Should -Be 0
        $run.Summary.Blocked | Should -Be 19
        $run.Summary.Deleted | Should -Be 0
        @($run.Results | Where-Object { $_.ReasonCode -eq 'ACK_MISSING' }).Count | Should -Be 19
        @($run.Results | Where-Object { $_.TechnicalCandidate }).Count | Should -Be 426
        @($run.Results | Where-Object { $_.CleanupAuthorized }).Count | Should -Be 0
    }

    It 'reaches 445 technical candidates only after reconvergence while authorization stays zero' {
        426..444 | ForEach-Object {
            $readyPath = $script:readyPaths[$_]
            $ready = Get-Content -LiteralPath $readyPath -Raw | ConvertFrom-Json
            $ackPath = (Join-Path $transportRoot ([string]$ready.FileName)) + '.imported.json'
            New-DSGDestinationVerificationAck -ReadyManifestPath $readyPath -DestinationPath $script:destinationPaths[$_] -AckPath $ackPath -VerifiedByHost 'TEST-PC' | Out-Null
        }

        $run = & $script:dryRunPath -TransportRoot $transportRoot -EvidenceRoot $evidenceRoot

        $run.Summary.XisfObserved | Should -Be 445
        $run.Summary.ReadyObserved | Should -Be 445
        $run.Summary.AckObserved | Should -Be 445
        $run.Summary.TechnicalCandidates | Should -Be 445
        $run.Summary.CleanupAuthorized | Should -Be 0
        $run.Summary.Blocked | Should -Be 0
        $run.Summary.Deleted | Should -Be 0
        @($run.Results | Where-Object { -not $_.TechnicalCandidate }).Count | Should -Be 0
        @($run.Results | Where-Object { $_.CleanupAuthorized }).Count | Should -Be 0
    }

    It 'discovers orphan and missing transport combinations without authorizing cleanup' {
        $orphanTransport = Join-Path $transportRoot 'orphan-no-ready.xisf'
        [System.IO.File]::WriteAllText($orphanTransport, 'orphan')

        $missingTransport = Join-Path $transportRoot 'ready-no-payload.xisf'
        $missingReady = $missingTransport + '.ready.json'
        [pscustomobject][ordered]@{
            SchemaVersion = '1.0'; State = 'READY'; FileName = 'ready-no-payload.xisf'
            SizeBytes = 7; Sha256 = ('A' * 64); SourceHost = 'TEST-EAGLE'
            SourcePath = 'D:\Images NINA\Target\ready-no-payload.xisf'
            Transport = 'OneDrive'; CreatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
        } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $missingReady -Encoding UTF8

        $orphanAckTransport = Join-Path $transportRoot 'orphan-ack.xisf'
        $orphanAck = $orphanAckTransport + '.imported.json'
        [pscustomobject]@{ SchemaVersion='1.0'; State='DESTINATION_VERIFIED'; FileName='orphan-ack.xisf' } |
            ConvertTo-Json | Set-Content -LiteralPath $orphanAck -Encoding UTF8

        $run = & $script:dryRunPath -TransportRoot $transportRoot -EvidenceRoot $evidenceRoot

        @($run.Results | Where-Object { $_.ReasonCode -eq 'READY_MISSING' }).Count | Should -Be 1
        @($run.Results | Where-Object { $_.ReasonCode -eq 'TRANSPORT_PAYLOAD_MISSING' }).Count | Should -Be 1
        @($run.Results | Where-Object { $_.ReasonCode -eq 'ORPHAN_ACK_READY_MISSING' }).Count | Should -Be 1
        $run.Summary.CleanupAuthorized | Should -Be 0
        $run.Summary.Deleted | Should -Be 0
    }
}
