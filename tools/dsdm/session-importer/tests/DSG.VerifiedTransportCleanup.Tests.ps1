BeforeAll {
    $script:modulePath = Join-Path $PSScriptRoot '..\DSG.VerifiedTransportCleanup.psm1'
    Import-Module $script:modulePath -Force
}

Describe 'AP-013C destination verification ACK' {
    BeforeEach {
        $root = Join-Path $TestDrive ([guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $root -Force | Out-Null
        $transport = Join-Path $root 'sample.xisf'
        $destination = Join-Path $root 'destination.xisf'
        [System.IO.File]::WriteAllText($transport, 'synthetic-scientific-content')
        Copy-Item -LiteralPath $transport -Destination $destination
        $hash = Get-DSGCleanupSha256 -LiteralPath $transport
        $ready = $transport + '.ready.json'
        [pscustomobject][ordered]@{
            SchemaVersion = '1.0'; State = 'READY'; FileName = 'sample.xisf'
            SizeBytes = (Get-Item -LiteralPath $transport).Length; Sha256 = $hash
            SourceHost = 'TEST-EAGLE'; SourcePath = 'D:\Images NINA\Target\sample.xisf'
            Transport = 'OneDrive'; CreatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
        } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ready -Encoding UTF8
        $ack = $transport + '.imported.json'
    }

    It 'creates a destination verified ACK and never deletes scientific files' {
        $result = New-DSGDestinationVerificationAck -ReadyManifestPath $ready -DestinationPath $destination -AckPath $ack -VerifiedByHost 'TEST-PC'
        $result.Status | Should -Be 'ACK_CREATED'
        Test-Path -LiteralPath $transport | Should -BeTrue
        Test-Path -LiteralPath $destination | Should -BeTrue
        Test-Path -LiteralPath $ack | Should -BeTrue
        $evidence = Test-DSGCleanupEvidence -ReadyManifestPath $ready -AckPath $ack
        $evidence.CleanupEligible | Should -BeTrue
        $evidence.ReasonCode | Should -Be 'ELIGIBLE_DRY_RUN'
        $evidence.Deleted | Should -Be 0
    }

    It 'is idempotent for an identical ACK' {
        New-DSGDestinationVerificationAck -ReadyManifestPath $ready -DestinationPath $destination -AckPath $ack | Out-Null
        $second = New-DSGDestinationVerificationAck -ReadyManifestPath $ready -DestinationPath $destination -AckPath $ack
        $second.Status | Should -Be 'ACK_EXISTS_VERIFIED'
    }

    It 'blocks when ACK has not converged' {
        $evidence = Test-DSGCleanupEvidence -ReadyManifestPath $ready -AckPath $ack
        $evidence.CleanupEligible | Should -BeFalse
        $evidence.ReasonCode | Should -Be 'ACK_MISSING'
        $evidence.Deleted | Should -Be 0
    }

    It 'blocks a destination hash mismatch' {
        Add-Content -LiteralPath $destination -Value 'tampered'
        { New-DSGDestinationVerificationAck -ReadyManifestPath $ready -DestinationPath $destination -AckPath $ack } | Should -Throw '*does not match READY manifest*'
        Test-Path -LiteralPath $ack | Should -BeFalse
    }

    It 'blocks if READY changes after ACK creation' {
        New-DSGDestinationVerificationAck -ReadyManifestPath $ready -DestinationPath $destination -AckPath $ack | Out-Null
        $manifest = Get-Content -LiteralPath $ready -Raw | ConvertFrom-Json
        $manifest.CreatedAtUtc = (Get-Date).AddMinutes(1).ToUniversalTime().ToString('o')
        $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ready -Encoding UTF8
        $evidence = Test-DSGCleanupEvidence -ReadyManifestPath $ready -AckPath $ack
        $evidence.CleanupEligible | Should -BeFalse
        $evidence.ReasonCode | Should -Be 'ACK_READY_HASH_MISMATCH'
        $evidence.Deleted | Should -Be 0
    }

    It 'blocks an ACK whose scientific hash conflicts with READY' {
        New-DSGDestinationVerificationAck -ReadyManifestPath $ready -DestinationPath $destination -AckPath $ack | Out-Null
        $ackObject = Get-Content -LiteralPath $ack -Raw | ConvertFrom-Json
        $ackObject.DestinationSha256 = ('0' * 64)
        $ackObject | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $ack -Encoding UTF8
        $evidence = Test-DSGCleanupEvidence -ReadyManifestPath $ready -AckPath $ack
        $evidence.CleanupEligible | Should -BeFalse
        $evidence.ReasonCode | Should -Be 'DESTINATION_HASH_MISMATCH'
        $evidence.Deleted | Should -Be 0
    }
}
