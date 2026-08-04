(() => {
  const loadEnterpriseStyles = () => {
    if (document.querySelector('link[data-dsg-enterprise-navigation]')) return;
    const anchor = [...document.querySelectorAll('link[rel="stylesheet"]')]
      .find((link) => /styles\/extra\.css(?:\?|$)/.test(link.href));
    if (!anchor) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = anchor.href.replace(/extra\.css(?:\?.*)?$/, 'enterprise-navigation.css');
    link.dataset.dsgEnterpriseNavigation = 'true';
    document.head.appendChild(link);
  };

  const loadThemeManager = () => {
    if (document.querySelector('script[data-dsg-theme-manager]')) return;
    const currentScript = [...document.scripts]
      .find((script) => /javascripts\/page-enhancements\.js(?:\?|$)/.test(script.src));
    if (!currentScript) return;
    const script = document.createElement('script');
    script.src = currentScript.src.replace(/page-enhancements\.js(?:\?.*)?$/, 'dsg-theme-manager.js');
    script.defer = true;
    script.dataset.dsgThemeManager = 'true';
    document.head.appendChild(script);
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

  const menuItem = (label, links, href) => {
    const groups = [];
    for (let index = 0; index < links.length; index += 2) {
      groups.push(`<div class="dsg-mega-menu__group"><strong>${index === 0 ? label.toUpperCase() : 'RISORSE'}</strong>${links.slice(index, index + 2).map(([title, path]) => `<a href="${href(path)}">${title}</a>`).join('')}</div>`);
    }
    return `<div class="dsg-enterprise-nav__item"><button class="dsg-enterprise-nav__action" type="button" data-dsg-menu aria-expanded="false">${label}⌄</button><div class="dsg-mega-menu">${groups.join('')}</div></div>`;
  };

  const drawerMarkup = (href) => `
    <div class="dsg-docs-backdrop"></div>
    <aside class="dsg-docs-drawer" aria-label="Tutta la documentazione">
      <div class="dsg-docs-drawer__header"><strong>TUTTA LA DOCUMENTAZIONE</strong><button class="dsg-docs-drawer__close" type="button" data-dsg-docs-close aria-label="Chiudi">×</button></div>
      <button class="dsg-docs-drawer__search" type="button" data-dsg-drawer-search>⌕ Cerca nella documentazione…</button>
      <div class="dsg-docs-drawer__filters" aria-label="Ricerche guidate">
        <button type="button" data-dsg-query="AP-">Architecture Package</button>
        <button type="button" data-dsg-query="ADR-">ADR</button>
        <button type="button" data-dsg-query="ARB-">Assessment</button>
        <button type="button" data-dsg-query="SOP">SOP</button>
        <button type="button" data-dsg-query="DSDM">Scientific Platform</button>
      </div>
      <div class="dsg-docs-drawer__links">
        <a href="${href()}"><span>⌂ Home</span><span>›</span></a>
        <a href="${href('mission-control/')}"><span>◉ Mission Control</span><span>›</span></a>
        <a href="${href('documentation/')}"><span>▤ Documentation Center</span><span>›</span></a>
        <a href="${href('roadmap/')}"><span>⚑ Roadmap Center</span><span>›</span></a>
        <a href="${href('architecture/')}"><span>◇ Architecture Center</span><span>›</span></a>
        <a href="${href('scientific-platform/')}"><span>♢ Scientific Platform</span><span>›</span></a>
        <a href="${href('scientific-session-catalog/')}"><span>✦ Session Explorer</span><span>›</span></a>
        <a href="${href('operations/')}"><span>⚙ Operations Center</span><span>›</span></a>
        <a href="${href('repository-intelligence/')}"><span>◎ Repository Intelligence</span><span>›</span></a>
        <a href="${href('repository-analytics/')}"><span>⌁ Repository Analytics</span><span>›</span></a>
        <a href="${href('scientific-platform-intelligence/')}"><span>✦ Scientific Intelligence</span><span>›</span></a>
        <a href="${href('analytics/')}"><span>▥ Analytics Center</span><span>›</span></a>
        <a href="${href('developer/development-guide/')}"><span>&lt;/&gt; Developer</span><span>›</span></a>
        <a href="${href('chapters/01-introduzione/')}"><span>◫ Manuale tecnico</span><span>›</span></a>
      </div>
    </aside>`;

  const buildEnterpriseNavigation = () => {
    const header = document.querySelector('.md-header');
    if (!header || header.querySelector('.dsg-enterprise-nav')) return;

    const nativeLogo = document.querySelector('.md-header__button.md-logo');
    const rootUrl = nativeLogo ? new URL(nativeLogo.href, document.baseURI) : new URL('./', document.baseURI);
    const href = (path = '') => new URL(path, rootUrl).href;
    const logoSource = nativeLogo?.querySelector('img')?.src || href('assets/images/dsg-logo.svg');

    const navigation = document.createElement('nav');
    navigation.className = 'dsg-enterprise-nav';
    navigation.setAttribute('aria-label', 'Navigazione principale Digital StarGate');
    navigation.innerHTML = `
      <a class="dsg-enterprise-nav__brand" href="${href()}">
        <img src="${logoSource}" alt="Logo Digital StarGate">
        <div><strong>DIGITAL STARGATE</strong><span>DOCUMENTATION PORTAL</span></div>
      </a>
      <div class="dsg-enterprise-nav__links">
        <a class="dsg-enterprise-nav__link" href="${href()}">Home</a>
        <a class="dsg-enterprise-nav__link" href="${href('mission-control/')}">Mission Control</a>
        ${menuItem('Programma', [
          ['Documentation Center', 'documentation/'],
          ['Roadmap Center', 'roadmap/'],
          ['Architecture Package', 'architecture/packages/AP-013-Scientific-Image-Repository-Architecture/'],
          ['Release Notes', 'releases/release-1.5-developer-edition/']
        ], href)}
        ${menuItem('Architettura', [
          ['Architecture Center', 'architecture/'],
          ['Decisioni ADR', 'architecture/ADR-001-Session-Layer/'],
          ['Assessment', 'architecture/assessments/ARB-012-AP-012-Independent-Architecture-Review/'],
          ['Validation e Review', 'architecture/validation/'],
          ['Governance e Metamodel', 'architecture/enterprise-metamodel/'],
          ['Traceability', 'architecture/traceability-register/']
        ], href)}
        ${menuItem('Scientific Platform', [
          ['Scientific Platform Center', 'scientific-platform/'],
          ['Session Explorer', 'scientific-session-catalog/'],
          ['Scientific Intelligence', 'scientific-platform-intelligence/'],
          ['AP-013 Scientific Repository', 'architecture/packages/AP-013-Scientific-Image-Repository-Architecture/'],
          ['Scientific Data Manager', 'architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model/'],
          ['Transfer Readiness', 'architecture/validation/AP-013-Transfer-Readiness-Gate/']
        ], href)}
        ${menuItem('Operations', [
          ['Operations Center', 'operations/'],
          ['Observatory Status', 'status/'],
          ['Automazione', 'chapters/15-automazione/'],
          ['Procedure operative', 'chapters/16-sop-avvio/'],
          ['Sicurezza e recovery', 'chapters/18-emergenze-recovery/'],
          ['Infrastructure', 'chapters/05-infrastruttura-rete/']
        ], href)}
        ${menuItem('Intelligence', [
          ['Repository Intelligence', 'repository-intelligence/'],
          ['Repository Analytics', 'repository-analytics/'],
          ['Analytics Center', 'analytics/'],
          ['Dashboard integrate', 'analytics/dashboard-integrated/'],
          ['Qualità e storico', 'analytics/history-validation/'],
          ['Developer Guide', 'developer/development-guide/']
        ], href)}
      </div>
      <div class="dsg-enterprise-nav__utilities">
        <button class="dsg-enterprise-nav__action" type="button" data-dsg-search>⌕ Cerca</button>
        <a class="dsg-enterprise-nav__action" href="https://github.com/maininimassimo-bit/digital-stargate-manual">◉ GitHub</a>
        <button class="dsg-enterprise-nav__action" type="button" data-dsg-theme>◐ Tema</button>
        <button class="dsg-enterprise-nav__action dsg-enterprise-nav__docs" type="button" data-dsg-docs>☰ Documentazione</button>
      </div>`;

    header.appendChild(navigation);
    document.body.insertAdjacentHTML('beforeend', drawerMarkup(href));

    const currentPath = window.location.pathname.replace(/\/+$/, '');
    [...navigation.querySelectorAll('a.dsg-enterprise-nav__link')].forEach((link) => {
      if (new URL(link.href).pathname.replace(/\/+$/, '') === currentPath) link.classList.add('is-active');
    });

    navigation.querySelectorAll('[data-dsg-menu]').forEach((button) => {
      button.addEventListener('click', (event) => {
        event.stopPropagation();
        const item = button.closest('.dsg-enterprise-nav__item');
        navigation.querySelectorAll('.dsg-enterprise-nav__item.is-open').forEach((open) => {
          if (open !== item) open.classList.remove('is-open');
        });
        item.classList.toggle('is-open');
        button.setAttribute('aria-expanded', item.classList.contains('is-open'));
      });
    });

    document.addEventListener('click', () => navigation.querySelectorAll('.dsg-enterprise-nav__item.is-open').forEach((item) => item.classList.remove('is-open')));
    navigation.querySelector('[data-dsg-search]')?.addEventListener('click', () => openSearch());

    const drawer = document.querySelector('.dsg-docs-drawer');
    const backdrop = document.querySelector('.dsg-docs-backdrop');
    const setDrawer = (open) => {
      drawer?.classList.toggle('is-open', open);
      backdrop?.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };

    navigation.querySelector('[data-dsg-docs]')?.addEventListener('click', () => setDrawer(true));
    drawer?.querySelector('[data-dsg-docs-close]')?.addEventListener('click', () => setDrawer(false));
    backdrop?.addEventListener('click', () => setDrawer(false));
    drawer?.querySelector('[data-dsg-drawer-search]')?.addEventListener('click', () => {
      setDrawer(false);
      openSearch();
    });
    drawer?.querySelectorAll('[data-dsg-query]').forEach((button) => {
      button.addEventListener('click', () => {
        setDrawer(false);
        openSearch(button.dataset.dsgQuery || '');
      });
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') setDrawer(false);
    });
  };

  loadEnterpriseStyles();
  loadThemeManager();
  document.addEventListener('DOMContentLoaded', buildEnterpriseNavigation);
  if (typeof document$ !== 'undefined') document$.subscribe(buildEnterpriseNavigation);
})();

document.addEventListener("DOMContentLoaded", () => {
  const content = document.querySelector(".md-content__inner");
  if (!content) return;

  const firstHeading = content.querySelector(":scope > h1");
  if (!firstHeading || document.querySelector(".dsg-hero")) return;

  const pathParts = window.location.pathname
    .split("/")
    .filter(Boolean)
    .map((part) => decodeURIComponent(part).replace(/[-_]/g, " "));

  const breadcrumb = document.createElement("nav");
  breadcrumb.className = "dsg-breadcrumb";
  breadcrumb.setAttribute("aria-label", "Percorso pagina");

  const home = document.createElement("a");
  home.href = new URL("./", document.baseURI).href;
  home.textContent = "Home";
  breadcrumb.appendChild(home);

  pathParts.slice(-2).forEach((part, index, parts) => {
    const sep = document.createElement("span");
    sep.className = "dsg-breadcrumb__sep";
    sep.textContent = "›";
    breadcrumb.appendChild(sep);

    const label = document.createElement("span");
    label.textContent = index === parts.length - 1
      ? firstHeading.textContent.trim()
      : part.replace(/\b\w/g, (letter) => letter.toUpperCase());
    breadcrumb.appendChild(label);
  });

  content.insertBefore(breadcrumb, firstHeading);

  const navLinks = [...document.querySelectorAll(".md-nav--primary a.md-nav__link")]
    .filter((link) => {
      const href = link.getAttribute("href");
      return href && !href.startsWith("#") && link.textContent.trim();
    });

  const normalize = (url) => {
    const parsed = new URL(url, document.baseURI);
    return parsed.pathname.replace(/index\.html$/, "").replace(/\/+$/, "");
  };

  const currentPath = normalize(window.location.href);
  const currentIndex = navLinks.findIndex((link) => normalize(link.href) === currentPath);
  if (currentIndex === -1) return;

  const previous = navLinks[currentIndex - 1];
  const next = navLinks[currentIndex + 1];
  if (!previous && !next) return;

  const pageNav = document.createElement("nav");
  pageNav.className = "dsg-page-nav";
  pageNav.setAttribute("aria-label", "Navigazione tra le pagine");

  const createCard = (link, label, direction) => {
    const card = document.createElement("a");
    card.href = link.href;
    const small = document.createElement("span");
    small.className = "dsg-page-nav__label";
    small.textContent = direction === "previous" ? `← ${label}` : `${label} →`;
    const title = document.createElement("span");
    title.className = "dsg-page-nav__title";
    title.textContent = link.textContent.trim();
    card.append(small, title);
    return card;
  };

  if (previous) pageNav.appendChild(createCard(previous, "Pagina precedente", "previous"));
  if (next) pageNav.appendChild(createCard(next, "Pagina successiva", "next"));
  content.appendChild(pageNav);
});
