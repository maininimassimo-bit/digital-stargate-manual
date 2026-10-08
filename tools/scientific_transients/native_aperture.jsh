// Trusted local entry only; caller supplies local files, never a portal payload.
// Include installed AperturePhotometryEngine.js with SETTINGS_MODULE defined.
function DSGNativeAperture(m) {
   function need(ok, code) { if (!ok) throw Error(code); }
   function fields(v, names) { need(v && typeof v==='object' && !Array.isArray(v) && Object.keys(v).sort().join(',')===names.slice().sort().join(','),'NATIVE_FIELDS'); }
   function sha(path) { return new CryptographicHash(CryptographicHash.SHA256).hash(File.readFile(path)).toHex(); }
   function finite(v) { return typeof v==='number' && Number.isFinite(v); }
   function opaque(v) { return typeof v==='string' && /^[a-f0-9]{32}$/.test(v); }
   fields(m,['protocol','runDirectory','operationRef','input','parameters','runtime','targets']);
   need(m.protocol==='DSG_NATIVE_APERTURE_V1' && opaque(m.operationRef),'NATIVE_IDENTITY');
   need(typeof m.runDirectory==='string' && /^[A-Za-z]:[/]/.test(m.runDirectory) && m.runDirectory.indexOf('..')<0 && m.runDirectory.indexOf('\\')<0 && !/["\x00-\x1f]/.test(m.runDirectory),'NATIVE_LOCAL_ROOT');
   fields(m.input,['sha256','imageIndex','width','height','channels','linearity']);
   need(/^[a-f0-9]{64}$/.test(m.input.sha256) && Number.isInteger(m.input.imageIndex) && m.input.imageIndex>=0 && m.input.imageIndex<16,'NATIVE_INPUT');
   need(Number.isInteger(m.input.width) && Number.isInteger(m.input.height) && m.input.width>0 && m.input.height>0 && m.input.width*m.input.height<=100000000 && m.input.channels===1 && m.input.linearity==='DECLARED_LINEAR_NOT_ATTESTED','NATIVE_GEOMETRY');
   fields(m.parameters,['coordinateConvention','apertureRadius','annulusInner','annulusOuter']);
   need(m.parameters.coordinateConvention==='PI_NATIVE_GEOMETRIC' && finite(m.parameters.apertureRadius) && m.parameters.apertureRadius>0 && m.parameters.apertureRadius<=512 && finite(m.parameters.annulusInner) && finite(m.parameters.annulusOuter) && m.parameters.annulusInner>1 && m.parameters.annulusOuter>m.parameters.annulusInner && m.parameters.annulusOuter<=16,'NATIVE_PARAMETERS');
   fields(m.runtime,['librarySha256','engineSha256','catalogSha256','pixInsightVersion']);
   ['librarySha256','engineSha256','catalogSha256'].forEach(function(k){need(/^[a-f0-9]{64}$/.test(m.runtime[k]),'NATIVE_RUNTIME');});
   need(Array.isArray(m.targets) && m.targets.length>0 && m.targets.length<=1024,'NATIVE_TARGETS');
   var ids={};m.targets.forEach(function(t){fields(t,['sourceRef','x','y']);need(opaque(t.sourceRef) && !ids[t.sourceRef] && finite(t.x) && finite(t.y) && t.x>=0 && t.y>=0 && t.x<m.input.width && t.y<m.input.height,'NATIVE_TARGET');ids[t.sourceRef]=true;});
   var root=m.runDirectory, owned=[], rows=[], window=null, terminal=null;
   var engine='C:/Program Files/PixInsight/src/scripts/AperturePhotometry/AperturePhotometryEngine.js';
   var catalog='C:/Program Files/PixInsight/src/scripts/AperturePhotometry/AperturePhotometryCatalogs.js';
   function write(name,value) { need(!File.exists(root+'/'+name),'NATIVE_NO_OVERWRITE');File.writeTextFile(root+'/'+name,JSON.stringify(value,null,2)); }
   function versions() { return [CoreApplication.versionMajor,CoreApplication.versionMinor,CoreApplication.versionRelease].join('.')+' build '+CoreApplication.versionBuild; }
   function runtime() { need(versions()===m.runtime.pixInsightVersion && sha(root+'/native_aperture.jsh')===m.runtime.librarySha256 && sha(engine)===m.runtime.engineSha256 && sha(catalog)===m.runtime.catalogSha256,'NATIVE_RUNTIME_CHANGED'); }
   function cancel() { if(File.exists(root+'/cancel.json')) {var c=JSON.parse(File.readTextFile(root+'/cancel.json'));fields(c,['operationRef','requested']);need(c.operationRef===m.operationRef && c.requested===true,'NATIVE_CANCEL_IDENTITY');throw Error('NATIVE_CANCEL_REQUESTED');} }
   function history(prefix) {
      need(!File.exists(root+'/'+prefix+'-initial.js') && !File.exists(root+'/'+prefix+'-current.js'),'NATIVE_NO_OVERWRITE');
      File.writeTextFile(root+'/'+prefix+'-initial.js',window.mainView.initialProcessing.toSource('JavaScript','DSGApertureInitial',0,0));
      File.writeTextFile(root+'/'+prefix+'-current.js',window.mainView.processing.toSource('JavaScript','DSGApertureCurrent',0,0));
   }
   need(!File.exists(root+'/started.json') && !File.exists(root+'/terminal.json'),'NATIVE_REPLAY_REFUSED');
   try {
      runtime();cancel();need(sha(root+'/input.xisf')===m.input.sha256,'NATIVE_INPUT_CHANGED');
      need(JSON.stringify(JSON.parse(File.readTextFile(root+'/parameters.json')))===JSON.stringify(m),'NATIVE_PARAMETERS_CHANGED');
      var parametersSha=sha(root+'/parameters.json');
      write('started.json',{operationRef:m.operationRef,at:new Date().toISOString(),runtime:m.runtime,input:m.input,parameters:m.parameters,targets:m.targets});
      owned=ImageWindow.open(root+'/input.xisf');need(owned.length>m.input.imageIndex,'NATIVE_IMAGE_INDEX');window=owned[m.input.imageIndex];
      var image=window.mainView.image;
      need(!image.isComplex && image.width===m.input.width && image.height===m.input.height && image.numberOfNominalChannels===1,'NATIVE_IMAGE_GEOMETRY');
      image.selectedChannel=0;
      var pixels=PhotometryPixels.FromImage(image),before=pixels.data.slice();
      for(var i=0;i<before.length;i++)need(Number.isFinite(before[i]),'NATIVE_NONFINITE_INPUT');
      history('input');
      var q={psfMode:false,annulusBackground:true,stabilizedBackground:false,growth:1,apertureRadius:m.parameters.apertureRadius,annulusInner:m.parameters.annulusInner,annulusOuter:m.parameters.annulusOuter};
      m.targets.forEach(function(t){
         cancel();
         var result=PhotometryPixels.Measure(pixels,{x:t.x,y:t.y,hasPSF:false,fwtmX:0,fwtmY:0,theta:0,B:0,srectSide:0},q);
         if(!result.clipped) ['flux','area','background','peak','noise','localCount'].forEach(function(k){need(Number.isFinite(result[k]),'NATIVE_NONFINITE_RESULT');});
         var available=!result.clipped && result.localCount>0;
         var row={sourceRef:t.sourceRef,x:t.x,y:t.y,clipped:result.clipped,backgroundAvailable:available,fluxNormalizedSampleSum:available?result.flux:null,area:result.clipped?null:result.area,background:available?result.background:null,skyNoiseDiagnostic:available?result.noise:null,skySampleCount:result.clipped?0:result.localCount,fullVariance:null,significance:null,scienceValidation:'NOT_VALIDATED'};
         rows.push(row);write('measurement-'+('00000'+rows.length).slice(-5)+'.json',row);
      });
      var changed=0;for(var k=0;k<before.length;k++)if(before[k]!==pixels.data[k])changed++;
      need(changed===0,'NATIVE_PIXELS_CHANGED');runtime();need(sha(root+'/input.xisf')===m.input.sha256 && sha(root+'/parameters.json')===parametersSha,'NATIVE_INPUT_OR_PARAMETERS_CHANGED');cancel();
      need(!File.exists(root+'/checkpoint.xisf'),'NATIVE_NO_OVERWRITE');need(window.saveAs(root+'/checkpoint.xisf',false,false,true,false),'NATIVE_CHECKPOINT_SAVE');history('checkpoint');
      terminal={protocol:m.protocol,operationRef:m.operationRef,state:'COMPLETED',runtime:m.runtime,inputSha256:m.input.sha256,imageIndex:m.input.imageIndex,rows:rows,changedPixels:changed,checkpointSha256:sha(root+'/checkpoint.xisf'),historySha256:sha(root+'/checkpoint-current.js'),parametersSha256:sha(root+'/parameters.json'),scienceValidation:'NOT_VALIDATED',unit:'NORMALIZED_SAMPLE_SUM',fullAperturePhotometryWorkflowExecuted:false,providerRequestsInvoked:0};
   } catch(e) {
      var retained=[];
      if(window!==null){try{need(!File.exists(root+'/failed-checkpoint.xisf'),'NATIVE_NO_OVERWRITE');need(window.saveAs(root+'/failed-checkpoint.xisf',false,false,true,false),'NATIVE_CHECKPOINT_SAVE');history('failed');retained.push('failed-checkpoint.xisf','failed-initial.js','failed-current.js');}catch(saveError){retained.push('NOT_SAVED');}}
      terminal={protocol:m.protocol,operationRef:m.operationRef,state:e && e.message==='NATIVE_CANCEL_REQUESTED'?'CANCELLED':'FAILED',rows:rows,retained:retained,error:String(e).slice(0,1024),scienceValidation:'NOT_VALIDATED'};
   } finally {
      if(terminal!==null)write('terminal.json',terminal);
      owned.forEach(function(w){w.forceClose();});
   }
   return terminal;
}
