// Procedural visual geometry only. No source, signal or device state is consumed.
export function createObservatory(T, scene, keep) {
 let shell, shellGrid, roofRibs, model, stars;
 scene.add(new T.HemisphereLight(0xc5e8ff,0x1a2434,2.5));
 const sun=new T.DirectionalLight(0xe9f6ff,4);sun.position.set(3,9,6);scene.add(sun);
 const blue=new T.PointLight(0x57bfff,80,25);blue.position.set(-6,4,-3);scene.add(blue);
 const warm=new T.PointLight(0xf2c994,60,25);warm.position.set(4,3,1);scene.add(warm);
 const metal=keep(new T.MeshStandardMaterial({color:0xa3b3bd,metalness:.55,roughness:.32}));
 const dark=keep(new T.MeshStandardMaterial({color:0x14283a,metalness:.7,roughness:.28}));
 const white=keep(new T.MeshStandardMaterial({color:0xd6e2e6,metalness:.25,roughness:.36}));
 const orange=keep(new T.MeshStandardMaterial({color:0xd17641,metalness:.45,roughness:.32}));
 const glow=keep(new T.MeshBasicMaterial({color:0x75e0f0,toneMapped:false}));
 const lens=keep(new T.MeshStandardMaterial({color:0x183955,metalness:.9,roughness:.12,emissive:0x12334e,emissiveIntensity:.65}));
 const mesh=(g,m,parent=scene)=>{const x=new T.Mesh(keep(g),m);parent.add(x);return x;};
 const cylinder=(rt,rb,h,m,parent)=>mesh(new T.CylinderGeometry(rt,rb,h,48),m,parent);
 const box=(x,y,z,m,parent)=>mesh(new T.BoxGeometry(x,y,z),m,parent);
 const ring=(r,t,m,y,parent=scene)=>{const x=mesh(new T.TorusGeometry(r,t,8,128),m,parent);x.rotation.x=Math.PI/2;x.position.y=y;return x;};
 const floor=cylinder(3.8,4,.24,dark);floor.position.y=-.2;
 ring(3.8,.028,glow,-.05);ring(4.35,.012,glow,-.25);
 const grid=new T.GridHelper(24,32,0x326781,0x142e41);grid.position.y=-.34;scene.add(grid);keep(grid.geometry);keep(grid.material);
 // Il basamento resta in sezione per rendere visibile la meccanica.
 const wallMat=keep(new T.MeshStandardMaterial({color:0x53798c,transparent:true,opacity:.12,side:T.DoubleSide,depthWrite:false,metalness:.3,roughness:.4}));
 const wall=mesh(new T.CylinderGeometry(3.35,3.35,1.55,64,1,true),wallMat);wall.position.y=.8;
 ring(3.36,.07,metal,1.58);ring(3.36,.045,metal,.04);
 const shellMat=keep(new T.MeshStandardMaterial({color:0xc0d4df,metalness:.38,roughness:.35,transparent:true,opacity:.075,side:T.DoubleSide,depthWrite:false}));
 const shellGeo=keep(new T.SphereGeometry(3.35,48,24,0,Math.PI*2,0,Math.PI/2));
 shell=new T.Mesh(shellGeo,shellMat);shell.position.y=1.6;scene.add(shell);
 const wireMat=keep(new T.MeshBasicMaterial({color:0x73cee0,wireframe:true,transparent:true,opacity:.24,depthWrite:false}));
 shellGrid=mesh(new T.SphereGeometry(3.36,24,12,0,Math.PI*2,0,Math.PI/2),wireMat);shellGrid.position.y=1.6;
 // Arco di giunzione sulla cupola, visibile anche nella vista esterna.
 roofRibs=new T.Group();scene.add(roofRibs);
 for(const z of [-.18,.18]){const pts=[];for(let i=0;i<=64;i++){const a=i/64*Math.PI;pts.push(new T.Vector3(Math.cos(a)*3.355,1.6+Math.sin(a)*3.355,z));}const curve=new T.CatmullRomCurve3(pts);mesh(new T.TubeGeometry(curve,64,.025,5,false),metal,roofRibs);}
 model=new T.Group();scene.add(model);
 const pier=cylinder(.38,.5,1.8,metal,model);pier.position.y=.94;ring(.5,.045,dark,.17,model);
 const foot=cylinder(.85,.95,.12,dark,model);foot.position.y=.03;
 for(let i=0;i<3;i++){const a=i/3*Math.PI*2;const leg=box(.16,.15,1.35,metal,model);leg.position.set(Math.cos(a)*.55,.16,Math.sin(a)*.55);leg.rotation.y=-a+Math.PI/2;}
 const mount=box(.8,.52,.75,dark,model);mount.position.y=2.04;
 const axis=cylinder(.27,.27,1.3,metal,model);axis.position.set(0,2.45,0);axis.rotation.z=-.7;
 const head=box(.6,.45,.6,orange,model);head.position.set(.32,2.78,0);
 const shaft=cylinder(.045,.045,1.4,metal,model);shaft.rotation.z=-.7;shaft.position.set(-.42,1.96,0);
 const weight=cylinder(.32,.32,.28,dark,model);weight.rotation.z=-.7;weight.position.set(-.82,1.51,0);
 const tube=new T.Group();tube.position.set(.38,3.07,0);tube.rotation.set(.1,0,-.86);model.add(tube);
 cylinder(.47,.47,2.1,white,tube);
 for(const y of [-.68,.68]){const collar=cylinder(.5,.5,.13,dark,tube);collar.position.y=y;}
 const rail=box(.15,1.7,.12,orange,tube);rail.position.z=.48;
 const aperture=cylinder(.46,.46,.19,dark,tube);aperture.position.y=1.1;
 const glass=cylinder(.405,.405,.016,lens,tube);glass.position.y=1.205;
 const rim=mesh(new T.TorusGeometry(.45,.026,8,48),metal,tube);rim.rotation.x=Math.PI/2;rim.position.y=1.2;
 const obstruction=cylinder(.115,.115,.07,dark,tube);obstruction.position.y=1.25;
 const cameraBody=cylinder(.24,.24,.4,orange,tube);cameraBody.position.y=-1.25;
 const cameraBack=cylinder(.22,.22,.08,dark,tube);cameraBack.position.y=-1.48;
 const finder=cylinder(.085,.085,.72,dark,tube);finder.position.set(.5,.25,0);
 const computer=box(.55,.12,.4,orange,tube);computer.position.set(-.5,-.25,0);
 const cablePts=[new T.Vector3(.55,1.8,.25),new T.Vector3(.8,2,.6),new T.Vector3(.9,2.7,.5),new T.Vector3(.45,2.8,.2)];mesh(new T.TubeGeometry(new T.CatmullRomCurve3(cablePts),24,.025,5,false),dark,model);
 // Costellazione di sfondo: una sola draw call.
 let seed=31;const random=()=>((seed=(seed*1664525+1013904223)>>>0)/4294967296);const points=new Float32Array(450*3);
 for(let i=0;i<450;i++)points.set([(random()-.5)*70,random()*35+3,(random()-.5)*70],i*3);
 const starGeo=keep(new T.BufferGeometry());starGeo.setAttribute('position',new T.BufferAttribute(points,3));stars=new T.Points(starGeo,keep(new T.PointsMaterial({color:0x90b8cc,size:.055,transparent:true,opacity:.65})));scene.add(stars);

 return {
   update({view}) {
     const exterior=view==='exterior';
     const neutral=view==='neutral';
     shell.visible=shellGrid.visible=roofRibs.visible=model.visible=wall.visible=!neutral;
     shell.material.opacity=exterior?1:.075;
     shell.material.transparent=!exterior; shell.material.depthWrite=exterior;
     wall.material.opacity=exterior?1:.12;
     wall.material.transparent=!exterior; wall.material.depthWrite=exterior;
     shellGrid.material.opacity=exterior?.08:.24;
   }
 };
}
