import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { describeForecast } from "../src/forecast.mjs";
import { handleIntent, commandBoundaryResponse } from "../src/voice.mjs";
import { handler } from "../src/index.mjs";
import { createSources } from "../src/sources.mjs";

const baseTime = Date.parse("2026-11-26T15:00:00Z");

test("ExplainStatus Alexa samples preserve the status slot and Alexa-compatible apostrophes", () => {
  const modelPath = new URL("../skill-package/interactionModels/custom/it-IT.json", import.meta.url);
  const model = JSON.parse(readFileSync(fileURLToPath(modelPath), "utf8"));
  const intent = model.interactionModel.languageModel.intents.find(({ name }) => name === "ExplainStatus");

  assert.ok(intent, "ExplainStatus intent exists");
  assert.ok(intent.samples.length > 0);
  assert.ok(intent.samples.every((sample) => sample.includes("{StatusCode}")), "each sample passes its status to the handler");
  assert.ok(intent.samples.every((sample) => !/[‘’]/u.test(sample)), "samples use ASCII apostrophes accepted by Alexa build");
  assert.ok(intent.samples.some((sample) => sample.includes("{StatusCode}") && sample.toLowerCase().includes("osservatorio")));
});

test("unavailable-status voice phrase has a dedicated deterministic intent", async () => {
  const model = JSON.parse(readFileSync(fileURLToPath(new URL("../skill-package/interactionModels/custom/it-IT.json", import.meta.url)), "utf8"));
  const intent = model.interactionModel.languageModel.intents.find(({ name }) => name === "ExplainUnavailableStatus");
  assert.ok(intent);
  assert.deepEqual(intent.slots, []);
  assert.ok(intent.samples.includes("cosa significa lo stato non disponibile dell'osservatorio"));
  assert.ok(intent.samples.every((sample) => !/[‘’]/u.test(sample)));

  const response = await handleIntent("ExplainUnavailableStatus", {}, {});
  assert.match(response.response.outputSpeech.text, /^Non disponibile significa che la fonte o la proiezione/);
});

function projection(overrides = {}) {
  return {
    schemaVersion: "1.0",
    projectionType: "BKL031_F9_REPEATABLE_CURRENT_NIGHT",
    generatedAtUtc: "2026-11-26T14:00:00Z",
    environment: "EVALUATION",
    authority: "NONE",
    consumerMode: "READ_ONLY",
    site: { publicLabel: "Manciano (GR), Italia", timezoneIana: "Europe/Rome", coordinateDisclosure: "PROHIBITED" },
    forecast: { providerId: "METEOHUB", upstreamAuthorityId: "ITALIAMETEO_ARPAE", modelId: "ICON_2I", runInitialisationUtc: "2026-11-26T12:00:00Z", retrievedAtUtc: "2026-11-26T14:00:00Z", freshnessState: "FRESH" },
    nightWindow: { fromUtc: "2026-11-26T15:00:00Z", toUtcExclusive: "2026-11-26T18:00:00Z" },
    method: { id: "BKL031-F9-SWISSEPH-MOSHIER-SIDEREAL@1.2" },
    weatherPolicy: { id: "DSG-F9-PLANNER-WEATHER-GATE@1.3" },
    hourly: [
      { validAtUtc: "2026-11-26T15:00:00Z", weather: { temperatureC: 14, dewPointC: 8, cloudCoverPct: 50, relativeHumidityPct: 70, precipitationMm: 0, windSpeedKmh: 12, windGustKmh: 18 } },
      { validAtUtc: "2026-11-26T16:00:00Z", weather: { temperatureC: 13, dewPointC: 8, cloudCoverPct: 40, relativeHumidityPct: 75, precipitationMm: 0.002, windSpeedKmh: 10, windGustKmh: 15 } },
      { validAtUtc: "2026-11-26T17:00:00Z", weather: { temperatureC: 12, dewPointC: 7, cloudCoverPct: 30, relativeHumidityPct: 80, precipitationMm: 0, windSpeedKmh: 8, windGustKmh: 12 } }
    ],
    ...overrides
  };
}

