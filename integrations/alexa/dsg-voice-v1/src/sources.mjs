import { describeForecast } from "./forecast.mjs";

const BASE = "https://maininimassimo-bit.github.io/digital-stargate-manual/data/";
const PATHS = Object.freeze({
  f9_forecast: "observation-planner-f9-current-night.json"
});
const MAX_BYTES = 2_500_000;

async function readBodyLimited(response) {
  if (!response.body) return null;
  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > MAX_BYTES) {
        await reader.cancel();
        return null;
      }
      chunks.push(Buffer.from(value));
    }
    return Buffer.concat(chunks, total).toString("utf8");
  } finally {
    reader.releaseLock();
  }
}

async function readApprovedJson(key) {
  const approved = process.env["DSG_VOICE_APPROVE_" + key.toUpperCase()] === "true";
  if (!approved) return { state: "UNAVAILABLE" };
  const path = PATHS[key];
  if (!path) return { state: "UNAVAILABLE" };
  try {
    const response = await fetch(BASE + path, { method: "GET", redirect: "error", headers: { accept: "application/json" }, signal: AbortSignal.timeout(1500) });
    if (!response.ok || !/^application\/json(?:\s*;|$)/i.test(response.headers.get("content-type") ?? "") || Number(response.headers.get("content-length") ?? 0) > MAX_BYTES) return { state: "UNAVAILABLE" };
    const text = await readBodyLimited(response);
    if (text === null) return { state: "UNAVAILABLE" };
    return { state: "CURRENT", value: JSON.parse(text) };
  } catch {
    return { state: "UNAVAILABLE" };
  }
}

export function createSources() {
  return {
    async getLatestSession() {
      // The current analytics catalogue has no voice-approved eligibility rule or
      // freshness timestamp. Keep this unavailable until a governed voice projection exists.
      return { state: "UNAVAILABLE" };
    },
    async getForecast(request) {
      const result = await readApprovedJson("f9_forecast");
      return result.state === "CURRENT"
        ? describeForecast(result.value, request)
        : { state: "UNAVAILABLE", speech: "La proiezione meteo non è disponibile." };
    },
    async getObservatorySummary() {
      return { state: "UNAVAILABLE" };
    },
    async getRecentAlerts() {
      return { state: "UNAVAILABLE" };
    }
  };
}
