(() => {
  'use strict';

  const initialize = ({ events } = {}) => {
    const root = document.querySelector('[data-dsg-documentation-center]');
    if (!root || root.dataset.dsgDocumentationReady === 'true') return;

    root.dataset.dsgDocumentationReady = 'true';

    root.querySelector('[data-dsg-doc-search]')?.addEventListener('click', () => {
      document.querySelector('label[for="__search"]')?.click();
    });

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
