(() => {
  'use strict';

  if (window.DSG?.components && window.DSG?.events) return;

  const registry = new Map();
  const subscriptions = new Map();
  let cycle = 0;

  const events = Object.freeze({
    on(type, listener) {
      if (typeof listener !== 'function') throw new TypeError('Event listener must be a function');
      const listeners = subscriptions.get(type) || new Set();
      listeners.add(listener);
      subscriptions.set(type, listeners);
      return () => listeners.delete(listener);
    },

    once(type, listener) {
      const unsubscribe = this.on(type, (detail) => {
        unsubscribe();
        listener(detail);
      });
      return unsubscribe;
    },

    emit(type, detail = {}) {
      document.dispatchEvent(new CustomEvent(`dsg:${type}`, { detail }));
      (subscriptions.get(type) || []).forEach((listener) => {
        try {
          listener(detail);
        } catch (error) {
          console.error(`Digital StarGate event listener failed: ${type}`, error);
        }
      });
    }
  });

  const normalizeComponent = (definition) => {
    if (!definition || typeof definition !== 'object') {
      throw new TypeError('Component definition must be an object');
    }

    const { name, initialize, destroy, order = 100 } = definition;
    if (!name || typeof name !== 'string') throw new TypeError('Component name is required');
    if (typeof initialize !== 'function') throw new TypeError(`Component ${name} requires initialize()`);

    return Object.freeze({
      name,
      initialize,
      destroy: typeof destroy === 'function' ? destroy : null,
      order: Number.isFinite(order) ? order : 100
    });
  };

  const destroyComponent = async (entry, context) => {
    if (entry.lastCycle === 0) return;

    try {
      if (typeof entry.cleanup === 'function') {
        await entry.cleanup();
      }
      if (entry.definition.destroy) {
        await entry.definition.destroy(context);
      }
      entry.cleanup = null;
      entry.state = 'destroyed';
      entry.error = null;
      events.emit('component-destroyed', {
        name: entry.definition.name,
        previousCycle: entry.lastCycle,
        cycle: context.cycle
      });
    } catch (error) {
      entry.cleanup = null;
      entry.state = 'destroy-error';
      entry.error = error;
      console.error(`Digital StarGate component destroy failed: ${entry.definition.name}`, error);
      events.emit('component-destroy-error', {
        name: entry.definition.name,
        previousCycle: entry.lastCycle,
        cycle: context.cycle,
        error
      });
    }
  };

  const runComponent = async (entry, context) => {
    if (entry.lastCycle === context.cycle) return;

    await destroyComponent(entry, context);

    try {
      const result = await entry.definition.initialize(context);
      entry.lastCycle = context.cycle;
      entry.state = 'ready';
      entry.cleanup = typeof result === 'function' ? result : null;
      entry.error = null;
      events.emit('component-ready', { name: entry.definition.name, cycle: context.cycle });
    } catch (error) {
      entry.lastCycle = context.cycle;
      entry.state = 'error';
      entry.error = error;
      console.error(`Digital StarGate component failed: ${entry.definition.name}`, error);
      events.emit('component-error', { name: entry.definition.name, cycle: context.cycle, error });
    }
  };

  const runAll = async (source = 'manual') => {
    cycle += 1;
    const context = Object.freeze({
      cycle,
      source,
      root: document,
      events,
      components
    });

    events.emit('lifecycle-start', { cycle, source });

    const entries = [...registry.values()]
      .sort((left, right) => left.definition.order - right.definition.order);

    for (const entry of entries) {
      await runComponent(entry, context);
    }

    events.emit('lifecycle-ready', { cycle, source, components: entries.length });
  };

  const components = Object.freeze({
    register(definition) {
      const normalized = normalizeComponent(definition);
      if (registry.has(normalized.name)) return registry.get(normalized.name).definition;

      registry.set(normalized.name, {
        definition: normalized,
        state: 'registered',
        lastCycle: 0,
        cleanup: null,
        error: null
      });

      events.emit('component-registered', { name: normalized.name, order: normalized.order });

      if (document.readyState !== 'loading') {
        queueMicrotask(() => runAll('late-registration'));
      }

      return normalized;
    },

    has(name) {
      return registry.has(name);
    },

    get(name) {
      return registry.get(name)?.definition || null;
    },

    status() {
      return [...registry.values()].map((entry) => ({
        name: entry.definition.name,
        order: entry.definition.order,
        state: entry.state,
        lastCycle: entry.lastCycle
      }));
    },

    run(source) {
      return runAll(source);
    }
  });

  window.DSG = Object.freeze({
    version: '2.0.0-rc2',
    events,
    components
  });

  const boot = () => runAll('dom-ready');

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot, { once: true });
  } else {
    boot();
  }

  if (window.document$?.subscribe) {
    window.document$.subscribe(() => runAll('instant-navigation'));
  }
})();
