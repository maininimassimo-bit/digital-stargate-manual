(() => {
  'use strict';

  const VERSION = '1.0.0-rc2';
  const runtimeState = new Map();
  let runtimeCycle = 0;

  const coreEvents = () => window.DSG?.events || null;

  const emit = (type, detail = {}) => {
    coreEvents()?.emit(`plugin-runtime-${type}`, {
      runtimeVersion: VERSION,
      runtimeCycle,
      ...detail
    });
  };

  const loggerFor = (pluginId) => Object.freeze({
    debug(message, detail) {
      console.debug(`[DSG Plugin:${pluginId}] ${message}`, detail ?? '');
    },
    info(message, detail) {
      console.info(`[DSG Plugin:${pluginId}] ${message}`, detail ?? '');
    },
    warn(message, detail) {
      console.warn(`[DSG Plugin:${pluginId}] ${message}`, detail ?? '');
    },
    error(message, detail) {
      console.error(`[DSG Plugin:${pluginId}] ${message}`, detail ?? '');
    }
  });

  const serviceCatalog = () => Object.freeze({
    scientific: window.DSGScientificDataEngine || null,
    search: window.DSGSearchService || null,
    operations: window.DSGOperationsService || null,
    theme: window.DSGThemeService || null,
    plugins: window.DSGPluginRegistry || null
  });

  const buildContext = (definition, source) => Object.freeze({
    cycle: runtimeCycle,
    source,
    root: document,
    events: coreEvents(),
    components: window.DSG?.components || null,
    services: serviceCatalog(),
    plugin: Object.freeze({
      id: definition.id,
      version: definition.version,
      apiVersion: definition.apiVersion,
      capabilities: definition.capabilities,
      dependencies: definition.dependencies,
      metadata: definition.metadata
    }),
    logger: loggerFor(definition.id)
  });

  const getEntry = (id) => {
    if (!runtimeState.has(id)) {
      runtimeState.set(id, {
        state: 'registered',
        initializedAt: null,
        disposedAt: null,
        lastCycle: 0,
        cleanup: null,
        error: null
      });
    }
    return runtimeState.get(id);
  };

  const initializePlugin = async (definition, source) => {
    const entry = getEntry(definition.id);
    if (entry.lastCycle === runtimeCycle && entry.state === 'ready') return;

    entry.state = 'initializing';
    entry.error = null;
    emit('initialize-start', { id: definition.id, version: definition.version, source });

    try {
      const result = await definition.initialize(buildContext(definition, source));
      entry.cleanup = typeof result === 'function' ? result : null;
      entry.state = 'ready';
      entry.initializedAt = new Date().toISOString();
      entry.lastCycle = runtimeCycle;
      emit('initialize-ready', { id: definition.id, version: definition.version, source });
    } catch (error) {
      entry.state = 'error';
      entry.error = error;
      entry.lastCycle = runtimeCycle;
      console.error(`Digital StarGate plugin failed during initialize: ${definition.id}`, error);
      emit('initialize-error', {
        id: definition.id,
        version: definition.version,
        source,
        message: error.message
      });
    }
  };

  const disposePlugin = async (definition, source) => {
    const entry = getEntry(definition.id);
    if (!['ready', 'error'].includes(entry.state) && !entry.cleanup) return;

    entry.state = 'disposing';
    emit('dispose-start', { id: definition.id, version: definition.version, source });

    try {
      if (typeof entry.cleanup === 'function') {
        await entry.cleanup();
      }
      if (typeof definition.dispose === 'function') {
        await definition.dispose(buildContext(definition, source));
      }
      entry.cleanup = null;
      entry.state = 'disposed';
      entry.disposedAt = new Date().toISOString();
      entry.error = null;
      emit('dispose-ready', { id: definition.id, version: definition.version, source });
    } catch (error) {
      entry.state = 'dispose-error';
      entry.error = error;
      console.error(`Digital StarGate plugin failed during dispose: ${definition.id}`, error);
      emit('dispose-error', {
        id: definition.id,
        version: definition.version,
        source,
        message: error.message
      });
    }
  };

  const resolveDefinitions = (selection) => {
    const registry = window.DSGPluginRegistry;
    const resolver = window.DSGPluginDependencyResolver;
    if (!registry) throw new Error('DSGPluginRegistry is not available');
    if (!resolver) throw new Error('DSGPluginDependencyResolver is not available');

    return resolver.resolve(selection).map((id) => {
      const definition = registry.get(id);
      if (!definition) throw new Error(`Plugin ${id} disappeared after dependency resolution`);
      return definition;
    });
  };

  const run = async (selection, source = 'manual') => {
    runtimeCycle += 1;
    const definitions = resolveDefinitions(selection);

    emit('cycle-start', {
      source,
      plugins: definitions.map((definition) => definition.id)
    });

    for (const definition of definitions) {
      await initializePlugin(definition, source);
    }

    const summary = status();
    emit('cycle-ready', {
      source,
      plugins: definitions.length,
      ready: summary.ready,
      errors: summary.errors
    });

    return summary;
  };

  const dispose = async (selection, source = 'manual') => {
    const registry = window.DSGPluginRegistry;
    const resolver = window.DSGPluginDependencyResolver;
    if (!registry) throw new Error('DSGPluginRegistry is not available');
    if (!resolver) throw new Error('DSGPluginDependencyResolver is not available');

    const order = [...resolver.resolve(selection)].reverse();
    for (const id of order) {
      const definition = registry.get(id);
      if (definition) await disposePlugin(definition, source);
    }

    return status();
  };

  const status = () => {
    const entries = [...runtimeState.entries()]
      .map(([id, entry]) => Object.freeze({
        id,
        state: entry.state,
        initializedAt: entry.initializedAt,
        disposedAt: entry.disposedAt,
        lastCycle: entry.lastCycle,
        error: entry.error ? entry.error.message : null
      }))
      .sort((left, right) => left.id.localeCompare(right.id));

    return Object.freeze({
      version: VERSION,
      cycle: runtimeCycle,
      plugins: Object.freeze(entries),
      ready: entries.filter((entry) => entry.state === 'ready').length,
      errors: entries.filter((entry) => entry.state === 'error' || entry.state === 'dispose-error').length,
      disposed: entries.filter((entry) => entry.state === 'disposed').length
    });
  };

  window.DSGPluginRuntime = Object.freeze({
    version: VERSION,
    run,
    dispose,
    status
  });

  const initialize = ({ events } = {}) => {
    events?.emit('plugin-runtime-ready', {
      version: VERSION,
      capabilities: [
        'dependency-aware-initialize',
        'reverse-order-dispose',
        'context-injection',
        'failure-isolation',
        'instant-navigation-lifecycle'
      ]
    });
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'plugin-runtime',
      order: 57,
      initialize,
      destroy: () => dispose(null, 'component-destroy')
    });
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  } else {
    initialize();
  }
})();
