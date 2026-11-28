const HOUR = 60 * 60 * 1000;
const PROJECTION_TYPE = "BKL031_F9_REPEATABLE_CURRENT_NIGHT";
const WEATHER_POLICY = "DSG-F9-PLANNER-WEATHER-GATE@1.3";
const F9_METHOD = "BKL031-F9-SWISSEPH-MOSHIER-SIDEREAL@1.2";
const ZONE = "Europe/Rome";

function parseInstant(value) {
  const timestamp = Date.parse(value);
  return Number.isFinite(timestamp) ? timestamp : null;
}

function localTime(timestamp, includeDate = false) {
  const options = includeDate
    ? { timeZone: ZONE, day: "numeric", month: "long", hour: "2-digit", minute: "2-digit", hourCycle: "h23", timeZoneName: "short" }
    : { timeZone: ZONE, hour: "2-digit", minute: "2-digit", hourCycle: "h23", timeZoneName: "short" };
  return new Intl.DateTimeFormat("it-IT", options).format(new Date(timestamp));
}

function numberSpeech(value, maximumFractionDigits = 1) {
  return new Intl.NumberFormat("it-IT", { maximumFractionDigits }).format(value);
}

function sourceLabel() {
  return "MeteoHub; autorità ItaliaMeteo e ARPAE, modello ICON due I, licenza CC BY quattro";
}

function provenance(projection) {
  const run = parseInstant(projection.forecast.runInitialisationUtc);
  const retrieval = parseInstant(projection.forecast.retrievedAtUtc);
  return "Fonte " + sourceLabel() + ". Run inizializzato il " + localTime(run, true) + ", dati recuperati il " + localTime(retrieval, true) + ".";
}

function checkProjection(projection, now) {
  if (!projection || typeof projection !== "object") return "MISSING";
  if (projection.schemaVersion !== "1.0" || projection.projectionType !== PROJECTION_TYPE) return "UNSUPPORTED";
  if (projection.environment !== "EVALUATION" || projection.authority !== "NONE" || projection.consumerMode !== "READ_ONLY") return "UNSUPPORTED";
  if (projection.site?.coordinateDisclosure !== "PROHIBITED" || projection.site?.timezoneIana !== ZONE || projection.site?.publicLabel !== "Manciano (GR), Italia") return "UNSUPPORTED";
  if (projection.method?.id !== F9_METHOD || projection.weatherPolicy?.id !== WEATHER_POLICY) return "UNSUPPORTED";
  if (projection.forecast?.providerId !== "METEOHUB" || projection.forecast?.upstreamAuthorityId !== "ITALIAMETEO_ARPAE" || projection.forecast?.modelId !== "ICON_2I") return "UNSUPPORTED";
  const run = parseInstant(projection.forecast?.runInitialisationUtc);
  const generated = parseInstant(projection.generatedAtUtc);
  const retrieved = parseInstant(projection.forecast?.retrievedAtUtc);
  if (run === null || generated === null || retrieved === null) return "INVALID";
  if (generated > now + 5 * 60 * 1000 || retrieved > now + 5 * 60 * 1000 || run > now + 5 * 60 * 1000) return "INVALID";
  if (projection.forecast?.freshnessState === "STALE" || now - generated > 18 * HOUR || now - run > 18 * HOUR || now - retrieved > 18 * HOUR) return "STALE";
  if (projection.forecast?.freshnessState !== "FRESH") return "INVALID";
  if (!Array.isArray(projection.hourly) || projection.hourly.length === 0) return "MISSING";
  return "CURRENT";
}

function expectedHours(start, end) {
  const result = [];
  for (let time = start; time < end; time += HOUR) result.push(time);
  return result;
}

function validWeather(row) {
  if (!row || typeof row !== "object") return false;
  const validAt = parseInstant(row.validAtUtc);
  if (validAt === null || validAt % HOUR !== 0 || !row.weather || typeof row.weather !== "object") return false;
  const required = ["temperatureC", "dewPointC", "cloudCoverPct", "relativeHumidityPct", "precipitationMm", "windSpeedKmh", "windGustKmh"];
  if (!required.every((key) => row.weather[key] === null || (typeof row.weather[key] === "number" && Number.isFinite(row.weather[key])))) return false;
  const w = row.weather;
  const percentageValid = (value) => value === null || (value >= 0 && value <= 100);
  const nonNegative = (value) => value === null || value >= 0;
  return percentageValid(w.cloudCoverPct) && percentageValid(w.relativeHumidityPct) &&
    nonNegative(w.precipitationMm) && nonNegative(w.windSpeedKmh) && nonNegative(w.windGustKmh) &&
    (w.precipitationUncertain === undefined || typeof w.precipitationUncertain === "boolean");
}

function nightWindowState(start, end, now) {
  const futureHour = Math.ceil(now / HOUR) * HOUR;
  if (end <= futureHour) return "PAST";
  if (start > futureHour) return "FUTURE";
  return "CURRENT";
}

function renderSample(row) {
  const w = row.weather;
  const fields = [];
  fields.push(w.precipitationUncertain === true
    ? "precipitazione indeterminata"
    : w.precipitationMm === null ? "precipitazione non disponibile"
      : w.precipitationMm === 0 ? "precipitazione zero millimetri"
        : "precipitazione " + numberSpeech(w.precipitationMm, 4) + " millimetri");
  fields.push(w.windSpeedKmh === null ? "vento non disponibile" : "vento " + numberSpeech(w.windSpeedKmh) + " chilometri orari");
  fields.push(w.windGustKmh === null ? "raffiche non disponibili" : "raffiche " + numberSpeech(w.windGustKmh) + " chilometri orari");
  fields.push(w.cloudCoverPct === null ? "nuvolosità non disponibile" : "nuvolosità " + numberSpeech(w.cloudCoverPct) + " per cento");
  fields.push(w.relativeHumidityPct === null ? "umidità non disponibile" : "umidità " + numberSpeech(w.relativeHumidityPct) + " per cento");
  fields.push(w.dewPointC === null ? "punto di rugiada non disponibile" : "punto di rugiada " + numberSpeech(w.dewPointC) + " gradi");
  return "Alle " + localTime(Date.parse(row.validAtUtc)) + ": " + fields.join(", ") + ".";
}

