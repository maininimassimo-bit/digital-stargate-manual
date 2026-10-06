/* Trusted source-preparation candidate. Requires caller-held native lease.
 * Not connected to portal queue until its own approval/collection contract is validated.
 * AstrometricMetadata, ImageReprojection and MosaicByCoordinatesEngine are installed PJSR dependencies.
 */
function DSGValidateMosaicCanvas(c){
   function require(ok,message){if(!ok)throw Error(message);}
   require(c && Object.keys(c).sort().join(',')==='centerDec,centerRA,height,resolution,rotation,width','Canvas fields');
   ['centerRA','centerDec','resolution','rotation'].forEach(function(key){require(typeof c[key]==='number' && Number.isFinite(c[key]),'Canvas numeric bounds');});
   require(c.centerRA>=0 && c.centerRA<360 && c.centerDec>=-90 && c.centerDec<=90 && c.resolution>0 && c.resolution<=0.01 && Math.abs(c.rotation)<=360,'Canvas coordinate bounds');
   require(Number.isInteger(c.width) && Number.isInteger(c.height) && c.width>=1000 && c.height>=800 && c.width<=12000 && c.height<=12000,'Canvas geometry bounds');
   return c;
}
function DSGPrepareMosaicGroup(spec, record, save, checkCancel) {
   function require(ok,message){if(!ok)throw Error(message);}
   var fields=['canvas','inputs','role','shrink','feather'];
   require(Object.keys(spec).sort().join(',')===fields.sort().join(','),'Mosaic group fields');
   require(['RGB','R','G','B','L','Ha','OIII','SII'].indexOf(spec.role)>=0,'Mosaic role');
   require(Array.isArray(spec.inputs) && spec.inputs.length>=2 && spec.inputs.length<=16,'Mosaic panel count');
   require(Number.isInteger(spec.shrink) && spec.shrink>=0 && spec.shrink<=5,'Mosaic shrink bounds');
   require(Number.isInteger(spec.feather) && spec.feather>=1 && spec.feather<=100,'Mosaic feather bounds');
   var c=DSGValidateMosaicCanvas(spec.canvas);
   var ids={}, channels=spec.role==='RGB'?3:1;
   spec.inputs.forEach(function(item){
      require(Object.keys(item).sort().join(',')==='panelId,window','Selected mosaic input fields');
      require(typeof item.panelId==='string' && /^[A-Za-z0-9_-]{1,40}$/.test(item.panelId) && !ids[item.panelId],'Unique mosaic panel id');
      ids[item.panelId]=true;
      require(item.window && !item.window.isNull && item.window.hasAstrometricSolution,'Solved panel required');
      var im=item.window.mainView.image;
      require(im.isReal && im.bitsPerSample===32 && im.numberOfNominalChannels===channels,'Mosaic panel sample format');
   });
   var engine=new MosaicByCoordinatesEngine;
   engine.centerCoordsAuto=false;engine.centerRA=c.centerRA;engine.centerDec=c.centerDec;
   engine.resolutionAuto=false;engine.resolution=c.resolution;
   engine.rotationAuto=false;engine.rotation=c.rotation;
   engine.projectionAuto=false;engine.projection=Projection.Gnomonic;
   engine.dimensionsAuto=false;engine.width=c.width;engine.height=c.height;
   var reference=engine.CreateMetadata(c.width,c.height);
   var bounds=spec.inputs.map(function(item){
      var metadata=new AstrometricMetadata;metadata.ExtractMetadata(item.window);
      var box=ImageReprojection.reprojectedBounds(reference,metadata);
      require([box.x0,box.y0,box.x1,box.y1].every(Number.isFinite),'Panel projected bounds');
      require(box.x0>=-1 && box.y0>=-1 && box.x1<=c.width+1 && box.y1<=c.height+1,'Canvas clips panel bounds');
      return box;
   });
   // Every panel must belong to the same connected footprint. Bounding overlap is
   // a geometric prerequisite; stellar/seam quality still requires native review.
   var reached=[true];
   for(var pass=0;pass<spec.inputs.length;++pass)
      for(var i=0;i<bounds.length;++i)if(reached[i])
         for(var j=0;j<bounds.length;++j){
            var a=bounds[i],b=bounds[j];
            if(Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0)>32 && Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0)>32)reached[j]=true;
         }
   require(spec.inputs.every(function(_,i){return reached[i];}),'Disconnected mosaic panels');
   var frames=[];
   for(var i=0;i<spec.inputs.length;++i){
      checkCancel();
      var item=spec.inputs[i],warped=null;
      try{
         warped=(new ImageReprojection(InterpolationAlgorithm.Auto,0.3,'_mosaic_grid')).reprojectedImage(reference,item.window);
         require(warped && !warped.isNull && warped.mainView.image.width===c.width && warped.mainView.image.height===c.height,'Reprojection geometry');
         var checkpoint=save(warped,spec.role+'-'+item.panelId+'-registered.xisf');
         require(typeof checkpoint==='string' && checkpoint.endsWith('.xisf'),'Registered checkpoint path');
         frames.push(checkpoint);
         record('astrometric-reprojection',{role:spec.role,panelId:item.panelId,sourceView:item.window.mainView.id,output:checkpoint,canvas:c,method:'PJSR_IMAGE_REPROJECTION_1_4_4_NO_SOURCE_OFFSET'});
      }finally{if(warped && !warped.isNull)warped.forceClose();}
   }
   checkCancel();
   var before=ImageWindow.windows.map(function(w){return w.mainView.id;});
   var process=new GradientMergeMosaic;
   process.targetFrames=frames.map(function(path){return [true,path];});
   process.type=GradientMergeMosaic.Average;process.nShrinkCount=spec.shrink;
   process.nFeatherRadius=spec.feather;process.blackPoint=0;process.generateMask=false;
   record('process-started',{role:spec.role,process:'GradientMergeMosaic',nativeSource:process.toSource(),dependencies:frames});
   require(process.executeGlobal(),'GradientMergeMosaic failed');
   var created=ImageWindow.windows.filter(function(w){return before.indexOf(w.mainView.id)<0;});
   require(created.length===1,'Unexpected mosaic output views');
   var result=created[0],im=result.mainView.image;
   require(im.width===c.width && im.height===c.height && im.numberOfNominalChannels===channels && im.isReal && [32,64].indexOf(im.bitsPerSample)>=0,'Mosaic output format');
   record('process-completed',{role:spec.role,process:'GradientMergeMosaic',target:result.mainView.id,historyIndex:result.mainView.historyIndex,bitsPerSample:im.bitsPerSample});
   if(im.bitsPerSample===64){
      checkCancel();
      result.setSampleFormat(32,true);
      require(result.mainView.image.isReal && result.mainView.image.bitsPerSample===32,'Mosaic Float32 conversion failed');
      record('sample-format-conversion',{role:spec.role,target:result.mainView.id,fromBits:64,toBits:32,method:'ImageWindow.setSampleFormat',historyIndex:result.mainView.historyIndex});
   }
   reference.SaveKeywords(result);reference.SaveProperties(result);result.regenerateAstrometricSolution();
   save(result,spec.role+'-mosaic-linear.xisf');
   return result;
}

