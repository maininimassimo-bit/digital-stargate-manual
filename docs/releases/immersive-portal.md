# Immersive Portal — rilascio pubblicato

| Campo | Valore |
|---|---|
| Identificativo | DSG-REL-IMMERSIVE-001 |
| Data | 29/09/2026 |
| Stato | Pubblicato; limiti di verifica fisica e assistiva registrati |
| Baseline verificata | `d0779f1d31f539cf45c0883c3d4bfca94dd6f301` |
| Ambito | Redesign visuale completo; nessuna modifica alla semantica dei dati |

## Esperienza realizzata

La baseline del 29/09/2026 usa una shell comune per tutte le pagine Material. La home e 18 hub
integrano modelli Three.js procedurali: StarGate/atlante celeste oppure cupola e
strumentazione illustrativa. Tipografia, pannelli, tabelle, focus e navigazione
ricevono un trattamento coerente in light/dark. I manuali e le pagine di dettaglio
documentale restano leggibili senza scaricare il renderer.

Le viste dell'osservatorio sono controlli grafici: non aprono cupole, non puntano
telescopi e non indicano lo stato reale degli apparati. Il rendering non legge né
modifica la telemetria. Nessun dato dimostrativo è incluso nel sito integrato.

## Integrità dei contenuti

Una build della baseline e la prima build del redesign sono state confrontate con
`verify-immersive-content.py`: **828 pagine HTML esistenti** conservano testo,
binding `data-*`, anchor e link, escludendo il solo componente decorativo aggiunto.
Gli aggiornamenti tecnici successivi sono modifiche documentali intenzionali e
vengono esclusi esplicitamente dal confronto finale.

I consumer, valutatori, JSON, generatori di dati e workflow di pubblicazione
autorevoli non sono modificati. La home continua a leggere le projection originali;
il fallback della pagina status conserva gli stati UNKNOWN/STALE.

## Componenti e manutenzione

L'[implementazione tecnica](../ui/immersive-portal-implementation.md) documenta
template, moduli, mappa delle scene, limiti di rendering, versionamento vendor,
accessibilità, test e rollback. Three.js è fissato a 0.180.0 e servito localmente
dal sito; licenza MIT e manifest SHA-256 sono inclusi. Non vengono introdotti
GSAP, Spline o runtime server.

## Validation record

| Verifica | Evidence |
|---|---|
| Build baseline e redesign | `mkdocs build --strict --config-file mkdocs.pages.yml`, completate localmente |
| Preservazione contenuti | 828 pagine nella prima comparazione integrale, PASS |
| Browser regression | PASS locale Edge headless: 19 hub × 2 viewport (1440/390 px); temi, comandi visuali, persistenza/remount, ricerca/Escape, reduced-motion, WebGL bloccato, no-JS |
| Integrità vendor e presentation boundary | PASS locale: `verify-immersive-assets.mjs` |
| Gate esistenti | PASS locale: no-inline JS; ricerca (5 check); integrità 830 pagine; 14 test EAGLE/score; regression homepage; coerenza roadmap e Scientific Platform |
| CI GitHub | 22 check PR superati su `fb60018b5b14c3397bc51e869ac21cad6ca3bfbd`; workflow post-merge superati |
| ARB / Release Quality | Review AI-assistite in passaggi distinti, stesso assistente implementatore; nessuna approvazione umana indipendente dichiarata |
| Deployment Pages | Workflow autorevole completato sul merge `2ea44f897b22a675cb8fd7bfe00734d86eaf6ddc` |
| Verifica sito pubblico | PASS: 19 scene × 2 viewport, ricerca, controlli, essential/remount, reduced-motion, fallback; provider esterni bloccati durante il test, nessuna attestazione della loro disponibilità |

## Registro di pubblicazione

