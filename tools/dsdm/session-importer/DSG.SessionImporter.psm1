Set-StrictMode -Version Latest

function ConvertTo-DSGInvariantDecimal {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $number = 0.0
    $style = [System.Globalization.NumberStyles]::Float
    $culture = [System.Globalization.CultureInfo]::InvariantCulture

    if (-not [double]::TryParse($Value, $style, $culture, [ref]$number)) {
        throw "Value '$Value' is not a valid invariant decimal."
    }

    return $number
}

function Resolve-DSGTargetAndTelescope {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$CombinedValue,

        [Parameter(Mandatory = $false)]
        [string[]]$KnownTelescopes = @()
    )

    $matches = @(
        foreach ($telescope in @($KnownTelescopes)) {
            if ([string]::IsNullOrWhiteSpace($telescope)) {
                continue
            }

            if ($CombinedValue.EndsWith($telescope, [System.StringComparison]::OrdinalIgnoreCase)) {
                $targetLength = $CombinedValue.Length - $telescope.Length
                $target = $CombinedValue.Substring(0, $targetLength).TrimEnd('_', ' ')

                if (-not [string]::IsNullOrWhiteSpace($target)) {
                    [pscustomobject]@{
                        Target = $target
                        Telescope = $telescope
                        MatchLength = $telescope.Length
                    }
                }
            }
        }
    )

    if ($matches.Count -eq 0) {
        return [pscustomobject]@{
            Status = 'AMBIGUOUS'
            Target = $null
            Telescope = $null
            Message = 'No configured telescope alias matched the central filename segment.'
        }
    }

    $bestLength = 0
    foreach ($match in $matches) {
        if ($match.MatchLength -gt $bestLength) {
            $bestLength = $match.MatchLength
        }
    }

    $best = @($matches | Where-Object { $_.MatchLength -eq $bestLength })
    if ($best.Count -ne 1) {
        return [pscustomobject]@{
            Status = 'AMBIGUOUS'
            Target = $null
            Telescope = $null
            Message = 'More than one telescope alias matched with the same precedence.'
        }
    }

    return [pscustomobject]@{
        Status = 'PARSED'
        Target = $best[0].Target
        Telescope = $best[0].Telescope
        Message = $null
    }
}

