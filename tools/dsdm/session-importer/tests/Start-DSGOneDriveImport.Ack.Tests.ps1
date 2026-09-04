Describe 'Start-DSGOneDriveImport AP-013C ACK integration' {
    BeforeEach {
        $root = Join-Path $TestDrive ([guid]::NewGuid().ToString('N'))
        $transportRoot = Join-Path $root 'transport'
        $destinationRoot = Join-Path $root 'destination'
        $evidenceRoot = Join-Path $root 'evidence'
        New-Item -ItemType Directory -Path $transportRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null

        $transportFile = Join-Path $transportRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($transportFile, 'synthetic-scientific-content')
        $hash = (Get-FileHash -LiteralPath $transportFile -Algorithm SHA256).Hash.ToLowerInvariant()
        $readyPath = $transportFile + '.ready.json'
        [pscustomobject][ordered]@{
            SchemaVersion = '1.0'; State = 'READY'; FileName = 'sample.xisf'
            SizeBytes = (Get-Item -LiteralPath $transportFile).Length; Sha256 = $hash
            SourceHost = 'TEST-EAGLE'; SourcePath = 'D:\Images NINA\Target\sample.xisf'
            Transport = 'OneDrive'; CreatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
        } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $readyPath -Encoding UTF8

        $destinationPath = Join-Path $destinationRoot 'sample.xisf'
        $planPath = Join-Path $root 'transfer-plan.csv'
        [pscustomobject]@{
            FileName = 'sample.xisf'
            SourceRelativePath = 'sample.xisf'
            PlannedAction = 'COPY_NEW'
            PlannedDestination = $destinationPath
        } | Export-Csv -LiteralPath $planPath -NoTypeInformation -Encoding UTF8

        $scriptPath = Join-Path $PSScriptRoot '..\Start-DSGOneDriveImport.ps1'
    }

    It 'creates ACK after COPIED_VERIFIED and preserves transport' {
        & $scriptPath -TransferPlanPath $planPath -TransportRoot $transportRoot -DestinationRoot $destinationRoot -EvidenceRoot $evidenceRoot -MaxFilesPerRun 10 | Out-Null

        Test-Path -LiteralPath $destinationPath | Should -BeTrue
        Test-Path -LiteralPath $transportFile | Should -BeTrue
        Test-Path -LiteralPath ($transportFile + '.imported.json') | Should -BeTrue

        $summaryPath = Get-ChildItem -LiteralPath $evidenceRoot -Filter 'import-manifest.json' -File -Recurse | Select-Object -First 1 -ExpandProperty FullName
        $summary = Get-Content -LiteralPath $summaryPath -Raw | ConvertFrom-Json
        $summary.SchemaVersion | Should -Be '1.2'
        $summary.CopiedVerified | Should -Be 1
        $summary.AckCreated | Should -Be 1
        $summary.AckFailed | Should -Be 0
        $summary.SourceFilesDeleted | Should -Be 0
        $summary.TransportFilesDeleted | Should -Be 0
    }

    It 'creates ACK for an already imported identical destination without rewriting it' {
        Copy-Item -LiteralPath $transportFile -Destination $destinationPath
        $before = (Get-Item -LiteralPath $destinationPath).LastWriteTimeUtc
        Start-Sleep -Milliseconds 50

        & $scriptPath -TransferPlanPath $planPath -TransportRoot $transportRoot -DestinationRoot $destinationRoot -EvidenceRoot $evidenceRoot -MaxFilesPerRun 10 | Out-Null

        (Get-Item -LiteralPath $destinationPath).LastWriteTimeUtc | Should -Be $before
        Test-Path -LiteralPath ($transportFile + '.imported.json') | Should -BeTrue
        $summaryPath = Get-ChildItem -LiteralPath $evidenceRoot -Filter 'import-manifest.json' -File -Recurse | Select-Object -First 1 -ExpandProperty FullName
        $summary = Get-Content -LiteralPath $summaryPath -Raw | ConvertFrom-Json
        $summary.AlreadyImportedSkipped | Should -Be 1
        $summary.AckCreated | Should -Be 1
        $summary.TransportFilesDeleted | Should -Be 0
    }

    It 'does not create ACK when destination conflicts' {
        [System.IO.File]::WriteAllText($destinationPath, 'conflicting-data')

        & $scriptPath -TransferPlanPath $planPath -TransportRoot $transportRoot -DestinationRoot $destinationRoot -EvidenceRoot $evidenceRoot -MaxFilesPerRun 10 | Out-Null

        Test-Path -LiteralPath ($transportFile + '.imported.json') | Should -BeFalse
        Test-Path -LiteralPath $transportFile | Should -BeTrue
    }
}
