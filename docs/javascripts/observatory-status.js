(() => {
  'use strict';

  const RELAY_BASE = 'https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app';
  const RUNTIME_ENDPOINT = `${RELAY_BASE}/v1/observatory-status`;
  const EAGLE_HEALTH_ENDPOINT = `${RELAY_BASE}/v1/eagle-health`;
  const FALLBACK_DATA_PATH = '../data/realtime/observatory-status.json';
  const EAGLE_HEALTH_PATH = '../data/realtime/eagle-health.json';
  const LATEST_SCIENTIFIC_PATH = '../data/realtime/latest-observation.json';
  const REFRESH_MS = 15000;

  const parseTime = value => { const date = value ? new Date(value) : null; return date && !Number.isNaN(date.getTime()) ? date : null; };
  const isFresh = signal => { const freshUntil = parseTime(signal?.fresh_until_utc); return Boolean(freshUntil && freshUntil.getTime() >= Date.now()); };
  const normalize = signal => !signal || !isFresh(signal) ? { ...(signal || {}), state: 'UNKNOWN', quality: signal ? 'STALE' : 'UNKNOWN' } : signal;
  const text = value => value === undefined || value === null || value === '' ? '—' : String(value);
  const bool = value => value === true ? 'Sì' : value === false ? 'No' : '—';
  const number = (value, digits, suffix) => Number.isFinite(Number(value)) ? `${Number(value).toLocaleString('it-IT', { minimumFractionDigits: digits, maximumFractionDigits: digits })}${suffix}` : '—';
  const bytes = value => { const n=Number(value); if(!Number.isFinite(n)) return '—'; if(n>=1024**3)return `${(n/(1024**3)).toLocaleString('it-IT',{maximumFractionDigits:1})} GiB`; if(n>=1024**2)return `${(n/(1024**2)).toLocaleString('it-IT',{maximumFractionDigits:1})} MiB`; return `${n.toLocaleString('it-IT')} B`; };
  const badge = state => { const value=String(state||'UNKNOWN').toUpperCase(); if(['SAFE','OPEN','CLOSED','PARKED','TRACKING','ONLINE','IDLE','READY','CURRENT','AVAILABLE','MAINS_PRESENT'].includes(value))return `🟢 ${value}`; if(['UNSAFE','FAULT','OFFLINE','ALARM','MAINS_LOST'].includes(value))return `🔴 ${value}`; return `🟡 ${value}`; };
  const set = (key,value) => document.querySelectorAll(`[data-observatory-status="${key}"]`).forEach(element=>{element.textContent=value;});
  const setEagle = (key,value) => document.querySelectorAll(`[data-eagle-health="${key}"]`).forEach(element=>{element.textContent=value;});
  const setLatestScientific = (key,value) => document.querySelectorAll(`[data-latest-scientific="${key}"]`).forEach(element=>{element.textContent=value;});

  const render = (payload,transport='HOSTED') => {
    const systems=payload?.systems||{}, diagnostics=payload?.diagnostics||{}, safety=payload?.safety||{};
    const dome=normalize(systems.dome), mount=normalize(systems.mount), camera=normalize(systems.camera), power=normalize(systems.power), network=normalize(systems.network), weather=normalize(systems.weather);
    const payloadFresh=parseTime(payload?.fresh_until_utc)?.getTime()>=Date.now(); const overallQuality=payloadFresh?text(payload?.quality||'UNKNOWN'):'STALE'; const safetyState=payloadFresh?text(safety.observed_state||'UNKNOWN'):'UNKNOWN';
    set('transport',transport); set('quality',badge(overallQuality)); set('observed-at',parseTime(payload?.observed_at_utc)?.toLocaleString('it-IT')||'—'); set('source',text(payload?.source_component));
    set('safety-state',badge(safetyState)); set('safety-detail',`Fonte: ${text(safety.authority)} · telemetria, non autorità di comando`);
    set('dome-state',badge(dome.state)); set('dome-detail',`Shutter: ${text(diagnostics.dome_raw_shutter_status)} · qualità: ${text(dome.quality)}`);
    set('mount-state',badge(mount.state)); set('mount-detail',`parked: ${bool(diagnostics.mount_at_park)} · home: ${bool(diagnostics.mount_at_home)} · tracking: ${bool(diagnostics.mount_tracking)} · pier: ${text(diagnostics.mount_side_of_pier)}`);
    set('camera-state',badge(camera.state)); set('camera-detail',`cooler: ${bool(diagnostics.camera_cooler_on)} · power: ${number(diagnostics.camera_cooler_power_pct,0,' %')} · temperatura: ${number(diagnostics.camera_temperature_c,1,' °C')} · exposing: ${bool(diagnostics.camera_exposing)}`);
    set('power-state',badge(power.state)); set('power-detail',`Rete 12 V J6: ${bool(power.mains_present)} · fault: ${bool(power.power_fault)} · safeties: ${text(power.safeties_raw)} · mask: ${text(power.power_fault_mask)} · TS Shelter safe: ${bool(power.safety_is_safe??diagnostics.power_safety_is_safe)} · qualità: ${text(power.quality)}`);
    set('network-state',badge(network.state)); set('network-detail',`Interfaccia: ${text(diagnostics.network_interface)} · gateway: ${text(diagnostics.network_gateway)} (${bool(diagnostics.network_gateway_reachable)}, ${number(diagnostics.network_gateway_latency_ms,0,' ms')}) · Internet: ${bool(diagnostics.network_internet_reachable)} (${number(diagnostics.network_internet_latency_ms,0,' ms')}) · DNS: ${bool(diagnostics.network_dns_resolved)} (${number(diagnostics.network_dns_latency_ms,0,' ms')}) · qualità: ${text(network.quality)}`);
    set('network-link-detail',`Active link: ${text(network.active_link)} · VPN: ${bool(network.vpn)} · LTE failover: ${bool(network.lte_failover)}`);
    set('weather-state',badge(weather.state)); set('weather-temperature',number(weather.temperature_c,1,' °C')); set('weather-humidity',number(weather.humidity_pct,1,' %')); set('weather-dew-point',number(weather.dew_point_c,1,' °C')); set('weather-wind',number(weather.wind_speed_kmh,1,' km/h')); set('weather-gust',number(weather.wind_gust_kmh,1,' km/h')); set('weather-rain',number(weather.rain_rate_mm_h,2,' mm/h')); set('weather-pressure',number(weather.pressure_hpa,1,' hPa')); set('weather-cloud-cover',number(weather.cloud_cover_pct,0,' %')); set('weather-sqm',number(weather.sqm_mag_arcsec2,2,' mag/arcsec²')); set('weather-sky-temperature',number(weather.sky_temperature_c,1,' °C'));
  };

  const renderEagleUnavailable = quality => { setEagle('quality',badge(quality||'UNKNOWN')); setEagle('summary','UNKNOWN / POLICY_NOT_ACTIVATED'); setEagle('observed-at','—'); setEagle('source','—'); ['cpu','memory','storage-capacity','storage-health','uptime','time-sync'].forEach(key=>setEagle(key,'—')); };
  const renderEagle = (payload,transport='HOSTED') => {
    if(payload?.component!=='DSG.EagleHealthPortalProjection'||payload?.summary?.state!=='UNKNOWN'||payload?.summary?.reason!=='POLICY_NOT_ACTIVATED')throw new Error('Invalid EAGLE health portal projection contract');
    const payloadFresh=isFresh(payload), signals=payload?.signals||{}; setEagle('quality',badge(payloadFresh?payload.quality:'STALE')); setEagle('summary','UNKNOWN / POLICY_NOT_ACTIVATED'); setEagle('observed-at',parseTime(payload?.observed_at_utc)?.toLocaleString('it-IT')||'—'); setEagle('source',`${text(payload?.source_component)} · ${text(payload?.host)} · ${transport}`);
    const cpu=normalize(signals.cpu), memory=normalize(signals.memory), storage=normalize(signals.storage), uptime=normalize(signals.uptime), timeSync=normalize(signals.time_sync);
    const cpuData=cpu.quality==='CURRENT'?cpu.data||{}:{}, memoryData=memory.quality==='CURRENT'?memory.data||{}:{}, storageData=storage.quality==='CURRENT'?storage.data||{}:{}, uptimeData=uptime.quality==='CURRENT'?uptime.data||{}:{}, timeData=timeSync.quality==='CURRENT'?timeSync.data||{}:{};
    setEagle('cpu',cpu.quality==='CURRENT'?`${text(cpuData.model)} · load ${number(cpuData.load_pct,0,' %')} · ${text(cpuData.physical_cores)} core / ${text(cpuData.logical_processors)} logical`:`${text(cpu.quality)} · ${text(cpu.reason)}`);
    setEagle('memory',memory.quality==='CURRENT'?`${bytes(memoryData.available_physical_bytes)} disponibili / ${bytes(memoryData.total_physical_bytes)} · ratio ${number(Number(memoryData.available_ratio)*100,1,' %')}`:`${text(memory.quality)} · ${text(memory.reason)}`);
    const logical=Array.isArray(storageData.logical_disks)?storageData.logical_disks:[]; setEagle('storage-capacity',storage.quality==='CURRENT'&&logical.length?logical.map(d=>`${text(d.device_id)} ${bytes(d.free_bytes)} liberi / ${bytes(d.size_bytes)} (${number(d.free_pct,1,' %')})`).join(' · '):`${text(storage.quality)} · ${text(storage.reason)}`);
    const physical=Array.isArray(storageData.physical_disks)?storageData.physical_disks:[]; setEagle('storage-health',storage.quality==='CURRENT'&&physical.length?physical.map(d=>`${text(d.friendly_name)}: ${text(d.health_status)} / ${Array.isArray(d.operational_status)?d.operational_status.join(', '):text(d.operational_status)}`).join(' · '):`${text(storage.quality)} · ${text(storage.reason)}`);
    setEagle('uptime',uptime.quality==='CURRENT'?`${number(Number(uptimeData.uptime_seconds)/86400,2,' giorni')} · boot ${parseTime(uptimeData.last_boot_at_utc)?.toLocaleString('it-IT')||'—'}`:`${text(uptime.quality)} · ${text(uptime.reason)}`);
    setEagle('time-sync',timeSync.quality==='CURRENT'?`servizio ${text(timeData.service_state)} · sorgente ${text(timeData.time_source)} · offset ${number(timeData.offset_ms,1,' ms')}`:`${text(timeSync.quality)} · ${text(timeSync.reason)}`);
  };

  const renderLatestScientific = payload => { const metrics=payload?.metrics||{}; setLatestScientific('session-id',text(payload?.session_id)); setLatestScientific('target',text(payload?.target?.name)); setLatestScientific('metadata-state',text(payload?.metadata_state)); setLatestScientific('integration',number(metrics.integration_hours,2,' h')); setLatestScientific('frames',Number.isFinite(Number(metrics.completed_frames))?Number(metrics.completed_frames).toLocaleString('it-IT'):'—'); setLatestScientific('rms',number(metrics.rms_total_arcsec,3,'″')); };
  const renderUnavailable = () => render({quality:'UNKNOWN',systems:{},safety:{}},'UNAVAILABLE');
  const fetchJson = async url => { const response=await fetch(url,{cache:'no-store'}); if(!response.ok)throw new Error(`HTTP ${response.status}`); return response.json(); };
  const refreshLatestScientific = async () => { try{renderLatestScientific(await fetchJson(new URL(LATEST_SCIENTIFIC_PATH,document.baseURI)));}catch(error){console.warn('Digital StarGate: latest scientific observation unavailable',error);renderLatestScientific({});} };
  const refreshEagleHealth = async () => {
    try { renderEagle(await fetchJson(EAGLE_HEALTH_ENDPOINT),'CLOUD RUN'); return; } catch(runtimeError) { console.warn('Digital StarGate: hosted EAGLE health unavailable',runtimeError); }
    try { renderEagle(await fetchJson(new URL(EAGLE_HEALTH_PATH,document.baseURI)),'FALLBACK'); } catch(fallbackError) { console.warn('Digital StarGate: fallback EAGLE health unavailable',fallbackError); renderEagleUnavailable('UNKNOWN'); }
  };
  let timer;
  const refresh = async () => { try{render(await fetchJson(RUNTIME_ENDPOINT),'CLOUD RUN');return;}catch(runtimeError){console.warn('Digital StarGate: hosted observatory telemetry unavailable',runtimeError);} try{render(await fetchJson(new URL(FALLBACK_DATA_PATH,document.baseURI)),'FALLBACK');}catch(fallbackError){console.warn('Digital StarGate: fallback observatory telemetry unavailable',fallbackError);renderUnavailable();} };
  const initialize = () => { if(!document.querySelector('[data-observatory-status], [data-eagle-health]'))return; clearInterval(timer); refreshLatestScientific(); refreshEagleHealth(); refresh(); timer=window.setInterval(()=>{refresh();refreshEagleHealth();},REFRESH_MS); };
  if(window.DSG?.components)window.DSG.components.register({name:'observatory-status',order:66,initialize}); else if(window.document$?.subscribe)window.document$.subscribe(initialize); else if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize,{once:true}); else initialize();
})();
