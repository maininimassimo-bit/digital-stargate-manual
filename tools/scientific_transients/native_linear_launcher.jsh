// Definition only. Included from the reviewed parent entry, outside the sealed work inputs.
// Actual PJSR compatibility remains unproven. No process creation, parent grant or science acceptance.
function DSGNativeLinearLaunch(root, expected) {
   function need(ok, code) { if (!ok) throw Error('NATIVE_LAUNCH_' + code); }
   function fields(value, keys) { need(value && typeof value === 'object' && !Array.isArray(value) &&
      Object.keys(value).sort().join(',') === keys.slice().sort().join(','), 'FIELDS'); }
   function hex(value, length) { return typeof value === 'string' && value.length === length && /^[a-f0-9]+$/.test(value); }
   need(typeof root === 'string' && /^[A-Za-z]:\x2f/.test(root) && root.length <= 512 &&
      !/[\x00-\x1f\x7f-\uffff\\"'<>|:*?\[\]]/.test(root.slice(2)) && !/\x2f$/.test(root), 'ROOT');
   root.slice(3).split('/').forEach(function (p) { need(p.length > 0 && p !== '.' && p !== '..' && !/[. ]$/.test(p), 'ROOT_COMPONENT'); });
   fields(expected, ['operationRef', 'ownerNonce', 'processSessionRef', 'sealSha256', 'grantSha256', 'wrapperSha256', 'parentDeadlineUTC']);
   ['operationRef', 'ownerNonce', 'processSessionRef'].forEach(function (key) { need(hex(expected[key], 32), 'EXPECTED'); });
   ['sealSha256', 'grantSha256', 'wrapperSha256'].forEach(function (key) { need(hex(expected[key], 64), 'EXPECTED'); });
   need(root.slice(root.lastIndexOf('/') + 1) === expected.operationRef, 'OPERATION_DIRECTORY');
   need(typeof expected.parentDeadlineUTC === 'string' && /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/.test(expected.parentDeadlineUTC), 'DEADLINE');
   var deadline = Date.parse(expected.parentDeadlineUTC), start = Date.now(), lastWall = start, lastMono = 0, timer = new ElapsedTime;
   need(isFinite(deadline) && new Date(deadline).toISOString().replace('.000Z', 'Z') === expected.parentDeadlineUTC, 'DEADLINE');
   var remaining = Math.min(180, (deadline - start) / 1000), clockInvalid = false;
   var MIB = 1048576, ownership = null, seal = null;
   function clock(retaining) {
      var now = Date.now(), elapsed = timer.value;
      if (!(typeof elapsed === 'number' && isFinite(elapsed) && elapsed >= lastMono && now >= lastWall)) clockInvalid = true;
      lastWall = now; lastMono = elapsed;
      var within = !clockInvalid && elapsed < remaining && now < deadline;
      if (!retaining) need(within, clockInvalid ? 'CLOCK_CHANGED' : 'DEADLINE');
      return within;
   }
   function read(name, parse, retaining) {
      clock(retaining);
      var file = new File;
      try {
         file.openForReading(root + '/' + name);
         var size = file.size;
         need(typeof size === 'number' && Math.floor(size) === size && size > 0 && size <= MIB, 'READ_SIZE');
         var raw = file.read(15, size);
         need(raw.length === size && file.size === size, 'READ_CHANGED');
         var value = parse ? parseStrictPassiveAsciiJson(raw.toUint8Array(), {maxBytes: MIB, checkBudget: function () { clock(retaining); }}) : null;
         // Explicit SHA-256 algorithm code from installed pjsr/CryptographicHash.jsh.
         var pin = {value: value, sha256: new CryptographicHash(256).hash(raw).toHex(), byteLength: size};
         clock(retaining); return pin;
      } finally { file.close(); }
   }
   function fences() { need(!File.exists(root + '/native-publication-uncertain.json'), 'UNCERTAINTY'); }
   function guard() {
      clock(false); fences();
      if (File.exists(root + '/cancel.json')) {
         var c = read('cancel.json', true, false).value;
         fields(c, ['protocol', 'operationRef', 'requested']);
         need(c.protocol === 'DSG_NATIVE_LINEAR_CANCEL_V1' && c.operationRef === expected.operationRef && c.requested === true, 'CANCEL_SCHEMA');
         throw Error('NATIVE_LAUNCH_CANCELLED');
      }
   }
   function inputs(retaining) {
      need(read('launch-seal.json', false, retaining).sha256 === expected.sealSha256 &&
         read('launch-grant.json', false, retaining).sha256 === expected.grantSha256 &&
         read('native_linear_measurement.jsh', false, retaining).sha256 === expected.wrapperSha256, 'SOURCE_PINS');
      if (ownership !== null) need(read('native-owner.json', false, retaining).sha256 === ownership.ownerSha256 &&
         read('native-owner-ready.json', false, retaining).sha256 === ownership.ownerReadySha256, 'OWNER_PINS');
   }
   var runtimeNames = ['started-native.json', 'native.log', 'result.json', 'native-evidence.json', 'checkpoint.xisf',
      'source-initial.js', 'source-before.js', 'source-after.js', 'checkpoint-initial.js', 'checkpoint-current.js',
      'closing-source.js', 'closing-checkpoint.js', 'error-owned-1.xisf', 'error-owned-2.xisf', 'terminal.json',
      'terminal-ready.json', 'native-publication-uncertain.json', 'native-return.json'];
   function runtimeBound(additional) {
      var inputs = seal.files.map(function (p) { return p.name; }).concat(['launch-seal.json', 'launch-grant.json',
         'native-owner.json', 'native-owner-ready.json', 'cancel.json']);
      var finder = new FileFind, active = finder.begin(root + '/*'), total = additional, count = additional > 0 ? 1 : 0, found = [];
      try {
         while (active) {
            var name = finder.name;
            if (name !== '.' && name !== '..') {
               need(finder.isFile === true && finder.isDirectory === false && finder.isSymbolicLink === false &&
                  finder.isRedirectionPoint === false && finder.isReparsePoint === false && found.indexOf(name) < 0, 'INVENTORY');
               found.push(name); need(found.length <= 97 && (inputs.indexOf(name) >= 0 || runtimeNames.indexOf(name) >= 0), 'INVENTORY');
               if (runtimeNames.indexOf(name) >= 0) {
                  var file = new File;
                  try {
                     file.openForReading(root + '/' + name); var size = file.size;
                     need(typeof size === 'number' && Math.floor(size) === size && size >= 0 && size <= 192 * MIB, 'RUNTIME_SIZE');
                     total += size; ++count;
                  } finally { file.close(); }
               }
               need(count <= 20 && total <= 192 * MIB, 'RUNTIME_AGGREGATE'); clock(true);
            }
            active = finder.next();
         }
      } finally { finder.end(); }
   }
   function terminalSchema(t) {
      fields(t, ['protocol', 'operationRef', 'state', 'errorCode', 'retentionErrorCode', 'products', 'unclosedOwnedViews',
         'cooperativeDeadlineExceeded', 'fullPhysicalVariance', 'significance', 'scientificValidation', 'qualifiedControls',
         'provenanceVerified', 'physicalApplicabilityVerified']);
      need(t.protocol === 'DSG_NATIVE_LINEAR_TERMINAL_V1' && t.operationRef === expected.operationRef &&
         ['COMPLETED_CONDITIONAL_COMPUTATION', 'FAILED_RETAINED', 'CANCELLED_RETAINED', 'UNCERTAIN_RETENTION'].indexOf(t.state) >= 0 &&
         typeof t.unclosedOwnedViews === 'number' && Math.floor(t.unclosedOwnedViews) === t.unclosedOwnedViews &&
         t.unclosedOwnedViews >= 0 && t.unclosedOwnedViews <= 2 && typeof t.cooperativeDeadlineExceeded === 'boolean' &&
         t.fullPhysicalVariance === null && t.significance === null && t.scientificValidation === 'NOT_VALIDATED' &&
         t.qualifiedControls === 0 && t.provenanceVerified === false && t.physicalApplicabilityVerified === false &&
         Array.isArray(t.products) && t.products.length <= 18, 'TERMINAL');
      ['errorCode', 'retentionErrorCode'].forEach(function (key) {
         need(t[key] === null || typeof t[key] === 'string' && /^[A-Z0-9_]{1,96}$/.test(t[key]), 'TERMINAL_ERROR');
      });
      var seen = [];
      t.products.forEach(function (p) {
         fields(p, ['role', 'name', 'sha256', 'byteLength']);
         need(typeof p.name === 'string' && runtimeNames.slice(0, 14).indexOf(p.name) >= 0 && p.role === p.name &&
            seen.indexOf(p.name) < 0 && hex(p.sha256, 64) && typeof p.byteLength === 'number' &&
            Math.floor(p.byteLength) === p.byteLength && p.byteLength >= 0 && p.byteLength <= 192 * MIB, 'TERMINAL_PRODUCT');
         seen.push(p.name);
      });
   }
   try {
      need(!File.exists(root + '/native-return.json'), 'RETURN_COLLISION'); guard();
      inputs(false); seal = read('launch-seal.json', true, false).value;
      need(seal && Array.isArray(seal.files) && seal.files.length <= 72 &&
         seal.files.filter(function (p) { return p.name === 'native_linear_measurement.jsh' && p.sha256 === expected.wrapperSha256; }).length === 1, 'SEALED_WRAPPER');
      while (!File.exists(root + '/native-owner-ready.json')) { guard(); System.msleep(10); }
      guard();
      ownership = DSGNativeLinearOwnership(root, {operationRef: expected.operationRef, ownerNonce: expected.ownerNonce,
         processSessionRef: expected.processSessionRef, sealSha256: expected.sealSha256, grantSha256: expected.grantSha256}, guard);
      need(ownership.owner.parentDeadlineUTC === expected.parentDeadlineUTC, 'PARENT_DEADLINE');
      inputs(false); guard();
      // Only this actual call can establish causal return. Catch never fabricates it.
      var returned = DSGNativeLinearMeasurement(root, function (retaining) { return clock(retaining); });
      need(!clockInvalid, 'CLOCK_CHANGED');
      terminalSchema(returned);
      var terminal = read('terminal.json', true, true), ready = read('terminal-ready.json', true, true);
      need(JSON.stringify(returned) === JSON.stringify(terminal.value), 'ACTUAL_RETURN');
      fields(ready.value, ['protocol', 'operationRef', 'terminalSha256']);
      need(ready.value.protocol === 'DSG_NATIVE_LINEAR_TERMINAL_READY_V1' && ready.value.operationRef === expected.operationRef &&
         ready.value.terminalSha256 === terminal.sha256, 'READY');
      var record = {protocol: 'DSG_NATIVE_LINEAR_RETURNED_V1', operationRef: expected.operationRef, sealSha256: expected.sealSha256,
         wrapperSha256: expected.wrapperSha256, terminalSha256: terminal.sha256, readySha256: ready.sha256,
         state: returned.state, unclosedOwnedViews: returned.unclosedOwnedViews, fullPhysicalVariance: null, significance: null,
         scientificValidation: 'NOT_VALIDATED', qualifiedControls: 0, nativeProcessId: CoreApplication.pid,
         processSessionRef: expected.processSessionRef, ownerSha256: ownership.ownerSha256, ownerReadySha256: ownership.ownerReadySha256};
      var text = JSON.stringify(record);
      need(text.length <= MIB && /^[\x00-\x7f]*$/.test(text) && record.nativeProcessId === ownership.owner.nativeProcessId, 'RETURN');
      inputs(true); fences(); runtimeBound(text.length); clock(true); fences();
      need(!File.exists(root + '/native-return.json'), 'RETURN_COLLISION');
      File.writeTextFile(root + '/native-return.json', text); // Guarded single writer, not atomic create-new.
      var pin = read('native-return.json', true, true);
      need(pin.sha256 === new CryptographicHash(256).hash(text).toHex() && JSON.stringify(pin.value) === text, 'RETURN_READBACK');
      inputs(true);
      need(read('terminal.json', false, true).sha256 === terminal.sha256 && read('terminal-ready.json', false, true).sha256 === ready.sha256, 'FINAL_CONTROLS');
      runtimeBound(0); clock(true); need(!clockInvalid, 'CLOCK_CHANGED'); fences();
      return record; // Proves wrapper-return only, never launcher-finished or process exit.
   } catch (error) {
      try {
         if (!File.exists(root + '/native-publication-uncertain.json')) {
            var reason = error && typeof error.message === 'string' && /^[A-Z0-9_]{1,96}$/.test(error.message) ? error.message : 'NATIVE_LAUNCH_API_FAILURE';
            File.writeTextFile(root + '/native-publication-uncertain.json', JSON.stringify({protocol: 'DSG_NATIVE_LINEAR_PUBLICATION_FENCE_V1',
               operationRef: expected.operationRef, errorCode: reason, newNativeStartAllowed: false}));
         }
      } catch (fenceError) {}
      throw Error('NATIVE_LAUNCH_UNCERTAIN');
   }
}
