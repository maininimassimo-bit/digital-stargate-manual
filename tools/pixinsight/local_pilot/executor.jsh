// Trusted Windows-local executor. No eval, imports of History or network API.
// M27-specific empirical recipe: owner review required, no photometric claim.
function DSGProcessingSettings(value) {
   if(value===undefined) value={sharpenL:0.50,sharpenRGB:0.45,denoiseL:0.65,denoiseRGB:0.70,contrastLarge:0.22,contrastSmall:0.28,targetBackground:0.085};
   var bounds={sharpenL:[0,0.6],sharpenRGB:[0,0.55],denoiseL:[0.3,0.85],denoiseRGB:[0.3,0.85],contrastLarge:[0,0.4],contrastSmall:[0,0.4],targetBackground:[0.03,0.12]};
   if(!value || Object.keys(value).sort().join(',')!==Object.keys(bounds).sort().join(',')) throw Error('Unknown processing parameters');
   Object.keys(bounds).forEach(function(key){
      if(typeof value[key]!=='number' || !Number.isFinite(value[key]) || value[key]<bounds[key][0] || value[key]>bounds[key][1]) throw Error('Processing parameter outside bounds');
   });
   return value;
}

function DSGFieldSettings(value) {
   var keys=['target','backgroundROI','maskLow','maskHigh','contrastLargeRadius','contrastSmallRadius','starsStretch','saturation'];
   if(!value || Object.keys(value).sort().join(',')!==keys.sort().join(',')) throw Error('Field settings required');
   if(typeof value.target!=='string' || value.target.trim().length<1 || value.target.length>160 || /[\x00-\x1f]/.test(value.target)) throw Error('Field target required');
   var r=value.backgroundROI;
   if(!Array.isArray(r) || r.length!==4 || !r.every(function(n){return typeof n==='number' && Number.isFinite(n) && n>=0 && n<=1;}) || r[2]-r[0]<0.01 || r[3]-r[1]<0.01) throw Error('Reviewed background ROI required');
   [['maskLow',0,0.5],['maskHigh',0.05,1],['starsStretch',10,300],['saturation',0,0.3]].forEach(function(b){if(typeof value[b[0]]!=='number' || !Number.isFinite(value[b[0]]) || value[b[0]]<b[1] || value[b[0]]>b[2]) throw Error('Field parameter outside bounds');});
   if(value.maskHigh-value.maskLow<0.05) throw Error('Mask range required');
   ['contrastLargeRadius','contrastSmallRadius'].forEach(function(k){if(!Number.isInteger(value[k]) || value[k]<8 || value[k]>256) throw Error('Field radius outside bounds');});
   if(value.contrastSmallRadius>value.contrastLargeRadius) throw Error('Field radius order');
   return value;
}

