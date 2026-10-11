// Candidate read-only measurements. Include StarDetector V2 in the trusted launcher.
// No process changes image pixels, no network, no scientific acceptance flag.
function DSGMeasureNative(window, regions) {
   if (!window || window.isNull || !Array.isArray(regions) || regions.length > 8)
      throw Error('Measurement scope required');
   var image = window.mainView.image;
   var width = image.width, height = image.height;
   if (width < 32 || height < 32 || width > 12000 || height > 12000 ||
       [1,3].indexOf(image.numberOfNominalChannels) < 0) throw Error('Measurement geometry');
   function finite(value) { return typeof value === 'number' && Number.isFinite(value); }
   regions.forEach(function(r) {
      if (!Array.isArray(r) || r.length !== 4 || !r.every(Number.isInteger) ||
          r[0] < 0 || r[1] < 0 || r[2] > width || r[3] > height ||
          r[2]-r[0] < 32 || r[3]-r[1] < 32) throw Error('Measurement ROI');
   });
   var noise = [];
   image.pushSelections();
   try {
      image.resetSelections();
      regions.forEach(function(r, index) {
         image.selectedRect = new Rect(r[0], r[1], r[2], r[3]);
         for (var channel = 0; channel < image.numberOfNominalChannels; ++channel) {
            image.selectedChannel = channel;
            // Preserve each estimate/support count. No silent fallback or acceptance threshold.
            var estimates = [];
            [4,3,2].forEach(function(layers) {
               var pair = image.noiseMRS(layers, 0, 3);
               if (!Array.isArray(pair) || pair.length !== 2 || !finite(pair[0]) || pair[0] < 0 ||
                   !Number.isInteger(pair[1]) || pair[1] < 0 || pair[1] > image.selectedRect.area)
                  throw Error('Invalid native noise estimate');
               estimates.push({method:'MRS',layers:layers,sigma:pair[0],support:pair[1]});
            });
            noise.push({region:index,channel:channel,estimates:estimates});
         }
      });
   } finally { image.popSelections(); }
   var detector = new StarDetector;
   detector.structureLayers = 5;
   detector.hotPixelFilterRadius = 1;
   detector.noiseReductionFilterRadius = 0;
   detector.sensitivity = 0.5;
   detector.peakResponse = 0.5;
   detector.upperLimit = 1;
   var detected;
   image.pushSelections();
   try { image.resetSelections(); detected = detector.stars(image); }
   finally { image.popSelections(); }
   // Deterministic spatial coverage: brightest isolated candidate per 16x16 cell.
   // Detection choices are recorded, not universal quality thresholds.
   var cells = {};
   detected.forEach(function(s) {
      if (!s || !s.pos || !finite(s.pos.x) || !finite(s.pos.y) || !finite(s.flux) ||
          s.flux <= 0 || s.nmax !== 1 || s.pos.x < 0 || s.pos.y < 0 ||
          s.pos.x >= width || s.pos.y >= height) return;
      var key = Math.floor(16*s.pos.y/height)*16 + Math.floor(16*s.pos.x/width);
      var previous = cells[key];
      if (!previous || s.flux > previous.flux ||
          (s.flux === previous.flux && (s.pos.y < previous.pos.y ||
           (s.pos.y === previous.pos.y && s.pos.x < previous.pos.x)))) cells[key] = s;
   });
   var stars = Object.keys(cells).map(Number).sort(function(a,b){return a-b;}).map(function(k){return cells[k];});
   var fits = [];
   // Fit every nominal channel separately; detector coordinates come from intensity.
   for (var c = 0; c < image.numberOfNominalChannels && stars.length; ++c) {
      var psf = new DynamicPSF;
      psf.autoPSF = false; psf.circularPSF = false;
      psf.gaussianPSF = true; psf.moffatPSF = false;
      psf.moffat10PSF = false; psf.moffat8PSF = false; psf.moffat6PSF = false;
      psf.moffat4PSF = false; psf.moffat25PSF = false; psf.moffat15PSF = false;
      psf.lorentzianPSF = false; psf.regenerate = true;
      psf.views = [[window.mainView.id]];
      psf.stars = stars.map(function(s) {
         return [0,c,DynamicPSF.Star_DetectedOk,s.rect.x0,s.rect.y0,s.rect.x1,s.rect.y1,s.pos.x,s.pos.y];
      });
      if (!psf.executeGlobal()) throw Error('Native PSF fitting failed');
      psf.psf.forEach(function(row) {
         var index = row[DynamicPSF.psf_starIndex];
         if (row[DynamicPSF.psf_status] !== DynamicPSF.PSF_FittedOk) return;
         var values = [row[DynamicPSF.psf_B],row[DynamicPSF.psf_A],row[DynamicPSF.psf_cx],
                       row[DynamicPSF.psf_cy],row[DynamicPSF.psf_sx],row[DynamicPSF.psf_sy],
                       row[DynamicPSF.psf_theta],row[DynamicPSF.psf_mad]];
         if (!Number.isInteger(index) || index < 0 || index >= stars.length || !values.every(finite) ||
             values[4] <= 0 || values[5] <= 0 || values[7] < 0) throw Error('Invalid native PSF');
         fits.push({star:index,channel:c,model:'GAUSSIAN',background:values[0],amplitude:values[1],
                    x:values[2],y:values[3],sx:values[4],sy:values[5],theta:values[6],residual:values[7]});
      });
   }
   return {version:'DSG_PIAI_NATIVE_MEASUREMENTS_V2',width:width,height:height,
      channels:image.numberOfNominalChannels,regions:regions,noise:noise,
      starSelection:{detected:detected.length,selected:stars.length,grid:16,method:'BRIGHTEST_ISOLATED_PER_CELL'},
      detector:{version:2.01,structureLayers:5,hotPixelFilterRadius:1,noiseReductionFilterRadius:0,
                sensitivity:0.5,peakResponse:0.5,upperLimit:1},fits:fits,
      noiseUnits:'NORMALIZED_IMAGE_SAMPLES',noiseAssumption:'GAUSSIAN_COMPONENT_ESTIMATE',
      backgroundValidity:'NOT_ESTABLISHED',linearity:'NOT_ESTABLISHED',
      registration:'NOT_ESTABLISHED',acceptance:'NOT_ESTABLISHED'};
}