La [PR #429](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/429)
è stata integrata il 29/09/2026 dopo l'istruzione owner di procedere.
Il [verbale ARB/Release Quality](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/429#issuecomment-5893730865)
registra scope, disclosure della review, 22 check exact-head, branch zero behind,
rollback e applicazione di `W-DSG-AEM-RULESET-001`. Nessun Blocker/Major identificato.

Il [workflow Pages](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/36593414390)
ha pubblicato il merge `2ea44f897b22a675cb8fd7bfe00734d86eaf6ddc`.
L'evidence di verifica live e gli aggiornamenti documentali sono tracciati nella PR.
Le misure termiche su dispositivi fisici e l'audit assistivo completo rimangono
assegnati al gate futuro BKL-050; non sono dichiarati eseguiti o chiusi.

## Limiti espliciti

- Modello 3D schematico, non rilievo as-built o digital twin.
- Il movimento è limitato agli input: nessun rendering perpetuo a pagina ferma.
- Verifica mobile emulata; misure termiche su hardware reale non eseguite.
- Nessuna nuova accettazione di BKL-043 o chiusura di BKL-050.
- Pubblicazione subordinata ai gate applicabili descritti nel Release Playbook.

## Rollback

Revert atomico del commit/PR di presentazione e rebuild Pages. Fonti scientifiche,
telemetria, policy, apparati e dataset non richiedono ripristino perché non modificati.

## Incremento: cielo della notte nel Planner

Il simbolo della hero diventa un’immagine realistica selezionata dalla nuvolosità media e dalla pioggia previste nella finestra del Planner. Didascalia con valori, periodo e limiti illustrativi; fallback per dati indisponibili e immagine assente; nessun ulteriore rendering continuo. [Dettagli tecnici e test](../ui/planner-weather-sky.md). Evidenze esatte di CI e pubblicazione nella PR dedicata.

## Incremento: reperibilità delle pagine e atlante completo

Navigazione di sezione prima del contenuto su tutte le pagine; nuova mappa completa per ambito; menu laterale completato con sei destinazioni mancanti. L'audit di copertura verifica 831 pagine e impedisce che una pagina resti raggiungibile soltanto dal footer. La hero del Planner inquadra interamente il Celestial Atlas con spazio riservato ai controlli, anche su mobile. Dettagli e rollback nella guida di implementazione.


## Incremento: Roadmap compatta e Planner allineato

Stato progetto e target restano integrali in dettagli espandibili; schede package e milestone più compatte. Il progresso usa un indicatore prospettico leggero con percentuale e conteggi governati, senza duplicare la barra. Nel Planner cielo e atlante sono affiancati e allineati sotto l'introduzione, oppure impilati su mobile. [Implementazione e verifiche](../ui/immersive-portal-implementation.md). Nessuna variazione a dati, freshness, authority o policy; rollback tramite revert della PR e rebuild.

## Incremento: anteprime live Allsky Home e Status — 09/10/2026

La Home mostra il JPEG live Allsky al posto dello StarGate, con contenitore e badge preservati, pulsante Allsky e Vista essenziale. Observatory Status mantiene la cupola collegata al badge e aggiunge sotto l’anteprima Allsky; i due riquadri sono allineati alla colonna dei badge, con disposizione impilata su mobile. Immagine intera senza ritaglio, aggiornamento ogni 30 secondi e stati espliciti per pausa o collegamento indisponibile. L’ora di ricezione non equivale alla data di acquisizione. [Implementazione, manutenzione e rollback](../ui/immersive-portal-implementation.md#anteprime-allsky-nella-home-e-in-observatory-status-9-ottobre-2026).

| Incremento | Evidence pubblicata |
|---|---|
| Home | [PR #532](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/532), merge `e586c993297908b5c72a91210c64d172808653f1`; [Pages](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/37960111465) riuscito |
| Cupola e Allsky allineate in Status | [PR #533](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/533), merge `cba2d3a942fd5b1608a95bc42bbd2ba736bf9cbe`; [Pages](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/37962809653) riuscito |
| Coerenza degli asset in cache | [PR #535](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/535), merge `e895b7febadf132b8a0bee31582a35c5d8e77f8b`; [Pages](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/37964637276) riuscito |

I check richiesti sui rispettivi head e i workflow post-merge sono riusciti. I test browser usano fixture e bloccano provider esterni; il riscontro successivo sul sito pubblico ha verificato separatamente il JPEG reale 1936 × 1096 e l’allineamento in Status. La verifica live ha rilevato la cache di asset precedenti: la PR #535 ha corretto il problema tramite riferimenti di versione, verificati anche nella scheda già aperta.

Le modifiche sono di presentazione read-only: non cambiano telemetria, policy di freshness, autorità safety o configurazioni dell’Allsky. La disponibilità osservata del JPEG non costituisce un monitoraggio continuo o una conferma della sicurezza del cielo. Restano i limiti di collaudo fisico e assistivo della baseline.
