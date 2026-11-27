# BKL-046 · Rilevamento uniforme dei salti persistenti in Roman LIN0

Il protocollo è stato fissato dopo la diagnosi delle due finestre e prima della scansione completa. La regola verifica ogni pixel delle due fasce, dei 32 canali e delle 30 esposizioni. Per ciascuna esposizione sottrae la mediana del canale e confronta la differenza cumulativa di ogni lettura con la mediana e la scala robusta delle altre 29 esposizioni. Richiede un eccesso positivo alla lettura 1 sopra otto scale robuste e la persistenza alle letture 5 e 10 di almeno metà del primo eccesso, sopra le soglie delle rispettive letture. I pixel al limite di rappresentazione vengono esclusi dal rilevatore. Il controllo sintetico distingue un salto persistente da uno transitorio e da un salto di segno opposto.

| Fascia | Osservazioni pixel × esposizione | Eccessi alla lettura 1 | Eccessi persistenti |
| --- | ---: | ---: | ---: |
| Inferiore | 3.931.950 | 11 | 0 |
| Superiore | 3.931.890 | 68 | 12 |

Due dei dodici casi persistenti corrispondono a due pixel della finestra nota, al canale 4 nell'esposizione 20. Gli altri dieci corrispondono tutti a un singolo pixel del canale 15, alle coordinate locali (30, 8), in dieci esposizioni diverse. Questa posizione è distinta dalla finestra del canale 15 esaminata in precedenza.

La soglia è esplorativa e la scansione riusa le esposizioni della diagnosi. Le osservazioni spaziali e temporali sono dipendenti. I conteggi non misurano il tasso di falsi positivi o l'origine fisica dei segnali. La composizione del campione di previsione resta intatta. Servono riferimenti indipendenti per qualificare una maschera o una regola di attenuazione.

Per ripetere usare Python 3.12, il protocollo, la directory della diagnosi locale, il decodificatore LIN0, la cattura LIN0, NumPy 2.3.5 e un nuovo percorso per il rapporto.
