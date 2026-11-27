param([string]$b = $PSScriptRoot, [switch]$VerifyOnly)
$ErrorActionPreference = 'Stop'
$files=[ordered]@{ intera='fotometria-CALSPEC-v2.json'; frazionaria='sensibilita-apertura-frazionaria-v1.json' }
$data=@{}
$pins=[ordered]@{}
foreach($kind in $files.Keys){
    $p=Join-Path $b $files[$kind]
    $pins[$files[$kind]]=(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()
    $data[$kind]=Get-Content -LiteralPath $p -Raw | ConvertFrom-Json
}
if ($pins[$files.intera] -cne '8a6394cdc9d700f66ba3e44b86390b451b2b343b36f162e65db78e1ec9781d6c' -or $pins[$files.frazionaria] -cne '9d2910cdfc91af3fc912e34410df7b874e36895ed7794a76321c314f073880d8') { throw 'Fonti difformi.' }
$groups=@($data.intera.rows | Where-Object visit -in 'j8jq03','j8jq06' | Group-Object visit,band)
if ($groups.Count -ne 6) { throw 'Visite incomplete.' }
$fractional=@{}
foreach($row in $data.frazionaria.rows) { $fractional.Add($row.obs,$row) }
$rows=foreach($r in '3','5'){
    foreach($g in $groups){
        $x=@($g.Group | Sort-Object obs)
        if ($x.Count -ne 2) { throw 'Coppia incompleta.' }
        $y=@($fractional[$x[0].obs],$fractional[$x[1].obs])
        for($i=0;$i -lt 2;$i++){
            if($x[$i].apertures.$r.state -cne 'MEASURED' -or $y[$i].apertures.$r.state -cne 'MEASURED' -or
                 $x[$i].visit -cne $y[$i].visit -or $x[$i].band -cne $y[$i].band -or
                 ($x[$i].referenceSeed -join ',') -cne ($y[$i].referenceSeed -join ',')) { throw 'Confronto non omogeneo.' }
        }
        $a=200*($x[1].apertures.$r.rate-$x[0].apertures.$r.rate)/($x[1].apertures.$r.rate+$x[0].apertures.$r.rate)
        $c=200*($y[1].apertures.$r.rate-$y[0].apertures.$r.rate)/($y[1].apertures.$r.rate+$y[0].apertures.$r.rate)
        [pscustomobject][ordered]@{ raggioPixel=[int]$r; visita=$x[0].visit; filtro=$x[0].band; pose=@($x.obs); deltaInteraPct=$a; deltaFrazionariaPct=$c; absRidotto=([math]::Abs($c) -lt [math]::Abs($a)) }
    }
}
if($rows.Count -ne 12){throw 'Numero confronti inatteso.'}
$stats=foreach($r in 3,5){
    $rr=@($rows | Where-Object raggioPixel -eq $r)
    [pscustomobject]@{
        raggioPixel=$r
        coppieScartoRidotto=@($rr | Where-Object absRidotto).Count
        coppieTotali=$rr.Count
        scartoMedioAssolutoInteraPct=($rr | ForEach-Object {[math]::Abs($_.deltaInteraPct)}|Measure-Object -Average).Average
        scartoMedioAssolutoFrazionariaPct=($rr | ForEach-Object {[math]::Abs($_.deltaFrazionariaPct)}|Measure-Object -Average).Average
        scartoMassimoAssolutoInteraPct=($rr | ForEach-Object {[math]::Abs($_.deltaInteraPct)}|Measure-Object -Maximum).Maximum
        scartoMassimoAssolutoFrazionariaPct=($rr | ForEach-Object {[math]::Abs($_.deltaFrazionariaPct)}|Measure-Object -Maximum).Maximum
    }
}
$report=[ordered]@{schema='bkl046-acs-ripetibilita-intra-visita-v1'; pinSha256=$pins; formula='200 * (seconda - prima) / (seconda + prima)'; ordine='identificatore esposizione'; coppie=$rows; riepilogo=$stats; controlliQualificati=0; chiusureScientifiche=0}
$out=Join-Path $b 'ripetibilita-intra-visita-v1.json'
$enc=[Text.UTF8Encoding]::new($false)
$json=($report | ConvertTo-Json -Depth 8)+"`n"
if (!(Test-Path -LiteralPath $out)) {
    if ($VerifyOnly) { throw 'Riscontro da rileggere assente.' }
    $payload=$enc.GetBytes($json)
    $handle=[IO.File]::Open($out,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $handle.Write($payload,0,$payload.Length) } finally { $handle.Dispose() }
}
if ([IO.File]::ReadAllText($out,$enc) -cne $json) { throw 'Rilettura difforme.' }
Get-FileHash -LiteralPath $out | Select-Object -ExpandProperty Hash
$stats | ConvertTo-Json -Compress
$rows | Format-Table -AutoSize
