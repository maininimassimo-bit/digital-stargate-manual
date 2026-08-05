import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import vm from 'node:vm';

const root = new URL('../../', import.meta.url);

class TestCustomEvent extends Event {
  constructor(type, options = {}) {
    super(type);
    this.detail = options.detail;
  }
}

const loadSource = async (path) => readFile(new URL(path, root), 'utf8');

const createDocument = () => {
  const document = new EventTarget();
  document.readyState = 'loading';
  document.querySelector = () => null;
  document.dispatchEvent = EventTarget.prototype.dispatchEvent.bind(document);
  document.addEventListener = EventTarget.prototype.addEventListener.bind(document);
  return document;
};

const createSdkContext = async () => {
  const registeredComponents = [];
  const emitted = [];
  const document = createDocument();
  const components = {
    register(definition) {
      registeredComponents.push(definition);
      return definition;
    }
  };
  const events = {
    emit(type, detail) {
      emitted.push({ type, detail });
    }
  };
  const window = {
    DSG: { components, events, version: 'test' },
    console,
    document
  };
  const context = vm.createContext({
    window,
    document,
    console,
    CustomEvent: TestCustomEvent,
    Event,
    EventTarget,
    Map,
    Set,
    Object,
    Array,
    String,
    Number,
    Boolean,
    Date,
    Error,
    TypeError,
    Promise,
    queueMicrotask
  });

  for (const path of [
    'docs/javascripts/dsg-plugin-registry.js',
    'docs/javascripts/dsg-plugin-dependency-resolver.js',
    'docs/javascripts/dsg-plugin-runtime.js',
    'docs/javascripts/dsg-plugin-provider-contracts.js'
  ]) {
    vm.runInContext(await loadSource(path), context, { filename: path });
  }

  return { window, document, registeredComponents, emitted };
};

const plugin = (id, dependencies = [], hooks = {}) => ({
  id,
  version: '1.0.0',
  apiVersion: '1',
  capabilities: hooks.capabilities || [],
  dependencies,
  initialize: hooks.initialize || (() => undefined),
  dispose: hooks.dispose
});

test('Plugin Registry validates, registers idempotently and rejects conflicting duplicates', async () => {
  const { window } = await createSdkContext();
  const registry = window.DSGPluginRegistry;
  const manifest = plugin('alpha-plugin', [], { capabilities: ['operations-widget'] });

  const first = registry.register(manifest);
  const second = registry.register(manifest);

  assert.equal(first, second);
  assert.equal(registry.status().pluginCount, 1);
  assert.equal(registry.findByCapability('operations-widget').length, 1);
  assert.throws(
    () => registry.register(plugin('alpha-plugin', [], { initialize: () => 'different' })),
    /already registered/
  );
  assert.throws(
    () => registry.register({ ...manifest, id: 'Invalid ID' }),
    /kebab-case/
  );
});

test('Dependency Resolver returns deterministic order and reports missing dependencies', async () => {
  const { window } = await createSdkContext();
  const registry = window.DSGPluginRegistry;
  const resolver = window.DSGPluginDependencyResolver;

  registry.register(plugin('core-provider'));
  registry.register(plugin('beta-provider', ['core-provider']));
  registry.register(plugin('alpha-provider', ['core-provider']));
  registry.register(plugin('dashboard-provider', ['beta-provider', 'alpha-provider']));

  assert.deepEqual(
    [...resolver.resolve(['dashboard-provider'])],
    ['core-provider', 'alpha-provider', 'beta-provider', 'dashboard-provider']
  );

  registry.register(plugin('missing-consumer', ['not-registered']));
  const analysis = resolver.analyze(['missing-consumer']);
  assert.equal(analysis.valid, false);
  assert.deepEqual(
    Array.from(
      analysis.missingDependencies,
      (item) => `${item.pluginId}->${item.dependencyId}`
    ),
    ['missing-consumer->not-registered']
  );
});

