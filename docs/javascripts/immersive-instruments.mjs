import * as THREE from '../assets/vendor/three-0.180.0/three.module.min.js';

// The consumer supplies display metadata; this module neither evaluates nor fetches telemetry.
export function mountInstruments(panel, signal) {
  const resources = new Set(), listeners = new AbortController();
  let renderer, resizeObserver, intersectionObserver, frame = 0, disposed = false, visible = false, lost = false;
  let px = 0, py = 0;
  const keep = value => { resources.add(value); return value; };
  function dispose() {
    if (disposed) return;
    disposed = true; cancelAnimationFrame(frame); listeners.abort();
    resizeObserver?.disconnect(); intersectionObserver?.disconnect();
    resources.forEach(resource => resource.dispose());
    renderer?.dispose(); renderer?.forceContextLoss(); renderer?.domElement.remove();
    panel.classList.remove('is-instruments-ready'); signal.removeEventListener('abort', dispose);
  }
  if (signal.aborted) return dispose;
  signal.addEventListener('abort', dispose, { once: true });
  try {
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: matchMedia('(pointer: fine)').matches, powerPreference: 'low-power' });
    renderer.setClearColor(0, 0); renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.domElement.setAttribute('aria-hidden', 'true'); panel.append(renderer.domElement);
    const cards = [...panel.querySelectorAll('.dsg-instrument')];
    const models = cards.map(card => {
      const scene = new THREE.Scene(), group = new THREE.Group(); scene.add(group);
      scene.add(new THREE.HemisphereLight(0xdaf5ff, 0x283b50, 2.5));
      const light = new THREE.DirectionalLight(0xffffff, 3); light.position.set(-3, 4, 6); scene.add(light);
      const material = color => keep(new THREE.MeshStandardMaterial({ color, metalness: .58, roughness: .32 }));
      const metal = material(0x526e87), accent = material(({good:0x35ce97,bad:0xff6177,unknown:0xe4b354})[card.dataset.instrumentTone] || 0xe4b354);
      const threshold = material(0xf8c968);
      const mesh = (geometry, mat, x=0, y=0, z=0) => { const object = new THREE.Mesh(keep(geometry), mat); object.position.set(x,y,z); group.add(object); return object; };
      const ring = (radius, tube, mat, start=0, arc=Math.PI*2) => { const object=mesh(new THREE.TorusGeometry(radius,tube,8,64,arc),mat); object.rotation.z=start; return object; };
      const unknown = card.dataset.instrumentTone === 'unknown';
      const type = card.dataset.instrumentType;
      if (unknown) {
        for(let n=0;n<8;n++) ring(.8,.065,accent,n*Math.PI/4,.42);
        mesh(new THREE.BoxGeometry(.10,.45,.10),accent,0,.15);
        mesh(new THREE.SphereGeometry(.08,12,8),accent,0,-.3);
      } else if (type === 'dial') {
        const ratio = Math.max(0,Math.min(1,Number(card.dataset.instrumentRatio)||0));
        ring(.95,.085,metal);
        if(ratio>0) ring(.95,.095,accent,-Math.PI/2,Math.PI*2*ratio);
        for(let n=0;n<20;n++) {const a=n*Math.PI/10;mesh(new THREE.BoxGeometry(.025,.09,.04),metal,Math.sin(a)*1.13,Math.cos(a)*1.13).rotation.z=-a;}
        const a=-Math.PI/2+Math.PI*2*Number(card.dataset.instrumentLimit);
        mesh(new THREE.BoxGeometry(.055,.23,.12),threshold,Math.cos(a)*.95,Math.sin(a)*.95,.10).rotation.z=a-Math.PI/2;
        mesh(new THREE.CylinderGeometry(.70,.75,.10,40),metal).rotation.x=Math.PI/2;
      } else if (type === 'dome') {
        const open=card.dataset.instrumentState==='OPEN';
        mesh(new THREE.SphereGeometry(.82,32,16,open?.25:0,open?Math.PI*2-.5:Math.PI*2,0,Math.PI/2),metal,0,-.25);
        mesh(new THREE.CylinderGeometry(.88,.88,.15,32),accent,0,-.32);
      } else if (type === 'mount') {
        mesh(new THREE.CylinderGeometry(.18,.32,1.1,16),metal,0,-.2);
        mesh(new THREE.BoxGeometry(1.3,.32,.4),accent,0,.4).rotation.z=.4;
        mesh(new THREE.CylinderGeometry(.55,.55,.1,20),metal,0,-.8);
      } else if (type === 'camera') {
        mesh(new THREE.BoxGeometry(1.2,.8,.4),metal);
        const lens=mesh(new THREE.CylinderGeometry(.35,.35,.4,24),accent,0,0,.35);lens.rotation.x=Math.PI/2;
      } else if (type === 'power') {
        mesh(new THREE.BoxGeometry(1.3,.7,.35),metal);mesh(new THREE.BoxGeometry(.9,.28,.08),accent,0,0,.22);
        mesh(new THREE.BoxGeometry(.12,.22,.22),accent,.75);
      } else if (type === 'network') {
        for(const x of [-.7,0,.7])mesh(new THREE.SphereGeometry(.18,16,12),accent,x,x===0?.45:-.3);
        mesh(new THREE.BoxGeometry(1.4,.05,.06),metal,0,-.3);mesh(new THREE.BoxGeometry(.05,.75,.06),metal,0,.08);
      } else {
        ring(.78,.09,metal);mesh(new THREE.BoxGeometry(.055,.55,.10),accent,0,.25,.1);mesh(new THREE.BoxGeometry(.45,.055,.10),accent,.2,0,.1);
      }
      const camera=new THREE.PerspectiveCamera(35,1,.1,20);camera.position.z=4.8;
      return {scene,group,camera,port:card.querySelector('.dsg-instrument__port')};
    });
    function draw() {
      frame=0;
      if(disposed||lost||!visible||document.hidden||!panel.isConnected)return;
      const bounds=panel.getBoundingClientRect(); if(!bounds.width||!bounds.height)return;
      renderer.setPixelRatio(Math.min(devicePixelRatio||1,1,Math.sqrt(650000/(bounds.width*bounds.height))));
      renderer.setSize(bounds.width,bounds.height,false);renderer.setScissorTest(false);renderer.clear();renderer.setScissorTest(true);
      models.forEach(({scene,group,camera,port})=>{
        const rect=port.getBoundingClientRect();camera.aspect=rect.width/rect.height;camera.updateProjectionMatrix();
        group.rotation.set(-.28+py*.12,.23+px*.18,0);
        renderer.setViewport(rect.left-bounds.left,bounds.bottom-rect.bottom,rect.width,rect.height);
        renderer.setScissor(rect.left-bounds.left,bounds.bottom-rect.bottom,rect.width,rect.height);
        renderer.render(scene,camera);
      });
      panel.classList.add('is-instruments-ready');panel.dataset.instrumentsState='ready';
    }
    const wake=()=>{if(!frame&&!disposed&&visible&&!document.hidden)frame=requestAnimationFrame(draw);};
    const on=(target,name,fn,options={})=>target.addEventListener(name,fn,{...options,signal:listeners.signal});
    on(panel,'pointermove',event=>{if(!matchMedia('(hover: hover) and (pointer: fine)').matches)return;const r=panel.getBoundingClientRect();px=(event.clientX-r.left)/r.width-.5;py=(event.clientY-r.top)/r.height-.5;wake();},{passive:true});
    on(panel,'pointerleave',()=>{px=py=0;wake();});
    on(document,'visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;}else wake();});
    on(renderer.domElement,'webglcontextlost',event=>{event.preventDefault();lost=true;panel.classList.remove('is-instruments-ready');panel.dataset.instrumentsState='unavailable';});
    on(renderer.domElement,'webglcontextrestored',()=>{lost=false;wake();});
    resizeObserver=new ResizeObserver(wake);resizeObserver.observe(panel);
    intersectionObserver=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)wake();else{cancelAnimationFrame(frame);frame=0;}});intersectionObserver.observe(panel);
    return dispose;
  }catch(error){dispose();throw error;}
}
