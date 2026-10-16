// Bounded ASCII subset of UTF-8 JSON. Definition only; no file or native APIs.
// limits is trusted local code: {maxBytes: 1/8/64 MiB, checkBudget: null/function}.
function parseStrictPassiveAsciiJson(bytes, limits) {
   function need(ok, code) { if (!ok) throw Error('PASSIVE_JSON_' + code); }
   need(bytes instanceof Uint8Array, 'BYTE_INPUT');
   need(Object.getPrototypeOf(bytes) === Uint8Array.prototype, 'BYTE_PROTOTYPE');
   ['length', 'byteLength', 'byteOffset', 'buffer', 'subarray', 'constructor'].forEach(function (key) {
      need(!Object.prototype.hasOwnProperty.call(bytes, key), 'BYTE_ACTIVE_PROPERTY');
   });
   if (typeof SharedArrayBuffer !== 'undefined') need(!(bytes.buffer instanceof SharedArrayBuffer), 'SHARED_INPUT');
   if (limits === undefined) limits = {maxBytes: 1048576, checkBudget: null};
   need(limits && typeof limits === 'object' && !Array.isArray(limits) &&
      Object.keys(limits).sort().join(',') === 'checkBudget,maxBytes', 'LIMIT_FIELDS');
   var byteLimit = Object.getOwnPropertyDescriptor(limits, 'maxBytes');
   var monitor = Object.getOwnPropertyDescriptor(limits, 'checkBudget');
   need(byteLimit && Object.prototype.hasOwnProperty.call(byteLimit, 'value') &&
      monitor && Object.prototype.hasOwnProperty.call(monitor, 'value'), 'LIMIT_ACCESSOR');
   need([1048576, 8388608, 67108864].indexOf(byteLimit.value) >= 0 &&
      (monitor.value === null || typeof monitor.value === 'function'), 'LIMIT_VALUE');
   need(bytes.length > 0 && bytes.length <= byteLimit.value, 'BYTE_BOUND');
   var budget = monitor.value, pos = 0, nextCheck = 4096;
   var containers = 0, strings = 0, chars = 0, members = 0, numbers = 0;
   if (budget) budget();
   function tick() {
      if (pos >= nextCheck) { if (budget) budget(); nextCheck = pos + 4096; }
   }
   function peek() {
      tick();
      if (pos >= bytes.length) return -1;
      need(bytes[pos] < 128, 'ASCII_ENCODING');
      return bytes[pos];
   }
   function whitespace() {
      var c = peek();
      while (c === 32 || c === 9 || c === 10 || c === 13) { ++pos; c = peek(); }
   }
   function string() {
      need(peek() === 34, 'STRING');
      need(++strings <= 131072, 'STRING_COUNT_BOUND');
      ++pos;
      var out = '';
      while (true) {
         var c = peek();
         need(c >= 32, 'STRING_CONTROL_OR_EOF');
         ++pos;
         if (c === 34) return out;
         if (c === 92) {
            c = peek(); ++pos;
            if (c === 34 || c === 92 || c === 47) { /* literal escaped character */ }
            else if (c === 98) c = 8;
            else if (c === 102) c = 12;
            else if (c === 110) c = 10;
            else if (c === 114) c = 13;
            else if (c === 116) c = 9;
            else if (c === 117) {
               c = 0;
               for (var i = 0; i < 4; ++i) {
                  var h = peek(); ++pos;
                  need(h >= 48 && h <= 57 || h >= 65 && h <= 70 || h >= 97 && h <= 102, 'HEX_ESCAPE');
                  c = 16 * c + (h <= 57 ? h - 48 : h <= 70 ? h - 55 : h - 87);
               }
               need(c < 128, 'ASCII_ESCAPE');
            } else need(false, 'ESCAPE');
         }
         need(out.length < 192 && ++chars <= 4194304, 'STRING_CHAR_BOUND');
         out += String.fromCharCode(c);
      }
   }
   function digit(c) { return c >= 48 && c <= 57; }
   function number() {
      need(++numbers <= 2300000, 'NUMBER_COUNT_BOUND');
      var start = pos, nonzero = false;
      if (peek() === 45) ++pos;
      var c = peek();
      if (c === 48) ++pos;
      else {
         need(c >= 49 && c <= 57, 'NUMBER_GRAMMAR');
         do { if (c !== 48) nonzero = true; ++pos; c = peek(); } while (digit(c));
      }
      if (peek() === 46) {
         ++pos; need(digit(peek()), 'NUMBER_FRACTION');
         do { if (peek() !== 48) nonzero = true; ++pos; } while (digit(peek()));
      }
      c = peek();
      if (c === 69 || c === 101) {
         ++pos; c = peek(); if (c === 43 || c === 45) ++pos;
         need(digit(peek()), 'NUMBER_EXPONENT');
         do { ++pos; } while (digit(peek()));
      }
      // Bounded chunks avoid a huge argument list or a per-byte JS array.
      var parts = [];
      for (var begin = start; begin < pos; begin += 4096) {
         if (budget && pos - start >= 4096) budget();
         parts.push(String.fromCharCode.apply(null, bytes.subarray(begin, Math.min(pos, begin + 4096))));
      }
      var result = Number(parts.join(''));
      need(typeof result === 'number' && isFinite(result), 'NUMBER_NONFINITE');
      need(result !== 0 || !nonzero, 'NUMBER_UNDERFLOW');
      return result;
   }
   function container(depth) {
      need(depth <= 12, 'DEPTH_BOUND');
      need(++containers <= 65536, 'CONTAINER_COUNT_BOUND');
   }
   function value(depth) {
      whitespace();
      var c = peek();
      if (c === 34) return string();
      if (c === 45 || digit(c)) return number();
      if (c === 91) {
         container(depth); ++pos;
         var list = []; whitespace();
         if (peek() === 93) { ++pos; return list; }
         while (true) {
            need(list.length < 16384, 'ARRAY_BOUND');
            list.push(value(depth + 1)); whitespace();
            c = peek(); ++pos;
            if (c === 93) return list;
            need(c === 44, 'ARRAY_SEPARATOR');
         }
      }
      if (c === 123) {
         container(depth); ++pos;
         var object = Object.create(null), count = 0;
         whitespace();
         if (peek() === 125) { ++pos; return object; }
         while (true) {
            whitespace(); var key = string();
            need(key !== '__proto__' && key !== 'prototype' && key !== 'constructor', 'PROTOTYPE_KEY');
            need(!Object.prototype.hasOwnProperty.call(object, key), 'DUPLICATE_KEY');
            need(++count <= 32 && ++members <= 262144, 'MEMBER_BOUND');
            whitespace(); need(peek() === 58, 'COLON'); ++pos;
            object[key] = value(depth + 1); whitespace();
            c = peek(); ++pos;
            if (c === 125) return object;
            need(c === 44, 'OBJECT_SEPARATOR');
         }
      }
      var text = c === 116 ? 'true' : c === 102 ? 'false' : c === 110 ? 'null' : '';
      need(text !== '', 'VALUE');
      for (var i = 0; i < text.length; ++i) { need(peek() === text.charCodeAt(i), 'LITERAL'); ++pos; }
      return text === 'true' ? true : text === 'false' ? false : null;
   }
   var result = value(1);
   whitespace(); need(pos === bytes.length, 'TRAILING_TOKEN');
   if (budget) budget();
   return result;
}
