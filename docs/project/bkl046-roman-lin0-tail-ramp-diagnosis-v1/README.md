# BKL-046 · Evoluzione nelle letture delle anomalie locali Roman

Il controllo usa le 30 esposizioni LIN0 e le letture 0, 1, 5 e 10 archiviate per la fascia superiore. Le due finestre 3 × 3 sono quelle emerse dal precedente esame esplorativo della coda, alle coordinate locali (22, 20) del canale 4 e (54, 20) del canale 15. Per ogni lettura si sottrae il fondo locale stimato nell'anello e si applicano gli stessi pesi della somma ricampionata. I riquadri non includono valori al limite di rappresentazione nelle letture acquisite. Le unità sono somme pesate in ADU.

- Canale 4. Nell'esposizione 20 il salto fra lettura 0 e 1 vale +5.384,75 ADU. Nelle 28 esposizioni fuori dalla coppia 19–20 varia da −212 a +131,5 ADU. Il valore relativo alla lettura 0 resta +5.127,75 ADU alla lettura 10. L'altra esposizione della coppia presenta −18 ADU alla prima lettura. Il segnale è quindi localizzato a una singola esposizione e persiste fra le letture campionate.
- Canale 15. La finestra ha un fondo locale sottratto molto più alto già alla lettura 0. La mediana nelle 28 esposizioni di confronto è +23.169,25 ADU. Nella coppia 13–14, le variazioni dalla lettura 0 alla 1 sono +150 e −1.037,75 ADU. Alla lettura 10 diventano −8.917,25 e −8.935,75 ADU. La proiezione della differenza della coppia passa da −788,95 ADU alla lettura 1 a −5,66 ADU alla lettura 5. La variabilità iniziale del canale 15 ha un andamento diverso dal salto osservato nel canale 4.

Le finestre sono state selezionate dopo l'esame dei risultati. Il rapporto conserva le distribuzioni di riferimento e i valori delle coppie. Le sole letture campionate delimitano il momento del salto. L'origine fisica e una regola di rilevamento indipendente restano da verificare. Nessun caso è stato scartato dal campione principale.

Per riprodurre usare Python 3.12 con il protocollo, la directory del riscontro della coda, il decodificatore LIN0 a segnale comparabile, la cattura LIN0, le dipendenze NumPy e un nuovo percorso di uscita.
