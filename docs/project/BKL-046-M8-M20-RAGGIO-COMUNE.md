# BKL-046 · Dispersione CFA a raggio stellare confrontabile

Sulle pose Bayer di M8 e M20 si confronta il bilineare per parità con i depositi diretti da 1,00 e 0,70 px dopo convoluzione gaussiana. La larghezza del filtro si sceglie minimizzando la differenza mediana del raggio RMS stellare su quattro regioni del rivelatore e sulla calibrazione A. Si verifica il raggio sulle altre quattro regioni con entrambe le calibrazioni. Il programma esclude le stelle con meno del 90% di supporto comune dopo l'erosione richiesta dal filtro. Restano 22–24 stelle per parità per la stima e 26–29 per la verifica.

La griglia di ricerca sceglie σ = 0,70 px per il deposito da 1,00 e σ = 0,75 px per quello da 0,70, per tutte le parità. In verifica, il P90 dello scarto assoluto di raggio resta sotto lo 0,77% in ogni caso, entro la soglia del 5%. La mediana con segno resta entro la soglia del 2%. Il controllo eguaglia un indicatore di larghezza del profilo, senza attestare l'equivalenza della PSF o della risposta in frequenza.

La dispersione si misura su 202–229 finestre per parità. Le finestre provengono dalle stelle escluse dalla stima, con identico supporto per i metodi e le due metà temporali. Si usa la deviazione standard della somma compensata nel nucleo 3 × 3 o 5 × 5.

| Deposito confrontato con il bilineare dopo l'equalizzazione del raggio | Nucleo | Casi con dispersione minore nel bilineare | Variazione del bilineare |
| --- | ---: | ---: | ---: |
| 1,00 px | 3 × 3 | 6/8 | da −17,8% a +12,3% |
| 1,00 px | 5 × 5 | 8/8 | da −24,3% a −0,9% |
| 0,70 px | 3 × 3 | 6/8 | da −33,5% a +52,2% |
| 0,70 px | 5 × 5 | 6/8 | da −30,8% a +32,5% |

Gli otto casi per riga sono le quattro parità per due calibrazioni. La parità G2 mostra le inversioni. Il vantaggio generalizzato osservato a pari scala geometrica si riduce dopo l'equalizzazione del raggio stellare e dipende da parità e apertura. Le finestre riusano campo e pose, e la dispersione comprende PSF, fondo e registrazione. Restano da verificare altri campi, l'equivalenza della risposta spaziale completa e il processo nativo. Zero chiusure scientifiche e zero avvii PixInsight.

SHA-256 della ricevuta `6b0af19c12ba9719eb0fb9fc5320b66fac1bbad790593559e7e49b40d96a87f3`.
