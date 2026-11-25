# BKL-046 · Trasferimento del colore di apertura da IC 1805 a M8/M20

Il test riguarda la variazione del colore Bayer B−R tra aperture di raggio 3 e 6 pixel nativi. I due campi provengono da camere diverse e la risposta spettrale assoluta delle camere resta da calibrare. L'asse FILTER_COLOR/3 resta aperto. Zero avvii nativi e zero chiusure scientifiche.

## Identificazione delle stelle di M8/M20

La prima posa pubblica di Colmic ha un centro nominale, la focale e la dimensione del pixel, ma manca di WCS. Ho stimato orientamento, scala e traslazione da triangoli di stelle del piano verde CFA. Il modello polinomiale della proiezione TAN è stato stimato senza usare rivelazioni entro 125 pixel dalle 54 stelle Bayer tenute da parte. La proiezione Gaia usa i moti propri riportati all'epoca della posa.

L'archivio ESA ha restituito 91.495 sorgenti con G < 15 entro 2,55° e con il conteggio TAP verificato in ciascuna fascia. Una risposta monolitica apparentemente riuscita copriva solo una parte del campo ed è stata scartata. La soluzione associa 54/54 stelle in 8 zone con P90 di 0,682 px, ma il primo controllo casuale da 4 px dà 7 associazioni contro il massimo ammesso di 3. La ricevuta conserva il rifiuto iniziale.

Per il confronto cromatico è stata condotta una verifica esplorativa successiva: raggio 1,5 px, seconda sorgente del catalogo a più di 8 px e identificativi univoci. Il controllo ha ricalcolato le coppie indipendentemente e ha confrontato il risultato con 256 rimescolamenti delle ascisse. Restano 42/54 stelle in tutte le 8 zone. Il massimo casuale è 5 coppie e il P99 è 4. Il taglio di isolamento riguarda le sorgenti presenti fino a G < 15. [Posa e dati Siril](https://siril.org/tutorials/tuto-scripts/index.html) · [Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html)

## Trasferimento tra campi

La mediana di confronto e il modello lineare BP−RP provengono dalle stesse 18 stelle di IC 1805, calibrazione A. Entrambi sono applicati senza ritaratura alle 42 stelle M8/M20 selezionate, 5 delle quali fuori dall'intervallo BP−RP dell'addestramento. I valori A e B mostrano le due metà di calibrazione Bayer.

| Metodo | Mediana IC 1805, P90 A / B (mag) | BP−RP IC 1805, P90 A / B (mag) | Errore mediano con BP−RP A / B (mag) |
| --- | ---: | ---: | ---: |
| drop 1,0 | 0,17564 / 0,17908 | 0,17045 / 0,16875 | −0,05955 / −0,05959 |
| drop 0,7 | 0,18076 / 0,18384 | 0,16647 / 0,16558 | −0,05950 / −0,05915 |
| Bilineare per parità CFA | 0,19075 / 0,19425 | 0,19268 / 0,19172 | −0,03734 / −0,03644 |

La correzione riduce parzialmente il P90 per i due drop, ma peggiora l'errore mediano con segno per tutti e tre i metodi rispetto alla mediana di IC 1805. Anche ricalibrando soltanto l'intercetta su 22 stelle locali e verificandola sulle altre 20, il P90 rimane tra 0,156 e 0,207 mag e l'errore mediano peggiora. Il confronto non qualifica una correzione cromatica trasferibile. Rimangono da verificare il colore assoluto calibrato e la stabilità al variare di campo, fotocamera e fondo.

## Riproducibilità

- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-M8-M20-Gaia-a1675aa38ee7.zip`.
- Soluzione M8/M20: `b4d9d1ee43b8c707383b0884dbb2b577abb145696c1c05c447c98d337819c254`.
- Controllo delle coppie isolate: `a2d46c85c9695bf71f7402eafea55434040785e66e3bfe42b7297e931f6db0bb`.
- Trasferimento cromatico: `a1675aa38ee773464e549bff59970cc45c016d35d19669f5e442b9ba2511370a`.
- Il pacchetto contiene query, risposte Gaia per fascia, conteggi, catalogo aggregato, programmi e ricevute. Le ricevute fissano le impronte dei dati preesistenti.
