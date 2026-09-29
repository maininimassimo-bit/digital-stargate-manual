import * as THREE from '../assets/vendor/three-0.180.0/three.module.min.js';

// This module is loaded only for an enabled scene page. It never reads data panels.
export async function mountScene(stage, { signal }) {
  const observatory = stage.dataset.dsgScene === 'observatory';
  const factory = observatory
    ? await import('./immersive-observatory.mjs')
    : await import('./immersive-gateway.mjs');
  if (signal.aborted) return () => {};
  // A fresh canvas isolates delayed context-loss events from the previous renderer.
  const previousCanvas = stage.querySelector('canvas');
  const canvas = previousCanvas.cloneNode(false);
  previousCanvas.replaceWith(canvas);
  const compact = matchMedia('(max-width: 700px), (pointer: coarse)').matches;
  const resources = new Set();
  const keep = value => { resources.add(value); return value; };
  let renderer, resizeObserver, intersectionObserver, domeObserver;
  let disposed = false, lost = false, visible = true, frame = 0, timer = 0, until = 0, last = 0, time = 0;
  let view = 'section', px = 0, py = 0, angle = .73, elevation = .51, progress = 0;
  const domeSync = stage.hasAttribute('data-dsg-dome-sync');
  let following = domeSync;
  const observedView = () => ({CLOSED:'exterior',OPEN:'section'})[stage.dataset.dsgObservedDome] || 'neutral';
  if (domeSync) view = observedView();
  stage.querySelectorAll('[data-dsg-scene-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.dsgSceneView === view)));
  const listeners = new AbortController();
  const stop = () => { cancelAnimationFrame(frame); clearTimeout(timer); frame = timer = 0; };
  function dispose() {
    if (disposed) return;
    disposed = true; stop(); listeners.abort();
    resizeObserver?.disconnect(); intersectionObserver?.disconnect(); domeObserver?.disconnect();
    resources.forEach(resource => resource.dispose());
    renderer?.dispose(); renderer?.forceContextLoss();
    signal.removeEventListener('abort', dispose);
  }
  signal.addEventListener('abort', dispose, { once: true });
  try {
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: !compact, powerPreference: 'low-power' });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x08131f, .009);
    const camera = new THREE.PerspectiveCamera(observatory ? 39 : 48, 1, .1, 130);
    const model = observatory
      ? factory.createObservatory(THREE, scene, keep)
      : factory.createGateway(THREE, scene, keep, compact);
    let seed = 7;
    const random = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
    if (!observatory) {
      const positions = new Float32Array((compact ? 500 : 1400) * 3);
      for (let i = 0; i < positions.length; i += 3) positions.set([(random() - .5) * 60, (random() - .5) * 40, -5 - random() * 60], i);
      const geo = keep(new THREE.BufferGeometry()); geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      scene.add(new THREE.Points(geo, keep(new THREE.PointsMaterial({ color: 0x9ed2ee, size: .075 }))));
    }
    const active = () => !disposed && !lost && visible && !document.hidden;
    function render(now) {
      frame = 0;
      if (!active()) return;
      const dt = Math.min(.05, (now - last) / 1000); last = now; time += dt;
      const easing = 1 - Math.exp(-9 * dt);
      const rect = stage.getBoundingClientRect();
      const targetProgress = Math.min(1, Math.max(0, -rect.top / Math.max(1, rect.height)));
      progress += (targetProgress - progress) * easing;
      if (observatory) {
        angle += ((view === 'top' ? .35 : .73) + px * .26 - angle) * easing;
        elevation += ((view === 'top' ? 1.38 : .51) + py * .08 - elevation) * easing;
        const distance = camera.aspect < .8 ? 18 : 15;
        camera.position.set(Math.cos(angle) * Math.cos(elevation) * distance, Math.sin(elevation) * distance + 1, Math.sin(angle) * Math.cos(elevation) * distance);
        camera.lookAt(0, 1.5, 0);
      } else {
        // Fit the entire atlas in the usable viewport, including narrow/tall cards.
        const halfVertical = THREE.MathUtils.degToRad(camera.fov / 2);
        const halfHorizontal = Math.atan(Math.tan(halfVertical) * camera.aspect);
        const distance = 5 / Math.sin(Math.min(halfVertical, halfHorizontal)) * (1.1 - progress * .05);
        camera.position.set(px * .8, py * .5, distance);
        camera.lookAt(0, 0, 0);
      }
      model.update({ time, progress, view });
      stage.dataset.dsgRenderedView = view;
      renderer.render(scene, camera);
      // No endless ambient loop: stop after input settles, including desktop.
      if (now < until) timer = setTimeout(() => { timer = 0; frame = requestAnimationFrame(render); }, compact ? 32 : 16);
    }
    function wake() {
      until = performance.now() + 850;
      if (active() && !frame && !timer) { last = performance.now() - 16; frame = requestAnimationFrame(render); }
    }
    const resize = () => {
      const width = stage.clientWidth;
      let height = stage.clientHeight;
      if (!observatory) {
        const heading = stage.querySelector('.dsg-scene__heading');
        const toolbar = stage.querySelector('.dsg-scene__toolbar');
        const top = heading.offsetTop + heading.offsetHeight + 12;
        height = Math.max(1, toolbar.offsetTop - top - 12);
        canvas.style.top = `${top}px`; canvas.style.height = `${height}px`;
      }
      if (!width || !height || disposed) return;
      renderer.setPixelRatio(Math.min(devicePixelRatio || 1, compact ? 1 : 1.5, Math.sqrt(1500000 / (width * height))));
      renderer.setSize(width, height, false);
      camera.aspect = width / height; camera.updateProjectionMatrix(); wake();
    };
    const on = (target, name, fn, options = {}) => target.addEventListener(name, fn, { ...options, signal: listeners.signal });
    function updateViewControls() {
      stage.dataset.dsgViewMode = following ? 'auto' : 'manual';
      stage.dataset.dsgSelectedView = view;
      stage.querySelector('[data-dsg-follow-dome]')?.setAttribute('aria-pressed', String(following));
      stage.querySelectorAll('[data-dsg-scene-view]').forEach(item => item.setAttribute('aria-pressed', String(item.dataset.dsgSceneView === view)));
      if (domeSync) stage.querySelector('.dsg-scene__status').textContent = following
        ? (view === 'neutral' ? 'Stato non disponibile · nessuna apertura/chiusura dedotta' : view === 'exterior' ? 'Dal badge: esterno chiuso · nessun comando' : 'Dal badge: interno in sezione · nessun comando')
        : 'Vista libera · non rappresenta lo stato corrente';
    }
    const followBadge = () => { following = true; view = observedView(); updateViewControls(); wake(); };
    if (domeSync) {
      domeObserver = new MutationObserver(followBadge);
      domeObserver.observe(stage, { attributes:true, attributeFilter:['data-dsg-observed-dome'] });
      updateViewControls();
    }
    on(stage, 'pointermove', event => {
      if (compact) return;
      const rect = stage.getBoundingClientRect();
      px = (event.clientX - rect.left) / rect.width * 2 - 1; py = 1 - (event.clientY - rect.top) / rect.height * 2; wake();
    }, { passive: true });
    on(stage, 'pointerleave', () => { px = py = 0; wake(); });
    on(stage, 'click', event => {
      if (domeSync && event.target.closest('[data-dsg-follow-dome]')) { followBadge(); return; }
      const button = event.target.closest('[data-dsg-scene-view]');
      if (!button) return;
      view = button.dataset.dsgSceneView;
      following = false; updateViewControls();
      wake();
    });
    on(window, 'scroll', wake, { passive: true });
    on(document, 'visibilitychange', () => { stop(); if (!document.hidden) wake(); });
    on(canvas, 'webglcontextlost', event => {
      event.preventDefault(); lost = true; stop(); stage.classList.remove('is-ready');
      stage.querySelector('.dsg-scene__status').textContent = 'Contesto 3D sospeso · dati invariati';
    });
    on(canvas, 'webglcontextrestored', () => {
      lost = false; stage.classList.add('is-ready');
      stage.querySelector('.dsg-scene__status').textContent = 'Modello 3D illustrativo · controlli solo visuali'; if(domeSync) updateViewControls(); resize();
    });
    resizeObserver = new ResizeObserver(resize); resizeObserver.observe(stage);
    if (!observatory) {
      resizeObserver.observe(stage.querySelector('.dsg-scene__heading'));
      resizeObserver.observe(stage.querySelector('.dsg-scene__toolbar'));
    }
    intersectionObserver = new IntersectionObserver(entries => { visible = entries[0].isIntersecting; if (visible) wake(); else stop(); });
    intersectionObserver.observe(stage); resize();
    return dispose;
  } catch (error) { dispose(); throw error; }
}