test("forecast speaks weather fields, provenance and local coverage", () => {
  const result = describeForecast(projection(), { now: baseTime, period: "stanotte" });
  assert.equal(result.state, "CURRENT");
  assert.match(result.speech, /precipitazione zero millimetri/);
  assert.match(result.speech, /vento 12 chilometri orari/);
  assert.match(result.speech, /raffiche 18 chilometri orari/);
  assert.match(result.speech, /nuvolosità 50 per cento/);
  assert.match(result.speech, /umidità 70 per cento/);
  assert.match(result.speech, /punto di rugiada 8 gradi/);
  assert.match(result.speech, /Fonte MeteoHub/);
  assert.match(result.speech, /ItaliaMeteo e ARPAE/);
  assert.match(result.speech, /CC BY quattro/);
  assert.match(result.speech, /run inizializzato/i);
  assert.doesNotMatch(result.speech, /63\.8|85\.6331|raDeg|decDeg/);
});

test("forecast fails closed when run is older than 18 hours", () => {
  const current = projection();
  const stale = projection({ forecast: { ...current.forecast, runInitialisationUtc: "2026-11-25T12:00:00Z" } });
  const result = describeForecast(stale, { now: baseTime });
  assert.equal(result.state, "STALE");
  assert.match(result.speech, /non è aggiornato/);
  assert.match(result.speech, /run era inizializzato/);
});

test("forecast distinguishes partial coverage", () => {
  const current = projection();
  const partial = projection({ hourly: [current.hourly[0], current.hourly[2]] });
  const result = describeForecast(partial, { now: baseTime, period: "stanotte" });
  assert.equal(result.state, "PARTIAL");
  assert.match(result.speech, /solo una parte dell’intervallo/);
  assert.match(result.speech, /Campioni orari mancanti: 26 novembre alle ore 17:00/);
});

test("forecast disambiguates the repeated local hour at the CET/CEST transition", () => {
  const current = projection();
  const dst = projection({
    generatedAtUtc: "2026-10-24T20:00:00Z",
    forecast: { ...current.forecast, runInitialisationUtc: "2026-10-24T12:00:00Z", retrievedAtUtc: "2026-10-24T20:00:00Z" },
    nightWindow: { fromUtc: "2026-10-24T23:00:00Z", toUtcExclusive: "2026-10-25T02:00:00Z" },
    hourly: [
      { validAtUtc: "2026-10-24T23:00:00Z", weather: { ...current.hourly[0].weather } },
      { validAtUtc: "2026-10-25T00:00:00Z", weather: { ...current.hourly[1].weather } },
      { validAtUtc: "2026-10-25T01:00:00Z", weather: { ...current.hourly[2].weather } }
    ]
  });
  const result = describeForecast(dst, { now: Date.parse("2026-10-24T23:00:00Z"), period: "stanotte" });
  assert.equal(result.state, "CURRENT");
  assert.match(result.speech, /02:00 CEST/);
  assert.match(result.speech, /02:00 CET/);
});

test("uncertain precipitation is not spoken as zero", () => {
  const current = projection();
  current.hourly[0].weather.precipitationUncertain = true;
  const result = describeForecast(current, { now: baseTime, period: "prossime ore", hours: 1 });
  assert.match(result.speech, /precipitazione indeterminata/);
  assert.doesNotMatch(result.speech, /precipitazione zero/);
});

test("forecast rejects unsupported policy and non-finite readings", () => {
  assert.equal(describeForecast(projection({ weatherPolicy: { id: "unrecognized" } }), { now: baseTime }).state, "UNAVAILABLE");
  const noFreshness = projection();
  delete noFreshness.forecast.freshnessState;
  assert.equal(describeForecast(noFreshness, { now: baseTime }).state, "UNAVAILABLE");
  const invalid = projection();
  invalid.hourly[0].weather.windSpeedKmh = Infinity;
  const result = describeForecast(invalid, { now: baseTime });
  assert.equal(result.state, "UNAVAILABLE");
  assert.match(result.speech, /campione non valido/);
  assert.doesNotMatch(result.speech, /Infinity/);
});

