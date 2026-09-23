# BKL-050 — Final Portal Quality and Accessibility Acceptance

| Campo | Valore |
|---|---|
| Stato | Planned |
| Priorità | P2 come programmazione; i difetti confermati manterranno la propria severità operativa |
| Owner e accountable | Massimo Mainini |
| Approvazione del piano | 23/09/2026, approvazione esplicita dell'owner dopo l'audit del portale |
| Autorità roadmap | `.github/roadmap/roadmap-source.json`, milestone `M-BKL050-FINAL-PORTAL-QUALITY` |
| Ordine | **Ultima milestone da completare** dopo BKL-042, BKL-043, BKL-049 e le altre attività aperte approvate nella roadmap |
| Data obiettivo | Da concordare; nessuna data di completamento dedotta dalla data di approvazione |

## Obiettivo e perimetro

Completare la verifica finale del portale Digital StarGate, correggere i problemi confermati e ottenere un'accettazione supportata da evidenze su disponibilità, sicurezza, dati, performance, accessibilità, resa sui dispositivi, usabilità e indicizzazione. La milestone è pianificata e non modifica lo stato del package corrente BKL-042. La chiusura di BKL-050 avverrà soltanto dopo la chiusura delle altre attività approvate e dopo la verifica delle correzioni sul portale pubblicato.

Il lavoro sul portale mantiene `command_authority=NONE` e `safety_authority=NONE`. Ogni modifica rimane nel perimetro di presentazione, pubblicazione, osservabilità e consumer read-only; command path, broker, scheduler decisionale, remediation automatica e Safety Authority sono esclusi. Qualsiasi modifica a un servizio runtime richiede il proprio gate, separato da questa pianificazione.

## Evidenza iniziale dell'audit del 23/09/2026

- Cinque pagine principali e i relay Status/EAGLE Health hanno risposto correttamente nel campione; il campione non misura l'uptime storico.
- Il sitemap contiene 793 URL HTTPS univoci, tutti raggiungibili; canonical coerenti, nessun `noindex` e nessuna immagine senza `alt` nella scansione HTML. I 20 download PDF/CSV individuati rispondono `200`.
- `Strict-Transport-Security` era presente; `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options` e `Referrer-Policy` non erano presenti nelle cinque risposte HTML campionate.
- Il portale non pubblica `robots.txt` al percorso del progetto. Sono stati rilevati 404 titoli oltre 60 caratteri e 789 descrizioni duplicate.
- PageSpeed Insights ha restituito `429`: LCP, INP e CLS non sono ancora stati misurati. Nessuna attestazione WCAG AA, EAA, cross-device o di UX quantitativa deriva dal campione iniziale.
- La persistenza dei dati dopo riavvio e la continuità dei relay richiedono evidenze aggiuntive; lo snapshot read-only corrente esponeva correttamente anche gli stati `UNKNOWN`.

Questi risultati sono una baseline di pianificazione, non attestano una conformità già ottenuta. Ogni difetto sarà rivalutato su una build aggiornata prima dell'intervento.

## Piano di lavoro approvato

| Ordine interno | Attività | Evidenza di completamento |
|---|---|---|
| 1 | Disponibilità e sicurezza: storico uptime/latency, controllo degli header; progettazione e verifica progressiva delle policy compatibili con risorse e integrazioni del portale. | Misure ripetibili, policy approvate, header verificati sulle risposte pubbliche, assenza di regressioni funzionali. |
| 2 | Dati dinamici: mappa API/feed/proiezioni, freshness e fallback; test di coerenza tra fonte e vista, persistenza dove applicabile e comportamento fail-closed. | Tracce di test per dato corrente, scaduto e non disponibile; provenienza documentata, nessuna trasformazione di `UNKNOWN` in stato corrente. |
| 3 | Performance: baseline Lighthouse mobile/desktop e Core Web Vitals LCP, INP, CLS con dati real-user quando disponibili; ottimizzazioni sulle pagine principali. | Protocollo di misura ripetibile, valori iniziali e finali, obiettivi di accettazione concordati con il team. |
| 4 | Accessibilità: audit WCAG 2.2 AA automatico e manuale, tastiera, screen reader, focus, ARIA, contrasto dei temi chiaro/scuro, zoom/reflow, moduli e PDF; valutazione dell'applicabilità EAA. | Registro dei criteri A/AA con difetti, correzioni e retest; documenti verificati; valutazione legale dell'applicabilità separata dal collaudo tecnico. |
| 5 | Device/browser e UX: desktop standard/alta risoluzione, tablet portrait/landscape, smartphone iOS/Android, browser principali; menu e componenti dinamici; task utente e attriti. | Matrice di prova, risultati per breakpoint/browser, task e tempi misurati con metodo e consenso appropriati. |
| 6 | Indicizzazione e link: `robots.txt`, sitemap, canonical, title, meta description, `noindex`, link interni/esterni e reindirizzamenti necessari. | Crawl finale senza errori confermati, metadata revisionati sulle pagine prioritarie, nessuna esclusione accidentale. |

La sequenza interna è una proposta di esecuzione approvata. Le criticità alte che dovessero emergere durante il lavoro richiedono trattamento secondo la severità, senza attendere la chiusura formale della milestone finale.

## Gate di avvio e chiusura

**Avvio:** le altre attività approvate della roadmap sono chiuse o è registrata una decisione esplicita di Massimo Mainini che ne ridefinisce il rapporto con la milestone finale; baseline e matrice dei test sono aggiornate. L'approvazione della roadmap autorizza la pianificazione, non certifica il risultato dei test futuri.

**Chiusura:** ogni area del piano ha evidenze ripetibili, problemi confermati risolti o eccezioni esplicitamente accettate, controlli locali e GitHub Actions pertinenti riusciti, verifica sul sito pubblicato in entrambi i temi e sui dispositivi/browser concordati, e accettazione finale dell'owner. Lo stato passerà a `completed` soltanto dopo queste evidenze.

La canonical roadmap source resta l'autorità; `docs/data/roadmap.json` e `docs/data/scientific-platform-status.json` sono proiezioni generate e devono rimanere coerenti con essa.
