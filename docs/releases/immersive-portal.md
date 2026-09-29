# Immersive Portal — release candidate

| Campo | Valore |
|---|---|
| Identificativo | DSG-REL-IMMERSIVE-001 |
| Data | 29/09/2026 |
| Stato | Implemented candidate; non attestazione di deployment |
| Baseline verificata | `d0779f1d31f539cf45c0883c3d4bfca94dd6f301` |
| Ambito | Redesign visuale completo; nessuna modifica alla semantica dei dati |

## Esperienza realizzata

Il portale usa una shell comune per tutte le pagine Material. La home e 18 hub
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
| CI GitHub / ARB / Release Quality | Da verificare sul publication head; non dichiarate approvate da questo documento |
| Deployment Pages | Non attestato dal solo test locale |

## Limiti espliciti

- Modello 3D schematico, non rilievo as-built o digital twin.
- Il movimento è limitato agli input: nessun rendering perpetuo a pagina ferma.
- Verifica mobile emulata; misure termiche su hardware reale non eseguite.
- Nessuna nuova accettazione di BKL-043 o chiusura di BKL-050.
- Pubblicazione subordinata ai gate applicabili descritti nel Release Playbook.

## Rollback

Revert atomico del commit/PR di presentazione e rebuild Pages. Fonti scientifiche,
telemetria, policy, apparati e dataset non richiedono ripristino perché non modificati.
