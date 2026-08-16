(() => {
  'use strict';

  const DATA_PATH = 'data/realtime/observatory-status.json';
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
  const number = (value, digits, suffix) => Number.isFinite(Number(value)) ? `${Number(value).toLocaleString('it-IT', { minimumFractionDigits: digits, maximumFractionDigits: digits })}${suffix}` : '—';

  const badge = state => {
    const value = String(state || 'UNKNOWN').toUpperCase();
    if (['SAFE', 'OPEN', 'CLOSED', 'PARKED', 'TRACKING', 'ONLINE', 'IDLE'].includes(value)) return `🟢 ${value}`;
    if (['UNSAFE', 'FAULT', 'OFFLINE', 'ALARM'].includes(value)) return `🔴 ${value}`;
    return `🟡 ${value}`;
  };

  const set = (key, value) => {
    document.querySelectorAll(`[data-observatory-status="${key}"]`).forEach(element => { element.textContent = value; });
  };

  const render = payload => {
    const systems = payload?.systems || {};
    const dome = normalize(systems.dome), mount = normalize(systems.mount), camera = normalize(systems.camera), power = normalize(systems.power), network = normalize(systems.network), weather = normalize(systems.weather);
    const payloadFresh = parseTime(payload?.fresh_until_utc)?.getTime() >= Date.now();
    const overallQuality = payloadFresh ? text(payload?.quality || 'UNKNOWN') : 'STALE';

    set('quality', badge(overallQuality));
    set('observed-at', parseTime(payload?.observed_at_utc)?.toLocaleString('it-IT') || '—');
    set('source', text(payload?.source_component));
    set('dome-state', badge(dome.state));
    set('dome-detail', `OPEN: ${text(dome.open_sensor)} · CLOSED: ${text(dome.closed_sensor)} · SAFE: ${text(dome.safe_signal)}`);
    set('mount-state', badge(mount.state));
    set('mount-detail', `parked: ${text(mount.parked)} · tracking: ${text(mount.tracking)}`);
    set('camera-state', badge(camera.state));
    set('camera-detail', `cooling: ${text(camera.cooling)} · ${number(camera.temperature_c, 1, ' °C')}`);
    set('power-state', badge(power.state));
    set('power-detail', `UPS su batteria: ${text(power.ups_on_battery)}`);
    set('network-state', badge(network.state));
    set('network-detail', `link: ${text(network.active_link)} · VPN: ${text(network.vpn)} · LTE: ${text(network.lte_failover)}`);
    set('weather-state', badge(weather.state));
    set('weather-temperature', number(weather.temperature_c, 1, ' °C'));
    set('weather-humidity', number(weather.humidity_pct, 1, ' %'));
    set('weather-dew-point', number(weather.dew_point_c, 1, ' °C'));
    set('weather-wind', number(weather.wind_speed_kmh, 1, ' km/h'));
    set('weather-gust', number(weather.wind_gust_kmh, 1, ' km/h'));
    set('weather-rain', number(weather.rain_rate_mm_h, 2, ' mm/h'));
    set('weather-pressure', number(weather.pressure_hpa, 1, ' hPa'));
    set('weather-sqm', number(weather.sqm_mag_arcsec2, 2, ' mag/arcsec²'));
    set('weather-sky-temperature', number(weather.sky_temperature_c, 1, ' °C'));
  };

  const renderUnavailable = () => render({ quality: 'UNKNOWN', systems: {} });

  let timer;
  const refresh = async () => {
    try {
      const response = await fetch(new URL(DATA_PATH, document.baseURI), { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      render(await response.json());
    } catch (error) {
      console.warn('Digital StarGate: realtime observatory telemetry unavailable', error);
      renderUnavailable();
    }
  };

  const initialize = () => {
    if (!document.querySelector('[data-observatory-status]')) return;
    clearInterval(timer);
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
