# Portale immersivo — implementazione tecnica

| Campo | Valore |
|---|---|
| Identificativo | DSG-UI-IMMERSIVE-001 |
| Versione | 1.0 |
| Data | 29/09/2026 |
| Stato | Pubblicato — evidence e limiti nelle note di rilascio |
| Richiesta | Redesign completo del portale, mantenendo dati e contenuti, con aggiornamento tecnico |
| Baseline | `d0779f1d31f539cf45c0883c3d4bfca94dd6f301` |
| Boundary | Presentation-only; nessuna nuova fonte, policy, autorità o comando |

## 1. Ambito realizzato

La nuova presentazione si applica a tutte le pagine generate da Material tramite
`overrides/main.html`. Non sostituisce il motore MkDocs né duplica le pagine in
HTML standalone. I capitoli, gli ADR, i runbook, le tabelle e le superfici generate
dalla pipeline mantengono URL, testo, anchor e binding originali.

Il CSS condiviso aggiorna tipografia, superfici, bordi, gerarchie, navigazione
laterale, focus, tabelle e card in entrambi i temi. I 19 hub selezionati integrano
una scena WebGL. Le pagine documentali mantengono la navigazione laterale e non
caricano Three.js. La sidebar primaria dei soli hub è sostituita visivamente dalla
navigazione globale già esistente; drawer, ricerca e indice restano disponibili.

## 2. Mappa delle scene

| Pagina | Rappresentazione |
|---|---|
| Home | StarGate: anelli solidi, globo di particelle, orbite, halo procedurale |
| Stato osservatorio | Cupola, basamento, montatura, tubo ottico e camera schematici |
| Operations | Modello illustrativo dell'osservatorio |
| Mission Control, Analytics, Architettura, Documentazione | Atlante celeste illustrativo |
| Catalogo e dettaglio sessioni, Scientific Image Gallery, Scientific Platform, Scientific Intelligence | Atlante celeste illustrativo |
| Observation Planner, Session Comparison, Scientific Data Quality, Equipment Performance, Anomaly & Trend | Atlante celeste illustrativo |
| AI Post-Processing Assistant, BKL-042 Advisory | Atlante celeste illustrativo |
| Altre pagine, manuali, governance, roadmap, report | Shell editoriale condiviso, senza contesto WebGL aggiuntivo |

La mappa eseguibile è nel template. Nei sorgenti degli hub il commento
`<!-- DSG:IMMERSIVE-SCENE -->` indica esclusivamente il punto di composizione;
la build lo sostituisce con il partial. Non è un binding dati. I blocchi generati
`DSG:AUTO-HOMEPAGE` non vengono modificati.

## 3. Componenti e responsabilità

| File | Responsabilità |
|---|---|
| `overrides/main.html` | Estensione di `base.html`, preserva `super()`, applica shell e composizione |
| `overrides/partials/immersive-scene.html` | Canvas decorativo, etichette, poster statico, controlli accessibili |
| `docs/styles/immersive-portal.css` | Sistema visuale condiviso, responsive, light/dark, stampa |
| `docs/javascripts/immersive-portal.js` | Bootstrap idempotente, lazy load, preferenze e lifecycle |
| `docs/javascripts/immersive-renderer.mjs` | Renderer, camera, input, osservatori, limiti GPU, disposal |
| `docs/javascripts/immersive-gateway.mjs` | Geometria procedurale dello StarGate/atlante |
| `docs/javascripts/immersive-observatory.mjs` | Geometria procedurale dell'osservatorio |
| `docs/assets/vendor/three-0.180.0/` | Dipendenza bloccata e servita dallo stesso sito, licenza e hash |

L'adattamento in `page-enhancements.js` consente al breadcrumb esistente di trovare
l'H1 dentro la nuova shell; l'inserimento usa il parent dell'heading. La logica
tema resta di esclusiva competenza di `dsg-theme-manager.js`.

## 4. Dati e autorità

I moduli `immersive-*` non effettuano fetch e non leggono né modificano i binding
`data-observatory-status`, `data-eagle-health`, `data-bkl036-score` o le projection
scientifiche. Le importazioni di moduli sono caricamenti di asset statici, non
richieste a fonti operative.

Restano invariati:

- sorgenti relay/fallback, cadenze e valutatori di freshness;
- regole UNKNOWN/STALE/UNAVAILABLE e Health Score;
- Scientific Data Engine, cataloghi, lineage e provenance;
- separazione realtime/storico e boundary di safety;
- autenticazione, provider, pipeline e publish set dei dati.

Non viene portata in produzione alcuna fixture dei prototipi standalone.
Il modello è **illustrativo**, non un digital twin né una rappresentazione della
posizione o dell'apertura reale della cupola. “Strumenti”, “Esterno” e “Dall'alto”
modificano solo camera/materiali. Lo StarGate non è una mappa astrometrica.

