# BKL-051 — verifica delle sorgenti del controllo di avvio

`native_launch_control.py` è il verificatore in sola lettura del documento
`DSG_NATIVE_LINEAR_LAUNCH_CONTROL_V1` previsto dal contratto privato del
supervisore V5. È una dipendenza per la successiva pubblicazione parent V2;
non è ancora collegato al publisher o a un percorso di avvio.

Il chiamante fornisce l'impronta esternamente fissata del documento, una funzione
fidata di controllo della sessione e una funzione che attesta l'insieme esatto
delle sorgenti Python locali effettivamente caricate dal bootstrap verificato.
Quest'ultima deve verificare le identità vive e restituire modulo qualificato,
percorso, impronta e dimensione del buffer approvato. Non deve ricostruire
l'esecuzione con una scansione di file o dei moduli ordinariamente importati.
Le fixture dei test sono dichiarazioni sintetiche, prive di questa autorità.

Lo schema è chiuso e richiede una sola voce per ogni ruolo fisso di entry,
launcher, supervisore, eseguibili, quattro librerie, revisioni, consenso ed
entry/manifest del bootstrap. Le impronte scalari corrispondono alle rispettive
voci; le sorgenti parent corrispondono esattamente all'attestazione viva.
Sono respinti duplicati, ruoli estranei, alias, hard link, percorsi non canonici
e dimensioni errate. Anche un initializer vuoto deve essere dichiarato e fissato.

Il documento è limitato a 1 MiB, profondità 8 e 128 record. Ogni sorgente o
rapporto è limitato a 1 MiB, Python a 16 MiB, PixInsight a 512 MiB e la somma
dei record a 544 MiB. Le impronte sono calcolate a blocchi di 65.536 byte,
consultando il controllo fidato. Questi file non vengono copiati o eseguiti.
Il verificatore conserva l'identità del medesimo descrittore che ha fornito i
byte; `verify()` ricontrolla le identità originali, le impronte e l'attestazione
delle sorgenti. Una copia modificata del documento restituito non modifica
la fotografia interna.

## Ambito e limiti

Un esito positivo prova soltanto coerenza di questi byte e della dichiarazione
fidata ricevuta. Non autentica il consenso umano o l'indipendenza delle revisioni,
non dimostra versione o proprietà del processo e non concede avvii o chiusure.
Il futuro supervisore deve collegare i ruoli al bootstrap/runtime realmente in
uso, agli include nativi protetti, ai parametri sigillati, al proprio handle e
alla sessione originale. La guardia deve provenire da quella sessione viva.
Un callback costruito da dichiarazioni JSON non soddisfa tale requisito.

Il publisher V2 dovrà collegare questa fotografia immutabile a parent-intent,
Owner/ready e ricevuta causale, ricontrollarla durante e dopo la conservazione,
applicare i 16 MiB dei metadati parent e preservare l'incertezza per ogni errore.
Quelle integrazioni non sono ancora realizzate da questo componente. Runtime
standard e sistema operativo restano fidati; non è una sandbox contro alterazioni
ostili della memoria dello stesso utente.

Le prove usano esclusivamente file sintetici e callback simulati. Nessun
eseguibile è avviato, nessun dato astronomico è decodificato, nessun file viene
modificato dal verificatore. Rollback mediante revert dei tre nuovi file.
Milestone OPEN / NOT_VALIDATED; zero nuovi controlli reali qualificati.
