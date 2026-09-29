// Illustrative celestial atlas: no astrometric or telemetry claim.
export function createGateway(THREE, scene, keep, compact) {
 let gate, ticks, core, halo;
 let seed=42;const random=()=>((seed=(seed*1664525+1013904223)>>>0)/4294967296);
        // Portale meccanico tridimensionale: torus solidi e nervature istanziate.
        gate=new THREE.Group(); gate.position.set(0,0,0); scene.add(gate);
        scene.add(new THREE.HemisphereLight(0x8cbaff,0x091020,2));
        const light=new THREE.PointLight(0x59dfff,95,35); light.position.set(1,5,5); scene.add(light);
        const rim=new THREE.PointLight(0x8060ff,120,30); rim.position.set(8,-2,0); scene.add(rim);
        const metal=keep(new THREE.MeshStandardMaterial({color:0x27435b,metalness:.72,roughness:.28}));
        const cyan=keep(new THREE.MeshBasicMaterial({color:0x80efff,toneMapped:false}));
        const violet=keep(new THREE.MeshBasicMaterial({color:0x8a79ff,toneMapped:false}));
        const ring=(radius,tube,mat,z=0) => {
          const mesh=new THREE.Mesh(keep(new THREE.TorusGeometry(radius,tube,compact?6:10,compact?100:180)),mat);
          mesh.position.z=z; gate.add(mesh); return mesh;
        };
        ring(3.5,.16,metal); ring(3.76,.065,metal,-.2); ring(3.25,.055,cyan,.05);
        ring(3.56,.016,cyan,.17); ring(3.94,.012,violet,-.28);
        const back=ring(3.38,.035,violet,-.65); back.rotation.y=.07;
        ticks=new THREE.Group(); gate.add(ticks);
        const ribGeo=keep(new THREE.BoxGeometry(.055,.21,.32));
        const ribs=new THREE.InstancedMesh(ribGeo,metal,96);
        const markerGeo=keep(new THREE.BoxGeometry(.025,.095,.025));
        const markers=new THREE.InstancedMesh(markerGeo,cyan,96);
        const dummy=new THREE.Object3D();
        for(let i=0;i<96;i++) {
          const a=i/96*Math.PI*2;
          dummy.position.set(Math.cos(a)*3.63,Math.sin(a)*3.63,0);
          dummy.rotation.set(0,0,a-Math.PI/2); dummy.updateMatrix(); ribs.setMatrixAt(i,dummy.matrix);
          dummy.position.set(Math.cos(a)*3.86,Math.sin(a)*3.86,.03); dummy.updateMatrix(); markers.setMatrixAt(i,dummy.matrix);
        }
        ticks.add(ribs,markers);

        // Volume centrale: globo reticolare e particelle distribuite sulla sfera.
        core=new THREE.Group(); gate.add(core);
        const gridMaterial=keep(new THREE.MeshBasicMaterial({color:0x4bcbe6,wireframe:true,transparent:true,opacity:.2,depthWrite:false}));
        core.add(new THREE.Mesh(keep(new THREE.SphereGeometry(2.25,32,20)),gridMaterial));
        const shellCount=compact?650:1600;
        const shellPos=new Float32Array(shellCount*3);
        for(let i=0;i<shellCount;i++) {
          const y=1-2*(i+.5)/shellCount, a=i*2.399963;
          const r=Math.sqrt(1-y*y), radius=2.28+random()*.09;
          shellPos.set([Math.cos(a)*r*radius,y*radius,Math.sin(a)*r*radius],i*3);
        }
        const shellGeo=keep(new THREE.BufferGeometry()); shellGeo.setAttribute('position',new THREE.BufferAttribute(shellPos,3));
        core.add(new THREE.Points(shellGeo,keep(new THREE.PointsMaterial({color:0xa3f6ff,size:.055,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}))));
        // Orbites réellement inclinées dans l'espace, avec balises lumineuses.
        for(let i=0;i<3;i++) {
          const orbit=new THREE.Mesh(keep(new THREE.TorusGeometry(2.65+i*.12,.012,5,120)),i===1?violet:cyan);
          orbit.rotation.set(.65+i*.65,.2+i*.8,.4); core.add(orbit);
          const beacon=new THREE.Mesh(keep(new THREE.SphereGeometry(.065,8,8)),cyan);
          beacon.position.set(2.65+i*.12,0,0); orbit.add(beacon);
        }
        // Halo procédural: transparence additive, sans passe de bloom plein écran.
        const haloMat=keep(new THREE.ShaderMaterial({
          uniforms:{uTime:{value:0}},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,
          vertexShader:`varying vec2 vUv; void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
          fragmentShader:`precision mediump float; varying vec2 vUv; uniform float uTime;
            void main(){
              vec2 p=(vUv-.5)*2.; float r=length(p); float a=atan(p.y,p.x);
              float ring=exp(-pow((r-.69)*35.,2.));
              float aura=exp(-pow((r-.68)*7.,2.))*.24;
              float wave=.65+.35*sin(a*7.-uTime*.45+r*24.);
              float mist=exp(-r*r*5.)*.09*(.5+.5*sin(a*4.+r*18.-uTime*.25));
              vec3 col=mix(vec3(.12,.7,1.),vec3(.45,.2,1.),.5+.5*sin(a+uTime*.08));
              float alpha=(ring*.75+aura*wave+mist)*(1.-smoothstep(.85,1.,r));
              gl_FragColor=vec4(col,alpha);
            }`
        }));
        halo=new THREE.Mesh(keep(new THREE.PlaneGeometry(10,10)),haloMat); halo.position.z=-.4; gate.add(halo);

 return {update({time,progress,view}) {
   gate.rotation.y=-.3+progress*.65;
   gate.rotation.x=view==='top'?1.1:.18;
   ticks.rotation.z=-time*.035;
   core.rotation.y=time*.12;
   core.rotation.z=.3;
   halo.material.uniforms.uTime.value=time;
 }};
}
