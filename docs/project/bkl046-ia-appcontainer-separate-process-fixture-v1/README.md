# BKL-046 · Processo IA di prova in AppContainer su DSG-Shared

Il collaudo crea un profilo AppContainer temporaneo con zero capability e avvia un processo figlio sospeso, senza ereditare gli handle del custode. Prima della ripresa controlla il token primario, il SID del profilo e il numero di capability. Al termine controlla il codice di uscita e rimuove il profilo. [Avvio documentato di un AppContainer](https://learn.microsoft.com/it-it/windows/win32/secauthz/implementing-an-appcontainer)

Il figlio legge la richiesta e la scrive nel file di risposta predisposto, sia con una scrittura iniziale sia in aggiunta. L'aggiunta riuscita è un controllo positivo per il tentativo successivo di leggere la chiave nello stesso file di risposta. L'apertura della chiave per lettura e il tentativo di aggiungervi dati falliscono. Il custode rilegge due copie esatte della richiesta nel file di risposta e i byte intatti della chiave.

Le ACL sono limitate ai file sintetici. Solo il file di risposta della fixture riceve un'etichetta di integrità bassa per consentire la scrittura dal contenitore. Le ACL di produzione e il gate restano invariati. Il precedente processo con token ristretto si arrestava durante l'inizializzazione. L'AppContainer completa l'intero collaudo su file. La prova lascia aperti il worker effettivo, la custodia indipendente delle chiavi, il trasporto e le unità confermative.

Per ripetere usare Python 3.12 con `verifica.py <nuovo-rapporto>` dalla sessione ordinaria di DSG-Shared. Il comando usa una directory NTFS scrivibile per i soli file di prova e rimuove gli oggetti temporanei alla fine.
