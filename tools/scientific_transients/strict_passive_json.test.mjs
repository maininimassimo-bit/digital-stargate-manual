import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';
const context=vm.createContext({Uint8Array,SharedArrayBuffer});
vm.runInContext(readFileSync(new URL('./strict_passive_json.jsh',import.meta.url),'utf8'),context);
const parse=context.parseStrictPassiveAsciiJson;
const bytes=s=>new TextEncoder().encode(s);
const read=(s,limits)=>parse(bytes(s),limits);
const medium={maxBytes:8388608,checkBudget:null};
test('valid passive nested data, ASCII escapes and signed zero',()=>{
 const r=read(String.raw`{"a":[1,-0,2.5e-2,true,false,null],"text":"a\"\\\/\b\f\n\r\t\u0041"}`);
 assert.equal(Object.getPrototypeOf(r),null);assert.equal(Object.is(r.a[1],-0),true);
 assert.deepEqual([...r.a],[1,-0,.025,true,false,null]);assert.equal(r.text,'a"\\/\b\f\n\r\tA');
 const n=read('{"nested":{"toString":2}}');assert.equal(Object.getPrototypeOf(n.nested),null);
 assert.equal(n.nested.toString,2);
});
test('duplicate decoded keys and prototype names fail at every depth',()=>{
 for(const text of ['{"a":1,"a":2}',String.raw`{"a":1,"\u0061":2}`,
  '{"outer":{"a":1,"a":null}}','{"__proto__":1}','{"constructor":0}','{"x":{"prototype":[]}}',
  String.raw`{"\u005f_proto__":0}`,String.raw`{"\u0063onstructor":0}`]){
  assert.throws(()=>read(text),/DUPLICATE_KEY|PROTOTYPE_KEY/);
 }
 assert.equal({}.polluted,undefined);
});
test('malformed JSON has no fallback, eval or trailing acceptance',()=>{
 for(const text of ['', ' ', 'undefined', 'NaN', 'Infinity', '+1','.1','01','-01','1.','1e','1e+',
  '--1','[1,]','[,1]','{"a":1,}','{a:1}','{"a" 1}','{"a":}','{}{}','null true','truex','/*x*/0',
  '"unterminated','"\\x41"','"\\u00xz"','"a\n"','[','{','[true false]','"\\"']){
  assert.throws(()=>read(text),/PASSIVE_JSON_/);
 }
});
test('non-ASCII, BOM, malformed UTF8 and Unicode escapes are unsupported explicitly',()=>{
 for(const b of [new Uint8Array([0xef,0xbb,0xbf,48]),new Uint8Array([34,0xc3,34]),
  new Uint8Array([34,0xc0,0xaf,34]),bytes('"é"'),bytes('0\u00a0')])assert.throws(()=>parse(b),/ASCII_ENCODING/);
 for(const text of [String.raw`"\u0080"`,String.raw`"\ud800"`,String.raw`"\ud83d\ude00"`])
  assert.throws(()=>read(text),/ASCII_ESCAPE/);
});
test('finite Float64 parsing never silently underflows a nonzero decimal to zero',()=>{
 for(const text of ['1e309','-1e999','1e-999','-0.00001e-999'])assert.throws(()=>read(text),/NUMBER_NONFINITE|NUMBER_UNDERFLOW/);
 assert.equal(read('5e-324'),Number.MIN_VALUE);assert.equal(read('0e-999'),0);
 assert.equal(Object.is(read('-0.0e99'),-0),true);
 assert.equal(read('9007199254740992'),2**53); // Generic coefficient; index safety is a later schema guard.
});
test('byte bounds are checked before parser budget or materialization',()=>{
 assert.throws(()=>parse(new Uint8Array(1048577)),/BYTE_BOUND/);
 assert.throws(()=>parse(new Uint8Array(67108865),{maxBytes:67108864,checkBudget:()=>{throw Error('CALLED');}}),/BYTE_BOUND/);
 const exact=' '.repeat(1048575)+'0';assert.equal(read(exact),0);
 assert.throws(()=>parse([]),/BYTE_INPUT/);assert.throws(()=>parse(bytes('{}'),{maxBytes:1,checkBudget:null}),/LIMIT_VALUE/);
 assert.throws(()=>parse(bytes('{}'),{maxBytes:1048576,checkBudget:null,other:1}),/LIMIT_FIELDS/);
});
test('active buffer substitutions, shared bytes and accessor limits do not execute',()=>{
 const b=bytes('0');Object.defineProperty(b,'length',{get(){throw Error('EXECUTED');}});
 assert.throws(()=>parse(b),/BYTE_ACTIVE_PROPERTY/);
 const l={checkBudget:null};Object.defineProperty(l,'maxBytes',{enumerable:true,get(){throw Error('EXECUTED');}});
 assert.throws(()=>parse(bytes('0'),l),/LIMIT_ACCESSOR/);
 const shared=new Uint8Array(new SharedArrayBuffer(1));shared[0]=48;assert.throws(()=>parse(shared),/SHARED_INPUT/);
 class Custom extends Uint8Array{} assert.throws(()=>parse(new Custom([48])),/BYTE_PROTOTYPE/);
});
test('array, object, nesting and string exact boundaries',()=>{
 assert.equal(read('['+Array(16384).fill('0').join(',')+']').length,16384);
 assert.throws(()=>read('['+Array(16385).fill('0').join(',')+']'),/ARRAY_BOUND/);
 const obj=n=>'{'+Array.from({length:n},(_,i)=>`"k${i}":0`).join(',')+'}';
 assert.equal(Object.keys(read(obj(32))).length,32);assert.throws(()=>read(obj(33)),/MEMBER_BOUND/);
 assert.equal(read('"'+'x'.repeat(192)+'"').length,192);assert.throws(()=>read('"'+'x'.repeat(193)+'"'),/STRING_CHAR_BOUND/);
 assert.doesNotThrow(()=>read('['.repeat(12)+'0'+']'.repeat(12)));
 assert.throws(()=>read('['.repeat(13)+'0'+']'.repeat(13)),/DEPTH_BOUND/);
});
test('empty containers cannot bypass aggregate allocation counters',()=>{
 const group='['+Array(16384).fill('{}').join(',')+']';
 assert.throws(()=>read('['+Array(4).fill(group).join(',')+']'),/CONTAINER_COUNT_BOUND/);
});
test('aggregate string count and decoded character count are independent bounds',()=>{
 const group='['+Array(16384).fill('""').join(',')+']';
 assert.doesNotThrow(()=>read('['+Array(8).fill(group).join(',')+']'));
 assert.throws(()=>read('['+Array(9).fill(group).join(',')+']'),/STRING_COUNT_BOUND/);
 const long='['+Array(11000).fill('"'+'x'.repeat(192)+'"').join(',')+']';
 assert.throws(()=>read('['+long+','+long+']',medium),/STRING_CHAR_BOUND/);
});
test('aggregate numeric count rejects before extending beyond the model budget',()=>{
 const group='['+Array(16384).fill('0').join(',')+']';
 assert.throws(()=>read('['+Array(141).fill(group).join(',')+']',medium),/NUMBER_COUNT_BOUND/);
});
test('long numeric tokens use bounded chunks and preserve Number semantics',()=>{
 assert.equal(read('1'+'0'.repeat(10000)+'e-10000'),1);
 assert.equal(read('0.'+'0'.repeat(10000)+'1e10001'),1);
});
test('cooperative monitor fires in long whitespace, strings and number conversion',()=>{
 for(const text of [' '.repeat(9000)+'0','['+Array(5000).fill('"a"').join(',')+']',
  '1'+'0'.repeat(10000)+'e-10000']){
  let calls=0;assert.throws(()=>read(text,{maxBytes:1048576,checkBudget:()=>{if(++calls===2)throw Error('CANCELLED');}}),/CANCELLED/);
  assert.equal(calls,2);
 }
 let calls=0;assert.equal(read('123',{maxBytes:1048576,checkBudget:()=>{calls++;}}),123);assert.equal(calls,2);
});
test('input bytes stay unchanged and no caller-authored object becomes parsed data',()=>{
 const b=bytes('{"a":1}'),before=[...b];const r=parse(b);r.a=2;assert.deepEqual([...b],before);
 assert.throws(()=>parse({a:1}),/BYTE_INPUT/);
});
