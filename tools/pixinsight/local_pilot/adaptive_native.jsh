// Finite process factory for trusted native segments. No model code or network.
// The controller must verify the exact permit, physical facts, input copies,
// runtime/model files and checkpoint dependencies before invoking this factory.
function DSGAdaptiveNativeStep(step, tracks, context, callbacks) {
   function need(ok, text) { if (!ok) throw Error(text); }
   function finite(n) { return typeof n === 'number' && Number.isFinite(n); }
   var bounds = {
      BACKGROUND:{polyDegree:[0,2,true],boxSize:[5,32,true],boxSeparation:[5,64,true]},
      OPTICAL_CORRECT:{}, COLOR:{},
      DECONVOLVE:{sharpenL:[0,0.6,false],sharpenRGB:[0,0.55,false]},
      DENOISE:{denoiseL:[0.3,0.85,false],denoiseRGB:[0.3,0.85,false]},
      SEPARATE:{}, STRETCH:{targetBackground:[0.03,0.12,false]},
      MASK_BUILD:{maskLow:[0,0.5,false],maskHigh:[0.05,1,false]},
      LOCAL_CONTRAST:{contrastLarge:[0,0.4,false],contrastSmall:[0,0.4,false]},
      COMBINE:{}, RECOMBINE:{}
   };
   need(step && Object.keys(step).sort().join(',') === 'parameters,process' &&
        Object.prototype.hasOwnProperty.call(bounds, step.process), 'Adaptive process contract');
   var limits = bounds[step.process], p = step.parameters;
   need(p && Object.keys(p).sort().join(',') === Object.keys(limits).sort().join(','), 'Adaptive parameter keys');
   Object.keys(limits).forEach(function(k) {
      var b = limits[k];
      need(finite(p[k]) && p[k] >= b[0] && p[k] <= b[1] && (!b[2] || Number.isInteger(p[k])),
           'Adaptive parameter bounds');
   });
   need(context && ['LRGB','OSC','SHO','HOO'].indexOf(context.mode) >= 0 &&
        ['LINEAR_ATTESTED','NONLINEAR_ATTESTED'].indexOf(context.domain) >= 0 &&
        ['DIRECT','STARLESS'].indexOf(context.branch) >= 0, 'Adaptive native context');
   need(callbacks && typeof callbacks.apply === 'function' && typeof callbacks.cancel === 'function' &&
        typeof callbacks.clone === 'function' && typeof callbacks.secondary === 'function', 'Trusted native callbacks');
   need(tracks && tracks.RGB && tracks.L && !tracks.RGB.isNull && !tracks.L.isNull, 'Adaptive RGB/L tracks');
   var rgb = tracks.RGB, lum = tracks.L, im = rgb.mainView.image;
   var width = im.width, height = im.height;
   need(width >= 32 && height >= 32 && width <= 12000 && height <= 12000 &&
        im.numberOfNominalChannels === 3 && lum.mainView.image.numberOfNominalChannels === 1 &&
        lum.mainView.image.width === width && lum.mainView.image.height === height, 'Adaptive track geometry');
   ['RGB_STARS','L_STARS','MASK'].forEach(function(role) {
      if (!tracks[role]) return;
      var w = tracks[role];
      need(!w.isNull && w !== rgb && w !== lum && w.mainView.image.width === width &&
           w.mainView.image.height === height &&
           w.mainView.image.numberOfNominalChannels === (role === 'RGB_STARS' ? 3 : 1),
           'Adaptive dependency geometry');
   });
   var linear = ['BACKGROUND','OPTICAL_CORRECT','COLOR','DECONVOLVE','STRETCH'];
   var nonlinear = ['MASK_BUILD','LOCAL_CONTRAST','COMBINE','RECOMBINE'];
   need(linear.indexOf(step.process) < 0 || context.domain === 'LINEAR_ATTESTED', 'Adaptive linear process');
   need(nonlinear.indexOf(step.process) < 0 || context.domain === 'NONLINEAR_ATTESTED', 'Adaptive nonlinear process');
   function run(instance, window, role) {
      callbacks.cancel();
      need(callbacks.apply(instance, window, role) === true, 'Native process or checkpoint history guard failed');
   }
   function model(instance, key) {
      need(context.models && finite(context.models[key]) && context.models[key] > 0 && context.models[key] < 100,
           'Pinned ML model required');
      instance.ml_version = context.models[key];
      need(instance.ml_version === context.models[key], 'Native ML version mismatch');
      return instance;
   }
   function roi(instance, background) {
      var r = context.backgroundROI;
      need(Array.isArray(r) && r.length === 4 && r.every(Number.isInteger) && r[0] >= 0 && r[1] >= 0 &&
           r[2] <= width && r[3] <= height && r[2]-r[0] >= 32 && r[3]-r[1] >= 32, 'Verified background ROI required');
      if (background) {
         instance.backgroundUseROI = true; instance.backgroundROIX0 = r[0]; instance.backgroundROIY0 = r[1];
         instance.backgroundROIX1 = r[2]; instance.backgroundROIY1 = r[3];
      } else {
         instance.useROI = true; instance.roiX0 = r[0]; instance.roiY0 = r[1];
         instance.roiX1 = r[2]; instance.roiY1 = r[3];
      }
   }
   function expression(window, value, role) {
      var instance = new PixelMath;
      instance.expression = value; instance.useSingleExpression = true; instance.createNewImage = false;
      instance.rescale = false; instance.truncate = true; instance.use64BitWorkingImage = true;
      run(instance, window, role);
   }
   function separate(window, role) {
      var before = ImageWindow.windows.map(function(w) {return w.mainView.id;});
      var instance = model(new StarXTerminator, 'STARX');
      instance.output_stars = true; instance.unscreen = false;
      run(instance, window, role);
      var fresh = ImageWindow.windows.filter(function(w) {return before.indexOf(w.mainView.id) < 0;});
      need(fresh.length === 1, 'Unique native stars output required');
      need(fresh[0].mainView.image.width === width && fresh[0].mainView.image.height === height &&
           fresh[0].mainView.image.numberOfNominalChannels === window.mainView.image.numberOfNominalChannels,
           'Native stars geometry');
      callbacks.secondary(fresh[0], role + '_STARS');
      tracks[role + '_STARS'] = fresh[0];
   }
   var instance;
   switch (step.process) {
   case 'BACKGROUND':
      [rgb,lum].forEach(function(w,k) {
         instance = new AutomaticBackgroundExtractor;
         instance.polyDegree = p.polyDegree; instance.boxSize = p.boxSize; instance.boxSeparation = p.boxSeparation;
         instance.tolerance = 0.8; instance.targetCorrection = AutomaticBackgroundExtractor.Correction_Subtract;
         instance.normalize = true; instance.discardModel = true; instance.replaceTarget = true;
         run(instance, w, k ? 'L' : 'RGB');
      });
      break;
   case 'OPTICAL_CORRECT':
      instance = model(new BlurXTerminator, 'BLURX'); instance.correct_only = true;
      instance.auto_nonstellar_psf = true; instance.sharpen_stars = 0; instance.sharpen_nonstellar = 0;
      instance.adjust_star_halos = 0;
      run(instance, rgb, 'RGB');
      break;
   case 'COLOR':
      need(context.mode === 'LRGB' || context.mode === 'OSC', 'Assigned palette is not empirical colour calibration');
      instance = new BackgroundNeutralization; roi(instance, false); instance.backgroundHigh = 0.05;
      run(instance, rgb, 'RGB');
      instance = new ColorCalibration; instance.structureDetection = true; instance.structureLayers = 6;
      instance.noiseLayers = 2; instance.whiteLow = 0; instance.whiteHigh = 0.65;
      roi(instance, true); instance.backgroundHigh = 0.05; run(instance, rgb, 'RGB');
      break;
   case 'DECONVOLVE':
      [rgb,lum].forEach(function(w,k) {
         instance = model(new BlurXTerminator, 'BLURX'); instance.correct_only = false;
         instance.auto_nonstellar_psf = true;
         instance.sharpen_stars = 0.25; instance.sharpen_nonstellar = k ? p.sharpenL : p.sharpenRGB;
         instance.adjust_star_halos = 0; run(instance, w, k ? 'L' : 'RGB');
      });
      break;
   case 'DENOISE':
      [rgb,lum].forEach(function(w,k) {
         instance = model(new NoiseXTerminator, 'NOISEX'); instance.denoise = k ? p.denoiseL : p.denoiseRGB;
         instance.denoise_intensity = 0.65; instance.denoise_color = 0.80;
         instance.enable_color_separation = !k; instance.enable_frequency_separation = false; instance.iterations = 2;
         run(instance, w, k ? 'L' : 'RGB');
      });
      break;
   case 'SEPARATE':
      need(context.branch === 'STARLESS' && !tracks.RGB_STARS && !tracks.L_STARS, 'Distinct stars branch required');
      separate(rgb, 'RGB'); separate(lum, 'L');
      break;
   case 'STRETCH':
      // Check ROI before modifying either working track.
      roi(new MaskedStretch, false);
      if (context.branch === 'STARLESS')
         need(tracks.RGB_STARS && tracks.L_STARS, 'Preserved linear stars required');
      [rgb,lum].forEach(function(w,k) {
         instance = new MaskedStretch; instance.targetBackground = p.targetBackground;
         instance.numberOfIterations = 150; instance.clippingFraction = 0.00001;
         instance.backgroundLow = 0; instance.backgroundHigh = 0.05; instance.maskType = MaskedStretch.MaskType_Intensity;
         roi(instance, false); run(instance, w, k ? 'L' : 'RGB');
      });
      if (context.branch === 'STARLESS') {
         var stars = tracks.RGB_STARS;
         var median = stars.mainView.computeOrFetchProperty('Median');
         var background = [median.at(0),median.at(1),median.at(2)];
         need(background.every(finite), 'Stars median required');
         instance = new PixelMath; instance.useSingleExpression = false; instance.createNewImage = false;
         instance.rescale = false; instance.truncate = true; instance.use64BitWorkingImage = true;
         instance.expression = 'max(0,$T[0]-'+background[0]+')';
         instance.expression1 = 'max(0,$T[1]-'+background[1]+')';
         instance.expression2 = 'max(0,$T[2]-'+background[2]+')'; run(instance, stars, 'RGB_STARS');
         instance = new ArcsinhStretch; instance.stretch = 150; instance.blackPoint = 0;
         instance.protectHighlights = true; instance.useRGBWS = true; instance.previewClipped = false;
         run(instance, stars, 'RGB_STARS');
      }
      break;
   case 'MASK_BUILD':
      need(p.maskHigh-p.maskLow >= 0.05 && !tracks.MASK, 'New mask range required');
      tracks.MASK = callbacks.clone(lum, 'MASK');
      need(tracks.MASK && !tracks.MASK.isNull && tracks.MASK !== lum && tracks.MASK !== rgb &&
           tracks.MASK !== tracks.RGB_STARS && tracks.MASK !== tracks.L_STARS &&
           tracks.MASK.mainView.image.width === width && tracks.MASK.mainView.image.height === height &&
           tracks.MASK.mainView.image.numberOfNominalChannels === 1, 'Distinct native mask copy required');
      expression(tracks.MASK, 'min(1,max(0,($T-'+p.maskLow+')/'+(p.maskHigh-p.maskLow)+'))', 'MASK');
      break;
   case 'LOCAL_CONTRAST':
      need(tracks.MASK && !tracks.MASK.isNull && tracks.MASK.mainView.image.numberOfNominalChannels === 1 &&
           tracks.MASK.mainView.image.width === width && tracks.MASK.mainView.image.height === height,
           'Verified checkpoint mask required');
      lum.mask = tracks.MASK; lum.maskEnabled = true; lum.maskVisible = false; lum.maskInverted = false;
      try {
         [96,48].forEach(function(radius,k) {
            instance = new LocalHistogramEqualization; instance.radius = radius; instance.slopeLimit = 1.6;
            instance.amount = k ? p.contrastSmall : p.contrastLarge; run(instance, lum, 'L');
         });
      } finally {lum.removeMask();}
      break;
   case 'COMBINE':
      need(/^[A-Za-z_][A-Za-z0-9_]*$/.test(lum.mainView.id), 'Trusted luminance view identifier');
      instance = new LRGBCombination;
      instance.channels = [[false,'',1],[false,'',1],[false,'',1],[true,lum.mainView.id,1]];
      instance.mL = 0.5; instance.mc = 0.5; instance.clipHighlights = true; instance.noiseReduction = false;
      run(instance, rgb, 'RGB');
      break;
   case 'RECOMBINE':
      need(context.branch === 'STARLESS' && tracks.RGB_STARS &&
           /^[A-Za-z_][A-Za-z0-9_]*$/.test(tracks.RGB_STARS.mainView.id), 'Preserved nonlinear RGB stars required');
      expression(rgb, '1-(1-$T)*(1-'+tracks.RGB_STARS.mainView.id+')', 'RGB');
      break;
   }
   return tracks;
}
