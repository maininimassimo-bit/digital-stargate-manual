# BKL‑046 · Orientazione PSF e sensibilità al centraggio

Questo controllo integra l’asse aperto `PSF_PIXEL/2`. Il banco sintetico misura l’orientazione assiale in immagini Moffat senza rumore, alla scala di 0,65 pixel. I risultati valgono per il profilo, la scala e le fasi provati. [Evidenze su fase subpixel e fotometria](BKL-046-PSF-PIXEL-2-CONOSCENZA.md)

- **Momenti dei pixel.** Il raffinamento dell’integrazione converge nei 162 casi Moffat più stretti. L’errore di orientazione persiste e lo stimatore restituisce un angolo spurio in tutte le sei fasi circolari distinte.
- **Adattamento ai pixel con centro noto.** Tutti i 108 casi ellittici e i sei controlli circolari rispettano i criteri congelati. L’errore angolare massimo è 0,00056°.
- **Adattamento con centro traslato.** Si riusano 54 profili sintetici per 1.350 adattamenti, conservando le direzioni e tutti gli esiti. Ogni serie non nulla contiene 432 adattamenti e 48 controlli circolari.

| Scarto del centro | Adattamenti fuori criterio | Angoli spuri nei controlli circolari | P90 dell’errore degli angoli ellittici disponibili |
| --- | ---: | ---: | ---: |
| 0 | 0/54 | 0/6 | 0,000090° |
| 0,025 pixel | 352/432 | 22/48 | 29,50° |
| 0,05 pixel | 389/432 | 28/48 | 48,94° |
| 0,10 pixel | 407/432 | 32/48 | 67,25° |

Nei confronti a centro perturbato restano conservati gli angoli ellittici mancanti e l’unico arresto della ricerca per limite di iterazioni. I conteggi per direzione sono confronti accoppiati sugli stessi dati sintetici. Lo scarto di 0,025 pixel è il più piccolo provato, quindi la prova non determina la soglia operativa di centraggio.

L’adattamento con centro imposto rimane da qualificare per l’uso operativo. Il successivo confronto deve misurare l’adattamento congiunto di centro e forma, l’incertezza di orientazione e i controlli circolari anche in presenza di rumore e profili fuori famiglia. Nessuna chiusura scientifica.

## Ricevute

| Prova | SHA‑256 della ricevuta |
| --- | --- |
| Controllo dei momenti | `fd6c67be96218e398bbca2fb27f9d0c415ef09ebcf6482dbbdcc4664128c3715` |
| Raffinamento dell’integrazione | `72ca31b227af6f8af91b3e9ee9e2f91a773db138c79ef2dc1a5d5990044fd0bd` |
| Adattamento ai pixel a centro noto | `09a956438c42218937626b33a7ba9cc8a26e4ca6888a33a6a023f9c0250ceb8d` |
| Scarti controllati del centro | `2fdc039e93290922baf70aaa4842782cdb360c5bba6dd642071b64350244fabe` |
