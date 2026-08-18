[CmdletBinding()]
param(
    [string]$CloudWatcherCsv = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv',
    [ValidateRange(4096, 1048576)][int]$TailBytes = 262144
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-CsvFieldCount {
    param([Parameter(Mandatory = $true)][string]$Line)
    return ([regex]::Matches($Line, ',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)').Count + 1)
}

function Get-SharedHeaderAndTail {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][int]$Bytes
    )

    $stream = $null
    $reader = $null
    try {
        $stream = [System.IO.File]::Open($Path,[System.IO.FileMode]::Open,[System.IO.FileAccess]::Read,[System.IO.FileShare]::ReadWrite)
        $reader = New-Object System.IO.StreamReader($stream)
        $header = $reader.ReadLine()
        $length = $stream.Length
        $start = [math]::Max(0, $length - $Bytes)
        $stream.Seek($start, [System.IO.SeekOrigin]::Begin) | Out-Null
        if ($start -gt 0) { [void]$reader.ReadLine() }
        $lines = New-Object System.Collections.Generic.List[string]
        while (-not $reader.EndOfStream) {
            $line = $reader.ReadLine()
            if (-not [string]::IsNullOrWhiteSpace($line)) { $lines.Add($line) }
        }
        return [pscustomobject]@{ Header = $header; Lines = @($lines) }
    }
    finally {
        if ($reader) { $reader.Dispose() }
        elseif ($stream) { $stream.Dispose() }
    }
}

if (-not (Test-Path -LiteralPath $CloudWatcherCsv -PathType Leaf)) {
    throw "CloudWatcher CSV non trovato: $CloudWatcherCsv"
}

$tail = Get-SharedHeaderAndTail -Path $CloudWatcherCsv -Bytes $TailBytes
if ([string]::IsNullOrWhiteSpace($tail.Header)) { throw 'Header CloudWatcher assente.' }
$headerCount = Get-CsvFieldCount -Line $tail.Header
$row = $null
$rowLine = $null
for ($i = $tail.Lines.Count - 1; $i -ge 0; $i--) {
    if ((Get-CsvFieldCount -Line $tail.Lines[$i]) -ne $headerCount) { continue }
    try {
        $candidate = @($tail.Header, $tail.Lines[$i]) | ConvertFrom-Csv | Select-Object -First 1
        if ($candidate -and -not [string]::IsNullOrWhiteSpace([string]$candidate.Date) -and -not [string]::IsNullOrWhiteSpace([string]$candidate.Time)) {
            $row = $candidate
            $rowLine = $tail.Lines[$i]
            break
        }
    }
    catch { }
}

if (-not $row) { throw 'Nessuna riga strutturalmente completa trovata nella coda del file.' }

Write-Output 'Digital StarGate CloudWatcher weather field inspector - READ ONLY'
Write-Output ('Source: {0}' -f $CloudWatcherCsv)
Write-Output ('Header fields: {0}' -f $headerCount)
Write-Output ''
Write-Output '=== HEADER ==='
Write-Output $tail.Header
Write-Output ''
Write-Output '=== LATEST COMPLETE ROW ==='
Write-Output $rowLine
Write-Output ''
Write-Output '=== PARSED FIELDS ==='
$row.PSObject.Properties | ForEach-Object {
    Write-Output ('{0} = {1}' -f $_.Name, $_.Value)
}
Write-Output ''
Write-Output 'INSPECT RESULT: PASS'
