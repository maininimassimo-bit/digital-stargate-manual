$ErrorActionPreference='Stop'
$root='C:\DigitalStarGate\AllSkyNightWeather'
$checkout=Join-Path $root 'publisher'
$source='C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv'
function Git-Checked { & git -C $checkout @args; if($LASTEXITCODE){throw "Git failed: $($args[0])"} }
if ((Git-Checked remote get-url origin) -ne 'https://github.com/maininimassimo-bit/digital-stargate-manual.git'){throw 'Remote inatteso'}
if (Git-Checked status --porcelain){throw 'Checkout con modifiche locali'}
Git-Checked pull --ff-only origin main
$folder=Join-Path $checkout 'data/allsky-night-weather'
$files=Get-ChildItem $folder -Filter '*.json'
Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Collections.Generic;
using System.Globalization;
public static class RainBackfill {
    public static Dictionary<string, int> Scan(string source) {
        var days = new Dictionary<string, int>();
        var ranks = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase) {{"Dry",1},{"Wet",2},{"Rain",3}};
        var keys = new Dictionary<string, string[]>();
        var separator = new[]{"\",\""};
        using (var reader = new StreamReader(new FileStream(source, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))) {
            int column = Array.IndexOf(reader.ReadLine().Trim('"').Split(separator,StringSplitOptions.None), "Rain Condition");
            if (column < 2) throw new InvalidDataException("Rain Condition column missing");
            string line;
            while ((line=reader.ReadLine()) != null) {
                if (line.Length < 24 || line[0] != '"' || line[11]!='"' || line[13]!='"') continue;
                int hour = (line[14]-'0')*10 + line[15]-'0';
                if (hour >= 6 && hour < 19 || hour < 0 || hour > 23) continue;
                string date = line.Substring(1,10);
                string[] night;
                if (!keys.TryGetValue(date,out night)) {
                    DateTime day;
                    if (!DateTime.TryParseExact(date,"yyyy-MM-dd",CultureInfo.InvariantCulture,DateTimeStyles.None,out day)) continue;
                    night=new[]{day.ToString("yyyyMMdd"),day.AddDays(-1).ToString("yyyyMMdd")};
                    keys.Add(date,night);
                }
                string key=night[hour>=19?0:1];
                int rank;
                var columns=line.Trim('"').Split(separator,StringSplitOptions.None);
                if (columns.Length <= column || !ranks.TryGetValue(columns[column].Trim(),out rank)) continue;
                int previous;
                if (!days.TryGetValue(key,out previous) || rank > previous) days[key]=rank;
            }
        }
        return days;
    }
}
'@
$data=[RainBackfill]::Scan($source)
$encoding=[Text.UTF8Encoding]::new($false)
$changed=0
foreach($file in $files){
    if(!$data.ContainsKey($file.BaseName)){continue}
    $summary=Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json
    if($summary.PSObject.Properties['rain_condition']){continue}
    $summary | Add-Member -NotePropertyName rain_condition -NotePropertyValue (@('','dry','wet','rain')[$data[$file.BaseName]])
    [IO.File]::WriteAllText($file.FullName,($summary|ConvertTo-Json -Depth 4 -Compress),$encoding)
    $changed++
}
if($changed){
    Git-Checked add -- data/allsky-night-weather
    Git-Checked -c user.name='Digital StarGate Weather' -c user.email='maininimassimo-bit@users.noreply.github.com' commit -m 'Backfill AllSky nightly rain conditions'
    Git-Checked push origin HEAD:main
}
"Updated nights: $changed"
