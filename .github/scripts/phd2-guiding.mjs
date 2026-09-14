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

const headerMap = (line) => new Map(
  parseCsvRecord(line).map((name, index) => [name.trim().toLowerCase(), index])
);

const field = (row, header, name) => {
  const index = header.get(name.toLowerCase());
  return index === undefined ? '' : String(row[index] ?? '').trim();
};

export const parseGuideLog = (text, sourcePath = '', maxPoints = 96) => {
  const samples = [];
  const raValues = [];
  const decValues = [];
  const totalValues = [];
  const profiles = new Set();
  let segment = 0;
  let activeSegment = false;
  let settling = false;
  let header = null;
  let pixelScale = null;
  let sampleCountTotal = 0;
  let saturatedSampleCount = 0;
  let rejectedSampleCount = 0;
  let settlingExcludedSampleCount = 0;
  let unscaledSampleCount = 0;
  let settlingFailureCount = 0;

  for (const line of text.split(/\r?\n/)) {
    const low = line.toLowerCase();
    if (low.startsWith('equipment profile =')) {
      const profile = line.split('=', 2)[1]?.trim();
      if (profile) profiles.add(profile);
    }

    const scaleMatch = line.match(/Pixel scale\s*=\s*(\d+(?:\.\d+)?)\s*arc-sec\/px/i);
    if (scaleMatch) pixelScale = Number(scaleMatch[1]);

    if (line.startsWith('Guiding Begins at ')) {
      segment += 1;
      activeSegment = true;
      header = null;
      pixelScale = null;
      continue;
    }
    if (line.startsWith('Guiding Ends at ')) {
      activeSegment = false;
      header = null;
      continue;
    }
    if (low.startsWith('frame,time,')) {
      header = headerMap(line);
      continue;
    }
    if (low.includes('settling started')) {
      settling = true;
      continue;
    }
    if (low.includes('settling complete') || low.includes('settling failed')) {
      if (low.includes('settling failed')) settlingFailureCount += 1;
      settling = false;
      continue;
    }
    if (!activeSegment || header === null || !/^\d+,/.test(line)) continue;

    const row = parseCsvRecord(line);
    const elapsedSeconds = numberOrNull(field(row, header, 'Time'));
    const errorCode = numberOrNull(field(row, header, 'ErrorCode')) ?? 0;
    if (elapsedSeconds === null || !Number.isInteger(errorCode)) continue;

    sampleCountTotal += 1;
    if (settling) {
      settlingExcludedSampleCount += 1;
      continue;
    }

    const mount = field(row, header, 'mount').toUpperCase();
    if (mount === 'DROP' || ![0, 1].includes(errorCode)) {
      rejectedSampleCount += 1;
      continue;
    }
    if (pixelScale === null || !Number.isFinite(pixelScale)) {
      unscaledSampleCount += 1;
      continue;
    }

    const raRaw = numberOrNull(field(row, header, 'RARawDistance'));
    const decRaw = numberOrNull(field(row, header, 'DECRawDistance'));
    if (raRaw === null || decRaw === null) continue;

    const raArcsec = raRaw * pixelScale;
    const decArcsec = decRaw * pixelScale;
    const totalArcsec = Math.hypot(raArcsec, decArcsec);
    if (errorCode === 1) saturatedSampleCount += 1;
    raValues.push(raArcsec);
    decValues.push(decArcsec);
    totalValues.push(totalArcsec);
    samples.push({
      segment,
      elapsedSeconds: round(elapsedSeconds),
      raArcsec: round(raArcsec),
      decArcsec: round(decArcsec),
      totalArcsec: round(totalArcsec),
      saturated: errorCode === 1
    });
  }

  if (!samples.length) return null;

  const rmsRa = rms(raValues);
  const rmsDec = rms(decValues);
  return {
    sourcePath: String(sourcePath).replaceAll('\\', '/'),
    sampleCount: samples.length,
    sampleCountTotal,
    saturatedSampleCount,
    rejectedSampleCount,
    settlingExcludedSampleCount,
    unscaledSampleCount,
    settlingFailureCount,
    equipmentProfiles: [...profiles].sort(),
    segmentCount: segment,
    rmsMethod: 'PHD2 RARawDistance/DECRawDistance multiplied by the active segment pixel scale; ErrorCode 0 and STAR_SATURATED (1) included; settling excluded.',
    rmsRaArcsec: round(rmsRa),
    rmsDecArcsec: round(rmsDec),
    rmsTotalArcsec: round(Math.hypot(rmsRa ?? 0, rmsDec ?? 0)),
    p95TotalArcsec: round(percentile(totalValues, 95)),
    maxTotalArcsec: round(Math.max(...totalValues)),
    samples: downsample(samples, maxPoints)
  };
};
