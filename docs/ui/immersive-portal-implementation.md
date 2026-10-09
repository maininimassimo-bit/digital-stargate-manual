# Portale immersivo — implementazione tecnica

| Campo | Valore |
|---|---|
| Identificativo | DSG-UI-IMMERSIVE-001 |
| Versione | 1.1 |
| Data | 09/10/2026 |
| Stato | Pubblicato — evidence e limiti nelle note di rilascio |
| Richiesta | Redesign completo del portale, mantenendo dati e contenuti, con aggiornamento tecnico |
| Baseline iniziale | `d0779f1d31f539cf45c0883c3d4bfca94dd6f301` |
| Boundary | Presentazione read-only; fonti pubbliche esistenti, nessuna modifica a policy, autorità o comandi |

## 1. Ambito realizzato

La nuova presentazione si applica a tutte le pagine generate da Material tramite
`overrides/main.html`. Non sostituisce il motore MkDocs né duplica le pagine in
HTML standalone. I capitoli, gli ADR, i runbook, le tabelle e le superfici generate
dalla pipeline mantengono URL, testo, anchor e binding originali.

Il CSS condiviso aggiorna tipografia, superfici, bordi, gerarchie, navigazione
laterale, focus, tabelle e card in entrambi i temi. I 19 hub selezionati integrano
un riquadro visuale: la Home usa ora la ripresa Allsky, gli altri hub una scena WebGL. Le pagine documentali mantengono la navigazione laterale e non
caricano Three.js. La sidebar primaria dei soli hub è sostituita visivamente dalla
navigazione globale già esistente; drawer, ricerca e indice restano disponibili.

## 2. Mappa delle scene

| Pagina | Rappresentazione |
|---|---|
| Home | Anteprima JPEG live Allsky; contenitore e badge originali preservati |
| Stato osservatorio | Cupola schematica collegata al badge; anteprima live Allsky in un secondo riquadro sotto |
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
| `docs/javascripts/allsky-live-preview.js` | Anteprima pubblica Allsky, refresh, errori, pausa e lifecycle |
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
node .github/scripts/test-allsky-live-preview.cjs
node .github/scripts/test-status-allsky-layout.cjs
node .github/scripts/test-immersive-dome-sync.cjs
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
Mantenere una sola scena WebGL per pagina; la seconda superficie Allsky di Status è un’immagine HTML e non una seconda scena WebGL. Le pagine senza marker restano editoriali.

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

### Vista cupola collegata al badge (29/09/2026)

Su richiesta owner, soltanto in Observatory Status il modello osservatorio segue
il badge **Cupola osservata** già visualizzato. CLOSED seleziona l'esterno con
copertura e pareti opache chiuse; OPEN seleziona l'interno schematico in sezione.
UNKNOWN, stato assente o diverso da OPEN/CLOSED selezionano una vista neutra,
senza cupola o strumenti rappresentati come correnti. Non si simula una posizione
fisica misurata e non viene inviato alcun comando.

`status-dome-view.js` osserva il testo del badge e pubblica soltanto il preset
`data-dsg-observed-dome` sul contenitore visuale. Non esegue fetch, non modifica
il badge e non interpreta un secondo payload. `immersive-renderer.mjs` osserva
quel metadato, aggiorna la vista e ridisegna; observer e listener sono rilasciati
con la scena. La preferenza essenziale conserva il collegamento testuale e, alla
riattivazione, usa lo stato corrente. Operations mantiene le viste illustrative.

I pulsanti Interno/Esterno/Dall'alto consentono un'esplorazione dichiarata
**Vista libera**. **Segui badge** torna alla selezione automatica. Un cambio
semantico del badge ripristina automaticamente la vista collegata; un refresh
con lo stesso stato non interrompe l'esplorazione manuale.

`test-immersive-dome-sync.cjs` intercetta risposte sintetiche e verifica CLOSED →
OPEN → stale/UNKNOWN, stato intermedio, vista libera/automatica, refresh invariato,
riattivazione dopo vista essenziale, navigazione e mobile. I fixture non sono
pubblicati come dati. CI, review AI-assistita e verifica Pages sono registrate
nella PR di integrazione. Rollback: revert dell'incremento e rebuild Pages dalla
baseline `d7b3ab57747d670221f72ae37fdf566a19a07619`.

### Estensione dei pannelli status

