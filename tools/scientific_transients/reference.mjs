import {createHash} from 'node:crypto';

const fail = () => { throw new Error('INVALID_PUBLIC_REFERENCE_SAMPLE'); };
const numeric = value => {
  if (typeof value !== 'string' || !/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(value)) fail();
  const result = Number(value); if (!Number.isFinite(result)) fail(); return result;
};
function csv(text) {
  if (typeof text !== 'string' || Buffer.byteLength(text, 'utf8') > 65536) fail();
  const rows = []; let row = [], field = '', quoted = false, closed = false;
  const endField = () => { row.push(field); field = ''; closed = false; };
  const endRow = () => { endField(); rows.push(row); row = []; if (rows.length > 101) fail(); };
  for (let index = 0; index < text.length; index++) {
    const c = text[index];
    if (quoted) {
      if (c === '"' && text[index+1] === '"') { field += '"'; index++; }
      else if (c === '"') { quoted = false; closed = true; }
      else field += c;
    } else if (c === ',' ) endField();
    else if (c === '\r' || c === '\n') {
      if (c === '\r' && text[index+1] === '\n') index++;
      endRow();
    } else if (c === '"') {
      if (field || closed) fail(); quoted = true;
    } else { if (closed) fail(); field += c; }
  }
  if (quoted) fail();
  if (field || row.length || closed) endRow();
  if (rows.length < 2 || new Set(rows[0]).size !== rows[0].length || rows[0].some(h => !h)) fail();
  const headers = rows.shift();
  return rows.map(values => {
    if (values.length !== headers.length) fail();
    return Object.fromEntries(headers.map((name,index) => [name,values[index]]));
  });
}

export function inspectPublicSample(text, provider) {
  const profiles = {
    GAIA_DR3_PUBLIC_SAMPLE: {id:'source_id',ra:'ra',dec:'dec',required:['source_id','ref_epoch','ra','dec','pmra','pmdec']},
    PS1_DR2_PUBLIC_SAMPLE: {id:'objID',ra:'raMean',dec:'decMean',required:['objID','raMean','decMean','nDetections','gMeanPSFMag','rMeanPSFMag']}
  };
  if (!Object.hasOwn(profiles,provider)) fail();
  const profile=profiles[provider], rows=csv(text), seen=new Set();
  const sources=rows.map(row => {
    if (profile.required.some(key => !Object.hasOwn(row,key))) fail();
    const id=row[profile.id]; if (!/^\d{1,20}$/.test(id) || seen.has(id)) fail(); seen.add(id);
    const ra=numeric(row[profile.ra]), dec=numeric(row[profile.dec]);
    if (ra < 0 || ra >= 360 || dec < -90 || dec > 90) fail();
    const normalized={catalogId:id,raDeg:ra,decDeg:dec,measurementQuality:'UNKNOWN',rawFields:row};
    if (provider === 'GAIA_DR3_PUBLIC_SAMPLE') {
      normalized.astrometricEpoch={value:numeric(row.ref_epoch),unit:'JULIAN_YEAR',timeScale:'TCB'};
      normalized.properMotion={pmraMasPerYear:row.pmra === '' ? null : numeric(row.pmra),pmdecMasPerYear:row.pmdec === '' ? null : numeric(row.pmdec),raConvention:'MU_ALPHA_COS_DEC'};
      normalized.epochPropagation='NOT_PERFORMED_COVARIANCE_AND_METHOD_PENDING';
    } else {
      const detections=numeric(row.nDetections); if (!Number.isSafeInteger(detections) || detections < 0) fail();
      const magnitude = value => value === '' || value === '-999.0' || value === '-999' ? null : numeric(value);
      normalized.catalogDetectionCount=detections;
      normalized.magnitudes={g:magnitude(row.gMeanPSFMag),r:magnitude(row.rMeanPSFMag)};
      normalized.observationEpoch='UNKNOWN_AGGREGATE_IS_NOT_SINGLE_EPOCH';
    }
    return normalized;
  });
  return {kind:'BKL051_S1_PUBLIC_SAMPLE_INSPECTION_V1',provider,sourceSha256:createHash('sha256').update(text,'utf8').digest('hex'),
    state:'PUBLIC_SAMPLE_ONLY_NO_OWNER_ANALYSIS',sources,catalogCompleteness:'NOT_ESTABLISHED',
    crossMatchPerformed:false,photometryPerformed:false,candidateClassification:'NOT_EVALUATED'};
}