test("next-hours request is explicitly unavailable outside F9 current-night coverage", () => {
  const beforeNight = projection({ nightWindow: { fromUtc: "2026-11-26T18:00:00Z", toUtcExclusive: "2026-11-26T22:00:00Z" } });
  const before = describeForecast(beforeNight, { now: Date.parse("2026-11-26T15:00:00Z"), period: "prossime ore", hours: 3 });
  assert.equal(before.state, "UNAVAILABLE");
  assert.match(before.speech, /non contiene una finestra mobile/);

  const after = describeForecast(projection(), { now: Date.parse("2026-11-26T19:00:00Z"), period: "prossime ore", hours: 3 });
  assert.equal(after.state, "UNAVAILABLE");
  assert.match(after.speech, /non contiene una finestra mobile/);

  const exceedsNight = describeForecast(projection(), { now: Date.parse("2026-11-26T15:00:00Z"), period: "prossime ore", hours: 6 });
  assert.equal(exceedsNight.state, "UNAVAILABLE");
  assert.match(exceedsNight.speech, /non copre tutte le ore richieste/);
});

test("fresh F9 run with an expired night window does not report current forecast", () => {
  const expired = projection({ nightWindow: { fromUtc: "2026-11-26T12:00:00Z", toUtcExclusive: "2026-11-26T14:00:00Z" } });
  const result = describeForecast(expired, { now: baseTime, period: "stanotte" });
  assert.equal(result.state, "UNAVAILABLE");
  assert.match(result.speech, /finestra meteo richiesta non è coperta/);
});

test("forecast validates timestamp boundaries for the 18-hour freshness rule", () => {
  const exactlyAtLimit = projection({ forecast: { ...projection().forecast, runInitialisationUtc: "2026-11-25T21:00:00Z" } });
  assert.notEqual(describeForecast(exactlyAtLimit, { now: baseTime }).state, "STALE");
  const beyondLimit = projection({ forecast: { ...projection().forecast, runInitialisationUtc: "2026-11-25T20:59:59Z" } });
  assert.equal(describeForecast(beyondLimit, { now: baseTime }).state, "STALE");
  const futureRun = projection({ forecast: { ...projection().forecast, runInitialisationUtc: "2026-11-26T15:06:00Z" } });
  assert.equal(describeForecast(futureRun, { now: baseTime }).state, "UNAVAILABLE");
});

test("missing alert source is distinct from empty alert list", async () => {
  const missing = await handleIntent("GetRecentAlerts", {}, {});
  const empty = await handleIntent("GetRecentAlerts", {}, { getRecentAlerts: async () => ({ state: "EMPTY", generatedAtUtc: "2026-11-26T20:40:00Z" }) });
  assert.match(missing.response.outputSpeech.text, /fonte degli avvisi non è disponibile/);
  assert.match(empty.response.outputSpeech.text, /Non risultano avvisi registrati nella proiezione aggiornata il .*21:40 ora locale/);
  assert.notEqual(missing.response.outputSpeech.text, empty.response.outputSpeech.text);
});

test("command boundary remains read-only", () => {
  const result = commandBoundaryResponse();
  assert.match(result.response.outputSpeech.text, /non posso comandare/);
  assert.equal(result.response.shouldEndSession, true);
});

test("unsupported command intent is wired to the fixed refusal without source access", async () => {
  let reads = 0;
  const result = await handleIntent("UnsupportedCommandIntent", {}, {
    getForecast: async () => { reads += 1; return {}; },
    getLatestSession: async () => { reads += 1; return {}; }
  });
  assert.match(result.response.outputSpeech.text, /non posso comandare/);
  assert.match(result.response.outputSpeech.text, /Non fornisco giudizi di sicurezza/);
  assert.equal(reads, 0);
});

test("status explanation is deterministic", async () => {
  const unknown = await handleIntent("ExplainStatus", { StatusCode: { value: "sconosciuto" } }, {});
  const stale = await handleIntent("ExplainStatus", { StatusCode: { value: "dato non aggiornato" } }, {});
  assert.match(unknown.response.outputSpeech.text, /Non vuol dire che il sistema sia in buono stato/);
  assert.match(stale.response.outputSpeech.text, /limite di freschezza/);
});

