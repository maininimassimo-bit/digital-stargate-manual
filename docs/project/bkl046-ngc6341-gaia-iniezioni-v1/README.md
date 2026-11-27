# BKL-046 · Controllo del matcher Gaia con identità note

Il test usa la geometria del catalogo Gaia calibrato del pilot NGC 6341 per creare centroidi sintetici nelle tessere dispari. Il rapporto del pilot viene riprodotto prima di accettare i risultati. Il catalogo resta invariato e non viene adattato alle iniezioni.

| Caso simulato | Esito al raggio di 1 pixel |
| --- | --- |
| 216 centroidi con errore da 0,25 o 0,75 px | 216 identità corrette |
| 108 centroidi con errore di 1,25 px | 108 senza associazione |
| 208 rilevamenti duplicati da 104 sorgenti | 208 senza associazione |
| 104 falsi centroidi a 8 px dalla previsione usata per generarli | 104 senza associazione |
| 104 falsi centroidi posti a 0,20 px da una previsione Gaia | 104 associazioni accettate |

I conteggi aggregano due pose e due chip. Le pose condividono gran parte della geometria. La coincidenza costruita mostra che una corrispondenza reciproca e univoca può accettare un falso centro quando manca il vero rilevamento. Il test non simula la formazione dell'immagine e le proporzioni dei casi sono scelte per costruzione. I risultati caratterizzano il matcher e non stimano completezza o falsi positivi sulle immagini reali.

Eseguire `iniezioni.py` con lo script e il rapporto congelati del pilot, la directory FITS e Gaia, il JSON dei centroidi, la directory dei pacchetti Python e un nuovo percorso di uscita.
