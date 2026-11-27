# Registrazione delle tre pose M51 prima del demosaicing

Il protocollo usa le tre pose originali Canon EOS 6D già fissate. La prima è il riferimento. La ricerca iniziale prova la relazione nelle coordinate memorizzate e con rotazione di 180°. L’analisi lavora sulla media dei due verdi, senza alterare il RAW. Se il picco supera entrambe le soglie congelate, segue la misura locale su nove riquadri. La firma della traslazione viene verificata con uno spostamento intero noto. Un confronto affine richiede almeno sei riquadri.

| Posa | Picco nelle coordinate memorizzate | Picco con rotazione di 180° | Esito |
| --- | ---: | ---: | --- |
| Centrale | 0,753 | 0,366 | Orientamento memorizzato preferito. Cinque riquadri su nove misurabili. |
| Ultima | 0,255 | 0,295 | Differenza di 0,040, inferiore al margine congelato di 0,09. |

Nei cinque riquadri validi della posa centrale lo spostamento sull’asse Y varia da −159,25 a −148,70 pixel nativi. Il protocollo lascia aperto il modello geometrico perché mancano riquadri sufficienti, e lascia irrisolto il confronto dell’ultima posa. Nessuna parità globale è stata assegnata. Lo spostamento osservato non documenta un dither intenzionale.

Una prossima qualificazione può usare associazioni stellari e un riferimento astrometrico indipendente per aumentare il supporto geometrico. Conservare gli esiti insufficienti del protocollo attuale. Per riprodurre eseguire `misura.py protocollo.json <acquisizione-M51> <sorgente-registrazione> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`.
