# BKL-046 — Collaudo offline del rilascio Stream34 v11

Ho eseguito il modulo operatore fissato dal soggetto `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1` con un canale, un supervisore e un coordinatore simulati. Il collaudo verifica la sequenza fra riscontro della finestra, autorizzazione di chiusura, ricevute di pubblicazione, uscita del processo padre e verifica contabile finale.

| Esito | Casi | Richieste di rilascio al coordinatore simulato |
| --- | ---: | ---: |
| Successo con record interi, frammentati o uscita ritardata | 3 | Una per caso |
| Rifiuto prima del rilascio | 16 | Zero |
| Esito del rilascio non confermato | 1 | Una, con esito terminale respinto |

Il caso con uscita ritardata consegna l'ultimo record e termina il flusso, trattenendo ancora l'evento di uscita del padre. La verifica finale e la chiamata di rilascio restano sospese fino a quell'evento. I rifiuti coprono, fra gli altri, identità o prenotazione diversa, record incompleto, esito di uscita avverso, impronte delle ricevute incoerenti, indisponibilità del supervisore e verifica finale negativa. Nel caso di risposta incerta, la chiamata al coordinatore è già avvenuta e il modulo respinge la conferma. Il collaudo non stabilisce lo stato di un registro reale dopo una risposta incerta.

Nessuna ammissione richiesta, nessun accesso al registro canonico e nessun avvio di PixInsight. Il riscontro riguarda l'ordine e i rifiuti del modulo operatore. La qualifica del pacchetto completo, le revisioni autentiche e la prova nativa restano aperte.

| Evidenza | SHA-256 |
| --- | --- |
| Collaudo | `cb90b3f944f66a1d4eaaaee6218ae143c935357c62723dff09a368c39034e132` |
| Riscontro | `2427614fe1ef7ad1db23105bab42fbb067f5d17d514dce516e092efc1e27488a` |
| Archivio riprodotto da H: | `6e510d9bf966a64ec86489b853d65b575b6fd622f24f15f3fe310103a000c27b` |
