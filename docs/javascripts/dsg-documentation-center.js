(() => {
  'use strict';

  const SCRIPT_URL = document.currentScript?.src || null;
  const SITE_ROOT = SCRIPT_URL ? new URL('../', SCRIPT_URL) : new URL('./', document.baseURI);
  const ROADMAP_URL = new URL('data/roadmap.json', SITE_ROOT);

  const setText = (root, selector, value) => {
    const node = root.querySelector(selector);
    if (node && value !== undefined && value !== null) node.textContent = String(value);
  };

  const loadRoadmap = async (root, events) => {
    try {
      const response = await fetch(ROADMAP_URL, { cache: 'no-store' });
      if (!response.ok) throw new Error(`Roadmap request failed: ${response.status}`);
      const roadmap = await response.json();
      const architecture = roadmap.waves?.find((wave) => wave.id === 'architecture-program');
      const activeArchitecture = architecture?.items?.filter((item) => item.status === 'active') || [];

      setText(root, '[data-doc-kpi-ap-count]', architecture?.items?.length || 0);
      setText(root, '[data-doc-kpi-ap-range]', architecture?.items?.length ? `AP-001 → AP-${String(architecture.items.length).padStart(3, '0')}` : 'N/D');
      setText(root, '[data-doc-kpi-current-package]', roadmap.currentPackage || 'N/D');
      setText(root, '[data-doc-kpi-current-note]', roadmap.nextMilestone || roadmap.target || 'Roadmap governata');
      setText(root, '[data-doc-kpi-active-ap]', activeArchitecture.length);

      events?.emit('documentation-center-roadmap-ready', {
        currentPackage: roadmap.currentPackage,
        architecturePackages: architecture?.items?.length || 0,
        activeArchitecturePackages: activeArchitecture.length
      });
    } catch (error) {
      console.error('Documentation Center roadmap load failed', error);
      events?.emit('documentation-center-roadmap-error', { message: error.message });
    }
  };

  const initialize = ({ events } = {}) => {
    const root = document.querySelector('[data-dsg-documentation-center]');
    if (!root || root.dataset.dsgDocumentationReady === 'true') return;

    root.dataset.dsgDocumentationReady = 'true';

    root.querySelector('[data-dsg-doc-search]')?.addEventListener('click', () => {
      document.querySelector('label[for="__search"]')?.click();
    });

    loadRoadmap(root, events);

    events?.emit('documentation-center-ready', {
      title: document.title,
      searchCenter: Boolean(root.querySelector('[data-dsg-search-center]'))
    });
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'documentation-center',
      order: 74,
      initialize
    });
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  } else {
    initialize();
  }
})();