test('Dependency Resolver detects cycles', async () => {
  const { window } = await createSdkContext();
  const registry = window.DSGPluginRegistry;
  const resolver = window.DSGPluginDependencyResolver;

  registry.register(plugin('cycle-a', ['cycle-b']));
  registry.register(plugin('cycle-b', ['cycle-a']));

  const analysis = resolver.analyze(['cycle-a']);
  assert.equal(analysis.valid, false);
  assert.ok(analysis.cycle);
  assert.equal(analysis.cycle[0], analysis.cycle.at(-1));
  assert.throws(() => resolver.resolve(['cycle-a']), /dependency cycle/);
});

test('Plugin Runtime initializes in dependency order and disposes in reverse order', async () => {
  const { window } = await createSdkContext();
  const registry = window.DSGPluginRegistry;
  const runtime = window.DSGPluginRuntime;
  const calls = [];

  registry.register(plugin('base-plugin', [], {
    initialize: () => {
      calls.push('init:base');
      return () => calls.push('cleanup:base');
    },
    dispose: () => calls.push('dispose:base')
  }));
  registry.register(plugin('feature-plugin', ['base-plugin'], {
    initialize: (context) => {
      calls.push(`init:feature:${context.plugin.id}`);
      return () => calls.push('cleanup:feature');
    },
    dispose: () => calls.push('dispose:feature')
  }));

  const runStatus = await runtime.run(['feature-plugin'], 'test-run');
  assert.equal(runStatus.ready, 2);
  assert.deepEqual(calls, ['init:base', 'init:feature:feature-plugin']);

  const disposeStatus = await runtime.dispose(['feature-plugin'], 'test-dispose');
  assert.equal(disposeStatus.disposed, 2);
  assert.deepEqual(calls, [
    'init:base',
    'init:feature:feature-plugin',
    'cleanup:feature',
    'dispose:feature',
    'cleanup:base',
    'dispose:base'
  ]);
});

test('Plugin Runtime isolates initialize failures', async () => {
  const { window } = await createSdkContext();
  const registry = window.DSGPluginRegistry;
  const runtime = window.DSGPluginRuntime;
  let healthyInitialized = false;

  registry.register(plugin('broken-plugin', [], {
    initialize: () => {
      throw new Error('expected failure');
    }
  }));
  registry.register(plugin('healthy-plugin', [], {
    initialize: () => {
      healthyInitialized = true;
    }
  }));

  const status = await runtime.run(['broken-plugin', 'healthy-plugin'], 'failure-isolation');
  assert.equal(healthyInitialized, true);
  assert.equal(status.ready, 1);
  assert.equal(status.errors, 1);
});

test('Provider Contracts validate a compliant operations widget', async () => {
  const { window } = await createSdkContext();
  const contracts = window.DSGPluginProviderContracts;
  const provider = { id: 'test-widget', render() {} };

  assert.equal(contracts.validate('operations-widget', provider), provider);
  assert.throws(
    () => contracts.validate('operations-widget', { id: 'invalid-widget' }),
    /render\(context\) is required/
  );
});

test('Enterprise Core executes cleanup and destroy before the next lifecycle cycle', async () => {
  const document = createDocument();
  document.readyState = 'loading';
  const window = { console, document };
  const context = vm.createContext({
    window,
    document,
    console,
    CustomEvent: TestCustomEvent,
    Event,
    EventTarget,
    Map,
    Set,
    Object,
    Array,
    String,
    Number,
    Boolean,
    Date,
    Error,
    TypeError,
    Promise,
    queueMicrotask
  });

  vm.runInContext(
    await loadSource('docs/javascripts/dsg-enterprise-core.js'),
    context,
    { filename: 'docs/javascripts/dsg-enterprise-core.js' }
  );

  const calls = [];
  window.DSG.components.register({
    name: 'lifecycle-test',
    initialize({ cycle }) {
      calls.push(`init:${cycle}`);
      return () => calls.push(`cleanup:${cycle}`);
    },
    destroy({ cycle }) {
      calls.push(`destroy:${cycle}`);
    }
  });

  await window.DSG.components.run('first-test-cycle');
  await window.DSG.components.run('second-test-cycle');

  assert.deepEqual(calls, [
    'init:1',
    'cleanup:1',
    'destroy:2',
    'init:2'
  ]);
});
