// P2 trusted Windows-local executor. No eval, imports of History or network API.
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
   require(m.recipe==='LRGB_LINEAR_PREP_V1', 'Recipe not allowed');
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
   function save(window,name) {
      checkCancel();
      var path=root+'/outputs/'+name;
      require(!File.exists(path), 'Output already exists');
      require(window.saveAs(path,false,false,true,false), 'Native save failed');
      outputs.push({name:name,sha256:hash(path),viewId:window.mainView.id,
         width:window.mainView.image.width,height:window.mainView.image.height,
         channels:window.mainView.image.numberOfNominalChannels,nonLinear:false});
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
      rgb.keywords=targets[0].keywords;
      event('process-completed',{label:'RGB-composition',target:rgb.mainView.id});
      save(rgb,'RGB-linear.xisf');
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
