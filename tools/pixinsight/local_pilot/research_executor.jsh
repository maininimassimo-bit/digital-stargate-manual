// Trusted one-segment controller. No provider, network or History execution.
function DSGResearchExecute(m) {
   function need(ok,text) {if(!ok)throw Error(text);}
   function hash(path) {return (new CryptographicHash(CryptographicHash.SHA256)).hash(File.readFile(path)).toHex();}
   function write(path,value) {
      need(!File.exists(path),'Create-only adaptive artifact');
      var f=new File;f.createForWriting(path);
      try {f.write(ByteArray.stringToUTF8(JSON.stringify(value)));} finally {f.close();}
   }
   need(m.version==='DSG_PIAI_RESEARCH_NATIVE_V1' && Number.isInteger(m.permit.ordinal), 'Adaptive manifest');
   need(!File.exists(m.report) && !File.exists(m.failure), 'Adaptive attempt cannot replay');
   var ack=JSON.parse(File.readTextFile(m.startAcknowledgement));
   need(hash(m.startAcknowledgement)===m.startAcknowledgementSha256 && ack.executeAllowed===true &&
        ack.ordinal===m.permit.ordinal,'Acknowledged single-use native start required');
   var owned=[],events=[],tracks={},sources={},intermediates={},parent=[],current=[],lease=new File;
   function owns(window) {return owned.some(function(w){return !w.isNull && w.mainView.id===window.mainView.id;});}
   function guard() {
      var core={major:CoreApplication.versionMajor,minor:CoreApplication.versionMinor,
         release:CoreApplication.versionRelease,revision:CoreApplication.versionRevision,build:CoreApplication.versionBuild};
      Object.keys(core).forEach(function(key){need(core[key]===m.coreVersion[key],'Pinned PixInsight core changed');});
      m.sources.forEach(function(s){need(hash(s.source)===s.sha256,'Original source changed');});
      m.runtimeFiles.forEach(function(f){need(hash(f.path)===f.sha256,'Pinned runtime file changed');});
   }
   function cancel() {
      if(File.exists(m.cancel)) {
         var value=JSON.parse(File.readTextFile(m.cancel));
         need(value.jobId===m.permit.jobId && value.permitSha256===m.permitSha256,'Cancellation identity');
         throw Error('DSG_ADAPTIVE_CANCELLED');
      }
   }
   function id(role) {return 'DSGA_'+m.permit.jobId.substring(5)+'_'+m.permit.ordinal+'_'+role;}
   function open(row,role) {
      need(hash(row.copy)===row.sha256,'Native copy changed');
      var ws=ImageWindow.open(row.copy);owned=owned.concat(ws);
      need(row.imageIndex>=0 && row.imageIndex<ws.length,'Native selected index');
      var w=ws[row.imageIndex],im=w.mainView.image;
      need(im.width===row.width && im.height===row.height && im.numberOfNominalChannels===row.channels &&
           im.isReal && im.bitsPerSample===32,'Native selected Float32 geometry');
      need(ImageWindow.windowById(id(role)).isNull,'Unique work identifier');
      w.mainView.id=id(role);return w;
   }
   function clone(w,role) {
      cancel();var im=w.mainView.image;
      need(ImageWindow.windowById(id(role)).isNull,'Unique clone identifier');
      var out=new ImageWindow(im.width,im.height,im.numberOfNominalChannels,32,true,im.isColor,id(role));
      owned.push(out);out.mainView.beginProcess();
      try {out.mainView.image.assign(im);} finally {out.mainView.endProcess();}
      out.keywords=w.keywords;
      if(w.hasAstrometricSolution)out.copyAstrometricSolution(w);
      w.mainView.properties.forEach(function(key){
         if(key==='Image:Id' || key.indexOf('XISF:')===0)return;
         out.mainView.setPropertyValue(key,w.mainView.propertyValue(key));
         out.mainView.setPropertyAttributes(key,w.mainView.propertyAttributes(key));
      });
      events.push({kind:'derived-copy',role:role,parent:w.mainView.id});return out;
   }
   function apply(process,w,role) {
      cancel();var before=w.mainView.historyIndex,source=process.toSource();
      events.push({kind:'process-started',role:role,nativeSource:source,historyIndex:before});
      var existing=ImageWindow.windows.map(function(window){return window.mainView.id;});
      try {need(process.executeOn(w.mainView)===true,'Native process failed');}
      finally {
         ImageWindow.windows.forEach(function(window){
            if(existing.indexOf(window.mainView.id)<0 && !owns(window)) {
               owned.push(window);intermediates['UNASSIGNED_NATIVE_'+owned.length]=window;
            }
         });
      }
      need(w.mainView.historyIndex>before,'Native History was not recorded');
      events.push({kind:'process-completed',role:role,historyIndex:w.mainView.historyIndex});return true;
   }
   function save(w,role,phase) {
      cancel();var path=m.outputDirectory+'/'+phase+'_'+role+'.xisf';
      need(!File.exists(path),'Native checkpoint already exists');
      var view=w.mainView;
      var history={initial:view.initialProcessing.toSource(),current:view.processing.toSource(),historyIndex:view.historyIndex};
      var historyPath=m.outputDirectory+'/'+phase+'_'+role+'_history.json';write(historyPath,history);
      need(w.saveAs(path,false,false,true,false),'Native save failed');
      var beforeMeasurement=view.historyIndex,report=DSGMeasureNative(w,m.regions);
      need(view.historyIndex===beforeMeasurement,'Read-only checkpoint measurement changed History');
      report.sourceSha256=hash(path);report.imageIndex=0;
      report.adapterSha256=m.measurementSha256;report.starDetectorSha256=m.starDetectorSha256;
      report.coreVersion={major:CoreApplication.versionMajor,minor:CoreApplication.versionMinor,
         release:CoreApplication.versionRelease,revision:CoreApplication.versionRevision,build:CoreApplication.versionBuild};
      report.historyUnchanged=true;report.originalUnchanged=true;report.status='MEASURED';
      return {role:role,path:path,sha256:report.sourceSha256,width:report.width,height:report.height,
         channels:report.channels,historyPath:historyPath,historySha256:hash(historyPath),measurement:report};
   }
   function snapshot(phase) {
      var result=[];
      ['RGB','L'].forEach(function(role){if(tracks[role])result.push(save(tracks[role],role,phase));});
      return result;
   }
   console.beginLog(m.log);
   try {
      lease.openForReadWrite(m.nativeLease);
      var conflicting=null;
      try {conflicting=new File;conflicting.openForReadWrite(m.nativeLease);} catch(ignore) {conflicting=null;}
      if(conflicting!==null){conflicting.close();throw Error('Exclusive native lease unavailable');}
      guard();cancel();
      if(m.permit.parentId==='CP000') {
         m.inputs.forEach(function(row){sources[row.role]=open(row,row.role);});
         var p=m.preparation;
         if(p.mode==='OSC') {
            tracks.RGB=clone(sources.RGB,'RGB_WORK');tracks.L=clone(sources.RGB,'L_WORK');
            var pm=new PixelMath;pm.expression='0.2126*$T[0]+0.7152*$T[1]+0.0722*$T[2]';
            pm.useSingleExpression=true;pm.createNewImage=false;pm.rescale=false;pm.truncate=false;
            apply(pm,tracks.L,'L_PREPARATION');
            var gray=new ConvertToGrayscale;apply(gray,tracks.L,'L_PREPARATION');
         } else {
            var base=sources[p.rgbMapping[0]],im=base.mainView.image;
            tracks.RGB=new ImageWindow(im.width,im.height,3,32,true,true,id('RGB_WORK'));owned.push(tracks.RGB);
            var cc=new ChannelCombination;cc.colorSpace=ChannelCombination.RGB;
            cc.inheritAstrometricSolution=true;
            cc.channels=p.rgbMapping.map(function(role){return [true,sources[role].mainView.id];});
            apply(cc,tracks.RGB,'RGB_PREPARATION');
            tracks.L=clone(sources[p.luminance.role],'L_WORK');
         }
         if(p.factor===2) {
            [tracks.RGB,tracks.L].forEach(function(w,k){var rs=new IntegerResample;
               rs.zoomFactor=-2;rs.downsamplingMode=IntegerResample.Average;
               rs.gammaCorrection=false;rs.forceResolution=false;rs.noGUIMessages=true;
               apply(rs,w,k?'L_SAMPLING':'RGB_SAMPLING');});
         }
         need(tracks.RGB.mainView.image.width===p.workingGeometry[0] &&
              tracks.RGB.mainView.image.height===p.workingGeometry[1] &&
              tracks.L.mainView.image.numberOfNominalChannels===1,'Prepared geometry');
         parent=snapshot('parent');
      } else {
         m.inputs.forEach(function(row){tracks[row.role]=open(row,row.role);});
         parent=m.parentArtifacts;
      }
      var step=m.permit.step;
      if(step.process==='SPCC') {
         need(m.context.domain==='LINEAR_ATTESTED' && tracks.RGB.hasAstrometricSolution,'SPCC linear WCS required');
         need(Object.keys(step.parameters).length===0,'Pinned SPCC parameters');
         var profile=m.photometricProfile;
         var gaia=new Gaia;gaia.dataRelease=Gaia.DataRelease_3_SP;gaia.command='configure';
         gaia.databaseFilePaths=profile.gaiaFiles;gaia.generateTextOutput=false;
         need(gaia.executeGlobal(),'Local Gaia configuration');gaia.command='get-info';
         need(gaia.executeGlobal() && gaia.isValid && gaia.databaseHasMeanSpectrumData,'Gaia spectrum database');
         var spcc=new SpectrophotometricColorCalibration;spcc.narrowbandMode=false;
         spcc.redFilterName=profile.rgbFilters[0];spcc.greenFilterName=profile.rgbFilters[1];spcc.blueFilterName=profile.rgbFilters[2];
         spcc.redFilterTrCurve=profile.filterCurves[0];spcc.greenFilterTrCurve=profile.filterCurves[1];spcc.blueFilterTrCurve=profile.filterCurves[2];
         spcc.deviceQECurveName=profile.qe;spcc.deviceQECurve=profile.qeCurve;
         spcc.whiteReferenceName=profile.whiteReference;spcc.whiteReferenceSpectrum=profile.whiteSpectrum;
         spcc.catalogId='GaiaDR3SP';spcc.autoLimitMagnitude=true;spcc.applyCalibration=true;
         spcc.neutralizeBackground=false;spcc.generateGraphs=false;spcc.generateTextFiles=true;
         spcc.outputDirectory=m.outputDirectory;
         apply(spcc,tracks.RGB,'RGB');
         write(m.outputDirectory+'/SPCC-native-properties.json',{
            whiteBalance:String(tracks.RGB.mainView.propertyValue('PCL:SPCC:WhiteBalanceFactors')),
            calibrationSignature:String(tracks.RGB.mainView.propertyValue('PCL:Signature:ColorCalibration'))});
      } else if(step.process==='VIVIDNESS') {
         need(m.context.domain==='NONLINEAR_ATTESTED' && Object.keys(step.parameters).join(',')==='saturation' &&
              Number.isFinite(step.parameters.saturation) && step.parameters.saturation>=0 && step.parameters.saturation<=0.25,
              'Bounded presentation saturation');
         var curves=new CurvesTransformation;curves.S=[[0,0],[0.5,0.5+step.parameters.saturation],[1,1]];
         curves.St=CurvesTransformation.AkimaSubsplines;apply(curves,tracks.RGB,'RGB');
      } else {
         need(['OPTICAL_CORRECT','DECONVOLVE','DENOISE','STRETCH','COMBINE'].indexOf(step.process)>=0,'Admitted research process');
         DSGAdaptiveNativeStep(step,tracks,m.context,{apply:apply,cancel:cancel,clone:clone,
            secondary:function(w){if(!owns(w))owned.push(w);}});
      }
      current=snapshot('current');
      var intermediateArtifacts=Object.keys(intermediates).map(function(role){return save(intermediates[role],role,'intermediate');});
      guard();cancel();
      write(m.events,events);
      write(m.report,{version:m.version,status:'NATIVE_SEGMENT_COMPLETE',permitSha256:m.permitSha256,
         parent:parent,current:current,intermediates:intermediateArtifacts,eventsSha256:hash(m.events),sourceGuard:'UNCHANGED',
         scientificAcceptance:'NOT_ESTABLISHED',loadedModels:'SELECTOR_AND_HASH_BOUND_NOT_INDEPENDENTLY_ATTESTED'});
   } catch(error) {
      var partial=[];
      var rescue={};Object.keys(tracks).forEach(function(role){rescue[role]=tracks[role];});
      Object.keys(intermediates).forEach(function(role){rescue[role]=intermediates[role];});
      Object.keys(rescue).forEach(function(role){
         var w=rescue[role],path=m.outputDirectory+'/partial_'+role+'.xisf';
         try {
            if(!File.exists(path) && !w.isNull) {
               var h=m.outputDirectory+'/partial_'+role+'_history.json';
               write(h,{initial:w.mainView.initialProcessing.toSource(),current:w.mainView.processing.toSource(),
                        historyIndex:w.mainView.historyIndex});
               need(w.saveAs(path,false,false,true,false),'Partial save failed');
               partial.push({role:role,path:path,sha256:hash(path),historyPath:h,historySha256:hash(h)});
            }
         } catch(saveError) {partial.push({role:role,status:'NOT_SAVED',reason:String(saveError)});}
      });
      if(!File.exists(m.events))write(m.events,events);
      write(m.failure,{version:m.version,status:'NATIVE_SEGMENT_FAILED_OR_CANCELLED',reason:String(error),
         partial:partial,eventsSha256:hash(m.events)});
      throw error;
   } finally {
      // Checkpoints/History remain on disk. Close only this isolated instance's owned views.
      owned.forEach(function(w){if(!w.isNull)w.forceClose();});
      if(lease.isOpen)lease.close();console.endLog();
      write(m.done,{status:'OWNED_VIEWS_CLOSED',permitSha256:m.permitSha256});
   }
}
