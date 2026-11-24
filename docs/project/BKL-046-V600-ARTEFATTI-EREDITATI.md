# BKL-046 · Disponibilità degli artefatti ereditati da v600

L’audit su DSG-Shared abbina le **11.217 voci** del manifest v600 al riscontro storico dei byte e controlla oggi tutti i percorsi registrati. I percorsi storici H: sono risolti su H: fisico tramite la mappatura della VM. I percorsi nel profilo Codex storico sono risolti su J: fisico. Ogni posizione è stata verificata come file ordinario con dimensione identica alla rilettura storica.

| Storage e ruolo | Posizioni con dimensione conforme |
| --- | ---: |
| H: · studio | 8.165 |
| H: · mirror | 8.165 |
| H: · conoscenza | 96 |
| J: · studio | 3.052 |
| J: · mirror | 3.052 |
| **Totale** | **22.530** |

Per i 12 file di evidenza ProcessInstance, il registro requisiti v45 e la matrice v600 sono stati ricalcolati anche gli SHA-256 delle due copie registrate. Tutte le 28 letture coincidono con le impronte attese. La replica ha riutilizzato il programma, il manifest e le ricevute archiviati su H: e ha prodotto lo stesso riscontro.

Il controllo integrale delle posizioni misura disponibilità e dimensione. La nuova verifica dei byte copre i 14 artefatti ProcessInstance. Gli altri artefatti conservano il riferimento alla verifica storica. La qualifica del blocco del publisher e del recupero dopo interruzione resta aperta. Il registro autorevole punta a v600.

| Evidenza | SHA-256 |
| --- | --- |
| Programma | bd598376f149051dec9e5539791fc0ee2a18788e9e49d5eb875b867f95b4a9fe |
| Riscontro riprodotto | 1ebf7bc5afd3b1b64090fdee55320fc2d697f694afff07f31b7b956a714ee119 |
