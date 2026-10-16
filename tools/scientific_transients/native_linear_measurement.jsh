// Definition only. Requires the three sealed DSG libraries and actual PJSR APIs.
// No launcher, grant creation, network, parent publication or scientific acceptance.
function DSGNativeLinearMeasurement(root) {
   function need(ok, code) { if (!ok) throw Error('NATIVE_LINEAR_' + code); }
   function integer(x, lo, hi) { return typeof x === 'number' && isFinite(x) && Math.floor(x) === x && x >= lo && x <= hi; }
   function sha(x) { return typeof x === 'string' && /^[a-f0-9]{64}$/.test(x); }
   function fields(x, keys) { need(x && typeof x === 'object' && !Array.isArray(x) && Object.keys(x).sort().join(',') === keys.slice().sort().join(','), 'FIELDS'); }
   var MIB = 1048576, BYTE_ARRAY_TYPE = 15; // Installed PJSR DataType.jsh SHA503f8d097b7b7a6a1892cb7d00e782e1fbccecb6746987d52e9b758793a4e298.
   var entryUTC = Date.now(), timer = new ElapsedTime, remaining = 180, deadline = null, lastUTC = entryUTC;
   var operation = null, owned = [], written = Object.create(null), products = [], totalBytes = 0, extraBytes = 0;
   var sourceHandle = null, logOpen = false, overrun = false, retentionError = null;
   var names = ['started-native.json', 'native.log', 'result.json', 'native-evidence.json', 'checkpoint.xisf',
      'source-initial.js', 'source-before.js', 'source-after.js', 'checkpoint-initial.js', 'checkpoint-current.js',
      'closing-source.js', 'closing-checkpoint.js', 'error-owned-1.xisf', 'error-owned-2.xisf', 'terminal.json', 'terminal-ready.json',
      'native-publication-uncertain.json'];
   var components = ['PHOTON_READ_DIGITIZATION', 'DARK_MASTER_AND_TEMPORAL', 'FLAT_GAIN_NORMALIZATION',
      'CALIBRATION', 'SKY_BACKGROUND_ESTIMATOR', 'RESAMPLING_REGISTRATION', 'QUANTIZATION', 'REFERENCE_PSF_APERTURE_SELECTION'];
   need(typeof root === 'string' && /^[A-Za-z]:\//.test(root) && root.length <= 512 &&
      !/[\x00-\x1f\x7f-\uffff\\"'<>|:*?\[\]]/.test(root.slice(2)) && !/\/$/.test(root), 'ROOT');
   root.slice(3).split('/').forEach(function (p) { need(p.length > 0 && p !== '.' && p !== '..' && !/[. ]$/.test(p), 'ROOT_COMPONENT'); });
   function checkTime(retaining) {
      var now = Date.now(), elapsed = timer.value;
      need(typeof elapsed === 'number' && isFinite(elapsed) && elapsed >= 0, 'MONOTONIC_CLOCK');
      var invalid = now < lastUTC || now < entryUTC;
      lastUTC = now;
      var expired = invalid || elapsed >= remaining || (deadline !== null && now >= deadline);
      if (expired) overrun = true;
      if (!retaining) need(!expired, invalid ? 'CLOCK_CHANGED' : 'DEADLINE');
   }
   function digest(bytes) { return new CryptographicHash(CryptographicHash.SHA256).hash(bytes).toHex(); }
   function bounded(path, cap, expected, hold, monitor) {
      var f = new File, kept = false;
      try {
         f.openForReading(path);
         var size = f.size;
         need(integer(size, 1, cap) && (expected === null || size === expected), 'READ_SIZE');
         if (monitor) monitor();
         var raw = f.read(BYTE_ARRAY_TYPE, size);
         need(raw.length === size && f.size === size, 'READ_CHANGED');
         var bytes = raw.toUint8Array();
         need(bytes.length === size, 'READ_CONVERSION');
         var hash = digest(raw);
         if (monitor) monitor();
         kept = hold;
         return {bytes: bytes, sha256: hash, byteLength: size, handle: hold ? f : null};
      } finally { if (!kept) f.close(); }
   }
   function readJSON(name, cap, monitor) {
      var raw = bounded(root + '/' + name, cap, null, false, monitor);
      return {value: parseStrictPassiveAsciiJson(raw.bytes, {maxBytes: cap, checkBudget: monitor || null}),
         sha256: raw.sha256, byteLength: raw.byteLength};
   }
   function cancellation() {
      if (!File.exists(root + '/cancel.json')) return;
      var c = readJSON('cancel.json', MIB, null).value;
      fields(c, ['protocol', 'operationRef', 'requested']);
      need(c.protocol === 'DSG_NATIVE_LINEAR_CANCEL_V1' && c.operationRef === operation && c.requested === true, 'CANCEL_SCHEMA');
      throw Error('NATIVE_LINEAR_CANCELLED');
   }
   function budget() { checkTime(false); cancellation(); }
   function hashFile(name, cap, monitor) {
      var f = new File;
      try {
         f.openForReading(root + '/' + name);
         var size = f.size, read = 0, h = new CryptographicHash(CryptographicHash.SHA256);
         need(integer(size, 0, cap), 'HASH_SIZE');
         h.initialize();
         while (read < size) {
            if (monitor) monitor();
            var count = Math.min(65536, size - read), part = f.read(BYTE_ARRAY_TYPE, count);
            need(part.length === count && f.size === size, 'HASH_CHANGED');
            h.update(part); read += count;
         }
         if (monitor) monitor();
         need(f.size === size, 'HASH_CHANGED');
         return {sha256: h.finalize().toHex(), byteLength: size};
      } finally { f.close(); }
   }
   function utc(text) {
      need(typeof text === 'string' && /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/.test(text), 'UTC');
      var n = Date.parse(text);
      need(isFinite(n) && new Date(n).toISOString().replace('.000Z', 'Z') === text, 'UTC');
      return n;
   }
   function code(error) {
      var text = error && error.message;
      return typeof text === 'string' && /^[A-Z0-9_]{1,96}$/.test(text) ? text : 'NATIVE_LINEAR_API_FAILURE';
   }
   function limit(name) {
      if (/\.xisf$/.test(name)) return 192 * MIB;
      if (/\.js$/.test(name)) return 4 * MIB;
      if (name === 'native.log') return 32 * MIB;
      if (name === 'result.json') return 8 * MIB;
      return MIB;
   }
   function absent(name) {
      need(names.indexOf(name) >= 0 && !written[name] && !File.exists(root + '/' + name), 'OUTPUT_COLLISION');
      written[name] = true; // A failed first write cannot be repeated in this invocation.
   }
   function addProduct(name) {
      need(!products.some(function (p) { return p.name === name; }), 'PRODUCT_DUPLICATE');
      var pin = hashFile(name, limit(name), function () { checkTime(true); });
      need(products.length < 18 && totalBytes + pin.byteLength <= 192 * MIB, 'PRODUCT_AGGREGATE');
      totalBytes += pin.byteLength;
      products.push({role: name, name: name, sha256: pin.sha256, byteLength: pin.byteLength});
   }
   function utf8Size(text, cap) {
      need(typeof text === 'string' && text.length <= cap, 'TEXT_BOUND');
      var bytes = 0;
      for (var i = 0; i < text.length; ++i) {
         var c = text.charCodeAt(i);
         if (c < 128) ++bytes;
         else if (c < 2048) bytes += 2;
         else if (c >= 55296 && c <= 56319 && i + 1 < text.length && text.charCodeAt(i + 1) >= 56320 && text.charCodeAt(i + 1) <= 57343) { bytes += 4; ++i; }
         else bytes += 3;
         need(bytes <= cap, 'TEXT_BOUND');
         if (i % 4096 === 0) checkTime(true);
      }
      return bytes;
   }
   function writeText(name, text, product) {
      var bytes = utf8Size(text, limit(name));
      need(totalBytes + extraBytes + bytes <= 192 * MIB, 'PRODUCT_AGGREGATE');
      absent(name);
      File.writeTextFile(root + '/' + name, text); // W7 fresh single-writer scratch, NOT atomic create-new.
      var pin = hashFile(name, limit(name), function () { checkTime(true); });
      need(pin.byteLength === bytes && pin.sha256 === digest(text), 'WRITE_READBACK');
      if (product) addProduct(name);
      else extraBytes += bytes;
      return pin;
   }
   function writeJSON(name, value, product) {
      var text = JSON.stringify(value);
      need(typeof text === 'string' && /^[\x00-\x7f]*$/.test(text), 'JSON_OUTPUT_ASCII');
      var pin = writeText(name, text, product);
      var reread = readJSON(name, limit(name), null);
      need(reread.sha256 === pin.sha256 && JSON.stringify(reread.value) === text, 'JSON_WRITE_READBACK');
      return pin;
   }
   function history(window, which, name) {
      var view = window.mainView;
      writeText(name, (which === 'initial' ? view.initialProcessing : view.processing).toSource(), true);
   }
   function save(window, name) {
      absent(name);
      need(window.saveAs(root + '/' + name, false, false, true, false, 'properties fits-keywords no-compress-data'), 'CHECKPOINT_SAVE');
      addProduct(name);
   }
   function geometry(window, source) {
      var image = window.mainView.image;
      need(image.width === source.width && image.height === source.height && image.numberOfChannels === 1 &&
         image.numberOfNominalChannels === 1 && image.bitsPerSample === 64 && !image.isInteger && !image.isComplex, 'IMAGE_GEOMETRY');
      return image;
   }
   function compare(window, expected, source, monitor) {
      var image = geometry(window, source), visited = 0;
      for (var y = 0; y < source.height; ++y) {
         for (var x = 0; x < source.width; x += 65536) {
            monitor();
            var count = Math.min(65536, source.width - x), values = new Float64Array(count);
            image.getSamples(values, x, y, x + count, y + 1, 0);
            for (var i = 0; i < count; ++i) {
               need(Object.is(values[i], expected[y * source.width + x + i]), 'IMAGE_VALUE_CHANGED');
               if (++visited % 4096 === 0) monitor();
            }
         }
      }
      monitor();
   }
   function frozen(value, count) {
      if (value === null || typeof value !== 'object') return;
      need(++count.nodes <= 65536, 'FREEZE_BOUND');
      Object.keys(value).forEach(function (key) {
         if (++count.steps % 4096 === 0) budget();
         frozen(value[key], count);
      });
      Object.freeze(value);
   }
   function kernelShape(k, p) {
      fields(k, ['protocol', 'identity', 'grid', 'pixelIndices', 'aperture', 'background', 'basis', 'factors', 'budget']);
      need(k.protocol === 'DSG_NATIVE_LINEAR_UNCERTAINTY_V1', 'KERNEL_PROTOCOL');
      fields(k.identity, ['imageSha256', 'gridSha256', 'maskSha256', 'normalizationSha256', 'weightSha256', 'modelSha256',
         'factorSourceSha256', 'epochRef', 'unit', 'coordinateConvention']);
      ['imageSha256', 'gridSha256', 'maskSha256', 'normalizationSha256', 'weightSha256', 'modelSha256', 'factorSourceSha256'].forEach(function (name) { need(sha(k.identity[name]), 'KERNEL_HASH'); });
      need(k.identity.imageSha256 === p.source.sha256 && typeof k.identity.epochRef === 'string' && /^[a-zA-Z0-9_-]{1,96}$/.test(k.identity.epochRef) &&
         ['ADU', 'NORMALIZED_SAMPLE', 'NANOMAGGY_PER_PIXEL'].indexOf(k.identity.unit) >= 0 &&
         k.identity.coordinateConvention === 'PI_NATIVE_GEOMETRIC_ROW_MAJOR', 'KERNEL_IDENTITY');
      fields(k.grid, ['width', 'height', 'channels', 'channel']);
      need(k.grid.width === p.source.width && k.grid.height === p.source.height && k.grid.channels === 1 && k.grid.channel === 0, 'KERNEL_GRID');
      need(Array.isArray(k.pixelIndices) && integer(k.pixelIndices.length, 2, 16384), 'KERNEL_SUPPORT');
      var n = k.pixelIndices.length, alpha = 0, sky = 0;
      [k.aperture, k.background].forEach(function (v) { need(Array.isArray(v) && v.length === n, 'KERNEL_VECTOR'); });
      for (var i = 0; i < n; ++i) {
         need(integer(k.pixelIndices[i], 0, p.source.width * p.source.height - 1) && (i === 0 || k.pixelIndices[i] > k.pixelIndices[i - 1]), 'KERNEL_INDEX');
         need(typeof k.aperture[i] === 'number' && typeof k.background[i] === 'number' &&
            k.aperture[i] >= 0 && k.aperture[i] <= 1 && k.background[i] >= 0 && k.background[i] <= 1 &&
            !(k.aperture[i] > 0 && k.background[i] > 0) && (k.aperture[i] > 0 || k.background[i] > 0), 'KERNEL_WEIGHTS');
         alpha += k.aperture[i]; sky += k.background[i];
         if (i % 4096 === 0) budget();
      }
      need(alpha > 0 && Math.abs(sky - 1) <= 64 * Math.pow(2, -52) * n, 'KERNEL_BACKGROUND');
      fields(k.basis, ['sha256', 'whiteningEvidenceSha256', 'latentRefs']);
      need(sha(k.basis.sha256) && sha(k.basis.whiteningEvidenceSha256) && Array.isArray(k.basis.latentRefs) &&
         integer(k.basis.latentRefs.length, 1, 16384) && Array.isArray(k.factors) && k.factors.length === k.basis.latentRefs.length, 'KERNEL_BASIS');
      var seen = Object.create(null), responses = 0;
      for (i = 0; i < k.factors.length; ++i) {
         budget();
         var ref = k.basis.latentRefs[i], f = k.factors[i];
         need(typeof ref === 'string' && /^[a-zA-Z0-9_-]{1,96}$/.test(ref) && !seen[ref], 'KERNEL_LATENT'); seen[ref] = true;
         fields(f, ['latentRef', 'rows', 'responses', 'structuralZeroEvidenceSha256']);
         need(f.latentRef === ref && Array.isArray(f.rows) && Array.isArray(f.responses) && f.rows.length <= n &&
            f.rows.length === f.responses.length, 'KERNEL_FACTOR');
         responses += f.rows.length; need(responses <= 1048576, 'KERNEL_RESPONSE_BOUND');
         need(f.rows.length === 0 ? sha(f.structuralZeroEvidenceSha256) : f.structuralZeroEvidenceSha256 === null, 'KERNEL_STRUCTURAL_ZERO');
         for (var j = 0; j < f.rows.length; ++j) {
            need(integer(f.rows[j], 0, n - 1) && (j === 0 || f.rows[j] > f.rows[j - 1]) &&
               typeof f.responses[j] === 'number' && isFinite(f.responses[j]) && f.responses[j] !== 0, 'KERNEL_RESPONSE');
            if (j % 4096 === 0) budget();
         }
      }
      need(Array.isArray(k.budget) && k.budget.length === components.length, 'KERNEL_BUDGET');
      k.budget.forEach(function (b, index) {
         fields(b, ['component', 'state', 'evidenceSha256', 'domainSha256']);
         need(b.component === components[index] && ['REPRESENTED_JOINTLY', 'EXCLUDED_WITH_DOMAIN_EVIDENCE', 'MISSING'].indexOf(b.state) >= 0,
            'KERNEL_BUDGET_STATE');
         need(b.state === 'MISSING' ? b.evidenceSha256 === null && b.domainSha256 === null : sha(b.evidenceSha256) && sha(b.domainSha256), 'KERNEL_BUDGET_EVIDENCE');
      });
   }
   // Bootstrap is read-only. Failure here cannot authorize a native attempt or overwrite output.
   names.forEach(function (name) { need(!File.exists(root + '/' + name), 'INITIAL_OUTPUT_COLLISION'); });
   var grantRead = readJSON('launch-grant.json', MIB, function () { checkTime(false); });
   var grant = grantRead.value;
   fields(grant, ['protocol', 'operationRef', 'sealSha256', 'purpose', 'authorized', 'maxStarts', 'maxRuntimeSeconds', 'expiresUTC', 'createdUTC', 'deadlineUTC']);
   need(grant.protocol === 'DSG_NATIVE_LINEAR_SINGLE_START_GRANT_V1' && typeof grant.operationRef === 'string' && /^[a-f0-9]{32}$/.test(grant.operationRef) &&
      sha(grant.sealSha256) && grant.purpose === 'DEVELOPMENT' && grant.authorized === true && grant.maxStarts === 1 && grant.maxRuntimeSeconds === 180, 'FRESH_GRANT');
   operation = grant.operationRef;
   need(root.slice(root.lastIndexOf('/') + 1) === operation, 'OPERATION_DIRECTORY');
   var created = utc(grant.createdUTC), expires = utc(grant.expiresUTC);
   deadline = utc(grant.deadlineUTC);
   need(created <= entryUTC && deadline === created + 180000 && expires <= deadline && expires > Date.now() && entryUTC < expires, 'GRANT_TIME');
   remaining = Math.min(180, (deadline - entryUTC) / 1000); checkTime(false);
   var sealRead = readJSON('launch-seal.json', MIB, function () { checkTime(false); }), seal = sealRead.value;
   fields(seal, ['protocol', 'operationRef', 'createdUTC', 'files', 'arbSha256', 'rqSha256', 'inputClosureAccepted']);
   need(sealRead.sha256 === grant.sealSha256 && seal.protocol === 'DSG_NATIVE_LINEAR_LAUNCH_SEAL_V1' && seal.operationRef === operation &&
      utc(seal.createdUTC) <= created && sha(seal.arbSha256) && sha(seal.rqSha256) && seal.inputClosureAccepted === false &&
      Array.isArray(seal.files) && integer(seal.files.length, 8, 72), 'SEAL');
   var sealed = Object.create(null), inputBytes = sealRead.byteLength + grantRead.byteLength;
   var fixed = ['parameters.json', 'kernel-spec.json', 'source.fits', 'source-lineage.json', 'native_linear_uncertainty.jsh',
      'native_linear_measurement.jsh', 'strict_passive_json.jsh', 'native_float32_primary.jsh'];
   seal.files.forEach(function (r) {
      fields(r, ['role', 'name', 'sha256', 'byteLength']);
      need(typeof r.name === 'string' && (fixed.indexOf(r.name) >= 0 || /^source-card-[a-f0-9]{64}\.json$/.test(r.name)) &&
         r.role === r.name && !sealed[r.name] && sha(r.sha256) && integer(r.byteLength, 1, r.name === 'source.fits' || r.name === 'kernel-spec.json' ? 64 * MIB : MIB), 'SEALED_ROLE');
      if (/^source-card-/.test(r.name)) need(r.name === 'source-card-' + r.sha256 + '.json', 'CARD_FILENAME');
      sealed[r.name] = r; inputBytes += r.byteLength;
   });
   need(inputBytes <= 200 * MIB && fixed.every(function (name) { return !!sealed[name]; }), 'INPUT_CLOSURE');
   function enumeration(allowed) {
      var finder = new FileFind, found = [], active = finder.begin(root + '/*');
      try {
         while (active) {
            var name = finder.name;
            if (name !== '.' && name !== '..') {
               need(finder.isFile === true && finder.isDirectory === false && finder.isSymbolicLink === false && finder.isRedirectionPoint === false &&
                  finder.isReparsePoint === false && allowed.indexOf(name) >= 0 && found.indexOf(name) < 0, 'UNEXPECTED_ENTRY');
               found.push(name); need(found.length <= 75, 'ENTRY_BOUND');
            }
            active = finder.next();
         }
      } finally { finder.end(); }
      return found;
   }
   var initialNames = fixed.concat(Object.keys(sealed).filter(function (n) { return fixed.indexOf(n) < 0; }), ['launch-seal.json', 'launch-grant.json']);
   var initial = enumeration(initialNames.concat(['cancel.json']));
   need(initialNames.every(function (n) { return initial.indexOf(n) >= 0; }), 'MISSING_INPUT');
   function rehashInputs(monitor) {
      seal.files.concat([{name: 'launch-seal.json', sha256: sealRead.sha256, byteLength: sealRead.byteLength},
         {name: 'launch-grant.json', sha256: grantRead.sha256, byteLength: grantRead.byteLength}]).forEach(function (r) {
         var actual = hashFile(r.name, r.byteLength, monitor);
         need(actual.sha256 === r.sha256 && actual.byteLength === r.byteLength, 'SEALED_BYTES_CHANGED');
      });
   }
   rehashInputs(function () { checkTime(false); });
   var parameterRead = readJSON('parameters.json', MIB, function () { checkTime(false); }), p = parameterRead.value;
   need(parameterRead.sha256 === sealed['parameters.json'].sha256, 'PARAMETER_BYTES_CHANGED');
   fields(p, ['protocol', 'operationRef', 'purpose', 'expectedPixInsightVersion', 'kernelSpecSha256', 'lineageSha256', 'source', 'dependencies', 'maxRuntimeSeconds', 'bindings']);
   need(p.protocol === 'DSG_NATIVE_LINEAR_MEASUREMENT_V1' && p.operationRef === operation && p.purpose === 'DEVELOPMENT' && p.maxRuntimeSeconds === 180 &&
      typeof p.expectedPixInsightVersion === 'string' && /^[\x20-\x7e]{1,96}$/.test(p.expectedPixInsightVersion) &&
      p.kernelSpecSha256 === sealed['kernel-spec.json'].sha256 && p.lineageSha256 === sealed['source-lineage.json'].sha256, 'PARAMETERS');
   fields(p.source, ['sha256', 'byteLength', 'primaryHeaderSha256', 'dataOffset', 'width', 'height', 'sampleFormat', 'orientation', 'bscale', 'bzero']);
   need(p.source.sha256 === sealed['source.fits'].sha256 && p.source.byteLength === sealed['source.fits'].byteLength && sha(p.source.primaryHeaderSha256) &&
      integer(p.source.width, 1, 4194304) && integer(p.source.height, 1, 4194304) && p.source.width * p.source.height <= 4194304 &&
      integer(p.source.dataOffset, 2880, 1048320) && p.source.dataOffset % 2880 === 0 && p.source.sampleFormat === 'FLOAT32_BE' &&
      p.source.orientation === 'FITS_AXIS1_FAST_NO_FLIP' && p.source.bscale === 1 && p.source.bzero === 0, 'SOURCE_PARAMETERS');
   fields(p.dependencies, ['coreSha256', 'wrapperSha256', 'parserSha256', 'primarySha256']);
   [['coreSha256', 'native_linear_uncertainty.jsh'], ['wrapperSha256', 'native_linear_measurement.jsh'],
      ['parserSha256', 'strict_passive_json.jsh'], ['primarySha256', 'native_float32_primary.jsh']].forEach(function (pair) {
      need(p.dependencies[pair[0]] === sealed[pair[1]].sha256, 'DEPENDENCY_BINDING');
   });
   var version = [CoreApplication.versionMajor, CoreApplication.versionMinor, CoreApplication.versionRelease].join('.') + ' build ' + CoreApplication.versionBuild;
   need(version === p.expectedPixInsightVersion && DSGNativeLinearUncertainty.budgetMonitorProtocol === 'DSG_NATIVE_LINEAR_TRUSTED_BUDGET_V1', 'RUNTIME');
   var terminalState = 'FAILED_RETAINED', errorCode = null, result = null, sourceWindow = null, decoded = null;
   absent('native.log'); console.beginLog(root + '/native.log'); logOpen = true;
   try {
      writeJSON('started-native.json', {protocol: 'DSG_NATIVE_LINEAR_STARTED_V1', operationRef: operation,
         parametersSha256: parameterRead.sha256, sealSha256: sealRead.sha256, pixInsightVersion: version, maxStarts: 1}, true);
      budget();
      var kernelRead = readJSON('kernel-spec.json', 64 * MIB, budget), kernel = kernelRead.value;
      var lineageRead = readJSON('source-lineage.json', MIB, budget), lineage = lineageRead.value;
      need(kernelRead.sha256 === p.kernelSpecSha256 && lineageRead.sha256 === p.lineageSha256, 'MODEL_BYTES_CHANGED');
      fields(lineage, ['protocol', 'sourceSha256', 'parentManifestSha256', 'providerProductCardSha256', 'upstreamPixInsightHistory', 'interpretation']);
      need(lineage.protocol === 'DSG_NATIVE_SOURCE_LINEAGE_V1' && lineage.sourceSha256 === p.source.sha256 && sha(lineage.parentManifestSha256) &&
         sha(lineage.providerProductCardSha256) && lineage.upstreamPixInsightHistory === 'NOT_PRESENT_IN_SOURCE_FITS' &&
         lineage.interpretation === 'SOURCE_PROVENANCE_NOT_PHYSICAL_ACCEPTANCE', 'LINEAGE');
      kernelShape(kernel, p);
      var references = Object.create(null);
      ['gridSha256', 'maskSha256', 'normalizationSha256', 'weightSha256', 'modelSha256', 'factorSourceSha256'].forEach(function (key) { references['identity.' + key] = kernel.identity[key]; });
      references['basis.sha256'] = kernel.basis.sha256; references['basis.whiteningEvidenceSha256'] = kernel.basis.whiteningEvidenceSha256;
      kernel.budget.forEach(function (b) { if (b.state !== 'MISSING') {
         references['budget.' + b.component + '.evidenceSha256'] = b.evidenceSha256;
         references['budget.' + b.component + '.domainSha256'] = b.domainSha256;
      }});
      references['lineage.parentManifestSha256'] = lineage.parentManifestSha256;
      references['lineage.providerProductCardSha256'] = lineage.providerProductCardSha256;
      need(Array.isArray(p.bindings) && p.bindings.length === Object.keys(references).length && p.bindings.length <= 64, 'BINDING_COUNT');
      var boundRoles = Object.create(null), boundCards = Object.create(null);
      p.bindings.forEach(function (b) {
         budget(); fields(b, ['role', 'referenceSha256', 'cardSha256']);
         need(typeof b.role === 'string' && references[b.role] === b.referenceSha256 && sha(b.referenceSha256) && sha(b.cardSha256) && !boundRoles[b.role], 'BINDING_ROLE');
         var name = 'source-card-' + b.cardSha256 + '.json';
         need(sealed[name] && sealed[name].sha256 === b.cardSha256, 'BINDING_CLOSURE');
         var cardRead = readJSON(name, MIB, budget), c = cardRead.value;
         fields(c, ['protocol', 'role', 'referenceSha256', 'sourceSha256', 'kernelSpecSha256', 'scope']);
         need(cardRead.sha256 === b.cardSha256 && c.protocol === 'DSG_NATIVE_LINEAR_BINDING_CARD_V1' && c.role === b.role && c.referenceSha256 === b.referenceSha256 &&
            c.sourceSha256 === p.source.sha256 && c.kernelSpecSha256 === p.kernelSpecSha256 && c.scope === 'DECLARATION_ONLY_NOT_PHYSICAL_ACCEPTANCE', 'BINDING_CARD');
         boundRoles[b.role] = true; boundCards[name] = true;
      });
      need(Object.keys(sealed).filter(function (n) { return /^source-card-/.test(n); }).every(function (n) { return !!boundCards[n]; }), 'UNUSED_CARD');
      var raw = bounded(root + '/source.fits', 64 * MIB, p.source.byteLength, true, budget);
      sourceHandle = raw.handle;
      need(raw.sha256 === p.source.sha256 && digest(raw.bytes.subarray(0, p.source.dataOffset)) === p.source.primaryHeaderSha256, 'SOURCE_BYTES_CHANGED');
      decoded = DSGNativeFloat32Primary.decode(raw.bytes, {byteLength: p.source.byteLength, dataOffset: p.source.dataOffset, width: p.source.width, height: p.source.height}, budget).values;
      raw.bytes = null;
      budget();
      sourceWindow = new ImageWindow(p.source.width, p.source.height, 1, 64, true, false, 'DSG_linear_' + operation);
      owned.push({window: sourceWindow, kind: 'source'});
      geometry(sourceWindow, p.source);
      history(sourceWindow, 'initial', 'source-initial.js');
      var processOpen = false;
      try {
         sourceWindow.mainView.beginProcess(0); processOpen = true;
         sourceWindow.mainView.image.setSamples(decoded);
      } finally { if (processOpen) sourceWindow.mainView.endProcess(); }
      compare(sourceWindow, decoded, p.source, budget);
      history(sourceWindow, 'current', 'source-before.js');
      kernel.samples = [];
      kernel.pixelIndices.forEach(function (index, i) {
         if (i % 4096 === 0) budget();
         var sample = sourceWindow.mainView.image.sample(index % p.source.width, Math.floor(index / p.source.width), 0);
         need(Object.is(sample, decoded[index]), 'SUPPORT_SAMPLE_CHANGED');
         kernel.samples.push(sample);
      });
      frozen(kernel, {nodes: 0, steps: 0});
      result = DSGNativeLinearUncertainty.inspect(kernel, budget);
      budget(); compare(sourceWindow, decoded, p.source, budget);
      history(sourceWindow, 'current', 'source-after.js');
      writeJSON('result.json', result, true);
      budget(); save(sourceWindow, 'checkpoint.xisf'); budget();
      var opened = ImageWindow.open(root + '/checkpoint.xisf', '', 'no-normalize');
      need(Array.isArray(opened), 'CHECKPOINT_RETURN');
      opened.forEach(function (window) { owned.push({window: window, kind: 'checkpoint'}); });
      need(opened.length === 1, 'CHECKPOINT_COUNT');
      budget();
      history(opened[0], 'initial', 'checkpoint-initial.js');
      compare(opened[0], decoded, p.source, budget);
      history(opened[0], 'current', 'checkpoint-current.js');
      rehashInputs(budget); compare(sourceWindow, decoded, p.source, budget);
      writeJSON('native-evidence.json', {protocol: 'DSG_NATIVE_LINEAR_EVIDENCE_V1', operationRef: operation,
         sourceSha256: p.source.sha256, parametersSha256: parameterRead.sha256, kernelSpecSha256: p.kernelSpecSha256,
         lineageSha256: p.lineageSha256, dependencies: p.dependencies, pixInsightVersion: version,
         sourceFormat: 'FLOAT32_BE', orientation: 'FITS_AXIS1_FAST_NO_FLIP', sourceValueImportCompared: true,
         allSourceValuesPreserved: true, checkpointKind: 'NATIVE_MATERIALIZATION_OF_SOURCE_VALUES', checkpointReopenCompared: true,
         upstreamPixInsightHistory: 'NOT_PRESENT_IN_SOURCE_FITS', fullPhysicalVariance: null, significance: null,
         scientificValidation: 'NOT_VALIDATED', qualifiedControls: 0, provenanceVerified: false, physicalApplicabilityVerified: false}, true);
      budget(); terminalState = 'COMPLETED_CONDITIONAL_COMPUTATION';
   } catch (error) {
      errorCode = code(error);
      terminalState = errorCode === 'NATIVE_LINEAR_CANCELLED' ? 'CANCELLED_RETAINED' : 'FAILED_RETAINED';
   } finally {
      if (owned.length > 2) {
         // Do not truncate the actual count into the bounded terminal schema, or close unknown extra views.
         console.writeln('NATIVE_LINEAR_OWNERSHIP_EXCESS_UNCERTAIN count=' + owned.length);
         if (sourceHandle !== null) { try { sourceHandle.close(); } catch (ignored) {} sourceHandle = null; }
         if (logOpen) { try { console.endLog(); } catch (ignoredLog) {} logOpen = false; }
         throw Error('NATIVE_LINEAR_OWNERSHIP_EXCESS_UNCERTAIN');
      }
      while (owned.length) {
         var item = owned[owned.length - 1];
         try {
            var initialName = item.kind + '-initial.js';
            if (!products.some(function (pin) { return pin.name === initialName; })) history(item.window, 'initial', initialName);
            if (terminalState !== 'COMPLETED_CONDITIONAL_COMPUTATION') save(item.window, 'error-owned-' + owned.length + '.xisf');
            history(item.window, 'current', 'closing-' + item.kind + '.js');
            item.window.forceClose(); owned.pop();
         } catch (retention) { retentionError = code(retention); break; }
      }
      if (sourceHandle !== null) {
         try { sourceHandle.close(); sourceHandle = null; } catch (sourceClose) { retentionError = code(sourceClose); }
      }
      try { rehashInputs(function () { checkTime(true); }); } catch (changed) { retentionError = code(changed); }
      if (logOpen) {
         try { console.endLog(); logOpen = false; addProduct('native.log'); } catch (logError) { retentionError = code(logError); }
      }
      checkTime(true);
      if (overrun && terminalState === 'COMPLETED_CONDITIONAL_COMPUTATION') { terminalState = 'FAILED_RETAINED'; errorCode = 'NATIVE_LINEAR_DEADLINE'; }
      if (retentionError !== null) { terminalState = 'UNCERTAIN_RETENTION'; if (errorCode === null) errorCode = 'NATIVE_LINEAR_RETENTION_FAILURE'; }
   }
   function verifyProducts() {
      products.forEach(function (pin) {
         var observed = hashFile(pin.name, limit(pin.name), function () { checkTime(true); });
         need(observed.sha256 === pin.sha256 && observed.byteLength === pin.byteLength, 'FINAL_PRODUCT_CHANGED');
      });
   }
   try {
      verifyProducts(); rehashInputs(function () { checkTime(true); }); checkTime(true);
      if (overrun && terminalState === 'COMPLETED_CONDITIONAL_COMPUTATION') { terminalState = 'FAILED_RETAINED'; errorCode = 'NATIVE_LINEAR_DEADLINE'; }
      var terminal = {protocol: 'DSG_NATIVE_LINEAR_TERMINAL_V1', operationRef: operation, state: terminalState,
         errorCode: errorCode, retentionErrorCode: retentionError, products: products, unclosedOwnedViews: owned.length,
         cooperativeDeadlineExceeded: overrun, fullPhysicalVariance: null, significance: null, scientificValidation: 'NOT_VALIDATED',
         qualifiedControls: 0, provenanceVerified: false, physicalApplicabilityVerified: false};
      function finalChecks() {
         verifyProducts(); rehashInputs(function () { checkTime(true); }); checkTime(true);
         need(overrun === terminal.cooperativeDeadlineExceeded, 'FINAL_DEADLINE_CHANGED');
         if (terminal.state === 'COMPLETED_CONDITIONAL_COMPUTATION') { need(!overrun, 'DEADLINE'); cancellation(); }
      }
      var terminalPin = writeJSON('terminal.json', terminal, false);
      finalChecks();
      var readyPin = writeJSON('terminal-ready.json', {protocol: 'DSG_NATIVE_LINEAR_TERMINAL_READY_V1', operationRef: operation, terminalSha256: terminalPin.sha256}, false);
      finalChecks();
      [['terminal.json', terminalPin], ['terminal-ready.json', readyPin]].forEach(function (row) {
         var observed = hashFile(row[0], MIB, function () { checkTime(true); });
         need(observed.sha256 === row[1].sha256 && observed.byteLength === row[1].byteLength, 'FINAL_CONTROL_CHANGED');
      });
      checkTime(true); need(overrun === terminal.cooperativeDeadlineExceeded, 'FINAL_DEADLINE_CHANGED');
      if (terminal.state === 'COMPLETED_CONDITIONAL_COMPUTATION') cancellation();
      checkTime(true); need(overrun === terminal.cooperativeDeadlineExceeded, 'FINAL_DEADLINE_CHANGED');
      return terminal;
   } catch (publicationError) {
      try { writeJSON('native-publication-uncertain.json', {protocol: 'DSG_NATIVE_LINEAR_PUBLICATION_FENCE_V1',
         operationRef: operation, errorCode: code(publicationError), newNativeStartAllowed: false}, false); } catch (fenceError) {}
      // Stale terminal/ready stay untouched. Parent must preserve exceptional outcome even if fence IO fails.
      throw Error('NATIVE_LINEAR_FINAL_PUBLICATION_UNCERTAIN');
   }
}
