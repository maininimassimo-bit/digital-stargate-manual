# BKL-046 · Cattura della finestra testimone visibile su DSG-Shared

Due esecuzioni nella sessione interattiva Windows 2 hanno associato il processo originale al suo HWND tramite handle del processo, PID, data di creazione e thread della finestra. In ogni esecuzione un secondo processo ha aperto una finestra con lo stesso titolo e colori diversi.

La cattura PrintWindow ha restituito i pixel attesi su entrambe le finestre. I due BMP originali hanno SHA-256 `2e0e7ced28c41b13bd5644e605684a0f8cf7908bd19bd87549d8baef7d85ac3e`. Il testimone originale ha registrato WM_CLOSE, è uscito con codice 0 e il suo HWND è scomparso. Il secondo tentativo di chiusura è stato respinto e la finestra omonima è rimasta aperta fino alla pulizia del test. Il foreground coincideva nei punti controllati.

Il testimone disegna con WM_PAINT e risponde a WM_PRINTCLIENT. Il risultato vale per questa implementazione Win32 visibile. La cattura della finestra Qt di PixInsight e la gestione di un eventuale blocco di PrintWindow nel launcher scientifico restano da qualificare. Le prove native e le chiusure scientifiche restano a zero. Nessuna richiesta di ammissione.
SHA-256 archivio H: a606bb4041336b61a0bc7f084a306063b566a4f320667e20b867a98f5f8a55ea.
