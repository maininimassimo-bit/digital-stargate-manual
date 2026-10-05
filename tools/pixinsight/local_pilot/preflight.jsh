// BKL-049-EXT-PIAI P1. Trusted local library; imported History is never code.
function DSGPilotPreflight(manifest) {
   function require(ok, message) { if (!ok) throw new Error(message); }
   require(manifest.schemaVersion === '1.0', 'Unsupported manifest');
   require(/^[A-Za-z0-9_-]{1,64}$/.test(manifest.jobId), 'Invalid job identity');
   require(manifest.mode === 'PREFLIGHT_ONLY', 'Processing is not enabled in P1');
   require(manifest.inputs.length === 4, 'Four selected masters required');
   var roles = ['R', 'G', 'B', 'L'];
   var constructors = {
      AutomaticBackgroundExtractor: function() { return new AutomaticBackgroundExtractor; },
      ChannelCombination: function() { return new ChannelCombination; },
      BackgroundNeutralization: function() { return new BackgroundNeutralization; },
      ColorCalibration: function() { return new ColorCalibration; },
      BlurXTerminator: function() { return new BlurXTerminator; },
      NoiseXTerminator: function() { return new NoiseXTerminator; },
      StarXTerminator: function() { return new StarXTerminator; },
      MaskedStretch: function() { return new MaskedStretch; },
      LocalHistogramEqualization: function() { return new LocalHistogramEqualization; },
      LRGBCombination: function() { return new LRGBCombination; },
      CurvesTransformation: function() { return new CurvesTransformation; },
      PixelMath: function() { return new PixelMath; }
   };
   var result = {
      schemaVersion: '1.0', jobId: manifest.jobId, mode: manifest.mode,
      startedAt: new Date().toISOString(), status: 'RUNNING',
      pixInsightVersion: [CoreApplication.versionMajor, CoreApplication.versionMinor, CoreApplication.versionRelease].join('.') + ' build ' + CoreApplication.versionBuild,
      modules: [], inputs: [], openedExistingViews: ImageWindow.windows.length,
      processingExecuted: false, providerRequests: 0
   };
   function hash(path) { return (new CryptographicHash(CryptographicHash.SHA256)).hash(File.readFile(path)).toHex(); }
   var width, height;
   for (var k=0; k<roles.length; ++k) {
      var input=manifest.inputs[k];
      require(input.role === roles[k], 'Role order must be R,G,B,L');
      require(/^[a-f0-9]{64}$/.test(input.sha256), 'Missing source integrity');
      require(File.exists(input.path), 'Missing selected master');
      require(hash(input.path) === input.sha256, 'Source digest mismatch');
      var windows = ImageWindow.open(input.path);
      require(Number.isInteger(input.imageIndex) && input.imageIndex >= 0 && input.imageIndex < windows.length, 'Explicit XISF image index required');
      var window=windows[input.imageIndex], im=window.mainView.image;
      require(im.width===input.width && im.height===input.height, 'Selected image dimensions mismatch');
      require(im.numberOfNominalChannels === 1 && !im.isColor, 'Monochrome master required');
      if(k===0) { width=im.width; height=im.height; }
      require(im.width===width && im.height===height, 'Master dimensions differ');
      result.inputs.push({role:input.role,sha256:input.sha256,width:im.width,height:im.height,
         bitsPerSample:im.bitsPerSample,historyIndex:window.mainView.historyIndex,
         median:Number(im.median()),mad:Number(im.MAD()),modified:window.isModified,
         imageIndex:input.imageIndex,containerImageCount:windows.length});
      // Deliberately leave read-only source windows open for operator inspection.
      // No process execution, save, clone or close is performed by this preflight.
      require(hash(input.path) === input.sha256, 'Source changed during inspection');
   }
   Object.keys(constructors).forEach(function(id) {
      try { var p=constructors[id](); result.modules.push({processId:id,available:true,version:null,versionEvidence:'NOT_EXPOSED_BY_PROCESS_INSTANCE'}); }
      catch(e) { result.modules.push({processId:id,available:false,error:String(e)}); }
   });
   require(result.modules.every(function(p) {return p.available;}), 'Required module missing; no fallback');
   result.status='PREFLIGHT_PASSED'; result.finishedAt=new Date().toISOString();
   return result;
}
