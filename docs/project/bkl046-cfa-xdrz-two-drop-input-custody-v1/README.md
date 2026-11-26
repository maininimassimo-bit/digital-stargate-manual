# Custodia degli ingressi CFA per i due depositi

Su DSG-Shared sono stati riletti i 15 ingressi interi e posati i 9 ingressi frazionari nel percorso O: previsto dal batch. La posa rilegge le impronte dello ZIP, dei singoli file e dei file già presenti. Il piano lega i 12 casi a questi ingressi e verifica che ciascun XDRZ punti ai FITS custoditi. Sono state rilette anche le impronte dei tre file PixInsight fissati dal kit e del selettore R4. Lo script PJSR è stato composto in memoria usando un contesto di prova.

Su copie NTFS, tutti i 24 ingressi sono rimasti leggibili mentre le aperture in scrittura venivano respinte. Gli stessi file sono risultati nuovamente apribili in scrittura dopo la chiusura della custodia. Un XDRZ alterato, un FITS mancante, un writer già attivo, una posa preesistente alterata e un legame padre incoerente sono stati respinti.

La custodia deve essere mantenuta dal padre fino all’uscita del processo originale. Questo collaudo verifica il componente e la posa degli ingressi. L’integrazione con il padre reale, la verifica della destinazione protetta, le revisioni e l’ammissione restano necessarie. PixInsight non è stato avviato.

Il programma `prepara.py` effettua la posa idempotente degli ingressi frazionari e il controllo in memoria. `collaudo.py` verifica la custodia su copie isolate.
