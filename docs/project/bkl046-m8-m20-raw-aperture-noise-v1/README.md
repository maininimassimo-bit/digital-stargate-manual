# Rumore di aperture compensate sui pixel Bayer originali

Il controllo BKL-046 rilegge le differenze fra le coppie di flat e dark brevi di M8–M20 e riproduce il rapporto sulla varianza temporale. Usa gli stessi pixel validi per entrambi i tipi di esposizione. In ciascuna parità, le finestre disgiunte da 7 × 7 campioni contengono un nucleo da 3 × 3 o 5 × 5. Dal nucleo si sottrae il fondo stimato sul bordo. Il controllo sintetico verifica che il filtro annulli un piano e che il modello diagonale riproduca il caso con covarianza nulla.

Per le quattro parità, i due tipi di esposizione e i due nuclei, la mediana del rapporto fra deviazione standard misurata e previsione diagonale va da 0,970 a 1,019 sulle coppie e sui riquadri di verifica. L’errore relativo P90 della previsione diagonale va da 10,3% a 15,4%. Un fattore per parità e tipo di apertura, stimato su coppie e riquadri disgiunti, migliora il P90 in 7 confronti su 16.

La dispersione delle stime locali rimane ampia anche quando il rapporto mediano è vicino a uno. Il confronto riguarda pixel Bayer originali, con finestre espresse nel reticolo di ciascuna parità. I rapporti misurati nelle ricostruzioni includono un altro campionamento, il fondo e la registrazione. Resta aperta la verifica a risoluzione equivalente con un modello di covarianza che si trasferisca a dati indipendenti.

Per replicare eseguire `misura.py <protocollo.json> <studio-varianza> <calibratori> <pacchetti-Python> <nuovo-riscontro.json>`.
