(() => {
  'use strict';

  const rootUrl = () => {
    const logo = document.querySelector('.md-header__button.md-logo');
    return logo ? new URL(logo.href, document.baseURI) : new URL('./', document.baseURI);
  };

  const href = (path = '') => new URL(path, rootUrl()).href;
  const normalize = (value) => new URL(value, document.baseURI).pathname
    .replace(/index\.html$/, '')
    .replace(/\/+$/, '');

  const ensureNavigationStyles = () => {
    if (document.querySelector('link[data-dsg-enterprise-navigation]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href('styles/enterprise-navigation.css');
    link.dataset.dsgEnterpriseNavigation = 'true';
    document.head.appendChild(link);
  };

  const openSearch = (query = '') => {
    document.querySelector('label[for="__search"]')?.click();
    window.setTimeout(() => {
      const input = document.querySelector('.md-search__input');
      if (!input) return;
      input.value = query;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.focus();
    }, 80);
  };

  const drawerGroup = (title, links) => `
    <section class="dsg-docs-drawer__group">
      <strong>${title}</strong>
      ${links.map(([label, path]) => `<a href="${href(path)}"><span>${label}</span><span aria-hidden="true">→</span></a>`).join('')}
    </section>`;

  const drawerMarkup = () => `
    <div class="dsg-docs-backdrop" data-dsg-docs-backdrop></div>
    <aside class="dsg-docs-drawer" aria-label="Navigazione completa" aria-hidden="true" inert data-dsg-docs-drawer>
      <div class="dsg-docs-drawer__header">
        <strong>Esplora Digital StarGate</strong>
        <button class="dsg-docs-drawer__close" type="button" data-dsg-docs-close aria-label="Chiudi navigazione">×</button>
      </div>
      <button class="dsg-docs-drawer__search" type="button" data-dsg-drawer-search>Cerca in tutta la documentazione…</button>
      ${drawerGroup('OSSERVATORIO', [
        ['Mission Control', 'mission-control/'],
        ['Stato osservatorio', 'status/'],
        ['Catalogo sessioni', 'scientific-session-catalog/'],
        ['Report sessioni', 'session-reports/']
      ])}
      ${drawerGroup('SCIENZA E ANALYTICS', [
        ['Scientific Platform', 'scientific-platform/'],
        ['Analytics Center', 'analytics/'],
        ['Session Comparison', 'session-comparison/'],
        ['Anomaly & Trend', 'anomaly-trend-center/'],
        ['Equipment Performance', 'equipment-performance/']
      ])}
      ${drawerGroup('OPERATIONS E CONOSCENZA', [
        ['Operations Center', 'operations/'],
        ['Architecture Center', 'architecture/'],
        ['Documentation Center', 'documentation/'],
        ['Roadmap', 'roadmap/'],
        ['Governance Center', 'project/'],
        ['Manuale tecnico', 'chapters/01-introduzione/']
      ])}
    </aside>`;

  const updateActiveLinks = (navigation) => {
    const current = normalize(window.location.href);
    navigation.querySelectorAll('.dsg-enterprise-nav__link').forEach((link) => {
      const active = normalize(link.href) === current
        || (normalize(link.href) !== normalize(href()) && current.startsWith(`${normalize(link.href)}/`));
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  };

  const refreshCurrentPackage = async (navigation) => {
    const label = navigation.querySelector('[data-dsg-current-package]');
    if (!label) return;
    try {
      const response = await fetch(href('data/roadmap.json'), { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const roadmap = await response.json();
      label.textContent = roadmap.currentPackage || 'Roadmap';
      label.title = roadmap.nextMilestone || 'Package corrente';
    } catch {
      label.textContent = 'Roadmap';
      label.title = 'Projection roadmap non disponibile';
    }
  };

  const buildNavigation = () => {
    ensureNavigationStyles();
    const header = document.querySelector('.md-header');
    if (!header) return;

    let navigation = header.querySelector('.dsg-enterprise-nav');
    if (!navigation) {
      const nativeLogo = document.querySelector('.md-header__button.md-logo');
      const logoSource = nativeLogo?.querySelector('img')?.src || href('assets/images/dsg-logo.svg');

      navigation = document.createElement('nav');
      navigation.className = 'dsg-enterprise-nav';
      navigation.setAttribute('aria-label', 'Navigazione principale');
      navigation.innerHTML = `
        <a class="dsg-enterprise-nav__brand" href="${href()}">
          <img src="${logoSource}" alt="">
          <div><strong>DIGITAL STARGATE</strong><small>MANCIANO OBSERVATORY</small></div>
        </a>
        <div class="dsg-enterprise-nav__links">
          <a class="dsg-enterprise-nav__link" href="${href('mission-control/')}">Osservatorio</a>
          <a class="dsg-enterprise-nav__link" href="${href('scientific-platform/')}">Scienza</a>
          <a class="dsg-enterprise-nav__link" href="${href('analytics/')}">Analytics</a>
          <a class="dsg-enterprise-nav__link" href="${href('operations/')}">Operations</a>
          <a class="dsg-enterprise-nav__link" href="${href('architecture/')}">Architettura</a>
          <a class="dsg-enterprise-nav__link" href="${href('roadmap/')}">Roadmap</a>
        </div>
        <div class="dsg-enterprise-nav__utilities">
          <span class="dsg-enterprise-nav__current" data-dsg-current-package aria-label="Package corrente">…</span>
          <button class="dsg-enterprise-nav__action" type="button" data-dsg-search aria-label="Cerca"><span>Cerca</span> ⌕</button>
          <button class="dsg-enterprise-nav__action" type="button" data-dsg-theme aria-label="Cambia tema"><span>Tema</span> ◐</button>
          <button class="dsg-enterprise-nav__action" type="button" data-dsg-docs aria-expanded="false"><span>Esplora</span> ☰</button>
        </div>`;
      header.appendChild(navigation);
      document.body.insertAdjacentHTML('beforeend', drawerMarkup());

      const drawer = document.querySelector('[data-dsg-docs-drawer]');
      const backdrop = document.querySelector('[data-dsg-docs-backdrop]');
      const trigger = navigation.querySelector('[data-dsg-docs]');
      let returnFocus = null;

      const setDrawer = (open) => {
        if (!drawer || !backdrop || !trigger) return;
        drawer.classList.toggle('is-open', open);
        backdrop.classList.toggle('is-open', open);
        drawer.setAttribute('aria-hidden', String(!open));
        drawer.toggleAttribute('inert', !open);
        trigger.setAttribute('aria-expanded', String(open));
        document.body.style.overflow = open ? 'hidden' : '';
        if (open) {
          returnFocus = document.activeElement;
          drawer.querySelector('[data-dsg-docs-close]')?.focus();
        } else if (returnFocus instanceof HTMLElement) {
          returnFocus.focus();
        }
      };

      trigger?.addEventListener('click', () => setDrawer(true));
      drawer?.querySelector('[data-dsg-docs-close]')?.addEventListener('click', () => setDrawer(false));
      backdrop?.addEventListener('click', () => setDrawer(false));
      drawer?.querySelector('[data-dsg-drawer-search]')?.addEventListener('click', () => {
        setDrawer(false);
        openSearch();
      });
      drawer?.addEventListener('click', (event) => {
        if (event.target.closest('a')) setDrawer(false);
      });
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && drawer?.classList.contains('is-open')) setDrawer(false);
      });
      navigation.querySelector('[data-dsg-search]')?.addEventListener('click', () => openSearch());
      refreshCurrentPackage(navigation);
    }

    updateActiveLinks(navigation);
  };

  const addBreadcrumb = () => {
    const content = document.querySelector('.md-content__inner');
    if (!content || content.querySelector('.dsg-breadcrumb')) return;
    const heading = content.querySelector(':scope > h1');
    if (!heading || content.querySelector('.dsg-hero')) return;

    const relativePath = normalize(window.location.href)
      .replace(normalize(href()), '')
      .replace(/^\//, '');
    const segments = relativePath.split('/').filter(Boolean);
    if (!segments.length) return;

    const breadcrumb = document.createElement('nav');
    breadcrumb.className = 'dsg-breadcrumb';
    breadcrumb.setAttribute('aria-label', 'Percorso pagina');
    breadcrumb.innerHTML = `<a href="${href()}">Home</a><span aria-hidden="true">/</span><span aria-current="page">${heading.textContent.trim()}</span>`;
    content.insertBefore(breadcrumb, heading);
  };

  const addPageNavigation = () => {
    const content = document.querySelector('.md-content__inner');
    if (!content || content.querySelector('.dsg-page-nav')) return;

    const navLinks = [...document.querySelectorAll('.md-nav--primary a.md-nav__link')]
      .filter((link) => {
        const value = link.getAttribute('href');
        return value && !value.startsWith('#') && link.textContent.trim();
      });
    const current = normalize(window.location.href);
    const index = navLinks.findIndex((link) => normalize(link.href) === current);
    if (index < 0) return;

    const previous = navLinks[index - 1];
    const next = navLinks[index + 1];
    if (!previous && !next) return;

    const pageNav = document.createElement('nav');
    pageNav.className = 'dsg-page-nav';
    pageNav.setAttribute('aria-label', 'Navigazione tra le pagine');

    const card = (link, label, arrow) => {
      const element = document.createElement('a');
      element.href = link.href;
      element.innerHTML = `<span class="dsg-page-nav__label">${arrow === 'left' ? '← ' : ''}${label}${arrow === 'right' ? ' →' : ''}</span><span class="dsg-page-nav__title"></span>`;
      element.querySelector('.dsg-page-nav__title').textContent = link.textContent.trim();
      return element;
    };

    if (previous) pageNav.appendChild(card(previous, 'Pagina precedente', 'left'));
    if (next) pageNav.appendChild(card(next, 'Pagina successiva', 'right'));
    content.appendChild(pageNav);
  };

  const initialize = () => {
    buildNavigation();
    addBreadcrumb();
    addPageNavigation();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }
  if (window.document$?.subscribe) window.document$.subscribe(initialize);
})();

