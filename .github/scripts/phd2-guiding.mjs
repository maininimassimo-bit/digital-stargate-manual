const round = (value, digits = 3) => value === null ? null : Number(value.toFixed(digits));

const rms = (values) => values.length
  ? Math.sqrt(values.reduce((sum, value) => sum + (value * value), 0) / values.length)
  : null;

const percentile = (values, p) => {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const index = Math.min(sorted.length - 1, Math.max(0, Math.ceil((p / 100) * sorted.length) - 1));
  return sorted[index];
};

const downsample = (rows, maxPoints = 96) => {
  if (rows.length <= maxPoints) return rows;
  const step = (rows.length - 1) / (maxPoints - 1);
  return Array.from({ length: maxPoints }, (_, index) => rows[Math.round(index * step)]);
};

export const parseCsvRecord = (line) => {
  const fields = [];
  let field = '';
  let quoted = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (quoted) {
      if (char === '"' && line[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ',') {
      fields.push(field);
      field = '';
    } else {
      field += char;
    }
  }
  fields.push(field);
  return fields;
};

const numberOrNull = (value) => {
  const text = String(value ?? '').trim();
  if (!text) return null;
  const parsed = Number(text);
  return Number.isFinite(parsed) ? parsed : null;
};

// Same raw-distance / active pixel-scale population as the canonical analyzer.
export const parseGuideLog = (text, sourcePath = '', maxPoints = 96, scope = null) => {
  const samples=[],rawRa=[],rawDec=[],seen=new Map(),countedSegments=new Set();
  let segment=0;
  const wall=value=>Date.parse(value.replace(' ','T').replace(/(\.\d{3})\d+$/,'$1')+'Z');
  const start=scope?wall(scope.start_wall_clock):-Infinity,end=scope?wall(scope.end_wall_clock):Infinity;
  if(scope&&!(Number.isFinite(start)&&Number.isFinite(end)&&end>start))return null;
  for(const source of (Array.isArray(text)?text:[text])){
    let anchor=NaN,active=false,settling=false,scale=null,header=null;
    for(const line of source.split(/\r?\n/)){
      const low=line.toLowerCase();
      if(line.startsWith('Guiding Begins at ')){
        anchor=wall(line.slice(18));active=true;scale=null;header=null;segment++;
        if(!scope||(anchor>=start&&anchor<end))countedSegments.add(anchor);
        continue;
      }
      if(line.startsWith('Guiding Ends at ')){active=false;header=null;continue;}
      const pixel=line.match(/Pixel scale\s*=\s*([\d.]+)\s*arc-sec\/px/i);
      if(pixel)scale=numberOrNull(pixel[1]);
      if(low.startsWith('frame,time,')){header=new Map(parseCsvRecord(line).map((name,i)=>[name.trim().toLowerCase(),i]));continue;}
      if(low.includes('settling started')){settling=true;continue;}
      if(low.includes('settling complete')||low.includes('settling failed')){settling=false;continue;}
      if(!active||!header||settling||!(scale>0)||!/^\d+,/.test(line))continue;
      const row=parseCsvRecord(line),field=name=>row[header.get(name.toLowerCase())];
      const error=numberOrNull(field('ErrorCode')),elapsed=numberOrNull(field('Time'));
      const raPixels=numberOrNull(field('RARawDistance')),decPixels=numberOrNull(field('DECRawDistance'));
      if(![0,1].includes(error)||String(field('mount')).toUpperCase()==='DROP'||elapsed===null||elapsed<0||raPixels===null||decPixels===null)continue;
      const instant=anchor+elapsed*1000;
      if(scope&&!(instant>=start&&instant<end))continue;
      const key=`${anchor}|${field('Frame')}|${field('Time')}`,value=`${raPixels}|${decPixels}|${scale}|${error}`;
      if(seen.has(key)){if(seen.get(key)!==value)return null;continue;}
      seen.set(key,value);countedSegments.add(anchor);
      const raArcsec=raPixels*scale,decArcsec=decPixels*scale;
      rawRa.push(raArcsec);rawDec.push(decArcsec);
      samples.push({segment,elapsedSeconds:round(elapsed),raArcsec:round(raArcsec),decArcsec:round(decArcsec),totalArcsec:round(Math.hypot(raArcsec,decArcsec))});
    }
  }
  if(!samples.length)return null;
  const total=rawRa.map((ra,i)=>Math.hypot(ra,rawDec[i])),rmsRa=rms(rawRa),rmsDec=rms(rawDec);
  return {methodVersion:'PHD2-RAW-PIXELSCALE-1.0',sourcePath:String(sourcePath).replaceAll('\\','/'),sampleCount:samples.length,segmentCount:countedSegments.size,rmsRaArcsec:round(rmsRa),rmsDecArcsec:round(rmsDec),rmsTotalArcsec:round(Math.hypot(rmsRa,rmsDec)),p95TotalArcsec:round(percentile(total,95)),maxTotalArcsec:round(Math.max(...total)),samples:downsample(samples,maxPoints)};
};