function DSGDebayerSelectedMaster(window,pattern,record,checkCancel){
   if(['RGGB','BGGR','GBRG','GRBG'].indexOf(pattern)<0)throw Error('Explicit Bayer pattern required');
   if(!window || window.isNull || window.mainView.image.numberOfNominalChannels!==1 || !window.mainView.image.isReal || window.mainView.image.bitsPerSample!==32)throw Error('Float32 CFA selected master required');
   checkCancel();
   var process=new Debayer;
   if(typeof Debayer[pattern]!=='number')throw Error('Native Bayer pattern unavailable');
   process.cfaPattern=Debayer[pattern];process.debayerMethod=Debayer.VNG;
   process.fbddNoiseReduction=0;process.evaluateNoise=false;process.evaluateSignal=false;
   process.showImages=false;process.outputRGBImages=true;process.outputSeparateChannels=false;
   process.generateHistoryProperties=true;process.generateFITSKeywords=true;
   record('process-started',{process:'Debayer',target:window.mainView.id,nativeSource:process.toSource(),pattern:pattern});
   if(!process.executeOn(window.mainView))throw Error('Debayer native execution failed');
   var output=ImageWindow.windowById(process.outputImage);
   if(output.isNull || !output.mainView.image.isReal || output.mainView.image.bitsPerSample!==32 || output.mainView.image.numberOfNominalChannels!==3 || output.mainView.image.width!==window.mainView.image.width || output.mainView.image.height!==window.mainView.image.height)throw Error('Unexpected Debayer output');
   record('process-completed',{process:'Debayer',target:output.mainView.id,pattern:pattern});
   return output;
}
