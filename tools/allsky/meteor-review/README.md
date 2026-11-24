# Revisione manuale dei nuovi candidati temporali

Componente separato, attivato con autorizzazione Owner il 24 novembre 2026. Il rilevatore temporale continua a scrivere soltanto nel proprio archivio privato e il rilevatore ordinario rimane attivo. [Procedura operativa e limiti](../../../docs/operations/allsky-meteor-shadow.md#revisione-manuale-dei-nuovi-candidati-24-novembre-2026).

`review.py` serve una API su socket Unix locale: nessuna porta TCP o rete esterna. La pagina `meteor-review.php`, installata nella radice amministrativa, richiede l’autenticazione WebUI esistente e il relativo token CSRF per le decisioni. L’accesso pubblico resta negato dalla allowlist lighttpd preesistente.

`new_after` deve essere fissato una sola volta all’attivazione autorizzata: non copiare il placeholder dell’esempio e non retrodatare il limite. Il servizio lo registra anche nello stato privato e rifiuta un valore diverso al riavvio. Sono ammessi solo timestamp di ripresa e file successivi a quel limite; lo storico precedente non è visualizzato né approvabile. Il servizio registra privatamente decisione, hash dell’immagine/metadati, autore e ora. La versione deve coincidere con quella mostrata nell’anteprima.

L’approvazione copia il JPEG senza modificarlo e genera una miniatura pubblica; le annotazioni sono soltanto nell’anteprima privata. Una immagine già presente viene conservata senza sovrascrittura. Il rifiuto conserva l’originale privato. La scelta è finale nell’interfaccia corrente: una diversa decisione richiede manutenzione esplicita. Non equivale a una classificazione astronomica certificata. Nessuna immagine reale è stata pubblicata nel collaudo.

La nuova voce nella pagina amministrativa Meteors è introdotta in `html/includes/meteors.php`. Non inserire questo codice nel flusso di acquisizione e non abilitare `publish` nel worker privato. Il contatore pubblico della notte continua a rappresentare il rilevatore ordinario: questa integrazione non somma i risultati temporali in attesa.

Dipendenze già presenti sul Raspberry: Python 3.9, OpenCV e NumPy. Il test usa esclusivamente directory temporanee e immagini sintetiche:

```bash
/home/pi/allsky/venv/bin/python test_review.py
```

Configurazione/codice/unit sono nel backup di configurazione. `/var/lib/dsg-meteor-review` e `/var/lib/dsg-meteor-shadow` restano privati e fuori dall’export pubblico; per un ripristino che conservi tutte le decisioni occorre anche un backup privato coerente dei rispettivi stati. Il solo ripristino dello snapshot di configurazione non ricrea il registro di revisione. Disattivazione: `sudo systemctl disable --now dsg-meteor-review.service`; il rilevatore ordinario e il worker privato continuano a funzionare.
