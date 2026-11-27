# BKL-046 · Ripetibilità dell'orientazione PSF su stelle M8/M20

Il controllo usa 19 stelle di verifica già selezionate in zone distinte da quelle usate per stimare le larghezze. Mantiene i centri e le larghezze geometriche d'archivio, 2,75 pixel in rosso e 3,125 in blu. Il fit confronta profili Moffat circolari ed ellittici integrati su nove campioni per pixel, con ampiezza positiva e un piano di fondo. Sceglie la forma su una partizione a scacchiera e la verifica sui pixel complementari, poi scambia le partizioni. L'angolo richiede almeno il 10% di riduzione dell'errore quadratico in entrambe le verifiche, rapporto assiale al massimo 0,85 e accordo fra partizioni entro 15 gradi.

| Confronto | Fit con angolo nelle due condizioni | Stelle confrontabili | Accordo entro 15 gradi |
| --- | ---: | ---: | ---: |
| Rosso, calibrazioni A/B | 5 / 6 | 5 | 5 |
| Blu, calibrazioni A/B | 1 / 2 | 1 | 1 |
| Rosso/blu, calibrazione A | 5 / 1 | 0 | Non valutabile |
| Rosso/blu, calibrazione B | 6 / 2 | 0 | Non valutabile |

I controlli sintetici lasciano indeterminato il caso circolare e recuperano l'angolo noto del caso ellittico sulla griglia. Le calibrazioni A e B riusano le stesse acquisizioni. L'accordo riguarda angoli discretizzati su immagini ricostruite, senza una misura indipendente di riferimento. Fondo, vicini, larghezza e forma delle ali possono influire sull'orientazione stimata. La verifica spaziale riduce la dipendenza dall'adattamento ai pixel usati per il fit. Il ricampionamento lascia correlazioni fra le due partizioni. Resta da qualificare l'orientazione fisica e cromatica su dati indipendenti e in PixInsight.

Il programma usa il protocollo, la directory con i ritagli archiviati e la ricevuta delle larghezze, NumPy 2.3.5 e un percorso nuovo per il rapporto. [Ritagli e larghezze M8/M20](../BKL-046-SPATIAL-STATS-NATIVE-CONTROL-2026-11-13.md)