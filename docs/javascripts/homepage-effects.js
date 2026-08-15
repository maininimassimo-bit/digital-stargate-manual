(() => {
  'use strict';

  const resolveSiteRoot = () => {
    const logo = document.querySelector('.md-header__button.md-logo');
    return logo ? new URL(logo.href, document.baseURI) : new URL('./', document.baseURI);
  };

  const ensureLatestObservationShowcase = () => {
    const home = document.querySelector('.dsg-enterprise-home');
    if (!home || home.querySelector('.dsg-showcase__media')) return;

    const domainSection = home.querySelector('.dsg-domain-section');
    const section = document.createElement('section');
    section.className = 'dsg-showcase dsg-program-section';
    section.setAttribute('aria-label', 'Ultima osservazione astronomica');
    section.innerHTML = `
      <div class="dsg-section-intro">
        <span class="dsg-section-kicker">ULTIMA OSSERVAZIONE</span>
        <h2>Vista astronomica governata</h2>
      </div>
      <div class="dsg-showcase__layout">
        <div class="dsg-showcase__media" aria-label="Mappa dinamica dell'ultima osservazione astronomica"></div>
        <div class="dsg-showcase__content">
          <span class="dsg-section-kicker">SCIENTIFIC SNAPSHOT</span>
          <h2>Ultima osservazione</h2>
          <p>La mappa Aladin Lite è centrata sulle coordinate pubblicate dalla projection governata <code>latest-observation.json</code>.</p>
          <div class="dsg-showcase__metrics">
            <div><span>Integrazione</span><strong>—</strong></div>
            <div><span>Light</span><strong>—</strong></div>
            <div><span>RMS</span><strong>—</strong></div>
          </div>
          <a class="md-button" href="./scientific-session-catalog/">Apri Session Explorer</a>
        </div>
      </div>`;

    if (domainSection) home.insertBefore(section, domainSection);
    else home.appendChild(section);
  };

  // MkDocs loads homepage-effects.js before latest-observation.js. Mount the
  // showcase immediately so the latest-observation component always finds its
  // DOM target during component initialization; DOMContentLoaded remains as a
  // defensive retry for alternate loading paths.
  ensureLatestObservationShowcase();

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest?.('[data-dsg-search]');
    if (!trigger) return;

    event.preventDefault();
    event.stopImmediatePropagation();

    const destination = new URL('documentation/#enterprise-search-center', resolveSiteRoot());
    window.location.assign(destination.href);
  }, true);

  document.addEventListener('DOMContentLoaded', () => {
    ensureLatestObservationShowcase();

    const counters = document.querySelectorAll('.dsg-counter');

    if (!counters.length || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      counters.forEach((counter) => {
        const value = Number(counter.dataset.value || 0);
        const decimals = Number(counter.dataset.decimals || 0);
        const suffix = counter.dataset.suffix || '';
        counter.textContent = value.toLocaleString('it-IT', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        }) + suffix;
      });
      return;
    }

    const animate = (counter) => {
      const target = Number(counter.dataset.value || 0);
      const decimals = Number(counter.dataset.decimals || 0);
      const suffix = counter.dataset.suffix || '';
      const duration = 900;
      const start = performance.now();

      const frame = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;

        counter.textContent = current.toLocaleString('it-IT', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        }) + suffix;

        if (progress < 1) requestAnimationFrame(frame);
      };

      requestAnimationFrame(frame);
    };

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.35 });

    counters.forEach((counter) => observer.observe(counter));
  });
})();