function ConvertFrom-DSGNinaFileName {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$FileName,

        [Parameter(Mandatory = $false)]
        [string[]]$KnownTelescopes = @()
    )

    process {
        $originalFileName = [System.IO.Path]::GetFileName($FileName)
        $extension = [System.IO.Path]::GetExtension($originalFileName)
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($originalFileName)
        $errors = New-Object 'System.Collections.Generic.List[string]'
        $warnings = New-Object 'System.Collections.Generic.List[string]'

        $result = [ordered]@{
            ParserVersion = '0.2.1'
            OriginalFileName = $originalFileName
            Extension = $extension
            ParseStatus = 'FAILED'
            ImageType = $null
            BinningX = $null
            BinningY = $null
            ExposureSeconds = $null
            Gain = $null
            Offset = $null
            Target = $null
            Telescope = $null
            SensorTemperatureC = $null
            Filter = $null
            FrameNumber = $null
            DateTimeObserved = $null
            FwhmObserved = $null
            FocusPosition = $null
            Errors = @()
            Warnings = @()
        }

        try {
            $focusMatch = [regex]::Match($baseName, '^(?<prefix>.+)_Fok_(?<focus>-?\d*)$')
            if (-not $focusMatch.Success) {
                throw 'Missing or invalid _Fok_ segment.'
            }
            $focusValue = $focusMatch.Groups['focus'].Value
            if (-not [string]::IsNullOrWhiteSpace($focusValue)) {
                $result.FocusPosition = [int64]$focusValue
            }

            $beforeFocus = $focusMatch.Groups['prefix'].Value
            $fwhmMatch = [regex]::Match($beforeFocus, '^(?<prefix>.+)_FWHM_(?<fwhm>(?:-?\d+(?:\.\d+)?|NaN))$', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
            if (-not $fwhmMatch.Success) {
                throw 'Missing or invalid _FWHM_ segment.'
            }

            $fwhmValue = $fwhmMatch.Groups['fwhm'].Value
            if ($fwhmValue -ieq 'NaN') {
                $result.FwhmObserved = $null
                $warnings.Add('FWHM is unavailable in the NINA filename (NaN).')
            }
            else {
                $result.FwhmObserved = ConvertTo-DSGInvariantDecimal -Value $fwhmValue
            }
            $prefix = $fwhmMatch.Groups['prefix'].Value

            $suffixPattern = '^(?<head>.+)_(?<filter>[^_]*)_(?<frame>\d+)_(?<date>\d{4}-\d{2}-\d{2})_(?<time>\d{2}-\d{2}-\d{2})$'
            $suffixMatch = [regex]::Match($prefix, $suffixPattern)
            if (-not $suffixMatch.Success) {
                throw 'Unable to parse filter, frame number, date and time suffix.'
            }
            $filterValue = $suffixMatch.Groups['filter'].Value
            if ([string]::IsNullOrWhiteSpace($filterValue)) {
                $result.Filter = 'UNKNOWN'
            }
            else {
                $result.Filter = $filterValue
            }

            $result.FrameNumber = [int]$suffixMatch.Groups['frame'].Value
            $result.DateTimeObserved = ('{0}_{1}' -f $suffixMatch.Groups['date'].Value, $suffixMatch.Groups['time'].Value)

            $head = $suffixMatch.Groups['head'].Value
            $temperatureMatch = [regex]::Match($head, '^(?<prefix>.+)__(?<temperature>-?\d+(?:\.\d+)?)C$')
            if (-not $temperatureMatch.Success) {
                throw 'Unable to parse the double-underscore sensor temperature segment.'
            }

            $result.SensorTemperatureC = ConvertTo-DSGInvariantDecimal -Value $temperatureMatch.Groups['temperature'].Value
            $leftAndCenter = $temperatureMatch.Groups['prefix'].Value

            $leftPattern = '^(?<imageType>[A-Za-z]+)_(?<binX>\d+)x(?<binY>\d+)_(?<exposure>\d+(?:\.\d+)?)s_(?<gain>-?\d+(?:\.\d+)?)_(?<offset>-?\d+(?:\.\d+)?)_(?<center>.+)$'
            $leftMatch = [regex]::Match($leftAndCenter, $leftPattern)
            if (-not $leftMatch.Success) {
                throw 'Unable to parse the fixed leading NINA fields.'
            }

            $result.ImageType = $leftMatch.Groups['imageType'].Value.ToUpperInvariant()
            $result.BinningX = [int]$leftMatch.Groups['binX'].Value
            $result.BinningY = [int]$leftMatch.Groups['binY'].Value
            $result.ExposureSeconds = ConvertTo-DSGInvariantDecimal -Value $leftMatch.Groups['exposure'].Value
            $result.Gain = ConvertTo-DSGInvariantDecimal -Value $leftMatch.Groups['gain'].Value
            $result.Offset = ConvertTo-DSGInvariantDecimal -Value $leftMatch.Groups['offset'].Value

            $resolution = Resolve-DSGTargetAndTelescope -CombinedValue $leftMatch.Groups['center'].Value -KnownTelescopes $KnownTelescopes
            $result.Target = $resolution.Target
            $result.Telescope = $resolution.Telescope

            if ($resolution.Status -eq 'PARSED') {
                $result.ParseStatus = 'PARSED'
            }
            else {
                $result.ParseStatus = 'AMBIGUOUS'
                $errors.Add($resolution.Message)
            }
        }
        catch {
            $errors.Add($_.Exception.Message)
            $result.ParseStatus = 'FAILED'
        }

        $result.Errors = @($errors)
        $result.Warnings = @($warnings)
        [pscustomobject]$result
    }
}

Export-ModuleMember -Function ConvertFrom-DSGNinaFileName
