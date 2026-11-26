# BKL-046 · Kit per la posa inattiva del launcher CFA

Il kit unisce l'archivio del soggetto a due depositi, l'installatore e il verificatore con il token ordinario. Il comando blocca i due esecutori Python sulle impronte fissate e compila gli stessi byte verificati. Usa il runtime installato sotto WindowsApps e rifiuta la posa dal token ordinario.

Per ripetere il collaudo, eseguire Posa-CFA-BKL046.ps1 con -Mode Validate e -ReceiptDirectory verso una cartella scrivibile già esistente, dalla PowerShell ordinaria di DSGSetup. Il collaudo scrive solo nella directory delle ricevute e nella sua replica temporanea. Per la posa reale usare -Mode InstallInactive dalla PowerShell amministrativa di DSG-Shared. Dopo la posa eseguire -Mode VerifyInstalled dalla PowerShell ordinaria usata per il lancio. Ogni passaggio produce ricevute nuove e verifica che attivazione, ammissione e avvii nativi siano assenti.

Il riscontro attesta il collaudo ordinario, il rifiuto del tentativo di posa senza elevazione e l'assenza della directory di produzione. Il kit completo è conservato su H: e sul volume VM ospitato da K:. La posa reale, le revisioni autentiche e l'ammissione R4 restano aperte.
