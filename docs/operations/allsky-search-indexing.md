---
title: Allsky e portale · indicizzazione Google
description: Configurazione tecnica dei metadati, delle sitemap e di Google Search Console per il portale Digital Stargate e il sito Allsky pubblico.
---

# Allsky e portale: indicizzazione Google

**Data configurazione:** 09/10/2026. La pubblicazione e la richiesta di scansione rendono i contenuti disponibili ai motori di ricerca; non certificano l’avvenuta indicizzazione né una posizione nei risultati.

## Pagine e indirizzi di riferimento

| Contenuto | URL canonico |
|---|---|
| Portale | `https://maininimassimo-bit.github.io/digital-stargate-manual/` |
| Presentazione Allsky | `https://maininimassimo-bit.github.io/digital-stargate-manual/allsky/` |
| Sito Allsky completo | `https://digitalstargate.freeddns.it:23232/allsky/` |

La [pagina Allsky](../allsky/index.md) aggiunge testo HTML descrittivo, anteprima live e collegamenti alle gallerie. È raggiungibile dalla Home e dalla navigazione Osservatorio. Riutilizza il componente delle anteprime esistenti: aggiornamento ogni 30 secondi, ridimensionamento senza taglio, Vista essenziale e gestione dell’indisponibilità. Il timestamp fotografico resta distinto dall’ora di ricezione nel browser.

La Home mantiene la hero e usa un titolo descrittivo, evitando la precedente duplicazione del nome del sito. MkDocs genera descrizioni, indirizzi canonici e sitemap dal `site_url` di `mkdocs.pages.yml`. La sitemap del portale è `https://maininimassimo-bit.github.io/digital-stargate-manual/sitemap.xml` e comprende la nuova pagina Allsky.

## Metadati del sito Allsky

In `/home/pi/allsky/html/allsky/index.php` sono impostati lingua italiana, titolo **Allsky live a Manciano | Digital Stargate**, descrizione standard, canonical e metadati Open Graph coerenti con il sito pubblico. L’immagine condivisa è l’URL assoluto `/current/image.jpg`. Il titolo della scheda è distinto dall’intestazione visibile della pagina.

Il sito live è dinamico; il testo divulgativo stabile della pagina nel portale permette di descrivere il progetto anche senza caricare la ripresa. I candidati della galleria meteore restano esplicitamente non confermati.

## Sitemap e robots.txt Allsky

- `/home/pi/allsky/html/allsky/sitemap.xml` elenca la Home pubblica e le quattro gallerie: videos, startrails, keograms e meteors.
- `/home/pi/allsky/html/robots.txt` è servito in `https://digitalstargate.freeddns.it:23232/robots.txt`, alla radice dell’host e della porta corretti.
- La regola lighttpd della porta pubblica ammette esattamente questi due file aggiuntivi. Non è stata estesa l’esposizione della WebUI amministrativa.

```text
User-agent: *
Disallow: /
Allow: /allsky/
Allow: /current/image.jpg
Disallow: /allsky/configuration.json
Disallow: /allsky/data.json
Disallow: /allsky/myFiles/
Sitemap: https://digitalstargate.freeddns.it:23232/allsky/sitemap.xml
```

Robots.txt disciplina la scansione e **non è un controllo di accesso**. L’isolamento dell’amministrazione dipende dalle regole del web server. Prima della modifica, robots.txt rispondeva 403: Google tratta normalmente un 4xx diverso da 429 come assenza di robots.txt; non è corretto attribuire a quel solo 403 un blocco dell’indicizzazione.

GitHub Pages ospita il portale sotto un percorso di progetto. Un file robots.txt dentro quel percorso non governa l’intero host: la posizione valida sarebbe `https://maininimassimo-bit.github.io/robots.txt`, che al controllo risponde 404. Non sono stati modificati altri repository per pubblicarlo; il portale usa la propria sitemap e Search Console.

## Search Console e controlli operativi

Le proprietà da gestire sono di tipo **Prefisso URL**, con gli indirizzi completi della Home del portale e della Home Allsky riportati sopra. La porta `23232` fa parte dell’indirizzo della seconda proprietà.

Il tag pubblico di verifica del portale è nel blocco `extrahead` di `overrides/main.html`, soltanto sulla Home. Il tag della proprietà Allsky è nel suo `index.php`. I tag non sono credenziali di accesso, ma devono restare pubblicati per mantenere la verifica.

Procedura dopo la pubblicazione:

1. Verificare ogni proprietà con il metodo Tag HTML.
2. Inviare la relativa `sitemap.xml` nel report Sitemap e controllarne l’esito di lettura. La conferma di invio non equivale a recupero riuscito.
3. Usare Controllo URL per Home, presentazione Allsky e sito live; richiedere l’indicizzazione quando il test lo consente.
4. Controllare Pagine e Problemi di sicurezza. Registrare separatamente disponibilità HTTP, verifica proprietà, lettura sitemap, richiesta e indicizzazione effettiva.

Al controllo iniziale del 09/10/2026, **la proprietà Allsky è verificata tramite Tag HTML**, ma Google segnala **Pagine ingannevoli**, senza URL di esempio. La sitemap è stata inviata; il report iniziale indica **Impossibile recuperare / Impossibile leggere la Sitemap**, mentre la verifica HTTP esterna del file restituisce 200 con XML valido. La causa del mancato recupero non è stata determinata: non attribuirla automaticamente alla porta, al certificato o alla segnalazione.

