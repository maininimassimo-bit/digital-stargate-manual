// Trusted Windows-local executor. No eval, imports of History or network API.
// M27-specific empirical recipe: owner review required, no photometric claim.
function DSGRunM27Nonlinear(m,rgb,lum,apply,save,event,checkCancel) {
   var prefix='DSG_'+m.jobId+'_';
   function clone(w,suffix) {
      checkCancel();
      var id=prefix+suffix;
      if(!ImageWindow.windowById(id).isNull) throw Error('Work view already exists');
      var im=w.mainView.image,out=new ImageWindow(im.width,im.height,im.numberOfNominalChannels,32,true,im.isColor,id);
      out.mainView.beginProcess();
      try {out.mainView.image.assign(im);} finally {out.mainView.endProcess();}
      out.keywords=w.keywords;
      w.mainView.properties.forEach(function(key) {
         if(key==='Image:Id' || key.indexOf('XISF:')===0) return;
         out.mainView.setPropertyValue(key,w.mainView.propertyValue(key));
         out.mainView.setPropertyAttributes(key,w.mainView.propertyAttributes(key));
      });
      if(w.hasAstrometricSolution) out.regenerateAstrometricSolution();
      event('derived-copy',{target:id,dependencies:[w.mainView.id]});
      return out;
   }
   function run(p,w,label,deps) {apply(p,w,label,deps || [w.mainView.id]);}
   function roi(p,background) {
      var width=rgb.mainView.image.width,height=rgb.mainView.image.height;
      var x0=Math.round(width*0.022),y0=Math.round(height*0.036),x1=Math.round(width*0.216),y1=Math.round(height*0.231);
      if(background) {p.backgroundUseROI=true;p.backgroundROIX0=x0;p.backgroundROIY0=y0;p.backgroundROIX1=x1;p.backgroundROIY1=y1;}
      else {p.useROI=true;p.roiX0=x0;p.roiY0=y0;p.roiX1=x1;p.roiY1=y1;}
   }
   function pm(w,expression,label,deps) {
      var p=new PixelMath;p.expression=expression;p.useSingleExpression=true;
      p.createNewImage=false;p.rescale=false;p.truncate=true;p.use64BitWorkingImage=true;
      run(p,w,label,deps);
   }
   function masked(w,mask,inverted,fn) {
      w.mask=mask;w.maskEnabled=true;w.maskVisible=false;w.maskInverted=inverted;
      event('mask-attached',{target:w.mainView.id,mask:mask.mainView.id,inverted:inverted});
      try {fn();} finally {w.removeMask();event('mask-detached',{target:w.mainView.id});}
   }
   function separate(w,suffix,label) {
      var before=ImageWindow.windows.map(function(x){return x.mainView.id;});
      var p=new StarXTerminator;p.output_stars=true;p.unscreen=false;
      run(p,w,label);
      var fresh=ImageWindow.windows.filter(function(x){return before.indexOf(x.mainView.id)<0;});
      if(fresh.length!==1) throw Error('Unique stars output required');
      fresh[0].mainView.id=prefix+suffix;
      event('secondary-output',{target:fresh[0].mainView.id,dependencies:[w.mainView.id],action:label});
      return fresh[0];
   }
   [rgb,lum].forEach(function(w,k) {
      var p=new AutomaticBackgroundExtractor;p.polyDegree=2;p.tolerance=0.8;p.boxSize=m.background.boxSize;p.boxSeparation=m.background.boxSeparation;
      p.targetCorrection=AutomaticBackgroundExtractor.Correction_Subtract;p.normalize=true;p.discardModel=true;p.replaceTarget=true;
      run(p,w,'radial-'+(k?'L':'RGB'));
   });
   var p=new BlurXTerminator;p.correct_only=true;run(p,rgb,'optical-RGB');
   p=new BackgroundNeutralization;roi(p,false);p.backgroundHigh=0.05;run(p,rgb,'neutralize-RGB');
   p=new ColorCalibration;p.structureDetection=true;p.structureLayers=6;p.noiseLayers=2;p.whiteLow=0;p.whiteHigh=0.65;roi(p,true);p.backgroundHigh=0.05;
   run(p,rgb,'calibrate-RGB');
   [rgb,lum].forEach(function(w,k) {
      var bx=new BlurXTerminator;bx.correct_only=false;bx.sharpen_stars=0.25;bx.sharpen_nonstellar=k?0.50:0.45;bx.adjust_star_halos=0;
      run(bx,w,'deconvolve-'+(k?'L':'RGB'));
   });
   [rgb,lum].forEach(function(w,k) {
      var nx=new NoiseXTerminator;nx.denoise=k?0.65:0.70;nx.denoise_intensity=0.65;nx.denoise_color=0.80;
      nx.enable_color_separation=!k;nx.enable_frequency_separation=false;nx.iterations=2;
      run(nx,w,'denoise-'+(k?'L':'RGB'));save(w,(k?'L':'RGB')+'-processed-linear.xisf');
   });
   var stars=separate(rgb,'stars','separate-RGB');
   separate(lum,'Lstars','separate-L');
   save(rgb,'RGB-starless-linear.xisf');save(lum,'L-starless-linear.xisf');save(stars,'stars-linear.xisf');
   var med=stars.mainView.computeOrFetchProperty('Median'),background=[med.at(0),med.at(1),med.at(2)];
   [rgb,lum].forEach(function(w,k) {
      var ms=new MaskedStretch;ms.targetBackground=0.085;ms.numberOfIterations=150;ms.clippingFraction=0.00001;
      roi(ms,false);ms.backgroundLow=0;ms.backgroundHigh=0.05;ms.maskType=MaskedStretch.MaskType_Intensity;
      run(ms,w,'stretch-'+(k?'L':'RGB'));
   });
   var mask=clone(lum,'mask');pm(mask,'min(1,max(0,($T-0.115)/0.40))','mask-build');save(mask,'mask.xisf',true);
   masked(rgb,mask,true,function() {
      var c=new CurvesTransformation;c.K=[[0,0],[1,1]];c.S=[[0,0],[0.20,0.07],[0.50,0.18],[0.80,0.30],[1,0.40]];
      run(c,rgb,'background-color',[rgb.mainView.id,mask.mainView.id]);
   });
   masked(lum,mask,false,function() {
      var h=new LocalHistogramEqualization;h.radius=96;h.slopeLimit=1.6;h.amount=0.22;
      run(h,lum,'contrast-large',[lum.mainView.id,mask.mainView.id]);
      h=new LocalHistogramEqualization;h.radius=48;h.slopeLimit=1.6;h.amount=0.28;
      run(h,lum,'contrast-small',[lum.mainView.id,mask.mainView.id]);
      var c=new CurvesTransformation;c.K=[[0,0],[0.2,0.16],[0.4,0.35],[0.6,0.62],[0.8,0.85],[1,1]];
      run(c,lum,'contrast-curve',[lum.mainView.id,mask.mainView.id]);
   });
   save(lum,'L-nonlinear.xisf',true);save(rgb,'RGB-nonlinear.xisf',true);
   var result=clone(rgb,'final');
   p=new LRGBCombination;p.channels=[[false,'',1],[false,'',1],[false,'',1],[true,lum.mainView.id,1]];
   p.mL=0.5;p.mc=0.5;p.clipHighlights=true;p.noiseReduction=false;
   run(p,result,'LRGB-combine',[rgb.mainView.id,lum.mainView.id]);
   masked(result,mask,false,function() {
      var c=new CurvesTransformation;c.K=[[0,0],[1,1]];c.S=[[0,0],[0.15,0.21],[0.4,0.53],[0.65,0.78],[1,1]];
      run(c,result,'nebula-color',[result.mainView.id,mask.mainView.id]);
   });
   p=new PixelMath;p.useSingleExpression=false;p.createNewImage=false;p.rescale=false;p.truncate=true;p.use64BitWorkingImage=true;
   p.expression='max(0,$T[0]-'+background[0]+')';p.expression1='max(0,$T[1]-'+background[1]+')';p.expression2='max(0,$T[2]-'+background[2]+')';
   run(p,stars,'stars-background');
   p=new ArcsinhStretch;p.stretch=150;p.blackPoint=0;p.protectHighlights=true;p.useRGBWS=true;p.previewClipped=false;
   run(p,stars,'stars-stretch');
   p=new CurvesTransformation;p.K=[[0,0],[1,1]];p.S=[[0,0],[0.2,0.25],[0.5,0.58],[0.8,0.85],[1,1]];
   run(p,stars,'stars-color');save(stars,'stars-nonlinear.xisf',true);
   pm(result,'1-(1-$T)*(1-'+stars.mainView.id+')','stars-recombine',[result.mainView.id,stars.mainView.id]);
   result.keywords=result.keywords.filter(function(k){return ['FILTER','IMAGETYP','EXPTIME'].indexOf(k.name)<0;}).concat([
      new FITSKeyword('FILTER',"'LRGB'",'RGB with L luminance'),
      new FITSKeyword('IMAGETYP',"'Processed LRGB'",'Nonlinear local pilot; Owner review required')]);
   result.mainView.setPropertyValue('Instrument:Filter:Name','LRGB');
   result.mainView.setPropertyValue('Image:Type','Processed nonlinear LRGB');
   result.mainView.deleteProperty('PCL:TotalExposureTime');
   result.mainView.deleteProperty('Instrument:ExposureTime');
   event('metadata-updated',{target:result.mainView.id,combinedFilter:true,aggregateExposureNotAsserted:true});
   save(result,'LRGB-nonlinear.xisf',true);result.show();result.bringToFront();
}
function DSGExecuteLocalPilot(m) {
   function require(ok, message) { if(!ok) throw Error(message); }
   function hash(path) { return (new CryptographicHash(CryptographicHash.SHA256)).hash(File.readFile(path)).toHex(); }
   function write(path, value) {
      require(!File.exists(path), 'Receipt already exists');
      var f=new File;
      f.createForWriting(path);
      try { f.write(ByteArray.stringToUTF8(JSON.stringify(value,null,2))); }
      finally { f.close(); }
   }
   require(m.schemaVersion==='1.0' && /^[A-Za-z][A-Za-z0-9_]{0,47}$/.test(m.jobId), 'Invalid manifest');
   require(m.recipe==='LRGB_LINEAR_PREP_V1' || m.recipe==='M27_LRGB_NONLINEAR_V1', 'Recipe not allowed');
   var nonlinear=m.recipe==='M27_LRGB_NONLINEAR_V1';
   require(m.jobDirectory===m.workerRoot+'/'+m.jobId, 'Invalid job directory');
   require(m.inputs.length===4, 'Four inputs required');
   require(m.runtimeLibrary===m.jobDirectory+'/executor.jsh' && /^[a-f0-9]{64}$/.test(m.runtimeSha256), 'Runtime snapshot required');
   require(/^[a-f0-9]{32}$/.test(m.token), 'Invalid reservation token');
   var root=m.jobDirectory, roles=['R','G','B','L'];
   roles.forEach(function(role,k) {
      var i=m.inputs[k];
      require(i.role===role && i.path===root+'/inputs/'+role+'.xisf', 'Input escaped job');
      require(/^[a-f0-9]{64}$/.test(i.sha256), 'Invalid input digest');
      require(Number.isInteger(i.imageIndex) && i.imageIndex>=0 && i.imageIndex<16, 'Explicit image index required');
      require(Number.isInteger(i.width) && Number.isInteger(i.height) && i.width>0 && i.height>0 && i.width<=12000 && i.height<=12000, 'Invalid dimensions');
   });
   require(Object.keys(m.background).sort().join(',')==='boxSeparation,boxSize,polyDegree', 'Unknown background parameters');
   [['polyDegree',0,2],['boxSize',5,32],['boxSeparation',5,64]].forEach(function(b) {
      require(Number.isInteger(m.background[b[0]]) && m.background[b[0]]>=b[1] && m.background[b[0]]<=b[2], 'Parameter outside bounds');
   });
   require(!File.exists(root+'/terminal.json') && !File.exists(root+'/events/0000-started.json'), 'Job already executed; replay refused');
   // Windows native exclusive handle remains held across all pixel operations.
   var lease=new File;
   lease.openForReadWrite(m.workerRoot+'/active-job.json');
   var eventOrdinal=0, executed=0, outputs=[], targets=[], originals=[];
   var terminal={schemaVersion:'1.0',jobId:m.jobId,token:m.token,status:'FAILED',recipe:m.recipe,
      startedAt:new Date().toISOString(),processCount:0,outputs:outputs,providerRequests:0,
      pixInsightVersion:[CoreApplication.versionMajor,CoreApplication.versionMinor,CoreApplication.versionRelease].join('.')+' build '+CoreApplication.versionBuild};
   function event(label,data) {
      var ordinal=('0000'+eventOrdinal++).slice(-4);
      write(root+'/events/'+ordinal+'-'+label+'.json', {at:new Date().toISOString(),event:label,jobId:m.jobId,data:data});
   }
   function checkCancel() {
      if(File.exists(root+'/cancel.json')) {
         var marker=JSON.parse(File.readTextFile(root+'/cancel.json'));
         require(marker.jobId===m.jobId && marker.token===m.token && marker.requested===true, 'Cancellation identity mismatch');
         throw Error('DSG_CANCEL_REQUESTED');
      }
   }
   function apply(process,window,label,dependencies) {
      checkCancel();
      event('process-started',{label:label,target:window.mainView.id,dependencies:dependencies,nativeSource:process.toSource()});
      require(process.executeOn(window.mainView), 'Native process failed: '+label);
      executed++;
      event('process-completed',{label:label,target:window.mainView.id,historyIndex:window.mainView.historyIndex});
   }
   function save(window,name,nonLinear) {
      checkCancel();
      var path=root+'/outputs/'+name;
      require(!File.exists(path), 'Output already exists');
      require(window.saveAs(path,false,false,true,false), 'Native save failed');
      outputs.push({name:name,sha256:hash(path),viewId:window.mainView.id,
         width:window.mainView.image.width,height:window.mainView.image.height,
         channels:window.mainView.image.numberOfNominalChannels,nonLinear:nonLinear===true});
      event('checkpoint',outputs[outputs.length-1]);
   }
   try {
      var reservation=JSON.parse(lease.read(DataType.ByteArray,lease.size).utf8ToString());
      require(reservation.jobId===m.jobId && reservation.token===m.token, 'Reservation mismatch');
      var conflictingHandle=null, denied=false;
      try { conflictingHandle=new File; conflictingHandle.openForReadWrite(m.workerRoot+'/active-job.json'); }
      catch(error) { denied=true; }
      if(conflictingHandle!==null && conflictingHandle.isOpen) conflictingHandle.close();
      require(denied, 'Native exclusive lease not enforced on this platform');
      terminal.exclusiveLeaseVerified=true;
      require(hash(m.runtimeLibrary)===m.runtimeSha256, 'Runtime snapshot integrity mismatch');
      terminal.runtimeSha256=m.runtimeSha256;
      // Check again after acquiring the exclusive lease.
      require(!File.exists(root+'/events/0000-started.json'), 'Job already claimed');
      event('started',{recipe:m.recipe});
      Console.show(); Console.writeln('DSG local pilot: '+m.jobId); Console.abortEnabled=true;
      checkCancel();
      // All constructors must be available before any work copy is processed.
      var abe=new AutomaticBackgroundExtractor, cc=new ChannelCombination;
      if(nonlinear) {
         // Fail before pixel processing if any required native module is missing.
         [new BlurXTerminator,new NoiseXTerminator,new StarXTerminator,
          new BackgroundNeutralization,new ColorCalibration,new MaskedStretch,
          new PixelMath,new LocalHistogramEqualization,new CurvesTransformation,
          new LRGBCombination,new ArcsinhStretch];
         require(m.inputs[0].width>=1000 && m.inputs[0].height>=800,'M27 recipe minimum geometry');
      }
      for(var k=0;k<4;++k) {
         var input=m.inputs[k];
         require(hash(input.path)===input.sha256 && hash(input.sourcePath)===input.sha256, 'Input/source digest mismatch');
         var ws=ImageWindow.open(input.path);
         require(input.imageIndex<ws.length, 'Selected container image missing');
         var selected=ws[input.imageIndex], im=selected.mainView.image;
         require(im.width===input.width && im.height===input.height && !im.isColor && im.numberOfNominalChannels===1, 'Selected master incompatible');
         require(!selected.isModified && im.isReal && im.bitsPerSample===32, 'Unmodified Float32 master required');
         originals.push(selected);
         var id='DSG_'+m.jobId+'_'+roles[k];
         require(ImageWindow.windowById(id).isNull, 'Work view already exists');
         var copy=new ImageWindow(im.width,im.height,1,32,true,false,id);
         copy.mainView.beginProcess();
         try {copy.mainView.image.assign(im);} finally {copy.mainView.endProcess();}
         copy.keywords=selected.keywords;
         // Properties are kept private with the XISF; use upstream metadata on copies.
         selected.mainView.properties.forEach(function(key) {
            if(key==='Image:Id' || key.indexOf('XISF:')===0) return;
            copy.mainView.setPropertyValue(key,selected.mainView.propertyValue(key));
            copy.mainView.setPropertyAttributes(key,selected.mainView.propertyAttributes(key));
         });
         if(selected.hasAstrometricSolution) copy.regenerateAstrometricSolution();
         targets.push(copy);
         event('copy-created',{role:roles[k],sourceDigest:input.sha256,imageIndex:input.imageIndex,target:id});
      }
      for(var k=0;k<4;++k) {
         abe=new AutomaticBackgroundExtractor;
         abe.polyDegree=m.background.polyDegree; abe.boxSize=m.background.boxSize;
         abe.boxSeparation=m.background.boxSeparation;
         abe.targetCorrection=AutomaticBackgroundExtractor.Correction_Subtract;
         abe.normalize=true; abe.discardModel=true; abe.replaceTarget=true;
         apply(abe,targets[k],'background-'+roles[k],[m.inputs[k].sha256]);
         save(targets[k],roles[k]+'-linear.xisf');
      }
      checkCancel();
      cc.channels=[[true,targets[0].mainView.id],[true,targets[1].mainView.id],[true,targets[2].mainView.id]];
      event('process-started',{label:'RGB-composition',dependencies:targets.slice(0,3).map(function(w){return w.mainView.id;}),nativeSource:cc.toSource()});
      require(cc.executeGlobal(),'RGB composition failed'); executed++;
      var rgb=ImageWindow.activeWindow;
      require(!rgb.isNull && rgb.mainView.image.numberOfNominalChannels===3,'RGB output missing');
      rgb.mainView.id='DSG_'+m.jobId+'_RGB';
      // P2 compatibility; P3 retains native combination metadata rather than
      // attributing RGB to the Red filter/exposure. Astrometry is inherited by CC.
      if(!nonlinear) rgb.keywords=targets[0].keywords;
      if(nonlinear && targets[0].hasAstrometricSolution)
         require(rgb.hasAstrometricSolution,'Combined RGB astrometry missing');
      event('process-completed',{label:'RGB-composition',target:rgb.mainView.id});
      save(rgb,'RGB-linear.xisf');
      if(nonlinear) DSGRunM27Nonlinear(m,rgb,targets[3],apply,save,event,checkCancel);
      rgb.show();
      terminal.status='COMPLETED';
   } catch(error) {
      terminal.status=String(error).indexOf('DSG_CANCEL_REQUESTED')>=0?'CANCELLED':'FAILED';
      terminal.error=String(error);
      Console.criticalln('DSG '+terminal.status+': '+terminal.error);
   } finally {
      terminal.processCount=executed;
      terminal.originalViewsUnmodified=originals.every(function(w){return !w.isModified;});
      try {
         require(m.inputs.every(function(i){return hash(i.path)===i.sha256 && hash(i.sourcePath)===i.sha256;}),'Final input/source integrity mismatch');
         require(terminal.originalViewsUnmodified,'Input view modified');
      } catch(error) {terminal.status='FAILED';terminal.integrityError=String(error);}
      terminal.finishedAt=new Date().toISOString();
      try {write(root+'/terminal.json',terminal);} finally {lease.close();}
      Console.writeln('DSG terminal: '+terminal.status+'; processes: '+executed);
   }
   return terminal;
}
