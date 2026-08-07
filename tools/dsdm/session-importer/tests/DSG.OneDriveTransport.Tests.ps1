BeforeAll {
    $script:transportModulePath = Join-Path $PSScriptRoot '..\DSG.OneDriveTransport.psm1'
    Import-Module $script:transportModulePath -Force
}

Describe 'DSG.OneDriveTransport export' {
    BeforeEach {
        $root = Join-Path $TestDrive 'export'
        $sourceRoot = Join-Path $root 'source'
        $transportRoot = Join-Path $root 'transport'
        New-Item -ItemType Directory -Path $sourceRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $transportRoot -Force | Out-Null
        $sourceFile = Join-Path $sourceRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($sourceFile, 'synthetic-scientific-content')
    }

    It 'calculates deterministic SHA-256' {
        $first = Get-DSGTransportSha256 -LiteralPath $sourceFile
        $second = Get-DSGTransportSha256 -LiteralPath $sourceFile
        $first | Should -Be $second
    }

    It 'exports through staging, writes READY manifest and preserves source' {
        $result = Export-DSGOneDriveTransportFile `
            -SourcePath $sourceFile `
            -TransportRoot $transportRoot `
            -StabilityDelaySeconds 0

        $result.Status | Should -Be 'READY'
        $result.SourceDeleted | Should -BeFalse
        Test-Path -LiteralPath $sourceFile -PathType Leaf | Should -BeTrue
        Test-Path -LiteralPath $result.TransportPath -PathType Leaf | Should -BeTrue
        Test-Path -LiteralPath ($result.TransportPath + '.dsg-partial') | Should -BeFalse
        Test-Path -LiteralPath $result.ManifestPath -PathType Leaf | Should -BeTrue

        $manifest = Get-Content -LiteralPath $result.ManifestPath -Raw | ConvertFrom-Json
        $manifest.State | Should -Be 'READY'
        $manifest.SizeBytes | Should -Be (Get-Item -LiteralPath $sourceFile).Length
        $manifest.Sha256 | Should -Be (Get-DSGTransportSha256 -LiteralPath $sourceFile)
        (Get-DSGTransportSha256 -LiteralPath $result.TransportPath) | Should -Be $manifest.Sha256
    }

    It 'reuses an identical transport file without changing source' {
        $first = Export-DSGOneDriveTransportFile -SourcePath $sourceFile -TransportRoot $transportRoot -StabilityDelaySeconds 0
        $before = (Get-Item -LiteralPath $first.TransportPath).LastWriteTimeUtc
        Start-Sleep -Milliseconds 50

        $second = Export-DSGOneDriveTransportFile -SourcePath $sourceFile -TransportRoot $transportRoot -StabilityDelaySeconds 0

        $second.Status | Should -Be 'READY'
        (Get-Item -LiteralPath $second.TransportPath).LastWriteTimeUtc | Should -Be $before
        Test-Path -LiteralPath $sourceFile | Should -BeTrue
    }

    It 'blocks a conflicting transport file and never overwrites it' {
        $transportFile = Join-Path $transportRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($transportFile, 'different-content')
        $beforeHash = Get-DSGTransportSha256 -LiteralPath $transportFile

        {
            Export-DSGOneDriveTransportFile -SourcePath $sourceFile -TransportRoot $transportRoot -StabilityDelaySeconds 0
        } | Should -Throw '*Transport conflict*'

        (Get-DSGTransportSha256 -LiteralPath $transportFile) | Should -Be $beforeHash
        Test-Path -LiteralPath $sourceFile | Should -BeTrue
    }
}

Describe 'DSG.OneDriveTransport import' {
    BeforeEach {
        $root = Join-Path $TestDrive 'import'
        $transportRoot = Join-Path $root 'transport'
        $destinationRoot = Join-Path $root 'destination'
        New-Item -ItemType Directory -Path $transportRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null

        $transportFile = Join-Path $transportRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($transportFile, 'synthetic-scientific-content')
        $hash = Get-DSGTransportSha256 -LiteralPath $transportFile
        $manifestPath = $transportFile + '.ready.json'
        [pscustomobject][ordered]@{
            SchemaVersion = '1.0'
            State = 'READY'
            FileName = 'sample.xisf'
            SizeBytes = (Get-Item -LiteralPath $transportFile).Length
            Sha256 = $hash
            SourceHost = 'TEST-EAGLE'
            SourcePath = 'D:\Images NINA\Target\sample.xisf'
            Transport = 'OneDrive'
            CreatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
        } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
    }

    It 'copies a READY transport file through the existing COPY_ONLY engine' {
        $destination = Join-Path $destinationRoot 'Target\Light\2026-08-07\sample.xisf'
        $result = Import-DSGOneDriveTransportFile `
            -ManifestPath $manifestPath `
            -DestinationRoot $destinationRoot `
            -DestinationPath $destination

        $result.Status | Should -Be 'COPIED_VERIFIED'
        $result.SourceDeleted | Should -BeFalse
        $result.TransportDeleted | Should -BeFalse
        $result.OverwritePerformed | Should -BeFalse
        Test-Path -LiteralPath $transportFile | Should -BeTrue
        Test-Path -LiteralPath $destination | Should -BeTrue
        $result.SourceSha256 | Should -Be $result.TransportSha256
        $result.TransportSha256 | Should -Be $result.DestinationSha256
    }

    It 'skips an identical destination without rewriting it' {
        $destination = Join-Path $destinationRoot 'sample.xisf'
        Copy-Item -LiteralPath $transportFile -Destination $destination
        $before = (Get-Item -LiteralPath $destination).LastWriteTimeUtc
        Start-Sleep -Milliseconds 50

        $result = Import-DSGOneDriveTransportFile `
            -ManifestPath $manifestPath `
            -DestinationRoot $destinationRoot `
            -DestinationPath $destination

        $result.Status | Should -Be 'SKIP_IDENTICAL'
        (Get-Item -LiteralPath $destination).LastWriteTimeUtc | Should -Be $before
        Test-Path -LiteralPath $transportFile | Should -BeTrue
    }

    It 'blocks a conflicting destination and preserves both files' {
        $destination = Join-Path $destinationRoot 'sample.xisf'
        [System.IO.File]::WriteAllText($destination, 'conflicting-existing-data')
        $beforeHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash

        {
            Import-DSGOneDriveTransportFile `
                -ManifestPath $manifestPath `
                -DestinationRoot $destinationRoot `
                -DestinationPath $destination
        } | Should -Throw '*Destination conflict detected*'

        (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash | Should -Be $beforeHash
        Test-Path -LiteralPath $transportFile | Should -BeTrue
    }

    It 'rejects a non-READY manifest' {
        $badManifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
        $badManifest.State = 'INCOMPLETE'
        $badManifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

        $destination = Join-Path $destinationRoot 'sample.xisf'
        {
            Import-DSGOneDriveTransportFile `
                -ManifestPath $manifestPath `
                -DestinationRoot $destinationRoot `
                -DestinationPath $destination
        } | Should -Throw '*Manifest state must be READY*'
    }

    It 'rejects a transport file whose hash differs from the manifest' {
        Add-Content -LiteralPath $transportFile -Value 'tampered'
        $destination = Join-Path $destinationRoot 'sample.xisf'

        {
            Import-DSGOneDriveTransportFile `
                -ManifestPath $manifestPath `
                -DestinationRoot $destinationRoot `
                -DestinationPath $destination
        } | Should -Throw '*does not match READY manifest*'

        Test-Path -LiteralPath $destination | Should -BeFalse
    }
}
