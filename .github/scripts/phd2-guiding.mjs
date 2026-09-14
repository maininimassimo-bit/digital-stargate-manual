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

export const parseGuideLog = (text, sourcePath = '', maxPoints = 96) => {
  const samples = [];
  let segment = 0;
  let settling = false;

  for (const line of text.split(/\r?\n/)) {
    if (line.startsWith('Guiding Begins at ')) {
      segment += 1;
      settling = false;
      continue;
    }

    const low = line.toLowerCase();
    if (low.includes('settling started')) {
      settling = true;
      continue;
    }
    if (low.includes('settling complete')) {
      settling = false;
      continue;
    }
    if (settling || segment === 0 || !/^\d+,\s*[\d.]+,"[^"]+",/.test(line)) continue;

    const row = parseCsvRecord(line);
    if (row.length <= 17) continue;

    const errorCode = Number(row[17] || 0);
    if (!Number.isFinite(errorCode) || errorCode !== 0) continue;

    const elapsedSeconds = numberOrNull(row[1]);
    const raArcsec = numberOrNull(row[7]);
    const decArcsec = numberOrNull(row[8]);
    if (elapsedSeconds === null || raArcsec === null || decArcsec === null) continue;

    samples.push({
      segment,
      elapsedSeconds: round(elapsedSeconds),
      raArcsec: round(raArcsec),
      decArcsec: round(decArcsec),
      totalArcsec: round(Math.hypot(raArcsec, decArcsec))
    });
  }

  if (!samples.length) return null;

  const ra = samples.map((sample) => sample.raArcsec);
  const dec = samples.map((sample) => sample.decArcsec);
  const total = samples.map((sample) => sample.totalArcsec);
  const rmsRa = rms(ra);
  const rmsDec = rms(dec);

  return {
    sourcePath: String(sourcePath).replaceAll('\\', '/'),
    sampleCount: samples.length,
    segmentCount: Math.max(...samples.map((sample) => sample.segment)),
    rmsRaArcsec: round(rmsRa),
    rmsDecArcsec: round(rmsDec),
    rmsTotalArcsec: round(Math.hypot(rmsRa ?? 0, rmsDec ?? 0)),
    p95TotalArcsec: round(percentile(total, 95)),
    maxTotalArcsec: round(Math.max(...total)),
    samples: downsample(samples, maxPoints)
  };
};
