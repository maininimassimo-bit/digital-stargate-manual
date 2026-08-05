(() => {
  'use strict';

  const VERSION = '1.0.0-rc2';

  const events = () => window.DSG?.events || null;

  const emit = (type, detail = {}) => {
    events()?.emit(`plugin-dependency-${type}`, {
      resolverVersion: VERSION,
      ...detail
    });
  };

  const normalizeSelection = (selection, registry) => {
    if (selection == null) return registry.list().map((plugin) => plugin.id);
    if (!Array.isArray(selection)) {
      throw new TypeError('Plugin selection must be an array of plugin ids');
    }

    const normalized = selection.map((id) => {
      if (typeof id !== 'string' || !id.trim()) {
        throw new TypeError('Plugin selection entries must be non-empty strings');
      }
      return id.trim();
    });

    return [...new Set(normalized)].sort();
  };

  const buildGraph = (selection, registry) => {
    const requested = normalizeSelection(selection, registry);
    const graph = new Map();
    const missingPlugins = [];
    const missingDependencies = [];
    const queue = [...requested];
    const visited = new Set();

    while (queue.length) {
      const id = queue.shift();
      if (visited.has(id)) continue;
      visited.add(id);

      const plugin = registry.get(id);
      if (!plugin) {
        missingPlugins.push(id);
        continue;
      }

      const dependencies = [...plugin.dependencies].sort();
      graph.set(id, dependencies);

      dependencies.forEach((dependencyId) => {
        if (!registry.has(dependencyId)) {
          missingDependencies.push(Object.freeze({
            pluginId: id,
            dependencyId
          }));
          return;
        }
        queue.push(dependencyId);
      });
    }

    return Object.freeze({
      requested: Object.freeze(requested),
      graph,
      missingPlugins: Object.freeze([...new Set(missingPlugins)].sort()),
      missingDependencies: Object.freeze(
        missingDependencies.sort((left, right) => (
          left.pluginId.localeCompare(right.pluginId) ||
          left.dependencyId.localeCompare(right.dependencyId)
        ))
      )
    });
  };

  const detectCycle = (graph) => {
    const state = new Map();
    const stack = [];

    const visit = (id) => {
      const currentState = state.get(id) || 'unvisited';
      if (currentState === 'visited') return null;
      if (currentState === 'visiting') {
        const start = stack.indexOf(id);
        return [...stack.slice(start), id];
      }

      state.set(id, 'visiting');
      stack.push(id);

      for (const dependencyId of graph.get(id) || []) {
        if (!graph.has(dependencyId)) continue;
        const cycle = visit(dependencyId);
        if (cycle) return cycle;
      }

      stack.pop();
      state.set(id, 'visited');
      return null;
    };

    for (const id of [...graph.keys()].sort()) {
      const cycle = visit(id);
      if (cycle) return Object.freeze(cycle);
    }

    return null;
  };

  const topologicalSort = (graph) => {
    const indegree = new Map();
    const dependents = new Map();

    [...graph.keys()].forEach((id) => {
      indegree.set(id, 0);
      dependents.set(id, []);
    });

    graph.forEach((dependencies, id) => {
      dependencies.forEach((dependencyId) => {
        if (!graph.has(dependencyId)) return;
        indegree.set(id, indegree.get(id) + 1);
        dependents.get(dependencyId).push(id);
      });
    });

    dependents.forEach((items) => items.sort());

    const ready = [...indegree.entries()]
      .filter(([, count]) => count === 0)
      .map(([id]) => id)
      .sort();

    const ordered = [];

    while (ready.length) {
      const id = ready.shift();
      ordered.push(id);

      for (const dependentId of dependents.get(id) || []) {
        const next = indegree.get(dependentId) - 1;
        indegree.set(dependentId, next);
        if (next === 0) {
          ready.push(dependentId);
          ready.sort();
        }
      }
    }

    return Object.freeze(ordered);
  };

  const analyze = (selection) => {
    const registry = window.DSGPluginRegistry;
    if (!registry) {
      throw new Error('DSGPluginRegistry is not available');
    }

    const graphResult = buildGraph(selection, registry);
    const cycle = detectCycle(graphResult.graph);
    const valid = (
      graphResult.missingPlugins.length === 0 &&
      graphResult.missingDependencies.length === 0 &&
      cycle === null
    );

    const order = valid ? topologicalSort(graphResult.graph) : Object.freeze([]);

    const result = Object.freeze({
      valid,
      requested: graphResult.requested,
      order,
      missingPlugins: graphResult.missingPlugins,
      missingDependencies: graphResult.missingDependencies,
      cycle,
      graph: Object.freeze(
        [...graphResult.graph.entries()]
          .map(([id, dependencies]) => Object.freeze({
            id,
            dependencies: Object.freeze([...dependencies])
          }))
          .sort((left, right) => left.id.localeCompare(right.id))
      )
    });

    emit(valid ? 'resolved' : 'rejected', {
      requested: result.requested,
      order: result.order,
      missingPlugins: result.missingPlugins,
      missingDependencies: result.missingDependencies,
      cycle: result.cycle
    });

    return result;
  };

  const resolve = (selection) => {
    const result = analyze(selection);
    if (result.valid) return result.order;

    const reasons = [];
    if (result.missingPlugins.length) {
      reasons.push(`missing plugins: ${result.missingPlugins.join(', ')}`);
    }
    if (result.missingDependencies.length) {
      reasons.push(`missing dependencies: ${result.missingDependencies.map((item) => `${item.pluginId}->${item.dependencyId}`).join(', ')}`);
    }
    if (result.cycle) {
      reasons.push(`dependency cycle: ${result.cycle.join(' -> ')}`);
    }

    throw new Error(`Plugin dependency resolution failed (${reasons.join('; ')})`);
  };

  window.DSGPluginDependencyResolver = Object.freeze({
    version: VERSION,
    analyze,
    resolve
  });

  const initialize = ({ events: eventBus } = {}) => {
    eventBus?.emit('plugin-dependency-resolver-ready', {
      version: VERSION,
      capabilities: [
        'missing-plugin-detection',
        'missing-dependency-detection',
        'cycle-detection',
        'deterministic-ordering'
      ]
    });
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'plugin-dependency-resolver',
      order: 56,
      initialize
    });
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  } else {
    initialize();
  }
})();