I quadranti e simboli dei tre pannelli sono documentati in
[DSG-UI-INSTRUMENTS-001](digital-status-instruments.md), inclusi scale,
normalizzazione UNKNOWN, lifecycle dei canvas e suite di regressione.
La preferenza di vista essenziale è condivisa con la hero.

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 29/09/2026 | Shell comune, 19 scene, dipendenza locale, lifecycle e piano di regressione |

## Cielo atmosferico del Planner

La hero integra un [cielo illustrativo basato sul forecast notturno](planner-weather-sky.md), con tre asset locali, dati F9 già verificati, scadenza automatica e fallback neutro.

## Navigazione per sezione e mappa completa

L'audit del 29/09/2026 sul portale aggiornato verifica 831 pagine HTML documentali. Il menu grafico precedente ometteva sei destinazioni di primo livello ora reinserite: Galleria immagini, Dettaglio sessione, Observation Planner, AI Observatory Assistant, AI Post-Processing Assistant e Scientific Intelligence. Report delle sessioni era nel menu laterale, ma poco visibile dal percorso Scienza: ora figura esplicitamente nei collegamenti della sezione insieme al Catalogo sessioni.

`partials/section-navigation.html` inserisce prima del contenuto i collegamenti del gruppo MkDocs corrente: fino a sei voci immediatamente visibili, altre espandibili. Le sottosezioni mantengono la loro gerarchia. Ogni pagina offre inoltre [Mappa completa del portale](../portal-map/index.md), raggiungibile anche dal menu laterale. Funziona senza JavaScript.

La mappa usa il `nav` canonico e `hooks/portal_navigation.py` per includere anche i documenti non presenti in nav, raccolti per ambito (report individuali, architettura, governance, manuali, interfaccia, sviluppo, rilasci). Il catalogo è generato al build da tutte le pagine documentali: nessun inventario manuale da sincronizzare né richiesta runtime. I link precedente/successivo restano disponibili come comodità, non come unico ingresso.

`verify-immersive-navigation.py` controlla ogni pagina generata: presenza nella mappa, destinazioni risolte e navigazione prima del contenuto. `test-immersive-navigation.cjs` verifica i due esempi Owner, gruppi espandibili, mobile e navigazione senza JavaScript. I documenti sono reperibili per appartenenza al gruppo, senza alterarne stato, autorevolezza o contenuto.

## Inquadratura completa del Celestial Atlas

La distanza della camera usa il campo visivo più restrittivo fra verticale e orizzontale, con un volume conservativo di raggio 5 unità per l'atlante. Lo scroll varia la distanza mantenendo un margine di contenimento. Il canvas delle scene atlas/gateway occupa esclusivamente lo spazio fra intestazione e controlli. Nel Planner l'introduzione occupa la prima riga; cielo previsto e atlante sono affiancati con altezza condivisa (minimo 26 rem). Fino a 700 pixel si dispongono in sequenza e l'atlante ha altezza 28 rem. Il modello osservatorio e il collegamento al badge cupola non cambiano.

Verificati viewport 390, 768, 1157 e 1440 pixel, preset Orbita/Dall'alto e ridimensionamento; ispezione delle immagini con anello completo. Rimangono i limiti di pixel e l'arresto del rendering a riposo. Rollback: revert della PR di navigazione/inquadratura e rebuild; nessuna modifica ai dati. CI, review e pubblicazione sono registrate nella PR dedicata.


## Roadmap compatta e allineamento Planner — 29/09/2026

La Roadmap usa una hero a larghezza piena, identificativi sintetici del package e della prossima milestone, seguiti da `details` nativi per stato progetto e target integrali. Anche le note dei package e degli elementi aperti sono espandibili: nessuna nota è troncata, riscritta o rimossa. Le wave hanno due colonne su desktop e una su mobile; lo storico usa righe compatte con anteprima laterale. La legenda e le etichette testuali mantengono comprensibili gli stati senza dipendere dal colore.

Il precedente donut e la barra duplicata sono sostituiti da un indicatore prospettico CSS, senza nuove dipendenze, canvas o animazioni continue. Percentuale e conteggi conservano la priorità di `data.summary`, con il precedente fallback sui conteggi delle wave. Le larghezze verde/azzurro/ambra sono proporzionali a completati/in corso/pianificati sul totale; le tacche sono una scala percentuale, non singoli package. Il componente espone `role=meter`, valore e descrizione testuale dei conteggi. Non misura readiness o avanzamento fisico degli apparati.

