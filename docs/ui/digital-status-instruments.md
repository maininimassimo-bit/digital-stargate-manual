# Strumenti digitali di Observatory Status

| Campo | Valore |
|---|---|
| Identificativo | DSG-UI-INSTRUMENTS-001 |
| Data | 29/09/2026 |
| Ambito | Presentazione read-only di EAGLE, meteo e sistemi osservati |
| Baseline di rollback | `117786f913f508268be0c1bb308ef412c2c7e522` |

## Esperienza e dati

Su richiesta owner, i tre pannelli di Observatory Status sostituiscono le barre
con quadranti 3D per le grandezze numeriche e simboli schematici per gli stati.
Sono 17 schede: sei EAGLE, sei meteo e cinque sistemi, inclusa la rete.
Le etichette, i valori, le unità, le regole e le indicazioni di disponibilità
restano testo HTML accessibile. I controlli visuali non comandano apparati.
La cupola OPEN/CLOSED è un simbolo dello stato dichiarato, non un digital twin;
montatura e camera non rappresentano orientamento o posa fisica.

Il consumer `observatory-status.js` continua a usare i trasporti esistenti.
Le soglie BKL-036-F5 e BKL-032 non cambiano, né vengono modificati evaluator,
Health Score, JSON sorgenti, contratti pubblici, provider o Safety Authority.
Nessun valore degli esempi visuali è copiato nella produzione.

## Scale e stati

| Grandezza | Scala grafica | Soglia governata |
|---|---|---|
| CPU | 0–100% | massimo 90% |
| Memoria disponibile / dischi liberi | 0–100% | minimo 20% |
| Vento / raffiche | 0–30 / 0–40 km/h | massimo 15 / 20 km/h |
| Nuvolosità / umidità | 0–100% | massimo 50 / 90% |
| Margine dew point | 0–20 °C | maggiore di 3 °C |
| Pioggia | 0–1 mm/h | zero; positivo degradato |

Le scale sono esclusivamente grafiche: il numero effettivo resta visibile anche
fuori scala. La tacca ambra indica la soglia; verde/rosso sono accompagnati da
testo. UNKNOWN usa un simbolo interrotto e nessuna percentuale.
Uptime e Windows Time sono indicatori descrittivi, non quadranti numerici.

La revisione corregge incongruenze delle barre precedenti: `null`, stringhe vuote
e valori mancanti non diventano zero; sistemi e uptime scaduti diventano UNKNOWN;
un envelope EAGLE scaduto non mantiene quadranti correnti; evidence EAGLE invalida
o indisponibile non resta nella cache dei pannelli. Envelope osservatorio scaduto
o qualità dei sistemi non CURRENT sopprimono lo stato corrente nei simboli.
C: e D: assenti rimangono
esplicitamente UNKNOWN. Le policy numeriche restano invariate.

## Moduli e lifecycle

- `observatory-status.js`: normalizzazione, valutazione esistente e markup con
  metadati `data-instrument-*`. WeakMap evita sostituzioni identiche del DOM.
- `status-instruments.js`: enhancement della sola pagina status; import quando
  un pannello entra in vista, sincronizzazione della vista essenziale con la hero,
  riconciliazione quando il consumer sostituisce i pannelli.
- `immersive-instruments.mjs`: Three.js locale già versionato, nessun fetch di
  telemetria. Un canvas per pannello, scissor viewport per ciascuna scheda.
- `status-instruments.css`: schede responsive, poster statici e temi chiaro/scuro.

Al massimo tre contesti aggiuntivi; ciascuno limita il buffer a 650.000 pixel e
DPR ≤ 1. Antialias solo con puntatore fine. Nessun loop di rendering continuo:
ridisegno su resize, ingresso in vista e input; stop su scheda nascosta/offscreen.
Geometrie, materiali, contesti, observer e listener sono rilasciati su sostituzione
dei pannelli, cambio pagina o modalità. Le importazioni tardive sono annullate.

Il tasto Vista essenziale condivide `dsg-immersive-essential` con la hero tramite
l'evento locale `dsg:visual-mode-change`. Reduced-motion e Save-Data evitano il
caricamento. Errore WebGL o context loss mantengono numeri e poster; senza JS il
messaggio statico dichiara i valori indisponibili. La stampa esclude i canvas.

## Verifiche e rilascio

`test-immersive-instruments.cjs` usa esclusivamente risposte sintetiche intercettate
nel browser, mai pubblicate come telemetria: valori correnti, zero/null, soglie
limite, fuori scala, scadenza, indisponibilità, refresh, fallback, mobile,
vista essenziale e smontaggio. Nessuna richiesta di test raggiunge il relay.
Il workflow Immersive portal validation esegue questa suite dopo la regressione
dei 19 hub; restano applicabili i test EAGLE/score e il build strict/integrità link.

Evidence di review AI-assistita, exact-head CI, expected-head merge e verifica
Pages vengono registrate nella PR di integrazione. La presenza di questo
documento non prova un deployment. Misure termiche fisiche e audit assistivo
completo rimangono nel gate BKL-050; non ne viene dichiarata la chiusura.

Rollback: revert del commit di integrazione e rebuild tramite `deploy-pages.yml`.
Nessuna migrazione o ripristino dei dati scientifici/operativi.
