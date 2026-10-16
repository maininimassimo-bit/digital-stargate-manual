// Real source values may be decoded only inside PJSR. Node fixtures are synthetic.
// No file I/O, calibration, WCS import, scaling, mask filling or launch authority.
var DSGNativeFloat32Primary = (function () {
   function need(ok, code) { if (!ok) throw Error('PRIMARY_FLOAT32_' + code); }
   function integer(v, low, high) { return typeof v === 'number' && isFinite(v) && Math.floor(v) === v && v >= low && v <= high; }
   function checkpoint(monitor) {
      need(monitor === undefined || monitor === null || typeof monitor === 'function', 'MONITOR');
      var steps = 0;
      return function (force) { if (monitor && (force || ++steps >= 4096)) { steps = 0; monitor(); } };
   }
   function validate(bytes, expected) {
      need(bytes instanceof Uint8Array && Object.getPrototypeOf(bytes) === Uint8Array.prototype, 'BYTE_INPUT');
      ['length', 'byteLength', 'byteOffset', 'buffer', 'subarray', 'constructor'].forEach(function (key) {
         need(!Object.prototype.hasOwnProperty.call(bytes, key), 'BYTE_ACTIVE_PROPERTY');
      });
      if (typeof SharedArrayBuffer !== 'undefined') need(!(bytes.buffer instanceof SharedArrayBuffer), 'SHARED_INPUT');
      need(expected && typeof expected === 'object' && !Array.isArray(expected) &&
         Object.keys(expected).sort().join(',') === 'byteLength,dataOffset,height,width', 'EXPECTED_FIELDS');
      ['byteLength', 'dataOffset', 'height', 'width'].forEach(function (key) {
         var d = Object.getOwnPropertyDescriptor(expected, key);
         need(d && Object.prototype.hasOwnProperty.call(d, 'value'), 'EXPECTED_ACCESSOR');
      });
      need(integer(expected.byteLength, 2880, 67108864) && expected.byteLength % 2880 === 0 &&
         bytes.length === expected.byteLength, 'BYTE_BOUND');
      need(integer(expected.width, 1, 4194304) && integer(expected.height, 1, 4194304) &&
         expected.width * expected.height <= 4194304, 'GEOMETRY_BOUND');
      need(integer(expected.dataOffset, 2880, 1048320) && expected.dataOffset % 2880 === 0, 'OFFSET_BOUND');
      return {byteLength: expected.byteLength, dataOffset: expected.dataOffset, width: expected.width, height: expected.height};
   }
   function token(card) {
      need(card.charAt(8) === '=' && card.charAt(9) === ' ', 'VALUE_CARD');
      return card.substring(10).split('/')[0].replace(/^ +| +$/g, '');
   }
   function numeric(card) {
      var t = token(card);
      need(/^[+-]?[0-9]+$/.test(t), 'VALUE_NUMBER');
      var v = Number(t);
      need(isFinite(v), 'VALUE_NONFINITE');
      return v;
   }
   function identityValue(card, zero) {
      var t = token(card);
      need(/^[+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[DE][+-]?[0-9]+)?$/.test(t), 'IDENTITY_VALUE');
      var parts = t.replace('D', 'E').split('E'), mantissa = parts[0].replace(/^\+/, '');
      var digits = mantissa.replace('.', '');
      if (zero) { need(/^0+$/.test(digits), 'UNSUPPORTED_ZERO'); return 0; }
      digits = digits.replace(/^0+/, '');
      var significant = digits.replace(/0+$/, ''), trailing = digits.length - significant.length;
      var fractional = mantissa.indexOf('.') < 0 ? 0 : mantissa.length - mantissa.indexOf('.') - 1;
      var exponent = parts.length === 1 ? 0 : Number(parts[1]);
      need(integer(exponent, -192, 192) && significant === '1' && exponent + trailing - fractional === 0, 'UNSUPPORTED_SCALE');
      return 1;
   }
   function inspectInternal(bytes, expected, check) {
      expected = validate(bytes, expected); check(true);
      var required = ['SIMPLE', 'BITPIX', 'NAXIS', 'NAXIS1', 'NAXIS2'];
      var values = Object.create(null), seen = Object.create(null), offset = null;
      for (var at = 0; at + 80 <= Math.min(bytes.length, 1048320); at += 80) {
         for (var j = 0; j < 80; ++j) { need(bytes[at + j] >= 32 && bytes[at + j] <= 126, 'HEADER_ASCII'); check(); }
         var card = String.fromCharCode.apply(null, bytes.subarray(at, at + 80));
         var key = card.substring(0, 8).replace(/ +$/, '');
         need(key === '' || /^[A-Z0-9_-]{1,8}$/.test(key), 'KEYWORD');
         if (at < 400) need(key === required[at / 80], 'REQUIRED_ORDER');
         if (key === 'END') {
            need(/^END +$/.test(card), 'END_CARD');
            offset = Math.ceil((at + 80) / 2880) * 2880;
            need(offset <= bytes.length && offset <= 1048320, 'HEADER_BOUND');
            for (j = at + 80; j < offset; ++j) { need(bytes[j] === 32, 'HEADER_PADDING'); check(); }
            break;
         }
         need(['GROUPS', 'PCOUNT', 'GCOUNT', 'BLANK', 'XTENSION', 'ZIMAGE', 'ZCMPTYPE', 'ZBITPIX', 'ZNAXIS'].indexOf(key) < 0, 'UNSUPPORTED_HEADER');
         if (key.indexOf('NAXIS') === 0) need(['NAXIS', 'NAXIS1', 'NAXIS2'].indexOf(key) >= 0, 'UNSUPPORTED_AXIS');
         if (required.indexOf(key) >= 0 || key === 'BSCALE' || key === 'BZERO') {
            need(!seen[key], 'DUPLICATE_KEYWORD'); seen[key] = true;
            values[key] = key === 'SIMPLE' ? token(card) : key === 'BSCALE' ? identityValue(card, false) :
               key === 'BZERO' ? identityValue(card, true) : numeric(card);
         }
      }
      need(offset !== null && offset === expected.dataOffset, 'HEADER_OFFSET');
      need(values.SIMPLE === 'T' && values.BITPIX === -32 && values.NAXIS === 2 &&
         values.NAXIS1 === expected.width && values.NAXIS2 === expected.height, 'FORMAT_OR_GEOMETRY');
      need(!seen.BSCALE || values.BSCALE === 1, 'UNSUPPORTED_SCALE');
      need(!seen.BZERO || values.BZERO === 0 && 1 / values.BZERO === Infinity, 'UNSUPPORTED_ZERO');
      var count = expected.width * expected.height, dataBytes = count * 4;
      need(offset + Math.ceil(dataBytes / 2880) * 2880 <= bytes.length, 'DATA_TRUNCATED');
      check(true);
      return {protocol: 'DSG_NATIVE_FLOAT32_PRIMARY_LAYOUT_V1', width: expected.width, height: expected.height,
         channels: 1, bitpix: -32, sampleFormat: 'FLOAT32_BE', orientation: 'FITS_AXIS1_FAST_NO_FLIP',
         dataOffset: offset, dataBytes: dataBytes, sampleCount: count, bscale: 1, bzero: 0,
         fileIntegrityVerified: false, physicalApplicabilityVerified: false};
   }
   function inspect(bytes, expected, monitor) { return inspectInternal(bytes, expected, checkpoint(monitor)); }
   function decode(bytes, expected, monitor) {
      var check = checkpoint(monitor), layout = inspectInternal(bytes, expected, check);
      var view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
      var values = new Float64Array(layout.sampleCount);
      for (var i = 0; i < values.length; ++i) {
         var value = view.getFloat32(layout.dataOffset + 4 * i, false);
         need(isFinite(value), 'NONFINITE_SOURCE'); values[i] = value; check();
      }
      check(true);
      return {layout: layout, values: values};
   }
   return {inspect: inspect, decode: decode};
}());
