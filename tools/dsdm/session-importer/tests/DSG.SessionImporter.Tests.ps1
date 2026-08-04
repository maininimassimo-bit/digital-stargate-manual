$modulePath = Join-Path $PSScriptRoot '..\DSG.SessionImporter.psm1'
Import-Module $modulePath -Force

Describe 'ConvertFrom-DSGNinaFileName' {
    BeforeAll {
        $knownTelescopes = @(
            'Skywatcher quattro 200p',
            'OptiCo 60mm f-15',
            'Celestron C8 XLT'
        )
    }

    It 'parses the observed LDN 1320 filename correctly' {
        $fileName = 'LIGHT_1x1_600.00s_910_99_LDN 1320_Skywatcher quattro 200p__-10.00C_LPRO_0163_2026-07-17_04-16-06_FWHM_5.77_Fok_116189.xisf'

        $result = ConvertFrom-DSGNinaFileName `
            -FileName $fileName `
            -KnownTelescopes $knownTelescopes

        $result.ParseStatus | Should -Be 'PARSED'
        $result.ImageType | Should -Be 'LIGHT'
        $result.BinningX | Should -Be 1
        $result.BinningY | Should -Be 1
        $result.ExposureSeconds | Should -Be 600.0
        $result.Gain | Should -Be 910.0
        $result.Offset | Should -Be 99.0
        $result.Target | Should -Be 'LDN 1320'
        $result.Telescope | Should -Be 'Skywatcher quattro 200p'
        [double]$result.SensorTemperatureC | Should -Be ([double]-10.0)
        $result.Filter | Should -Be 'LPRO'
        $result.FrameNumber | Should -Be 163
        $result.DateTimeObserved | Should -Be '2026-07-17_04-16-06'
        $result.FwhmObserved | Should -Be 5.77
        $result.FocusPosition | Should -Be 116189
        $result.Extension | Should -Be '.xisf'
        $result.Errors.Count | Should -Be 0
    }

    It 'parses a decimal exposure and a telescope containing spaces and a dash' {
        $fileName = 'LIGHT_1x1_10.21s_1600_10_M33_OptiCo 60mm f-15__-15C_L_0001_2016-01-01_12-00-00_FWHM_4.23_Fok_12542.xisf'

        $result = ConvertFrom-DSGNinaFileName `
            -FileName $fileName `
            -KnownTelescopes $knownTelescopes

        $result.ParseStatus | Should -Be 'PARSED'
        $result.Target | Should -Be 'M33'
        $result.Telescope | Should -Be 'OptiCo 60mm f-15'
        $result.ExposureSeconds | Should -Be 10.21
        [double]$result.SensorTemperatureC | Should -Be ([double]-15.0)
        $result.Filter | Should -Be 'L'
        $result.FrameNumber | Should -Be 1
        $result.FwhmObserved | Should -Be 4.23
        $result.FocusPosition | Should -Be 12542
    }

    It 'parses DARK frames with no filter-specific semantics' {
        $fileName = 'DARK_2x2_300.00s_910_99_Dark Library_Celestron C8 XLT__-10.00C_NONE_0042_2026-08-01_07-10-00_FWHM_0.00_Fok_0.xisf'

        $result = ConvertFrom-DSGNinaFileName `
            -FileName $fileName `
            -KnownTelescopes $knownTelescopes

        $result.ParseStatus | Should -Be 'PARSED'
        $result.ImageType | Should -Be 'DARK'
        $result.BinningX | Should -Be 2
        $result.BinningY | Should -Be 2
        $result.Target | Should -Be 'Dark Library'
        $result.Telescope | Should -Be 'Celestron C8 XLT'
        $result.Filter | Should -Be 'NONE'
        $result.FwhmObserved | Should -Be 0.0
        $result.FocusPosition | Should -Be 0
    }

    It 'returns AMBIGUOUS when no telescope alias is available' {
        $fileName = 'LIGHT_1x1_600.00s_910_99_LDN 1320_Skywatcher quattro 200p__-10.00C_LPRO_0163_2026-07-17_04-16-06_FWHM_5.77_Fok_116189.xisf'

        $result = ConvertFrom-DSGNinaFileName -FileName $fileName

        $result.ParseStatus | Should -Be 'AMBIGUOUS'
        $result.Target | Should -BeNullOrEmpty
        $result.Telescope | Should -BeNullOrEmpty
        $result.Errors.Count | Should -Be 1
    }

    It 'uses the longest matching telescope alias' {
        $fileName = 'LIGHT_1x1_60.00s_100_10_M31_Skywatcher quattro 200p__-5.00C_L_0001_2026-08-01_01-00-00_FWHM_2.10_Fok_1000.xisf'
        $aliases = @(
            'quattro 200p',
            'Skywatcher quattro 200p'
        )

        $result = ConvertFrom-DSGNinaFileName `
            -FileName $fileName `
            -KnownTelescopes $aliases

        $result.ParseStatus | Should -Be 'PARSED'
        $result.Target | Should -Be 'M31'
        $result.Telescope | Should -Be 'Skywatcher quattro 200p'
    }

    It 'returns FAILED when the focus marker is missing' {
        $fileName = 'LIGHT_1x1_600.00s_910_99_M31_Celestron C8 XLT__-10.00C_L_0001_2026-08-01_01-00-00_FWHM_2.10.xisf'

        $result = ConvertFrom-DSGNinaFileName `
            -FileName $fileName `
            -KnownTelescopes $knownTelescopes

        $result.ParseStatus | Should -Be 'FAILED'
        $result.Errors[0] | Should -Match '_Fok_'
    }

    It 'returns FAILED when the temperature segment does not use the double underscore' {
        $fileName = 'LIGHT_1x1_600.00s_910_99_M31_Celestron C8 XLT_-10.00C_L_0001_2026-08-01_01-00-00_FWHM_2.10_Fok_1000.xisf'

        $result = ConvertFrom-DSGNinaFileName `
            -FileName $fileName `
            -KnownTelescopes $knownTelescopes

        $result.ParseStatus | Should -Be 'FAILED'
        $result.Errors[0] | Should -Match 'temperature'
    }

    It 'returns FAILED for a malformed exposure value' {
        $fileName = 'LIGHT_1x1_BADs_910_99_M31_Celestron C8 XLT__-10.00C_L_0001_2026-08-01_01-00-00_FWHM_2.10_Fok_1000.xisf'

        $result = ConvertFrom-DSGNinaFileName `
            -FileName $fileName `
            -KnownTelescopes $knownTelescopes

        $result.ParseStatus | Should -Be 'FAILED'
        $result.Errors.Count | Should -BeGreaterThan 0
    }

    It 'accepts pipeline input' {
        $fileName = 'LIGHT_1x1_60.00s_100_10_M31_Celestron C8 XLT__-5.00C_L_0001_2026-08-01_01-00-00_FWHM_2.10_Fok_1000.xisf'

        $result = $fileName | ConvertFrom-DSGNinaFileName -KnownTelescopes $knownTelescopes

        $result.ParseStatus | Should -Be 'PARSED'
        $result.Target | Should -Be 'M31'
    }
}
