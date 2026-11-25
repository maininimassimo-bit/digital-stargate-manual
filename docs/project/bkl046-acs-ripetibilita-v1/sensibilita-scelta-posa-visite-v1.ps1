param([string]$b = $PSScriptRoot, [switch]$VerifyOnly)
$ErrorActionPreference = 'Stop'
$names = [ordered]@{intera='fotometria-CALSPEC-v2.json';frazionaria='sensibilita-apertura-frazionaria-v1.json'}
$expected = @{intera='8a6394cdc9d700f66ba3e44b86390b451b2b343b36f162e65db78e1ec9781d6c';frazionaria='9d2910cdfc91af3fc912e34410df7b874e36895ed7794a76321c314f073880d8'}
$comparisons = foreach ($mode in $names.Keys) {
    $path = Join-Path $b $names[$mode]
    if ((Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() -cne $expected[$mode]) { throw 'Sorgente difforme.' }
    $j = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
    foreach ($radius in '3','5') {
        $rates = @{}
        foreach ($visit in 'j8jq03','j8jq06') {
            foreach ($band in 'F606W','F658N','F660N') {
                $rows = @($j.rows | Where-Object { $_.visit -ceq $visit -and $_.band -ceq $band -and $_.apertures.$radius.state -ceq 'MEASURED' } | Sort-Object obs)
                if ($rows.Count -ne 2 -or @($rows | Where-Object { $_.apertures.$radius.rate -le 0 }).Count) { throw 'Campione non valido.' }
                $rates["$visit/$band"] = @($rows | ForEach-Object { $_.apertures.$radius.rate })
            }
        }
        foreach ($ratio in 'F658N/F606W','F658N/F660N','F660N/F606W') {
            $numerator,$denominator = $ratio.Split('/')
            $samples = @(foreach ($n1 in $rates["j8jq03/$numerator"]) {
                foreach ($d1 in $rates["j8jq03/$denominator"]) {
                    foreach ($n2 in $rates["j8jq06/$numerator"]) {
                        foreach ($d2 in $rates["j8jq06/$denominator"]) {
                            100 * (($n2 / $d2) / ($n1 / $d1) - 1)
                        }
                    }
                }
            })
            if ($samples.Count -ne 16) { throw 'Combinazioni incomplete.' }
            $extrema = $samples | Measure-Object -Minimum -Maximum
            [pscustomobject][ordered]@{
                metodo=$mode
                raggioPixel=[int]$radius
                rapporto=$ratio
                combinazioni=$samples.Count
                minDeltaPct=$extrema.Minimum
                maxDeltaPct=$extrema.Maximum
                positivi=@($samples | Where-Object { $_ -gt 0 }).Count
                negativi=@($samples | Where-Object { $_ -lt 0 }).Count
                deltaPct=$samples
            }
        }
    }
}
if ($comparisons.Count -ne 12) { throw 'Risultato incompleto.' }
$pins = [ordered]@{}
foreach ($mode in $names.Keys) { $pins[$names[$mode]] = $expected[$mode] }
$report = [ordered]@{
    schema='bkl046-acs-scelta-posa-visite-v1'
    pinSha256=$pins
    visite=@('j8jq03','j8jq06')
    ordinamento='ID esposizione crescente, numeratore e denominatore prima visita, poi seconda visita'
    ambito='Inviluppo descrittivo deterministico. Le combinazioni riusano le stesse pose.'
    confronti=$comparisons
    controlliQualificati=0
    chiusureScientifiche=0
}
$out = Join-Path $b 'sensibilita-scelta-posa-visite-v1.json'
$enc = [Text.UTF8Encoding]::new($false)
$payload = $enc.GetBytes(($report | ConvertTo-Json -Depth 8) + "`n")
if (!(Test-Path -LiteralPath $out)) {
    if ($VerifyOnly) { throw 'Riscontro da rileggere assente.' }
    $handle = [IO.File]::Open($out,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $handle.Write($payload,0,$payload.Length) } finally { $handle.Dispose() }
}
if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($out)) -cne [Convert]::ToBase64String($payload)) { throw 'Riscontro difforme.' }
Get-FileHash -LiteralPath $out | Select-Object -ExpandProperty Hash
$comparisons | Format-Table metodo,raggioPixel,rapporto,minDeltaPct,maxDeltaPct,positivi,negativi -AutoSize
