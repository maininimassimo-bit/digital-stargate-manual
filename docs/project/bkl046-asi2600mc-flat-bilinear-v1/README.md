# BKL-046 · Varianza dei flat ASI2600MC dopo ricampionamento bilineare

La prova riusa sette coppie disgiunte di flat da 3 s, nove riquadri e quattro parità Bayer. Applica cinque fasi bilineari fisse e misura la varianza delle somme di quattro pixel. Verifica prima tutti i 252 rapporti originali sul riquadro intero. Poi confronta la differenza grezza, la correzione di un fattore d’illuminazione ricavato da altri riquadri e la sottrazione di un piano stimato nella metà opposta del riquadro. Le due metà sono separate da quattro colonne sulla griglia della parità Bayer. I tre trattamenti usano lo stesso supporto.

| Fase e trattamento | Errore mediano con propagazione completa | Errore mediano con propagazione diagonale | Entro il 10% con propagazione completa |
| --- | ---: | ---: | ---: |
| Mezzo pixel su entrambi gli assi, grezzo | 6,2% | 57,3% | 330/504 |
| Mezzo pixel su entrambi gli assi, scala di illuminazione | 6,3% | 57,3% | 330/504 |
| Mezzo pixel su entrambi gli assi, piano sottratto | 5,4% | 56,9% | 384/504 |

La previsione diagonale non rientra nel 10% in alcuno dei 504 confronti a questa fase. Il P95 dell’errore della propagazione completa scende dal 39,1% al 17,8% con la sottrazione del piano. Il rapporto mediano fra varianza misurata e stima diagonale empirica passa da 2,306 a 2,295. Il valore teorico con ingresso indipendente e omoscedastico a questa fase è 2,25. A fase nulla le due previsioni coincidono.

Le 504 misure per fase condividono coppie, riquadri e parità. Anche la sottrazione del piano lascia errori residui. Il campione riguarda una singola durata illuminata e un kernel offline sulla griglia Bayer. Restano da verificare la risposta a più dosi e la validità per gli operatori nativi. Zero avvii PixInsight e zero chiusure scientifiche.

Per riprodurre, passare a `misura.py` il protocollo, la directory `prior` del pacchetto, `Flats_3s.zip`, le dipendenze NumPy 2.3.5 e Astropy 7.2.0 e una nuova directory di uscita. Usare Python 3.12. Il pacchetto H/K contiene i dettagli di tutti i confronti e gli ingressi fissati per impronta.