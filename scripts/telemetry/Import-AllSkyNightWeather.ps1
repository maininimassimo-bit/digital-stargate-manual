$ErrorActionPreference='Stop'
$env:GIT_TERMINAL_PROMPT='0'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
$base='https://digitalstargate.freeddns.it:23232/allsky'
$published='https://maininimassimo-bit.github.io/digital-stargate-manual/data/realtime/allsky-night-weather.json'
$dates=@{}
foreach($category in 'videos','startrails','keograms'){
  $html=(Invoke-WebRequest "$base/$category/" -UseBasicParsing -TimeoutSec 20).Content
  $matches=[regex]::Matches($html,'href=[''"]\./[\w-]+-(20\d{6})\.(?:mp4|jpe?g)[''"]')
  if(!$matches.Count){throw "Catalogo vuoto: $category"}
  foreach($m in $matches){$dates[$m.Groups[1].Value]=$true}
}
$existing=(Invoke-RestMethod $published -TimeoutSec 20).nights
foreach($property in $existing.PSObject.Properties){$dates.Remove($property.Name)}
$root='C:\DigitalStarGate\AllSkyNightWeather'
$checkout=Join-Path $root 'publisher'
$repo='https://github.com/maininimassimo-bit/digital-stargate-manual.git'
function Git-Checked { & git @args; if($LASTEXITCODE){throw "Git failed: $($args[0])"} }
if ((Git-Checked -C $checkout remote get-url origin) -ne $repo){throw 'Remote inatteso'}
if (Git-Checked -C $checkout status --porcelain){throw 'Checkout con modifiche locali'}
Git-Checked -C $checkout pull --ff-only origin main
$folder=Join-Path $checkout 'data/allsky-night-weather'
$source='C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv'
$inv=[Globalization.CultureInfo]::InvariantCulture
$begin=(Get-Date).Date.AddHours(6)
if((Get-Date) -lt $begin){$begin=$begin.AddDays(-1)}
$latest=$begin.Date.AddDays(-1).ToString('yyyyMMdd')
$nightKeys=@{}
$dayKeys=@{}
foreach($k in $dates.Keys){
  if([string]::CompareOrdinal($k,$latest) -gt 0 -or (Test-Path "$folder/$k.json")){continue}
  $dt=[datetime]::ParseExact($k,'yyyyMMdd',$inv)
  $nightKeys[$dt.ToString('yyyy-MM-dd')]=$k
  $dayKeys[$dt.AddDays(1).ToString('yyyy-MM-dd')]=$k
}
$all=@{}
$stream=[IO.File]::Open($source,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
$reader=[IO.StreamReader]::new($stream)
try {
  $header=$reader.ReadLine()
  $pattern=[regex]::new('^"(\d{4}-\d{2}-\d{2})","(\d{2}:\d{2}:\d{2})",')
  while($null -ne ($line=$reader.ReadLine())){
    $m=$pattern.Match($line)
    if(!$m.Success){continue}
    $date=$m.Groups[1].Value;$hour=[int]$m.Groups[2].Value.Substring(0,2)
    $k=$null
    if($hour -ge 19){$k=$nightKeys[$date]}elseif($hour -lt 6){$k=$dayKeys[$date]}
    if($k){
      if(!$all.ContainsKey($k)){$all[$k]=[Collections.Generic.List[string]]::new()}
      $all[$k].Add($line)
    }
  }
} finally {$reader.Dispose()}
$count=0;$partialCount=0
foreach($k in ($all.Keys | Sort-Object)){
  $rows=@((@($header)+$all[$k].ToArray())|ConvertFrom-Csv|Sort-Object Date,Time)
  $seconds=[ordered]@{Clear=0;Cloudy=0;Overcast=0}
  $first=$last=$prev=$null
  $partial=$false
  $temps=[Collections.Generic.List[double]]::new()
  $hum=[Collections.Generic.List[double]]::new()
  $wind=[Collections.Generic.List[double]]::new()
  foreach($row in $rows){
    $x=$y=$z=0.0
    $style=[Globalization.NumberStyles]::Float
    if(![double]::TryParse($row.'Ambient Temperature',$style,$inv,[ref]$x) -or ![double]::TryParse($row.'Relative Humidity',$style,$inv,[ref]$y) -or ![double]::TryParse($row.'Wind Value',$style,$inv,[ref]$z)){ $partial=$true;continue }
    $state=$row.'Cloud Condition'
    if($state -notin 'Clear','Cloudy','Overcast'){$partial=$true;continue}
    $stamp=[datetime]::ParseExact("$($row.Date) $($row.Time)",'yyyy-MM-dd HH:mm:ss',$inv)
    if($last){$gap=($stamp-$last).TotalSeconds;if($gap -le 0){continue};if($gap -lt 60){$seconds[$prev]+=[int]$gap}else{$partial=$true}}
    if(!$first){$first=$stamp};$last=$stamp;$prev=$state
    $temps.Add($x);$hum.Add($y);$wind.Add($z)
  }
  if((($seconds.Values|Measure-Object -Sum).Sum) -le 0){continue}
  $start=[datetime]::ParseExact($k,'yyyyMMdd',$inv).AddHours(19)
  $end=$start.Date.AddDays(1).AddHours(6)
  $partial=$partial -or ($first-$start).TotalSeconds -ge 60 -or ($end-$last).TotalSeconds -ge 60
  if($partial){$partialCount++}
  $summary=[ordered]@{start=$first.ToString('HH:mm');end=$last.ToString('HH:mm');partial=[bool]$partial;seconds=$seconds;min=($temps|Measure-Object -Minimum).Minimum;max=($temps|Measure-Object -Maximum).Maximum;humidity=[math]::Round(($hum|Measure-Object -Average).Average);wind=[math]::Round(($wind|Measure-Object -Average).Average,1)}
  [IO.File]::WriteAllText("$folder/$k.json",($summary|ConvertTo-Json -Depth 3 -Compress),[Text.UTF8Encoding]::new($false))
  $count++
}
"Nuovi riepiloghi: $count. Parziali: $partialCount."
if($count){
  Git-Checked -C $checkout add -- data/allsky-night-weather
  Git-Checked -C $checkout -c user.name='Digital StarGate Weather' -c user.email='maininimassimo-bit@users.noreply.github.com' commit -m 'Import archived AllSky nightly weather'
  Git-Checked -C $checkout push origin HEAD:main
}
