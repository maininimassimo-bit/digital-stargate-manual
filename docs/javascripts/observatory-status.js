(() => {
  'use strict';

  const RUNTIME_ENDPOINT = 'https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app/v1/observatory-status';
  const FALLBACK_DATA_PATH = '../data/realtime/observatory-status.json';
  const LATEST_SCIENTIFIC_PATH = '../data/realtime/latest-observation.json';
  const REFRESH_MS = 15000;

  const parseTime = value => {
    const date = value ? new Date(value) : null;
    return date && !Number.isNaN(date.getTime()) ? date : null;
  };

  const isFresh = signal => {
    const freshUntil = parseTime(signal?.fresh_until_utc);
    return Boolean(freshUntil && freshUntil.getTime() >= Date.now());
  };

  const normalize = signal => {
    if (!signal || !isFresh(signal)) return { ...(signal || {}), state: 'UNKNOWN', quality: signal ? 'STALE' : 'UNKNOWN' };
    return signal;
  };

  const text = value => value === undefined || value === null || value === '' ? '—' : String(value);
  const bool = value => value === true ? 'Sì' : value === false ? 'No' : '—';
  const number = (value, digits, suffix) => Number.isFinite(Number(value)) ? `${Number(value).toLocaleString('it-IT', { minimumFractionDigits: digits, maximumFractionDigits: digits })}${suffix}` : '—';

  const badge = state => {
    const value = String(state || 'UNKNOWN').toUpperCase();
    if (['SAFE', 'OPEN', 'CLOSED', 'PARKED', 'TRACKING', 'ONLINE', 'IDLE', 'READY', 'CURRENT', 'AVAILABLE', 'MAINS_PRESENT'].includes(value)) return `🟢 ${value}`;
    if (['UNSAFE', 'FAULT', 'OFFLINE', 'ALARM', 'MAINS_LOST'].includes(value)) return `🔴 ${value}`;
    return `🟡 ${value}`;
  };

  const set = (key, value) => {
    document.querySelectorAll(`[data-observatory-status="${key}"]`).forEach(element => { element.textContent = value; });
  };

  const setLatestScientific = (key, value) => {
    document.querySelectorAll(`[data-latest-scientific="${key}"]`).forEach(element => { element.textContent = value; });
  };

  const render = (payload, transport = 'HOSTED') => {
    const systems = payload?.systems || {};
    const diagnostics = payload?.diagnostics || {};
    const safety = payload?.safety || {};
    const dome = normalize(systems.dome), mount = normalize(systems.mount), camera = normalize(systems.camera), power = normalize(systems.power), network = normalize(systems.network), weather = normalize(systems.weather);
    const payloadFresh = parseTime(payload?.fresh_until_utc)?.getTime() >= Date.now();
    const overallQuality = payloadFresh ? text(payload?.quality || 'UNKNOWN') : 'STALE';
    const safetyState = payloadFresh ? text(safety.observed_state || 'UNKNOWN') : 'UNKNOWN';

    set('transport', transport);
    set('quality', badge(overallQuality));
    set('observed-at', parseTime(payload?.observed_at_utc)?.toLocaleString('it-IT') || '—');
    set('source', text(payload?.source_component));

    set('safety-state', badge(safetyState));
    set('safety-detail', `Fonte: ${text(safety.authority)} · telemetria, non autorità di comando`);

    set('dome-state', badge(dome.state));
    set('dome-detail', `Shutter: ${text(diagnostics.dome_raw_shutter_status)} · qualità: ${text(dome.quality)}`);

    set('mount-state', badge(mount.state));
    set('mount-detail', `parked: ${bool(diagnostics.mount_at_park)} · home: ${bool(diagnostics.mount_at_home)} · tracking: ${bool(diagnostics.mount_tracking)} · pier: ${text(diagnostics.mount_side_of_pier)}`);

    set('camera-state', badge(camera.state));
    set('camera-detail', `cooler: ${bool(diagnostics.camera_cooler_on)} · power: ${number(diagnostics.camera_cooler_power_pct, 0, ' %')} · temperatura: ${number(diagnostics.camera_temperature_c, 1, ' °C')} · exposing: ${bool(diagnostics.camera_exposing)}`);

    set('power-state', badge(power.state));
    set('power-detail', `Rete 12 V J6: ${bool(power.mains_present)} · fault: ${bool(power.power_fault)} · safeties: ${text(power.safeties_raw)} · mask: ${text(power.power_fault_mask)} · TS Shelter safe: ${bool(power.safety_is_safe ?? diagnostics.power_safety_is_safe)} · qualità: ${text(power.quality)}`);

    set('network-state', badge(network.state));
    set('network-detail', `Interfaccia: ${text(diagnostics.network_interface)} · gateway: ${text(diagnostics.network_gateway)} (${bool(diagnostics.network_gateway_reachable)}, ${number(diagnostics.network_gateway_latency_ms, 0, ' ms')}) · Internet: ${bool(diagnostics.network_internet_reachable)} (${number(diagnostics.network_internet_latency_ms, 0, ' ms')}) · DNS: ${bool(diagnostics.network_dns_resolved)} (${number(diagnostics.network_dns_latency_ms, 0, ' ms')}) · qualità: ${text(network.quality)}`);
    set('network-link-detail', `Active link: ${text(network.active_link)} · VPN: ${bool(network.vpn)} · LTE failover: ${bool(network.lte_failover)}`);

    set('weather-state', badge(weather.state));
    set('weather-temperature', number(weather.temperature_c, 1, ' °C'));
    set('weather-humidity', number(weather.humidity_pct, 1, ' %'));
    set('weather-dew-point', number(weather.dew_point_c, 1, ' °C'));
    set('weather-wind', number(weather.wind_speed_kmh, 1, ' km/h'));
    set('weather-gust', number(weather.wind_gust_kmh, 1, ' km/h'));
    set('weather-rain', number(weather.rain_rate_mm_h, 2, ' mm/h'));
    set('weather-pressure', number(weather.pressure_hpa, 1, ' hPa'));
    set('weather-cloud-cover', number(weather.cloud_cover_pct, 0, ' %'));
    set('weather-sqm', number(weather.sqm_mag_arcsec2, 2, ' mag/arcsec²'));
    set('weather-sky-temperature', number(weather.sky_temperature_c, 1, ' °C'));
  };

  const renderLatestScientific = payload => {
    const metrics = payload?.metrics || {};
    setLatestScientific('session-id', text(payload?.session_id));
    setLatestScientific('target', text(payload?.target?.name));
    setLatestScientific('metadata-state', text(payload?.metadata_state));
    setLatestScientific('integration', number(metrics.integration_hours, 2, ' h'));
    setLatestScientific('frames', Number.isFinite(Number(metrics.completed_frames)) ? Number(metrics.completed_frames).toLocaleString('it-IT') : '—');
    setLatestScientific('rms', number(metrics.rms_total_arcsec, 3, '″'));
  };

  const renderUnavailable = () => render({ quality: 'UNKNOWN', systems: {}, safety: {} }, 'UNAVAILABLE');

  const fetchJson = async url => {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  };

  const refreshLatestScientific = async () => {
    try {
      const url = new URL(LATEST_SCIENTIFIC_PATH, document.baseURI);
      renderLatestScientific(await fetchJson(url));
    } catch (error) {
      console.warn('Digital StarGate: latest scientific observation unavailable', error);
      renderLatestScientific({});
    }
  };

  let timer;
  const refresh = async () => {
    try {
      render(await fetchJson(RUNTIME_ENDPOINT), 'CLOUD RUN');
      return;
    } catch (runtimeError) {
      console.warn('Digital StarGate: hosted observatory telemetry unavailable', runtimeError);
    }

    try {
      const fallbackUrl = new URL(FALLBACK_DATA_PATH, document.baseURI);
      render(await fetchJson(fallbackUrl), 'FALLBACK');
    } catch (fallbackError) {
      console.warn('Digital StarGate: fallback observatory telemetry unavailable', fallbackError);
      renderUnavailable();
    }
  };

  const initialize = () => {
    if (!document.querySelector('[data-observatory-status]')) return;
    clearInterval(timer);
    refreshLatestScientific();
    refresh();
    timer = window.setInterval(refresh, REFRESH_MS);
  };

  if (window.DSG?.components) {
    window.DSG.components.register({ name: 'observatory-status', order: 66, initialize });
  } else if (window.document$?.subscribe) {
    window.document$.subscribe(initialize);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }
})();
