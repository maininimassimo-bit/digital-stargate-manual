import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';
const code=readFileSync(new URL('./native_float32_primary.jsh',import.meta.url),'utf8');
const context=vm.createContext({Uint8Array,SharedArrayBuffer});vm.runInContext(code,context);
const helper=context.DSGNativeFloat32Primary;
// Constructed byte patterns only. No observational file or real sample is read.
const card=(key,value)=>(key.padEnd(8)+'= '+value).padEnd(80);
function fixture(bits=[0xbf800000,0x3f000000,0x40000000,0x40400000,0x80000000,1],width=3,height=2,extra=[]) {
 const cards=[card('SIMPLE','T'),card('BITPIX','-32'),card('NAXIS','2'),card('NAXIS1',String(width)),card('NAXIS2',String(height)),...extra];
 const raw=cards.join('')+'END'.padEnd(80),header=raw.padEnd(Math.ceil(raw.length/2880)*2880);
 const dataSize=Math.ceil(bits.length*4/2880)*2880;
 const bytes=new Uint8Array(header.length+dataSize);bytes.set(new TextEncoder().encode(header));
 const view=new DataView(bytes.buffer);bits.forEach((b,i)=>view.setUint32(header.length+4*i,b,false));
 return {bytes,expected:{byteLength:bytes.length,dataOffset:header.length,width,height}};
}
function decode(f,monitor){return helper.decode(f.bytes,f.expected,monitor);}
function overwrite(f,index,text){f.bytes.set(new TextEncoder().encode(text),index*80);}
test('independent IEEE bit-pattern oracle retains finite values and rejects nonfinite patterns',()=>{
 const cases=[[0,0],[0x80000000,-0],[1,2**-149],[0x007fffff,(2**23-1)*2**-149],
  [0x00800000,2**-126],[0x3f800000,1],[0xbf800000,-1],[0x40000000,2],[0x7f7fffff,(2-2**-23)*2**127]];
 for(const [bits,value] of cases){const r=decode(fixture([bits],1,1));assert(Object.is(r.values[0],value));
  assert.equal(r.layout.fileIntegrityVerified,false);assert.equal(r.layout.physicalApplicabilityVerified,false);}
 for(const bits of [0x7f800000,0xff800000,0x7fc00000])assert.throws(()=>decode(fixture([bits],1,1)),/NONFINITE_SOURCE/);
});
test('axis1-fast ordering and signed samples are never normalized or flipped',()=>{
 const f=fixture(),r=decode(f);assert.deepEqual([...r.values],[-1,.5,2,3,-0,2**-149]);
 assert.equal(r.layout.orientation,'FITS_AXIS1_FAST_NO_FLIP');assert.equal(r.layout.channels,1);
 assert.equal(r.layout.dataOffset,2880);assert.equal(r.layout.sampleCount,6);
});
test('nonzero backing-buffer offset uses exactly the supplied source view',()=>{
 const f=fixture(),backing=new Uint8Array(f.bytes.length+16);backing.fill(255);backing.set(f.bytes,8);
 f.bytes=backing.subarray(8,8+f.expected.byteLength);assert.deepEqual([...decode(f).values],[-1,.5,2,3,-0,2**-149]);
});
test('multiple header blocks and uninterpreted history preserve the declared offset',()=>{
 const f=fixture(undefined,3,2,Array.from({length:40},(_,i)=>('HISTORY synthetic '+i).padEnd(80)));
 assert.equal(f.expected.dataOffset,5760);assert.equal(decode(f).layout.dataOffset,5760);
});
test('only exact decimal identity scale and zero offset are accepted',()=>{
 for(const scale of ['1','+1.0','0.1E1','10D-1','0001.00000']){
  const f=fixture(undefined,3,2,[card('BSCALE',scale),card('BZERO','0.00D999')]);
  assert.equal(decode(f).values[0],-1);assert.equal(decode(f).layout.bscale,1);
 }
 for(const [key,value] of [['BSCALE','2'],['BSCALE','1.000000000000000001'],['BSCALE','1E999'],
  ['BSCALE','-1'],['BZERO','1'],['BZERO','1E-999'],['BZERO','-0.0']])
  assert.throws(()=>decode(fixture(undefined,3,2,[card(key,value)])),/UNSUPPORTED_SCALE|UNSUPPORTED_ZERO|IDENTITY_VALUE/);
});
test('mandatory order, type, dimensionality and geometry are exact',()=>{
 for(const [index,key,value] of [[0,'SIMPLE','F'],[0,'BITPIX','-32'],[1,'BITPIX','-64'],[2,'NAXIS','3'],
  [3,'NAXIS1','2'],[4,'NAXIS2','3'],[1,'BITPIX','-32junk'],[0,'SIMPLE',"'T'"]]){
  const f=fixture();overwrite(f,index,card(key,value));assert.throws(()=>decode(f),/PRIMARY_FLOAT32_/);
 }
 const bad=fixture();overwrite(bad,0,'simple  = T'.padEnd(80));assert.throws(()=>decode(bad),/KEYWORD/);
});
test('duplicate meaningful cards and unsupported primary formats fail closed',()=>{
 for(const extra of [[card('NAXIS1','3')],[card('BSCALE','1'),card('BSCALE','1')],[card('BZERO','0'),card('BZERO','0')],
  [card('NAXIS3','1')],[card('GROUPS','F')],[card('GCOUNT','1')],[card('PCOUNT','0')],[card('BLANK','0')],
  [card('XTENSION',"'IMAGE'")],[card('ZIMAGE','F')]])assert.throws(()=>decode(fixture(undefined,3,2,extra)),/DUPLICATE_KEYWORD|UNSUPPORTED_/);
});
test('header ASCII, END card, padding and declared offset are checked before decode',()=>{
 const ascii=fixture();ascii.bytes[600]=10;assert.throws(()=>decode(ascii),/HEADER_PADDING/);
 const high=fixture(undefined,3,2,['HISTORY'.padEnd(80)]);high.bytes[450]=255;assert.throws(()=>decode(high),/HEADER_ASCII/);
 const end=fixture();overwrite(end,5,'END     = T'.padEnd(80));assert.throws(()=>decode(end),/END_CARD/);
 const duplicateEnd=fixture();overwrite(duplicateEnd,6,'END'.padEnd(80));assert.throws(()=>decode(duplicateEnd),/HEADER_PADDING/);
 const wrong=fixture();wrong.expected.dataOffset=5760;assert.throws(()=>decode(wrong),/HEADER_OFFSET/);
 const missing=fixture();overwrite(missing,5,' '.repeat(80));assert.throws(()=>decode(missing),/PRIMARY_FLOAT32_/);
});
test('size, geometry, expected schema and active inputs fail before allocation',()=>{
 const hostile=vm.createContext({Uint8Array,SharedArrayBuffer,Float64Array:class{constructor(){throw Error('ALLOCATED');}}});
 vm.runInContext(code,hostile);const reject=f=>assert.throws(()=>hostile.DSGNativeFloat32Primary.decode(f.bytes,f.expected),/PRIMARY_FLOAT32_/);
 for(const change of [f=>f.expected.width=4194305,f=>f.expected.height=0,f=>f.expected.width=NaN,
  f=>f.expected.byteLength=67108865,f=>f.expected.byteLength--,f=>f.expected.dataOffset=1,
  f=>f.expected.other=0,f=>f.expected.width=2.5]){const f=fixture();change(f);reject(f);}
 const truncated=fixture([0],4194304,1);reject(truncated); // Header matches, padded primary data does not.
 const active=fixture();Object.defineProperty(active.expected,'width',{enumerable:true,get(){throw Error('EXECUTED');}});
 assert.throws(()=>decode(active),/EXPECTED_ACCESSOR/);
 const raw=fixture();Object.defineProperty(raw.bytes,'buffer',{get(){throw Error('EXECUTED');}});
 assert.throws(()=>decode(raw),/BYTE_ACTIVE_PROPERTY/);
 assert.throws(()=>helper.decode({},fixture().expected),/BYTE_INPUT/);
});
test('expected geometry is privately snapshotted before calling the trusted monitor',()=>{
 const f=fixture();let calls=0;const r=decode(f,()=>{calls++;f.expected.width=999999999;});
 assert.equal(r.layout.width,3);assert.equal(r.values.length,6);assert(calls>=3);
});
test('cooperative monitor interrupts header scan and long data decode without a returned array',()=>{
 const header=fixture(undefined,3,2,Array(60).fill('HISTORY synthetic'.padEnd(80)));
 let h=0;assert.throws(()=>decode(header,()=>{if(++h===2)throw Error('HEADER_CANCEL');}),/HEADER_CANCEL/);
 const long=fixture(Array(8192).fill(0x3f800000),8192,1);
 let d=0;assert.throws(()=>decode(long,()=>{if(++d===3)throw Error('DATA_CANCEL');}),/DATA_CANCEL/);
 assert.equal(d,3);assert.throws(()=>decode(fixture(),{}),/MONITOR/);
});
test('input bytes are preserved and a caller-authored layout cannot replace expected schema',()=>{
 const f=fixture(),before=[...f.bytes],layout=helper.inspect(f.bytes,f.expected);layout.width=1;
 assert.deepEqual([...decode(f).values],[-1,.5,2,3,-0,2**-149]);assert.deepEqual([...f.bytes],before);
 assert.throws(()=>helper.decode(f.bytes,layout),/EXPECTED_FIELDS/);
});
