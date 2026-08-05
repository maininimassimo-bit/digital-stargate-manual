(() => {
  'use strict';

  const VERSION = '1.0.0-rc2';
  const API_VERSION = '1';
  const ID_PATTERN = /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;
  const VERSION_PATTERN = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/;
  const plugins = new Map();
  const capabilityIndex = new Map();

  const events = () => window.DSG?.events || null;

  const emit = (type, detail = {}) => {
    events()?.emit(`plugin-${type}`, {
      registryVersion: VERSION,
      apiVersion: API_VERSION,
      ...detail
    });
  };

  const normalizeStringArray = (value, field, pluginId) => {
    if (value == null) return Object.freeze([]);
    if (!Array.isArray(value)) {
      throw new TypeError(`Plugin ${pluginId}: ${field} must be an array`);
    }

    const normalized = value.map((item) => {
      if (typeof item !== 'string' || !item.trim()) {
        throw new TypeError(`Plugin ${pluginId}: ${field} entries must be non-empty strings`);
      }
      return item.trim();
    });

    if (new Set(normalized).size !== normalized.length) {
      throw new TypeError(`Plugin ${pluginId}: ${field} contains duplicate entries`);
    }

    return Object.freeze(normalized);
  };

  const validateManifest = (manifest) => {
    if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
      throw new TypeError('Plugin manifest must be an object');
    }

    const id = typeof manifest.id === 'string' ? manifest.id.trim() : '';
    if (!ID_PATTERN.test(id)) {
      throw new TypeError('Plugin id must use lowercase kebab-case');
    }

    const version = typeof manifest.version === 'string' ? manifest.version.trim() : '';
    if (!VERSION_PATTERN.test(version)) {
      throw new TypeError(`Plugin ${id}: version must follow semantic versioning`);
    }

    const apiVersion = String(manifest.apiVersion || '').trim();
    if (apiVersion !== API_VERSION) {
      throw new TypeError(`Plugin ${id}: unsupported apiVersion ${apiVersion || '(missing)'}`);
    }

    if (typeof manifest.initialize !== 'function') {
      throw new TypeError(`Plugin ${id}: initialize(context) is required`);
    }

    const capabilities = normalizeStringArray(manifest.capabilities, 'capabilities', id);
    const dependencies = normalizeStringArray(manifest.dependencies, 'dependencies', id);

    if (dependencies.includes(id)) {
      throw new TypeError(`Plugin ${id}: a plugin cannot depend on itself`);
    }

    return Object.freeze({
      id,
      version,
      apiVersion,
      capabilities,
      dependencies,
      initialize: manifest.initialize,
      dispose: typeof manifest.dispose === 'function' ? manifest.dispose : null,
      metadata: Object.freeze({
        name: typeof manifest.name === 'string' && manifest.name.trim() ? manifest.name.trim() : id,
        description: typeof manifest.description === 'string' ? manifest.description.trim() : '',
        provider: typeof manifest.provider === 'string' ? manifest.provider.trim() : '',
        experimental: manifest.experimental === true
      })
    });
  };

  const sameDefinition = (left, right) => (
    left.id === right.id &&
    left.version === right.version &&
    left.apiVersion === right.apiVersion &&
    left.initialize === right.initialize &&
    left.dispose === right.dispose &&
    left.capabilities.join('|') === right.capabilities.join('|') &&
    left.dependencies.join('|') === right.dependencies.join('|')
  );

  const indexCapabilities = (definition) => {
    definition.capabilities.forEach((capability) => {
      const ids = capabilityIndex.get(capability) || new Set();
      ids.add(definition.id);
      capabilityIndex.set(capability, ids);
    });
  };

  const register = (manifest) => {
    let definition;

    try {
      definition = validateManifest(manifest);
    } catch (error) {
      emit('registration-rejected', { message: error.message });
      throw error;
    }

    const existing = plugins.get(definition.id);
    if (existing) {
      if (sameDefinition(existing.definition, definition)) {
        emit('registration-idempotent', {
          id: definition.id,
          version: definition.version
        });
        return existing.definition;
      }

      const error = new Error(`Plugin ${definition.id} is already registered with a different definition`);
      emit('registration-rejected', { id: definition.id, message: error.message });
      throw error;
    }

    const entry = {
      definition,
      state: 'registered',
      registeredAt: new Date().toISOString(),
      lastCycle: 0,
      error: null
    };

    plugins.set(definition.id, entry);
    indexCapabilities(definition);

    emit('registered', {
      id: definition.id,
      version: definition.version,
      capabilities: definition.capabilities,
      dependencies: definition.dependencies
    });

    return definition;
  };

  const has = (id) => plugins.has(id);

  const get = (id) => plugins.get(id)?.definition || null;

  const list = () => Object.freeze(
    [...plugins.values()]
      .map((entry) => Object.freeze({
        id: entry.definition.id,
        version: entry.definition.version,
        apiVersion: entry.definition.apiVersion,
        capabilities: entry.definition.capabilities,
        dependencies: entry.definition.dependencies,
        metadata: entry.definition.metadata,
        state: entry.state,
        registeredAt: entry.registeredAt,
        lastCycle: entry.lastCycle
      }))
      .sort((left, right) => left.id.localeCompare(right.id))
  );

  const findByCapability = (capability) => Object.freeze(
    [...(capabilityIndex.get(capability) || [])]
      .sort()
      .map((id) => plugins.get(id).definition)
  );

  const capabilities = () => Object.freeze(
    [...capabilityIndex.entries()]
      .map(([name, ids]) => Object.freeze({
        name,
        plugins: Object.freeze([...ids].sort())
      }))
      .sort((left, right) => left.name.localeCompare(right.name))
  );

  const status = () => Object.freeze({
    version: VERSION,
    apiVersion: API_VERSION,
    pluginCount: plugins.size,
    capabilityCount: capabilityIndex.size,
    plugins: list(),
    capabilities: capabilities()
  });

  const registry = Object.freeze({
    version: VERSION,
    apiVersion: API_VERSION,
    register,
    validate: validateManifest,
    has,
    get,
    list,
    findByCapability,
    capabilities,
    status
  });

  window.DSGPluginRegistry = registry;

  const initialize = ({ events: eventBus } = {}) => {
    eventBus?.emit('plugin-registry-ready', {
      version: VERSION,
      apiVersion: API_VERSION,
      capabilities: [
        'manifest-validation',
        'idempotent-registration',
        'duplicate-detection',
        'capability-discovery'
      ]
    });
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'plugin-registry',
      order: 55,
      initialize
    });
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  } else {
    initialize();
  }
})();
