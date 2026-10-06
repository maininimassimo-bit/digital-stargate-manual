// Trusted candidate preparation stage. Local only; no portal dispatch/acceptance.
function DSGExecuteMasterPreparation(m){
   function require(ok,message){if(!ok)throw Error(message);}
   function hash(path){return(new CryptographicHash(CryptographicHash.SHA256)).hash(File.readFile(path)).toHex();}
   function write(path,value){require(!File.exists(path),'Preparation artifact exists');var f=new File;f.createForWriting(path);try{f.write(ByteArray.stringToUTF8(JSON.stringify(value,null,2)));}finally{f.close();}}
   var lease=new File,terminalAuthorized=false,owned=[],outputs=[],processCount=0,eventCount=0;
   var receipt={schemaVersion:'1.0',jobId:m.jobId,token:m.token,status:'FAILED',authority:m.authority,
                recipe:'MASTER_PREPARATION_V1',outputs:outputs,providerRequests:0,nonLinear:false,
                runtimeHashes:m.runtimeHashes,engineSha256:m.engineSha256,requestSha256:m.requestSha256};
   function event(name,data){
      if(name==='process-completed')++processCount;
      write(m.jobDirectory+'/events/'+('0000'+(++eventCount)).slice(-4)+'.json',{event:name,data:data});
   }
   function cancel(){
      var path=m.jobDirectory+'/cancel.json';
      if(File.exists(path)){
         var request=JSON.parse(File.readTextFile(path));
         require(request.jobId===m.jobId && request.token===m.token && request.requested===true,'Cancellation identity mismatch');
         throw Error('PREPARATION_CANCELLED');
      }
   }
   function selected(row){
      cancel();require(hash(row.path)===row.sha256 && hash(row.sourcePath)===row.sha256,'Preparation input integrity');
      var windows=ImageWindow.open(row.path);windows.forEach(function(w){owned.push(w);});
      require(windows.length>=1 && windows.length<=16 && row.imageIndex<windows.length,'Explicit image selection');
      var chosen=windows[row.imageIndex];
      windows.forEach(function(w,i){if(i!==row.imageIndex)w.forceClose();});
      var im=chosen.mainView.image;
      require(!chosen.isModified && im.isReal && im.bitsPerSample===32 && im.width===row.width && im.height===row.height && im.numberOfNominalChannels===(m.mode==='OSC'?3:1),'Selected preparation master format');
      return chosen;
   }
   function save(window,name){
      require(Object.prototype.hasOwnProperty.call(m.expectedOutputs,name),'Scoped preparation output');
      require(!outputs.some(function(o){return o.name===name;}),'Duplicate preparation checkpoint');
      var path=m.jobDirectory+'/outputs/'+name,im=window.mainView.image;
      require(!File.exists(path) && im.isReal && im.bitsPerSample===32 && im.numberOfNominalChannels===m.expectedOutputs[name],'Preparation output format');
      require(window.saveAs(path,false,false,true,false),'Preparation checkpoint save');
      var output={name:name,sha256:hash(path),width:im.width,height:im.height,channels:im.numberOfNominalChannels,nonLinear:false};
      outputs.push(output);event('checkpoint',output);return path;
   }
   require(m.schemaVersion==='1.0' && /^[A-Za-z][A-Za-z0-9_]{0,47}$/.test(m.jobId) && m.authority==='LOCAL_SOURCE_PREPARATION_NOT_OWNER_PORTAL_JOB','Preparation identity');
   require(m.jobDirectory===m.workerRoot+'/'+m.jobId && !File.exists(m.jobDirectory+'/terminal.json'),'Preparation job scope/replay');
   try{
      lease.openForReadWrite(m.workerRoot+'/active-job.json');
      var reservation=JSON.parse(lease.read(DataType.ByteArray,lease.size).utf8ToString());
      require(reservation.jobId===m.jobId && reservation.token===m.token && reservation.authority===m.authority && reservation.requestSha256===m.requestSha256,'Preparation reservation');
      var other=new File,denied=false;try{other.openForReadWrite(m.workerRoot+'/active-job.json');}catch(e){denied=true;}finally{if(other.isOpen)other.close();}
      require(denied,'Exclusive native preparation lease');terminalAuthorized=true;receipt.exclusiveLeaseVerified=true;
      require(Object.keys(m.runtimeHashes).sort().join(',')==='preparation_executor.jsh,source_preparation.jsh','Preparation runtime scope');
      Object.keys(m.runtimeHashes).forEach(function(name){require(hash(m.jobDirectory+'/'+name)===m.runtimeHashes[name],'Preparation runtime integrity');});
      require(hash(m.enginePath)===m.engineSha256,'Installed astrometric engine integrity');
      require(hash(m.jobDirectory+'/request.json')===m.requestSha256,'Preparation immutable request integrity');
      var request=JSON.parse(File.readTextFile(m.jobDirectory+'/request.json'));
      ['schemaVersion','jobId','mode','layout','bayerPattern','canvas','shrink','feather'].forEach(function(key){require(JSON.stringify(request[key])===JSON.stringify(m[key]),'Preparation immutable parameters');});
      require(request.inputs.length===m.inputs.length&&m.inputs.every(function(row,i){var original=request.inputs[i];return row.sourcePath===original.path&&['panelId','role','sha256','imageIndex','width','height'].every(function(k){return row[k]===original[k];});}),'Preparation immutable source binding');
      var roles=m.mode==='LRGB'?['R','G','B','L']:m.mode==='SHO'?['SII','Ha','OIII']:m.mode==='HOO'?['Ha','OIII']:m.mode==='OSC'?['RGB']:m.mode==='OSC_CFA'?['CFA']:null;
      require(roles && (m.layout==='SINGLE'||m.layout==='PANELS'),'Preparation mode/layout');
      require(m.mode==='OSC_CFA'?['RGGB','BGGR','GBRG','GRBG'].indexOf(m.bayerPattern)>=0:m.bayerPattern===null,'Explicit Bayer pattern');
      require(m.layout==='PANELS'||(m.mode==='OSC_CFA'&&m.canvas===null&&m.shrink===0&&m.feather===0),'Single preparation scope');
      if(m.layout==='PANELS'){
         DSGValidateMosaicCanvas(m.canvas);
         require(Number.isInteger(m.shrink)&&m.shrink>=0&&m.shrink<=5&&Number.isInteger(m.feather)&&m.feather>=1&&m.feather<=100,'Preparation bounded merge parameters');
         require(typeof GradientMergeMosaic==='function','GradientMergeMosaic module required');
      }
      if(m.mode==='OSC_CFA')require(typeof Debayer==='function','Debayer module required');
      require(Array.isArray(m.inputs)&&m.inputs.length>=1&&m.inputs.length<=64,'Preparation input bound');
      var panels=[],seen={},expected={};
      m.inputs.forEach(function(row){
         require(/^[A-Za-z0-9_-]{1,40}$/.test(row.panelId)&&roles.indexOf(row.role)>=0&&Number.isInteger(row.imageIndex)&&row.imageIndex>=0&&row.imageIndex<16,'Preparation selected role/index');
         require(row.path===m.jobDirectory+'/inputs/'+row.role+'-'+row.panelId+'.xisf'&&/^[a-f0-9]{64}$/.test(row.sha256),'Preparation copied input scope');
         require(!seen[row.panelId+':'+row.role],'Duplicate preparation role');seen[row.panelId+':'+row.role]=true;
         if(panels.indexOf(row.panelId)<0)panels.push(row.panelId);
      });
      require(m.layout==='PANELS'?panels.length>=2&&panels.length<=16:panels.length===1,'Preparation panel count');
      var order=[];panels.forEach(function(p){roles.forEach(function(r){order.push(p+':'+r);});});
      require(m.inputs.map(function(r){return r.panelId+':'+r.role;}).join(',')===order.join(','),'Preparation exact role order');
      var resultRoles=m.mode==='OSC_CFA'?['RGB']:roles;
      if(m.mode==='OSC_CFA')panels.forEach(function(p){expected['RGB-'+p+'-debayer.xisf']=3;});
      if(m.layout==='PANELS')resultRoles.forEach(function(r){panels.forEach(function(p){expected[r+'-'+p+'-registered.xisf']=r==='RGB'?3:1;});expected[r+'-mosaic-linear.xisf']=r==='RGB'?3:1;});
      else expected['RGB-linear.xisf']=3;
      require(Object.keys(expected).sort().join(',')===Object.keys(m.expectedOutputs).sort().join(',')&&Object.keys(expected).every(function(k){return expected[k]===m.expectedOutputs[k];}),'Preparation checkpoint envelope');
      require(m.nativeProcessCount===(m.mode==='OSC_CFA'?panels.length:0)+(m.layout==='PANELS'?resultRoles.length:0),'Preparation process envelope');
      // Validate every selected image/WCS before any pixel operation.
      m.inputs.forEach(function(row){var w=selected(row);try{require(m.layout!=='PANELS'||w.hasAstrometricSolution,'Solved mosaic source required');}finally{w.forceClose();}});
      Console.show();Console.abortEnabled=true;
      resultRoles.forEach(function(resultRole){
         var sourceRole=m.mode==='OSC_CFA'?'CFA':resultRole,group=[];
         try{
            panels.forEach(function(panel){
               var row=m.inputs.filter(function(r){return r.role===sourceRole&&r.panelId===panel;})[0],input=selected(row);
               event('source-selected',{panelId:panel,role:sourceRole,imageIndex:row.imageIndex,sourceSha256:row.sha256,target:input.mainView.id});
               var prepared=input;
               if(m.mode==='OSC_CFA'){
                  prepared=DSGDebayerSelectedMaster(input,m.bayerPattern,function(name,data){event(name,Object.assign({role:'RGB',panelId:panel},data));},cancel);owned.push(prepared);
                  if(m.layout==='PANELS'){
                     var metadata=new AstrometricMetadata;metadata.ExtractMetadata(input);metadata.SaveKeywords(prepared);metadata.SaveProperties(prepared);prepared.regenerateAstrometricSolution();
                     require(prepared.hasAstrometricSolution,'Debayer astrometric transfer');
                     event('astrometric-metadata-transfer',{panelId:panel,source:input.mainView.id,target:prepared.mainView.id,geometryUnchanged:true});
                  }
                  save(prepared,'RGB-'+panel+'-debayer.xisf');input.forceClose();
               }
               group.push({panelId:panel,window:prepared});
            });
            if(m.layout==='PANELS'){
               var mosaic=DSGPrepareMosaicGroup({role:resultRole,inputs:group,canvas:m.canvas,shrink:m.shrink,feather:m.feather},event,save,cancel);owned.push(mosaic);mosaic.forceClose();
            }else save(group[0].window,'RGB-linear.xisf');
         }finally{group.forEach(function(item){if(!item.window.isNull)item.window.forceClose();});}
      });
      require(outputs.length===Object.keys(expected).length&&processCount===m.nativeProcessCount,'Preparation completeness');
      require(m.inputs.every(function(r){return hash(r.sourcePath)===r.sha256&&hash(r.path)===r.sha256;}),'Preparation originals/copies unchanged');
      receipt.originalIntegrity='UNCHANGED';receipt.status='COMPLETED';receipt.scientificAcceptance='OWNER_REVIEW_REQUIRED';
   }catch(error){receipt.error=String(error);if(receipt.error.indexOf('PREPARATION_CANCELLED')>=0)receipt.status='CANCELLED';Console.criticalln(receipt.error);}
   finally{
      try{
         owned.forEach(function(w){if(!w.isNull)w.forceClose();});receipt.processCount=processCount;
         if(terminalAuthorized)write(m.jobDirectory+'/terminal.json',receipt);
      }finally{if(lease.isOpen)lease.close();}
   }
   return receipt;
}
