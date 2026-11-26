param([switch]$Preview)
$ErrorActionPreference = 'Stop'
$env:GIT_TERMINAL_PROMPT = '0'
$root = 'C:\DigitalStarGate\AllSkyNightWeather'
$source = 'C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv'
$repo = 'https://github.com/maininimassimo-bit/digital-stargate-manual.git'
$now = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::UtcNow, 'W. Europe Standard Time')
$end = $now.Date.AddHours(6)
if ($now -lt $end) { $end = $end.AddDays(-1) }
$start = $end.Date.AddDays(-1).AddHours(19)
$key = $start.ToString('yyyyMMdd')
$culture = [Globalization.CultureInfo]::InvariantCulture
$seconds = [ordered]@{Clear=0; Cloudy=0; Overcast=0}
$temps = [Collections.Generic.List[double]]::new()
$humidity = [Collections.Generic.List[double]]::new()
$wind = [Collections.Generic.List[double]]::new()
$first = $last = $previous = $null
$partial = $false
$header = Get-Content -LiteralPath $source -TotalCount 1
$lines = @($header) + @(Get-Content -LiteralPath $source -Tail 25000)
foreach ($row in ($lines | ConvertFrom-Csv)) {
    $stamp = [datetime]::MinValue
    if (![datetime]::TryParseExact("$($row.Date) $($row.Time)", 'yyyy-MM-dd HH:mm:ss', $culture, [Globalization.DateTimeStyles]::None, [ref]$stamp)) { continue }
    if ($stamp -lt $start -or $stamp -ge $end) { continue }
    $temp = $hum = $speed = 0.0
    $style = [Globalization.NumberStyles]::Float
    if (![double]::TryParse($row.'Ambient Temperature', $style, $culture, [ref]$temp) -or
        ![double]::TryParse($row.'Relative Humidity', $style, $culture, [ref]$hum) -or
        ![double]::TryParse($row.'Wind Value', $style, $culture, [ref]$speed)) { $partial = $true; continue }
    $temps.Add($temp); $humidity.Add($hum); $wind.Add($speed)
    $condition = $row.'Cloud Condition'
    if ($condition -notin @('Clear','Cloudy','Overcast')) { $partial = $true; continue }
    if (!$first) { $first = $stamp }
    if ($last) {
        $gap = ($stamp - $last).TotalSeconds
        if ($gap -ge 60) { $partial = $true }
        elseif ($gap -gt 0) { $seconds[$previous] += [int]$gap }
        else { continue }
    }
    $last = $stamp
    $previous = $condition
}
if (!$first -or (($seconds.Values | Measure-Object -Sum).Sum -le 0)) { throw "Nessun intervallo CloudWatcher valido per $key" }
$partial = $partial -or ($first - $start).TotalSeconds -ge 60 -or ($end - $last).TotalSeconds -ge 60
$summary = [ordered]@{
    start = $first.ToString('HH:mm'); end = $last.ToString('HH:mm'); partial = [bool]$partial
    seconds = $seconds
    min = ($temps | Measure-Object -Minimum).Minimum; max = ($temps | Measure-Object -Maximum).Maximum
    humidity = [math]::Round(($humidity | Measure-Object -Average).Average)
    wind = [math]::Round(($wind | Measure-Object -Average).Average, 1)
}
$json = $summary | ConvertTo-Json -Depth 3 -Compress
if ($Preview) { "$key $json"; return }
function Git-Checked {
    & git @args
    if ($LASTEXITCODE) { throw "Git failed: $($args[0])" }
}
$checkout = Join-Path $root 'publisher'
if (!(Test-Path "$checkout/.git")) {
    Git-Checked clone --depth 1 --filter=blob:none --sparse --branch main $repo $checkout
    Git-Checked -C $checkout sparse-checkout set data/allsky-night-weather
}
if ((Git-Checked -C $checkout remote get-url origin) -ne $repo) { throw 'Remote inatteso' }
if (Git-Checked -C $checkout status --porcelain) { throw 'Checkout con modifiche locali' }
Git-Checked -C $checkout pull --ff-only origin main
$folder = Join-Path $checkout 'data/allsky-night-weather'
New-Item -ItemType Directory -Force $folder | Out-Null
$file = Join-Path $folder "$key.json"
if ((Test-Path $file) -and ([IO.File]::ReadAllText($file) -eq $json)) { "Riepilogo $key gia pubblicato"; return }
[IO.File]::WriteAllText($file, $json, [Text.UTF8Encoding]::new($false))
Git-Checked -C $checkout add -- "data/allsky-night-weather/$key.json"
Git-Checked -C $checkout -c user.name='Digital StarGate Weather' -c user.email='maininimassimo-bit@users.noreply.github.com' commit -m "Publish AllSky nightly weather $key"
Git-Checked -C $checkout push origin HEAD:main
"Riepilogo $key inviato"
