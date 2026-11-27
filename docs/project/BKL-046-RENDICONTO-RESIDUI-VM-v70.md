# BKL-046 · Aggiornamento del rendiconto VM v70

Questo aggiornamento si aggiunge al rendiconto v69, SHA-256 `0f3573b85ca2a4a5a03d91fd33d29692141f1f1a16be0b47c5db5ff3b7a5463a`. La copertura resta di 4.920 requisiti e 14.521 criteri. Sono aperti 19 criteri Owner, sette famiglie e 25 assi scientifici. Le chiusure scientifiche restano zero.

- **CFA_DITHER_DRIZZLE/2.** Tre verifiche riproducibili su IC 1805 chiariscono i limiti della selezione del modello, della concordanza tra parità verdi e del confronto con Gaia. Anche sul sottoinsieme con identità Gaia verificata, il P90 della registrazione fra pose è circa 0,380 pixel e supera la soglia di 0,30. Il confronto scientifico a scala comune in PixInsight resta aperto.
- **Stream34 v11.** Su DSG-Shared sono stati riletti tutti i 70 membri del pacchetto del launcher e il selettore del coordinatore. Il collaudo isolato precedente aveva verificato gli otto input e l'identità dei 30 file di stato prima e dopo. La rilettura del 25 novembre 2026 rileva 11,12 GiB di RAM fisica disponibile e 12,56 GiB di commit disponibile. Le misure valgono al momento del controllo.
- **Ammissione Stream34.** Il fascicolo è ancora in attesa di ARB per il soggetto `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1`. Dopo ARB servono RQ legata alla ricevuta ARB, le impronte autenticate delle autorità e del deployment, l'enrollment di sessione e l'ammissione del coordinatore. Il controllo non ha richiesto ammissione. Nessuna prenotazione attiva o processo PixInsight risultava nella VM.
- **Incremento v571 e conoscenza v1.146.** La ricevuta di conservazione corrisponde al manifest locale. Nel repository pubblico la release rilevata non aveva asset. Il trasferimento integrale su GitHub resta da verificare, con destinazione e perimetro di distribuzione da definire tramite il canale autorizzato.

Impronta SHA-256 del delta locale `b67c3d7f0ea1cabb4dfd16e7ef505f3a1b74491cff8cffc4eae024eac78cf854`.
