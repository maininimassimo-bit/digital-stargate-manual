const HELP = "Puoi chiedermi lo stato pubblicato dell’osservatorio, l’ultima sessione pubblicata, gli avvisi recenti, il significato di uno stato o le previsioni per stanotte e per le prossime ore. Posso solo consultare dati pubblicati. Non comando dispositivi e non fornisco valutazioni di sicurezza.";
const STATUS = Object.freeze({
  unknown: "Sconosciuto significa che la fonte non ha fornito un valore utilizzabile. Non vuol dire che il sistema sia in buono stato.",
  stale: "Dato non aggiornato significa che il limite di freschezza della fonte è stato superato. Non posso presentarlo come corrente.",
  unavailable: "Non disponibile significa che la fonte o la proiezione non è raggiungibile o non contiene un dato utilizzabile.",
  partial: "Parziale significa che la fonte copre solo una parte del periodo o dei dati richiesti.",
  conflicting: "Conflittuale significa che le fonti riportano dati incompatibili. Non scelgo automaticamente un valore."
});

function response(speech, shouldEndSession = true) {
  return { version: "1.0", response: { outputSpeech: { type: "PlainText", text: speech }, shouldEndSession } };
}

function localDate(value) {
  const dateOnly = typeof value === "string" && /^\d{4}-\d{2}-\d{2}$/.test(value);
  const time = Date.parse(dateOnly ? value + "T12:00:00Z" : value);
  if (!Number.isFinite(time)) return null;
  return new Intl.DateTimeFormat("it-IT", dateOnly
    ? { timeZone: "UTC", dateStyle: "long" }
    : { timeZone: "Europe/Rome", dateStyle: "long" }).format(new Date(time));
}

function localDateTime(value) {
  const time = Date.parse(value);
  if (!Number.isFinite(time)) return null;
  return new Intl.DateTimeFormat("it-IT", { timeZone: "Europe/Rome", day: "numeric", month: "long", year: "numeric", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).format(new Date(time));
}

async function getSession(sources) {
  const result = await sources.getLatestSession();
  if (!result || result.state === "UNAVAILABLE") return "La fonte delle sessioni pubblicate non è disponibile.";
  if (result.state === "EMPTY") return "Non risultano sessioni pubblicate nel catalogo disponibile.";
  if (result.state !== "CURRENT" || !result.session) return "Non riesco a verificare una sessione pubblicata.";
  const date = localDate(result.session.observationDate);
  if (!date) return "La data della sessione pubblicata non è valida.";
  const target = result.session.target ? " L’oggetto pubblicato è " + result.session.target + "." : "";
  return "L’ultima sessione presente nel catalogo pubblicato risale al " + date + "." + target + " Fonte: catalogo scientifico pubblicato.";
}

export async function handleIntent(intentName, slots = {}, sources = {}) {
  switch (intentName) {
    case "GetObservatorySummary": {
      return response("La proiezione di riepilogo dell’osservatorio non è disponibile.");
    }
    case "GetLatestSession":
      return response(await getSession(sources));
    case "GetRecentAlerts": {
      const result = await sources.getRecentAlerts?.();
      if (!result || result.state === "UNAVAILABLE") return response("La fonte degli avvisi non è disponibile. Non posso confermare se ci siano avvisi.");
      if (result.state === "EMPTY") {
        const publishedAt = localDateTime(result.generatedAtUtc);
        return response(publishedAt
          ? "Non risultano avvisi registrati nella proiezione aggiornata il " + publishedAt + " ora locale."
          : "La proiezione non riporta avvisi ma manca un orario di pubblicazione verificato.");
      }
      return response("La fonte degli avvisi non usa un formato vocale approvato; non posso leggere i dettagli.");
    }
    case "ExplainStatus": {
      const code = String(slots.StatusCode?.value ?? slots.statusCode?.value ?? "").toLowerCase();
      const normalized = code.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z]/g, "");
      const map = { sconosciuto: "unknown", statosconosciuto: "unknown", datosconosciuto: "unknown", unknown: "unknown", stale: "stale", nonaggiornato: "stale", nonaggiornata: "stale", datononaggiornato: "stale", datononaggiornata: "stale", unavailable: "unavailable", nondisponibile: "unavailable", datonondisponibile: "unavailable", partial: "partial", parziale: "partial", datoparziale: "partial", conflicting: "conflicting", conflittuale: "conflicting", datoconflittuale: "conflicting" };
      const explanation = STATUS[map[normalized]];
      return response(explanation ?? "Non ho una spiegazione approvata per questo stato.");
    }
    case "ExplainUnavailableStatus":
      return response(STATUS.unavailable);
    case "GetWeatherForecast": {
      const hourSlot = slots.HourCount?.value ?? slots.hourCount?.value;
      const periodSlot = slots.Period?.value ?? slots.period?.value;
      const result = await sources.getForecast?.({
        period: hourSlot !== undefined ? "prossime ore" : periodSlot ?? "stanotte",
        hours: Number(hourSlot ?? 3)
      });
      if (!result) return response("La proiezione meteo non è disponibile.");
      return response(result.speech ?? "La proiezione meteo non è disponibile.");
    }
    case "UnsupportedCommandIntent":
      return commandBoundaryResponse();
    default:
      return response("Non ho capito la richiesta. Puoi chiedermi aiuto.");
  }
}

export function launchResponse() {
  return response("Benvenuto in Digital StarGate. Puoi consultare informazioni pubblicate dell’osservatorio. Che cosa vuoi sapere?", false);
}

export function helpResponse() {
  return response(HELP, false);
}

export function cancelResponse() {
  return response("Va bene, chiudo.");
}

export function commandBoundaryResponse() {
  return response("Posso consultare informazioni pubblicate, ma non posso comandare cupola, montatura o altri dispositivi, modificare o avviare attività. Non fornisco giudizi di sicurezza né esiti GO o NO-GO.");
}
