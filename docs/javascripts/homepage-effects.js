(() => {
  'use strict';

  const resolveSiteRoot = () => {
    const logo = document.querySelector('.md-header__button.md-logo');
    return logo ? new URL(logo.href, document.baseURI) : new URL('./', document.baseURI);
  };

  const ensureLatestObservationStyles = () => {
    if (document.querySelector('link[data-dsg-latest-observation-layout]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('styles/latest-observation-home.css', resolveSiteRoot()).href;
    link.dataset.dsgLatestObservationLayout = 'true';
    document.head.appendChild(link);
  };

  const ensureLatestObservationShowcase = () => {
    const home = document.querySelector('.dsg-enterprise-home');
    if (!home || home.querySelector('.dsg-showcase__media')) return;
    ensureLatestObservationStyles();

    const domainSection = home.querySelector('.dsg-domain-section');
    const section = document.createElement('section');
    section.className = 'dsg-showcase dsg-program-section dsg-latest-observation';
    section.setAttribute('aria-label', 'Ultima osservazione astronomica');
    section.innerHTML = `
      <div class="dsg-latest-observation__header">
        <div>
          <span class="dsg-section-kicker">ULTIMA OSSERVAZIONE</span>
          <h2>Vista astronomica governata</h2>
          <p>La vista è centrata sulle coordinate pubblicate dalla projection governata <code>latest-observation.json</code>.</p>
        </div>
        <a class="md-button dsg-latest-observation__explorer" href="./scientific-session-catalog/">Apri Session Explorer →</a>
      </div>
      <p data-latest-sky-note role="status">Caricamento dell’ultima sessione importata.</p>
      <button type="button" class="md-button" data-latest-sky-refresh>Aggiorna vista astronomica</button>
      <div class="dsg-showcase__layout">
        <div class="dsg-showcase__media" aria-label="Mappa dinamica dell'ultima osservazione astronomica"></div>
        <aside class="dsg-showcase__content" aria-label="Coordinate dell'ultima osservazione">
          <span class="dsg-section-kicker">SCIENTIFIC SNAPSHOT</span>
          <h2>Ultima osservazione</h2>
          <div class="dsg-showcase__sky-panel dsg-showcase__coordinate-panel">
            <div class="dsg-showcase__sky-meta">
              <span>Sessione</span><span data-sky-session>—</span>
              <span>Survey</span><span data-sky-survey>—</span>
              <span>FOV</span><span data-sky-fov>—</span>
              <span>RA (J2000)</span><span data-sky-ra>—</span>
              <span>DEC (J2000)</span><span data-sky-dec>—</span>
              <span>Coordinate source</span><span data-sky-source>—</span>
            </div>
          </div>
        </aside>
      </div>
      <div class="dsg-latest-observation__metrics-wrap">
        <span class="dsg-section-kicker">SCIENTIFIC SNAPSHOT</span>
        <div class="dsg-showcase__metrics">
          <div><span>Integrazione</span><strong>—</strong></div>
          <div><span>Light</span><strong>—</strong></div>
          <div><span>RMS</span><strong>—</strong></div>
        </div>
      </div>`;

    if (domainSection) home.insertBefore(section, domainSection);
    else home.appendChild(section);
  };

  const setText = (root, selector, value) => {
    const node = root.querySelector(selector);
    if (node) node.textContent = value;
  };

  const asNumber = (value) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
  };

  const hasNumber = (value) => value !== null && value !== undefined && value !== '' && Number.isFinite(Number(value));

  const formatNumber = (value, digits = 0) => asNumber(value).toLocaleString('it-IT', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  });

  const formatDate = (value) => {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return '—';
    const parsed = new Date(value);
    return Number.isNaN(parsed.getTime()) || parsed.toISOString().slice(0,10) !== value ? '—' : parsed.toLocaleDateString('it-IT', {timeZone:'UTC'});
  };

  const formatRa = (degrees) => {
    if (!Number.isFinite(Number(degrees))) return '—';
    const totalSeconds = Math.round((((Number(degrees) % 360) + 360) % 360) / 15 * 3600);
    const hours = Math.floor(totalSeconds / 3600) % 24;
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    return `${String(hours).padStart(2, '0')}h ${String(minutes).padStart(2, '0')}m ${String(seconds).padStart(2, '0')}s`;
  };

  const formatDec = (degrees) => {
    if (!Number.isFinite(Number(degrees))) return '—';
    const value = Number(degrees);
    const totalSeconds = Math.round(Math.abs(value) * 3600);
    const units = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    return `${value >= 0 ? '+' : '−'}${String(units).padStart(2, '0')}° ${String(minutes).padStart(2, '0')}′ ${String(seconds).padStart(2, '0')}″`;
  };

  const fetchProjection = async (path, signal) => {
    const response = await fetch(new URL(path, resolveSiteRoot()), { cache: 'no-store', signal });
    if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    return response.json();
  };

  const hydrateHomeSnapshot = async (board) => {
    if (!board?.isConnected || board.dataset.homeSnapshotLoading === 'true') return;
    board.dataset.homeSnapshotLoading = 'true';
    const button = board.querySelector('[data-home-refresh]');
    if (button) button.disabled = true;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);

    try {
      const [roadmap, catalog, latest] = await Promise.all([
        fetchProjection('data/roadmap.json', controller.signal),
        fetchProjection('data/scientific-session-catalog.json', controller.signal),
        fetchProjection('data/realtime/latest-observation.json', controller.signal)
      ]);
      if (!board.isConnected) return;
      if (!roadmap?.summary || !hasNumber(roadmap.summary.percentCompleted) || !Array.isArray(roadmap.waves) || !Array.isArray(catalog?.sessions)) {
        throw new Error('Contratto projection incompleto');
      }

      const roadmapItems = roadmap.waves.flatMap((wave) => Array.isArray(wave.items) ? wave.items : []);
      const current = roadmapItems.find((item) => item.id === roadmap.currentPackage);
      const sessions = catalog.sessions;
      const latestId = String(latest?.session_id || '');
      const ids = sessions.map(session => session.sessionId);
      if (new Set(ids).size !== ids.length || !/^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$/.test(latestId) || !ids.includes(latestId)) throw new Error('Identità catalogo/latest non coerente');
      const latestCatalog = sessions.find((session) => session.sessionId === latestId);
      const target = latest?.target || {};
      const equipment = latest?.equipment || {};
      const metrics = latest?.metrics || {};
      const integration = asNumber(metrics.integration_hours ?? latestCatalog.integrationHours);
      const frames = asNumber(metrics.completed_frames ?? latestCatalog.lightCompleted);
      const rmsValue = metrics.rms_total_arcsec ?? latestCatalog.rmsTotalArcsec;
      const rms = hasNumber(rmsValue) ? `${formatNumber(rmsValue, 3)} arcsec` : '—';
      const severity = String(latestCatalog.severity || 'UNKNOWN').toUpperCase();
      const coordinates = hasNumber(target.ra_deg) && hasNumber(target.dec_deg)
        ? `RA ${formatRa(target.ra_deg)} · Dec ${formatDec(target.dec_deg)} · ${target.epoch || 'J2000'}`
        : 'Coordinate non disponibili';
      const equipmentLabel = [equipment.telescope, equipment.camera].filter(Boolean).join(' · ') || 'Configurazione non disponibile';

      setText(board, '[data-home-current-package]', roadmap.currentPackage || 'UNKNOWN');
      setText(board, '[data-home-current-detail]', `${current?.title || 'Package corrente'} · avanzamento programma ${asNumber(roadmap.summary.percentCompleted)}%`);
      setText(board, '[data-home-latest-session]', latestId || 'UNKNOWN');
      const integrationLabel = hasNumber(metrics.integration_hours ?? latestCatalog.integrationHours) ? `${formatNumber(integration, 2)} h` : 'integrazione —';
      const framesLabel = hasNumber(metrics.completed_frames ?? latestCatalog.lightCompleted) ? `${formatNumber(frames)} light` : 'light —';
      setText(board, '[data-home-latest-detail]', `${target.name || latestCatalog.target || 'Target non disponibile'} · ${coordinates} · ${equipmentLabel} · ${integrationLabel} · ${framesLabel} · ${severity} · RMS ${rms}`);

      const latestLink = board.querySelector('[data-home-latest-link]');
      if (latestLink) {latestLink.href = new URL(`scientific-session-detail/?sessionId=${encodeURIComponent(latestId)}`, resolveSiteRoot()).href;latestLink.textContent = 'Apri dettaglio sessione';}

      const counter = value => typeof value === 'number' && Number.isInteger(value) && value >= 0;
      const hours = value => typeof value === 'number' && Number.isFinite(value) && value >= 0;
      if (sessions.some(session => ['lightStarted','lightCompleted'].some(key => session[key] != null && !counter(session[key])) || (session.integrationHours != null && !hours(session.integrationHours)))) throw new Error('Conteggi catalogo non validi');
      const acquisitions = sessions.filter(session => (counter(session.lightStarted) && session.lightStarted > 0) || (counter(session.lightCompleted) && session.lightCompleted > 0));
      const withoutLight = sessions.filter(session => session.lightStarted === 0 && session.lightCompleted === 0).length;
      const uncertain = sessions.length - acquisitions.length - withoutLight;
      const totalHours = sessions.reduce((sum, session) => sum + (hours(session.integrationHours) ? session.integrationHours : 0), 0);
      const totalFrames = sessions.reduce((sum, session) => sum + (counter(session.lightCompleted) ? session.lightCompleted : 0), 0);
      const unknownTargets = new Set(['UNKNOWN','N/A','NA','NOT_AVAILABLE','TARGET NON DISPONIBILE','NON DISPONIBILE','SCONOSCIUTO','—','-']);
      const targets = new Set(sessions.map(session => String(session.target || '').trim().toUpperCase()).filter(value => value && !unknownTargets.has(value)));
      const partial = sessions.some(session => !hours(session.integrationHours) || !counter(session.lightCompleted));
      setText(board, '[data-home-session-count]', `${acquisitions.length} sessioni con LIGHT`);
      setText(board, '[data-home-session-totals]', `${formatNumber(totalHours, 2)} h · ${formatNumber(totalFrames)} light · ${targets.size} target identificati${partial ? ' · totali parziali' : ''}`);
      setText(board, '[data-home-session-records]', `Catalogo: ${sessions.length} registrazioni · ${withoutLight} senza LIGHT${uncertain ? ` · ${uncertain} con acquisizione non determinabile` : ''}`);
      setText(board, '[data-home-freshness]', `Roadmap aggiornata: ${formatDate(roadmap.updatedAt)}`);
      const night = `${latestId.slice(0,10).split('-').reverse().join('/')}–${latestId.slice(11).split('-').reverse().join('/')}`;
      const generated = typeof latest.generated_at === 'string' ? new Date(latest.generated_at) : new Date(NaN);
      const updated = Number.isFinite(generated.getTime()) ? generated.toLocaleString('it-IT',{dateStyle:'short',timeStyle:'short',timeZone:'Europe/Rome'}) : 'non disponibile';
      setText(board, '[data-home-latest-freshness]', `Acquisizione: ${night} · Aggiornamento dati: ${updated}`);
      setText(board, '[data-home-refresh-status]', 'Aggiornamento automatico ogni 60 secondi mentre la pagina è visibile.');
      board.dataset.homeSnapshotState = 'ready';
    } catch (error) {
      if (!board.isConnected) return;
      setText(board, '[data-home-current-package]', 'UNKNOWN');
      setText(board, '[data-home-current-detail]', 'Projection roadmap non disponibile');
      setText(board, '[data-home-latest-session]', 'UNKNOWN');
      setText(board, '[data-home-latest-detail]', 'Projection scientifica non disponibile');
      setText(board, '[data-home-session-count]', '—');
      setText(board, '[data-home-session-totals]', 'Conteggi non disponibili');
      setText(board, '[data-home-freshness]', 'Dati non disponibili');
      setText(board, '[data-home-latest-freshness]', 'Date non disponibili');
      setText(board, '[data-home-session-records]', 'Registrazioni non disponibili');
      setText(board, '[data-home-refresh-status]', 'Aggiornamento non riuscito. Riprova con Aggiorna; il prossimo tentativo è automatico.');
      const link = board.querySelector('[data-home-latest-link]');
      if (link) {link.href = new URL('scientific-session-catalog/',resolveSiteRoot()).href;link.textContent = 'Apri catalogo';}
      board.dataset.homeSnapshotState = 'unavailable';
      console.warn('Digital StarGate homepage projection:', error);
    } finally {
      clearTimeout(timeout);
      if (button) button.disabled = false;
      board.dataset.homeSnapshotLoading = 'false';
    }
  };

  const initializeHome = () => {
    ensureLatestObservationShowcase();
    const board = document.querySelector('[data-dsg-home-snapshot]');
    if (!board || board.dataset.homeSnapshotRefreshReady === 'true') return;
    board.dataset.homeSnapshotRefreshReady = 'true';
    const refresh = () => hydrateHomeSnapshot(board);
    const visible = () => {if (!document.hidden) refresh();};
    board.querySelector('[data-home-refresh]')?.addEventListener('click',refresh);
    document.addEventListener('visibilitychange',visible);
    const timer = setInterval(() => {
      if (!board.isConnected) {clearInterval(timer);document.removeEventListener('visibilitychange',visible);return;}
      if (!document.hidden) refresh();
    },60000);
    refresh();
  };

  initializeHome();

  document.addEventListener('DOMContentLoaded', () => {
    initializeHome();
    const counters = document.querySelectorAll('.dsg-counter');
    if (!counters.length || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      counters.forEach((counter) => {
        const value = Number(counter.dataset.value || 0), decimals = Number(counter.dataset.decimals || 0), suffix = counter.dataset.suffix || '';
        counter.textContent = value.toLocaleString('it-IT', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix;
      });
      return;
    }
    const animate = (counter) => {
      const target = Number(counter.dataset.value || 0), decimals = Number(counter.dataset.decimals || 0), suffix = counter.dataset.suffix || '', duration = 900, start = performance.now();
      const frame = (now) => {
        const progress = Math.min((now - start) / duration, 1), current = target * (1 - Math.pow(1 - progress, 3));
        counter.textContent = current.toLocaleString('it-IT', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix;
        if (progress < 1) requestAnimationFrame(frame);
      };
      requestAnimationFrame(frame);
    };
    const observer = new IntersectionObserver((entries, obs) => entries.forEach((entry) => { if (entry.isIntersecting) { animate(entry.target); obs.unobserve(entry.target); } }), { threshold: 0.35 });
    counters.forEach((counter) => observer.observe(counter));
  });

  if (window.document$?.subscribe) window.document$.subscribe(initializeHome);
})();
