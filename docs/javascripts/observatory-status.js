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
  const badge = state => { const value=String(state||'UNKNOWN').toUpperCase(); if(['SAFE','OPEN','CLOSED','PARKED','TRACKING','ONLINE','IDLE','READY','CURRENT','AVAILABLE','MAINS_PRESENT','HEALTHY'].includes(value))return `🟢 ${value}`; if(['UNSAFE','FAULT','OFFLINE','ALARM','MAINS_LOST'].includes(value))return `🔴 ${value}`; return `🟡 ${value}`; };
  const set = (key,value) => document.querySelectorAll(`[data-observatory-status="${key}"]`).forEach(element=>{element.textContent=value;});
  const setEagle = (key,value) => document.querySelectorAll(`[data-eagle-health="${key}"]`).forEach(element=>{element.textContent=value;});
  const setLatestScientific = (key,value) => document.querySelectorAll(`[data-latest-scientific="${key}"]`).forEach(element=>{element.textContent=value;});
  let latestObservatoryPayload = null;
  let latestEaglePayload = null;
  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
  // Presentation scales are separate from governed evaluation thresholds.
  const finiteValue = value => (typeof value === 'number' || typeof value === 'string' && value.trim() !== '') && Number.isFinite(Number(value));
  const domainBar = (label, value, threshold, unit, state, note) => {
    const hasValue = state !== 'unavailable' && finiteValue(value);
    const numeric = hasValue ? Number(value) : null;
    const minimum = threshold?.minExclusive ?? threshold?.min;
    const maximum = unit.includes('%') ? 100 : threshold?.max === 0 ? 1 : threshold?.max !== undefined ? threshold.max * 2 : 20;
    const limit = threshold?.max ?? minimum;
    const ratio = hasValue ? Math.max(0, Math.min(1, numeric / maximum)) : 0;
    const isBad = hasValue && ((threshold?.max !== undefined && numeric > threshold.max) || (threshold?.minExclusive !== undefined && numeric <= threshold.minExclusive) || (threshold?.min !== undefined && numeric < threshold.min));
    const tone = !hasValue ? 'unknown' : isBad || state === 'bad' ? 'bad' : 'good';
    const display = hasValue ? `${numeric.toLocaleString('it-IT', { maximumFractionDigits: 1 })}${unit}` : 'UNKNOWN';
    const status = !hasValue ? 'Non corrente / non disponibile' : isBad ? 'Soglia superata' : 'Entro soglia';
    return `<article class="dsg-instrument is-${tone}" data-instrument-type="dial" data-instrument-value="${hasValue ? numeric : ''}" data-instrument-ratio="${ratio}" data-instrument-limit="${limit / maximum}" data-instrument-tone="${tone}"><h4>${escapeHtml(label)}</h4><div class="dsg-instrument__port" aria-hidden="true"><span class="dsg-instrument__poster" style="--instrument-fill:${ratio * 360}deg"></span></div><strong class="dsg-instrument__value">${escapeHtml(display)}</strong><span class="dsg-instrument__status">${status}</span><small>${escapeHtml(note)}</small><small>Scala 0–${maximum}${escapeHtml(unit)}${hasValue && (numeric < 0 || numeric > maximum) ? ' · fuori scala' : ''}</small></article>`;
  };
  const stateBar = (label, state, detail) => {
    const value = String(state || 'UNKNOWN').toUpperCase();
    const good = ['SAFE','OPEN','CLOSED','PARKED','TRACKING','ONLINE','IDLE','READY','MAINS_PRESENT','AVAILABLE','CURRENT','HEALTHY'].includes(value);
    const bad = ['UNSAFE','FAULT','OFFLINE','ALARM','MAINS_LOST','DEGRADED'].includes(value);
    const tone = good ? 'good' : bad ? 'bad' : 'unknown';
    const type = ({ Cupola:'dome', Montatura:'mount', Camera:'camera', Alimentazione:'power', Rete:'network', Uptime:'clock', 'Windows Time':'clock' })[label] || 'state';
    return `<article class="dsg-instrument is-${tone}" data-instrument-type="${type}" data-instrument-state="${escapeHtml(value)}" data-instrument-tone="${tone}"><h4>${escapeHtml(label)}</h4><div class="dsg-instrument__port" aria-hidden="true"><span class="dsg-instrument__symbol">${tone === 'unknown' ? '?' : bad ? '!' : '●'}</span></div><strong class="dsg-instrument__value">${escapeHtml(value)}</strong><small>${escapeHtml(detail || 'Stato descrittivo read-only')}</small></article>`;
  };
  const domainMarkup = new WeakMap();
  const renderDomainBars = () => {
    const root = document.querySelector('[data-observatory-domains]');
    if (!root) return;
    const weather = latestObservatoryPayload?.systems?.weather;
    const observatoryFresh = isFresh(latestObservatoryPayload);
    const systems = Object.fromEntries(Object.entries(latestObservatoryPayload?.systems || {}).map(([key, value]) => {
      const normalized = normalize(value);
      return [key, observatoryFresh && normalized.quality === 'CURRENT' ? normalized : { ...normalized, state: 'UNKNOWN', quality: observatoryFresh ? normalized.quality : 'STALE' }];
    }));
    const eagle = latestEaglePayload;
    const signals = eagle?.signals || {};
    const current = signal => isFresh(eagle) && signal && isFresh(signal) && signal.quality === 'CURRENT' ? signal.data || {} : null;
    const cpu = current(signals.cpu), memory = current(signals.memory), storage = current(signals.storage), timeSync = current(signals.time_sync);
    const eagleState = isFresh(eagle) ? eagle?.summary?.state : 'UNAVAILABLE / STALE_OR_MISSING';
    const weatherCurrent = observatoryFresh && weather && isFresh(weather) && weather.quality === 'CURRENT' ? weather : null;
    const weatherTemp = Number(weatherCurrent?.temperature_c), weatherDew = Number(weatherCurrent?.dew_point_c);
    const dewMargin = finiteValue(weatherCurrent?.temperature_c) && finiteValue(weatherCurrent?.dew_point_c) ? weatherTemp - weatherDew : null;
    const sections = [];
    sections.push(`<section class="dsg-domain-group dsg-instrument-panel"><h3>EAGLE Health</h3><p>Policy BKL-036-F5 · aggregate: ${escapeHtml(eagleState || 'UNAVAILABLE')}</p><div class="dsg-instrument-grid">${domainBar('CPU load', cpu?.load_pct, {max:90}, ' %', cpu ? 'good' : 'unavailable', cpu ? 'verde ≤ 90%; rosso > 90%' : 'UNAVAILABLE / non corrente')}${domainBar('Memoria disponibile', finiteValue(memory?.available_ratio) ? Number(memory.available_ratio) * 100 : null, {min:20}, ' %', memory ? 'good' : 'unavailable', memory ? 'verde ≥ 20%; rosso < 20%' : 'UNAVAILABLE / non corrente')}${['C:', 'D:'].map(id => { const disk = (Array.isArray(storage?.logical_disks) ? storage.logical_disks : []).find(d => d.device_id === id); return domainBar(`Storage ${id}`, disk?.free_pct, {min:20}, ' % libero', disk ? 'good' : 'unavailable', 'verde ≥ 20%; rosso < 20%'); }).join('')}${stateBar('Uptime', Boolean(current(signals.uptime)) ? 'CURRENT' : 'UNKNOWN', 'Nessuna soglia di degrado; freshness obbligatoria')}${stateBar('Windows Time', timeSync?.last_successful_sync_utc ? 'CURRENT' : 'UNKNOWN', timeSync?.last_successful_sync_utc ? 'Sync corrente verificata' : 'Sync corrente non computabile')}</div></section>`);
    sections.push(`<section class="dsg-domain-group dsg-instrument-panel"><h3>Meteo operativo</h3><p>Policy BKL-032 · decision-support read-only</p><div class="dsg-instrument-grid">${domainBar('Vento medio', weatherCurrent?.wind_speed_kmh, {max:15}, ' km/h', weatherCurrent ? 'good' : 'unavailable', 'verde ≤ 15; rosso > 15')}${domainBar('Raffiche', weatherCurrent?.wind_gust_kmh, {max:20}, ' km/h', weatherCurrent ? 'good' : 'unavailable', 'verde ≤ 20; rosso > 20')}${domainBar('Nuvolosità', weatherCurrent?.cloud_cover_pct, {max:50}, ' %', weatherCurrent ? 'good' : 'unavailable', 'verde ≤ 50%; rosso > 50%')}${domainBar('Umidità relativa', weatherCurrent?.humidity_pct, {max:90}, ' %', weatherCurrent ? 'good' : 'unavailable', 'verde ≤ 90%; rosso > 90%')}${domainBar('Margine dew point', dewMargin, {minExclusive:3}, ' °C', weatherCurrent ? 'good' : 'unavailable', 'temperatura ambiente − dewpoint; verde > 3 °C; rosso ≤ 3 °C')}${domainBar('Pioggia', weatherCurrent?.rain_rate_mm_h, {max:0}, ' mm/h', weatherCurrent ? 'good' : 'unavailable', 'verde = 0; rosso > 0')}</div></section>`);
    sections.push(`<section class="dsg-domain-group dsg-instrument-panel"><h3>Sistemi osservati</h3><p>Stato descrittivo della telemetria N.I.N.A.; nessuna soglia numerica aggiunta</p><div class="dsg-instrument-grid">${stateBar('Cupola', systems.dome?.state, systems.dome?.quality || 'UNKNOWN')}${stateBar('Montatura', systems.mount?.state, systems.mount?.quality || 'UNKNOWN')}${stateBar('Camera', systems.camera?.state, systems.camera?.quality || 'UNKNOWN')}${stateBar('Alimentazione', systems.power?.state, systems.power?.quality || 'UNKNOWN')}${stateBar('Rete', systems.network?.state, systems.network?.quality || 'UNKNOWN')}</div></section>`);
    const markup = `<div class="dsg-domain-bars__legend"><span class="is-good">Verde · entro soglia / stato positivo</span><span class="is-bad">Rosso · soglia superata / stato degradato</span><span class="is-unknown">Ambra · non corrente o non disponibile</span></div>${sections.join('')}`;
    if (domainMarkup.get(root) !== markup) { domainMarkup.set(root, markup); root.innerHTML = markup; }
  };

  const render = (payload,transport='HOSTED') => {
    latestObservatoryPayload = payload;
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
    renderDomainBars();
  };

  const renderEagleUnavailable = quality => { latestEaglePayload = null; renderDomainBars(); setEagle('quality',badge(quality||'UNKNOWN')); setEagle('summary','UNAVAILABLE / NO_CURRENT_SNAPSHOT'); setEagle('observed-at','—'); setEagle('source','—'); ['cpu','memory','storage-capacity','storage-health','uptime','time-sync'].forEach(key=>setEagle(key,'—')); };
  const renderEagle = (payload,transport='HOSTED') => {
    if(payload?.component!=='DSG.EagleHealthPortalProjection'||!['HEALTHY','DEGRADED','UNAVAILABLE','UNKNOWN'].includes(payload?.summary?.state)||!payload?.summary?.reason)throw new Error('Invalid EAGLE health portal projection contract');
    latestEaglePayload = payload;
    const payloadFresh=isFresh(payload), signals=payload?.signals||{}; setEagle('quality',badge(payloadFresh?payload.quality:'STALE')); setEagle('summary',payloadFresh?`${text(payload.summary.state)} / ${text(payload.summary.reason)}`:'UNAVAILABLE / STALE_PROJECTION'); setEagle('observed-at',parseTime(payload?.observed_at_utc)?.toLocaleString('it-IT')||'—'); setEagle('source',`${text(payload?.source_component)} · ${text(payload?.host)} · ${transport}`);
    const cpu=normalize(signals.cpu), memory=normalize(signals.memory), storage=normalize(signals.storage), uptime=normalize(signals.uptime), timeSync=normalize(signals.time_sync);
    const cpuData=cpu.quality==='CURRENT'?cpu.data||{}:{}, memoryData=memory.quality==='CURRENT'?memory.data||{}:{}, storageData=storage.quality==='CURRENT'?storage.data||{}:{}, uptimeData=uptime.quality==='CURRENT'?uptime.data||{}:{}, timeData=timeSync.quality==='CURRENT'?timeSync.data||{}:{};
    setEagle('cpu',cpu.quality==='CURRENT'?`${text(cpuData.model)} · load ${number(cpuData.load_pct,0,' %')} · ${text(cpuData.physical_cores)} core / ${text(cpuData.logical_processors)} logical`:`${text(cpu.quality)} · ${text(cpu.reason)}`);
    setEagle('memory',memory.quality==='CURRENT'?`${bytes(memoryData.available_physical_bytes)} disponibili / ${bytes(memoryData.total_physical_bytes)} · ratio ${number(Number(memoryData.available_ratio)*100,1,' %')}`:`${text(memory.quality)} · ${text(memory.reason)}`);
    const logical=Array.isArray(storageData.logical_disks)?storageData.logical_disks:[]; setEagle('storage-capacity',storage.quality==='CURRENT'&&logical.length?logical.map(d=>`${text(d.device_id)} ${bytes(d.free_bytes)} liberi / ${bytes(d.size_bytes)} (${number(d.free_pct,1,' %')})`).join(' · '):`${text(storage.quality)} · ${text(storage.reason)}`);
    const physical=Array.isArray(storageData.physical_disks)?storageData.physical_disks:[]; setEagle('storage-health',storage.quality==='CURRENT'&&physical.length?physical.map(d=>`${text(d.friendly_name)}: ${text(d.health_status)} / ${Array.isArray(d.operational_status)?d.operational_status.join(', '):text(d.operational_status)}`).join(' · '):`${text(storage.quality)} · ${text(storage.reason)}`);
    setEagle('uptime',uptime.quality==='CURRENT'?`${number(Number(uptimeData.uptime_seconds)/86400,2,' giorni')} · boot ${parseTime(uptimeData.last_boot_at_utc)?.toLocaleString('it-IT')||'—'}`:`${text(uptime.quality)} · ${text(uptime.reason)}`);
    setEagle('time-sync',timeSync.quality==='CURRENT'?`servizio ${text(timeData.service_state)} · sorgente ${text(timeData.time_source)} · offset ${number(timeData.offset_ms,1,' ms')}`:`${text(timeSync.quality)} · ${text(timeSync.reason)}`);
    renderDomainBars();
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
  const initialize = () => { if(!document.querySelector('[data-observatory-status], [data-eagle-health]'))return; clearInterval(timer); refreshLatestScientific(); refreshEagleHealth(); refresh(); timer=window.setInterval(()=>{renderDomainBars();refresh();refreshEagleHealth();},REFRESH_MS); };
  if(window.DSG?.components)window.DSG.components.register({name:'observatory-status',order:66,initialize}); else if(window.document$?.subscribe)window.document$.subscribe(initialize); else if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize,{once:true}); else initialize();
})();