function DSGRunM27Nonlinear(m,rgb,lum,apply,save,event,checkCancel) {
   var settings=DSGProcessingSettings(m.processing);
   var field=m.recipe!=='M27_LRGB_NONLINEAR_V1'?DSGFieldSettings(m.field):null;
   var mode=m.recipe==='OSC_FIELD_NONLINEAR_V1'?'OSC':m.recipe==='SHO_FIELD_NONLINEAR_V1'?'SHO':m.recipe==='HOO_FIELD_NONLINEAR_V1'?'HOO':'LRGB';
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
      var r=field?field.backgroundROI:[0.022,0.036,0.216,0.231];
      var x0=Math.round(width*r[0]),y0=Math.round(height*r[1]),x1=Math.round(width*r[2]),y1=Math.round(height*r[3]);
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
      var p=new AutomaticBackgroundExtractor;p.polyDegree=field?m.background.polyDegree:2;p.tolerance=0.8;p.boxSize=m.background.boxSize;p.boxSeparation=m.background.boxSeparation;
      p.targetCorrection=AutomaticBackgroundExtractor.Correction_Subtract;p.normalize=true;p.discardModel=true;p.replaceTarget=true;
      run(p,w,'radial-'+(k?'L':'RGB'));
   });
   var p=new BlurXTerminator;p.correct_only=true;run(p,rgb,'optical-RGB');
   p=new BackgroundNeutralization;roi(p,false);p.backgroundHigh=0.05;run(p,rgb,'neutralize-RGB');
   if(mode!=='SHO' && mode!=='HOO') {
      p=new ColorCalibration;p.structureDetection=true;p.structureLayers=6;p.noiseLayers=2;p.whiteLow=0;p.whiteHigh=0.65;roi(p,true);p.backgroundHigh=0.05;
      run(p,rgb,'calibrate-RGB');
   }
   [rgb,lum].forEach(function(w,k) {
      var bx=new BlurXTerminator;bx.correct_only=false;bx.sharpen_stars=0.25;bx.sharpen_nonstellar=k?settings.sharpenL:settings.sharpenRGB;bx.adjust_star_halos=0;
      run(bx,w,'deconvolve-'+(k?'L':'RGB'));
   });
   [rgb,lum].forEach(function(w,k) {
      var nx=new NoiseXTerminator;nx.denoise=k?settings.denoiseL:settings.denoiseRGB;nx.denoise_intensity=0.65;nx.denoise_color=0.80;
      nx.enable_color_separation=!k;nx.enable_frequency_separation=false;nx.iterations=2;
      run(nx,w,'denoise-'+(k?'L':'RGB'));save(w,(k?'L':'RGB')+'-processed-linear.xisf');
   });
   var stars=separate(rgb,'stars','separate-RGB');
   separate(lum,'Lstars','separate-L');
   save(rgb,'RGB-starless-linear.xisf');save(lum,'L-starless-linear.xisf');save(stars,'stars-linear.xisf');
   var med=stars.mainView.computeOrFetchProperty('Median'),background=[med.at(0),med.at(1),med.at(2)];
   [rgb,lum].forEach(function(w,k) {
      var ms=new MaskedStretch;ms.targetBackground=settings.targetBackground;ms.numberOfIterations=150;ms.clippingFraction=0.00001;
      roi(ms,false);ms.backgroundLow=0;ms.backgroundHigh=0.05;ms.maskType=MaskedStretch.MaskType_Intensity;
      run(ms,w,'stretch-'+(k?'L':'RGB'));
   });
   var mask=clone(lum,'mask');pm(mask,field?'min(1,max(0,($T-'+field.maskLow+')/'+(field.maskHigh-field.maskLow)+'))':'min(1,max(0,($T-0.115)/0.40))','mask-build');save(mask,'mask.xisf',true);
   masked(rgb,mask,true,function() {
      var c=new CurvesTransformation;c.K=[[0,0],[1,1]];c.S=field?[[0,0],[1,1]]:[[0,0],[0.20,0.07],[0.50,0.18],[0.80,0.30],[1,0.40]];
      run(c,rgb,'background-color',[rgb.mainView.id,mask.mainView.id]);
   });
   masked(lum,mask,false,function() {
      var h=new LocalHistogramEqualization;h.radius=field?field.contrastLargeRadius:96;h.slopeLimit=1.6;h.amount=settings.contrastLarge;
      run(h,lum,'contrast-large',[lum.mainView.id,mask.mainView.id]);
      h=new LocalHistogramEqualization;h.radius=field?field.contrastSmallRadius:48;h.slopeLimit=1.6;h.amount=settings.contrastSmall;
      run(h,lum,'contrast-small',[lum.mainView.id,mask.mainView.id]);
      var c=new CurvesTransformation;c.K=field?[[0,0],[1,1]]:[[0,0],[0.2,0.16],[0.4,0.35],[0.6,0.62],[0.8,0.85],[1,1]];
      run(c,lum,'contrast-curve',[lum.mainView.id,mask.mainView.id]);
   });
   save(lum,'L-nonlinear.xisf',true);save(rgb,'RGB-nonlinear.xisf',true);
   var result=clone(rgb,'final');
   p=new LRGBCombination;p.channels=[[false,'',1],[false,'',1],[false,'',1],[true,lum.mainView.id,1]];
   p.mL=0.5;p.mc=0.5;p.clipHighlights=true;p.noiseReduction=false;
   run(p,result,'LRGB-combine',[rgb.mainView.id,lum.mainView.id]);
   masked(result,mask,false,function() {
      var c=new CurvesTransformation;c.K=[[0,0],[1,1]];c.S=field?[[0,0],[0.5,0.5+field.saturation],[1,1]]:[[0,0],[0.15,0.21],[0.4,0.53],[0.65,0.78],[1,1]];
      run(c,result,'nebula-color',[result.mainView.id,mask.mainView.id]);
   });
   p=new PixelMath;p.useSingleExpression=false;p.createNewImage=false;p.rescale=false;p.truncate=true;p.use64BitWorkingImage=true;
   p.expression='max(0,$T[0]-'+background[0]+')';p.expression1='max(0,$T[1]-'+background[1]+')';p.expression2='max(0,$T[2]-'+background[2]+')';
   run(p,stars,'stars-background');
   p=new ArcsinhStretch;p.stretch=field?field.starsStretch:150;p.blackPoint=0;p.protectHighlights=true;p.useRGBWS=true;p.previewClipped=false;
   run(p,stars,'stars-stretch');
   p=new CurvesTransformation;p.K=[[0,0],[1,1]];p.S=field?[[0,0],[0.5,0.5+field.saturation/2],[1,1]]:[[0,0],[0.2,0.25],[0.5,0.58],[0.8,0.85],[1,1]];
   run(p,stars,'stars-color');save(stars,'stars-nonlinear.xisf',true);
   pm(result,'1-(1-$T)*(1-'+stars.mainView.id+')','stars-recombine',[result.mainView.id,stars.mainView.id]);
   result.keywords=result.keywords.filter(function(k){return ['FILTER','IMAGETYP','EXPTIME'].indexOf(k.name)<0;}).concat([
      new FITSKeyword('FILTER',"'"+mode+"'",mode==='LRGB'?'RGB with L luminance':mode==='OSC'?'OSC with derived luminance':'Assigned narrowband palette; Ha-derived luminance'),
      new FITSKeyword('IMAGETYP',"'Processed "+mode+"'",'Nonlinear local pilot; Owner review required')]);
   result.mainView.setPropertyValue('Instrument:Filter:Name',mode);
   result.mainView.setPropertyValue('Image:Type','Processed nonlinear '+mode);
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
   var fieldRecipes=['LRGB_FIELD_NONLINEAR_V1','OSC_FIELD_NONLINEAR_V1','SHO_FIELD_NONLINEAR_V1','HOO_FIELD_NONLINEAR_V1'];
   require(m.recipe==='LRGB_LINEAR_PREP_V1' || m.recipe==='M27_LRGB_NONLINEAR_V1' || fieldRecipes.indexOf(m.recipe)>=0, 'Recipe not allowed');
   var nonlinear=m.recipe!=='LRGB_LINEAR_PREP_V1';
   if(fieldRecipes.indexOf(m.recipe)>=0) {DSGFieldSettings(m.field);require(m.processing!==undefined,'Reviewed processing settings required');}
   else require(m.field===undefined,'Field settings require field recipe');
   if(nonlinear) DSGProcessingSettings(m.processing);
   else require(m.processing===undefined, 'Processing options require nonlinear recipe');
   require(m.jobDirectory===m.workerRoot+'/'+m.jobId, 'Invalid job directory');
   var roles=m.recipe==='OSC_FIELD_NONLINEAR_V1'?['RGB']:m.recipe==='SHO_FIELD_NONLINEAR_V1'?['SII','Ha','OIII']:m.recipe==='HOO_FIELD_NONLINEAR_V1'?['Ha','OIII']:['R','G','B','L'];
   require(m.inputs.length===roles.length, 'Recipe master count required');
   require(m.runtimeLibrary===m.jobDirectory+'/executor.jsh' && /^[a-f0-9]{64}$/.test(m.runtimeSha256), 'Runtime snapshot required');
   require(/^[a-f0-9]{32}$/.test(m.token), 'Invalid reservation token');
   var root=m.jobDirectory;
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
      for(var k=0;k<roles.length;++k) {
         var input=m.inputs[k];
         require(hash(input.path)===input.sha256 && hash(input.sourcePath)===input.sha256, 'Input/source digest mismatch');
         var ws=ImageWindow.open(input.path);
         require(input.imageIndex<ws.length, 'Selected container image missing');
         var selected=ws[input.imageIndex], im=selected.mainView.image;
         var expectedChannels=m.recipe==='OSC_FIELD_NONLINEAR_V1'?3:1;
         require(im.width===input.width && im.height===input.height && im.isColor===(expectedChannels===3) && im.numberOfNominalChannels===expectedChannels, 'Selected master incompatible');
         require(!selected.isModified && im.isReal && im.bitsPerSample===32, 'Unmodified Float32 master required');
         originals.push(selected);
         var id='DSG_'+m.jobId+'_'+roles[k];
         require(ImageWindow.windowById(id).isNull, 'Work view already exists');
         var copy=new ImageWindow(im.width,im.height,expectedChannels,32,true,expectedChannels===3,id);
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
      for(var k=0;k<roles.length;++k) {
         abe=new AutomaticBackgroundExtractor;
         abe.polyDegree=m.background.polyDegree; abe.boxSize=m.background.boxSize;
         abe.boxSeparation=m.background.boxSeparation;
         abe.targetCorrection=AutomaticBackgroundExtractor.Correction_Subtract;
         abe.normalize=true; abe.discardModel=true; abe.replaceTarget=true;
         apply(abe,targets[k],'background-'+roles[k],[m.inputs[k].sha256]);
         save(targets[k],roles[k]+'-linear.xisf');
      }
      checkCancel();
      var rgb,lum;
      if(m.recipe==='OSC_FIELD_NONLINEAR_V1') {
         rgb=targets[0];
         lum=new ImageWindow(rgb.mainView.image.width,rgb.mainView.image.height,1,32,true,false,'DSG_'+m.jobId+'_L');
         var derived=new PixelMath;derived.expression='0.2126*'+rgb.mainView.id+'[0]+0.7152*'+rgb.mainView.id+'[1]+0.0722*'+rgb.mainView.id+'[2]';
         derived.useSingleExpression=true;derived.createNewImage=false;derived.rescale=false;derived.truncate=false;derived.use64BitWorkingImage=true;
         apply(derived,lum,'derive-L',[rgb.mainView.id]);
         event('derived-luminance',{target:lum.mainView.id,dependencies:[rgb.mainView.id],method:'LINEAR_RGB_WEIGHTED_NOT_PHOTOMETRIC'});
         save(lum,'L-linear.xisf');
      } else {
      var channelIndexes=m.recipe==='SHO_FIELD_NONLINEAR_V1'?[0,1,2]:m.recipe==='HOO_FIELD_NONLINEAR_V1'?[0,1,1]:[0,1,2];
      cc.channels=channelIndexes.map(function(index){return [true,targets[index].mainView.id];});
      event('process-started',{label:'RGB-composition',dependencies:targets.slice(0,3).map(function(w){return w.mainView.id;}),nativeSource:cc.toSource()});
      require(cc.executeGlobal(),'RGB composition failed'); executed++;
      rgb=ImageWindow.activeWindow;
      require(!rgb.isNull && rgb.mainView.image.numberOfNominalChannels===3,'RGB output missing');
      rgb.mainView.id='DSG_'+m.jobId+'_RGB';
      // P2 compatibility; P3 retains native combination metadata rather than
      // attributing RGB to the Red filter/exposure. Astrometry is inherited by CC.
      if(!nonlinear) rgb.keywords=targets[0].keywords;
      if(nonlinear && targets[0].hasAstrometricSolution)
         require(rgb.hasAstrometricSolution,'Combined RGB astrometry missing');
      event('process-completed',{label:'RGB-composition',target:rgb.mainView.id});
      save(rgb,'RGB-linear.xisf');
      if(m.recipe==='SHO_FIELD_NONLINEAR_V1' || m.recipe==='HOO_FIELD_NONLINEAR_V1') {
         var ha=targets[m.recipe==='SHO_FIELD_NONLINEAR_V1'?1:0];
         lum=new ImageWindow(ha.mainView.image.width,ha.mainView.image.height,1,32,true,false,'DSG_'+m.jobId+'_L');
         lum.mainView.beginProcess();try{lum.mainView.image.assign(ha.mainView.image);}finally{lum.mainView.endProcess();}
         event('derived-copy',{target:lum.mainView.id,dependencies:[ha.mainView.id],method:'HA_DERIVED_LUMINANCE'});
         save(lum,'L-linear.xisf');
      } else lum=targets[3];
      }
      if(nonlinear) DSGRunM27Nonlinear(m,rgb,lum,apply,save,event,checkCancel);
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
