import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {summarizeNightSky} from '../../docs/javascripts/planner-weather-sky.mjs';

// Run the actual consumer with a minimal DOM and a governed public projection.
const source=fs.readFileSync(new URL('../../docs/javascripts/observation-planner-f9.js',import.meta.url),'utf8').replace(/^import .*;\r?\n/,'');
const baseline=JSON.parse(fs.readFileSync(new URL('../../docs/data/observation-planner-f9-current-night.json',import.meta.url)));
async function render(uncertain,policy='DSG-F9-PLANNER-WEATHER-GATE@1.2'){
  const data=structuredClone(baseline);data.weatherPolicy.id=policy;
  // Keep this test independent of the age of the checked-in forecast.
  const now=Date.parse(data.generatedAtUtc);
  for(const row of data.hourly){Object.assign(row.weather,{cloudCoverPct:0,relativeHumidityPct:20,precipitationMm:0,temperatureC:15,dewPointC:4,windSpeedKmh:0,windGustKmh:0});}
  if(uncertain)data.hourly[0].weather.precipitationUncertain=true;
  const controls=new Map(['setup','status','category','results'].map(k=>['#dsg-f9-'+k,{value:k==='setup'?data.setupProfiles[0].setupId:'ALL',innerHTML:'',addEventListener(){}}]));
  let panel='';const root={isConnected:true,innerHTML:'',querySelector:s=>controls.get(s)||null,querySelectorAll:s=>s==='.dsg-op-panel'?[{}, {insertAdjacentHTML:(_,html)=>{panel=html;}}]:[],prepend(){}};
  class Clock extends Date{static now(){return now;}}
  vm.runInNewContext(source,{Date:Clock,document:{hidden:false,querySelector:()=>root,createElement:()=>({}),addEventListener(){}},window:{addEventListener(){}},createWeatherSky:()=>({show(){},clear(){}}),AbortController,fetch:async()=>({ok:true,json:async()=>data}),setTimeout:()=>1,clearTimeout(){},setInterval:()=>1,clearInterval(){}});
  await new Promise(resolve=>setImmediate(resolve));
  assert.ok(root.innerHTML.includes('Planner della notte corrente'),root.innerHTML);
  return {panel,ranking:controls.get('#dsg-f9-results').innerHTML,data,now};
}
const uncertain=await render(true);
assert.match(uncertain.panel,/precipitazione indeterminata \(precisione GRIB\)/);
assert.match(uncertain.panel,/<strong>indeterminata<\/strong>/);
assert.match(uncertain.panel,/aria-label="Meteo NO-GO"/);
assert.equal(summarizeNightSky(uncertain.data,uncertain.now),null);
const clear=await render(false);
assert.match(clear.panel,/aria-label="Meteo GO"/);
assert.doesNotMatch(clear.panel,/indeterminata/);
assert.equal(summarizeNightSky(clear.data,clear.now)?.state,'clear');
const legacy=await render(false,'DSG-F9-PLANNER-WEATHER-GATE@1.1');
assert.match(legacy.ranking,/Graduatoria e finestre sospese/);
console.log('F9 consumer: uncertainty, dry baseline, sky and legacy-policy checks PASS');
