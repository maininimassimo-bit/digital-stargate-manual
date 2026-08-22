(() => {
  'use strict';

  const PLUGIN_ID = 'operations-health-demo';
  const HOST_SELECTOR = '[data-dsg-plugin-operations-health-demo]';

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

  const provider = Object.freeze({
    id: 'operations-health-demo-widget',

    render(context) {
      const host = context.root.querySelector(HOST_SELECTOR);
      if (!host) return null;

      const operations = context.services.operations;
      const snapshot = operations?.getSnapshot?.() || null;
      const componentTotals = snapshot?.components?.totals || {};
      const runtimeStatus = window.DSGPluginRuntime?.status?.() || {};
      const registryStatus = context.services.plugins?.status?.() || {};

      host.innerHTML = `
        <article class="dsg-operations-dashboard__panel" data-dsg-plugin-demo-rendered>
          <span>PLUGIN SDK · OPERATIONS WIDGET</span>
          <h3>${escapeHtml(context.plugin.metadata.name)}</h3>
          <p>Widget dimostrativo registrato e inizializzato tramite Enterprise Plugin SDK.</p>
          <div class="dsg-operations-boundary">
            <article><strong>Plugin</strong><span>${escapeHtml(context.plugin.id)} ${escapeHtml(context.plugin.version)}</span></article>
            <article><strong>Componenti ready</strong><span>${escapeHtml(componentTotals.ready || 0)}</span></article>
            <article><strong>Plugin registrati</strong><span>${escapeHtml(registryStatus.pluginCount || 0)}</span></article>
            <article><strong>Runtime ready</strong><span>${escapeHtml(runtimeStatus.ready || 0)}</span></article>
          </div>
        </article>`;

      return host;
    }
  });

  const manifest = {
    id: PLUGIN_ID,
    name: 'Operations Health Demo Plugin',
    description: 'Provider dimostrativo read-only per il contratto operations-widget.',
    provider: 'Digital StarGate',
    version: '1.0.0',
    apiVersion: '1',
    capabilities: ['operations-widget'],
    dependencies: [],

    initialize(context) {
      const contracts = window.DSGPluginProviderContracts;
      if (!contracts) throw new Error('DSGPluginProviderContracts is not available');

      contracts.validate('operations-widget', provider);
      const host = provider.render(context);

      context.events?.emit('plugin-demo-ready', {
        id: context.plugin.id,
        capability: 'operations-widget',
        rendered: Boolean(host),
        cycle: context.cycle
      });

      context.logger.info('Demo provider initialized', {
        rendered: Boolean(host),
        cycle: context.cycle
      });

      return () => {
        host?.querySelector('[data-dsg-plugin-demo-rendered]')?.remove();
        context.events?.emit('plugin-demo-cleanup', {
          id: context.plugin.id,
          cycle: context.cycle
        });
      };
    },

    dispose(context) {
      context.root
        .querySelector(HOST_SELECTOR)
        ?.querySelector('[data-dsg-plugin-demo-rendered]')
        ?.remove();

      context.events?.emit('plugin-demo-disposed', {
        id: context.plugin.id,
        cycle: context.cycle
      });
    }
  };

  const registerAndRun = async () => {
    const registry = window.DSGPluginRegistry;
    const runtime = window.DSGPluginRuntime;

    if (!registry) throw new Error('DSGPluginRegistry is not available');
    if (!runtime) throw new Error('DSGPluginRuntime is not available');

    registry.register(manifest);
    await runtime.run([PLUGIN_ID], 'demo-plugin-load');
  };

  registerAndRun().catch((error) => {
    console.error('Digital StarGate demo plugin failed', error);
    window.DSG?.events?.emit('plugin-demo-error', {
      id: PLUGIN_ID,
      message: error.message
    });
  });
})();
