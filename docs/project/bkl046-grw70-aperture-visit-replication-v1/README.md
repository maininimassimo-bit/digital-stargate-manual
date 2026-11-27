# BKL-046 · Ripetibilità fra visite delle aperture GRW+70°5824

Ho fissato venti visite del programma 11907, distribuite a rango regolare nel tempo fra le 62 visite di catalogo ancora disponibili. Le dodici visite già esaminate sono escluse. Ho verificato 60 FLC distinti. Con la posizione Gaia e la parallasse geocentrica, 45 pose risultano oltre il limite sul picco, quattro hanno DQ nel nucleo, dieci hanno supporto insufficiente e una è misurabile a entrambi i raggi. Nessuna terna completa supera il protocollo astrometrico assoluto.

Applicando alle nuove pose la regola esplorativa del centro previsto dalle altre due bande, 16 pose sono respinte per DQ al nucleo, 38 per supporto insufficiente e sei sono misurabili a entrambi i raggi. Tutte le bande risultano valide su due visite, entrambe UVIS2. I valori riportano colore a 10 pixel meno colore a 5 pixel, in millimagnitudini. [Protocollo del centro relativo](../bkl046-grw70-held-out-band-apertures-v1/README.md)

| Visita | F438W − F606W | F438W − F814W | F606W − F814W |
| --- | ---: | ---: | ---: |
| ibbsb0 | +15,74 | +29,49 | +13,75 |
| ibbsd5 | +9,44 | +8,69 | −0,75 |
| ibbsz1, studio esplorativo precedente | +3,28 | +9,65 | +6,37 |

Fra le due nuove visite lo scarto nel termine di apertura F438W − F814W è di 20,79 mmag. Per prevedere una visita, il protocollo richiede almeno altre due visite nuove dello stesso chip. Escludendo la visita da prevedere ne rimane una. La visita esplorativa precedente resta disponibile per confronto separato. Il rapporto registra quindi zero predizioni che soddisfano il criterio fissato.

I risultati aggiungono due epoche a una seconda stella e mostrano che la correzione d'apertura varia anche sullo stesso chip. Il centro relativo usa le altre due bande della stessa visita. Rimangono aperti il riferimento astrometrico di campo, l'incertezza fra pose e la validazione della correzione su visite indipendenti. Nessuna chiusura scientifica o esecuzione PixInsight.

Per replicare, eseguire `misura.py` con il kit estratto, il kit originale dei tre calibratori, NumPy 2.3.5/Astropy 7.2.0, un nuovo risultato e lo SHA-256 del manifest di acquisizione `cd532c4f14609939a53c36ed4763ca28d684d745d408e5d627ef5f2a55bba090`. Per `misura-centro.py`, passare gli stessi kit e dipendenze, il rapporto esplorativo precedente, il percorso del nuovo risultato, lo SHA-256 di acquisizione e quello del rapporto primario `be9a72f3babbc956f59dc060a166561275c38136e5dc2e7572e099cd5e2e77e1`.