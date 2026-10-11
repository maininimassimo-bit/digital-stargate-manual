// Read-only measurements of explicit, independently hashed copies. No network.
function DSGAnalyzeMasters(m) {
   function require(ok,message) {if(!ok)throw Error(message);}
   function hash(path) {return (new CryptographicHash(CryptographicHash.SHA256)).hash(File.readFile(path)).toHex();}
   function write(path,value) {
      require(!File.exists(path),'Analysis receipt already exists');
      var f=new File;f.createForWriting(path);
      try {f.write(ByteArray.stringToUTF8(JSON.stringify(value)));} finally {f.close();}
   }
   require(m.version==='DSG_PIAI_READ_ONLY_ANALYSIS_V2' && Array.isArray(m.inputs) &&
      m.inputs.length>=1 && m.inputs.length<=4,'Analysis manifest');
   require(!File.exists(m.report),'Analysis already completed; replay refused');
   require(hash(m.measurementLibrary)===m.measurementSha256 &&
      hash(m.starDetectorLibrary)===m.starDetectorSha256,'Analysis component changed');
   var rows=[],windows=[];
   console.beginLog(m.log);
   try {
      m.inputs.forEach(function(input) {
         require(hash(input.source)===input.sha256 && hash(input.copy)===input.sha256,'Analysis source changed');
         require(Number.isInteger(input.imageIndex) && input.imageIndex>=0 && input.imageIndex<16,'Explicit analysis index');
         windows=ImageWindow.open(input.copy);
         require(windows.length>input.imageIndex,'Analysis image missing');
         var w=windows[input.imageIndex],im=w.mainView.image,history=w.mainView.historyIndex;
         require(im.width===input.width && im.height===input.height && im.numberOfNominalChannels===input.channels,
            'Analysis geometry changed');
         var report=DSGMeasureNative(w,input.regions);
         require(w.mainView.historyIndex===history && hash(input.source)===input.sha256 &&
            hash(input.copy)===input.sha256,'Analysis must preserve originals and History');
         report.sourceSha256=input.sha256;report.imageIndex=input.imageIndex;
         report.adapterSha256=m.measurementSha256;report.starDetectorSha256=m.starDetectorSha256;
         report.coreVersion={major:CoreApplication.versionMajor,minor:CoreApplication.versionMinor,
            release:CoreApplication.versionRelease,revision:CoreApplication.versionRevision,build:CoreApplication.versionBuild};
         report.historyUnchanged=true;report.originalUnchanged=true;report.status='MEASURED';
         rows.push({role:input.role,report:report});
         windows.forEach(function(window){window.forceClose();});windows=[];
      });
      // Verify every original again after all measurements, not only its own phase.
      m.inputs.forEach(function(input){require(hash(input.source)===input.sha256 && hash(input.copy)===input.sha256,'Analysis final source guard');});
      require(hash(m.measurementLibrary)===m.measurementSha256 &&
         hash(m.starDetectorLibrary)===m.starDetectorSha256,'Analysis final component guard');
      write(m.report,{version:m.version,status:'READ_ONLY_MEASURED',measurements:rows,
         originalUnchanged:true,historyUnchanged:true,scientificAcceptance:'NOT_ESTABLISHED'});
      console.writeln('READ_ONLY_ANALYSIS_COMPLETE');
   } finally {
      windows.forEach(function(window){window.forceClose();});console.endLog();
   }
}