Nel Planner i bordi del cielo previsto e del Celestial Atlas sono allineati sotto l'introduzione. Il ResizeObserver esistente adatta il canvas anche quando si espandono i dettagli del meteo. Restano invariati il contenimento del globo, i controlli visivi, il refresh F9 e la scadenza dei dati.

File: `docs/styles/roadmap.css`, `docs/javascripts/roadmap.js`, le due pagine Markdown e `docs/styles/planner-weather-sky.css`. Il test `test-immersive-compact-layout.cjs` confronta titoli, stati, note e summary con la projection, verifica apertura da tastiera, overflow a 390/768/1157/1440 pixel e allineamento del Planner. La suite di navigazione verifica separatamente canvas e controlli. Temi chiaro/scuro e screenshot sono verificati in browser; non equivale a un audit assistivo completo. Nessuna modifica alla canonical source o alla projection roadmap. Rollback: revert della PR di presentazione e rebuild Pages; CI, review e pubblicazione nella PR.

## Anteprime Allsky nella Home e in Observatory Status — 9 ottobre 2026

La Home sostituisce il modello StarGate della hero con la ripresa pubblica Allsky, mantenendo dimensioni originali del contenitore, font e stile del badge. Il pulsante **Allsky** apre il sito completo in una nuova scheda; **Dall’alto** è rimosso soltanto dalla Home. La Home non importa il renderer WebGL per questa anteprima.

In Observatory Status, `.dsg-status-overview` affianca il gruppo di otto badge a `.dsg-status-visuals`: cupola ridimensionata sopra e Allsky sotto. I due riquadri hanno la stessa larghezza; la sommità della cupola e il fondo dell’Allsky coincidono con i bordi del gruppo badge. La griglia usa due righe di altezza uguale, con minimo 20 rem, distanziate di 1 rem. Fino a 850 px i badge precedono i due pannelli impilati, alti 22 rem ciascuno. Il canvas della cupola occupa soltanto lo spazio tra titolo e controlli. Il collegamento a **Cupola osservata**, le viste libere e gli stati UNKNOWN/STALE restano quelli documentati sopra.

Il marker `<!-- DSG:ALLSKY-PREVIEW -->` compone la seconda superficie in Status. Il partial riusa il componente della Home con `status_preview`; il pannello Allsky non espone `data-dsg-scene`, preservando un solo bootstrap WebGL. Il controllo `data-dsg-allsky-mode` condivide la preferenza `dsg-immersive-essential` e l’evento `dsg:visual-mode-change` con cupola e strumenti.

La sorgente è il JPEG pubblico HTTPS `https://digitalstargate.freeddns.it:23232/current/image.jpg`, senza credenziali. L’immagine usa `object-fit: contain`, senza ritaglio. Non è uno stream video continuo: il browser richiede un nuovo fotogramma ogni 30 secondi dopo la ricezione precedente. **Ultima ricezione** indica l’ora del browser; non certifica la data di acquisizione, riportata nell’overlay del fotogramma. L’anteprima non è un indicatore di safety né di freshness della telemetria.

**Vista essenziale** sospende il refresh e mantiene l’ultima immagine ricevuta, se disponibile; **Attiva il live** lo riprende. La preferenza persiste tra pagine. Una scheda nascosta sospende le richieste; il cambio pagina rilascia timer e listener. Un errore di caricamento nasconde l’immagine e mostra uno stato esplicito con riprova automatica; un timeout di 15 secondi segnala l’aggiornamento non disponibile, senza attestare come corrente un nuovo fotogramma.

CSS, bootstrap, script Allsky e import del renderer usano il riferimento di versione `status-allsky-20261009`. Aggiornare questo riferimento quando cambiano asset coordinati: una scheda può altrimenti combinare HTML nuovo con CSS o controlli precedenti in cache. Non riguarda la cache dei contratti o dei dati governati.

Verifiche: build strict; test di contenimento e allineamento a 1440/1007/768/390 px; refresh, preferenza persistente, errore/ripristino e teardown con fixture; regressione della cupola OPEN/CLOSED/UNKNOWN e degli altri hub. La verifica pubblica nel browser ha confermato immagine reale 1936 × 1096, stato ready, contenimento e allineamento. Evidence e commit sono nelle [note di rilascio](../releases/immersive-portal.md#incremento-anteprime-live-allsky-home-e-status-09102026).

Rollback: revert delle PR Home/Status/cache nell’ordine inverso e rebuild Pages. Nessun ripristino di immagini, telemetria o configurazioni degli apparati è richiesto.
