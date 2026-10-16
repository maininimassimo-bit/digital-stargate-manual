// Pure Float64 algebra. No image/file/network APIs; actual pixels belong to a native wrapper.
// Hashes and supplied factors are declarations, never physical acceptance.
var DSGNativeLinearUncertainty = (function () {
   var EPS = Math.pow(2, -52);
   var COMPONENTS = ['PHOTON_READ_DIGITIZATION', 'DARK_MASTER_AND_TEMPORAL',
      'FLAT_GAIN_NORMALIZATION', 'CALIBRATION', 'SKY_BACKGROUND_ESTIMATOR',
      'RESAMPLING_REGISTRATION', 'QUANTIZATION', 'REFERENCE_PSF_APERTURE_SELECTION'];
   function need(ok, code) { if (!ok) throw Error('LINEAR_' + code); }
   function finite(x) { return typeof x === 'number' && isFinite(x); }
   function integer(x, low, high) { return finite(x) && Math.floor(x) === x && x >= low && x <= high; }
   function fields(x, names) {
      need(x && typeof x === 'object' && !Array.isArray(x) &&
         Object.keys(x).sort().join(',') === names.slice().sort().join(','), 'FIELDS');
   }
   function sha(x) { return typeof x === 'string' && /^[a-f0-9]{64}$/.test(x); }
   function ref(x) { return typeof x === 'string' && /^[a-zA-Z0-9_-]{1,96}$/.test(x); }
   function product(x, y) {
      var p = x * y;
      need(finite(p), 'PRODUCT_OVERFLOW');
      need(x === 0 || y === 0 || p !== 0, 'PRODUCT_UNDERFLOW');
      return p;
   }
   function normalProduct(x, y) {
      var p = product(x, y);
      need(p === 0 || Math.abs(p) >= Math.pow(2, -1022), 'PRODUCT_SUBNORMAL');
      return p;
   }
   function split(x) {
      // Dekker split. Refuse unsupported extremes rather than losing the low part.
      var c = normalProduct(134217729, x);
      var high = c - (c - x);
      need(finite(high), 'SPLIT_OVERFLOW');
      return [high, x - high];
   }
   function addProduct(s, x, y) {
      var p = normalProduct(x, y);
      if (x === 0 || y === 0) { add(s, p); return; }
      var a = split(x), b = split(y);
      // Error-free TwoProduct when the checked intermediates are representable.
      var e1 = p - normalProduct(a[0], b[0]);
      var e2 = e1 - normalProduct(a[1], b[0]);
      var e3 = e2 - normalProduct(a[0], b[1]);
      var error = normalProduct(a[1], b[1]) - e3;
      need(finite(error), 'PRODUCT_ERROR_OVERFLOW');
      add(s, p); add(s, error);
   }
   function accumulator() { return {partials: []}; }
   function add(s, x) {
      // A nonoverlapping expansion retains several levels of cancellation.
      var p = s.partials, retained = 0;
      for (var i = 0; i < p.length; ++i) {
         var y = p[i];
         if (Math.abs(x) < Math.abs(y)) { var swap = x; x = y; y = swap; }
         var high = x + y;
         need(finite(high), 'SUM_OVERFLOW');
         var low = y - (high - x); // FastTwoSum, |x| >= |y|.
         if (low !== 0) p[retained++] = low;
         x = high;
      }
      p.length = retained;
      if (x !== 0) p.push(x);
      need(p.length <= 2048, 'SUM_EXPANSION_BOUND');
   }
   function total(s) {
      var t = 0;
      for (var i = 0; i < s.partials.length; ++i) { t += s.partials[i]; need(finite(t), 'SUM_OVERFLOW'); }
      need(s.partials.length === 0 || t !== 0, 'SUM_RESIDUAL_LOST');
      return t;
   }
   function sum(values) {
      var s = accumulator();
      for (var i = 0; i < values.length; ++i) add(s, values[i]);
      return total(s);
   }
   function dot(a, b) {
      var s = accumulator();
      for (var i = 0; i < a.length; ++i) addProduct(s, a[i], b[i]);
      return total(s);
   }
   function squaredNorm(a) {
      var scale = 0, i;
      for (i = 0; i < a.length; ++i) scale = Math.max(scale, Math.abs(a[i]));
      if (scale === 0) return {variance: 0, sigma: 0};
      var s = accumulator();
      for (i = 0; i < a.length; ++i) {
         var r = a[i] / scale;
         need(a[i] === 0 || r !== 0, 'RATIO_UNDERFLOW');
         add(s, product(r, r));
      }
      var sigma = product(scale, Math.sqrt(total(s)));
      return {variance: product(sigma, sigma), sigma: sigma};
   }
   function inspect(m) {
      fields(m, ['protocol', 'identity', 'grid', 'pixelIndices', 'samples', 'aperture',
         'background', 'basis', 'factors', 'budget']);
      need(m.protocol === 'DSG_NATIVE_LINEAR_UNCERTAINTY_V1', 'PROTOCOL');
      fields(m.identity, ['imageSha256', 'gridSha256', 'maskSha256', 'normalizationSha256',
         'weightSha256', 'modelSha256', 'factorSourceSha256', 'epochRef', 'unit', 'coordinateConvention']);
      var hashes = ['imageSha256', 'gridSha256', 'maskSha256', 'normalizationSha256',
         'weightSha256', 'modelSha256', 'factorSourceSha256'];
      for (var h = 0; h < hashes.length; ++h) need(sha(m.identity[hashes[h]]), 'HASH');
      need(ref(m.identity.epochRef) && ['ADU', 'NORMALIZED_SAMPLE', 'NANOMAGGY_PER_PIXEL'].indexOf(m.identity.unit) >= 0 &&
         m.identity.coordinateConvention === 'PI_NATIVE_GEOMETRIC_ROW_MAJOR', 'IDENTITY');
      fields(m.grid, ['width', 'height', 'channels', 'channel']);
      need(integer(m.grid.width, 1, 100000000) && integer(m.grid.height, 1, 100000000) &&
         m.grid.width * m.grid.height <= 100000000 && integer(m.grid.channels, 1, 16) &&
         integer(m.grid.channel, 0, m.grid.channels - 1), 'GRID');
      need(Array.isArray(m.pixelIndices) && m.pixelIndices.length >= 2 && m.pixelIndices.length <= 16384, 'SUPPORT');
      var n = m.pixelIndices.length, arrays = [m.samples, m.aperture, m.background], i, j;
      for (i = 0; i < arrays.length; ++i) need(Array.isArray(arrays[i]) && arrays[i].length === n, 'VECTOR');
      for (i = 0; i < n; ++i) {
         need(integer(m.pixelIndices[i], 0, m.grid.width * m.grid.height - 1) &&
            (i === 0 || m.pixelIndices[i] > m.pixelIndices[i - 1]), 'PIXEL_ORDER');
         need(finite(m.samples[i]) && finite(m.aperture[i]) && finite(m.background[i]), 'NONFINITE');
         need(m.aperture[i] >= 0 && m.aperture[i] <= 1 && m.background[i] >= 0 && m.background[i] <= 1 &&
            !(m.aperture[i] > 0 && m.background[i] > 0) &&
            (m.aperture[i] > 0 || m.background[i] > 0), 'WEIGHTS');
      }
      var alpha = sum(m.aperture), backgroundResidual = sum(m.background) - 1;
      var tau = 64 * EPS * n, w = [];
      need(alpha > 0 && Math.abs(backgroundResidual) <= tau, 'BACKGROUND_NORMALIZATION');
      for (i = 0; i < n; ++i) w.push(m.aperture[i] - product(alpha, m.background[i]));
      var skyResidual = sum(w);
      need(Math.abs(skyResidual) <= tau * Math.max(1, alpha), 'CONSTANT_SKY_RESIDUAL');
      fields(m.basis, ['sha256', 'whiteningEvidenceSha256', 'latentRefs']);
      need(sha(m.basis.sha256) && sha(m.basis.whiteningEvidenceSha256) && Array.isArray(m.basis.latentRefs) &&
         m.basis.latentRefs.length >= 1 && m.basis.latentRefs.length <= 16384, 'BASIS');
      var seen = {}, refs = m.basis.latentRefs;
      for (i = 0; i < refs.length; ++i) {
         need(ref(refs[i]) && !Object.prototype.hasOwnProperty.call(seen, '$' + refs[i]), 'LATENT_ID');
         seen['$' + refs[i]] = true;
      }
      need(Array.isArray(m.factors) && m.factors.length === refs.length, 'FACTOR_COVERAGE');
      var count = 0, u = [];
      for (i = 0; i < refs.length; ++i) {
         var f = m.factors[i];
         fields(f, ['latentRef', 'rows', 'responses', 'structuralZeroEvidenceSha256']);
         need(f.latentRef === refs[i] && Array.isArray(f.rows) && Array.isArray(f.responses) &&
            f.rows.length === f.responses.length && f.rows.length <= n, 'FACTOR');
         count += f.rows.length;
         need(count <= 1048576, 'RESPONSE_BOUND');
         need(f.rows.length === 0 ? sha(f.structuralZeroEvidenceSha256) : f.structuralZeroEvidenceSha256 === null, 'STRUCTURAL_ZERO');
         var s = accumulator();
         for (j = 0; j < f.rows.length; ++j) {
            need(integer(f.rows[j], 0, n - 1) && (j === 0 || f.rows[j] > f.rows[j - 1]), 'FACTOR_ROW');
            need(finite(f.responses[j]) && f.responses[j] !== 0, 'FACTOR_RESPONSE');
            addProduct(s, w[f.rows[j]], f.responses[j]);
         }
         u.push(total(s));
      }
      need(Array.isArray(m.budget) && m.budget.length === COMPONENTS.length, 'BUDGET');
      var states = [];
      for (i = 0; i < COMPONENTS.length; ++i) {
         var b = m.budget[i];
         fields(b, ['component', 'state', 'evidenceSha256', 'domainSha256']);
         need(b.component === COMPONENTS[i] && ['REPRESENTED_JOINTLY', 'EXCLUDED_WITH_DOMAIN_EVIDENCE', 'MISSING'].indexOf(b.state) >= 0, 'BUDGET_COMPONENT');
         need(b.state === 'MISSING' ? b.evidenceSha256 === null && b.domainSha256 === null :
            sha(b.evidenceSha256) && sha(b.domainSha256), 'BUDGET_EVIDENCE');
         states.push({component: b.component, state: b.state, evidenceSha256: b.evidenceSha256, domainSha256: b.domainSha256});
      }
      var norm = squaredNorm(u), identity = {};
      Object.keys(m.identity).forEach(function (key) { identity[key] = m.identity[key]; });
      return {protocol: 'DSG_NATIVE_LINEAR_UNCERTAINTY_RESULT_V1', identity: identity,
         fluxUnit: m.identity.unit + '_WEIGHTED_SUM', varianceUnit: '(' + m.identity.unit + '_WEIGHTED_SUM)^2',
         basisSha256: m.basis.sha256, whiteningEvidenceSha256: m.basis.whiteningEvidenceSha256,
         latentRefs: refs.slice(), latentResponses: u, budget: states,
         observedFiniteApertureFlux: dot(w, m.samples),
         varianceUnderSuppliedJointModel: norm.variance,
         standardUncertaintyUnderSuppliedJointModel: norm.sigma,
         diagnostics: {arithmetic: 'FLOAT64_TWO_PRODUCT_EXPANSION_SUM_SCALED_NORM', supportPixels: n,
            nonzeroResponses: count, alpha: alpha, backgroundNormalizationResidual: backgroundResidual,
            constantSkyResidual: skyResidual, normalizationTolerance: tau,
            constantSkyTolerance: tau * Math.max(1, alpha), roundoffErrorBound: null},
         provenanceVerified: false, physicalApplicabilityVerified: false,
         fullPhysicalVariance: null, significance: null, scientificValidation: 'NOT_VALIDATED', qualifiedControls: 0};
   }
   function compare(leftInput, rightInput) {
      // Recompute from inputs; never accept caller-authored result objects as evidence.
      var l = inspect(leftInput), r = inspect(rightInput);
      need(l.basisSha256 === r.basisSha256 && l.whiteningEvidenceSha256 === r.whiteningEvidenceSha256 &&
         l.latentRefs.length === r.latentRefs.length &&
         l.identity.unit === r.identity.unit &&
         l.identity.normalizationSha256 === r.identity.normalizationSha256, 'CROSS_BASIS_OR_UNIT');
      var d = [];
      for (var i = 0; i < l.latentRefs.length; ++i) {
         need(l.latentRefs[i] === r.latentRefs[i], 'CROSS_LATENT_ORDER');
         d.push(sum([l.latentResponses[i], -r.latentResponses[i]]));
      }
      return {protocol: 'DSG_NATIVE_LINEAR_CROSS_RESULT_V1', basisSha256: l.basisSha256,
         covarianceUnderSuppliedJointModel: dot(l.latentResponses, r.latentResponses),
         differenceUnderSuppliedJointModel: sum([l.observedFiniteApertureFlux, -r.observedFiniteApertureFlux]),
         differenceVarianceUnderSuppliedJointModel: squaredNorm(d).variance,
         fullPhysicalVariance: null, significance: null, scientificValidation: 'NOT_VALIDATED', qualifiedControls: 0};
   }
   return {inspect: inspect, compare: compare};
}());