export function describeForecast(projection, options = {}) {
  const now = options.now ?? Date.now();
  const period = options.period ?? "stanotte";
  const hours = options.hours ?? 3;
  const freshness = checkProjection(projection, now);
  if (freshness === "STALE") {
    const run = parseInstant(projection?.forecast?.runInitialisationUtc);
    const retrieved = parseInstant(projection?.forecast?.retrievedAtUtc);
    const source = projection?.forecast?.upstreamAuthorityId === "ITALIAMETEO_ARPAE" && projection?.forecast?.modelId === "ICON_2I"
      ? "Fonte MeteoHub; autorità ItaliaMeteo e ARPAE, modello ICON due I, licenza CC BY quattro."
      : "Fonte non verificata.";
    const runText = run === null ? "" : " Il run era inizializzato il " + localTime(run, true) + ".";
    const retrievalText = retrieved === null ? "" : " I dati erano stati recuperati il " + localTime(retrieved, true) + ".";
    return { state: "STALE", speech: "Il dato meteo non è aggiornato e non posso presentarlo come corrente. " + source + runText + retrievalText };
  }
  if (freshness === "MISSING") return { state: "UNAVAILABLE", speech: "La proiezione meteo non è disponibile." };
  if (freshness !== "CURRENT") return { state: "UNAVAILABLE", speech: "La proiezione meteo non è valida o usa un contratto non supportato." };

  const startOfNight = parseInstant(projection.nightWindow?.fromUtc);
  const endOfNight = parseInstant(projection.nightWindow?.toUtcExclusive);
  if (startOfNight === null || endOfNight === null || endOfNight <= startOfNight || startOfNight % HOUR !== 0 || endOfNight % HOUR !== 0) {
    return { state: "UNAVAILABLE", speech: "L’intervallo della previsione non è valido." };
  }
  const firstFutureHour = Math.ceil(now / HOUR) * HOUR;
  const start = Math.max(firstFutureHour, startOfNight);
  let end = endOfNight;
  let expectedStart = start;
  let expectedEnd = end;
  if (period === "prossime ore") {
    if (!Number.isInteger(hours) || hours < 1 || hours > 12) {
      return { state: "INVALID_REQUEST", speech: "Posso consultare da una a dodici ore. Dimmi un intervallo valido." };
    }
    const requestedEnd = firstFutureHour + hours * HOUR;
    if (startOfNight >= requestedEnd || endOfNight <= firstFutureHour) {
      return { state: "UNAVAILABLE", speech: "La proiezione F9 copre solo la notte corrente; non contiene una finestra mobile per le prossime ore. " + provenance(projection) };
    }
    expectedStart = firstFutureHour;
    expectedEnd = requestedEnd;
    end = Math.min(requestedEnd, endOfNight);
  } else if (period !== "stanotte") {
    return { state: "INVALID_REQUEST", speech: "Posso consultare le previsioni per stanotte o per le prossime ore." };
  }
  if (start >= end) return { state: "UNAVAILABLE", speech: "La finestra meteo richiesta non è coperta dal run corrente. " + provenance(projection) };

  const rowsByTime = new Map();
  for (const row of projection.hourly) {
    const time = parseInstant(row?.validAtUtc);
    if (time !== null && time >= start && time < end && !validWeather(row)) {
      return { state: "UNAVAILABLE", speech: "La proiezione contiene un campione non valido nell’intervallo richiesto e non può essere usata." };
    }
    if (!validWeather(row)) continue;
    if (time >= start && time < end) {
      if (rowsByTime.has(time)) return { state: "UNAVAILABLE", speech: "La proiezione meteo contiene campioni duplicati e non può essere usata." };
      rowsByTime.set(time, row);
    }
  }
  const expected = expectedHours(expectedStart, expectedEnd);
  const rows = expected.filter((time) => rowsByTime.has(time)).map((time) => rowsByTime.get(time));
  if (rows.length === 0) return { state: "UNAVAILABLE", speech: "La proiezione non contiene campioni meteo per l’intervallo richiesto. " + provenance(projection) };

  const coverageStart = localTime(Date.parse(rows[0].validAtUtc), true);
  const coverageEnd = localTime(Math.min(end, Date.parse(rows[rows.length - 1].validAtUtc) + HOUR), true);
  const partial = rows.length !== expected.length;
  const missingSamples = expected.filter((time) => !rowsByTime.has(time)).map((time) => localTime(time, true));
  const prefix = partial
    ? "La previsione copre solo una parte dell’intervallo, da " + coverageStart + " a " + coverageEnd + " ora locale. Campioni orari mancanti: " + missingSamples.join("; ") + ". "
    : "Previsione da " + coverageStart + " a " + coverageEnd + " ora locale. ";
  const locality = projection.site?.publicLabel ? "Località " + projection.site.publicLabel + ". " : "";
  const samples = rows.map(renderSample).join(" ");
  const source = provenance(projection);
  return { state: partial ? "PARTIAL" : "CURRENT", coverage: { expectedHours: expected.length, availableHours: rows.length }, speech: locality + prefix + samples + " " + source };
}