test("forecast hour-count slot selects the next-hours mode", async () => {
  let request;
  await handleIntent("GetWeatherForecast", { HourCount: { value: "4" } }, {
    getForecast: async (value) => { request = value; return { state: "UNAVAILABLE", speech: "no" }; }
  });
  assert.equal(request.period, "prossime ore");
  assert.equal(request.hours, 4);
});

test("summary and alert details cannot speak unapproved dynamic text", async () => {
  const summary = await handleIntent("GetObservatorySummary", {}, {
    getObservatorySummary: async () => ({ state: "CURRENT", speech: "raw internal detail" })
  });
  const alerts = await handleIntent("GetRecentAlerts", {}, {
    getRecentAlerts: async () => ({ state: "CURRENT", alerts: [{ message: "raw internal detail", occurredAt: "2026-11-26T20:00:00Z" }] })
  });
  assert.doesNotMatch(summary.response.outputSpeech.text, /raw internal detail/);
  assert.doesNotMatch(alerts.response.outputSpeech.text, /raw internal detail/);
});

test("Lambda handler rejects a request with the wrong Alexa skill ID", async () => {
  process.env.DSG_VOICE_SKILL_ID = "amzn1.ask.skill.expected";
  await assert.rejects(handler({ context: { System: { application: { applicationId: "amzn1.ask.skill.other" } } }, request: { requestId: "r1", type: "LaunchRequest" } }), /identity mismatch/);
});

test("Lambda handler serves Italian launch without reading projections", async () => {
  process.env.DSG_VOICE_SKILL_ID = "amzn1.ask.skill.expected";
  delete process.env.DSG_VOICE_APPROVE_SESSION_CATALOG;
  delete process.env.DSG_VOICE_APPROVE_F9_FORECAST;
  const result = await handler({
    context: { System: { application: { applicationId: "amzn1.ask.skill.expected" } } },
    request: { requestId: "r2", type: "LaunchRequest", locale: "it-IT" }
  });
  assert.match(result.response.outputSpeech.text, /Benvenuto in Digital StarGate/);
});

test("Lambda handler treats Alexa NavigateHomeIntent as a read-only exit", async () => {
  process.env.DSG_VOICE_SKILL_ID = "amzn1.ask.skill.expected";
  const result = await handler({
    context: { System: { application: { applicationId: "amzn1.ask.skill.expected" } } },
    request: { requestId: "r3", type: "IntentRequest", locale: "it-IT", intent: { name: "AMAZON.NavigateHomeIntent", slots: {} } }
  });
  assert.equal(result.response.shouldEndSession, true);
  assert.match(result.response.outputSpeech.text, /chiudo/);
});

test("source adapter keeps session disabled and forecast does not fetch by default", async () => {
  process.env.DSG_VOICE_APPROVE_SESSION_CATALOG = "true";
  delete process.env.DSG_VOICE_APPROVE_F9_FORECAST;
  const originalFetch = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => { calls += 1; throw new Error("unexpected fetch"); };
  try {
    const sources = createSources();
    assert.equal((await sources.getLatestSession()).state, "UNAVAILABLE");
    assert.equal((await sources.getForecast({ period: "stanotte" })).state, "UNAVAILABLE");
    assert.equal(calls, 0);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("approved F9 reader rejects non-JSON responses without speaking response text", async () => {
  process.env.DSG_VOICE_APPROVE_F9_FORECAST = "true";
  const originalFetch = globalThis.fetch;
  let target;
  globalThis.fetch = async (url, options) => {
    target = { url: String(url), options };
    return new Response("private error body", { status: 200, headers: { "content-type": "text/html" } });
  };
  try {
    const result = await createSources().getForecast({ period: "stanotte" });
    assert.equal(result.state, "UNAVAILABLE");
    assert.doesNotMatch(result.speech, /private error body/);
    assert.match(target.url, /digital-stargate-manual\/data\/observation-planner-f9-current-night\.json$/);
    assert.equal(target.options.method, "GET");
    assert.equal(target.options.redirect, "error");
  } finally {
    delete process.env.DSG_VOICE_APPROVE_F9_FORECAST;
    globalThis.fetch = originalFetch;
  }
});
