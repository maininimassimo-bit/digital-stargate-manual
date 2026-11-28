import { handleIntent, launchResponse, helpResponse, cancelResponse } from "./voice.mjs";
import { createSources } from "./sources.mjs";

const sources = createSources();

function assertSkillIdentity(event, expectedSkillId) {
  if (!expectedSkillId) throw new Error("DSG_VOICE_SKILL_ID is not configured");
  const actual = event?.context?.System?.application?.applicationId
    ?? event?.session?.application?.applicationId
    ?? null;
  if (actual !== expectedSkillId) throw new Error("Alexa skill identity mismatch");
}

export async function handler(event) {
  assertSkillIdentity(event, process.env.DSG_VOICE_SKILL_ID);
  const request = event?.request;
  if (!request || typeof request.requestId !== "string" || typeof request.type !== "string") {
    throw new Error("Malformed Alexa request");
  }
  if (request.locale && request.locale !== "it-IT") {
    return { version: "1.0", response: { outputSpeech: { type: "PlainText", text: "Questa skill è disponibile in italiano." }, shouldEndSession: true } };
  }
  switch (request.type) {
    case "LaunchRequest":
      return launchResponse();
    case "SessionEndedRequest":
      return { version: "1.0", response: {} };
    case "IntentRequest": {
      const name = request.intent?.name;
      if (name === "AMAZON.HelpIntent") return helpResponse();
      if (name === "AMAZON.CancelIntent" || name === "AMAZON.StopIntent" || name === "AMAZON.NavigateHomeIntent") return cancelResponse();
      if (name === "AMAZON.FallbackIntent") return { version: "1.0", response: { outputSpeech: { type: "PlainText", text: "Non ho capito. Puoi chiedermi aiuto." }, shouldEndSession: false } };
      return handleIntent(name, request.intent?.slots ?? {}, sources);
    }
    default:
      return { version: "1.0", response: { outputSpeech: { type: "PlainText", text: "Richiesta non supportata." }, shouldEndSession: true } };
  }
}