Il controllo delle cinque pagine pubbliche, anche con user-agent Googlebot e referrer Google, non ha individuato moduli di raccolta dati, iframe o reindirizzamenti esterni; gli script della Home sono locali e le librerie controllate non differiscono dalla baseline Git. Questo controllo circoscritto non costituisce una scansione completa del sistema né prova che la segnalazione sia un falso positivo. Un eventuale riesame deve riportare questi limiti e i controlli reali, senza dichiarare bonifiche non effettuate. Lo stato aggiornato e gli esiti di pubblicazione sono tracciati anche nell’evidence della pull request.

Su autorizzazione dell’owner è stata inviata una richiesta di rivalutazione tramite il modulo **Google Navigazione sicura**, con conferma di invio riuscito il 09/10/2026. Il testo descrive il sito astronomico, l’assenza di URL di esempio e i controlli circoscritti; non dichiara una bonifica o una scansione completa. Non è stato utilizzato il riesame Search Console che richiedeva di attestare «Tutti i problemi sono stati risolti». La conferma di invio del modulo non rimuove la segnalazione: l’esito Google resta da verificare.

Il test dell’URL Allsky pubblicato, eseguito da Google il 09/10/2026 alle 21:07 Europe/Rome, riporta **L’URL è disponibile per Google / La pagina può essere indicizzata**. La successiva richiesta di indicizzazione è stata accettata e l’URL aggiunto alla coda prioritaria. Questo esito distingue la recuperabilità della Home dal problema del report Sitemap e non annulla la segnalazione di sicurezza. L’indicizzazione effettiva resta una decisione di Google.

## Esiti dopo la pubblicazione del portale

La modifica è stata pubblicata con la [PR #541](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/541). Il merge `fcc2560b15e26c1c1a22aaff90f61040c0ac4480` è incluso nel successivo `93be5531da5243c79c3f3f03f9762095700a6f45`, il cui workflow Pages `37979592720` è concluso con successo. Sono stati verificati HTTP 200 della Home, della pagina Allsky, di questa procedura, del capitolo 27 revisione 0.6 e della sitemap; il browser riceve l’anteprima live a risoluzione originale 1936 px, ridimensionata nel riquadro.

| Operazione del 09/10/2026 | Esito osservato |
|---|---|
| Proprietà Search Console del portale | Verificata con Tag HTML dopo la pubblicazione |
| Proprietà Search Console Allsky | Verificata con Tag HTML |
| Sitemap del portale | Invio confermato; report iniziale «Impossibile recuperare» |
| Sitemap Allsky | Invio confermato; report iniziale «Impossibile recuperare» |
| Home del portale | Richiesta di indicizzazione accettata nella coda prioritaria |
| Pagina Allsky nel portale | Richiesta di indicizzazione accettata nella coda prioritaria |
| Home del sito Allsky | Test pubblico positivo e richiesta di indicizzazione accettata |
| Report sicurezza del portale | «Nessun problema rilevato» al controllo |
| Classificazione Navigazione sicura Allsky | Richiesta di rivalutazione inviata; esito pendente |

La verifica HTTP delle sitemap, anche con user-agent Googlebot, restituisce 200 e XML valido: 955 URL / 194.522 byte nel portale e 5 URL / 513 byte in Allsky. Tutti gli URL appartengono al rispettivo prefisso e i file rispettano i limiti di 50.000 URL e 50 MB. Sono conteggi del controllo, non valori immutabili del catalogo. Non è stata identificata la causa dell’errore iniziale in Search Console; non sono state effettuate reinoltri ripetuti né dichiarata la lettura riuscita.

Al momento delle richieste i tre URL risultavano sconosciuti all’indice. **Indicizzazione richiesta** è la conferma della coda, non la prova della comparsa nei risultati. Il prossimo controllo deve verificare lettura delle sitemap, decisione di Navigazione sicura e stato indicizzato degli URL, senza duplicare le richieste già accettate.

## Verifica tecnica e ripristino

Sono stati verificati sintassi PHP e lighttpd, risposta HTTP 200 della Home e dei due file SEO, struttura XML con cinque URL e risposta 403 degli ingressi amministrativi pubblici controllati. Sul portale: compilazione MkDocs rigorosa, canonical, descrizioni, tag Google, nuova voce sitemap e test delle anteprime Home/Stato.

Backup privato Allsky: `/home/pi/allsky-private-archive/public-seo-20261009-205647`, contenente pagina e configurazione lighttpd precedenti. Per ripristinare: copiare `index.php` nella Home Allsky e `public-https.conf` in `/etc/lighttpd/conf-enabled/98-allsky-public-https.conf`, validare lighttpd e ricaricare il servizio. Robots e sitemap sono file nuovi; rimuoverli solo dopo aver verificato che siano ancora quelli introdotti da questa modifica. Sul portale usare un revert della modifica e la normale ricompilazione Pages.

Dopo aggiornamenti Allsky controllare che non siano stati sovrascritti metadati e tag Google; dopo aggiornamenti del portale verificare Home, pagina Allsky e sitemap. Non aggiungere coordinate precise, credenziali, amministrazione o percorsi privati alle sitemap.

## Riferimenti

- [Google: pubblicare un sito nella Ricerca](https://developers.google.com/search/docs/fundamentals/get-on-google).
- [Google: posizione e interpretazione di robots.txt](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec).
- [Google: report Problemi di sicurezza e riesame](https://support.google.com/webmasters/answer/9044101).
- [Progetto tecnico AllSky](../chapters/27-sistema-allsky.md).
