# BKL-046 · Isolamento NTFS con token Windows ristretto

Il collaudo su DSG-Shared crea in una directory temporanea tre file sintetici con DACL esplicite. Il custode accede con il token ordinario. Il rispondente viene rappresentato da un thread con un token Windows ristretto. Il programma verifica la presenza del token sul thread prima delle aperture e ripristina il contesto al termine. [Token ristretti Windows](https://learn.microsoft.com/en-us/windows/win32/secauthz/restricted-tokens)

| Operazione con il token ristretto | Risultato |
| --- | --- |
| Leggere la richiesta | 0. Lettura riuscita e byte confrontati. |
| Aprire la chiave di confronto per lettura, scrittura, cancellazione, cambio DACL o cambio proprietario | 5 per tutte le richieste. |
| Scrivere nel file di risposta predisposto | 0. Il custode ha poi riletto i byte esatti. |
| Cancellare o sostituire i figli attraverso la directory comune | 5 per cancellazione di figli e creazione di un nuovo file. |

Il custode ha riletto la chiave prima e dopo la prova. La directory temporanea viene rimossa al termine. Le aperture sono effettuate dal sistema operativo sui file effettivi. Il collaudo usa un thread controllato nello stesso processo, quindi resta da verificare un rispondente in un processo separato, senza handle del custode, e la custodia operativa. Nessun provider è stato interrogato. Le ACL di produzione non vengono modificate.

Per ripetere usare Python 3.12 con `verifica.py <nuovo-rapporto>` da un token ordinario di DSG-Shared su una directory locale scrivibile.
