# BKL-046 · Confronto fra commit del processo e commit di sistema

Su DSG-Shared sono stati letti 16 campioni della funzione esatta di preflight Stream34 v11. Ogni lettura è racchiusa tra due chiamate a `GetPerformanceInfo`. Il margine di commit di sistema è la differenza tra limite e totale correnti, moltiplicata per la dimensione della pagina. `GlobalMemoryStatusEx` espone il commit disponibile al processo che esegue la chiamata. [MEMORYSTATUSEX](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/ns-sysinfoapi-memorystatusex) · [PERFORMANCE_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-performance_information)

In tutti i 16 campioni, memoria fisica disponibile e margine di commit sono rimasti entro gli intervalli delle letture adiacenti. I minimi osservati dal preflight erano 10,98 GiB di RAM e 12,18 GiB di commit. La misura usa il processo Python del collaudo. Il margine minimo osservato sul commit è stato di 0,18 GiB rispetto alla soglia. Il launcher deve ripetere il preflight nel proprio contesto immediatamente prima della creazione nativa.

La replica dall'archivio verifica le impronte e ricostruisce esattamente il riepilogo dei campioni salvati. Una nuova misura può produrre valori diversi. Nessuna pressione artificiale sulla memoria, richiesta di ammissione o apertura di PixInsight.
