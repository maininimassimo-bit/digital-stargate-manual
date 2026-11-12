# Affiancamento privato delle meteore Allsky

Sorgenti del servizio `dsg-meteor-shadow`, autorizzato dall’Owner e attivato il 12 novembre 2026. La [guida operativa](../../../docs/operations/allsky-meteor-shadow.md) descrive perimetro, prove, backup e disattivazione.

Il worker legge copie JPEG già salvate e mantiene risultati, stato e contatori separati. Non inserire `vendor/allsky_meteordetect.py` nel flusso Allsky: questo codice è un consumatore asincrono con adattatore privato, non una seconda istanza del modulo ordinario.

## File e dipendenze

- `worker.py`: adattatore privato, registro SQLite, selezione dei nuovi file e controlli di isolamento.
- `config.example.json`: profilo senza coordinate o credenziali; sull’impianto si chiama `config.json`.
- `meteor-mask.png`: copia della maschera operativa verificata, identificata dal checksum nel profilo.
- `dsg-meteor-shadow.service`: unit con rete disabilitata, produzione in sola lettura e scritture limitate allo stato privato.
- `vendor`: modulo upstream immutato, provenienza e licenza MIT AllskyTeam.

Dipendenze già installate sul Raspberry: Python 3.9, OpenCV 4.6.0 e NumPy 1.24.4. Il profilo legge le coordinate dal settings Allsky locale per il solo controllo dell’orario notturno; non le incorpora nel repository. Il modulo viene importato con un sostituto privato di `allsky_shared`, senza accesso ai collector, al database o alle variabili dell’applicazione.

## Attivazione e manutenzione

I sorgenti qui presenti documentano l’installazione approvata. Copiare file o abilitare il modulo upstream nella WebUI non ricrea l’isolamento: servono unit, directory gestite da systemd, configurazione adattata e prove di avvio. Il worker rifiuta l’avvio se non risultano bloccate le scritture ai tre file di produzione verificati o la creazione di socket IPv4.

Una nuova maschera, soglia, versione del rilevatore o abilitazione della pubblicazione richiede una nuova valutazione e l’autorizzazione dell’Owner. Non sono previsti acquisti, servizi esterni o comandi verso dispositivi dell’osservatorio.
