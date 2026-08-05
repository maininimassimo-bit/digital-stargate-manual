BeforeAll {
    $script:modulePath = Join-Path $PSScriptRoot '..\DSG.SessionTransfer.psm1'
    $script:orchestratorPath = Join-Path $PSScriptRoot '..\Invoke-DSGSessionTransfer.ps1'

    Import-Module $script:modulePath -Force
}

Describe 'DSG.SessionTransfer primitives' {
    BeforeEach {
        $testRoot = Join-Path $TestDrive 'transfer'
        $sourceRoot = Join-Path $testRoot 'source'
        $destinationRoot = Join-Path $testRoot 'destination'

        New-Item -ItemType Directory -Path $sourceRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null

        $sourceFile = Join-Path $sourceRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($sourceFile, 'synthetic-scientific-content')
    }

    It 'accepts a destination path under the authorized root' {
        $candidate = Join-Path $destinationRoot 'Target\Light\sample.xisf'
        Test-DSGPathUnderRoot -RootPath $destinationRoot -CandidatePath $candidate | Should -BeTrue
    }

    It 'rejects a destination path outside the authorized root' {
        $candidate = Join-Path $testRoot 'outside\sample.xisf'
        Test-DSGPathUnderRoot -RootPath $destinationRoot -CandidatePath $candidate | Should -BeFalse
    }

    It 'classifies an absent destination as NEW' {
        $destinationFile = Join-Path $destinationRoot 'sample.xisf'
        $result = Get-DSGCollisionState -SourcePath $sourceFile -DestinationPath $destinationFile

        $result.State | Should -Be 'NEW'
        $result.SourceSize | Should -BeGreaterThan 0
        $result.DestinationSize | Should -BeNullOrEmpty
    }

    It 'classifies an identical destination as IDENTICAL' {
        $destinationFile = Join-Path $destinationRoot 'sample.xisf'
        Copy-Item -LiteralPath $sourceFile -Destination $destinationFile

        $result = Get-DSGCollisionState -SourcePath $sourceFile -DestinationPath $destinationFile

        $result.State | Should -Be 'IDENTICAL'
        $result.SourceSha256 | Should -Be $result.DestinationSha256
    }

    It 'classifies a different destination as CONFLICT' {
        $destinationFile = Join-Path $destinationRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($destinationFile, 'different-content')

        $result = Get-DSGCollisionState -SourcePath $sourceFile -DestinationPath $destinationFile

        $result.State | Should -Be 'CONFLICT'
    }

    It 'recognizes equal observations as stable' {
        $first = New-DSGFileObservation -LiteralPath $sourceFile
        $second = New-DSGFileObservation -LiteralPath $sourceFile

        Test-DSGStableObservation -FirstObservation $first -SecondObservation $second | Should -BeTrue
    }

    It 'recognizes changed observations as unstable' {
        $first = New-DSGFileObservation -LiteralPath $sourceFile
        Add-Content -LiteralPath $sourceFile -Value 'changed'
        $second = New-DSGFileObservation -LiteralPath $sourceFile

        Test-DSGStableObservation -FirstObservation $first -SecondObservation $second | Should -BeFalse
    }

    It 'copies through staging, verifies SHA-256 and preserves the source' {
        $destinationFile = Join-Path $destinationRoot 'Target\Light\sample.xisf'

        $result = Invoke-DSGCopyOnlyFile `
            -SourcePath $sourceFile `
            -DestinationRoot $destinationRoot `
            -DestinationPath $destinationFile

        $result.Status | Should -Be 'COPIED_VERIFIED'
        $result.SourceDeleted | Should -BeFalse
        Test-Path -LiteralPath $sourceFile | Should -BeTrue
        Test-Path -LiteralPath $destinationFile | Should -BeTrue
        Test-Path -LiteralPath ($destinationFile + '.dsg-partial') | Should -BeFalse
        (Get-DSGFileSha256 -LiteralPath $sourceFile) | Should -Be (Get-DSGFileSha256 -LiteralPath $destinationFile)
    }

    It 'skips an identical destination without rewriting it' {
        $destinationFile = Join-Path $destinationRoot 'sample.xisf'
        Copy-Item -LiteralPath $sourceFile -Destination $destinationFile
        $originalWriteTime = (Get-Item -LiteralPath $destinationFile).LastWriteTimeUtc

        Start-Sleep -Milliseconds 50
        $result = Invoke-DSGCopyOnlyFile `
            -SourcePath $sourceFile `
            -DestinationRoot $destinationRoot `
            -DestinationPath $destinationFile

        $result.Status | Should -Be 'SKIP_IDENTICAL'
        (Get-Item -LiteralPath $destinationFile).LastWriteTimeUtc | Should -Be $originalWriteTime
        Test-Path -LiteralPath $sourceFile | Should -BeTrue
    }

    It 'blocks a conflicting destination and never overwrites it' {
        $destinationFile = Join-Path $destinationRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($destinationFile, 'existing-conflict')
        $beforeHash = Get-DSGFileSha256 -LiteralPath $destinationFile

        {
            Invoke-DSGCopyOnlyFile `
                -SourcePath $sourceFile `
                -DestinationRoot $destinationRoot `
                -DestinationPath $destinationFile
        } | Should -Throw '*Destination conflict detected*'

        (Get-DSGFileSha256 -LiteralPath $destinationFile) | Should -Be $beforeHash
        Test-Path -LiteralPath $sourceFile | Should -BeTrue
    }
}

Describe 'Invoke-DSGSessionTransfer synthetic orchestration' {
    It 'produces a WhatIf manifest without copying or deleting files' {
        $root = Join-Path $TestDrive 'orchestration'
        $sourceRoot = Join-Path $root 'source'
        $destinationRoot = Join-Path $root 'destination'
        $evidenceRoot = Join-Path $root 'evidence'

        New-Item -ItemType Directory -Path $sourceRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $evidenceRoot -Force | Out-Null

        $sourceFile = Join-Path $sourceRoot 'LIGHT_1x1_60.00s_100_10_TestTarget_TestScope__-10.0C_L_0001_2026-08-04_07-40-00_FWHM_2.00_Fok_1000.xisf'
        [System.IO.File]::WriteAllText($sourceFile, 'synthetic-transfer-content')

        $destinationFile = Join-Path $destinationRoot 'TestTarget\Light\2026-08-04\sample.xisf'
        $planPath = Join-Path $root 'transfer-plan.csv'
        @(
            [pscustomobject]@{
                SourceFullPath = $sourceFile
                SourceRelativePath = (Split-Path -Leaf $sourceFile)
                PlannedDestination = $destinationFile
                PlannedAction = 'COPY_NEW'
            }
        ) | Export-Csv -LiteralPath $planPath -NoTypeInformation -Encoding UTF8

        $configurationPath = Join-Path $root 'session-transfer.test.json'
        $configuration = [ordered]@{
            schemaVersion = '1.0'
            mode = 'COPY_ONLY'
            source = [ordered]@{
                sourceId = 'TEST-SOURCE'
                host = 'LOCALHOST'
                rootPath = $sourceRoot
            }
            destination = [ordered]@{
                storageVolumeId = 'TEST-DESTINATION'
                rootPath = $destinationRoot
                expectedVolumeLabel = ''
            }
            evidence = [ordered]@{
                outputRoot = $evidenceRoot
            }
            window = [ordered]@{
                notBeforeLocal = '00:00'
                doNotStartAfterLocal = '23:59'
                mustFinishBeforeLocal = '23:59'
            }
            transfer = [ordered]@{
                stabilityObservationDelaySeconds = 0
                maxFilesPerRun = 1
                hashAlgorithm = 'SHA-256'
                stagingExtension = '.dsg-partial'
            }
            safety = [ordered]@{
                sourceCleanupAuthorized = $false
                allowTransferMode = $true
                allowDestinationWrites = $true
                overwriteExisting = $false
            }
        }

        $configuration | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $configurationPath -Encoding UTF8

        & $script:orchestratorPath `
            -ConfigurationPath $configurationPath `
            -TransferPlanPath $planPath `
            -WhatIf | Out-Null

        Test-Path -LiteralPath $sourceFile | Should -BeTrue
        Test-Path -LiteralPath $destinationFile | Should -BeFalse

        $runDirectory = Get-ChildItem -LiteralPath $evidenceRoot -Directory | Select-Object -First 1
        $runDirectory | Should -Not -BeNullOrEmpty

        $manifestPath = Join-Path $runDirectory.FullName 'transfer-manifest.json'
        Test-Path -LiteralPath $manifestPath | Should -BeTrue

        $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
        $manifest.Mode | Should -Be 'COPY_ONLY'
        $manifest.Status | Should -Be 'COMPLETED'
        $manifest.WhatIfCount | Should -Be 1
        $manifest.SourceFilesDeleted | Should -Be 0
        $manifest.Safety.SourceCleanupAuthorized | Should -BeFalse
        $manifest.Safety.OverwriteExisting | Should -BeFalse
    }
}
