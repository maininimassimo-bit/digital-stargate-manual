// Presentation only. Called with the projection already accepted by the F9 consumer.
const HOUR = 3_600_000;
export function summarizeNightSky(d, now = Date.now()) {
  const from = Date.parse(d?.nightWindow?.fromUtc), to = Date.parse(d?.nightWindow?.toUtcExclusive);
  const run = Date.parse(d?.forecast?.runInitialisationUtc);
  const rows = d?.hourly;
  if (!Number.isFinite(from) || !Number.isFinite(to) || !Number.isFinite(run) ||
      now < run || now > run + 18 * HOUR || now >= to || from > now + 24 * HOUR ||
      to <= from || to - from > 24 * HOUR || !Array.isArray(rows) || !rows.length) return null;
  // The existing summary uses equally spaced hourly samples over this exact window.
  const expected = Math.ceil((to - from) / HOUR);
  if (rows.length !== expected) return null;
  let clouds = 0, rain = 0, wetHours = 0;
  for (const [i, row] of rows.entries()) {
    const {cloudCoverPct: c, precipitationMm: p} = row.weather || {};
    if ('precipitationUncertain' in (row.weather || {}) && row.weather.precipitationUncertain !== false) return null;
    if (Date.parse(row.validAtUtc) !== from + i * HOUR || !Number.isFinite(c) ||
        c < 0 || c > 100 || !Number.isFinite(p) || p < 0) return null;
    clouds += c; rain += p; if (p > 0) wetHours++;
  }
  const meanCloud = clouds / rows.length;
  // A visual convention, never a weather gate or readiness classification.
  return {state: rain > 0 ? 'rain' : meanCloud <= 20 ? 'clear' : 'cloudy',
    meanCloud, rain, wetHours, count: rows.length, from, to,
    expires: Math.min(to, run + 18 * HOUR + 1)};
}

export function createWeatherSky(host) {
  if (!host) return {show() {}, clear() {}};
  let timer, projection;
  const labels = {clear: 'Cielo prevalentemente sereno', cloudy: 'Cielo nuvoloso', rain: 'Pioggia prevista nella notte'};
  const title = host.querySelector('[data-sky-title]'), details = host.querySelector('[data-sky-details]');
  const image = host.querySelector('img'), period = host.querySelector('[data-sky-period]');
  function clear(message = 'Previsione non disponibile o scaduta') {
    clearTimeout(timer); projection = null; host.dataset.skyState = 'unknown';
    image.hidden = true; image.removeAttribute('src');
    title.textContent = message; details.textContent = 'Nessuna condizione del cielo dedotta.'; period.textContent = '';
  }
  image.addEventListener('error', () => {image.hidden = true; host.dataset.skyImage = 'unavailable';});
  image.addEventListener('load', () => {image.hidden = false; host.dataset.skyImage = 'ready';});
  function show(d) {
    const s = summarizeNightSky(d);
    if (!s) return clear();
    clearTimeout(timer); projection = d; host.dataset.skyState = s.state;
    title.textContent = labels[s.state];
    const number = (n, digits) => n.toLocaleString('it-IT', {minimumFractionDigits: digits, maximumFractionDigits: digits});
    details.textContent = `Nuvole medie ${number(s.meanCloud, 1)}% · Pioggia totale ${number(s.rain, 3)} mm · ${s.wetHours}/${s.count} campioni con pioggia`;
    const date = n => new Date(n).toLocaleString('it-IT', {timeZone: 'Europe/Rome', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'});
    period.textContent = `${date(s.from)} – ${date(s.to)} · Europe/Rome · ${s.count} campioni orari`;
    image.alt = `${labels[s.state]}: illustrazione della media notturna, non fotografia del sito`;
    const src = new URL(`../assets/images/planner-sky/${s.state}.webp`, import.meta.url).href;
    if (image.src !== src) {image.hidden = true; image.src = src;}
    timer = setTimeout(() => clear(), Math.max(1, s.expires - Date.now()));
  }
  document.addEventListener('visibilitychange', () => {if (!document.hidden && projection) show(projection);});
  window.addEventListener('pageshow', () => {if (projection) show(projection);});
  return {show, clear};
}
