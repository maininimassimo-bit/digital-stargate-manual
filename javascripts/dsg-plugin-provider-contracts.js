(() => {
  'use strict';

  const VERSION = '1.0.0-rc2';
  const contracts = new Map();

  const events = () => window.DSG?.events || null;

  const emit = (type, detail = {}) => {
    events()?.emit(`plugin-provider-${type}`, {
      contractsVersion: VERSION,
      ...detail
    });
  };

  const freezeContract = (definition) => Object.freeze({
    id: definition.id,
    capability: definition.capability,
    validate: definition.validate,
    describe: typeof definition.describe === 'function' ? definition.describe : null
  });

  const registerContract = (definition) => {
    if (!definition || typeof definition !== 'object') {
      throw new TypeError('Provider contract definition must be an object');
    }
    if (typeof definition.id !== 'string' || !definition.id.trim()) {
      throw new TypeError('Provider contract id is required');
    }
    if (typeof definition.capability !== 'string' || !definition.capability.trim()) {
      throw new TypeError(`Provider contract ${definition.id}: capability is required`);
    }
    if (typeof definition.validate !== 'function') {
      throw new TypeError(`Provider contract ${definition.id}: validate(provider) is required`);
    }

    const id = definition.id.trim();
    const existing = contracts.get(id);
    if (existing) return existing;

    const contract = freezeContract({
      ...definition,
      id,
      capability: definition.capability.trim()
    });

    contracts.set(id, contract);
    emit('contract-registered', { id: contract.id, capability: contract.capability });
    return contract;
  };

  const getContract = (id) => contracts.get(id) || null;

  const listContracts = () => Object.freeze(
    [...contracts.values()]
      .map((contract) => Object.freeze({
        id: contract.id,
        capability: contract.capability
      }))
      .sort((left, right) => left.id.localeCompare(right.id))
  );

  const validateProvider = (contractId, provider) => {
    const contract = getContract(contractId);
    if (!contract) throw new Error(`Unknown provider contract: ${contractId}`);

    const result = contract.validate(provider);
    if (result !== true) {
      const reason = typeof result === 'string' ? result : 'provider rejected by contract';
      emit('validation-rejected', { contractId, reason });
      throw new TypeError(`${contractId}: ${reason}`);
    }

    emit('validation-ready', { contractId });
    return provider;
  };

  registerContract({
    id: 'operations-widget',
    capability: 'operations-widget',
    validate(provider) {
      if (!provider || typeof provider !== 'object') return 'provider must be an object';
      if (typeof provider.id !== 'string' || !provider.id.trim()) return 'id is required';
      if (typeof provider.render !== 'function') return 'render(context) is required';
      return true;
    }
  });

  registerContract({
    id: 'search-provider',
    capability: 'search-provider',
    validate(provider) {
      if (!provider || typeof provider !== 'object') return 'provider must be an object';
      if (typeof provider.id !== 'string' || !provider.id.trim()) return 'id is required';
      if (typeof provider.search !== 'function') return 'search(query, options) is required';
      return true;
    }
  });

  registerContract({
    id: 'scientific-view',
    capability: 'scientific-view',
    validate(provider) {
      if (!provider || typeof provider !== 'object') return 'provider must be an object';
      if (typeof provider.id !== 'string' || !provider.id.trim()) return 'id is required';
      if (typeof provider.mount !== 'function') return 'mount(context) is required';
      return true;
    }
  });

  registerContract({
    id: 'repository-intelligence-provider',
    capability: 'repository-intelligence-provider',
    validate(provider) {
      if (!provider || typeof provider !== 'object') return 'provider must be an object';
      if (typeof provider.id !== 'string' || !provider.id.trim()) return 'id is required';
      if (typeof provider.getSnapshot !== 'function') return 'getSnapshot() is required';
      return true;
    }
  });

  registerContract({
    id: 'navigation-extension',
    capability: 'navigation-extension',
    validate(provider) {
      if (!provider || typeof provider !== 'object') return 'provider must be an object';
      if (typeof provider.id !== 'string' || !provider.id.trim()) return 'id is required';
      if (typeof provider.getItems !== 'function') return 'getItems(context) is required';
      return true;
    }
  });

  window.DSGPluginProviderContracts = Object.freeze({
    version: VERSION,
    register: registerContract,
    get: getContract,
    list: listContracts,
    validate: validateProvider
  });

  const initialize = ({ events: eventBus } = {}) => {
    eventBus?.emit('plugin-provider-contracts-ready', {
      version: VERSION,
      contracts: listContracts()
    });
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'plugin-provider-contracts',
      order: 58,
      initialize
    });
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  } else {
    initialize();
  }
})();
