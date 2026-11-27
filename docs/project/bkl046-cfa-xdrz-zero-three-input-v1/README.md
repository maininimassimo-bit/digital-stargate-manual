# Cinque bracci CFA a tre ingressi

Il kit estende il controllo CFA a tre ingressi con due bracci a pixel azzerato. Ogni braccio usa tre mosaici distinti. Il terzo mosaico è identico nelle cinque prove e viene tradotto in modo da non sommare peso verde nelle due celle discriminanti. Anche il riferimento, la fase RGGB, la geometria e le altre impostazioni sono fissati. Le mappe attese sull’intero campo usano il modello a tre ingressi.

I risultati attesi per peso conservato o esclusione rimangono rispettivamente 0,125 / 2 e 0,25 / 1 alla cella (13, 8), e circa 0,09 / 2 e 0,18 / 1 alla cella (14, 7). Le mappe complete e le impronte sono nel riscontro. Il confronto usa i cinque bracci e le tolleranze del comparatore precedente.

Per rigenerare il kit, eseguire `genera.py <fixture-originale-a-tre-ingressi> <piano-originale.json> <pacchetti-Python> <nuova-directory-kit>`. Eseguire poi `classifica.py <pacchetti-Python> <directory-kit> <nuovo-rapporto.json> --self-test`. Il piano originale e il suo manifest sono inclusi nell’archivio locale.

Per una prova nativa, il launcher deve ancora produrre e attestare le mappe dei pesi grezzi, rileggere le impostazioni effettive insieme alla console e ottenere le revisioni e l’ammissione. Il requisito di tre ingressi deriva dal piano precedente. Il kit e il comparatore sono stati eseguiti offline.