## 5. Caricamento, prestazioni e accessibilità

Three.js 0.180.0, MIT, è vendorizzato in due moduli minificati: circa 720 KB
complessivi non compressi, oltre alla licenza e al manifest. Il browser non
dipende da una CDN esterna. I percorsi si risolvono rispetto al modulo, quindi
funzionano sotto `/digital-stargate-manual/` e nei deep link.

Il bootstrap è leggero e caricato globalmente. Il renderer viene importato solo
quando la pagina contiene una scena e non sono attivi reduced-motion,
Save-Data o la preferenza essenziale. I moduli di geometria sono importati per tipo.

- DPR massimo 1 desktop/touch compatto e 1,5 desktop ordinario; budget 1,5 MP.
- Rendering a richiesta: stop dopo 850 ms senza input; niente loop perpetuo.
- Pausa quando scena fuori viewport o tab nascosta.
- Geometrie condivise/istanziate dove applicabile; niente post-processing fullscreen.
- Reduced-motion o Save-Data: poster CSS, nessun primo download WebGL.
- Preferenza `dsg-immersive-essential` in localStorage; errori storage tollerati.
- Teardown su cambio pagina e modalità: abort, timer, observer, geometrie/materiali,
  renderer e perdita esplicita del contesto rilasciato.
- Controlli HTML con focus, stato `aria-pressed` e dimensione minima 44 px.
- Canvas decorativo `aria-hidden`; nessuna informazione primaria disponibile solo in 3D.
- Puntatore nativo preservato; reticolo magnetico soltanto sulle sei card della home.
- JavaScript/WebGL assenti: poster e contenuti originali restano disponibili.
- Il renderer è escluso dalla stampa.

Non sono introdotti GSAP, Spline o servizi nuovi: per questa implementazione
l'interpolazione nativa è sufficiente. Cambi della preferenza riduzione movimento
e navigazione Material `document$` sono supportati; `navigation.instant` non viene
abilitata dalla presente modifica.

## 6. Verifica e manutenzione

Gate locali e di CI:

```sh
node .github/scripts/verify-immersive-assets.mjs
node .github/scripts/verify-no-inline-portal-js.mjs
node .github/scripts/verify-portal-search.mjs
python -m mkdocs build --strict --config-file mkdocs.pages.yml
python .github/scripts/verify-published-site.py --site site --base-path /digital-stargate-manual/
node .github/scripts/test-immersive-portal.cjs
```

Il browser test richiede Playwright 1.62.1 e un server locale. Impostare
`DSG_TEST_BASE_URL`; opzionalmente `DSG_BROWSER_CHANNEL=msedge` per Edge installato.
I provider esterni vengono bloccati nel test: non occorrono credenziali o accesso
agli apparati. Il workflow `portal-immersive-validation.yml` esegue build, integrità
asset e browser regression e non pubblica il sito.

Per confrontare contenuti, anchor, link e binding con una build precedente:

```sh
python .github/scripts/verify-immersive-content.py --baseline /path/to/baseline-site --site site
```

Escludere esplicitamente soltanto i documenti tecnici aggiornati intenzionalmente.
I test del consumer EAGLE e dello score restano quelli esistenti: il visual layer
non li sostituisce. Evidence e limiti di verifica sono registrati nelle
[note di rilascio](../releases/immersive-portal.md).

## 7. Estensione e rollback

Per abilitare una nuova scena, aggiungere la pagina alla mappa del template e il
marker al suo hero, senza collocarlo in contenuto rigenerato automaticamente.
Mantenere una sola scena per pagina. Le pagine senza marker restano editoriali.

Per aggiornare Three.js sostituire entrambi i moduli dalla stessa versione,
conservare MIT, aggiornare il manifest SHA-256 e ripetere i test browser/fallback.

Rollback: revert atomico del commit/PR di presentazione e nuova build con il
workflow Pages esistente. Non ripristinare o modificare projection, dataset,
runtime EAGLE o configurazioni dell'osservatorio. La preferenza localStorage
residua è innocua.

## 8. Limiti e gate di rilascio

La pubblicazione e le review AI-assistite sono registrate nelle
[note di rilascio](../releases/immersive-portal.md). Non sono dichiarate
approvazioni umane indipendenti o verifiche fisiche degli apparati. Il testing headless
non sostituisce misure termiche su smartphone reali o un audit assistivo completo.
La modifica non chiude BKL-043 né anticipa la closure complessiva di BKL-050.
ARB/Release Quality ed exact-head CI restano gate applicabili alla pubblicazione.

## 9. Revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 29/09/2026 | Shell comune, 19 scene, dipendenza locale, lifecycle e piano di regressione |
