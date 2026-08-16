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
      <div class="dsg-showcase__layout">
        <div class="dsg-showcase__media" aria-label="Mappa dinamica dell'ultima osservazione astronomica"></div>
        <aside class="dsg-showcase__content" aria-label="Coordinate dell'ultima osservazione">
          <span class="dsg-section-kicker">SCIENTIFIC SNAPSHOT</span>
          <h2>Ultima osservazione</h2>
          <div class="dsg-showcase__sky-panel dsg-showcase__coordinate-panel">
            <div class="dsg-showcase__sky-meta">
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

  ensureLatestObservationShowcase();

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest?.('[data-dsg-search]');
    if (!trigger) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    window.location.assign(new URL('documentation/#enterprise-search-center', resolveSiteRoot()).href);
  }, true);

  document.addEventListener('DOMContentLoaded', () => {
    ensureLatestObservationShowcase();
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
})();
